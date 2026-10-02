# Contributing

Install `.[mcp]`, run unit tests and `python tests/smoke_mcp.py`. No key is needed for tests. Please include the exact package version, model version (if applicable), sanitized reproduction, expected result and actual result.

Do not submit private source code, logs, customer records or credentials. State the license and provenance of any dataset. Clearly distinguish synthetic fixtures, mocked API contracts, provider replays and newly collected live results.

Keep the model, questions and threshold grid frozen before evaluating new data. Changes to a question, taxonomy, eligibility or score require a scope/revision change and new calibration. Preserve the rules baseline and unknown/review outcomes.

This repository welcomes issue-triage contributions first. CI-log reduction and Skill routing are future experiments, not current features. No contribution should add automatic issue comments/labels, paid calls in CI or telemetry without an explicit product decision.
