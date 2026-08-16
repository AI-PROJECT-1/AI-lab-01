"""Pure SAT entailment checks shared by deduction and Hint diagnostics."""

from __future__ import annotations

from dataclasses import dataclass

from agent.deduction_trace import SATQueryTrace
from core.enums import Classification, Status
from core.public_state import PublicKnowledgeState
from logic.cnf_encoder import CNFEncoder
from sat.dpll import DPLLSolver


@dataclass(frozen=True, slots=True)
class EntailmentCheck:
    classification: Classification
    sat_queries: tuple[SATQueryTrace, ...]

    @property
    def sat_calls(self) -> int:
        return len(self.sat_queries)


def classify_public_target(
    public_state: PublicKnowledgeState,
    character_id: str,
) -> EntailmentCheck:
    """Classify one public target without producing a deduction trace step."""

    encoder = CNFEncoder(public_state)
    variable = encoder.mapper.variable_for(character_id)
    encoding = encoder.build_kb()
    variable_count = encoding.primary_variable_count + encoding.auxiliary_variable_count
    queries: list[SATQueryTrace] = []

    base = DPLLSolver().solve(encoding.clauses, variable_count)
    queries.append(_query_trace("KB", None, base))
    if not base.is_sat:
        return EntailmentCheck(Classification.INCONSISTENT, tuple(queries))

    assume_innocent = DPLLSolver().solve(encoding.clauses, variable_count, (-variable,))
    queries.append(_query_trace("assume INNOCENT", Status.INNOCENT, assume_innocent))
    if not assume_innocent.is_sat:
        return EntailmentCheck(Classification.CRIMINAL, tuple(queries))

    assume_criminal = DPLLSolver().solve(encoding.clauses, variable_count, (variable,))
    queries.append(_query_trace("assume CRIMINAL", Status.CRIMINAL, assume_criminal))
    classification = Classification.INNOCENT if not assume_criminal.is_sat else Classification.UNKNOWN
    return EntailmentCheck(classification, tuple(queries))


def _query_trace(purpose: str, assumption: Status | None, result) -> SATQueryTrace:
    statistics = result.statistics
    return SATQueryTrace(
        purpose,
        assumption,
        result.status.value,
        statistics.decisions,
        statistics.propagations,
        statistics.backtracks,
        statistics.runtime,
    )
