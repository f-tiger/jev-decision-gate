# Discovery setup for maintainers

The public product is **Jev Decision Gate**. Lead with Issue triage, the ready-made review workflow and the no-key demo. Public README copy focuses on installation and features; detailed methodology remains in the linked evaluation documents.

## Repository profile

Ready-to-apply values are in [`distribution/repository-profile.json`](../distribution/repository-profile.json). These are repository settings, not settings GitHub applies merely because a JSON file is committed.

**About description**

Jev-powered GitHub Issue triage for coding agents. MCP server, Agent Skill and Python CLI with batch checks, calibrated review and a no-key local demo.

**Topics**

`jev`, `typesafe-ai`, `mcp`, `mcp-server`, `agent-skills`, `issue-triage`, `developer-tools`, `python`

**Website**

`https://baipiaoji.com/en/developers?utm_source=github&utm_medium=about&utm_campaign=jev_decision_gate`

**Social preview**

Upload [`social-preview.png`](assets/social-preview.png) in GitHub's repository Settings → Social preview. It is 1280 × 640 and under 1 MB. Rebuild with `python tools/render_social_preview.py` (Pillow and DejaVu fonts).

A maintainer who already has an authenticated GitHub CLI with the necessary repository permissions can apply the text fields with:

```bash
gh repo edit f-tiger/jev-decision-gate --description 'Jev-powered GitHub Issue triage for coding agents. MCP server, Agent Skill and Python CLI with batch checks, calibrated review and a no-key local demo.' --homepage 'https://baipiaoji.com/en/developers?utm_source=github&utm_medium=about&utm_campaign=jev_decision_gate' --add-topic jev,typesafe-ai,mcp,mcp-server,agent-skills,issue-triage,developer-tools,python
```

## Smithery publication packet

- Requested publisher name: `f-tiger/jev-decision-gate` (confirm ownership of the Smithery namespace when signing in).
- Display name: **Jev Decision Gate**.
- Summary: use the About description above.
- Repository: <https://github.com/f-tiger/jev-decision-gate>.
- Type: **local stdio / MCPB bundle**.
- Public artifact: [jev-decision-gate-0.3.1.mcpb](https://github.com/f-tiger/jev-decision-gate/releases/download/v0.3.1/jev-decision-gate-0.3.1.mcpb).
- SHA256: `58586a72fa7bc9b43894f671faaba35b39b7cabcdeda6ae5d1aa764bd404925e`.
- Required configuration: existing Issue JSON directory.
- Optional configuration: enable Jev (default false), protected TypeSafe key, per-invocation call limit.
- Runtime: MCPB manifest 0.4 with UV; verify marketplace runtime support during upload.
- First-run instructions: [MCP setup](mcp.md); choose the data directory and try rules mode.

Smithery's publishing guide supports uploading a pre-built local MCPB. Once authenticated with Smithery and with namespace ownership confirmed, its documented CLI flow is:

```bash
smithery mcp publish ./jev-decision-gate-0.3.1.mcpb -n f-tiger/jev-decision-gate
```

Download the public artifact and verify its hash before publishing. No private source, model key or Issue data belongs in the bundle. Record the resulting public listing URL only after its page and install configuration are verified. A prepared packet is not a submitted or accepted listing.

## Existing discovery receipts

- Official MCP Registry: [active v0.3.1 record](https://registry.modelcontextprotocol.io/v0.1/servers/io.github.f-tiger%2Fjev-decision-gate/versions/0.3.1).
- Jev Users: [newest-project listing](https://jevusers.com/?sort=newest) was observed linking to the exact `f-tiger/jev-decision-gate` repository on 2026-10-02. This confirms an indexed entry, not endorsement or user adoption; its displayed counts can lag GitHub.
- Existing Awesome submissions remain tracked in [distribution status](distribution.md); update those applications rather than creating duplicates.

## References

Checked 2026-10-02:

- [GitHub repository topics](https://docs.github.com/articles/classifying-your-repository-with-topics)
- [GitHub social previews](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview)
- [Smithery publishing](https://smithery.ai/docs/build/publish)
- [Skills directory FAQ](https://skills.sh/docs/faq)
