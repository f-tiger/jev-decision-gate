"""Build a deterministic, source-only UV MCPB and its Registry metadata."""
import hashlib
import json
import re
import tomllib
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = "https://github.com/f-tiger/jev-decision-gate"
NAME = "io.github.f-tiger/jev-decision-gate"


def main():
    version = json.loads((ROOT / "distribution/release.json").read_text())["version"]
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise SystemExit("Release version must be X.Y.Z")
    manifest = json.loads((ROOT / "distribution/manifest.json").read_text())
    versions = [manifest["version"]]
    for path in ("pyproject.toml", "distribution/pyproject.toml"):
        versions.append(tomllib.loads((ROOT / path).read_text())["project"]["version"])
    if any(v != version for v in versions):
        raise SystemExit("Release, package and bundle versions must match")
    files = {
        "manifest.json": ROOT / "distribution/manifest.json",
        "pyproject.toml": ROOT / "distribution/pyproject.toml",
        "uv.lock": ROOT / "distribution/uv.lock",
        "server/main.py": ROOT / "distribution/main.py",
        "LICENSE": ROOT / "LICENSE",
        "README.md": ROOT / "distribution/README.md",
    }
    for name in ("__init__.py", "cli.py", "contracts.py", "decision_engine.py",
                 "io.py", "mcp_server.py", "risk_gate.py", "triage.py",
                 "demo-issues.json"):
        files[f"src/jev_decision_gate/{name}"] = ROOT / "src/jev_decision_gate" / name
    output = ROOT / "dist"
    output.mkdir(exist_ok=True)
    artifact = output / f"jev-decision-gate-{version}.mcpb"
    with zipfile.ZipFile(artifact, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, path in sorted(files.items()):
            if path.is_symlink() or not path.is_file():
                raise SystemExit(f"Missing or symlinked bundle input: {path.relative_to(ROOT)}")
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes(), compresslevel=9)
    digest = hashlib.sha256(artifact.read_bytes()).hexdigest()
    server = {
        "$schema": "https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json",
        "name": NAME,
        "title": "Jev Decision Gate by BPJ",
        "description": "Local Issue triage with optional Jev judgments and calibrated acceptance gates.",
        "version": version,
        "repository": {"url": REPO, "source": "github"},
        "packages": [{
            "registryType": "mcpb",
            "identifier": f"{REPO}/releases/download/v{version}/{artifact.name}",
            "fileSha256": digest,
            "transport": {"type": "stdio"},
        }],
    }
    (output / "server.json").write_text(json.dumps(server, indent=2) + "\n", encoding="utf-8")
    (output / "SHA256SUMS").write_text(f"{digest}  {artifact.name}\n", encoding="utf-8")
    print(json.dumps({"artifact": str(artifact), "sha256": digest, "version": version}))


if __name__ == "__main__":
    main()
