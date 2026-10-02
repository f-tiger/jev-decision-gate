# Jev Decision Gate for Cursor

Add local GitHub Issue triage, response checks and calibrated review to Cursor Agent.

Install [UV](https://docs.astral.sh/uv/getting-started/installation/) and Git first. UV downloads the pinned release and its Python environment on first use. The source is pinned to the exact v0.3.1 commit. No repository checkout is required. These commands run on your own computer.

Choose an existing absolute directory containing Issue JSON files. Replace `/absolute/path/to/issue-json` in the examples with that directory. Keep a narrow data directory rather than your home directory.

## Configure your project

Merge the following into `.cursor/mcp.json` in the project where you want to use the tool. If that file already contains servers, add only the `jev-decision-gate` entry. Use forward slashes in Windows paths, for example `C:/Users/you/issue-json`.

```json
{
  "mcpServers": {
    "jev-decision-gate": {
      "command": "uvx",
      "args": [
        "--python",
        "3.12",
        "--from",
        "jev-decision-gate[mcp] @ git+https://github.com/f-tiger/jev-decision-gate@69d2c69f0c49f6537cb2f4feb47502fba9112e42",
        "jev-gate-mcp",
        "--data-root",
        "/absolute/path/to/issue-json"
      ]
    }
  }
}
```

Before enabling the server, warm the package cache in a terminal:

```bash
uvx --python 3.12 --from "jev-decision-gate[mcp] @ git+https://github.com/f-tiger/jev-decision-gate@69d2c69f0c49f6537cb2f4feb47502fba9112e42" jev-gate-mcp --help
```

Open Cursor's MCP settings, enable the server and inspect the tools. If Cursor cannot find `uvx`, use its absolute executable path in `command`.

## First task

Ask your agent:

> Use Jev Decision Gate to run the rules baseline on `issues.json`. Show the predicted kind, module and information sufficiency, then explain the review recommendations.

A working connection exposes six tools, including `triage_issues`. Rules mode needs no TypeSafe key. [Example Issue JSON](../../examples/issues.synthetic.json) is available if you do not have your own file. Save it as `issues.json` inside your selected directory.

To enable Jev later, follow [MCP configuration](../mcp.md). Host model charges may apply when an agent invokes the tool. Client configuration examples never contain API keys.

## Remove

Remove only the `jev-decision-gate` entry from `.cursor/mcp.json`.

Sources: [Cursor MCP documentation](https://cursor.com/docs/context/mcp) and [install-link format](https://cursor.com/docs/mcp/install-links), checked 2026-10-02. A shared one-click link cannot know your authorized local directory; this configuration asks you to choose it explicitly. The underlying MCP command is exercised by the smoke test; the Cursor GUI is not part of it.
