"""Cross-layer validation of the small sample promised by Phase 02."""

from __future__ import annotations

import unittest
from pathlib import Path

from core.enums import Status
from core.public_state import PublicKnowledgeState, RevealedClue
from game.puzzle_loader import PuzzleLoader
from logic.cnf_encoder import CNFEncoder
from logic.semantic_evaluator import evaluate
from sat.dpll import DPLLSolver
from sat.sat_result import SATStatus
from tests.fixture_paths import PUZZLE_FIXTURES


SAMPLE_PATH = PUZZLE_FIXTURES / "sample_3x3.json"


class SamplePuzzleValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.puzzle = PuzzleLoader.load(SAMPLE_PATH)

    def test_every_clue_is_true_under_the_declared_solution(self) -> None:
        complete_assignment = {
            card.character.id: card.hidden_status is Status.CRIMINAL
            for card in self.puzzle.cards
        }
        for card in self.puzzle.cards:
            with self.subTest(clue_id=card.clue.id):
                self.assertTrue(evaluate(card.clue, complete_assignment))

    def test_complete_clue_set_has_exactly_one_primary_model(self) -> None:
        state = PublicKnowledgeState(
            puzzle_id=self.puzzle.id,
            title=self.puzzle.title,
            size=self.puzzle.size,
            characters=tuple(card.character for card in self.puzzle.ordered_cards),
            revealed_clues=tuple(
                RevealedClue(card.character.id, card.clue)
                for card in self.puzzle.ordered_cards
            ),
            known_verdicts=(),
            is_complete=False,
        )
        encoding = CNFEncoder(state).build_kb()
        variable_count = encoding.primary_variable_count + encoding.auxiliary_variable_count
        first = DPLLSolver().solve(encoding.clauses, variable_count)
        self.assertIs(first.status, SATStatus.SAT)

        primary_blocking_clause = tuple(
            -variable if first.assignment[variable] else variable
            for variable in range(1, encoding.primary_variable_count + 1)
        )
        second = DPLLSolver().solve(
            (*encoding.clauses, primary_blocking_clause),
            variable_count,
        )
        self.assertIs(second.status, SATStatus.UNSAT)


if __name__ == "__main__":
    unittest.main()
