"""Validation gates for every distributable 3x3 and 4x4 puzzle."""

from __future__ import annotations

import unittest
from pathlib import Path

from agent.logic_agent import LogicAgent
from core.enums import Status
from core.public_state import PublicKnowledgeState, RevealedClue
from game.game_engine import GameEngine
from game.puzzle_loader import PuzzleLoader
from logic.semantic_evaluator import evaluate


PUZZLE_DIR = Path(__file__).parents[1] / "puzzles"
PUZZLE_PATHS = tuple(sorted(PUZZLE_DIR.glob("*.json")))
PUZZLE_PATHS = tuple(path for path in PUZZLE_PATHS if path.name != "schema.json")


class PuzzleSuiteTests(unittest.TestCase):
    def test_production_suite_has_standard_3x3_and_advanced_4x4(self) -> None:
        puzzles = tuple(PuzzleLoader.load(path) for path in PUZZLE_PATHS)
        self.assertEqual(
            {puzzle.id for puzzle in puzzles},
            {"standard-deduction-3x3", "advanced-deduction-4x4"},
        )
        self.assertEqual({puzzle.size for puzzle in puzzles}, {3, 4})

    def test_every_puzzle_is_true_unique_and_progressively_solvable(self) -> None:
        for path in PUZZLE_PATHS:
            with self.subTest(puzzle=path.name):
                puzzle = PuzzleLoader.load(path)
                assignment = {
                    card.character.id: card.hidden_status is Status.CRIMINAL
                    for card in puzzle.cards
                }
                self.assertTrue(all(evaluate(card.clue, assignment) for card in puzzle.cards))

                complete_state = PublicKnowledgeState(
                    puzzle.id,
                    puzzle.title,
                    puzzle.size,
                    tuple(card.character for card in puzzle.ordered_cards),
                    tuple(RevealedClue(card.character.id, card.clue) for card in puzzle.ordered_cards),
                    (),
                    False,
                )
                uniqueness = LogicAgent().check_uniqueness(complete_state)
                self.assertTrue(uniqueness.is_consistent)
                self.assertTrue(uniqueness.is_unique)

                engine = GameEngine(puzzle, LogicAgent())
                deductions = engine.auto_solve()
                self.assertEqual(len(deductions), puzzle.size * puzzle.size - len(puzzle.initially_revealed_ids))
                self.assertTrue(engine.public_state().is_complete)


if __name__ == "__main__":
    unittest.main()
