#!/usr/bin/env python3
"""Reproduce input-price arithmetic; no model calls or measured-usage claims."""
import argparse
from decimal import Decimal
import json
from pathlib import Path

SNAPSHOT = Path(__file__).resolve().parents[1] / "examples/pricing-snapshot.json"


def calculate(snapshot, tokens=1_000_000, fallback_fraction="0.1"):
    n, f = Decimal(str(tokens)), Decimal(str(fallback_fraction))
    if not n.is_finite() or n <= 0 or n != n.to_integral_value():
        raise ValueError("input tokens must be a positive integer")
    if not f.is_finite() or not 0 <= f <= 1:
        raise ValueError("fallback fraction must be between 0 and 1")
    prices = [Decimal(str(snapshot[k]["input_per_million"])) for k in ["baseline", "jev", "lower_cost_baseline"]]
    if any(not p.is_finite() or p <= 0 for p in prices):
        raise ValueError("input prices must be finite and positive")
    baseline, jev, lower = [n * p / 1_000_000 for p in prices]
    cascade = jev + f * baseline
    return {
        "evidence_kind": "hypothetical_input_price_arithmetic_not_live_benchmark",
        "price_as_of": snapshot["as_of"],
        "hypothetical_input_tokens_each": int(n),
        "input_token_volume_ratio": 1,
        "baseline_input_usd": float(baseline),
        "jev_input_usd": float(jev),
        "baseline_to_jev_input_price_ratio": float(baseline / jev),
        "input_price_reduction_percent": float((1 - jev / baseline) * 100),
        "lower_cost_baseline_to_jev_input_price_ratio": float(lower / jev),
        "assumed_fallback_input_fraction": float(f),
        "cascade_input_usd": float(cascade),
        "baseline_to_cascade_input_cost_ratio": float(baseline / cascade),
        "live_token_savings": None,
        "live_quality": None,
        "live_end_to_end_savings": None,
        "exclusions": ["output charges", "retries", "human review", "infrastructure", "taxes"],
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input-tokens", type=int, default=1_000_000)
    p.add_argument("--fallback-fraction", default="0.1")
    args = p.parse_args()
    result = calculate(json.loads(SNAPSHOT.read_text()), args.input_tokens, args.fallback_fraction)
    print(json.dumps(result, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
