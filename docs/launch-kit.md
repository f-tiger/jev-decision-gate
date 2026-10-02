# Launch copy and evidence links

Prepared 2026-10-02. **Social posts remain drafts. Two directory applications have been submitted; see [distribution status](distribution.md) for receipts and review status.** Select only channels where the maintainer participates and the current rules allow this format. This project was developed with AI assistance. It is independent of TypeSafe.

## The short pitch

Jev Decision Gate is an open-source Python/MCP/Skill tool for GitHub Issue triage. Try an offline rules baseline, optionally connect Jev, and independently calibrate which predictions can be accepted. Uncertain items stay in review. No issue edits or account signup are required for the local demo.

## X: cost-led version

> $10 vs $0.042 per million input tokens: Fable 5.1 and Jev's standard uncached prices. That's a 238× price gap—not 238× fewer tokens.
>
> I built an open-source Issue-triage MCP + Skill to explore what survives in a real workflow. The README compares a bare LLM API, direct Jev and our ready-made MCP workflow. Direct Jev gets the same model price; our extra token savings are unmeasured. Cost math and an offline case are included.
>
> Try it: https://github.com/f-tiger/jev-decision-gate

Attach `docs/assets/token-cost-en.gif`. Keep the price qualifier in the post when cropping a frame. The author should review and personalize the wording before posting.

## X / community: workflow-led version (primary)

> Your issue classifier can return valid JSON and still be wrong.
>
> Direct Jev gives you typed judgments. Jev Decision Gate adds batch Issue input, response checks, acceptance calibration and review recommendations in six MCP tools. Install the workflow, try it without a key, then bring your own labeled cases. MIT.
>
> https://github.com/f-tiger/jev-decision-gate

Lead with the workflow version so users can see why to install this project. Test cost-led framing in a separate, comparable window. A single post's outcome is not a randomized A/B test.

## Show HN

Suggested title: **Show HN: Jev Issue triage with calibrated acceptance and an offline demo**

Submission URL: https://github.com/f-tiger/jev-decision-gate

Author comment draft:

> I wanted a small way to test whether typed decisions fit repeated issue triage. This developer preview predicts kind, module and whether information is sufficient, then keeps uncertain decisions for review. It never changes GitHub issues.
>
> You can try the rules baseline without an account or key. The README animation compares bare LLM and Jev APIs with the included MCP workflow, then separates dated model prices from our added features; it does not claim live savings. Its actual offline fixture has 8/12 jointly correct predictions and all 12 in review; live Jev-versus-LLM results remain pending. The code includes the Jev HTTP adapter and a separate calibration/evaluation workflow.
>
> AI assisted with the implementation. I'm interested in installation blockers and examples where the taxonomy or abstention policy does not fit your workflow.

Use only when the author can discuss the implementation and respond. [Show HN rules](https://news.ycombinator.com/showhn.html) favor something runnable, easy to try, substantive and personally understood. They prohibit asking friends for votes. Do not present a routine documentation update as a new Show HN product.

## Jev-directory entry

> [Jev Decision Gate](https://github.com/f-tiger/jev-decision-gate) — Python CLI, local MCP and Skill for Issue kind/module/information decisions using Jev, with independent acceptance calibration and an offline rules baseline; live Jev measurements pending.

Evidence packet:

- Implementation: `src/jev_decision_gate/triage.py` — actual request construction, HTTP adapter, response validation and review outcomes.
- Runnable checks: `tests/test_triage.py`, `tests/smoke_mcp.py`, public Actions run.
- Walkthrough: `README.md`, `docs/assets/token-cost-en.gif`.
- Boundaries and prices: `docs/token-cost.md`, `docs/verification.json`.
- Authorship disclosure: substantially AI-assisted implementation.

For yibie/awesome-jev, follow its one-entry/one-category rule and supply runnable implementation evidence. For jevbest.com, its Submit Project link opens a review form asking for a public repo and Jev evidence. Neither acceptance nor publication is guaranteed; do not claim a listing before it appears.

## 中文短文案

> 直接调用 Jev 能得到结构化判断，批量接入、结果检查和复核策略仍需要开发。Jev Decision Gate 把这些做成六个现成 MCP 工具，也可通过 Skill 安装。
>
> README 用“大模型／直接 Jev／我们的 MCP”三栏演示区别。无需密钥先跑本地规则，再用自己的数据校准。直接 Jev 和我们的 MCP 使用相同的模型单价；MCP 额外节省多少 token 仍待实测。
>
> https://github.com/f-tiger/jev-decision-gate

## Metadata for maintainers

Suggested About description: `Issue triage with Jev, calibrated acceptance, and transparent token-cost comparisons. Python, local MCP and Skill. Offline demo included.`

Suggested topics: `jev`, `typesafe-ai`, `mcp`, `agent-skills`, `issue-triage`, `llm-evaluation`, `developer-tools`, `python`.

Suggested social preview: the static English three-way comparison poster, keeping all three columns and the workflow distinction legible. About/topics/social-preview settings are proposals; this update does not claim they were applied.
