Jev Decision Gate v0.3.1 unifies the Skill, MCP server, CLI, Python package and documentation under the Jev name. Independent MIT project by BPJ.

- Six tools for Issue triage, independent calibration, held-out evaluation and routing recommendations.
- New commands: `jev-gate` and `jev-gate-mcp`; legacy `bpj-gate` commands and Python imports remain compatible in the source package.
- Download the `.mcpb` asset and import it into a host supporting MCPB 0.4 and UV. Select the directory containing your Issue JSON. Hosts may download Python and locked dependencies on first use.
- Jev is off by default; rules mode needs no provider key. Paid Jev calls require explicit opt-in and protected host configuration.
- Source and conventional Python stdio setup remain available for other MCP hosts.
- `SHA256SUMS` verifies the bundle; `server.json` describes its MCP Registry distribution.

Developer preview: synthetic tests and rules output do not establish live Jev quality or token savings. No live model comparison has been run. The server does not edit GitHub Issues.

Skill installation for compatible agents:

```bash
npx skills add f-tiger/jev-decision-gate --skill jev-decision-gate
```

[Installation guide](https://github.com/f-tiger/jev-decision-gate/blob/main/docs/mcp.md) · [Tryout report](https://github.com/f-tiger/jev-decision-gate/issues/new?template=tryout.yml)
