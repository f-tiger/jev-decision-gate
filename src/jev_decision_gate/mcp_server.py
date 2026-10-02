"""Local stdio MCP server. Jev access is explicitly enabled at startup."""
import argparse
import hashlib
import json
from pathlib import Path
from typing import Any
from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from .decision_engine import DecisionEngine
from .contracts import CalibrationResult, EvaluationResult, RoutingResult
from .io import read_json
from .triage import MODEL, calibrate_report, evaluate_report, read_gate, triage


def create_server(data_root, allow_jev=False, max_calls=20):
    engine = DecisionEngine(data_root)
    server = MCPServer("Jev Decision Gate", version="0.3.1", instructions=(
        "Read-only local triage and scored-trace evaluation. Relative JSON paths stay in the configured data root. "
        "Jev mode sends selected issue title/body to TypeSafe and may incur API costs; requires startup opt-in. "
        "No GitHub writes, no hosted service, no guaranteed savings. Uncalibrated or failed judgments require review. "
        "Policies live in this process. Never present synthetic examples as measured Jev performance."))

    def invoke(operation, *args, **kwargs):
        try:
            return operation(*args, **kwargs)
        except ValueError as exc:
            raise ToolError(str(exc)) from None
        except OSError:
            raise ToolError("Could not read a JSON file within the configured data root") from None

    @server.tool(structured_output=True)
    def calibrate_gate(calibration_file: str, scope: str, max_error: float = .05, delta: float = .05) -> CalibrationResult:
        """Calibrate caller-supplied scored traces; costs and truth labels must come from the caller."""
        return invoke(engine.calibrate, calibration_file, scope, max_error, delta)

    @server.tool(structured_output=True)
    def evaluate_gate(policy_id: str, test_file: str) -> EvaluationResult:
        """Replay disjoint scored traces against fallback-only using caller-supplied costs and outcomes."""
        return invoke(engine.evaluate, policy_id, test_file)

    @server.tool(structured_output=True)
    def route_batch(policy_id: str, requests_file: str) -> RoutingResult:
        """Recommend acceptance or fallback from supplied scores; execute no downstream actions."""
        return invoke(engine.route, policy_id, requests_file)

    @server.tool(structured_output=True)
    def triage_issues(issues_file: str, provider: str = "rules", policy_id: str | None = None,
                      input_usd_per_million: float | None = None) -> dict[str, Any]:
        """Triage at most 200 local issues. Jev requires --allow-jev, a key, and stays within startup max_calls."""
        if provider == "jev" and not allow_jev:
            raise ToolError("Jev is disabled; restart with --allow-jev only for authorized outbound model calls")
        rows = invoke(read_json, issues_file, engine.root)
        gate = invoke(engine.policy, policy_id) if policy_id else None
        return invoke(triage, rows, provider=provider, model=MODEL, gate=gate,
                      max_calls=max_calls, input_usd_per_million=input_usd_per_million)

    @server.tool(structured_output=True)
    def calibrate_issue_gate(report_file: str, max_error: float = .05, delta: float = .05) -> dict[str, Any]:
        """Fit an Issue-specific policy from an independent fully labeled triage report saved locally."""
        report = invoke(read_json, report_file, engine.root)
        result = invoke(calibrate_report, report, max_error, delta)
        gate = invoke(read_gate, result)
        policy_id = "issue_" + hashlib.sha256(json.dumps(result, sort_keys=True).encode()).hexdigest()[:24]
        with engine.lock:
            if policy_id not in engine.policies and len(engine.policies) >= 32:
                raise ToolError("32 policies loaded; restart to clear")
            engine.policies[policy_id] = gate
        public_gate = {k: v for k, v in result["gate"].items() if k != "calibration_ids"}
        return {"policy_id": policy_id, "active": gate.threshold is not None,
                "gate": public_gate, "note": result["note"]}

    @server.tool(structured_output=True)
    def evaluate_issue_gate(policy_id: str, report_file: str) -> dict[str, Any]:
        """Evaluate joint Issue correctness and acceptance coverage on a disjoint labeled report."""
        return invoke(evaluate_report, invoke(engine.policy, policy_id), invoke(read_json, report_file, engine.root))

    return server


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--allow-jev", action="store_true")
    parser.add_argument("--max-calls", type=int, choices=range(1, 201), default=20, metavar="1..200")
    args = parser.parse_args()
    create_server(args.data_root, args.allow_jev, args.max_calls).run(transport="stdio")


if __name__ == "__main__":
    main()
