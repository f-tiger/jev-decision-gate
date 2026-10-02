# Distribution and submission status

Checked 2026-10-02. Public names are unified as Jev Decision Gate in v0.3.1; see [upgrade notes](release.md) for compatibility. Installation, Registry registration and curated directory acceptance are different outcomes.

| Channel | Status | Evidence / next step |
|---|---|---|
| Public source | Available | [Repository](https://github.com/f-tiger/jev-decision-gate) |
| Skills CLI | jev-decision-gate v0.3.1 public install and rules demo verified | `npx skills add f-tiger/jev-decision-gate --skill jev-decision-gate` |
| skills.sh listing | Not confirmed | Listing/discovery is influenced by genuine CLI installs; no installs or rankings are fabricated |
| GitHub MCPB release | Published v0.3.1 preview | [Release and downloads](https://github.com/f-tiger/jev-decision-gate/releases/tag/v0.3.1); public download SHA256 verified |
| Official MCP Registry | Registered; active v0.3.1 | [Exact Registry record](https://registry.modelcontextprotocol.io/v0.1/servers/io.github.f-tiger%2Fjev-decision-gate/versions/0.3.1); name/version/asset hash verified |
| heyjunpenn/awesome-jev (jevbest) | Submitted; awaiting review | [Submission #72](https://github.com/heyjunpenn/awesome-jev/issues/72) |
| hellogumbo/awesome-jev | Submitted; awaiting review | [Submission #152](https://github.com/hellogumbo/awesome-jev/issues/152) |
| yibie/awesome-jev | Not submitted | Requires a category-file PR and regenerated README |
| UV quick start | Pinned v0.3.1 launch published | [Claude Code](clients/claude-code.md), [Codex](clients/codex.md), [Cursor](clients/cursor.md); see [checks](discovery-verification.json) |
| Jev Users | Indexed entry observed 2026-10-02 | [Newest list](https://jevusers.com/?sort=newest) links to the exact f-tiger repository; not an adoption metric |
| GitHub About / Topics / social preview | Profile text and 1280×640 image prepared; settings not applied | [Ready-to-apply profile and image](discovery-setup.md); current connector lacks repository-settings writes |
| Smithery | Publication packet prepared; not submitted | [Existing MCPB and submission details](discovery-setup.md); publisher authentication is required |

[Successful automated publication](https://github.com/f-tiger/jev-decision-gate/actions/runs/36959163942): verification → public release → OIDC registration → Registry readback.

## Release maintenance

The workflow runs tests, checks the Skill's code parity, validates the MCPB manifest and official Registry JSON Schema, and exercises the actual archive in modern and legacy protocol modes. Only then does it publish a GitHub preview release. A separate job with `id-token: write` registers it through GitHub OIDC; no long-lived Registry token, PyPI account or container registry is required. The release-writing permission is restricted to its own job.

Change `distribution/release.json` on `main` to deliberately trigger a release, or run the workflow manually; `v*` tags also trigger it. Versions in the root package, bundle manifest and bundle pyproject must match. Refresh `distribution/uv.lock` when dependencies change. Use a **new version** for changed artifacts; retries require identical existing release bytes and do not overwrite them.

The MCPB builder includes only allowlisted source, the launcher, manifest, lockfile, license and bundle guide. Private data, reports, environment files and local environments are excluded. The archive is deterministic for the same inputs/build toolchain. The Registry step downloads the public asset and checks its SHA256, publishes, then reads back the exact active name/version/package record.

## Honest distribution metrics

Track successful installs, successful rules runs, live evaluations with user-authorized data, and repeat usage separately. Stars, directory entries and website clicks are discovery signals, not evidence of model quality or savings. This project does not emit telemetry. Test installs disable the third-party Skills CLI telemetry and are not claimed as independent adoption.

Live Jev comparisons are still unmeasured. Price ratios in the README are arithmetic from dated list prices, not token-volume reductions or measured total-cost savings.

## Sources

- [Official MCP Registry: GitHub Actions/OIDC](https://modelcontextprotocol.io/registry/github-actions)
- [Official MCP Registry: MCPB packages](https://modelcontextprotocol.io/registry/package-types)
- [MCPB manifest specification](https://github.com/modelcontextprotocol/mcpb/blob/main/MANIFEST.md)
- [Skills FAQ](https://skills.sh/docs/faq)
- [heyjunpenn/awesome-jev](https://github.com/heyjunpenn/awesome-jev)
- [hellogumbo submission guidelines](https://github.com/hellogumbo/awesome-jev/blob/main/CONTRIBUTING.md)
- [yibie submission guidelines](https://github.com/yibie/awesome-jev/blob/main/CONTRIBUTING.md)
