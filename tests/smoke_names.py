"""Check a real installed CLI under the new name and legacy compatibility entry points."""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from jev_decision_gate.risk_gate import Gate
from jev_decision_gate.triage import triage
from bpj_decision_gate.risk_gate import Gate as LegacyGate
from bpj_decision_gate.triage import triage as legacy_triage

assert LegacyGate is Gate and legacy_triage is triage, "Both imports must share one implementation"

with tempfile.TemporaryDirectory(prefix="jev-names-") as directory:
    root = Path(directory)
    summaries = []
    for executable in ("jev-gate", "bpj-gate"):
        command = shutil.which(executable)
        assert command, f"Install the package before checking {executable}"
        output = root / f"{executable}.json"
        subprocess.run([command, "demo", "--out", str(output)], check=True, capture_output=True)
        report = json.loads(output.read_text())
        assert report["summary"]["model_calls"] == 0 and len(report["rows"]) == 12
        summaries.append(report["summary"])
    assert summaries[0] == summaries[1]
    for module in ("jev_decision_gate.cli", "bpj_decision_gate.cli"):
        subprocess.run([sys.executable, "-m", module, "--help"], check=True, capture_output=True)
    for executable in ("jev-gate-mcp", "bpj-gate-mcp"):
        subprocess.run([shutil.which(executable), "--help"], check=True, capture_output=True)
print("Jev CLI/imports and legacy BPJ entry points passed; offline rules only")
