"""MCPB launcher: translate explicit host configuration to the existing server."""
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))


def main():
    data_root = os.environ.get("BPJ_DATA_ROOT", "")
    if not data_root or not Path(data_root).is_absolute() or not Path(data_root).is_dir():
        raise SystemExit("BPJ_DATA_ROOT must be an existing absolute directory")
    allow = os.environ.get("BPJ_ALLOW_JEV", "false").lower()
    if allow not in {"true", "false"}:
        raise SystemExit("BPJ_ALLOW_JEV must be true or false")
    maximum = os.environ.get("BPJ_MAX_CALLS", "20")
    if not re.fullmatch(r"[0-9]{1,3}", maximum) or not 1 <= int(maximum) <= 200:
        raise SystemExit("BPJ_MAX_CALLS must be an integer from 1 to 200")
    if allow == "true" and not os.environ.get("TYPESAFE_API_KEY", "").strip():
        raise SystemExit("Enabling Jev requires a TypeSafe API key in protected host configuration")
    from jev_decision_gate.mcp_server import create_server
    create_server(Path(data_root), allow == "true", int(maximum)).run(transport="stdio")


if __name__ == "__main__":
    main()
