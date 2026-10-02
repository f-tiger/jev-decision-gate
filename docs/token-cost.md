# Token volume, token price, and actual savings

The README animation compares general LLM APIs, direct Jev and our MCP on the same Issue-triage goal. It separates existing workflow features, official list prices, hypothetical arithmetic, and real offline rules output. **No live Jev-versus-LLM comparison has been run.** The illustration is not a screen recording of an existing dashboard.

## The MCP contribution

Our MCP provides the existing batch triage, task/usage validation, independent calibration, held-out evaluation and accept/review workflow. It uses the same Jev model pricing as direct Jev. It does not provide a measured extra token reduction over direct Jev; agent-host tool descriptions, arguments, results and reasoning may add tokens and costs. See the [three-way comparison](why-use-mcp.md).

## The price comparison

Snapshot date: **2026-10-02**. USD per million tokens, standard synchronous API input/output prices, excluding cache and batch discounts.

| Model | Input / 1M | Output / 1M | Input price divided by Jev's |
|---|---:|---:|---:|
| Claude Fable 5.1 | $10 | $50 | 238.10× |
| Claude Haiku 4.5 | $1 | $5 | 23.81× |
| Jev 1.13 | $0.042 | $0 | 1× |

Sources: [TypeSafe model pricing](https://docs.typesafe.ai/models), [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing). The saved [snapshot](../examples/pricing-snapshot.json) is dated, not a live price feed.

The illustration gives both providers **the same hypothetical 1,000,000 billable input tokens**. Thus its token-volume ratio is **1×** and its Fable/Jev input-price ratio is **238.10×**. This is equivalent to a 99.58% reduction in the illustrated input charge, not a measured reduction in tokens, total bills or error rates.

Jev output is free to bill. It can still have nonzero `usage.output_tokens`; the [official API examples](https://docs.typesafe.ai/api) show both usage fields. Actual providers may tokenize identical text differently. Questions, instructions, schema overhead, reasoning, cache and batching also change the bill. A short JSON-mode LLM baseline is fairer than forcing the baseline to generate a long explanation.

Fable is the expensive reference behind the 238× headline, not the only relevant alternative. Haiku's input-price ratio is 23.81×. Fable cache reads are $0.25/M: an all-cache-read price-only comparison would be 5.95× before cache writes, misses and output. These are price comparisons, not assertions that the models deliver equal quality or equivalent general capabilities.

## Reproduce the numbers

From the repository root, Python 3.11+; no dependencies or API key:

```bash
python tools/price_scenario.py --input-tokens 1000000 --fallback-fraction 0.1
```

For illustration only, suppose Jev processes all input and an additional 10% of the original input-token budget goes to Fable:

```text
Fable alone, input only = 1,000,000 × $10 / 1,000,000 = $10
Jev input              = 1,000,000 × $0.042 / 1,000,000 = $0.042
Extra Fable input      =   100,000 × $10 / 1,000,000 = $1
Combined input charge  = $1.042
Input-cost ratio       = $10 / $1.042 = 9.5969...
```

Ten percent refers to **input-token volume**, not necessarily 10% of issues. Output charges, retries, human review, infrastructure and taxes are excluded. There is no measured 90% acceptance rate. The current review action does not invoke Fable. At 100% fallback, the illustration is more expensive than Fable alone: $10.042 versus $10. The calculator keeps live results null.

## What the case actually proves

The trial frame summarizes all 12 original English synthetic fixtures. Eight match all three expected fields; all 12 remain in review because the gate is uncalibrated. [Inspect every row](assets/demo-report.json), including the failures. Chinese captions translate the example; they are not a Chinese-model benchmark.

The offline rules demo has zero backend/provider model calls; an agent-host model may still consume tokens to invoke it and read its results. Comparing that zero to a paid model and advertising infinite savings would be misleading. The public-price illustration and rules demo deliberately have different evidence labels.

## What is needed for an actual savings claim

Run the same independently labeled issues and fixed taxonomy through Jev and a short structured-output LLM baseline. Record provider-returned input/output usage, cached and reasoning usage where available, every attempt, failures, wall time, exact models and dated prices. Keep per-issue results so token counts can be paired to identical tasks.

Calibrate on one split and evaluate on a separate, representative held-out split. Report joint label accuracy, accepted coverage, errors among accepted items, abstentions and fallback outcomes together with cost. Include the costs of calibration, failed requests, fallback and review; amortize one-time work explicitly. Do not select a prompt or threshold on the final test set. The shipped 12 examples demonstrate mechanics and are too small to establish customer savings.

Report both `(baseline tokens / Jev tokens)` and `(baseline total cost / full workflow cost)` with their own denominators. Only publish a savings claim if quality meets a predeclared requirement and usage is sufficiently complete. An unknown bill is not zero. No API credentials are currently configured for this comparison.

## Rebuild the animation

Install Pillow in a development environment, plus DejaVu Sans and Noto Sans CJK fonts. Fonts are not bundled. Set `DEMO_CJK_FONT` to a local CJK font if needed:

```bash
python -m pip install Pillow
python tools/render_readme_demo.py
```

This reruns the offline baseline and reads the price snapshot; it never calls paid models. It creates English and Chinese looping GIFs, static posters, `demo-report.json` and `price-scenario.json` in `docs/assets/`. The GIFs include evidence labels throughout and the README provides static alternatives. Update the snapshot and captions together when prices change.

## 中文口径

三栏动画先说明 LLM API、直接 Jev 与我们的 MCP 的工作流差异。价格页的 238 倍是 **Fable 5.1 与 Jev 的未缓存输入单价之比**，不是我们实测减少了 238 倍 token。动画使用双方各 100 万输入 token 的假设；Jev 输出免费，但不应把它写成零输出 token。10% 回退也是情景假设，不是当前自动接受率。项目的真实模型效果、token 用量与端到端费用仍待配对实测。复现价格计算无需密钥，运行 Jev 需要用户自己的 TypeSafe 密钥。
