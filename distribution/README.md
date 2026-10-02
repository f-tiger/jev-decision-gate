# Jev Decision Gate MCP bundle

Early developer preview, version 0.3.0. Independent MIT project by BPJ; not an official TypeSafe product.

Import the `.mcpb` file into a host supporting MCPB manifest 0.4 and its UV runtime. Choose an existing absolute directory containing the JSON files the tool may read. Hosts may download UV, Python and locked dependencies on first use; this installation is not fully offline. Hosts without UV bundle support can use the [standard Python stdio setup](https://github.com/f-tiger/jev-decision-gate/blob/main/docs/mcp.md).

Jev is disabled by default. Ask the assistant to run `triage_issues` with `provider: rules` on a relative Issue JSON path. Six tools support triage, independent calibration and held-out evaluation. Reports return to the host; the server makes no GitHub changes and writes no reports itself.

Optional Jev mode sends selected title/body text to TypeSafe and may incur charges. Enable it explicitly and use protected host configuration for the key. The call cap applies to each invocation, not account spending. No live Jev savings have been measured. The default rules baseline and synthetic fixtures do not measure Jev quality.

[Source and examples](https://github.com/f-tiger/jev-decision-gate) · [Security boundaries](https://github.com/f-tiger/jev-decision-gate/blob/main/SECURITY.md)
