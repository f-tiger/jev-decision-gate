"""Run the bundled BPJ CLI without installing the project."""
import sys
from bpj_decision_gate.cli import main
if __name__ == "__main__":
    sys.exit(main())
