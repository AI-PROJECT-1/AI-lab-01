"""Public, report-friendly records for SAT-backed deductions."""

from __future__ import annotations

from dataclasses import dataclass, replace

from core.enums import Classification, Status


@dataclass(frozen=True, slots=True)
class SATQueryTrace:
    purpose: str
    assumption: Status | None
    result: str
    decisions: int
    propagations: int
    backtracks: int
    runtime: float


@dataclass(frozen=True, slots=True)
class DeductionTraceStep:
    step_number: int
    active_clue_ids: tuple[str, ...]
    character_id: str | None
    sat_queries: tuple[SATQueryTrace, ...]
    verdict: Classification
    newly_revealed_clue: str | None = None

    def with_revealed_clue(self, clue_id: str | None) -> "DeductionTraceStep":
        return replace(self, newly_revealed_clue=clue_id)

    def display_text(self) -> str:
        target = self.character_id or "KB"
        query_summary = ", ".join(
            f"{query.purpose}={query.result}" for query in self.sat_queries
        )
        reveal = f"; revealed {self.newly_revealed_clue}" if self.newly_revealed_clue else ""
        return f"Step {self.step_number}: {target} -> {self.verdict.value} ({query_summary}){reveal}"


@dataclass(frozen=True, slots=True)
class Deduction:
    character_id: str
    status: Status
    trace: DeductionTraceStep


@dataclass(frozen=True, slots=True)
class HintResult:
    deduction: Deduction | None
    classification: Classification
    message: str


@dataclass(frozen=True, slots=True)
class UniquenessResult:
    is_consistent: bool
    is_unique: bool
    first_model: dict[str, bool] | None
    sat_calls: int

