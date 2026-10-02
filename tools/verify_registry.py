"""Verify generated schema, public asset and exact Registry version without credentials."""
import argparse
import hashlib
import json
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def get(url):
    request = urllib.request.Request(url, headers={"User-Agent": "jev-decision-gate-release-check/0.3.1"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--schema-only", action="store_true")
    modes.add_argument("--asset-only", action="store_true")
    modes.add_argument("--registry", action="store_true")
    args = parser.parse_args()
    expected = json.loads((ROOT / "dist/server.json").read_text())
    package = expected["packages"][0]
    if args.schema_only:
        import jsonschema
        schema = json.loads(get(expected["$schema"]))
        jsonschema.validate(expected, schema)
        print("Registry server.json passes the official JSON Schema")
    elif args.asset_only:
        digest = hashlib.sha256(get(package["identifier"])).hexdigest()
        if digest != package["fileSha256"]:
            raise SystemExit("Public release asset SHA256 does not match server.json")
        print("Unauthenticated public release download matches the recorded SHA256")
    else:
        name = urllib.parse.quote(expected["name"], safe="")
        version = urllib.parse.quote(expected["version"], safe="")
        url = f"https://registry.modelcontextprotocol.io/v0.1/servers/{name}/versions/{version}"
        try:
            payload = json.loads(get(url))
        except urllib.error.HTTPError as error:
            if error.code == 404:
                raise SystemExit("This version is not registered yet") from None
            raise
        actual = payload["server"]
        for field in ("name", "version", "packages"):
            if actual[field] != expected[field]:
                raise SystemExit(f"Registry {field} differs from the verified release")
        status = payload.get("_meta", {}).get("io.modelcontextprotocol.registry/official", {}).get("status")
        if status != "active":
            raise SystemExit(f"Registry version is not active: {status}")
        print(json.dumps({"status": "registered", "name": actual["name"], "version": actual["version"],
                          "url": url, "sha256": package["fileSha256"]}, indent=2))


if __name__ == "__main__":
    main()
