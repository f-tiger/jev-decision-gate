import math
import unittest
from bpj_decision_gate.risk_gate import fit_gate, evaluate, upper_error_bound


def row(i, score=.99, correct=True, **extra):
    return dict(id=str(i), scope="demo-v1-en", score=score, cheap_correct=correct,
                fallback_correct=True, eligible=True, cheap_cost=.1,
                fallback_cost=1., overhead_cost=.01, **extra)


class GateTests(unittest.TestCase):
    def test_exact_zero_error_bound(self):
        self.assertAlmostEqual(upper_error_bound(0, 100, .05), 1-.05**.01)

    def test_bound_extremes(self):
        self.assertEqual(upper_error_bound(0, 0, .05), 1)
        self.assertEqual(upper_error_bound(20, 20, .05), 1)

    def test_overconfident_wrong_predictions_rejected(self):
        gate, _ = fit_gate([row(i, correct=False) for i in range(200)], "demo-v1-en")
        self.assertIsNone(gate.threshold)

    def test_small_sample_cannot_certify(self):
        gate, _ = fit_gate([row(i) for i in range(5)], "demo-v1-en")
        self.assertIsNone(gate.threshold)

    def test_good_predictions_and_disjoint_test(self):
        gate, _ = fit_gate([row(i) for i in range(300)], "demo-v1-en")
        self.assertIsNotNone(gate.threshold)
        result = evaluate(gate, [row("test-1")])
        self.assertEqual(result["accepted"], 1)
        self.assertAlmostEqual(result["observed_cost"], .11)

    def test_scope_change_and_ineligible_force_fallback(self):
        gate, _ = fit_gate([row(i) for i in range(300)], "demo-v1-en")
        r1, r2 = row("test-1"), row("test-2")
        r1["scope"] = "demo-v2-zh"
        r2["eligible"] = False
        result = evaluate(gate, [r1, r2])
        self.assertEqual(result["accepted"], 0)
        self.assertAlmostEqual(result["observed_cost"], 2.02)

    def test_rejected_cheap_inference_is_charged(self):
        gate, _ = fit_gate([row(i) for i in range(300)], "demo-v1-en")
        result = evaluate(gate, [row("test", score=.1)])
        self.assertAlmostEqual(result["observed_cost"], 1.11)
        self.assertLess(result["savings_fraction"], 0)

    def test_fallback_not_assumed_correct(self):
        gate, _ = fit_gate([row(i) for i in range(300)], "demo-v1-en")
        r = row("test", score=.1)
        r["fallback_correct"] = False
        self.assertEqual(evaluate(gate, [r])["overall_error"], 1)

    def test_leakage_rejected(self):
        rows = [row(i) for i in range(300)]
        gate, _ = fit_gate(rows, "demo-v1-en")
        with self.assertRaises(ValueError):
            evaluate(gate, rows)

    def test_invalid_numbers_and_labels(self):
        for key, value in [("score", math.nan), ("score", 1.1), ("cheap_cost", -1),
                           ("cheap_correct", "true")]:
            r = row(1)
            r[key] = value
            with self.assertRaises(ValueError):
                fit_gate([r], "demo-v1-en")

    def test_disjoint_id_is_not_a_drift_detector(self):
        gate, _ = fit_gate([row(i) for i in range(300)], "demo-v1-en")
        shifted = [row(f"shift-{i}", correct=False) for i in range(50)]
        self.assertEqual(evaluate(gate, shifted)["selective_error"], 1)


if __name__ == "__main__":
    unittest.main()
