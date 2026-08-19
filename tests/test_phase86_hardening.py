"""Phase 8.6 production-catalog, puzzle-hardening, and manual-lock gates."""

from __future__ import annotations

from dataclasses import fields
from pathlib import Path
import tkinter as tk
import unittest

from agent.logic_agent import LogicAgent
from core.enums import Classification, Status, VerdictOutcome
from core.public_state import PublicKnowledgeState
from experiments.analyze_puzzles import analyze_puzzle
from experiments.run_experiments import puzzle_paths
from game.game_engine import GameEngine
from game.puzzle_loader import PuzzleLoader
from gui.app import DEFAULT_PUZZLE, GriductiveApp
from gui.character_card import appearance_for
from gui.controller import GameController, ManualVerdictLockedError
from gui.hint_session import progress_hint_session
from gui.puzzle_catalog import PUZZLE_CATALOG, puzzle_path
from gui.verdict_panel import verdict_context_for
from gui.view_model import build_card_views, compose_card_visual_state
from tests.fixture_paths import PUZZLE_FIXTURES


STANDARD_ID = "standard-deduction-3x3"
ADVANCED_ID = "advanced-deduction-4x4"
PRODUCTION_IDS = (
    STANDARD_ID,
    "intermediate-cipher-3x3",
    ADVANCED_ID,
    "advanced-lantern-4x4",
    "expert-orbit-5x5",
    "expert-parity-5x5",
)


class StaticAgent:
    def __init__(self, classification: Classification) -> None:
        self.classification = classification

    def classify(self, _public_state, _character_id: str) -> Classification:
        return self.classification


def card_for(state: PublicKnowledgeState, character_id: str):
    return next(card for card in build_card_views(state) if card.character_id == character_id)


class ProductionPuzzleHardeningTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.standard = analyze_puzzle(puzzle_path(STANDARD_ID))
        cls.advanced = analyze_puzzle(puzzle_path(ADVANCED_ID))

    def test_catalog_and_experiment_set_are_production_only(self) -> None:
        ids = tuple(entry.puzzle_id for entry in PUZZLE_CATALOG)
        self.assertEqual(ids, PRODUCTION_IDS)
        self.assertNotIn("Tutorial", {entry.difficulty for entry in PUZZLE_CATALOG})
        self.assertNotIn("sample-3x3-fact-chain", ids)
        self.assertEqual(tuple(path.name for path in puzzle_paths()), tuple(
            puzzle_path(puzzle_id).name for puzzle_id in PRODUCTION_IDS
        ))
        screen_copy = (Path(__file__).parents[1] / "gui" / "puzzle_select.py").read_text(encoding="utf-8")
        self.assertNotIn("Tutorial", screen_copy)
        self.assertNotIn("The Gallery Shift", screen_copy)

    def test_legacy_tutorial_is_test_only_and_startup_is_standard(self) -> None:
        tutorial = PUZZLE_FIXTURES / "sample_3x3.json"
        self.assertTrue(tutorial.is_file())
        self.assertEqual(PuzzleLoader.load(tutorial).id, "sample-3x3-fact-chain")
        self.assertEqual(DEFAULT_PUZZLE.resolve(), puzzle_path(STANDARD_ID).resolve())

    def test_production_puzzles_have_no_direct_answer_fact_clues(self) -> None:
        for profile in (self.standard, self.advanced):
            with self.subTest(puzzle=profile["puzzle_id"]):
                self.assertEqual(profile["fact_clues"], 0)
                self.assertEqual(profile["direct_answer_fact_ids"], [])
                self.assertEqual(profile["direct_single_fact_deductions"], 0)

    def test_quality_profiles_record_non_linear_deterministic_reveals(self) -> None:
        for puzzle_id, profile in ((STANDARD_ID, self.standard), (ADVANCED_ID, self.advanced)):
            puzzle = PuzzleLoader.load(puzzle_path(puzzle_id))
            unresolved_row_major = [
                card.character.id for card in puzzle.ordered_cards if not card.initially_revealed
            ]
            self.assertNotEqual(profile["deduction_target_sequence"], unresolved_row_major)
            self.assertEqual(profile["support_size_1_count"], 0)
            self.assertEqual(profile["support_size_gte_2_count"], profile["deduction_steps"])
            repeated = analyze_puzzle(puzzle_path(puzzle_id))
            self.assertEqual(repeated["deduction_target_sequence"], profile["deduction_target_sequence"])
            self.assertEqual(repeated["reveal_owner_sequence"], profile["reveal_owner_sequence"])

    def test_standard_and_advanced_quality_baselines_remain_strong(self) -> None:
        self.assertEqual((self.standard["deduction_steps"], self.standard["average_support_size"]), (7, 2.0))
        self.assertEqual(self.standard["maximum_support_size"], 2)
        self.assertGreater(self.advanced["average_support_size"], 2)
        self.assertGreaterEqual(self.advanced["maximum_support_size"], 4)
        for profile in (self.standard, self.advanced):
            self.assertTrue(profile["consistent"])
            self.assertTrue(profile["unique"])
            self.assertTrue(profile["progressively_solvable"])


class ManualVerdictLockTests(unittest.TestCase):
    def setUp(self) -> None:
        puzzle = PuzzleLoader.load(puzzle_path(STANDARD_ID))
        self.controller = GameController(GameEngine(puzzle, LogicAgent()))

    def _lock_b1(self):
        self.controller.select_character("B1")
        before = self.controller.state()
        result = self.controller.submit_selected(Status.INNOCENT)
        self.assertEqual(result.outcome, VerdictOutcome.CONTRADICTED)
        return before, result

    def test_contradicted_locks_without_mutating_public_state_or_revealing_answer(self) -> None:
        before, result = self._lock_b1()
        after = self.controller.state()
        self.assertEqual(after, before)
        self.assertIsNone(after.status_of("B1"))
        self.assertIsNone(after.clue_for("B1"))
        self.assertTrue(self.controller.is_manual_locked("B1"))
        self.assertEqual(self.controller.manual_locked_ids, frozenset({"B1"}))
        self.assertNotIn("lock", repr(after).casefold())
        self.assertIsNotNone(result.forced_status)  # Engine contract remains intact.

    def test_opposite_manual_retry_is_blocked_before_engine_submission(self) -> None:
        self._lock_b1()
        trace_before = self.controller.trace()
        with self.assertRaises(ManualVerdictLockedError):
            self.controller.submit_selected(Status.CRIMINAL)
        self.assertEqual(self.controller.trace(), trace_before)
        self.assertIsNone(self.controller.state().status_of("B1"))

    def test_not_provable_does_not_lock_and_can_be_retried(self) -> None:
        puzzle = PuzzleLoader.load(puzzle_path(STANDARD_ID))
        controller = GameController(GameEngine(puzzle, StaticAgent(Classification.UNKNOWN)))
        controller.select_character("B1")
        before = controller.state()
        first = controller.submit_selected(Status.INNOCENT)
        second = controller.submit_selected(Status.CRIMINAL)
        self.assertEqual((first.outcome, second.outcome), (
            VerdictOutcome.NOT_PROVABLE,
            VerdictOutcome.NOT_PROVABLE,
        ))
        self.assertEqual(controller.state(), before)
        self.assertFalse(controller.is_manual_locked("B1"))

    def test_accepted_and_inconsistent_do_not_lock(self) -> None:
        self.controller.select_character("B1")
        accepted = self.controller.submit_selected(Status.CRIMINAL)
        self.assertEqual(accepted.outcome, VerdictOutcome.ACCEPTED)
        self.assertFalse(self.controller.is_manual_locked("B1"))
        self.assertEqual(self.controller.state().status_of("B1"), Status.CRIMINAL)

        puzzle = PuzzleLoader.load(puzzle_path(STANDARD_ID))
        inconsistent = GameController(GameEngine(puzzle, StaticAgent(Classification.INCONSISTENT)))
        inconsistent.select_character("B1")
        result = inconsistent.submit_selected(Status.CRIMINAL)
        self.assertEqual(result.outcome, VerdictOutcome.INCONSISTENT)
        self.assertFalse(inconsistent.is_manual_locked("B1"))

    def test_restart_and_load_clear_all_locks(self) -> None:
        self._lock_b1()
        self.controller.restart()
        self.assertEqual(self.controller.manual_locked_ids, frozenset())
        self._lock_b1()
        self.controller.load(PuzzleLoader.load(puzzle_path(ADVANCED_ID)))
        self.assertEqual(self.controller.manual_locked_ids, frozenset())
        self.assertEqual(self.controller.state().puzzle_id, ADVANCED_ID)

    def test_locked_card_context_and_visual_modifier_are_neutral(self) -> None:
        self._lock_b1()
        before_trace = self.controller.trace()
        interaction = self.controller.activate_character("B1")
        self.assertEqual(interaction.character_id, "B1")
        self.assertEqual(self.controller.trace(), before_trace)
        card = card_for(self.controller.state(), "B1")
        context = verdict_context_for(card, manual_locked=True)
        self.assertFalse(context.can_submit)
        self.assertIn("LOCKED", context.identity)
        self.assertIn("Manual verdict locked", context.detail)
        visual = compose_card_visual_state(card, manual_locked=True)
        self.assertTrue(visual.modifiers.manual_locked)
        self.assertIsNotNone(appearance_for(visual).lock_outline)
        self.assertIsNone(card.status)
        self.assertIsNone(card.clue_text)

    def test_hint_stages_do_not_mutate_lock_or_present_a_verdict(self) -> None:
        self._lock_b1()
        state_before = self.controller.state()
        session, stage1, _ = progress_hint_session(
            None,
            self.controller.state,
            self.controller.hint,
            self.controller.trace,
        )
        _session, stage2, _ = progress_hint_session(
            session,
            self.controller.state,
            self.controller.hint,
            self.controller.trace,
        )
        visible = f"{stage1.title} {stage1.message} {stage2.title} {stage2.message}"
        self.assertNotIn("B1 = CRIMINAL", visible)
        self.assertNotIn("B1 = INNOCENT", visible)
        self.assertNotIn("Bria is CRIMINAL", visible)
        self.assertNotIn("Bria is INNOCENT", visible)
        self.assertEqual(self.controller.state(), state_before)
        self.assertTrue(self.controller.is_manual_locked("B1"))

    def test_solve_next_and_auto_solve_ignore_manual_penalty(self) -> None:
        self._lock_b1()
        solved = self.controller.solve_next()
        self.assertEqual(solved.character_id, "B1")
        self.assertEqual(solved.outcome, VerdictOutcome.ACCEPTED)
        self.assertEqual(self.controller.state().status_of("B1"), Status.CRIMINAL)
        self.assertNotIn("locked", repr(self.controller.trace()).casefold())

        restarted = GameController(GameEngine(PuzzleLoader.load(puzzle_path(STANDARD_ID)), LogicAgent()))
        restarted.select_character("B1")
        restarted.submit_selected(Status.INNOCENT)
        self.assertTrue(restarted.is_manual_locked("B1"))
        restarted.auto_solve()
        self.assertTrue(restarted.state().is_complete)


class ManualLockTkTests(unittest.TestCase):
    def setUp(self) -> None:
        try:
            self.root = tk.Tk()
        except tk.TclError as exc:
            self.skipTest(f"Tk is unavailable: {exc}")
        self.root.withdraw()
        self.app = GriductiveApp(self.root)
        self.root.update_idletasks()

    def tearDown(self) -> None:
        if hasattr(self, "root"):
            self.app._cancel_auto()
            self.root.destroy()

    def test_contradicted_disables_buttons_shows_lock_and_puzzle_switch_clears_it(self) -> None:
        self.app._select_character("B1")
        self.app._submit(Status.INNOCENT)
        self.assertTrue(self.app._controller.is_manual_locked("B1"))
        self.assertFalse(self.app._controls.verdict_panel.can_submit)
        self.assertTrue(self.app._board._buttons["B1"].visual_state.modifiers.manual_locked)
        visible = repr(self.app._feedback.feedback)
        self.assertIn("locked", visible.casefold())
        self.assertIn("hidden", visible.casefold())
        self.assertNotIn("CRIMINAL", visible)
        self.assertNotIn("INNOCENT", visible)

        self.app._play_shipped_puzzle(ADVANCED_ID)
        self.assertEqual(self.app._controller.manual_locked_ids, frozenset())
        self.assertEqual(self.app._controller.state().puzzle_id, ADVANCED_ID)

    def test_selecting_locked_card_does_not_reveal_clue_or_enable_verdicts(self) -> None:
        self.app._select_character("B1")
        self.app._submit(Status.INNOCENT)
        before = self.app._controller.state()
        trace = self.app._controller.trace()
        self.app._select_character("B1")
        self.assertEqual(self.app._controller.state(), before)
        self.assertEqual(self.app._controller.trace(), trace)
        self.assertIsNone(before.clue_for("B1"))
        self.assertFalse(self.app._controls.verdict_panel.can_submit)


class ManualLockBoundaryTests(unittest.TestCase):
    def test_lock_is_absent_from_public_dtos_and_protected_logic(self) -> None:
        self.assertNotIn("lock", {field.name for field in fields(PublicKnowledgeState)})
        root = Path(__file__).parents[1]
        protected = "\n".join(
            (root / path).read_text(encoding="utf-8")
            for path in (
                "agent/logic_agent.py",
                "agent/hint_explanation.py",
                "logic/cnf_encoder.py",
                "logic/semantic_evaluator.py",
                "sat/dpll.py",
            )
        )
        self.assertNotIn("manual_locked", protected)
        self.assertNotIn("ManualVerdictLocked", protected)


if __name__ == "__main__":
    unittest.main()
