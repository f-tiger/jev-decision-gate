"""Ensure the distributable Skill uses the same implementation as the package."""
from pathlib import Path
root = Path(__file__).resolve().parents[1]
source = root / "src/bpj_decision_gate"
bundled = root / "skills/bpj-decision-gate/scripts/bpj_decision_gate"
names = {p.name for p in source.iterdir() if p.suffix in {".py", ".json"}}
other = {p.name for p in bundled.iterdir() if p.suffix in {".py", ".json"}}
assert names == other, "package/Skill file lists differ"
for name in sorted(names):
    assert (source / name).read_bytes() == (bundled / name).read_bytes(), f"Skill drift: {name}"
print(f"Skill matches package: {len(names)} files")
