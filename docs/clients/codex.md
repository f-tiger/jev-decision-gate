# Jev Decision Gate for Codex

Give Codex six local MCP tools for GitHub Issue triage, calibration and review.

Install [UV](https://docs.astral.sh/uv/getting-started/installation/) and Git first. UV downloads the pinned release and its Python environment on first use. The source is pinned to the exact v0.3.1 commit. No repository checkout is required. These commands run on your own computer.

Choose an existing absolute directory containing Issue JSON files. Replace `/absolute/path/to/issue-json` in the examples with that directory. Keep a narrow data directory rather than your home directory.

## Add the server

```bash
codex mcp add jev-decision-gate -- uvx --python 3.12 --from "jev-decision-gate[mcp] @ git+https://github.com/f-tiger/jev-decision-gate@69d2c69f0c49f6537cb2f4feb47502fba9112e42" jev-gate-mcp --data-root "/absolute/path/to/issue-json"
```

Before starting Codex, warm the package cache:

```bash
uvx --python 3.12 --from "jev-decision-gate[mcp] @ git+https://github.com/f-tiger/jev-decision-gate@69d2c69f0c49f6537cb2f4feb47502fba9112e42" jev-gate-mcp --help
codex mcp list
```

Alternatively, merge this entry into your Codex `config.toml` instead of using the add command. Replace the directory placeholder. Do not replace the rest of your configuration.

```toml
[mcp_servers.jev-decision-gate]
command = "uvx"
args = ["--python", "3.12", "--from", "jev-decision-gate[mcp] @ git+https://github.com/f-tiger/jev-decision-gate@69d2c69f0c49f6537cb2f4feb47502fba9112e42", "jev-gate-mcp", "--data-root", "/absolute/path/to/issue-json"]
startup_timeout_sec = 60
```

If the host cannot find `uvx`, replace it with the executable's absolute path on your computer. Use forward slashes in Windows paths, for example `C:/Users/you/issue-json`.

## First task

Ask your agent:

> Use Jev Decision Gate to run the rules baseline on `issues.json`. Show the predicted kind, module and information sufficiency, then explain the review recommendations.

A working connection exposes six tools, including `triage_issues`. Rules mode needs no TypeSafe key. [Example Issue JSON](../../examples/issues.synthetic.json) is available if you do not have your own file. Save it as `issues.json` inside your selected directory.

To enable Jev later, follow [MCP configuration](../mcp.md). Host model charges may apply when an agent invokes the tool. Client configuration examples never contain API keys.

## Remove

Remove the `mcp_servers.jev-decision-gate` entry from your configuration, or use the removal command listed by `codex mcp --help`.

Source: [official Codex MCP documentation](https://developers.openai.com/codex/mcp), checked 2026-10-02. The underlying launch command and MCP calls are checked by this repository; the Codex application is not part of the automated smoke test.
