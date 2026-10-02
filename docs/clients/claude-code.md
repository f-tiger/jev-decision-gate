# Jev Decision Gate for Claude Code

Batch GitHub Issue triage with a local MCP server: classification, response checks, acceptance calibration and review recommendations.

Install [UV](https://docs.astral.sh/uv/getting-started/installation/) and Git first. UV downloads the pinned release and its Python environment on first use. The source is pinned to the exact v0.3.1 commit. No repository checkout is required. These commands run on your own computer.

Choose an existing absolute directory containing Issue JSON files. Replace `/absolute/path/to/issue-json` in the examples with that directory. Keep a narrow data directory rather than your home directory.

## Add the server

Run from the project where you want to use the tool:

```bash
claude mcp add --transport stdio --scope local jev-decision-gate -- uvx --python 3.12 --from "jev-decision-gate[mcp] @ git+https://github.com/f-tiger/jev-decision-gate@69d2c69f0c49f6537cb2f4feb47502fba9112e42" jev-gate-mcp --data-root "/absolute/path/to/issue-json"
```

The local scope makes the server available only in this project for your user. On Windows, the same one-line command can be used in PowerShell with a path such as `C:/Users/you/issue-json`.

Before starting Claude Code, warm the package cache to avoid a slow first connection:

```bash
uvx --python 3.12 --from "jev-decision-gate[mcp] @ git+https://github.com/f-tiger/jev-decision-gate@69d2c69f0c49f6537cb2f4feb47502fba9112e42" jev-gate-mcp --help
claude mcp get jev-decision-gate
```

Open Claude Code and use `/mcp` to inspect the connection and available tools.

## First task

Ask your agent:

> Use Jev Decision Gate to run the rules baseline on `issues.json`. Show the predicted kind, module and information sufficiency, then explain the review recommendations.

A working connection exposes six tools, including `triage_issues`. Rules mode needs no TypeSafe key. [Example Issue JSON](../../examples/issues.synthetic.json) is available if you do not have your own file. Save it as `issues.json` inside your selected directory.

To enable Jev later, follow [MCP configuration](../mcp.md). Host model charges may apply when an agent invokes the tool. Client configuration examples never contain API keys.

## Remove

```bash
claude mcp remove --scope local jev-decision-gate
```

Source: [Claude Code MCP documentation](https://code.claude.com/docs/en/mcp), checked 2026-10-02. The underlying launch command and MCP calls are checked by this repository; the Claude Code application is not part of the automated smoke test.
