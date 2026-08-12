"""SAT-entailment LogicAgent operating exclusively on public snapshots."""

from __future__ import annotations

from core.enums import Classification, Status, VerdictOutcome
from core.public_state import PublicKnowledgeState
from logic.cnf_encoder import CNFEncoder
from sat.dpll import DPLLSolver

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
            return HintResult(
                deduction,
                Classification.from_status(deduction.status),
                f"{deduction.character_id} is provably {deduction.status.value}.",
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
        encoder = CNFEncoder(public_state)
        variable = encoder.mapper.variable_for(character_id)
        encoding = encoder.build_kb()
        variable_count = encoding.primary_variable_count + encoding.auxiliary_variable_count
        active_clues = tuple(item.clue.id for item in public_state.revealed_clues)
        queries: list[SATQueryTrace] = []

        base = DPLLSolver().solve(encoding.clauses, variable_count)
        queries.append(self._query("KB", None, base))
        if not base.is_sat:
            return Classification.INCONSISTENT, self._trace(active_clues, character_id, queries, Classification.INCONSISTENT)

        assume_innocent = DPLLSolver().solve(encoding.clauses, variable_count, (-variable,))
        queries.append(self._query("assume INNOCENT", Status.INNOCENT, assume_innocent))
        if not assume_innocent.is_sat:
            return Classification.CRIMINAL, self._trace(active_clues, character_id, queries, Classification.CRIMINAL)

        assume_criminal = DPLLSolver().solve(encoding.clauses, variable_count, (variable,))
        queries.append(self._query("assume CRIMINAL", Status.CRIMINAL, assume_criminal))
        classification = Classification.INNOCENT if not assume_criminal.is_sat else Classification.UNKNOWN
        return classification, self._trace(active_clues, character_id, queries, classification)

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
    def _query(purpose: str, assumption: Status | None, result) -> SATQueryTrace:
        stats = result.statistics
        return SATQueryTrace(
            purpose,
            assumption,
            result.status.value,
            stats.decisions,
            stats.propagations,
            stats.backtracks,
            stats.runtime,
        )

    @staticmethod
    def _ordered_unresolved(public_state: PublicKnowledgeState):
        return tuple(
            character
            for character in sorted(public_state.characters, key=lambda item: (item.row, item.column, item.id))
            if public_state.status_of(character.id) is None
        )
