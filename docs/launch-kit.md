# Launch copy and evidence links

Prepared 2026-10-02. **Drafts, not posted or submitted.** Select only channels where the maintainer participates and the current rules allow this format. This project was developed with AI assistance. It is independent of TypeSafe.

## The short pitch

Jev Decision Gate is an open-source Python/MCP/Skill tool for GitHub Issue triage. Try an offline rules baseline, optionally connect Jev, and independently calibrate which predictions can be accepted. Uncertain items stay in review. No issue edits or account signup are required for the local demo.

## X: cost-led version

> $10 vs $0.042 per million input tokens: Fable 5.1 and Jev's standard uncached prices. That's a 238× price gap—not 238× fewer tokens.
>
> I built an open-source Issue-triage MCP + Skill to explore what survives in a real workflow. The README has the price math, an offline case, and a fallback scenario. Live Jev savings are still unmeasured.
>
> Try it: https://github.com/f-tiger/jev-decision-gate

Attach `docs/assets/token-cost-en.gif`. Keep the price qualifier in the post when cropping a frame. The author should review and personalize the wording before posting.

## X / community: workflow-led alternative

> Your issue classifier can return valid JSON and still be wrong.
>
> Jev Decision Gate keeps classification, missing-information checks and acceptance policy separate. Run the offline baseline, inspect the failures, then bring your own labeled cases. Python, MCP and Skill; MIT.
>
> https://github.com/f-tiger/jev-decision-gate

Compare this framing with the cost-led version in separate, comparable windows. A single post's outcome is not a randomized A/B test.

## Show HN

Suggested title: **Show HN: Jev Issue triage with calibrated acceptance and an offline demo**

Submission URL: https://github.com/f-tiger/jev-decision-gate

Author comment draft:

> I wanted a small way to test whether typed decisions fit repeated issue triage. This developer preview predicts kind, module and whether information is sufficient, then keeps uncertain decisions for review. It never changes GitHub issues.
>
> You can try the rules baseline without an account or key. The README animation compares dated list prices, not live savings. Its actual offline fixture has 8/12 jointly correct predictions and all 12 in review; live Jev-versus-LLM results remain pending. The code includes the Jev HTTP adapter and a separate calibration/evaluation workflow.
>
> AI assisted with the implementation. I'm interested in installation blockers and examples where the taxonomy or abstention policy does not fit your workflow.

Use only when the author can discuss the implementation and respond. [Show HN rules](https://news.ycombinator.com/showhn.html) favor something runnable, easy to try, substantive and personally understood. They prohibit asking friends for votes. Do not present a routine documentation update as a new Show HN product.

## Jev-directory entry

> [Jev Decision Gate](https://github.com/f-tiger/jev-decision-gate) — Python CLI, local MCP and Skill for Issue kind/module/information decisions using Jev, with independent acceptance calibration and an offline rules baseline; live Jev measurements pending.

Evidence packet:

- Implementation: `src/bpj_decision_gate/triage.py` — actual request construction, HTTP adapter, response validation and review outcomes.
- Runnable checks: `tests/test_triage.py`, `tests/smoke_mcp.py`, public Actions run.
- Walkthrough: `README.md`, `docs/assets/token-cost-en.gif`.
- Boundaries and prices: `docs/token-cost.md`, `docs/verification.json`.
- Authorship disclosure: substantially AI-assisted implementation.

For yibie/awesome-jev, follow its one-entry/one-category rule and supply runnable implementation evidence. For jevbest.com, its Submit Project link opens a review form asking for a public repo and Jev evidence. Neither acceptance nor publication is guaranteed; do not claim a listing before it appears.

## 中文短文案

> 同样 100 万输入 token，Fable 5.1 是 $10，Jev 是 $0.042，公开输入单价相差约 238 倍。真正接入后能省多少，还取决于判断质量、回退、缓存和实际用量。
>
> 我们做了 Jev Decision Gate：用 Issue 分类做一个可复现的 MCP / Skill 案例，README 动画展示单价、规则结果和回退测算。无需密钥可以先跑离线版；真实 Jev 节省仍待实测。
>
> https://github.com/f-tiger/jev-decision-gate

## Metadata for maintainers

Suggested About description: `Issue triage with Jev, calibrated acceptance, and transparent token-cost comparisons. Python, local MCP and Skill. Offline demo included.`

Suggested topics: `jev`, `typesafe-ai`, `mcp`, `agent-skills`, `issue-triage`, `llm-evaluation`, `developer-tools`, `python`.

Suggested social preview: the static English price poster, cropped only if the model names, price scope and date remain legible. About/topics/social-preview settings are proposals; this update does not claim they were applied.
