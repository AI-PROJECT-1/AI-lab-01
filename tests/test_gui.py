"""Headless Level 9 tests for the GUI controller and view models."""

from __future__ import annotations

import unittest
from pathlib import Path

from agent.mock_logic_agent import MockLogicAgent
from agent.logic_agent import LogicAgent
from core.enums import Status, VerdictOutcome
from game.game_engine import GameEngine
from game.puzzle_loader import PuzzleLoader
from gui.app import DEFAULT_PUZZLE
from gui.controller import GameController, SelectionRequiredError
from gui.view_model import build_card_views


SAMPLE_PATH = Path(__file__).parents[1] / "puzzles" / "sample_3x3.json"


class ViewModelTests(unittest.TestCase):
    def setUp(self) -> None:
        puzzle = PuzzleLoader.load(SAMPLE_PATH)
        self.engine = GameEngine(puzzle, MockLogicAgent())

    def test_cards_show_public_metadata_and_face_state(self) -> None:
        cards = build_card_views(self.engine.public_state())
        self.assertEqual(tuple(card.character_id for card in cards), ("A1", "B1", "C1", "A2", "B2", "C2", "A3", "B3", "C3"))
        self.assertTrue(cards[0].face_up)
        self.assertEqual(cards[0].status, Status.CRIMINAL)
        self.assertIn("CRIMINAL", cards[0].visible_text())
        self.assertIn("B1 is innocent", cards[0].visible_text())
        self.assertFalse(cards[1].face_up)
        unresolved_text = cards[1].visible_text()
        self.assertIn("B1", unresolved_text)
        self.assertIn("Ben", unresolved_text)
        self.assertIn("Baker", unresolved_text)
        for forbidden in ("UNKNOWN", "FACE-DOWN", "Clue: hidden", "CL-02"):
            self.assertNotIn(forbidden, unresolved_text)

    def test_accepted_verdict_flips_card_view(self) -> None:
        self.engine.submit_verdict("B1", Status.INNOCENT)
        card = build_card_views(self.engine.public_state())[1]
        self.assertTrue(card.face_up)
        self.assertEqual((card.status, card.clue_id), (Status.INNOCENT, "CL-02"))
        self.assertIn("INNOCENT", card.visible_text())
        self.assertIn("C1 is criminal", card.visible_text())

    def test_unrevealed_clue_appears_only_after_public_reveal(self) -> None:
        before = build_card_views(self.engine.public_state())[1]
        self.assertIsNone(before.clue_text)
        self.assertNotIn("C1 is criminal", before.visible_text())

        self.engine.submit_verdict("B1", Status.INNOCENT)
        after = build_card_views(self.engine.public_state())[1]
        self.assertEqual(after.clue_text, "C1 is criminal.")
        self.assertIn("C1 is criminal", after.visible_text())


class ControllerTests(unittest.TestCase):
    def setUp(self) -> None:
        puzzle = PuzzleLoader.load(SAMPLE_PATH)
        self.controller = GameController(GameEngine(puzzle, MockLogicAgent()))

    def test_manual_selection_and_verdict_flow(self) -> None:
        with self.assertRaises(SelectionRequiredError):
            self.controller.submit_selected(Status.CRIMINAL)
        self.controller.select_character("B1")
        contradicted = self.controller.submit_selected(Status.CRIMINAL)
        self.assertEqual(contradicted.outcome, VerdictOutcome.CONTRADICTED)
        accepted = self.controller.submit_selected(Status.INNOCENT)
        self.assertEqual(accepted.outcome, VerdictOutcome.ACCEPTED)

    def test_restart_clears_selection_and_progress(self) -> None:
        self.controller.select_character("B1")
        self.controller.submit_selected(Status.INNOCENT)
        state = self.controller.restart()
        self.assertIsNone(self.controller.selected_character_id)
        self.assertIsNone(state.status_of("B1"))

    def test_default_puzzle_exists(self) -> None:
        self.assertEqual(DEFAULT_PUZZLE.resolve(), SAMPLE_PATH.resolve())
        self.assertTrue(DEFAULT_PUZZLE.is_file())

    def test_canonical_clue_highlighting(self) -> None:
        self.assertEqual(self.controller.select_clue("A1"), ("B1",))

        extension_path = SAMPLE_PATH.with_name("extension_chain_3x3.json")
        controller = GameController(GameEngine(PuzzleLoader.load(extension_path), LogicAgent()))
        controller.solve_next()
        self.assertEqual(controller.select_clue("B1"), ("B1", "C1"))
        controller.solve_next()
        self.assertEqual(controller.select_clue("C1"), ("C1", "A2"))

    def test_progressive_controls_use_real_agent(self) -> None:
        controller = GameController(GameEngine(PuzzleLoader.load(SAMPLE_PATH), LogicAgent()))
        before = controller.state()
        hint = controller.hint()
        self.assertEqual(controller.state(), before)
        self.assertEqual(hint.deduction.character_id, "B1")
        first = controller.solve_next()
        self.assertEqual(first.character_id, "B1")
        remaining = controller.auto_solve()
        self.assertEqual(len(remaining), 7)
        self.assertTrue(controller.state().is_complete)


if __name__ == "__main__":
    unittest.main()
