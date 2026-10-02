# v0.3.1 release notes

Jev Decision Gate now uses one public name across the repository, Skill, MCP server, Python distribution, README examples and animated walkthrough.

- Skill: `jev-decision-gate`; install with `npx skills add f-tiger/jev-decision-gate --skill jev-decision-gate`.
- CLI: `jev-gate` and `jev-gate-mcp`.
- Python: `jev_decision_gate`; distribution metadata: `jev-decision-gate`.
- MCP server display: **Jev Decision Gate**; Registry name remains `io.github.f-tiger/jev-decision-gate`.
- BPJ remains the independent publisher. This is not an official TypeSafe product.

## Existing installations

The new package retains `bpj-gate`, `bpj-gate-mcp` and `bpj_decision_gate` imports as compatibility entry points to the same implementation. New examples use Jev names. Use a fresh virtual environment for the update, or uninstall the old `bpj-decision-gate` Python distribution before installing the new project into the existing environment; neither distribution has been published to PyPI.

For a Skill installed under the old `bpj-decision-gate` name, install the new name, verify a rules demo, then remove the old Skill through your host to avoid duplicate instructions. The maintainer's existing personal Skill is updated in place. Previous GitHub release artifacts remain immutable.

## Scope and evidence

Issue triage, six MCP tools, the rules baseline, Jev contract and acceptance method are unchanged. The rename does not establish new quality, token or cost results. Live Jev evaluation remains pending. [Verification](verification.json) and [publication status](distribution.md) record completed checks and active versions.

v0.3.0 was the first public preview, with a GitHub MCPB release and official Registry entry. Version 0.3.1 is [published](https://github.com/f-tiger/jev-decision-gate/releases/tag/v0.3.1) and [registered](https://registry.modelcontextprotocol.io/v0.1/servers/io.github.f-tiger%2Fjev-decision-gate/versions/0.3.1); public asset checksums and the active Registry record have been verified.
