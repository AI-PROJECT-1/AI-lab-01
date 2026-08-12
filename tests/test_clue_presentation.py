"""UI Phase 4 public clue presentation and inspection contracts."""

from __future__ import annotations

import unittest
from pathlib import Path

from agent.mock_logic_agent import MockLogicAgent
from core.clue import Clue
from core.enums import ClueType, RegionType, Status
from core.public_state import PublicKnowledgeState, RevealedClue
from core.region import Region
from game.game_engine import GameEngine
from game.puzzle_loader import PuzzleLoader
from gui.character_card import appearance_for
from gui.clue_card import ClueCardModifiers, build_clue_views, clue_appearance_for
from gui.controller import GameController
from gui.view_model import CardBaseState, CardModifiers, CardVisualState
from tests.test_logic import make_grid_characters


PUZZLES = Path(__file__).parents[1] / "puzzles"
SAMPLE_PATH = PUZZLES / "sample_3x3.json"
FOUR_BY_FOUR_PATH = PUZZLES / "fact_chain_4x4.json"


class PublicStateEngineStub:
    def __init__(self, state: PublicKnowledgeState) -> None:
        self._state = state

    def public_state(self) -> PublicKnowledgeState:
        return self._state


def public_state_with(clues: tuple[Clue, ...]) -> PublicKnowledgeState:
    characters = make_grid_characters(3)
    return PublicKnowledgeState(
        "clue-presentation",
        "Clue Presentation",
        3,
        characters,
        tuple(RevealedClue(characters[index].id, clue) for index, clue in enumerate(clues)),
        (),
        False,
    )


class PublicClueViewTests(unittest.TestCase):
    def test_only_revealed_clues_appear_and_unrevealed_text_is_absent(self) -> None:
        puzzle = PuzzleLoader.load(SAMPLE_PATH)
        engine = GameEngine(puzzle, MockLogicAgent())
        views = build_clue_views(engine.public_state())

        self.assertEqual(len(views), 1)
        self.assertEqual(views[0].clue_id, "CL-01")
        self.assertNotIn("CL-02", repr(views))
        self.assertNotIn("C1 is criminal", repr(views))

    def test_owner_identity_clue_id_and_complete_public_text_remain_accessible(self) -> None:
        long_text = (
            "Exactly two publicly counted characters in this deliberately long explicit clue "
            "must be criminal, and every word must remain available to the player."
        )
        state = public_state_with(
            (Clue("LONG-01", ClueType.FACT, target="B1", status=Status.INNOCENT, text=long_text),)
        )
        view = build_clue_views(state)[0]

        self.assertEqual((view.owner_name, view.owner_coordinate), ("Name 11", "A1"))
        self.assertEqual(view.clue_id, "LONG-01")
        self.assertEqual(view.clue_text, long_text)
        for value in ("Name 11", "A1", "LONG-01", long_text):
            self.assertIn(value, view.visible_text())

    def test_no_reveals_builds_an_empty_public_view(self) -> None:
        self.assertEqual(build_clue_views(public_state_with(())), ())

    def test_selected_and_newly_revealed_states_compose(self) -> None:
        base = clue_appearance_for(ClueCardModifiers())
        combined = clue_appearance_for(ClueCardModifiers(selected=True, newly_revealed=True))
        self.assertEqual(combined.surface, base.surface)
        self.assertEqual(combined.border, base.border)
        self.assertIsNotNone(combined.selection_outline)
        self.assertIsNotNone(combined.reveal_outline)

    def test_newly_revealed_emphasis_does_not_mutate_public_state(self) -> None:
        state = public_state_with((Clue("F", ClueType.FACT, target="B1", status=Status.INNOCENT),))
        before = repr(state)
        clue_appearance_for(ClueCardModifiers(newly_revealed=True))
        self.assertEqual(repr(state), before)


class CanonicalClueSelectionTests(unittest.TestCase):
    def _select(self, clue: Clue) -> tuple[tuple[str, ...], PublicKnowledgeState, GameController]:
        state = public_state_with((clue,))
        controller = GameController(PublicStateEngineStub(state))
        before = controller.state()
        highlighted = controller.select_clue("A1")
        self.assertEqual(controller.state(), before)
        self.assertEqual(controller.selected_clue_owner_id, "A1")
        return highlighted, before, controller

    def test_fact_and_binary_clues_use_canonical_references(self) -> None:
        cases = (
            (Clue("F", ClueType.FACT, target="C2", status=Status.CRIMINAL), ("C2",)),
            (Clue("S", ClueType.SAME, characters=("A1", "B2")), ("A1", "B2")),
            (Clue("D", ClueType.DIFFERENT, characters=("C1", "A3")), ("C1", "A3")),
            (Clue("I", ClueType.IMPLIES, characters=("B1", "C3")), ("B1", "C3")),
        )
        for clue, expected in cases:
            with self.subTest(clue_type=clue.type):
                self.assertEqual(self._select(clue)[0], expected)

    def test_row_column_neighbor_explicit_and_odd_use_canonical_regions(self) -> None:
        cases = (
            (
                Clue("R", ClueType.EXACTLY, region=Region(RegionType.ROW, index=2), k=1),
                ("A2", "B2", "C2"),
            ),
            (
                Clue("C", ClueType.AT_LEAST, region=Region(RegionType.COLUMN, index=2), k=1),
                ("B1", "B2", "B3"),
            ),
            (
                Clue("N", ClueType.AT_MOST, region=Region(RegionType.NEIGHBORS, center="A1"), k=2),
                ("B1", "A2", "B2"),
            ),
            (
                Clue("X", ClueType.EXACTLY, region=Region(RegionType.EXPLICIT, cells=("C3", "A1")), k=1),
                ("C3", "A1"),
            ),
            (
                Clue("O", ClueType.ODD, region=Region(RegionType.EXPLICIT, cells=("A2", "C2", "B3"))),
                ("A2", "C2", "B3"),
            ),
        )
        for clue, expected in cases:
            with self.subTest(clue_type=clue.type, region=clue.region.kind):
                self.assertEqual(self._select(clue)[0], expected)

    def test_character_selection_and_clue_highlight_preserve_base_states(self) -> None:
        criminal = appearance_for(
            CardVisualState(CardBaseState.CRIMINAL, CardModifiers(selected=True, clue_highlighted=True))
        )
        innocent = appearance_for(
            CardVisualState(CardBaseState.INNOCENT, CardModifiers(clue_highlighted=True))
        )
        unresolved = appearance_for(
            CardVisualState(CardBaseState.UNRESOLVED, CardModifiers(clue_highlighted=True))
        )
        self.assertIsNotNone(criminal.selection_outline)
        for card in (criminal, innocent, unresolved):
            self.assertIsNotNone(card.highlight_outline)
        self.assertNotEqual(criminal.surface, innocent.surface)
        self.assertNotEqual(innocent.surface, unresolved.surface)

    def test_restart_and_load_clear_clue_selection(self) -> None:
        controller = GameController(GameEngine(PuzzleLoader.load(SAMPLE_PATH), MockLogicAgent()))
        controller.select_clue("A1")
        controller.restart()
        self.assertIsNone(controller.selected_clue_owner_id)

        controller.select_clue("A1")
        controller.load(PuzzleLoader.load(FOUR_BY_FOUR_PATH))
        self.assertIsNone(controller.selected_clue_owner_id)


if __name__ == "__main__":
    unittest.main()
