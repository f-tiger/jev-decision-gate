# BPJ Decision Gate: developer first release

Date: 2026-10-02. Owner request: complete the Jev-inspired open-source MCP/Skill product and developer cases. This is the explicit product experiment authorization; it does not establish market demand or authorize outreach, spending or new accounts.

## Buyer and evidence

Initial user: a repository maintainer or small engineering team processing ambiguous GitHub Issues. Buyer hypothesis: the engineering lead who owns repeated triage work. No public evidence establishes that most Jev customers are programmers; its API, SDK and coding-agent documentation establish developer distribution, not a customer census.

BPJ has existing coding/API/agent categories, which offer a relevant entry point. This is not proof of demand for this product. The initial use case is a founder-selected hypothesis; customer validation remains outstanding. Public TypeSafe cookbooks and competing Jev MCP/routers show supply and usage patterns; paid demand and issue-triage lift remain unvalidated. Research sources: https://docs.typesafe.ai/introduction/coding-agents, https://docs.typesafe.ai/api, https://docs.typesafe.ai/models, https://github.com/TokenTrim/jev-routing-experiment. The last experiment is a reason to keep a rules baseline, not proof of general Jev superiority.

## Scope

Free MIT Python package in this independent repository, CLI, local stdio MCP, installable Skill guidance. One original synthetic Issue fixture. Deterministic baseline plus actual TypeSafe HTTP adapter with pinned model. No GitHub writes. No source code, logs, private issues or model credentials collected by BPJ. Jev mode sends explicitly selected issue title/body to TypeSafe; offline rules mode has no network calls.

Independent calibration split, fixed score mapping and threshold grid, exact one-sided binomial bound with a multiple-testing correction. Held-out evaluation rejects ID overlap. Insufficient evidence disables acceptance. Report provider usage, error counts and quality separately; manual-review cost is unknown. Never call toy examples customer results, confidence correctness, reduced tokens verified savings, or this integration a reproduction of Jev's model.

## Distribution and commercial test

Owner correction: publish as an independent public `f-tiger/jev-decision-gate` repository, because `agi-site` may become private. Do not publish product code in the site monorepo. README links to the existing BPJ developer page. Proposed bilingual landing content is included under `docs/` for later website integration; it is not claimed live. No new domain, cron, unsolicited posts or messages.

Free value: run, inspect, integrate and evaluate locally. Possible paid value: repeated hosted evaluation, team policy history and drift review. No paid Decision Gate SKU, checkout or hosted service is available in this release. Existing BPJ paid products are not represented as including it.

Evidence to collect before monetization: five independent developer installs, two teams returning with real labeled evaluation reports, and one concrete request for recurring service. These are proposed decision criteria, not achieved results. Stars, forks, page visits, install-link clicks, actual successful runs, qualified inquiries and paid orders must be separate. No telemetry is built into the package; adoption is self-reported unless independently verified. Reassess after 28 days of actual distribution, without changing criteria after results are known.

## Acceptance and adversarial checks

1. Installation and offline demo run from the packaged wheel, with no credentials.
2. Contract tests validate the TypeSafe request/response shape and cover malformed/failed responses, label leakage, path containment and missing credentials. Live Jev verification explicitly pending without a key.
3. MCP tools initialize and return structured output using the supported SDK protocols.
4. Calibration/test separation, taxonomy/model scope binding and failure-to-review behavior are verified.
5. Independent repository can be cloned and installed without access to agi-site. Website publication and real customer performance remain separate verification stages.
6. Round one challenges integration and data boundaries; round two challenges reproducibility, useful baseline and truthful claims. Both are self-review, not independent model reviews.
