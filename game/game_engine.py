"""Authoritative state machine for progressive Griductive gameplay."""

from __future__ import annotations

from agent.protocols import LogicAgentProtocol
from core.enums import Classification, Status, VerdictOutcome
from core.public_state import KnownVerdict, PublicKnowledgeState, RevealedClue
from core.puzzle import Puzzle
from core.results import VerdictResult


class AgentIntegrityError(RuntimeError):
    """Raised when an agent's forced verdict conflicts with the hidden solution."""


class GameEngine:
    """Own hidden puzzle data and expose commands plus immutable public snapshots."""

    def __init__(self, puzzle: Puzzle, agent: LogicAgentProtocol) -> None:
        self._agent = agent
        self._puzzle = puzzle
        self._revealed_ids: set[str] = set()
        self._known_statuses: dict[str, Status] = {}
        self.restart()

    def load(self, puzzle: Puzzle) -> PublicKnowledgeState:
        self._puzzle = puzzle
        return self.restart()

    def restart(self) -> PublicKnowledgeState:
        self._revealed_ids = set(self._puzzle.initially_revealed_ids)
        self._known_statuses = {
            character_id: self._puzzle.card_by_id(character_id).hidden_status
            for character_id in self._puzzle.initially_revealed_ids
        }
        return self.public_state()

    def public_state(self) -> PublicKnowledgeState:
        cards = self._puzzle.ordered_cards
        return PublicKnowledgeState(
            puzzle_id=self._puzzle.id,
            title=self._puzzle.title,
            size=self._puzzle.size,
            characters=tuple(card.character for card in cards),
            revealed_clues=tuple(
                RevealedClue(card.character.id, card.clue)
                for card in cards
                if card.character.id in self._revealed_ids
            ),
            known_verdicts=tuple(
                KnownVerdict(card.character.id, self._known_statuses[card.character.id])
                for card in cards
                if card.character.id in self._known_statuses
            ),
            is_complete=len(self._known_statuses) == len(cards),
        )

    def submit_verdict(self, character_id: str, status: Status) -> VerdictResult:
        try:
            card = self._puzzle.card_by_id(character_id)
        except KeyError as exc:
            raise ValueError(f"unknown character id: {character_id}") from exc
        if not isinstance(status, Status):
            raise TypeError("status must be a Status")

        already_known = self._known_statuses.get(character_id)
        if already_known is not None:
            if already_known is status:
                return VerdictResult(
                    VerdictOutcome.ACCEPTED,
                    character_id,
                    status,
                    forced_status=already_known,
                    message="This verdict is already public.",
                )
            return VerdictResult(
                VerdictOutcome.CONTRADICTED,
                character_id,
                status,
                forced_status=already_known,
                message=f"The public status is {already_known.value}.",
            )

        classification = self._agent.classify(self.public_state(), character_id)
        if classification is Classification.INCONSISTENT:
            return VerdictResult(
                VerdictOutcome.INCONSISTENT,
                character_id,
                status,
                message="The public knowledge state is inconsistent.",
            )
        forced_status = classification.as_status()
        if forced_status is None:
            return VerdictResult(
                VerdictOutcome.NOT_PROVABLE,
                character_id,
                status,
                message="Neither verdict is forced by the public knowledge.",
            )
        if forced_status is not status:
            return VerdictResult(
                VerdictOutcome.CONTRADICTED,
                character_id,
                status,
                forced_status=forced_status,
                message=f"The opposite verdict ({forced_status.value}) is forced.",
            )
        if card.hidden_status is not forced_status:
            raise AgentIntegrityError(
                f"agent verdict {forced_status.value} for {character_id} conflicts with puzzle data"
            )

        self._known_statuses[character_id] = forced_status
        self._revealed_ids.add(character_id)
        return VerdictResult(
            VerdictOutcome.ACCEPTED,
            character_id,
            status,
            forced_status=forced_status,
            revealed_clue=card.clue,
            message=f"{character_id} is proved {forced_status.value}; clue {card.clue.id} revealed.",
        )
