"""Final release-audit contracts for experiments and terminal behavior."""

from __future__ import annotations

import unittest
from pathlib import Path

from agent.logic_agent import LogicAgent
from agent.uniqueness import check_complete_clue_set_uniqueness
from core.clue import Clue
from core.enums import ClueType
from core.public_state import PublicKnowledgeState, RevealedClue
from experiments.run_experiments import main, puzzle_paths, run_suite
from game.game_engine import GameEngine
from game.puzzle_loader import PuzzleLoader
from tests.test_logic import make_grid_characters


ROOT = Path(__file__).parents[1]


class ExperimentRunnerTests(unittest.TestCase):
    def test_suite_records_every_distributable_3x3_and_4x4_with_required_metrics(self) -> None:
        report = run_suite(hint_runs=2)
        self.assertEqual(report["puzzle_set"], [path.name for path in puzzle_paths()])
        self.assertEqual({result["size"] for result in report["results"]}, {3, 4})
        for result in report["results"]:
            with self.subTest(puzzle=result["puzzle_file"]):
                self.assertEqual(result["status"], "PASS")
                self.assertIsNone(result["error"])
                self.assertTrue(result["progressive_solve"]["completed"])
                self.assertTrue(result["uniqueness"]["unique"])
                for key in (
                    "sat_calls",
                    "decisions",
                    "propagations",
                    "backtracks",
                    "reveal_waves",
                    "trace_steps",
                    "sat_query_runtime_seconds",
                    "whole_puzzle_wall_runtime_seconds",
                ):
                    self.assertGreaterEqual(result["progressive_solve"][key], 0)
                self.assertEqual(result["initial_kb"]["primary_variables"], result["size"] ** 2)
                self.assertEqual(result["complete_clue_set_cnf"]["primary_variables"], result["size"] ** 2)
                self.assertTrue(result["hint_support"]["available_every_run"])

    def test_cli_writes_machine_readable_result(self) -> None:
        target = ROOT / "experiments" / "results" / ".test_cli.json"
        try:
            self.assertEqual(main(["--output", str(target), "--hint-runs", "1"]), 0)
            text = target.read_text(encoding="utf-8")
            self.assertIn('"schema_version": 1', text)
            self.assertIn('"status": "PASS"', text)
        finally:
            target.unlink(missing_ok=True)


class FinalLogicAuditTests(unittest.TestCase):
    def test_complete_public_state_has_no_repeated_unresolved_target(self) -> None:
        engine = GameEngine(PuzzleLoader.load(ROOT / "puzzles" / "sample_3x3.json"), LogicAgent())
        engine.auto_solve()
        state = engine.public_state()
        agent = LogicAgent()
        self.assertTrue(state.is_complete)
        self.assertEqual(agent.classify_all(state), {})
        self.assertIsNone(agent.solve_next(state))
        self.assertEqual(agent.last_trace, ())

    def test_non_unique_complete_clue_set_is_detected(self) -> None:
        characters = make_grid_characters(2)
        clues = tuple(
            RevealedClue(
                character.id,
                Clue(f"S-{index}", ClueType.SAME, characters=("A1", "B1")),
            )
            for index, character in enumerate(characters, start=1)
        )
        state = PublicKnowledgeState("non-unique", "Non Unique", 2, characters, clues, (), False)
        result = check_complete_clue_set_uniqueness(state)
        self.assertTrue(result.is_consistent)
        self.assertFalse(result.is_unique)
        self.assertEqual(result.sat_calls, 2)

    def test_both_extensions_are_used_by_distributable_puzzles(self) -> None:
        used = {
            card.clue.type
            for path in puzzle_paths()
            for card in PuzzleLoader.load(path).cards
        }
        self.assertTrue({ClueType.IMPLIES, ClueType.ODD}.issubset(used))


if __name__ == "__main__":
    unittest.main()
