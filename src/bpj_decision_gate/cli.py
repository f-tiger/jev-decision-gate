"""Command-line entry points; no GitHub mutations or hidden telemetry."""
import argparse
import json
import sys
from importlib.resources import files
from pathlib import Path
from .io import read_json, write_json
from .triage import MODEL, triage, calibrate_report, read_gate, evaluate_report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    demo = commands.add_parser("demo", help="Run the bundled synthetic cases with the offline rules baseline")
    demo.add_argument("--out", required=True)
    demo.add_argument("--export-issues", help="Write the synthetic input for later provider comparison")
    run = commands.add_parser("triage", help="Suggest issue triage; Jev sends title/body to TypeSafe")
    run.add_argument("issues")
    run.add_argument("--provider", choices=["rules", "jev"], default="rules")
    run.add_argument("--model", default=MODEL)
    run.add_argument("--policy")
    run.add_argument("--max-calls", type=int, default=20)
    run.add_argument("--input-usd-per-million", type=float)
    run.add_argument("--out", required=True)
    fit = commands.add_parser("calibrate", help="Fit on an independent fully labeled triage report")
    fit.add_argument("report")
    fit.add_argument("--max-error", type=float, default=.05)
    fit.add_argument("--delta", type=float, default=.05)
    fit.add_argument("--out", required=True)
    test = commands.add_parser("evaluate", help="Evaluate a policy on a disjoint labeled triage report")
    test.add_argument("policy")
    test.add_argument("report")
    test.add_argument("--out", required=True)
    args = parser.parse_args()
    try:
        # Reject existing outputs before model calls to avoid paying for an unusable run.
        if Path(args.out).exists():
            raise ValueError("output already exists; use a fresh output path")
        if not Path(args.out).parent.is_dir():
            raise ValueError("output parent directory must already exist")
        if args.command == "demo":
            issues = json.loads(files("bpj_decision_gate").joinpath("demo-issues.json").read_text())
            if args.export_issues:
                write_json(args.export_issues, issues)
            result = triage(issues)
            result["dataset"] = "bpj-original-synthetic-issues-v1; toy demonstration, not a benchmark"
        elif args.command == "triage":
            result = triage(read_json(args.issues), provider=args.provider, model=args.model,
                            gate=read_gate(read_json(args.policy)) if args.policy else None,
                            max_calls=args.max_calls, input_usd_per_million=args.input_usd_per_million)
        elif args.command == "calibrate":
            result = calibrate_report(read_json(args.report), args.max_error, args.delta)
        else:
            result = evaluate_report(read_gate(read_json(args.policy)), read_json(args.report))
        write_json(args.out, result)
        print(json.dumps({"output": args.out, "summary": result.get("summary", result.get("note", "complete"))}, ensure_ascii=False))
        if args.command == "triage" and any(r["error"] for r in result["rows"]):
            return 2  # Partial report is saved. Failed items always need review.
        return 0
    except (ValueError, OSError) as exc:
        print(f"bpj-gate: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
