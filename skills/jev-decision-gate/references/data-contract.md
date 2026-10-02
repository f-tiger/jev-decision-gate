# Data contract and interpretation

Calibration and test files are nonempty JSON arrays. Each row contains:

| Field | Requirement |
|---|---|
| `id` | Unique nonempty string; calibration and test IDs must not overlap |
| `scope` | Frozen model + prompt + score mapping + workload/language identifier |
| `score` | Finite number between 0 and 1 supplied by a predictor; not automatically calibrated probability |
| `eligible` | Boolean; false always uses fallback |
| `cheap_correct` | Boolean, verified cheap prediction correctness |
| `fallback_correct` | Boolean, verified fallback correctness |
| `cheap_cost` | Nonnegative finite cost of cheap inference |
| `fallback_cost` | Nonnegative finite cost of fallback inference |
| `overhead_cost` | Nonnegative finite incremental routing/transport/processing cost |

Use the same currency or normalized cost unit throughout. Supply observed costs or explicitly labeled estimates. Keep quality labels from the target workload; model agreement alone is not ground truth. Deduplicate underlying examples as well as IDs. The program detects repeated IDs, not semantic duplication.

Prediction-only batch rows contain `id`, `scope`, `score`, `eligible`; no correctness labels are required. IDs must be 1..128 characters. Scope mismatch, ineligible requests, low scores or an inactive gate cause fallback recommendations. No model invocation or downstream action occurs.

The fixed candidate grid is 0.50, 0.60, 0.70, 0.80, 0.85, 0.90, 0.93, 0.95, 0.97, 0.99. One-sided exact binomial bounds use Bonferroni adjustment over the grid. Choose the passing candidate accepting the most calibration rows; break ties by higher threshold. This is an implementation of established statistics, not a novel statistical method. Its confidence statement assumes independent identically distributed data and a pre-frozen scorer and grid; repeated adaptive reuse invalidates it.

For an active in-scope eligible request, replay charges cheap inference even if it then falls back. Every request incurs overhead. Inactive or out-of-scope policies bypass cheap inference. Fallback-only baseline uses each row's fallback cost and correctness. Report selective and overall error separately. Replay does not measure live latency or drift. Fallback-only baseline must represent the same tasks and evaluation protocol.

MCP bounds: at most 5,000 calibration/test rows, 200 prediction rows, 8 MiB per file, 32 policies per process. Files must be `.json` under the trusted configured data root; symlinks resolving outside are rejected. This is a convenience boundary for trusted local files, not a sandbox against a hostile local process changing files concurrently. Registry state is lost on restart. `policy_id` is a reference, not an authorization token.
