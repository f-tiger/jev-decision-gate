# What the gate does and does not establish

The algorithm is established selective prediction assembled into a small auditable implementation. It is not a new foundation model or a reproduction of proprietary Jev training.

1. Freeze provider, model version, question wording, label descriptions, eligibility and score mapping.
2. If fitting any score transformation, use a training split separate from the gate calibration split.
3. Collect an independent, representative calibration split with human-reviewed labels.
4. Try a fixed grid: .5, .6, .7, .8, .85, .9, .93, .95, .97, .99.
5. Compute a one-sided exact Clopper–Pearson upper error bound for each accepted subset using delta divided by grid size.
6. Choose the passing threshold with highest coverage, breaking ties toward the higher threshold. If none passes, disable acceptance.
7. Report performance on a further held-out test split. Do not tune on its labels and still call it held-out.

Default maximum selective error is .05; default delta is .05. Under a frozen pipeline, representative i.i.d. observations and correct labels, the simultaneous bound supports selection across this fixed grid. These assumptions are not verified by the software. Duplicates, repeated tuning, label errors, temporal drift and correlated examples can invalidate the interpretation. Detecting duplicate IDs is only a guard, not proof of independent sampling.

## Issue score and correctness

The Jev score is the minimum of the returned probabilities for the three selected labels. This is a ranking statistic, **not** a calibrated probability that all three labels are correct. The API's `confidence` field is not used as correctness. Joint correctness means kind, module and information labels all equal the reviewed expected labels.

Eligibility requires a known kind, a known module and `information=sufficient`. The rules baseline uses fixed heuristic scores (.75/.25), not model probabilities. The scope digest includes the entire question contract and its revision; provider and pinned model also participate. A changed contract cannot silently reuse an old policy.

## Comparison protocol for a useful claim

Compare at least: manual triage, the cheap rules baseline, Jev with review gating, and any existing large-model workflow. Use the same untouched test cases and fixed acceptance criteria. Record label accuracy by field and jointly, acceptance coverage, accepted error, failure rate, total latency, input/output usage, retries, human intervention and downstream costs.

This preview reports only the measurements it has. A price estimate uses caller-supplied input price; current Jev documentation says output tokens are free, but verify your provider/account terms. Failure usage may be unknown. A report without fallback/manual-review costs cannot establish net savings. Token reduction alone also cannot establish better economics when caching, latency and labor differ.

## Bundled evidence

`examples/issues.synthetic.json` has 12 original toy examples, including unclear input and an instruction-injection attempt. These demonstrate wiring and expose simplistic rules; they cannot select production thresholds or substantiate customer claims. `docs/verification.json` records code tests separately from live-provider verification.

Source references checked 2026-10-02: [TypeSafe API](https://docs.typesafe.ai/api), [models](https://docs.typesafe.ai/models), [confidence](https://docs.typesafe.ai/primitives/choice). For statistical background see Clopper & Pearson (1934), *The Use of Confidence or Fiducial Limits Illustrated in the Case of the Binomial*, Biometrika 26(4), 404–413, DOI [10.1093/biomet/26.4.404](https://doi.org/10.1093/biomet/26.4.404).
