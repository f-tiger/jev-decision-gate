# Local MCP setup

Install with `python -m pip install '.[mcp]'` from the cloned project. This pins `mcp==2.2.0`. The default core package uses only the Python standard library. Use the absolute executable path from your virtual environment to avoid host PATH differences.

For hosts supporting the conventional `mcpServers` configuration:

```json
{
  "mcpServers": {
    "bpj-decision-gate": {
      "command": "/absolute/path/jev-decision-gate/.venv/bin/bpj-gate-mcp",
      "args": ["--data-root", "/absolute/path/authorized-json"]
    }
  }
}
```

On Windows, the command is the environment's `Scripts/bpj-gate-mcp.exe`. Hosts use different configuration locations and keys; use the host's current documentation. This project speaks local **stdio**, not remote HTTP, and is not yet published in the MCP Registry.

Add `--allow-jev` to `args` and expose `TYPESAFE_API_KEY` through the host's secret/environment mechanism only when you intend to make paid TypeSafe calls. Default `--max-calls 20` limits calls in **each tool invocation**, not per day or account. Requests above that limit fail before any model call. The user controls the provider's billing limits. There is no total-spend enforcement or hidden retry loop.

| Tool | Input and result |
|---|---|
| `triage_issues` | Relative Issue JSON path; rules or Jev; optional process-local policy; structured report |
| `calibrate_issue_gate` | Independent fully labeled triage report saved in data root; returns policy ID |
| `evaluate_issue_gate` | Policy ID and disjoint report path; joint correctness and coverage |
| `calibrate_gate` | Generic scored traces with supplied truth labels/costs; returns policy ID |
| `evaluate_gate` | Generic disjoint test traces; replayed costs and fallback outcomes |
| `route_batch` | Supplied scores; recommends accept/fallback without calling a model |

Example request to your assistant: “Use BPJ Decision Gate to run the rules baseline on `issues.json` in the configured directory. Explain which items need review. Do not change GitHub Issues.”

Reports are returned to the MCP host; if needed, the host saves them to an explicitly chosen JSON file for calibration. MCP itself does not write files. Result content may enter the host model's context. No policy persists after server restart. At most 32 policies live in memory. Calibrate again after restart, or use the CLI with an explicit policy file.

`data_root` is one trusted local workspace. Absolute paths, traversal and symlinks outside it are rejected. This is not a hostile multi-user filesystem sandbox: concurrent malicious path swaps are outside its design. There is no authentication, HTTP hosting, database or multi-tenant isolation.

## Generic scored traces

Each calibration/test row has `id`, `scope`, `eligible`, `score`, `cheap_correct`, `fallback_correct`, `cheap_cost`, `fallback_cost`, `overhead_cost`. Boolean fields must be actual booleans; score is finite in [0,1]; costs are finite and nonnegative in one consistent currency/unit. Every row needs observed or explicitly simulated outcomes for both routes; never fill unknown fallback correctness as true.

`route_batch` only needs `id`, `scope`, `eligible`, `score`. The generic cost replay skips cheap inference under a disabled gate. Issue reports instead preserve already-incurred usage and never infer savings; these are different reports with different evidence requirements.
