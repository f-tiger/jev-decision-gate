"""Offline selective decision gate. No model, API, training, or action execution.

Fixed score thresholds are tested on held-out labeled predictions using a
one-sided exact binomial bound and Bonferroni correction. This is established
statistics assembled into a small implementation, not a new statistical method.
The claim concerns error among accepted cheap-model predictions for the frozen
scope under i.i.d. sampling. It does not cover drift or fallback correctness.
"""
from __future__ import annotations
import argparse
import json
import math
from dataclasses import dataclass, asdict
from pathlib import Path


def upper_error_bound(errors: int, total: int, delta: float) -> float:
    """One-sided Clopper-Pearson upper bound by binomial-CDF inversion."""
    if not 0 < delta < 1 or not 0 <= errors <= total:
        raise ValueError("invalid binomial counts or delta")
    if total == 0 or errors == total:
        return 1.0
    if errors == 0:
        return -math.expm1(math.log(delta) / total)
    coeff = [math.lgamma(total + 1) - math.lgamma(i + 1)
             - math.lgamma(total - i + 1) for i in range(errors + 1)]

    def log_cdf(p: float) -> float:
        lp, lq = math.log(p), math.log1p(-p)
        terms = [c + i * lp + (total-i) * lq for i, c in enumerate(coeff)]
        largest = max(terms)
        return largest + math.log(sum(math.exp(t-largest) for t in terms))

    lo, hi = errors / total, 1.0
    for _ in range(65):
        mid = (lo + hi) / 2
        if mid == hi or mid == lo:
            break
        if log_cdf(mid) > math.log(delta):
            lo = mid
        else:
            hi = mid
    return hi


def validate_rows(rows: list[dict]) -> None:
    if not rows:
        raise ValueError("rows must not be empty")
    seen = set()
    for row in rows:
        if not isinstance(row.get("id"), str) or not row["id"] or row["id"] in seen:
            raise ValueError("IDs must be unique nonempty strings")
        seen.add(row["id"])
        for key in ("scope",):
            if not isinstance(row.get(key), str) or not row[key]:
                raise ValueError("scope must identify the frozen workload")
        for key in ("cheap_correct", "fallback_correct", "eligible"):
            if type(row.get(key)) is not bool:
                raise ValueError(f"{key} must be bool")
        for key in ("score", "cheap_cost", "fallback_cost", "overhead_cost"):
            value = row.get(key)
            if type(value) not in (int, float) or not math.isfinite(value) or value < 0:
                raise ValueError(f"{key} must be finite and nonnegative")
        if row["score"] > 1:
            raise ValueError("score must be in [0, 1]")


@dataclass(frozen=True)
class Gate:
    scope: str
    threshold: float | None
    max_error: float
    delta: float
    calibration_ids: tuple[str, ...]
    calibration_accepted: int
    calibration_errors: int
    upper_error: float | None
    candidates_tested: int

    def accepts(self, row: dict) -> bool:
        # Only prediction-time fields are used; never inspect correctness.
        return (self.threshold is not None and row["scope"] == self.scope
                and row["eligible"] and row["score"] >= self.threshold)


def fit_gate(rows: list[dict], scope: str, max_error: float = .05,
             delta: float = .05,
             thresholds: tuple[float, ...] = (.5, .6, .7, .8, .85, .9, .93, .95, .97, .99)) -> tuple[Gate, list[dict]]:
    """Freeze the model, score mapping and candidate grid before supplying rows.

    If a score calibrator is trained, use a DIFFERENT split for this gate fit.
    Repeatedly tuning on these labels invalidates the stated confidence bound.
    """
    validate_rows(rows)
    if not 0 < max_error < 1 or not 0 < delta < 1:
        raise ValueError("max_error and delta must lie in (0, 1)")
    if not thresholds or any(not math.isfinite(t) or not 0 <= t <= 1 for t in thresholds):
        raise ValueError("provide a fixed finite threshold grid in [0, 1]")
    thresholds = tuple(sorted(set(thresholds)))
    if any(r["scope"] != scope for r in rows):
        raise ValueError("use one frozen scope per calibration run")
    candidates = []
    for t in thresholds:
        selected = [r for r in rows if r["eligible"] and r["score"] >= t]
        n = len(selected)
        errors = sum(not r["cheap_correct"] for r in selected)
        upper = upper_error_bound(errors, n, delta / len(thresholds))
        candidates.append(dict(threshold=t, accepted=n, errors=errors,
                               upper_error=upper, passes=n > 0 and upper <= max_error))
    passing = [c for c in candidates if c["passes"]]
    best = max(passing, key=lambda c: (c["accepted"], c["threshold"])) if passing else None
    gate = Gate(scope, best["threshold"] if best else None, max_error, delta,
                tuple(r["id"] for r in rows), best["accepted"] if best else 0,
                best["errors"] if best else 0, best["upper_error"] if best else None,
                len(thresholds))
    return gate, candidates


def evaluate(gate: Gate, rows: list[dict]) -> dict:
    """Replay labeled, disjoint test traces. Costs are supplied, not estimated.

    For an active gate, eligible in-scope rows first incur cheap cost, then incur
    fallback cost only if rejected. Overhead cost applies to all requests.
    A disabled gate bypasses the cheap model. Missing outcomes are not allowed.
    """
    validate_rows(rows)
    if set(gate.calibration_ids) & {r["id"] for r in rows}:
        raise ValueError("calibration/test leakage: overlapping IDs")
    accepted, errors, overall_errors = 0, 0, 0
    spend, baseline = 0.0, 0.0
    for r in rows:
        baseline += r["fallback_cost"]
        used_cheap = gate.threshold is not None and r["scope"] == gate.scope and r["eligible"]
        accept = gate.accepts(r)
        accepted += int(accept)
        errors += int(accept and not r["cheap_correct"])
        overall_errors += int(not (r["cheap_correct"] if accept else r["fallback_correct"]))
        spend += r["overhead_cost"] + (r["cheap_cost"] if used_cheap else 0)
        if not accept:
            spend += r["fallback_cost"]
    return dict(total=len(rows), accepted=accepted, accepted_errors=errors,
                coverage=accepted/len(rows), selective_error=errors/accepted if accepted else None,
                overall_error=overall_errors/len(rows),
                fallback_only_error=sum(not r["fallback_correct"] for r in rows)/len(rows),
                observed_cost=spend, fallback_only_cost=baseline,
                savings_fraction=1-spend/baseline if baseline else None,
                note="Offline replay. Does not establish model accuracy or future savings.")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("calibration", type=Path)
    ap.add_argument("test", type=Path)
    ap.add_argument("--scope", required=True)
    ap.add_argument("--max-error", type=float, default=.05)
    ap.add_argument("--delta", type=float, default=.05)
    args = ap.parse_args()
    calibration = json.loads(args.calibration.read_text())
    test = json.loads(args.test.read_text())
    gate, candidates = fit_gate(calibration, args.scope, args.max_error, args.delta)
    print(json.dumps(dict(gate=asdict(gate), candidates=candidates,
                         test=evaluate(gate, test)), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
