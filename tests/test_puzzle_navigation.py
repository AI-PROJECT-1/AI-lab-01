"""Phase 8.5 contracts for the local puzzle-selection screen."""

from __future__ import annotations

from dataclasses import fields
from pathlib import Path
import tkinter as tk
import unittest
from unittest.mock import patch

from gui.app import GriductiveApp
from game.puzzle_loader import PuzzleLoader
from gui.puzzle_catalog import PUZZLE_CATALOG, PuzzleCatalogEntry, puzzle_path
from gui.screen_manager import ScreenName
from tests.fixture_paths import PUZZLE_FIXTURES


ROOT = Path(__file__).parents[1]
STANDARD_ID = "standard-deduction-3x3"
ADVANCED_ID = "advanced-deduction-4x4"
INITIAL = puzzle_path(STANDARD_ID)


class PuzzleCatalogTests(unittest.TestCase):
    def test_catalog_contains_only_production_standard_and_advanced(self) -> None:
        self.assertEqual({entry.difficulty for entry in PUZZLE_CATALOG}, {"Standard", "Advanced"})
        self.assertNotIn("sample-3x3-fact-chain", {entry.puzzle_id for entry in PUZZLE_CATALOG})
        catalog_paths = {puzzle_path(entry.puzzle_id).resolve() for entry in PUZZLE_CATALOG}
        shipped_paths = {
            path.resolve()
            for path in (ROOT / "puzzles").glob("*.json")
            if path.name != "schema.json"
        }
        self.assertEqual(catalog_paths, shipped_paths)
        for entry in PUZZLE_CATALOG:
            with self.subTest(puzzle=entry.puzzle_id):
                self.assertTrue(puzzle_path(entry.puzzle_id).is_file())
                puzzle = PuzzleLoader.load(puzzle_path(entry.puzzle_id))
                self.assertEqual((entry.puzzle_id, entry.name, entry.size), (puzzle.id, puzzle.title, puzzle.size))

    def test_catalog_metadata_has_no_hidden_answer_or_clue_payload(self) -> None:
        self.assertEqual(
            {field.name for field in fields(PuzzleCatalogEntry)},
            {"puzzle_id", "name", "size", "difficulty", "description"},
        )
        text = repr(PUZZLE_CATALOG).casefold()
        for forbidden in ("hidden", "solution", "status=", "criminal", "innocent"):
            self.assertNotIn(forbidden, text)


class PuzzleNavigationTests(unittest.TestCase):
    def setUp(self) -> None:
        try:
            self.root = tk.Tk()
        except tk.TclError as exc:
            self.skipTest(f"Tk is unavailable: {exc}")
        self.root.withdraw()
        self.app = GriductiveApp(self.root, INITIAL)
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

    def test_puzzle_select_opens_without_mutating_public_state(self) -> None:
        before = self.app._controller.state()
        self.app._show_puzzles()
        self.assertEqual(self.app._screen_manager.current, ScreenName.PUZZLES)
        self.assertEqual(self.app._controller.state(), before)
        self.assertEqual(self.app._puzzle_select.card_count, len(PUZZLE_CATALOG))

    def test_back_returns_to_identical_game_state_and_selection(self) -> None:
        self.app._select_character("B1")
        before = self.app._controller.state()
        self.app._show_puzzles()
        self.app._show_game()
        self.assertEqual(self.app._screen_manager.current, ScreenName.GAME)
        self.assertEqual(self.app._controller.state(), before)
        self.assertEqual(self.app._controller.selected_character_id, "B1")

    def test_repeated_navigation_does_not_duplicate_catalog_cards(self) -> None:
        for _ in range(4):
            self.app._show_puzzles()
            self.assertEqual(self.app._puzzle_select.card_count, len(PUZZLE_CATALOG))
            self.app._show_game()
        self.assertEqual(self.app._screen_manager.current, ScreenName.GAME)

    def test_selecting_shipped_puzzle_loads_exact_id_and_clears_stale_state(self) -> None:
        self.app._select_character("B1")
        self.app._select_clue("A1")
        self.app._hint()
        self.app._newly_revealed_id = "B1"
        self.app._show_puzzles()
        self.app._play_shipped_puzzle(STANDARD_ID)
        state = self.app._controller.state()
        self.assertEqual(state.puzzle_id, STANDARD_ID)
        self.assertEqual(self.app._screen_manager.current, ScreenName.GAME)
        self.assertIsNone(self.app._controller.selected_character_id)
        self.assertIsNone(self.app._controller.selected_clue_owner_id)
        self.assertIsNone(self.app._hint_state.session)
        self.assertIsNone(self.app._newly_revealed_id)
        self.assertEqual(self.app._highlighted_ids, ())
        self.assertFalse(state.is_complete)

    def test_selected_puzzle_cancels_stale_auto_callback_generation(self) -> None:
        self.app._auto_solve()
        stale_generation = self.app._auto_generation
        self.assertTrue(self.app._auto_running)
        self.app._play_shipped_puzzle(ADVANCED_ID)
        selected = self.app._controller.state()
        self.assertFalse(self.app._auto_running)
        self.assertGreater(self.app._auto_generation, stale_generation)
        self.app._auto_step(stale_generation)
        self.assertEqual(self.app._controller.state(), selected)

    def test_selecting_puzzle_clears_completed_presentation(self) -> None:
        self.app._controller.auto_solve()
        self.app._render()
        self.assertTrue(self.app._controller.state().is_complete)
        self.app._show_puzzles()
        self.app._play_shipped_puzzle(STANDARD_ID)
        self.assertFalse(self.app._controller.state().is_complete)
        self.assertFalse(self.app._completion.visible)

    def test_current_puzzle_indication_tracks_public_puzzle_id(self) -> None:
        self.app._show_puzzles()
        self.assertEqual(self.app._puzzle_select.current_puzzle_id, STANDARD_ID)
        visible = " ".join(
            str(widget.cget("text"))
            for card in self.app._puzzle_select._cards.values()
            for widget in self._widget_tree(card)
            if "text" in widget.keys()
        )
        self.assertEqual(visible.count("CURRENTLY PLAYING"), 1)
        self.app._play_shipped_puzzle(ADVANCED_ID)
        self.app._show_puzzles()
        self.assertEqual(self.app._puzzle_select.current_puzzle_id, ADVANCED_ID)

    @staticmethod
    def _widget_tree(widget):
        yield widget
        for child in widget.winfo_children():
            yield from PuzzleNavigationTests._widget_tree(child)

    def test_external_load_and_restart_remain_available_after_navigation(self) -> None:
        external = PUZZLE_FIXTURES / "extension_chain_3x3.json"
        self.app._show_puzzles()
        self.app._show_game()
        with patch("gui.app.filedialog.askopenfilename", return_value=str(external)):
            self.app._load()
        self.assertEqual(self.app._controller.state().puzzle_id, "extension-chain-3x3")
        self.app._controller.solve_next()
        self.app._restart()
        state = self.app._controller.state()
        self.assertEqual(state.puzzle_id, "extension-chain-3x3")
        self.assertFalse(state.is_complete)

    def test_catalog_screen_source_does_not_access_private_puzzle_data(self) -> None:
        source = "\n".join(
            (ROOT / relative).read_text(encoding="utf-8")
            for relative in ("gui/puzzle_catalog.py", "gui/puzzle_select.py", "gui/screen_manager.py")
        )
        for forbidden in ("hidden_status", "hidden_solution", "card_by_id", "._puzzle", "unrevealed"):
            self.assertNotIn(forbidden, source)


if __name__ == "__main__":
    unittest.main()
