---
name: bpj-decision-gate
description: "Triage GitHub Issue JSON with a local rules baseline or an authorized Jev call; calibrate acceptance and evaluate held-out quality. Also audit caller-supplied LLM routing scores and costs through Python or local MCP. Use for BPJ Decision Gate, Issue triage, selective acceptance, fallback evaluation, or MCP integration."
---

# BPJ Decision Gate

Use bundled deterministic code for evaluation. Distinguish Issue inference from generic scored-trace replay. Never invent labels, costs, model results, installed host connections or savings.

## Issue workflow

1. Read [issue-triage.md](references/issue-triage.md). Obtain authorized Issue JSON, provider choice and desired output location. Prefer the offline rules baseline first. Do not fetch private repositories or send their contents merely because the skill is installed.
2. Resolve scripts relative to this file. For a credential-free demonstration, run `python3 <skill>/scripts/triage_cli.py demo --out <new-report.json>`. Explicitly identify the 12 cases as synthetic and the provider as rules, not Jev.
3. Run real inputs with `python3 <skill>/scripts/triage_cli.py triage <issues.json> --provider rules --out <new-report.json>`. Choose Jev only when external processing and model calls are authorized; use `--provider jev` with `TYPESAFE_API_KEY` in the process environment. Never ask the user to paste a key into chat. Explain that selected title/body go to TypeSafe and may incur fees. Expected labels are never sent.
4. Require independently reviewed labels and frozen model/question/score versions before `calibrate`. Use a disjoint report with `evaluate`. Do not tune on the test set. A tiny demo cannot certify production acceptance. No policy means review; failed inference means review; insufficient calibration disables acceptance and avoids inference calls.
5. Report joint accuracy, coverage, accepted error, failure count and provider-reported usage separately. Selected-label probabilities are scores, not guaranteed correctness. An input-price estimate is not an invoice. Manual-review costs and total savings remain unknown unless separately measured.
6. Do not apply labels, comment on Issues, close tickets or execute recommendations. Keep raw private inputs and reports outside public repositories.

## Generic routing audit

Read [data-contract.md](references/data-contract.md). Supply independent calibration/test traces, frozen scope, actual booleans for both route outcomes and consistent costs. Run `python3 <skill>/scripts/risk_gate.py <calibration.json> <test.json> --scope <scope>`. For mechanics only, `scripts/demo.py --out <working-directory>` creates synthetic traces. Clearly label simulation and report quality regressions alongside cost changes.

## MCP

Read [mcp-setup.md](references/mcp-setup.md). Discover connected tools first. If no host is connected, use the CLI and accurately describe that route. Launch `scripts/mcp_server.py` in a Python environment with `mcp==2.2.0`. Jev is off by default; `--allow-jev` is a startup opt-in. Use a trusted local `--data-root`; paths must be relative and stay inside it. Policies last only for the current process. Returned reports may enter the host model's context.

## Limits

- Statistical bounds cover accepted predictions for a frozen pipeline under i.i.d. sampling and correct labels, not future drift, duplicate content or reviewer quality.
- Do not claim live Jev verification from a mocked contract test or synthetic fixture. Installation and discovery do not prove effective savings or retained users.
- Treat this as an independent early developer tool, not Jev's model, an official TypeSafe product, a hosted service or a multi-tenant router.
- Avoid public deployment, automatic purchases and hidden telemetry. Changing questions, labels, scoring or language distribution requires new evaluation.
