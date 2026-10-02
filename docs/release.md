# v0.3.0 release notes

First independent developer preview of BPJ Decision Gate.

- Issue triage: kind, module and information sufficiency.
- Deterministic offline baseline and version-pinned Jev HTTP adapter.
- Independent acceptance calibration and disjoint held-out evaluation.
- Python CLI/SDK, six local MCP tools and a bundled Skill.
- Bilingual instructions and 12 original synthetic cases.
- Model usage and failures recorded without inventing net savings.

Current limits: no live Jev run without a locally supplied key; no hosted service; no automatic issue edits; no model training or Jev reproduction; no PyPI/MCP Registry listing. The website introduction is prepared but not deployed. See verification.json for actual local test evidence. The first [GitHub Actions run](https://github.com/f-tiger/jev-decision-gate/actions/runs/36955430515) passed on Python 3.11 and 3.12, including 24 unit tests, both MCP protocol modes and wheel builds. Public cloning, installation and the offline demo also passed.

## Maintainer publication

Published: public [`f-tiger/jev-decision-gate`](https://github.com/f-tiger/jev-decision-gate), standalone, MIT. Description: “Issue triage with Jev, independent acceptance gates, and local MCP/Skills. Rules baseline included.” Suggested topics: `jev`, `mcp`, `agent-skills`, `issue-triage`, `selective-prediction`, `python`. These are proposed settings, not claimed to be applied.

Source is available on main. A version tag/GitHub Release has not yet been created. PyPI and MCP Registry publication require separate account permissions; neither is necessary for a Git-based install. Do not publish keys, private issues or reports. Do not promise a hosted/paid product from this release.
