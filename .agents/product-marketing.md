# Product Marketing Context

**Document version:** v6
**Last updated:** 2026-10-02

## Product overview
An independent open-source Issue triage and selective acceptance tool, exposed as CLI, Python SDK, MCP and Skill. Local MIT core; optional TypeSafe API fees paid by the user. No hosted Decision Gate subscription or checkout is offered.

## Target audience and personas
Hypothesis: repository maintainers and small engineering teams with repeated triage. User/champion: developer or maintainer. Potential buyer: engineering lead responsible for workflow cost and quality. Their job is to reduce repeated classification work while retaining ambiguous cases for review. This is a target segment, not a verified census of Jev customers.

## Problem and alternatives
Unstructured issues require classification, module assignment and missing-information checks. Actual time/cost has not been measured with customers. Alternatives include manual labels, deterministic rules, an existing large-model workflow and other Jev adapters. A rules baseline may already be sufficient; compare it before adding a model. No claim that competitors lack evaluation.

## Differentiation to test
A small, reproducible developer case; explicit abstention; independent calibration; costs and quality reported together; usable without a BPJ account. The advantage is a hypothesis until real users prefer it. Typed output is not correctness.

## Objections and switching
“Rules are enough”: run and compare the baseline. “Can I trust confidence?”: calibrate on reviewed independent data. “Must I upload private code?”: only selected issue text goes to TypeSafe in Jev mode; rules are local. Anti-persona: a user needing autonomous repository changes, general coding, guaranteed correctness or a hosted production SLA.

Push: repeated triage. Pull: inspectable decisions and review control. Habit: existing labels and scripts. Anxiety: wrong routing, API costs and private data. These are product hypotheses, not customer quotations.

## Language and voice
Use “triage”, “review”, “held-out evaluation”, “provider-reported usage”. Avoid “Jev clone”, “official”, “guaranteed savings”, “production proven”, unsupported savings percentages or fake badges. Direct, technical, candid. There are no customer testimonials or logos to cite.

## Proof and goals
Code tests and synthetic demos can establish mechanics. They cannot establish live Jev quality, retained customers or revenue. See docs/verification.json for current evidence. Desired conversion: successful local run, then a returning team with labeled results, then a specific recurring-service request. Keep visits, clone/download intent, confirmed installs, repeated use, inquiries and payments separate.

## Distribution experiment
Lead with the three-way LLM API / direct Jev / our MCP workflow comparison, followed by dated underlying-model prices, a reproducible Issue example and installation. Keep the MCP value proposition separate from Jev's model pricing; no incremental MCP token savings have been measured. The 238× Fable/Jev input-price ratio is not a measured token or workflow saving; include a cheaper-model reference and fallback assumptions. The GIF and snapshot are dated 2026-10-02. Prioritize Jev directories, compatible Skill hosts and developer communities; two directory applications are pending review; social posts remain drafts. See docs/growth-plan.zh-CN.md and docs/launch-kit.md.

## Changelog
- v6 (2026-10-02) — Brought Skill installation and Claude Code/Codex/Cursor entry points to the README top; prepared a social card and repository profile; confirmed Jev Users indexing. Keep detailed validation status in technical documents and public copy focused on shipped workflow value.
- v5 (2026-10-02) — Reframed the README animation around why to install our MCP, comparing the same task across three integration choices and separating model price from workflow value.
- v4 (2026-10-02) — Unified public name, Skill, CLI, MCP and Python package under Jev Decision Gate; legacy commands/imports remain compatibility aliases.
- v3 (2026-10-02) — Added cost-led discovery, evidence boundaries, developer installation funnel and a measurable distribution experiment after ecosystem research.
- v2 (2026-10-02) — Public repository named jev-decision-gate at owner request; legacy BPJ identifiers were retained at that stage; superseded by v4.
- v1 (2026-10-02) — Initial developer-first positioning; separate independent repository, offline evidence and possible future paid service.
