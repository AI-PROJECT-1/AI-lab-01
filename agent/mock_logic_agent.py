"""Development-only public FACT classifier used before the real SAT agent exists."""

from __future__ import annotations

from core.enums import Classification, ClueType, Status
from core.public_state import PublicKnowledgeState


class MockLogicAgent:
    """Classify explicit public FACTs; never inspect engine or hidden puzzle data.

    This is intentionally incomplete and must be replaced by the CNF/DPLL-backed
    agent during Phase 10. It exists only to exercise honest Phase 03-04 flows.
    """

    def classify(
        self,
        public_state: PublicKnowledgeState,
        character_id: str,
    ) -> Classification:
        character_ids = {character.id for character in public_state.characters}
        if character_id not in character_ids:
            raise KeyError(character_id)

        known = public_state.status_of(character_id)
        if known is not None:
            return Classification.from_status(known)

        fact_statuses: set[Status] = set()
        for revealed in public_state.revealed_clues:
            clue = revealed.clue
            if clue.type is ClueType.FACT and clue.target == character_id:
                fact_statuses.add(clue.status)

        if len(fact_statuses) > 1:
            return Classification.INCONSISTENT
        if fact_statuses:
            return Classification.from_status(next(iter(fact_statuses)))
        return Classification.UNKNOWN
