from __future__ import annotations

import itertools
import unittest
from unittest import mock

from core.clue import Clue
from core.enums import ClueType, RegionType
from core.region import Region
from logic.cnf_encoder import CNFEncoder
from logic.semantic_evaluator import evaluate
from tests.test_logic import cnf_satisfied, make_grid_characters


class ExtensionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.characters = make_grid_characters(3)
        state = mock.Mock()
        state.characters = self.characters
        state.revealed_clues = ()
        state.known_verdicts = ()
        self.encoder = CNFEncoder(state)
        ids = tuple(character.id for character in self.characters)
        self.assignments = tuple(
            dict(zip(ids, values, strict=True))
            for values in itertools.product((False, True), repeat=len(ids))
        )

    def _assert_equivalent(self, clue: Clue) -> None:
        clauses = tuple(self.encoder.encode_clue(clue))
        for assignment in self.assignments:
            self.assertEqual(
                cnf_satisfied(clauses, assignment, self.encoder.mapper),
                evaluate(clue, assignment),
                f"extension mismatch for {clue.id}: {assignment}",
            )

    def test_implies_semantics_and_cnf_are_exhaustively_equivalent(self) -> None:
        self._assert_equivalent(Clue("I", ClueType.IMPLIES, characters=("A1", "B1")))

    def test_odd_semantics_and_cnf_are_exhaustively_equivalent(self) -> None:
        self._assert_equivalent(
            Clue(
                "O",
                ClueType.ODD,
                region=Region(RegionType.EXPLICIT, cells=("A1", "B1", "C1")),
            )
        )

    def test_extension_contracts_reject_malformed_payloads(self) -> None:
        with self.assertRaises(ValueError):
            Clue("I", ClueType.IMPLIES, characters=("A1", "A1"))
        with self.assertRaises(ValueError):
            Clue("O", ClueType.ODD)
        with self.assertRaises(ValueError):
            Clue("O", ClueType.ODD, region=Region(RegionType.ROW, index=1), k=1)


if __name__ == "__main__":
    unittest.main()
