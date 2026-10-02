"""Exercise the shipped archive and interpolated host configuration; no paid API calls."""
import asyncio
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

from mcp import Client, StdioServerParameters


async def main(artifact):
    with tempfile.TemporaryDirectory(prefix="bpj-bundle-check-") as folder:
        root = Path(folder)
        bundle = root / "bundle"
        with zipfile.ZipFile(artifact) as archive:
            assert all(not Path(p).is_absolute() and ".." not in Path(p).parts for p in archive.namelist())
            archive.extractall(bundle)
        manifest = json.loads((bundle / "manifest.json").read_text())
        expected = json.loads((Path(__file__).resolve().parents[1] / "distribution/release.json").read_text())
        assert manifest["version"] == expected["version"], "Test the current release artifact"
        config = manifest["server"]["mcp_config"]
        data = root / "data"
        data.mkdir()
        shutil.copyfile(bundle / "src/jev_decision_gate/demo-issues.json", data / "issues.json")
        values = {"data_root": str(data), "allow_jev": "false", "max_calls": "20", "api_key": ""}
        env = {key: values[value.removeprefix("${user_config.").removesuffix("}")]
               for key, value in config["env"].items()}
        env["UV_NO_PROGRESS"] = "1"
        command = shutil.which(config["command"])
        assert command, "uv must be installed to test the UV bundle"
        args = [v.replace("${__dirname}", str(bundle)) for v in config["args"]]
        # Start the unmodified archive with the same command/variables a compatible host uses.
        results = []
        for mode in ("auto", "legacy"):
            params = StdioServerParameters(command=command, args=args, env=env)
            async with Client(params, mode=mode, read_timeout_seconds=120) as client:
                assert client.server_info and client.server_info.name == "Jev Decision Gate", client.server_info
                assert client.server_info.version == manifest["version"], client.server_info
                names = sorted(t.name for t in (await client.list_tools()).tools)
                assert names == ["calibrate_gate", "calibrate_issue_gate", "evaluate_gate",
                                 "evaluate_issue_gate", "route_batch", "triage_issues"]
                report = await client.call_tool("triage_issues", {"issues_file": "issues.json"})
                assert not report.is_error, report
                value = report.structured_content
                assert value["summary"]["model_calls"] == 0 and len(value["rows"]) == 12
                assert all(r["action"] == "review" for r in value["rows"])
                for request in ({"issues_file": "issues.json", "provider": "jev"},
                                {"issues_file": "../outside.json"}):
                    rejected = await client.call_tool("triage_issues", request)
                    assert rejected.is_error
                results.append({"mode": mode, "protocol": client.protocol_version, "tools": len(names),
                                "rules_issues": 12, "model_calls": 0, "status": "passed"})
        for bad in ({"BPJ_ALLOW_JEV": "yes"}, {"BPJ_ALLOW_JEV": "true"},
                    {"BPJ_MAX_CALLS": "201"}, {"BPJ_MAX_CALLS": "1.5"}, {"BPJ_DATA_ROOT": ""}):
            process = subprocess.run([command, *args], env={**os.environ, **env, **bad},
                                     capture_output=True, text=True, timeout=30)
            assert process.returncode != 0 and not process.stdout, bad
        print(json.dumps({"evidence": "BUNDLE INSTALLATION TEST, SYNTHETIC RULES ONLY", "checks": results,
                          "invalid_startup_configurations_rejected": 5}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", type=Path)
    asyncio.run(main(parser.parse_args().artifact.resolve()))
