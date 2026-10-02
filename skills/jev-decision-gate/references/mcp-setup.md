# Local MCP v0.3.1

Use Python 3.11+ with `mcp==2.2.0`:

```text
<venv-python> <skill>/scripts/mcp_server.py --data-root <absolute-authorized-directory>
```

This is local stdio. Set a supported host's command to the absolute Python executable and its args to the script path, --data-root and the directory. The public project is registered as `io.github.f-tiger/jev-decision-gate` in the official MCP Registry; see the repository's `docs/distribution.md` for version status. Installing this Skill supplies scripts and instructions; verify tool discovery before claiming the user's host is connected.

Jev requires `--allow-jev` at startup and TYPESAFE_API_KEY through the host's secret/environment mechanism. --max-calls defaults to 20 per invocation, not per day/account. Never commit keys. Smoke tests make no paid calls.

Issue tools: triage_issues(issues_file, provider, policy_id?, input_usd_per_million?), calibrate_issue_gate(report_file, max_error=.05, delta=.05), evaluate_issue_gate(policy_id, report_file). The host can save returned reports to an explicitly chosen local file for calibration. Tools themselves only read. Policy IDs are process-local; recalibrate after restart.

Generic tools: calibrate_gate(calibration_file, scope, max_error=.05, delta=.05), evaluate_gate(policy_id, test_file), route_batch(policy_id, requests_file). These require caller-supplied scores and costs; read data-contract.md first.

Relative JSON paths must remain in the trusted root. Traversal, absolute paths and escaping symlinks fail. Maximum 32 policies. This is not an adversarial filesystem sandbox or multi-tenant service. Outputs may enter model context; prefer concise summaries.

Run scripts/smoke_mcp.py in the same environment to verify actual communication using synthetic fixtures.
