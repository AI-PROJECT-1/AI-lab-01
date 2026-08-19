"""Phase 8.7 production expansion, fingerprint, and 5x5 UI gates."""

from __future__ import annotations

from pathlib import Path
import tkinter as tk
import unittest
from unittest.mock import patch

from agent.logic_agent import LogicAgent
from core.enums import ClueType, Status, VerdictOutcome
from experiments.analyze_puzzles import analyze_suite
from game.game_engine import GameEngine
from game.puzzle_loader import PuzzleLoader
from gui.app import GriductiveApp
from gui.board_view import board_density_for
from gui.controller import GameController
from gui.hint_session import progress_hint_session
from gui.puzzle_catalog import PUZZLE_CATALOG, puzzle_path
from gui.screen_manager import ScreenName


NEW_IDS = (
    "intermediate-cipher-3x3",
    "advanced-lantern-4x4",
    "expert-orbit-5x5",
    "expert-parity-5x5",
)
ALL_IDS = tuple(entry.puzzle_id for entry in PUZZLE_CATALOG)


class ProductionExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report = analyze_suite()
        cls.profiles = {
            profile["puzzle_id"]: profile for profile in cls.report["puzzles"]
        }

    def test_exactly_four_new_production_puzzles_create_two_per_size(self) -> None:
        self.assertEqual(len(ALL_IDS), 6)
        self.assertTrue(set(NEW_IDS).issubset(ALL_IDS))
        self.assertEqual(
            {size: sum(entry.size == size for entry in PUZZLE_CATALOG) for size in (3, 4, 5)},
            {3: 2, 4: 2, 5: 2},
        )

    def test_new_puzzles_are_valid_unique_and_guess_free(self) -> None:
        for puzzle_id in NEW_IDS:
            with self.subTest(puzzle=puzzle_id):
                profile = self.profiles[puzzle_id]
                puzzle = PuzzleLoader.load(puzzle_path(puzzle_id))
                self.assertTrue(profile["consistent"])
                self.assertTrue(profile["unique"])
                self.assertTrue(profile["progressively_solvable"])
                self.assertEqual(
                    profile["deduction_steps"],
                    puzzle.size * puzzle.size - len(puzzle.initially_revealed_ids),
                )
                self.assertTrue(all(step["target"] in step["forced_character_ids"] for step in profile["steps"]))

    def test_new_payloads_have_unique_ids_coordinates_clues_and_valid_initial_state(self) -> None:
        for puzzle_id in NEW_IDS:
            with self.subTest(puzzle=puzzle_id):
                puzzle = PuzzleLoader.load(puzzle_path(puzzle_id))
                character_ids = [card.character.id for card in puzzle.cards]
                clue_ids = [card.clue.id for card in puzzle.cards]
                self.assertEqual(len(character_ids), puzzle.size ** 2)
                self.assertEqual(len(character_ids), len(set(character_ids)))
                self.assertEqual(len(clue_ids), len(set(clue_ids)))
                self.assertEqual(set(character_ids), {
                    f"{chr(65 + column)}{row}"
                    for row in range(1, puzzle.size + 1)
                    for column in range(puzzle.size)
                })
                self.assertTrue(set(puzzle.initially_revealed_ids).issubset(character_ids))

    def test_new_puzzles_have_no_fact_shortcuts_and_every_support_is_multi_component(self) -> None:
        for puzzle_id in NEW_IDS:
            with self.subTest(puzzle=puzzle_id):
                profile = self.profiles[puzzle_id]
                self.assertEqual(profile["fact_clues"], 0)
                self.assertEqual(profile["support_size_1_count"], 0)
                self.assertEqual(profile["support_size_gte_2_count"], profile["deduction_steps"])
                self.assertTrue(all(step["support_size"] >= 2 for step in profile["steps"]))

    def test_each_5x5_uses_both_extensions_and_has_large_support(self) -> None:
        for puzzle_id in NEW_IDS[-2:]:
            with self.subTest(puzzle=puzzle_id):
                puzzle = PuzzleLoader.load(puzzle_path(puzzle_id))
                types = {card.clue.type for card in puzzle.cards}
                self.assertTrue({ClueType.IMPLIES, ClueType.ODD}.issubset(types))
                self.assertGreaterEqual(self.profiles[puzzle_id]["maximum_support_size"], 3)

    def test_same_size_puzzles_have_distinct_fingerprints_and_solutions(self) -> None:
        comparisons = self.report["same_size_pairwise_fingerprints"]
        self.assertEqual(len(comparisons), 3)
        for comparison in comparisons:
            with self.subTest(pair=(comparison["left"], comparison["right"])):
                self.assertGreater(comparison["solution_hamming_distance"], 0)
                structural_fields = (
                    "same_initial_reveals",
                    "same_target_sequence",
                    "same_support_sequence",
                    "same_clue_type_histogram",
                    "same_region_type_histogram",
                )
                self.assertFalse(all(comparison[field] for field in structural_fields))
                self.assertFalse(comparison["suspicious_structural_duplicate"])

        expert_pair = next(comparison for comparison in comparisons if comparison["size"] == 5)
        self.assertFalse(expert_pair["same_target_sequence"])
        self.assertFalse(expert_pair["same_support_sequence"])
        self.assertFalse(expert_pair["same_clue_type_histogram"])
        self.assertFalse(expert_pair["same_region_type_histogram"])
        self.assertFalse(expert_pair["same_initial_reveals"])

    def test_expert_b_has_a_branched_forced_frontier(self) -> None:
        profile = self.profiles["expert-parity-5x5"]
        self.assertGreaterEqual(len(profile["steps"][0]["forced_character_ids"]), 5)
        self.assertTrue(any(len(step["forced_character_ids"]) >= 4 for step in profile["steps"]))

    def test_real_hint_stages_are_public_non_mutating_and_verdict_free_for_all_new_puzzles(self) -> None:
        for puzzle_id in NEW_IDS:
            with self.subTest(puzzle=puzzle_id):
                controller = GameController(GameEngine(PuzzleLoader.load(puzzle_path(puzzle_id)), LogicAgent()))
                before = controller.state()
                session, stage1, _ = progress_hint_session(
                    None, controller.state, controller.hint, controller.trace
                )
                _session, stage2, _ = progress_hint_session(
                    session, controller.state, controller.hint, controller.trace
                )
                visible = f"{stage1.title} {stage1.message} {stage2.title} {stage2.message}"
                target = self.profiles[puzzle_id]["steps"][0]["target"]
                target_name = next(character.name for character in before.characters if character.id == target)
                for verdict in ("CRIMINAL", "INNOCENT"):
                    self.assertNotIn(f"{target} = {verdict}", visible)
                    self.assertNotIn(f"{target_name} is {verdict}", visible)
                self.assertEqual(controller.state(), before)

    def test_manual_anti_guess_lock_and_solver_trace_work_for_all_new_puzzles(self) -> None:
        for puzzle_id in NEW_IDS:
            with self.subTest(puzzle=puzzle_id):
                profile = self.profiles[puzzle_id]
                first = profile["steps"][0]
                forced = Status(first["verdict"])
                controller = GameController(GameEngine(PuzzleLoader.load(puzzle_path(puzzle_id)), LogicAgent()))
                controller.select_character(first["target"])
                before = controller.state()
                result = controller.submit_selected(forced.opposite)
                self.assertEqual(result.outcome, VerdictOutcome.CONTRADICTED)
                self.assertEqual(controller.state(), before)
                self.assertTrue(controller.is_manual_locked(first["target"]))
                controller.auto_solve()
                self.assertTrue(controller.state().is_complete)
                self.assertGreater(len(controller.trace()), 0)

    def test_support_profiles_reference_only_information_public_at_that_step(self) -> None:
        for puzzle_id in NEW_IDS:
            profile = self.profiles[puzzle_id]
            puzzle = PuzzleLoader.load(puzzle_path(puzzle_id))
            public_owners = list(puzzle.initially_revealed_ids)
            known_verdicts = list(puzzle.initially_revealed_ids)
            clue_id_by_owner = {card.character.id: card.clue.id for card in puzzle.cards}
            for step in profile["steps"]:
                with self.subTest(puzzle=puzzle_id, step=step["step"]):
                    active_clues = {clue_id_by_owner[owner] for owner in public_owners}
                    self.assertTrue(set(step["supporting_clue_ids"]).issubset(active_clues))
                    self.assertTrue(set(step["supporting_known_verdict_ids"]).issubset(known_verdicts))
                    self.assertNotIn("hidden", repr(step).casefold())
                public_owners.append(step["target"])
                known_verdicts.append(step["target"])

    def test_solution_and_progression_fingerprints_are_complete(self) -> None:
        for profile in self.report["puzzles"]:
            self.assertEqual(len(profile["solution_fingerprint"]), profile["size"] ** 2)
            self.assertEqual(
                len(profile["reveal_owner_sequence"]),
                profile["size"] ** 2,
            )
            self.assertEqual(
                len(profile["steps"]),
                len(profile["deduction_target_sequence"]),
            )


class FiveByFiveTkTests(unittest.TestCase):
    def setUp(self) -> None:
        try:
            self.root = tk.Tk()
        except tk.TclError as exc:
            self.skipTest(f"Tk is unavailable: {exc}")
        self.root.withdraw()
        self.app = GriductiveApp(self.root, puzzle_path("expert-orbit-5x5"))
        self.root.geometry("1180x660")
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

    def test_density_tiers_are_explicit_and_5x5_renders_all_cards(self) -> None:
        self.assertEqual([board_density_for(size) for size in (3, 4, 5)], ["standard", "compact", "dense"])
        self.assertEqual(self.app._board._density, "dense")
        self.assertEqual(len(self.app._board._buttons), 25)
        self.assertTrue(all(card._dense for card in self.app._board._buttons.values()))
        self.assertIsNone(self.app._board._buttons["A1"]._clue)
        self.assertIsNotNone(self.app._controller.state().clue_for("A1"))
        self.assertIn("A1", self.app._clues._cards)
        self.assertEqual(str(self.app._controls._puzzles_button.cget("style")), "DenseGame.TButton")
        self.assertEqual(str(self.app._controls._auto_button.cget("style")), "DenseSolver.TButton")

    def test_5x5_controls_clues_trace_and_completion_remain_available(self) -> None:
        before = self.app._controller.state()
        self.app._hint()
        self.assertEqual(self.app._controller.state(), before)
        self.app._solve_next()
        self.assertEqual(len(self.app._controller.state().known_verdicts), len(before.known_verdicts) + 1)
        self.assertGreater(len(self.app._controller.trace()), 0)
        self.app._controller.auto_solve()
        self.app._render()
        self.assertTrue(self.app._controller.state().is_complete)
        self.assertTrue(self.app._completion.visible)

    def test_5x5_navigation_and_restart_clear_transient_state(self) -> None:
        self.app._select_character("B1")
        self.app._submit(Status.CRIMINAL)
        self.assertTrue(self.app._controller.manual_locked_ids)
        self.app._select_clue("A1")
        self.app._hint()
        before = self.app._controller.state()
        self.app._show_puzzles()
        self.assertEqual(self.app._screen_manager.current, ScreenName.PUZZLES)
        self.assertEqual(self.app._controller.state(), before)
        self.assertEqual(self.app._puzzle_select.card_count, 6)
        self.app._play_shipped_puzzle("intermediate-cipher-3x3")
        self.assertEqual(self.app._controller.state().puzzle_id, "intermediate-cipher-3x3")
        self.assertEqual(self.app._controller.manual_locked_ids, frozenset())
        self.assertIsNone(self.app._controller.selected_clue_owner_id)
        self.assertEqual(self.app._solver_details_model.presentations(self.app._controller.trace()), ())
        self.app._solve_next()
        self.app._show_puzzles()
        self.app._play_shipped_puzzle("expert-parity-5x5")
        self.assertEqual(self.app._controller.state().puzzle_id, "expert-parity-5x5")
        self.assertIsNone(self.app._controller.selected_character_id)
        self.assertIsNone(self.app._hint_state.session)
        self.assertEqual(self.app._highlighted_ids, ())
        self.assertEqual(self.app._controller.manual_locked_ids, frozenset())
        self.app._select_character("C1")
        self.app._restart()
        self.assertIsNone(self.app._controller.selected_character_id)
        self.assertFalse(self.app._controller.state().is_complete)

    def test_catalog_is_scrollable_at_short_target_height(self) -> None:
        self.app._show_puzzles()
        self.root.update_idletasks()
        bbox = self.app._puzzle_select._canvas.bbox("all")
        self.assertIsNotNone(bbox)
        self.assertGreater(bbox[3] - bbox[1], self.app._puzzle_select._canvas.winfo_height())

    def test_5x5_load_cancels_auto_and_stale_callback_cannot_mutate_new_puzzle(self) -> None:
        self.app._auto_solve()
        stale_generation = self.app._auto_generation
        self.assertTrue(self.app._auto_running)
        with patch(
            "gui.app.filedialog.askopenfilename",
            return_value=str(puzzle_path("expert-parity-5x5")),
        ):
            self.app._load()
        loaded = self.app._controller.state()
        self.assertEqual(loaded.puzzle_id, "expert-parity-5x5")
        self.assertFalse(self.app._auto_running)
        self.assertGreater(self.app._auto_generation, stale_generation)
        self.assertIsNone(self.app._controller.selected_character_id)
        self.assertIsNone(self.app._hint_state.session)
        self.app._auto_step(stale_generation)
        self.assertEqual(self.app._controller.state(), loaded)


if __name__ == "__main__":
    unittest.main()
