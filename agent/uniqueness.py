"""Uniqueness checking for a deliberately supplied complete clue set."""

from __future__ import annotations

from agent.deduction_trace import UniquenessResult
from core.public_state import PublicKnowledgeState
from logic.cnf_encoder import CNFEncoder
from sat.dpll import DPLLSolver


def check_complete_clue_set_uniqueness(complete_state: PublicKnowledgeState) -> UniquenessResult:
    """Check uniqueness of clues in ``complete_state``, never of a gameplay KB implicitly.

    The caller must explicitly construct a state containing the complete clue set.
    Hidden labels are neither accepted nor required.
    """

    character_ids = {character.id for character in complete_state.characters}
    clue_owner_ids = {revealed.owner_id for revealed in complete_state.revealed_clues}
    if clue_owner_ids != character_ids:
        raise ValueError("uniqueness requires the complete clue set")
    if complete_state.known_verdicts:
        raise ValueError("uniqueness must use complete clues without verdict unit clauses")

    encoder = CNFEncoder(complete_state)
    encoding = encoder.build_kb()
    variable_count = encoding.primary_variable_count + encoding.auxiliary_variable_count
    first = DPLLSolver().solve(encoding.clauses, variable_count)
    if not first.is_sat:
        return UniquenessResult(False, False, None, 1)

    blocking_clause = tuple(
        -variable if first.assignment[variable] else variable
        for variable in range(1, encoding.primary_variable_count + 1)
    )
    second = DPLLSolver().solve((*encoding.clauses, blocking_clause), variable_count)
    model = {
        encoder.mapper.character_id_for(variable): first.assignment[variable]
        for variable in encoder.mapper.variables
    }
    return UniquenessResult(True, not second.is_sat, model, 2)
