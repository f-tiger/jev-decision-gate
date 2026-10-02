"""Compatibility alias; use jev_decision_gate.cli."""
from jev_decision_gate.cli import *  # noqa: F401,F403

if __name__ == "__main__":
    raise SystemExit(main())
