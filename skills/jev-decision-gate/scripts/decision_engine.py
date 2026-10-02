"""Local decision-gate SDK; scores and truth labels come from the caller."""
from __future__ import annotations
import hashlib
import json
import math
from dataclasses import asdict
from pathlib import Path
from threading import Lock
from risk_gate import Gate, evaluate, fit_gate


class DecisionEngine:
    """One trusted local workspace and a bounded, process-local policy registry."""
    def __init__(self, data_root: str | Path):
        self.root = Path(data_root).resolve(strict=True)
        if not self.root.is_dir():
            raise ValueError("data_root must be a directory")
        self.policies: dict[str, Gate] = {}
        self.lock = Lock()

    def read_rows(self, relative_file: str, limit: int = 5000) -> list[dict]:
        path = Path(relative_file)
        if path.is_absolute():
            raise ValueError("use a path relative to data_root")
        path = (self.root / path).resolve(strict=True)
        if not path.is_relative_to(self.root) or not path.is_file():
            raise ValueError("file must remain within data_root")
        if path.suffix != ".json":
            raise ValueError("only JSON dataset files are accepted")
        with path.open("rb") as stream:
            raw = stream.read(8 * 1024 * 1024 + 1)
        if len(raw) > 8 * 1024 * 1024:
            raise ValueError("dataset exceeds 8 MiB")
        rows = json.loads(raw)
        if not isinstance(rows, list) or not 1 <= len(rows) <= limit:
            raise ValueError(f"dataset must contain 1..{limit} rows")
        if any(not isinstance(r, dict) for r in rows):
            raise ValueError("each row must be an object")
        return rows

    def calibrate(self, calibration_file: str, scope: str,
                  max_error: float = .05, delta: float = .05) -> dict:
        rows = self.read_rows(calibration_file)
        gate, _ = fit_gate(rows, scope, max_error, delta)
        digest = hashlib.sha256(json.dumps(
            {"rows": rows, "scope": scope, "max_error": max_error,
             "delta": delta, "engine": "0.2.0"},
            sort_keys=True, allow_nan=False).encode()).hexdigest()
        policy_id = "gate_" + digest[:24]
        with self.lock:
            if policy_id not in self.policies and len(self.policies) >= 32:
                raise ValueError("32 policies loaded; restart and recalibrate to clear")
            self.policies[policy_id] = gate
        summary = {k: v for k, v in asdict(gate).items() if k != "calibration_ids"}
        return {"policy_id": policy_id, "active": gate.threshold is not None,
                "gate": summary,
                "bound_scope": "Accepted predictions only, under a frozen model, score mapping and i.i.d. data; no drift guarantee.",
                "lifetime": "This server process; recalibrate after restart."}

    def policy(self, policy_id: str) -> Gate:
        with self.lock:
            if policy_id not in self.policies:
                raise ValueError("unknown policy_id; call calibrate_gate in this process")
            return self.policies[policy_id]

    def evaluate(self, policy_id: str, test_file: str) -> dict:
        return {"policy_id": policy_id,
                "metrics": evaluate(self.policy(policy_id), self.read_rows(test_file)),
                "evidence": "Caller-supplied labeled traces, offline replay; not a production savings claim."}

    def route(self, policy_id: str, requests_file: str) -> dict:
        gate = self.policy(policy_id)
        rows = self.read_rows(requests_file, limit=200)
        decisions, seen = [], set()
        for row in rows:
            identifier = row.get("id")
            if not isinstance(identifier, str) or not 1 <= len(identifier) <= 128 or identifier in seen:
                raise ValueError("request IDs must be unique strings of 1..128 characters")
            seen.add(identifier)
            if not isinstance(row.get("scope"), str) or not row["scope"]:
                raise ValueError("each request needs a scope")
            if type(row.get("eligible")) is not bool:
                raise ValueError("eligible must be bool")
            score = row.get("score")
            if type(score) not in (int, float) or not math.isfinite(score) or not 0 <= score <= 1:
                raise ValueError("score must be finite and in [0, 1]")
            reason = ("disabled_gate" if gate.threshold is None else
                      "scope_mismatch" if row["scope"] != gate.scope else
                      "ineligible" if not row["eligible"] else
                      "below_threshold" if score < gate.threshold else "threshold_passed")
            decisions.append({"id": identifier,
                              "action": "accept_cheap" if gate.accepts(row) else "fallback",
                              "reason": reason})
        return {"policy_id": policy_id, "decisions": decisions,
                "executed_actions": False,
                "note": "Recommendations from supplied scores, not semantic inference or a correctness guarantee."}
