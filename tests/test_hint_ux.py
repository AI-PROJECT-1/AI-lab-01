"""UI Phase 5 contracts for progressive, public-only Hint presentation."""

from __future__ import annotations

import unittest
from dataclasses import replace
from pathlib import Path

from agent.deduction_trace import Deduction, DeductionTraceStep, HintResult
from agent.logic_agent import LogicAgent
from core.enums import Classification, Status
from core.public_state import PublicKnowledgeState
from game.game_engine import GameEngine
from game.puzzle_loader import PuzzleLoader
from gui.character_card import appearance_for
from gui.clue_card import ClueCardModifiers, clue_appearance_for
from gui.controller import GameController
from gui.hint_session import (
    HintStage,
    HintVisualState,
    begin_hint_session,
    can_advance_hint,
    fingerprint_public_state,
    progress_hint_session,
)
from gui.view_model import CardBaseState, CardModifiers, CardVisualState
from tests.fixture_paths import PUZZLE_FIXTURES


SAMPLE_PATH = PUZZLE_FIXTURES / "sample_3x3.json"
FOUR_BY_FOUR_PATH = PUZZLE_FIXTURES / "fact_chain_4x4.json"


class CountingController:
    def __init__(self, controller: GameController) -> None:
        self.controller = controller
        self.hint_calls = 0

    def state(self):
        return self.controller.state()

    def hint(self):
        self.hint_calls += 1
        return self.controller.hint()

    def trace(self):
        return self.controller.trace()


class ProgressiveHintSessionTests(unittest.TestCase):
    def setUp(self) -> None:
        engine = GameEngine(PuzzleLoader.load(SAMPLE_PATH), LogicAgent())
        self.controller = GameController(engine)
        self.counting = CountingController(self.controller)

    def _progress(self, session=None):
        return progress_hint_session(
            session,
            self.counting.state,
            self.counting.hint,
            self.counting.trace,
        )

    def test_first_click_calls_once_and_does_not_mutate_public_state(self) -> None:
        before = self.controller.state()
        session, presentation, reasoning = self._progress()
        self.assertTrue(reasoning)
        self.assertEqual(self.counting.hint_calls, 1)
        self.assertEqual(self.controller.state(), before)
        self.assertEqual(session.stage, HintStage.ACTIVE_CLUES)
        self.assertEqual(presentation.next_button_text, "Show target")

    def test_stage_one_filters_to_revealed_clues_and_avoids_causal_claims(self) -> None:
        session, presentation, _ = self._progress()
        public_ids = {item.clue.id for item in self.controller.state().revealed_clues}
        self.assertEqual(presentation.active_clue_ids, ("CL-01",))
        self.assertTrue(set(presentation.active_clue_ids).issubset(public_ids))
        self.assertNotIn("CL-02", repr(session))
        self.assertNotIn("C1 is criminal", presentation.message)
        for forbidden_claim in ("proves", "causes", "because of", "proof anchor is"):
            self.assertNotIn(forbidden_claim, presentation.message.casefold())

    def test_stage_two_uses_cache_and_shows_only_public_target_identity(self) -> None:
        session, _, _ = self._progress()
        trace_count = len(self.controller.trace())
        before = self.controller.state()
        session, presentation, reasoning = self._progress(session)

        self.assertFalse(reasoning)
        self.assertEqual(self.counting.hint_calls, 1)
        self.assertEqual(len(self.controller.trace()), trace_count)
        self.assertEqual(self.controller.state(), before)
        self.assertEqual(session.stage, HintStage.TARGET)
        self.assertEqual(presentation.target_character_id, "B1")
        self.assertEqual(presentation.message, "Focus on Ben · B1.")
        for hidden in ("INNOCENT", "CRIMINAL", "CL-02", "C1 is criminal"):
            self.assertNotIn(hidden, presentation.message)

    def test_one_two_stage_cycle_adds_at_most_one_reasoning_request(self) -> None:
        before_trace = len(self.controller.trace())
        session, _, _ = self._progress()
        after_stage_one = len(self.controller.trace())
        self._progress(session)
        self.assertEqual(self.counting.hint_calls, 1)
        self.assertGreater(after_stage_one, before_trace)
        self.assertEqual(len(self.controller.trace()), after_stage_one)

    def test_generic_stage_one_when_no_safe_active_clue_exists(self) -> None:
        state = self.controller.state()
        result = HintResult(None, Classification.UNKNOWN, "SENTINEL")
        session, presentation = begin_hint_session(state, result, ())
        self.assertEqual(session.active_clue_ids, ())
        self.assertIn("currently revealed public information", presentation.message)
        self.assertIn("No specific proof anchor", presentation.message)
        self.assertNotIn("SENTINEL", presentation.message)

    def test_unrevealed_trace_id_is_filtered_even_if_supplied(self) -> None:
        state = self.controller.state()
        real = self.controller.hint()
        malicious_trace = replace(real.deduction.trace, active_clue_ids=("CL-01", "CL-02", "SECRET"))
        result = HintResult(
            Deduction(real.deduction.character_id, real.deduction.status, malicious_trace),
            real.classification,
            "hidden status message",
        )
        session, presentation = begin_hint_session(state, result, (malicious_trace,))
        self.assertEqual(session.active_clue_ids, ("CL-01",))
        self.assertNotIn("CL-02", repr(presentation))
        self.assertNotIn("hidden status message", repr(presentation))

    def test_changed_public_state_never_advances_stale_target(self) -> None:
        session, _, _ = self._progress()
        self.controller.select_character("B1")
        self.controller.submit_selected(Status.INNOCENT)
        self.assertFalse(can_advance_hint(session, self.controller.state()))

        new_session, presentation, reasoning = self._progress(session)
        self.assertTrue(reasoning)
        self.assertEqual(self.counting.hint_calls, 2)
        self.assertEqual(new_session.stage, HintStage.ACTIVE_CLUES)
        self.assertIsNone(presentation.target_character_id)
        self.assertNotIn("Focus on Ben", presentation.message)

    def test_character_and_clue_selection_do_not_invalidate_unchanged_hint(self) -> None:
        session, _, _ = self._progress()
        fingerprint = session.fingerprint
        self.controller.select_character("C1")
        self.controller.select_clue("A1")
        self.assertEqual(fingerprint_public_state(self.controller.state()), fingerprint)
        self.assertTrue(can_advance_hint(session, self.controller.state()))
        self._progress(session)
        self.assertEqual(self.counting.hint_calls, 1)

    def test_manual_accepted_solve_next_and_auto_reveal_change_fingerprint(self) -> None:
        session, _, _ = self._progress()
        self.controller.select_character("B1")
        self.controller.submit_selected(Status.INNOCENT)
        self.assertFalse(can_advance_hint(session, self.controller.state()))

        controller = GameController(GameEngine(PuzzleLoader.load(SAMPLE_PATH), LogicAgent()))
        original = fingerprint_public_state(controller.state())
        controller.solve_next()
        self.assertNotEqual(fingerprint_public_state(controller.state()), original)

        controller = GameController(GameEngine(PuzzleLoader.load(SAMPLE_PATH), LogicAgent()))
        original = fingerprint_public_state(controller.state())
        controller.auto_solve()
        self.assertNotEqual(fingerprint_public_state(controller.state()), original)

    def test_restart_and_load_states_do_not_match_old_session(self) -> None:
        session, _, _ = self._progress()
        self.controller.select_character("B1")
        self.controller.submit_selected(Status.INNOCENT)
        self.controller.restart()
        self.assertEqual(self.controller.state(), GameEngine(PuzzleLoader.load(SAMPLE_PATH), LogicAgent()).public_state())

        visual = HintVisualState(session, ("CL-01",), "B1")
        visual.invalidate()
        self.assertIsNone(visual.session)
        self.assertEqual(visual.active_clue_ids, ())
        self.assertIsNone(visual.target_character_id)

        old_fingerprint = session.fingerprint
        self.controller.load(PuzzleLoader.load(FOUR_BY_FOUR_PATH))
        self.assertNotEqual(fingerprint_public_state(self.controller.state()), old_fingerprint)


class HintModifierCompositionTests(unittest.TestCase):
    def test_hint_target_composes_with_all_character_modifiers(self) -> None:
        appearance = appearance_for(
            CardVisualState(
                CardBaseState.CRIMINAL,
                CardModifiers(
                    selected=True,
                    clue_highlighted=True,
                    newly_revealed=True,
                    hint_target=True,
                ),
            )
        )
        self.assertIsNotNone(appearance.selection_outline)
        self.assertIsNotNone(appearance.highlight_outline)
        self.assertIsNotNone(appearance.reveal_outline)
        self.assertIsNotNone(appearance.hint_outline)
        self.assertIsNotNone(appearance.badge_background)

    def test_active_hint_clue_composes_with_selected_and_newly_revealed(self) -> None:
        base = clue_appearance_for(ClueCardModifiers())
        combined = clue_appearance_for(
            ClueCardModifiers(selected=True, newly_revealed=True, hint_active=True)
        )
        self.assertEqual(combined.surface, base.surface)
        self.assertIsNotNone(combined.selection_outline)
        self.assertIsNotNone(combined.reveal_outline)
        self.assertIsNotNone(combined.hint_outline)


if __name__ == "__main__":
    unittest.main()
