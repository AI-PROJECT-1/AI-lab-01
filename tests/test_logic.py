from __future__ import annotations

import itertools
import random
import unittest
from unittest import mock

from core.character import Character
from core.clue import Clue
from core.enums import ClueType, RegionType, Status
from core.region import Region
from logic.cnf_encoder import CNFEncoder, VariableMapper
from logic.semantic_evaluator import evaluate


def make_grid_characters(size: int) -> tuple[Character, ...]:
    return tuple(
        Character(f"{chr(ord('A') + column - 1)}{row}", f"Name {column}{row}", f"Profession {column}{row}", row, column)
        for row in range(1, size + 1)
        for column in range(1, size + 1)
    )


def clause_satisfied(clause: tuple[int, ...], assignment: dict[str, bool], mapper: VariableMapper) -> bool:
    return any((assignment[mapper.character_id_for(abs(literal))] != (literal < 0)) for literal in clause)


def cnf_satisfied(clauses: tuple[tuple[int, ...], ...], assignment: dict[str, bool], mapper: VariableMapper) -> bool:
    return all(clause_satisfied(clause, assignment, mapper) for clause in clauses)


class LogicEncodingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.characters = make_grid_characters(3)
        self.mapper = VariableMapper.from_characters(self.characters)

    def test_variable_mapping_is_deterministic(self) -> None:
        first_mapping = VariableMapper.from_characters(self.characters)
        second_mapping = VariableMapper.from_characters(tuple(sorted(self.characters, key=lambda item: (item.row, item.column, item.id))))
        self.assertEqual(first_mapping.variables, second_mapping.variables)
        self.assertEqual(first_mapping._mapping, second_mapping._mapping)

    def test_cnf_encoding_report_counts(self) -> None:
        public_state = mock.Mock()
        public_state.characters = self.characters
        public_state.revealed_clues = ()
        public_state.known_verdicts = ()
        encoder = CNFEncoder(public_state)
        kb = encoder.build_kb()
        self.assertEqual(kb.primary_variable_count, 9)
        self.assertEqual(kb.auxiliary_variable_count, 0)
        self.assertEqual(kb.clause_count, 0)
        self.assertEqual(kb.report(), {"primary_variables": 9, "auxiliary_variables": 0, "clauses": 0})


class CNFSemanticsIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.characters = make_grid_characters(3)
        self.assignments = self._generate_assignments(50)

    def _generate_assignments(self, count: int) -> list[dict[str, bool]]:
        ids = [character.id for character in self.characters]
        random.seed(0)
        assignments: list[dict[str, bool]] = []
        for _ in range(count):
            assignments.append({identifier: random.choice((False, True)) for identifier in ids})
        assignments.append({identifier: False for identifier in ids})
        assignments.append({identifier: True for identifier in ids})
        return assignments

    def _confirm_clue_equivalence(self, clue: Clue) -> None:
        public_state = unittest.mock.Mock()
        public_state.characters = self.characters
        public_state.revealed_clues = ()
        public_state.known_verdicts = ()
        encoder = CNFEncoder(public_state)
        clauses = tuple(encoder.encode_clue(clue))
        for assignment in self.assignments:
            expected = evaluate(clue, assignment)
            actual = cnf_satisfied(clauses, assignment, encoder.mapper)
            self.assertEqual(
                actual,
                expected,
                msg=(
                    f"CNF equiv failed for clue {clue.id} with assignment {assignment}: "
                    f"expected {expected}, got {actual}"
                ),
            )

    def test_fact_clue(self) -> None:
        clue = Clue("F", ClueType.FACT, target="A1", status=Status.CRIMINAL)
        self._confirm_clue_equivalence(clue)

    def test_same_clue(self) -> None:
        clue = Clue("S", ClueType.SAME, characters=("A1", "B1"))
        self._confirm_clue_equivalence(clue)

    def test_different_clue(self) -> None:
        clue = Clue("D", ClueType.DIFFERENT, characters=("A1", "B1"))
        self._confirm_clue_equivalence(clue)

    def test_exactly_row_clue(self) -> None:
        clue = Clue("E", ClueType.EXACTLY, region=Region(RegionType.ROW, index=1), k=1)
        self._confirm_clue_equivalence(clue)

    def test_exactly_zero_row_clue(self) -> None:
        clue = Clue("EZ", ClueType.EXACTLY, region=Region(RegionType.ROW, index=1), k=0)
        self._confirm_clue_equivalence(clue)

    def test_exactly_all_row_clue(self) -> None:
        clue = Clue("EA", ClueType.EXACTLY, region=Region(RegionType.ROW, index=1), k=3)
        self._confirm_clue_equivalence(clue)

    def test_at_least_zero_clue(self) -> None:
        clue = Clue("L0", ClueType.AT_LEAST, region=Region(RegionType.COLUMN, index=1), k=0)
        self._confirm_clue_equivalence(clue)

    def test_at_most_all_column_clue(self) -> None:
        clue = Clue("MA", ClueType.AT_MOST, region=Region(RegionType.COLUMN, index=1), k=3)
        self._confirm_clue_equivalence(clue)

    def test_at_most_neighbors_clue(self) -> None:
        clue = Clue("M", ClueType.AT_MOST, region=Region(RegionType.NEIGHBORS, center="B2"), k=2)
        self._confirm_clue_equivalence(clue)

    def test_exactly_explicit_clue(self) -> None:
        clue = Clue(
            "X",
            ClueType.EXACTLY,
            region=Region(RegionType.EXPLICIT, cells=("A1", "C3", "B2")),
            k=2,
        )
        self._confirm_clue_equivalence(clue)

    def test_explicit_region_with_duplicate_cells_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "distinct"):
            Region(RegionType.EXPLICIT, cells=("A1", "A1"))

    def test_invalid_explicit_region_raises(self) -> None:
        public_state = mock.Mock()
        public_state.characters = self.characters
        public_state.revealed_clues = ()
        public_state.known_verdicts = ()
        encoder = CNFEncoder(public_state)
        clue = Clue("BAD", ClueType.AT_LEAST, region=Region(RegionType.EXPLICIT, cells=("Z9",)), k=1)
        with self.assertRaises(ValueError):
            encoder.encode_clue(clue)

    def test_invalid_neighbor_region_raises(self) -> None:
        public_state = mock.Mock()
        public_state.characters = self.characters
        public_state.revealed_clues = ()
        public_state.known_verdicts = ()
        encoder = CNFEncoder(public_state)
        clue = Clue("BAD2", ClueType.AT_LEAST, region=Region(RegionType.NEIGHBORS, center="Z9"), k=1)
        with self.assertRaises(ValueError):
            encoder.encode_clue(clue)


if __name__ == "__main__":
    unittest.main()
