"""UI Phase 3 contracts for contextual verdict interaction and feedback."""

from __future__ import annotations

import unittest
from pathlib import Path

from agent.mock_logic_agent import MockLogicAgent
from core.enums import Classification, Status, VerdictOutcome
from core.results import VerdictResult
from game.game_engine import GameEngine
from game.puzzle_loader import PuzzleLoader
from gui.character_card import appearance_for
from gui.controller import GameController, SelectionRequiredError
from gui.feedback import FeedbackTone, feedback_for_verdict, newly_revealed_character
from gui.verdict_panel import verdict_context_for
from gui.view_model import build_card_views, compose_card_visual_state


PUZZLES = Path(__file__).parents[1] / "puzzles"
SAMPLE_PATH = PUZZLES / "sample_3x3.json"
FOUR_BY_FOUR_PATH = PUZZLES / "fact_chain_4x4.json"


class StaticAgent:
    def __init__(self, classification: Classification) -> None:
        self.classification = classification

    def classify(self, _public_state, _character_id: str) -> Classification:
        return self.classification


def card_for(state, character_id: str):
    return next(card for card in build_card_views(state) if card.character_id == character_id)


class VerdictContextTests(unittest.TestCase):
    def setUp(self) -> None:
        self.puzzle = PuzzleLoader.load(SAMPLE_PATH)
        self.engine = GameEngine(self.puzzle, MockLogicAgent())

    def test_verdict_buttons_are_disabled_without_unresolved_selection(self) -> None:
        self.assertFalse(verdict_context_for(None).can_submit)
        self.assertIn("select an unresolved character", verdict_context_for(None).identity.casefold())

        revealed = card_for(self.engine.public_state(), "A1")
        self.assertFalse(verdict_context_for(revealed).can_submit)

        unresolved = card_for(self.engine.public_state(), "B1")
        context = verdict_context_for(unresolved)
        self.assertTrue(context.can_submit)
        for public_identity in ("Ben", "B1", "Baker"):
            self.assertIn(public_identity, context.identity)

    def test_selecting_character_does_not_mutate_public_state(self) -> None:
        controller = GameController(self.engine)
        before = controller.state()
        controller.select_character("B1")
        self.assertEqual(controller.state(), before)

    def test_restart_and_load_clear_selection_and_prevent_stale_submission(self) -> None:
        controller = GameController(self.engine)
        controller.select_character("B1")
        controller.restart()
        self.assertIsNone(controller.selected_character_id)
        with self.assertRaises(SelectionRequiredError):
            controller.submit_selected(Status.INNOCENT)

        controller.select_character("B1")
        controller.load(PuzzleLoader.load(FOUR_BY_FOUR_PATH))
        self.assertIsNone(controller.selected_character_id)
        with self.assertRaises(SelectionRequiredError):
            controller.submit_selected(Status.INNOCENT)


class VerdictOutcomeFeedbackTests(unittest.TestCase):
    def setUp(self) -> None:
        self.puzzle = PuzzleLoader.load(SAMPLE_PATH)

    def test_accepted_uses_engine_api_and_reveals_exact_public_clue(self) -> None:
        controller = GameController(GameEngine(self.puzzle, MockLogicAgent()))
        controller.select_character("B1")
        before = controller.state()
        result = controller.submit_selected(Status.INNOCENT)
        after = controller.state()

        self.assertEqual(result.outcome, VerdictOutcome.ACCEPTED)
        self.assertIsNone(before.status_of("B1"))
        self.assertIsNone(before.clue_for("B1"))
        self.assertEqual(after.status_of("B1"), Status.INNOCENT)
        self.assertEqual(after.clue_for("B1").id, "CL-02")
        self.assertEqual(len(after.revealed_clues), len(before.revealed_clues) + 1)
        self.assertEqual(newly_revealed_character(result, before, after), "B1")

        feedback = feedback_for_verdict(result, card_for(after, "B1"))
        self.assertEqual(feedback.tone, FeedbackTone.SUCCESS)
        self.assertIn("Verdict accepted", feedback.title)

    def test_not_provable_preserves_public_state(self) -> None:
        engine = GameEngine(self.puzzle, StaticAgent(Classification.UNKNOWN))
        before = engine.public_state()
        result = engine.submit_verdict("B1", Status.CRIMINAL)
        after = engine.public_state()

        self.assertEqual(result.outcome, VerdictOutcome.NOT_PROVABLE)
        self.assertEqual(after, before)
        self.assertIsNone(newly_revealed_character(result, before, after))
        feedback = feedback_for_verdict(result, card_for(after, "B1"))
        self.assertEqual(feedback.tone, FeedbackTone.INFO)
        self.assertIn("does not force", feedback.message)

    def test_contradicted_preserves_state_and_reports_only_opposite(self) -> None:
        engine = GameEngine(self.puzzle, MockLogicAgent())
        before = engine.public_state()
        result = engine.submit_verdict("B1", Status.CRIMINAL)
        after = engine.public_state()

        self.assertEqual(result.outcome, VerdictOutcome.CONTRADICTED)
        self.assertEqual(after, before)
        feedback = feedback_for_verdict(result, card_for(after, "B1"))
        self.assertEqual(feedback.tone, FeedbackTone.WARNING)
        self.assertIn("forces the opposite verdict", feedback.message)
        self.assertNotIn(Status.INNOCENT.value, feedback.message)

    def test_inconsistent_does_not_reveal_and_has_error_feedback(self) -> None:
        engine = GameEngine(self.puzzle, StaticAgent(Classification.INCONSISTENT))
        before = engine.public_state()
        result = engine.submit_verdict("B1", Status.CRIMINAL)
        after = engine.public_state()

        self.assertEqual(result.outcome, VerdictOutcome.INCONSISTENT)
        self.assertEqual(after, before)
        self.assertIsNone(after.status_of("B1"))
        self.assertIsNone(after.clue_for("B1"))
        feedback = feedback_for_verdict(result, card_for(after, "B1"))
        self.assertEqual(feedback.tone, FeedbackTone.ERROR)
        self.assertIn("No character was revealed", feedback.message)

    def test_feedback_ignores_engine_message_and_forced_status_details(self) -> None:
        state = GameEngine(self.puzzle, MockLogicAgent()).public_state()
        result = VerdictResult(
            VerdictOutcome.CONTRADICTED,
            "B1",
            Status.CRIMINAL,
            forced_status=Status.INNOCENT,
            message="HIDDEN-SOLUTION-SENTINEL",
        )
        feedback = feedback_for_verdict(result, card_for(state, "B1"))
        visible = f"{feedback.title}\n{feedback.message}"
        self.assertNotIn("HIDDEN-SOLUTION-SENTINEL", visible)
        self.assertNotIn(Status.INNOCENT.value, visible)

    def test_new_reveal_modifier_is_presentation_only(self) -> None:
        engine = GameEngine(self.puzzle, MockLogicAgent())
        before = engine.public_state()
        result = engine.submit_verdict("B1", Status.INNOCENT)
        after = engine.public_state()
        card = card_for(after, "B1")

        normal = appearance_for(compose_card_visual_state(card))
        emphasized = appearance_for(compose_card_visual_state(card, newly_revealed=True))
        self.assertEqual(emphasized.surface, normal.surface)
        self.assertEqual(emphasized.badge_background, normal.badge_background)
        self.assertIsNotNone(emphasized.reveal_outline)
        self.assertEqual(newly_revealed_character(result, before, after), "B1")
        self.assertEqual(engine.public_state(), after)


if __name__ == "__main__":
    unittest.main()
