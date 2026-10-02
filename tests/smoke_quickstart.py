"""Exercise the documented UV launch against the public, pinned release (no model calls)."""
import asyncio
import json
import os
import tempfile
from pathlib import Path

from mcp import Client, StdioServerParameters

ROOT = Path(__file__).resolve().parents[1]


async def main():
    config = json.loads((ROOT / 'distribution/client-config.json').read_text())['mcpServers']['jev-decision-gate']
    assert '--allow-jev' not in config['args']
    with tempfile.TemporaryDirectory(prefix='jev quickstart ') as directory:
        data_root = Path(directory)
        (data_root / 'issues.json').write_bytes((ROOT / 'examples/issues.synthetic.json').read_bytes())
        args = [directory if arg == '/absolute/path/to/issue-json' else arg for arg in config['args']]
        env = {key: os.environ[key] for key in ('UV_TOOL_DIR', 'UV_CACHE_DIR', 'UV_PYTHON_INSTALL_DIR', 'HTTP_PROXY', 'HTTPS_PROXY', 'ALL_PROXY', 'NO_PROXY', 'http_proxy', 'https_proxy', 'all_proxy', 'no_proxy') if key in os.environ}
        params = StdioServerParameters(command=config['command'], args=args, env=env)
        async with Client(params, read_timeout_seconds=20) as client:
            assert client.server_info.name == 'Jev Decision Gate', client.server_info
            names = sorted(tool.name for tool in (await client.list_tools()).tools)
            assert len(names) == 6 and 'triage_issues' in names, names
            response = await client.call_tool('triage_issues', {'issues_file': 'issues.json', 'provider': 'rules'})
            assert not response.is_error, response
            report = response.structured_content
            assert report['summary']['issues'] == 12, report['summary']
            assert report['summary']['model_calls'] == 0, report['summary']
            assert report['summary']['review'] == 12, report['summary']
            rejected = await client.call_tool('triage_issues', {'issues_file': '../outside.json', 'provider': 'rules'})
            assert rejected.is_error, rejected
            print(json.dumps({'status': 'passed', 'source': config['args'][3], 'tools': names,
                              'synthetic_issues': 12, 'provider_calls': 0, 'review': 12,
                              'path_with_spaces': 'passed', 'outside_path': 'rejected'}))


if __name__ == '__main__':
    asyncio.run(main())
