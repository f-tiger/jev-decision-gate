# Issue triage v0.3.1

Input: a JSON array of 1..200 objects with unique string `id`, nonempty `title` and optional string `body`. Optional `expected` must include all three fields: `kind` in bug/feature/question/unknown; `module` in auth/api/ui/docs/unknown; `information` in sufficient/missing. Expected labels must be independently reviewed, not invented to match output.

Jev pins `jev-1.13.0`, batching three independent Choice questions per issue. It sends only title/body. Scope includes provider, model, question contract and score revision. The score is the minimum selected-label probability, not joint correctness probability. Rules scores are heuristics. Unknown kind/module or missing information makes a prediction ineligible for acceptance.

CLI: `python3 <skill>/scripts/triage_cli.py` followed by:

```text
demo --out fresh-demo.json --export-issues fresh-issues.json
triage issues.json --provider rules --out fresh-report.json
triage issues.json --provider jev --max-calls 20 --out fresh-jev.json
calibrate calibration-report.json --out fresh-policy.json
evaluate fresh-policy.json held-out-report.json --out fresh-evaluation.json
triage new-issues.json --provider jev --policy fresh-policy.json --out fresh-decisions.json
```

Outputs must not already exist; parent directories must exist. Optional `--input-usd-per-million` uses a caller-verified current input price. Default 20 requests per invocation, configurable to 200. No automatic retries; failed usage may be unknown. Exit 2 indicates failure or a saved report with provider errors. Inspect it before claiming success.

Reports omit title/body but retain IDs, labels and optionally expected labels; they are not anonymous. Keep private reports private. Files are bounded to 8 MiB, issue text to 16,000 UTF-8 bytes, payloads to 24,000 bytes, responses to 1 MiB. No silent truncation.

The 12 bundled cases are synthetic. Low sample size normally disables acceptance. Do not loosen thresholds to force a passing demo. Calibration/test IDs must be disjoint; semantic deduplication and sampling validity remain the data owner's responsibility.

References: https://docs.typesafe.ai/api and https://docs.typesafe.ai/models. Missing credentials block live Jev verification, not local evaluation. Do not request keys for rules mode.
