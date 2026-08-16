"""SAT-entailment LogicAgent operating exclusively on public snapshots."""

from __future__ import annotations

from core.enums import Classification, Status, VerdictOutcome
from core.public_state import PublicKnowledgeState
from agent.entailment import classify_public_target
from agent.hint_explanation import extract_irreducible_support

from agent.deduction_trace import (
    Deduction,
    DeductionTraceStep,
    HintResult,
    SATQueryTrace,
    UniquenessResult,
)
from agent.uniqueness import check_complete_clue_set_uniqueness


class LogicAgent:
    """Prove verdicts with SAT assumptions; never inspect a Puzzle or GameEngine."""

    def __init__(self) -> None:
        self._step_number = 0
        self.last_trace: tuple[DeductionTraceStep, ...] = ()

    def reset_trace(self) -> None:
        self._step_number = 0
        self.last_trace = ()

    def classify(self, public_state: PublicKnowledgeState, character_id: str) -> Classification:
        classification, trace = self._classify_one(public_state, character_id)
        self.last_trace = (trace,)
        return classification

    def classify_all(self, public_state: PublicKnowledgeState) -> dict[str, Classification]:
        results: dict[str, Classification] = {}
        traces: list[DeductionTraceStep] = []
        for character in self._ordered_unresolved(public_state):
            classification, trace = self._classify_one(public_state, character.id)
            results[character.id] = classification
            traces.append(trace)
            if classification is Classification.INCONSISTENT:
                break
        self.last_trace = tuple(traces)
        return results

    def check_verdict(
        self,
        public_state: PublicKnowledgeState,
        character_id: str,
        requested_status: Status,
    ) -> VerdictOutcome:
        if not isinstance(requested_status, Status):
            raise TypeError("requested_status must be a Status")
        classification = self.classify(public_state, character_id)
        if classification is Classification.INCONSISTENT:
            return VerdictOutcome.INCONSISTENT
        forced = classification.as_status()
        if forced is None:
            return VerdictOutcome.NOT_PROVABLE
        return VerdictOutcome.ACCEPTED if forced is requested_status else VerdictOutcome.CONTRADICTED

    def get_hint(self, public_state: PublicKnowledgeState) -> HintResult:
        deduction = self.solve_next(public_state)
        if deduction is not None:
            try:
                explanation = extract_irreducible_support(
                    public_state,
                    deduction.character_id,
                    deduction.status,
                )
            except Exception:
                explanation = None
            return HintResult(
                deduction,
                Classification.from_status(deduction.status),
                f"{deduction.character_id} is provably {deduction.status.value}.",
                explanation,
            )
        if self.last_trace and self.last_trace[-1].verdict is Classification.INCONSISTENT:
            return HintResult(None, Classification.INCONSISTENT, "The public knowledge base is inconsistent.")
        return HintResult(None, Classification.UNKNOWN, "No unresolved verdict is currently forced.")

    def solve_next(self, public_state: PublicKnowledgeState) -> Deduction | None:
        traces: list[DeductionTraceStep] = []
        for character in self._ordered_unresolved(public_state):
            classification, trace = self._classify_one(public_state, character.id)
            traces.append(trace)
            status = classification.as_status()
            if status is not None:
                self.last_trace = tuple(traces)
                return Deduction(character.id, status, trace)
            if classification is Classification.INCONSISTENT:
                self.last_trace = tuple(traces)
                return None
        self.last_trace = tuple(traces)
        return None

    def auto_solve(self, public_state: PublicKnowledgeState) -> tuple[Deduction, ...]:
        """Return the deterministic wave of verdicts forced by this public KB.

        GameEngine is responsible for revealing cards and requesting later waves.
        """

        deductions: list[Deduction] = []
        traces: list[DeductionTraceStep] = []
        for character in self._ordered_unresolved(public_state):
            classification, trace = self._classify_one(public_state, character.id)
            traces.append(trace)
            status = classification.as_status()
            if status is not None:
                deductions.append(Deduction(character.id, status, trace))
            elif classification is Classification.INCONSISTENT:
                break
        self.last_trace = tuple(traces)
        return tuple(deductions)

    def check_uniqueness(self, complete_state: PublicKnowledgeState) -> UniquenessResult:
        return check_complete_clue_set_uniqueness(complete_state)

    def _classify_one(
        self,
        public_state: PublicKnowledgeState,
        character_id: str,
    ) -> tuple[Classification, DeductionTraceStep]:
        active_clues = tuple(item.clue.id for item in public_state.revealed_clues)
        check = classify_public_target(public_state, character_id)
        return check.classification, self._trace(
            active_clues,
            character_id,
            list(check.sat_queries),
            check.classification,
        )

    def _trace(
        self,
        active_clues: tuple[str, ...],
        character_id: str,
        queries: list[SATQueryTrace],
        verdict: Classification,
    ) -> DeductionTraceStep:
        self._step_number += 1
        return DeductionTraceStep(
            self._step_number,
            active_clues,
            character_id,
            tuple(queries),
            verdict,
        )

    @staticmethod
    def _ordered_unresolved(public_state: PublicKnowledgeState):
        return tuple(
            character
            for character in sorted(public_state.characters, key=lambda item: (item.row, item.column, item.id))
            if public_state.status_of(character.id) is None
        )
