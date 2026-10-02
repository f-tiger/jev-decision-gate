"""Wire-level stdio checks using synthetic fixtures, no model/API calls."""
import asyncio
import json
import sys
import tempfile
from pathlib import Path

from mcp import Client, StdioServerParameters


def write_fixture(root, name, rows):
    (root / name).write_text(json.dumps(rows), encoding="utf-8")


async def check_mode(root, mode):
    params = StdioServerParameters(
        command=sys.executable,
        args=[str(Path(__file__).with_name("mcp_server.py")), "--data-root", str(root)])
    async with Client(params, mode=mode, read_timeout_seconds=20) as client:
        assert client.server_info and client.server_info.name == "Jev Decision Gate", client.server_info
        names = sorted(t.name for t in (await client.list_tools()).tools)
        assert names == ["calibrate_gate", "calibrate_issue_gate", "evaluate_gate", "evaluate_issue_gate", "route_batch", "triage_issues"], names
        fitted = await client.call_tool("calibrate_gate", {
            "calibration_file": "calibration.json", "scope": "synthetic-v1"})
        assert not fitted.is_error, fitted
        fitted = fitted.structured_content
        assert fitted["active"] and fitted["gate"]["threshold"] == .99, fitted
        assert "calibration_ids" not in fitted["gate"]
        policy_id = fitted["policy_id"]
        evaluation = await client.call_tool("evaluate_gate", {
            "policy_id": policy_id, "test_file": "test.json"})
        assert not evaluation.is_error, evaluation
        metrics = evaluation.structured_content["metrics"]
        assert metrics["total"] == 3 and metrics["accepted"] == 2, metrics
        assert metrics["accepted_errors"] == 1, metrics
        assert abs(metrics["observed_cost"] - 2.1) < 1e-10, metrics
        routed = await client.call_tool("route_batch", {
            "policy_id": policy_id, "requests_file": "requests.json"})
        assert not routed.is_error, routed
        result = routed.structured_content
        assert [r["reason"] for r in result["decisions"]] == [
            "threshold_passed", "below_threshold", "scope_mismatch", "ineligible"]
        assert [r["action"] for r in result["decisions"]] == [
            "accept_cheap", "fallback", "fallback", "fallback"]
        assert result["executed_actions"] is False
        errors = [
            ("evaluate_gate", {"policy_id": policy_id, "test_file": "calibration.json"}),
            ("route_batch", {"policy_id": "missing", "requests_file": "requests.json"}),
            ("route_batch", {"policy_id": policy_id, "requests_file": "invalid.json"}),
            ("route_batch", {"policy_id": policy_id, "requests_file": "oversized.json"}),
            ("calibrate_gate", {"calibration_file": "../outside.json", "scope": "synthetic-v1"}),
            ("calibrate_gate", {"calibration_file": str(root / "calibration.json"), "scope": "synthetic-v1"}),
            ("calibrate_gate", {"calibration_file": "escape.json", "scope": "synthetic-v1"}),
        ]
        for name, args in errors:
            rejected = await client.call_tool(name, args)
            assert rejected.is_error, (name, args, rejected)
        disabled = await client.call_tool("calibrate_gate", {
            "calibration_file": "tiny.json", "scope": "synthetic-v1"})
        assert not disabled.is_error and not disabled.structured_content["active"]
        bypass = await client.call_tool("route_batch", {
            "policy_id": disabled.structured_content["policy_id"], "requests_file": "requests.json"})
        assert not bypass.is_error
        assert all(r["reason"] == "disabled_gate" for r in bypass.structured_content["decisions"])
        triaged = await client.call_tool("triage_issues", {"issues_file": "issues.json"})
        assert not triaged.is_error, triaged
        issue_report = triaged.structured_content
        assert issue_report["summary"]["model_calls"] == 0
        assert all(r["action"] == "review" for r in issue_report["rows"])
        write_fixture(root, "issue-report.json", issue_report)
        issue_fit = await client.call_tool("calibrate_issue_gate", {"report_file": "issue-report.json"})
        assert not issue_fit.is_error and not issue_fit.structured_content["active"]
        issue_policy = issue_fit.structured_content["policy_id"]
        for item in issue_report["rows"]:
            item["id"] = "held-" + item["id"]
        write_fixture(root, "issue-held.json", issue_report)
        issue_test = await client.call_tool("evaluate_issue_gate", {"policy_id": issue_policy, "report_file": "issue-held.json"})
        assert not issue_test.is_error and issue_test.structured_content["coverage"] == 0
        for tool, arguments in [
            ("triage_issues", {"issues_file": "issues.json", "provider": "jev"}),
            ("triage_issues", {"issues_file": "../outside.json"}),
            ("evaluate_issue_gate", {"policy_id": issue_policy, "report_file": "issue-report.json"}),
        ]:
            rejected = await client.call_tool(tool, arguments)
            assert rejected.is_error, rejected
        return {"mode": mode, "protocol": client.protocol_version, "tools": names,
                "status": "passed", "rejected_invalid_calls": len(errors) + 3}


async def main():
    with tempfile.TemporaryDirectory(prefix="bpj-mcp-check-") as folder:
        root = Path(folder) / "data"
        root.mkdir()
        row = {"scope": "synthetic-v1", "score": .99, "eligible": True,
               "cheap_correct": True, "fallback_correct": True,
               "cheap_cost": .1, "fallback_cost": 1.5, "overhead_cost": .1}
        calibration = [dict(row, id=f"cal-{i}") for i in range(600)]
        write_fixture(root, "calibration.json", calibration)
        write_fixture(root, "tiny.json", calibration[:1])
        write_fixture(root, "test.json", [dict(row, id="test-1"),
                       dict(row, id="test-2", cheap_correct=False),
                       dict(row, id="test-3", score=.2)])
        request = {"scope": "synthetic-v1", "score": .999, "eligible": True}
        requests = [dict(request, id="a"), dict(request, id="b", score=.2),
                    dict(request, id="c", scope="changed-v2"),
                    dict(request, id="d", eligible=False)]
        write_fixture(root, "requests.json", requests)
        write_fixture(root, "invalid.json", [dict(request, id="bad", score=True)])
        write_fixture(root, "oversized.json", [dict(request, id=f"b-{i}") for i in range(201)])
        write_fixture(root.parent, "outside.json", calibration)
        (root / "escape.json").symlink_to(root.parent / "outside.json")
        from importlib.resources import files
        write_fixture(root, "issues.json", json.loads(files("jev_decision_gate").joinpath("demo-issues.json").read_text()))
        results = []
        for mode in ("auto", "legacy"):
            results.append(await check_mode(root, mode))
        print(json.dumps({"evidence": "SYNTHETIC INTEROPERABILITY TEST ONLY", "checks": results}, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
