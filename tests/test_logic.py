from __future__ import annotations

import itertools
import unittest
from unittest import mock

from core.character import Character
from core.clue import Clue
from core.enums import ClueType, RegionType, Status
from core.public_state import KnownVerdict, RevealedClue
from core.region import Region
from logic.cnf_encoder import CNFEncoder, VariableMapper
from logic.region_resolver import RegionResolver
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

    def test_variable_mapping_rejects_duplicate_character_ids(self) -> None:
        with self.assertRaisesRegex(ValueError, "unique"):
            VariableMapper.from_characters((self.characters[0], self.characters[0]))

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

    def test_kb_contains_revealed_clues_and_known_verdicts_only(self) -> None:
        public_state = mock.Mock()
        public_state.characters = self.characters
        public_state.revealed_clues = (
            RevealedClue(
                "A1",
                Clue("VISIBLE", ClueType.FACT, target="B1", status=Status.CRIMINAL),
            ),
        )
        public_state.known_verdicts = (KnownVerdict("C1", Status.INNOCENT),)
        encoding = CNFEncoder(public_state).build_kb()
        self.assertEqual(encoding.clauses, ((2,), (-3,)))


class RegionResolverTests(unittest.TestCase):
    def setUp(self) -> None:
        self.resolver = RegionResolver(make_grid_characters(3))

    def test_row_column_and_explicit_regions(self) -> None:
        self.assertEqual(
            self.resolver.resolve(Region(RegionType.ROW, index=2)),
            ("A2", "B2", "C2"),
        )
        self.assertEqual(
            self.resolver.resolve(Region(RegionType.COLUMN, index=2)),
            ("B1", "B2", "B3"),
        )
        self.assertEqual(
            self.resolver.resolve(Region(RegionType.EXPLICIT, cells=("C3", "A1"))),
            ("C3", "A1"),
        )

    def test_corner_edge_and_interior_neighbors(self) -> None:
        self.assertEqual(
            self.resolver.resolve(Region(RegionType.NEIGHBORS, center="A1")),
            ("B1", "A2", "B2"),
        )
        self.assertEqual(
            self.resolver.resolve(Region(RegionType.NEIGHBORS, center="B1")),
            ("A1", "C1", "A2", "B2", "C2"),
        )
        self.assertEqual(
            self.resolver.resolve(Region(RegionType.NEIGHBORS, center="B2")),
            ("A1", "B1", "C1", "A2", "C2", "A3", "B3", "C3"),
        )

    def test_out_of_bounds_row_and_column_are_rejected(self) -> None:
        for region in (
            Region(RegionType.ROW, index=4),
            Region(RegionType.COLUMN, index=4),
        ):
            with self.subTest(region=region), self.assertRaisesRegex(ValueError, "outside"):
                self.resolver.resolve(region)


class CNFSemanticsIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.characters = make_grid_characters(3)
        self.assignments = self._generate_assignments()

    def _generate_assignments(self) -> list[dict[str, bool]]:
        ids = [character.id for character in self.characters]
        return [
            dict(zip(ids, values, strict=True))
            for values in itertools.product((False, True), repeat=len(ids))
        ]

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

    def test_at_least_nontrivial_clue(self) -> None:
        clue = Clue("L2", ClueType.AT_LEAST, region=Region(RegionType.ROW, index=2), k=2)
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

    def test_single_cell_region(self) -> None:
        clue = Clue(
            "ONE",
            ClueType.EXACTLY,
            region=Region(RegionType.EXPLICIT, cells=("A1",)),
            k=1,
        )
        self._confirm_clue_equivalence(clue)

    def test_all_counting_clues_reject_k_greater_than_region(self) -> None:
        public_state = mock.Mock()
        public_state.characters = self.characters
        public_state.revealed_clues = ()
        public_state.known_verdicts = ()
        encoder = CNFEncoder(public_state)
        for clue_type in (ClueType.EXACTLY, ClueType.AT_LEAST, ClueType.AT_MOST):
            clue = Clue(
                f"BAD-{clue_type.value}",
                clue_type,
                region=Region(RegionType.ROW, index=1),
                k=4,
            )
            with self.subTest(clue_type=clue_type), self.assertRaisesRegex(ValueError, "region size"):
                encoder.encode_clue(clue)
            with self.subTest(clue_type=clue_type), self.assertRaisesRegex(ValueError, "region size"):
                evaluate(clue, self.assignments[0])

    def test_out_of_bounds_row_and_column_clues_are_rejected(self) -> None:
        public_state = mock.Mock()
        public_state.characters = self.characters
        public_state.revealed_clues = ()
        public_state.known_verdicts = ()
        encoder = CNFEncoder(public_state)
        for region in (
            Region(RegionType.ROW, index=4),
            Region(RegionType.COLUMN, index=4),
        ):
            clue = Clue("BAD-REGION", ClueType.EXACTLY, region=region, k=0)
            with self.subTest(region=region), self.assertRaisesRegex(ValueError, "outside"):
                encoder.encode_clue(clue)

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
