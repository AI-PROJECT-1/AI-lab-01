"""UI Phase 7 contracts for card inspection, completion, and lifecycle safety."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import time
import tkinter as tk
import unittest
from unittest.mock import patch

from agent.logic_agent import LogicAgent
from core.enums import Status
from game.game_engine import GameEngine
from game.puzzle_loader import PuzzleLoader
from gui.app import GriductiveApp
from gui.completion_panel import completion_presentation_for
from gui.controller import CharacterInteractionKind, GameController
from gui.hint_session import HintStage


ROOT = Path(__file__).parents[1]
PUZZLES = ROOT / "puzzles"
SAMPLE_PATH = PUZZLES / "sample_3x3.json"
FOUR_BY_FOUR_PATH = PUZZLES / "fact_chain_4x4.json"


class SolverForbiddenEngine:
    """Expose one public snapshot and fail if a presentation click invokes gameplay."""

    def __init__(self, state) -> None:
        self._state = state
        self.solver_calls = 0
        self.hint_calls = 0
        self.submission_calls = 0

    def public_state(self):
        return self._state

    def solve_next(self):
        self.solver_calls += 1
        raise AssertionError("card inspection must not invoke the solver")

    def get_hint(self):
        self.hint_calls += 1
        raise AssertionError("card inspection must not invoke Hint")

    def submit_verdict(self, *_args):
        self.submission_calls += 1
        raise AssertionError("card inspection must not submit a verdict")


class SolvedCharacterInspectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.state = GameEngine(PuzzleLoader.load(SAMPLE_PATH), LogicAgent()).public_state()
        self.engine = SolverForbiddenEngine(self.state)
        self.controller = GameController(self.engine)

    def test_unresolved_click_is_normal_selection_without_hidden_clue(self) -> None:
        before = self.controller.state()
        interaction = self.controller.activate_character("B1")

        self.assertEqual(interaction.kind, CharacterInteractionKind.SELECT_FOR_VERDICT)
        self.assertEqual(self.controller.selected_character_id, "B1")
        self.assertIsNone(self.controller.selected_clue_owner_id)
        self.assertIsNone(interaction.clue_id)
        self.assertEqual(interaction.referenced_character_ids, ())
        self.assertNotIn("CL-02", repr(interaction))
        self.assertEqual(self.controller.state(), before)

    def test_revealed_click_selects_exact_public_owner_clue_and_canonical_cells(self) -> None:
        before = self.controller.state()
        interaction = self.controller.activate_character("A1")

        self.assertEqual(interaction.kind, CharacterInteractionKind.INSPECT_PUBLIC_CLUE)
        self.assertEqual(interaction.clue_id, self.state.clue_for("A1").id)
        self.assertEqual(interaction.clue_id, "CL-01")
        self.assertEqual(interaction.referenced_character_ids, ("B1",))
        self.assertEqual(self.controller.selected_clue_owner_id, "A1")
        self.assertIsNone(self.controller.selected_character_id)
        self.assertEqual(self.controller.state(), before)

    def test_inspection_calls_no_solver_hint_or_submission(self) -> None:
        self.controller.activate_character("A1")
        self.assertEqual(
            (self.engine.solver_calls, self.engine.hint_calls, self.engine.submission_calls),
            (0, 0, 0),
        )

    def test_switching_from_clue_inspection_to_unresolved_selection_clears_clue_context(self) -> None:
        self.controller.activate_character("A1")
        self.controller.activate_character("B1")
        self.assertIsNone(self.controller.selected_clue_owner_id)
        self.assertEqual(self.controller.selected_character_id, "B1")

    def test_restart_and_load_clear_card_driven_inspection(self) -> None:
        real = GameController(GameEngine(PuzzleLoader.load(SAMPLE_PATH), LogicAgent()))
        real.activate_character("A1")
        real.restart()
        self.assertIsNone(real.selected_clue_owner_id)

        real.activate_character("A1")
        real.load(PuzzleLoader.load(FOUR_BY_FOUR_PATH))
        self.assertIsNone(real.selected_clue_owner_id)


class CompletionPresentationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.initial = GameEngine(PuzzleLoader.load(SAMPLE_PATH), LogicAgent()).public_state()

    def test_incomplete_state_has_no_completion_presentation(self) -> None:
        presentation = completion_presentation_for(self.initial)
        self.assertFalse(presentation.visible)
        self.assertEqual((presentation.title, presentation.message), ("", ""))

    def test_completion_uses_public_flag_and_deduction_accurate_copy(self) -> None:
        presentation = completion_presentation_for(replace(self.initial, is_complete=True))
        self.assertTrue(presentation.visible)
        self.assertEqual(presentation.title, "Puzzle solved")
        self.assertIn("logically resolved", presentation.message)
        self.assertNotIn("guess", presentation.message.casefold())

    def test_completion_modules_do_not_reference_hidden_solution_or_private_engine_state(self) -> None:
        sources = "\n".join(
            (ROOT / relative).read_text(encoding="utf-8")
            for relative in ("gui/completion_panel.py", "gui/controller.py")
        )
        for forbidden in ("hidden_solution", "hidden_status", "._puzzle", "card_by_id"):
            self.assertNotIn(forbidden, sources)


class TkGameplayCompletionTests(unittest.TestCase):
    def setUp(self) -> None:
        try:
            self.root = tk.Tk()
        except tk.TclError as exc:
            self.skipTest(f"Tk is unavailable: {exc}")
        self.root.withdraw()
        self.app = GriductiveApp(self.root, SAMPLE_PATH)
        self.root.update_idletasks()

    def tearDown(self) -> None:
        if not hasattr(self, "root"):
            return
        try:
            self.app._cancel_auto()
            if self.app._solver_details_window is not None:
                self.app._solver_details_window.close()
            self.root.destroy()
        except tk.TclError:
            pass

    def _complete_with_solve_next(self) -> None:
        limit = len(self.app._controller.state().characters) + 1
        for _ in range(limit):
            if self.app._controller.state().is_complete:
                return
            self.app._solve_next()
        self.fail("Solve Next did not complete the test puzzle")

    def _prepare_last_unresolved(self) -> tuple[str, Status]:
        while True:
            state = self.app._controller.state()
            unresolved = tuple(
                item.id for item in state.characters if state.status_of(item.id) is None
            )
            if len(unresolved) == 1:
                target = unresolved[0]
                status = LogicAgent().classify(state, target).as_status()
                self.assertIsNotNone(status)
                self.app._render()
                return target, status
            result = self.app._controller.solve_next()
            self.assertIsNotNone(result)

    def test_app_unresolved_and_revealed_card_flows_are_distinct(self) -> None:
        before = self.app._controller.state()
        self.app._select_character("B1")
        self.assertEqual(self.app._controller.selected_character_id, "B1")
        self.assertIsNone(self.app._controller.selected_clue_owner_id)
        self.assertEqual(self.app._controller.state(), before)

        self.app._select_character("A1")
        self.assertIsNone(self.app._controller.selected_character_id)
        self.assertEqual(self.app._controller.selected_clue_owner_id, "A1")
        self.assertEqual(self.app._highlighted_ids, ("B1",))
        self.assertEqual(self.app._feedback.feedback.title, "Public clue selected")

    def test_final_manual_accepted_verdict_triggers_completion(self) -> None:
        target, status = self._prepare_last_unresolved()
        self.app._select_character(target)
        self.app._submit(status)

        self.assertTrue(self.app._controller.state().is_complete)
        self.assertTrue(self.app._completion.visible)
        self.assertEqual(self.app._feedback.feedback.title, "Verdict accepted")

    def test_final_solve_next_step_triggers_completion(self) -> None:
        self._prepare_last_unresolved()
        self.app._solve_next()
        self.assertTrue(self.app._controller.state().is_complete)
        self.assertTrue(self.app._completion.visible)

    def test_auto_solve_stops_on_final_reveal_without_extra_step(self) -> None:
        self.app._auto_solve()
        deadline = time.monotonic() + 5
        while self.app._auto_running and time.monotonic() < deadline:
            self.root.update()
            time.sleep(0.01)

        self.assertTrue(self.app._controller.state().is_complete)
        self.assertTrue(self.app._completion.visible)
        self.assertFalse(self.app._auto_running)
        self.assertIsNone(self.app._auto_after_id)
        self.assertEqual(self.app._feedback.feedback.title, "Auto Solve")
        self.assertIn("Puzzle solved", self.app._feedback.feedback.message)

    def test_completion_disables_gameplay_actions_but_keeps_details_and_board(self) -> None:
        self._complete_with_solve_next()
        self.assertFalse(self.app._controls.verdict_panel.can_submit)
        self.assertFalse(self.app._controls.hint_available)
        self.assertFalse(self.app._controls.solve_next_available)
        self.assertFalse(self.app._controls.auto_solve_available)
        self.assertEqual(len(self.app._board._buttons), 9)
        self.assertTrue(self.app._board.grid_info())

        before = self.app._controller.state()
        self.app._toggle_solver_details()
        self.assertTrue(self.app._solver_details_model.is_open)
        self.assertEqual(self.app._controller.state(), before)

    def test_hint_session_and_modifiers_clear_when_completion_is_rendered(self) -> None:
        self.app._hint()
        self.assertEqual(self.app._hint_state.session.stage, HintStage.ACTIVE_CLUES)
        self.app._controller.auto_solve()
        self.app._render()
        self.assertIsNone(self.app._hint_state.session)
        self.assertEqual(self.app._hint_state.active_clue_ids, ())
        self.assertIsNone(self.app._hint_state.target_character_id)
        self.assertEqual(self.app._hint_state.supporting_verdict_ids, ())
        self.assertEqual(self.app._controls.hint_button_text, "Hint")

    def test_clue_inspection_remains_available_after_completion(self) -> None:
        self._complete_with_solve_next()
        before = self.app._controller.state()
        self.app._select_character("A1")
        self.assertEqual(self.app._controller.selected_clue_owner_id, "A1")
        self.assertEqual(self.app._highlighted_ids, ("B1",))
        self.assertEqual(self.app._controller.state(), before)

    def test_restart_exits_completion_and_clears_every_transient(self) -> None:
        self._complete_with_solve_next()
        self.app._select_character("A1")
        self.app._newly_revealed_id = "C3"
        self.app._restart()

        self.assertFalse(self.app._completion.visible)
        self.assertFalse(self.app._controller.state().is_complete)
        self.assertIsNone(self.app._controller.selected_character_id)
        self.assertIsNone(self.app._controller.selected_clue_owner_id)
        self.assertEqual(self.app._highlighted_ids, ())
        self.assertIsNone(self.app._newly_revealed_id)
        self.assertTrue(self.app._controls.hint_available)

    def test_load_exits_completion_and_clears_every_transient(self) -> None:
        self._complete_with_solve_next()
        self.app._select_character("A1")
        self.app._newly_revealed_id = "C3"

        with patch("gui.app.filedialog.askopenfilename", return_value=str(FOUR_BY_FOUR_PATH)):
            self.app._load()

        self.assertEqual(self.app._controller.state().size, 4)
        self.assertFalse(self.app._completion.visible)
        self.assertIsNone(self.app._controller.selected_character_id)
        self.assertIsNone(self.app._controller.selected_clue_owner_id)
        self.assertEqual(self.app._highlighted_ids, ())
        self.assertIsNone(self.app._newly_revealed_id)
        self.assertIsNone(self.app._hint_state.session)
        self.assertEqual(self.app._solver_details_model._sources, {})

    def test_stale_auto_callback_cannot_mutate_restarted_or_loaded_puzzle(self) -> None:
        self.app._auto_solve()
        stale_generation = self.app._auto_generation
        self.app._restart()
        restarted = self.app._controller.state()
        self.app._auto_step(stale_generation)
        self.assertEqual(self.app._controller.state(), restarted)

        self.app._auto_solve()
        stale_generation = self.app._auto_generation
        with patch("gui.app.filedialog.askopenfilename", return_value=str(FOUR_BY_FOUR_PATH)):
            self.app._load()
        loaded = self.app._controller.state()
        self.app._auto_step(stale_generation)
        self.assertEqual(self.app._controller.state(), loaded)

    def test_protected_completion_handlers_do_not_reason_again_after_completion(self) -> None:
        self._complete_with_solve_next()
        trace = self.app._controller.trace()
        state = self.app._controller.state()
        self.app._hint()
        self.app._solve_next()
        self.app._auto_solve()
        self.app._submit(Status.CRIMINAL)
        self.assertEqual(self.app._controller.state(), state)
        self.assertEqual(self.app._controller.trace(), trace)


if __name__ == "__main__":
    unittest.main()
