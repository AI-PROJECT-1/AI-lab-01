"""Authoritative state machine for progressive Griductive gameplay."""

from __future__ import annotations

from agent.deduction_trace import DeductionTraceStep, HintResult
from agent.protocols import LogicAgentProtocol, ProgressiveLogicAgentProtocol
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
        self._trace: list[DeductionTraceStep] = []
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
        self._trace = []
        if hasattr(self._agent, "reset_trace"):
            self._agent.reset_trace()
        return self.public_state()

    @property
    def deduction_trace(self) -> tuple[DeductionTraceStep, ...]:
        return tuple(self._trace)

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
        self._capture_agent_trace()
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
        return self._accept_deduction(character_id, forced_status)

    def get_hint(self) -> HintResult:
        agent = self._progressive_agent()
        hint = agent.get_hint(self.public_state())
        self._capture_agent_trace()
        return hint

    def solve_next(self) -> VerdictResult | None:
        agent = self._progressive_agent()
        deduction = agent.solve_next(self.public_state())
        self._capture_agent_trace()
        if deduction is None:
            return None
        return self._accept_deduction(deduction.character_id, deduction.status)

    def auto_solve(self) -> tuple[VerdictResult, ...]:
        """Progressively rebuild the public KB after every accepted reveal."""

        results: list[VerdictResult] = []
        while not self.public_state().is_complete:
            result = self.solve_next()
            if result is None:
                break
            results.append(result)
        return tuple(results)

    def _accept_deduction(self, character_id: str, status: Status) -> VerdictResult:
        card = self._puzzle.card_by_id(character_id)
        if card.hidden_status is not status:
            raise AgentIntegrityError(
                f"agent verdict {status.value} for {character_id} conflicts with puzzle data"
            )
        self._known_statuses[character_id] = status
        self._revealed_ids.add(character_id)
        if self._trace:
            self._trace[-1] = self._trace[-1].with_revealed_clue(card.clue.id)
        return VerdictResult(
            VerdictOutcome.ACCEPTED,
            character_id,
            status,
            forced_status=status,
            revealed_clue=card.clue,
            message=f"{character_id} is proved {status.value}; clue {card.clue.id} revealed.",
        )

    def _progressive_agent(self) -> ProgressiveLogicAgentProtocol:
        if not isinstance(self._agent, ProgressiveLogicAgentProtocol):
            raise RuntimeError("the configured agent does not support progressive deduction")
        return self._agent

    def _capture_agent_trace(self) -> None:
        trace = getattr(self._agent, "last_trace", ())
        if trace:
            self._trace.extend(trace)
