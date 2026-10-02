# Jev Decision Gate · by BPJ

**Triage GitHub Issues with Jev. Keep uncertain decisions in the review queue.**

[中文](README.zh-CN.md) · [MCP setup](docs/mcp.md) · [Evaluation method](docs/evaluation.md) · [BPJ developer tools](https://baipiaoji.com/en/developers?utm_source=github&utm_medium=readme&utm_campaign=decision_gate)

An independent MIT-licensed Python tool for repository maintainers. Run a rules baseline, optionally call TypeSafe's Jev, and calibrate which suggestions may be accepted. The first case predicts **issue kind, affected module and information sufficiency**. It never edits issues, applies labels, posts comments or closes tickets.

Version **0.3.0**, early developer preview. This is an integration and statistical gate, **not Jev's model, training algorithm, or an official TypeSafe product**. Live Jev measurements are pending. The bundled cases are original synthetic examples, not customer outcomes or a representative benchmark.

## Run in two minutes

Python 3.11+:

```bash
git clone https://github.com/f-tiger/jev-decision-gate.git
cd jev-decision-gate
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install '.[mcp]'
bpj-gate demo --out demo-report.json --export-issues demo-issues.json
```

The demo runs locally without keys or network requests. It produces real output from a deliberately simple rules baseline. All items initially require review. Keep the report: compare on your own labels before choosing a provider. Commands refuse to overwrite existing output files.

## Call Jev on selected issues

Set `TYPESAFE_API_KEY` through your local environment or secret manager. **Do not paste a key into an issue, model chat, repository or MCP configuration committed to Git.** Jev mode sends selected title/body text to `https://api.typesafe.ai/v1/systemone`; BPJ receives nothing.

```bash
bpj-gate triage demo-issues.json --provider jev --max-calls 12 --out jev-report.json
```

The default pins `jev-1.13.0`. One request per issue batches three independent questions against the same issue. There are no automatic retries. Failure returns a review recommendation and records unknown usage rather than assuming zero cost. Exit code 2 means an input failure or a saved report with provider failures; inspect stderr and the report.

To estimate the cost of provider-reported input tokens, explicitly add `--input-usd-per-million YOUR_CURRENT_PRICE`. Output is an estimate, not an invoice. Failed calls may be billed without reported usage. Human review and fallback model costs are not measured, so the triage report leaves savings unset.

## Bring your own cases

```json
[
  {
    "id": "myrepo-123",
    "title": "Login fails after session expiry",
    "body": "Steps, environment, actual behavior and expected behavior...",
    "expected": {"kind": "bug", "module": "auth", "information": "sufficient"}
  }
]
```

`expected` is optional at inference time and required for calibration/evaluation. It is never sent to Jev. Use human-reviewed labels. Fixed labels in v0.3.0:

| Field | Labels |
|---|---|
| `kind` | `bug`, `feature`, `question`, `unknown` |
| `module` | `auth`, `api`, `ui`, `docs`, `unknown` |
| `information` | `sufficient`, `missing` |

This taxonomy is intentionally narrow. Repositories whose modules do not fit should customize the question contract and recalibrate. No claim is made about accuracy in Chinese or other languages; evaluate the language you actually use.

## Calibrate, then test separately

Run inference on independently labeled calibration and test files, then:

```bash
bpj-gate calibrate calibration-report.json --out policy.json
bpj-gate evaluate policy.json held-out-report.json --out evaluation.json
bpj-gate triage new-issues.json --provider jev --policy policy.json --out decisions.json
```

The model, taxonomy and score mapping must be frozen before calibration. IDs must be disjoint across calibration and evaluation; semantic duplicates must also be removed by the dataset owner. Small samples or high error disable the gate. A disabled policy skips model calls and sends every item to review. Policy scope mismatches fail before inference.

The fixed threshold search uses an exact one-sided binomial bound with Bonferroni correction. The bound concerns errors among accepted predictions under i.i.d. sampling. It does not cover distribution drift, adversarial input or reviewer accuracy. [Read the assumptions and score definition](docs/evaluation.md).

## MCP, Skill and Python

```bash
bpj-gate-mcp --data-root /absolute/path/to/authorized-json
```

Jev is disabled by default in MCP. Add `--allow-jev --max-calls 20` at startup only when outbound model calls are authorized and the process can read your key. [Six tools and client configuration](docs/mcp.md).

Use the installable instructions under [`skills/bpj-decision-gate/`](skills/bpj-decision-gate/) in a compatible Skill host. Installation locations differ by host; this repository does not silently install or modify your host. The bundled Skill can run the same Python implementation without downloading project code during a task.

```python
from bpj_decision_gate.triage import triage
report = triage([{"id": "example-1", "title": "API error", "body": "Please investigate"}])
```

## What is free? What is paid?

The package, MCP server, Skill, fixtures and evaluator are free under MIT. Jev usage is billed separately by TypeSafe according to your account. BPJ does not sell a hosted Decision Gate service in this preview. Recurring evaluation, policy history and team review are possible future paid features; demand and delivery have not been validated.

See [BPJ developer tools](https://baipiaoji.com/en/developers?utm_source=github&utm_medium=readme&utm_campaign=decision_gate) for the existing website. No private source code or keys are required to browse it. The package has no telemetry; website visits and GitHub stars do not prove successful installations.

## Verify and contribute

```bash
python -m unittest discover -s tests -v
python tests/smoke_mcp.py
```

Tests use mocks and synthetic fixtures, never paid APIs. [Verification status](docs/verification.json), [security boundaries](SECURITY.md), [contributing](CONTRIBUTING.md) and [roadmap](docs/roadmap.md). Contributions are welcome for independently labeled, redistributable cases, failure reports and controlled comparisons with a rules baseline. Keep private issues and credentials out of public contributions.

Protocol reference: [TypeSafe API](https://docs.typesafe.ai/api), [models](https://docs.typesafe.ai/models), [MCP Python SDK](https://py.sdk.modelcontextprotocol.io/). Jev references describe interoperability; no affiliation is implied.
