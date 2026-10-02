"""Synthetic mechanics demo only. No real model performance is measured."""
import json
import argparse
import random
from dataclasses import asdict
from pathlib import Path
from risk_gate import fit_gate, evaluate

SCOPE = "synthetic-model-v1_question-v1_en"

def generate(prefix, seed, n):
    rng = random.Random(seed)
    result = []
    for i in range(n):
        score = rng.uniform(.5, 1)
        # Deliberately constructed relationship, NOT learned or observed.
        correctness = .995 if score >= .9 else (.96 if score >= .8 else .75)
        result.append(dict(id=f"{prefix}-{i}", scope=SCOPE, score=score,
            cheap_correct=rng.random() < correctness,
            fallback_correct=rng.random() < .99, eligible=True,
            cheap_cost=.0002, fallback_cost=.002, overhead_cost=.00005))
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    out = parser.parse_args().out
    out.mkdir(parents=True, exist_ok=True)
    calibration, test = generate("cal", 13, 1500), generate("test", 29, 800)
    gate, candidates = fit_gate(calibration, SCOPE)
    for name, data in [("calibration.json", calibration), ("test.json", test)]:
        (out/name).write_text(json.dumps(data, indent=2))
    summary = dict(evidence_type="SYNTHETIC MECHANICS DEMO ONLY",
        gate={k:v for k,v in asdict(gate).items() if k != "calibration_ids"},
        candidates=candidates, test=evaluate(gate, test))
    (out/"synthetic_results.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))
