"""Development-only public FACT classifier used before the real SAT agent exists."""

from __future__ import annotations

from core.enums import Classification, ClueType, Status
from core.public_state import PublicKnowledgeState


class MockLogicAgent:
    """Classify explicit public FACTs; never inspect engine or hidden puzzle data.

    This is intentionally incomplete and must be replaced by the CNF/DPLL-backed
    production agent in the application. It remains only for focused legacy tests.
    """

    def classify(
        self,
        public_state: PublicKnowledgeState,
        character_id: str,
    ) -> Classification:
        character_ids = {character.id for character in public_state.characters}
        if character_id not in character_ids:
            raise KeyError(character_id)

        public_statuses: set[Status] = set()
        known = public_state.status_of(character_id)
        if known is not None:
            public_statuses.add(known)
        for revealed in public_state.revealed_clues:
            clue = revealed.clue
            if clue.type is ClueType.FACT and clue.target == character_id:
                public_statuses.add(clue.status)

        if len(public_statuses) > 1:
            return Classification.INCONSISTENT
        if public_statuses:
            return Classification.from_status(next(iter(public_statuses)))
        return Classification.UNKNOWN
