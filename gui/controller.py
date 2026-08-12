"""Headless-testable controller for manual GUI actions."""

from __future__ import annotations

from core.enums import Status
from core.public_state import PublicKnowledgeState
from core.puzzle import Puzzle
from core.results import VerdictResult
from game.game_engine import GameEngine


class SelectionRequiredError(ValueError):
    pass


class GameController:
    def __init__(self, engine: GameEngine) -> None:
        self._engine = engine
        self._selected_character_id: str | None = None
        self._selected_clue_owner_id: str | None = None

    @property
    def selected_character_id(self) -> str | None:
        return self._selected_character_id

    @property
    def selected_clue_owner_id(self) -> str | None:
        return self._selected_clue_owner_id

    def state(self) -> PublicKnowledgeState:
        return self._engine.public_state()

    def select_character(self, character_id: str) -> None:
        if character_id not in {item.id for item in self.state().characters}:
            raise ValueError(f"unknown character id: {character_id}")
        self._selected_character_id = character_id

    def select_clue(self, owner_id: str) -> tuple[str, ...]:
        state = self.state()
        clue = state.clue_for(owner_id)
        if clue is None:
            raise ValueError(f"owner {owner_id} has no revealed clue")
        self._selected_clue_owner_id = owner_id
        from logic.region_resolver import referenced_cells

        return referenced_cells(clue, state.characters)

    def submit_selected(self, status: Status) -> VerdictResult:
        if self._selected_character_id is None:
            raise SelectionRequiredError("select a character before submitting a verdict")
        return self._engine.submit_verdict(self._selected_character_id, status)

    def restart(self) -> PublicKnowledgeState:
        self._selected_character_id = None
        self._selected_clue_owner_id = None
        return self._engine.restart()

    def load(self, puzzle: Puzzle) -> PublicKnowledgeState:
        self._selected_character_id = None
        self._selected_clue_owner_id = None
        return self._engine.load(puzzle)

    def hint(self):
        return self._engine.get_hint()

    def solve_next(self) -> VerdictResult | None:
        return self._engine.solve_next()

    def auto_solve(self) -> tuple[VerdictResult, ...]:
        return self._engine.auto_solve()

    def trace(self):
        return self._engine.deduction_trace
