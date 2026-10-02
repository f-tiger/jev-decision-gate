import copy
import json
import os
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch
from jev_decision_gate.io import read_json, write_json
from jev_decision_gate.risk_gate import Gate
from jev_decision_gate.triage import (MODEL, TAXONOMY, ProviderError, build_request,
    scope_for, parse_response, triage, calibrate_report, read_gate, evaluate_report, http_post, ENDPOINT)


ISSUE = {"id": "test-1", "title": "API error", "body": "Empty payload returns HTTP 500; expected 400.",
         "expected": {"kind": "bug", "module": "api", "information": "sufficient"}}


def response():
    expected = ISSUE["expected"]
    return {"model": MODEL, "answers": {
        key: {"type": "choice", "choice": expected[key],
              "probabilities": {label: .99 if label == expected[key] else .01/(len(choices)-1) for label in choices},
              "confidence": .5}
        for key, choices in TAXONOMY.items()}, "usage": {"input_tokens": 100, "output_tokens": 30}}


class TriageTests(unittest.TestCase):
    def test_http_transport_uses_fixed_endpoint_and_safe_error_messages(self):
        from urllib.error import HTTPError
        with patch("urllib.request.build_opener") as factory:
            opened = factory.return_value.open
            opened.return_value.__enter__.return_value.read.return_value = json.dumps(response()).encode()
            self.assertEqual(http_post(build_request(ISSUE), "unit-test-only"), response())
            request = opened.call_args.args[0]
            self.assertEqual(request.full_url, ENDPOINT)
            self.assertEqual(request.get_method(), "POST")
            self.assertEqual(request.get_header("Authorization"), "Bearer unit-test-only")
            self.assertNotIn("expected", json.loads(request.data)["state"]["issue"])
            self.assertEqual(opened.call_args.kwargs["timeout"], 30)
            opened.side_effect = HTTPError(ENDPOINT, 401, "unit-test-only secret", {}, None)
            with self.assertRaises(ProviderError) as caught:
                http_post(build_request(ISSUE), "unit-test-only")
            self.assertEqual(str(caught.exception), "TypeSafe HTTP 401; request was not retried")

    def test_expected_labels_and_metadata_never_leave_process(self):
        issue = ISSUE | {"private_note": "secret", "token": "secret"}
        req = build_request(issue)
        self.assertEqual(req["state"], {"issue": {"title": issue["title"], "body": issue["body"]}})
        self.assertNotIn("secret", json.dumps(req))
        self.assertEqual(set(req["questions"]), set(TAXONOMY))
        for question in req["questions"].values():
            self.assertIn("state.issue", question["instructions"])

    def test_contract_parses_selected_probabilities_not_confidence(self):
        pred, score, usage = parse_response(response(), MODEL)
        self.assertEqual(pred, ISSUE["expected"])
        self.assertEqual(score, .99)
        self.assertEqual(usage["input_tokens"], 100)

    def test_malformed_contracts_fail_closed(self):
        samples = []
        r = response(); r["model"] = "jev-latest"; samples.append(r)
        r = response(); r["answers"].pop("module"); samples.append(r)
        r = response(); r["answers"]["kind"]["probabilities"]["bug"] = True; samples.append(r)
        r = response(); r["answers"]["kind"]["probabilities"]["bug"] = float('nan'); samples.append(r)
        r = response(); r["answers"]["kind"]["choice"] = "question"; samples.append(r)
        r = response(); r["answers"]["kind"]["choice"] = ["bug"]; samples.append(r)
        r = response(); r["usage"]["input_tokens"] = -1; samples.append(r)
        r = response(); r["usage"]["input_tokens"] = 10**100; samples.append(r)
        r = response(); r.pop("usage"); samples.append(r)
        for r in samples:
            with self.subTest(response=r), self.assertRaises(ProviderError):
                parse_response(r, MODEL)

    def test_rules_offline_without_api_key(self):
        with patch.dict(os.environ, {}, clear=True):
            r = triage([ISSUE], transport=lambda *_: self.fail("network call"))
        self.assertEqual(r["summary"]["model_calls"], 0)
        self.assertEqual(r["rows"][0]["action"], "review")
        self.assertIsNone(r["summary"]["savings_fraction"])

    def test_jev_requires_key_and_respects_preflight_budget(self):
        with patch.dict(os.environ, {}, clear=True), self.assertRaisesRegex(ValueError, "TYPESAFE_API_KEY"):
            triage([ISSUE], provider="jev")
        with self.assertRaisesRegex(ValueError, "max_calls"):
            triage([ISSUE, ISSUE | {"id": "test-2"}], provider="jev", max_calls=1,
                   transport=lambda *_: self.fail("network call"))

    def test_success_and_partial_failure_accounting(self):
        def transport(payload, key):
            if payload["state"]["issue"]["title"] == "Fail":
                raise ProviderError("TypeSafe transport failed; request was not retried")
            return response()
        with patch.dict(os.environ, {"TYPESAFE_API_KEY": "unit-test-only"}):
            r = triage([ISSUE, ISSUE | {"id": "test-2", "title": "Fail"}], provider="jev",
                       transport=transport, input_usd_per_million=.042)
        self.assertEqual(r["summary"]["reported_input_tokens"], 100)
        self.assertEqual(r["summary"]["calls_with_unknown_usage"], 1)
        self.assertFalse(r["summary"]["cost_complete"])
        self.assertAlmostEqual(r["summary"]["estimated_reported_usage_usd"], .0000042)
        self.assertEqual(r["rows"][1]["reason"], "provider_failure")
        self.assertEqual(r["rows"][1]["action"], "review")
        self.assertNotIn("unit-test-only", json.dumps(r))

    def test_disabled_gate_avoids_model_calls_even_without_key(self):
        gate = Gate(scope_for("jev"), None, .05, .05, (), 0, 0, None, 10)
        with patch.dict(os.environ, {}, clear=True):
            r = triage([ISSUE], provider="jev", gate=gate, transport=lambda *_: self.fail("network call"))
        self.assertEqual(r["summary"]["model_calls"], 0)
        self.assertEqual(r["rows"][0]["reason"], "disabled_gate")

    def test_scope_changes_invalidate_gate_before_model_call(self):
        gate = Gate(scope_for("rules"), .5, .05, .05, (), 100, 0, .05, 10)
        with self.assertRaisesRegex(ValueError, "scope"):
            triage([ISSUE], provider="jev", gate=gate)

    def test_tiny_calibration_disables_acceptance_and_rejects_leakage(self):
        report = triage([ISSUE])
        document = calibrate_report(report)
        gate = read_gate(document)
        self.assertIsNone(gate.threshold)
        with self.assertRaisesRegex(ValueError, "overlapping"):
            evaluate_report(gate, report)
        report["rows"][0]["id"] = "held-out"
        test = evaluate_report(gate, report)
        self.assertEqual(test["coverage"], 0)
        self.assertIsNone(test["selective_error"])
        self.assertIsNone(test["savings_fraction"])

    def test_adequate_synthetic_calibration_and_actual_decision(self):
        # Algorithm fixture only. This does not measure Jev model quality.
        report = {"scope": scope_for("jev"), "rows": [
            {"id": f"cal-{i}", "scope": scope_for("jev"), "score": .99, "eligible": True, "correct": True}
            for i in range(600)]}
        gate = read_gate(calibrate_report(report))
        self.assertEqual(gate.threshold, .99)
        with patch.dict(os.environ, {"TYPESAFE_API_KEY": "unit-test-only"}):
            r = triage([ISSUE], provider="jev", gate=gate, transport=lambda *_: response())
        self.assertEqual(r["rows"][0]["action"], "accept")
        self.assertEqual(evaluate_report(gate, r)["selective_error"], 0)

    def test_input_limits_and_labels(self):
        for issues in [[], [ISSUE, ISSUE], [ISSUE | {"body": 4}], [ISSUE | {"body": "中"*6000}],
                       [ISSUE | {"expected": {"kind": "other"}}],
                       [ISSUE | {"expected": ISSUE["expected"] | {"kind": ["bug"]}}]]:
            with self.subTest(issues=str(issues)[:50]), self.assertRaises(ValueError):
                triage(issues)

    def test_path_boundary_nonfinite_and_overwrite(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)/"data"; root.mkdir()
            outside = Path(temp)/"out.json"; outside.write_text("[]")
            (root/"link.json").symlink_to(outside)
            for name in ["../out.json", "link.json", str(outside)]:
                with self.assertRaises(ValueError): read_json(name, root)
            path = root/"ok.json"; write_json(path, {"valid": True})
            with self.assertRaises(FileExistsError): write_json(path, {})
            self.assertEqual(read_json("ok.json", root), {"valid": True})
            path.write_text('{"bad": NaN}')
            with self.assertRaises(ValueError): read_json(path)


if __name__ == "__main__":
    unittest.main()
