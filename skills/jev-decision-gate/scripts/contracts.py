"""Typed MCP result contracts; dictionaries from the SDK are validated against them."""
from dataclasses import dataclass
from typing import Literal


@dataclass
class GateSummary:
    scope: str
    threshold: float | None
    max_error: float
    delta: float
    calibration_accepted: int
    calibration_errors: int
    upper_error: float | None
    candidates_tested: int


@dataclass
class CalibrationResult:
    policy_id: str
    active: bool
    gate: GateSummary
    bound_scope: str
    lifetime: str


@dataclass
class EvaluationMetrics:
    total: int
    accepted: int
    accepted_errors: int
    coverage: float
    selective_error: float | None
    overall_error: float
    fallback_only_error: float
    observed_cost: float
    fallback_only_cost: float
    savings_fraction: float | None
    note: str


@dataclass
class EvaluationResult:
    policy_id: str
    metrics: EvaluationMetrics
    evidence: str


@dataclass
class Decision:
    id: str
    action: Literal["accept_cheap", "fallback"]
    reason: Literal["disabled_gate", "scope_mismatch", "ineligible", "below_threshold", "threshold_passed"]


@dataclass
class RoutingResult:
    policy_id: str
    decisions: list[Decision]
    executed_actions: Literal[False]
    note: str
