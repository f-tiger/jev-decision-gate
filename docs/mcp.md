# Local MCP setup

## MCPB bundle

Download [`jev-decision-gate-0.3.0.mcpb`](https://github.com/f-tiger/jev-decision-gate/releases/tag/v0.3.0) from the public release. It is registered as [`io.github.f-tiger/jev-decision-gate`](https://registry.modelcontextprotocol.io/v0.1/servers/io.github.f-tiger%2Fjev-decision-gate/versions/0.3.0) with the official MCP Registry. The release includes `SHA256SUMS` and Registry metadata. [Publication and directory status](distribution.md).

Import the bundle into a host supporting **MCPB manifest 0.4 with the UV runtime**, then choose an existing absolute directory containing your Issue JSON. UV may download Python and locked dependencies on first launch. Host support varies; the conventional setup below remains available. The bundle has been exercised on Linux; GUI host import, macOS and Windows have not been verified.

Leave **Enable paid Jev calls** off to use the rules baseline without a key. To enable Jev later, use the host's protected configuration for the optional API key. The bundle prompts for a directory, an explicit Jev opt-in and a per-invocation call cap. Never put credentials in the download URL or chat. This preview bundle is unsigned; the release includes its SHA256 checksum.

## Python stdio setup

Install with `python -m pip install '.[mcp]'` from the cloned project. This pins `mcp==2.2.0`. The default core package uses only the Python standard library. Use the absolute executable path from your virtual environment to avoid host PATH differences.

For hosts supporting the conventional `mcpServers` configuration:

```json
{
  "mcpServers": {
    "jev-decision-gate": {
      "command": "/absolute/path/jev-decision-gate/.venv/bin/jev-gate-mcp",
      "args": ["--data-root", "/absolute/path/authorized-json"]
    }
  }
}
```

On Windows, the command is the environment's `Scripts/jev-gate-mcp.exe`. Hosts use different configuration locations and keys; use the host's current documentation. This project speaks local **stdio**, not remote HTTP.

Add `--allow-jev` to `args` and expose `TYPESAFE_API_KEY` through the host's secret/environment mechanism only when you intend to make paid TypeSafe calls. Default `--max-calls 20` limits calls in **each tool invocation**, not per day or account. Requests above that limit fail before any model call. The user controls the provider's billing limits. There is no total-spend enforcement or hidden retry loop.

| Tool | Input and result |
|---|---|
| `triage_issues` | Relative Issue JSON path; rules or Jev; optional process-local policy; structured report |
| `calibrate_issue_gate` | Independent fully labeled triage report saved in data root; returns policy ID |
| `evaluate_issue_gate` | Policy ID and disjoint report path; joint correctness and coverage |
| `calibrate_gate` | Generic scored traces with supplied truth labels/costs; returns policy ID |
| `evaluate_gate` | Generic disjoint test traces; replayed costs and fallback outcomes |
| `route_batch` | Supplied scores; recommends accept/fallback without calling a model |

Example request to your assistant: “Use Jev Decision Gate to run the rules baseline on `issues.json` in the configured directory. Explain which items need review. Do not change GitHub Issues.”

Reports are returned to the MCP host; if needed, the host saves them to an explicitly chosen JSON file for calibration. MCP itself does not write files. Result content may enter the host model's context. No policy persists after server restart. At most 32 policies live in memory. Calibrate again after restart, or use the CLI with an explicit policy file.

`data_root` is one trusted local workspace. Absolute paths, traversal and symlinks outside it are rejected. This is not a hostile multi-user filesystem sandbox: concurrent malicious path swaps are outside its design. There is no authentication, HTTP hosting, database or multi-tenant isolation.

## Generic scored traces

Each calibration/test row has `id`, `scope`, `eligible`, `score`, `cheap_correct`, `fallback_correct`, `cheap_cost`, `fallback_cost`, `overhead_cost`. Boolean fields must be actual booleans; score is finite in [0,1]; costs are finite and nonnegative in one consistent currency/unit. Every row needs observed or explicitly simulated outcomes for both routes; never fill unknown fallback correctness as true.

`route_batch` only needs `id`, `scope`, `eligible`, `score`. The generic cost replay skips cheap inference under a disabled gate. Issue reports instead preserve already-incurred usage and never infer savings; these are different reports with different evidence requirements.
