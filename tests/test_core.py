"""Level 1 tests for shared domain contracts."""

from __future__ import annotations

import unittest
from dataclasses import FrozenInstanceError, fields

from core.character import Character, cell_id_for, column_label
from core.clue import Clue
from core.enums import ClueType, RegionType, Status
from core.public_state import KnownVerdict, PublicKnowledgeState, RevealedClue
from core.puzzle import Puzzle, PuzzleCard
from core.region import Region


def make_card(cell: str, row: int, column: int, *, initial: bool = False) -> PuzzleCard:
    character = Character(cell, f"Name {cell}", f"Job {cell}", row, column)
    clue = Clue(f"CL-{cell}", ClueType.FACT, target=cell, status=Status.CRIMINAL)
    return PuzzleCard(character, Status.CRIMINAL, clue, initial)


class CoordinateTests(unittest.TestCase):
    def test_column_labels_are_deterministic(self) -> None:
        self.assertEqual((column_label(1), column_label(26), column_label(27)), ("A", "Z", "AA"))
        self.assertEqual(cell_id_for(4, 3), "C4")

    def test_character_rejects_mismatched_coordinate(self) -> None:
        with self.assertRaisesRegex(ValueError, "match"):
            Character("B1", "Ada", "Analyst", 1, 1)


class RegionTests(unittest.TestCase):
    def test_all_required_region_contracts(self) -> None:
        self.assertEqual(Region(RegionType.ROW, index=2).describe(), "row 2")
        self.assertEqual(Region(RegionType.COLUMN, index=1).describe(), "column 1")
        self.assertEqual(Region(RegionType.NEIGHBORS, center="B2").describe(), "neighbors of B2")
        self.assertEqual(Region(RegionType.EXPLICIT, cells=("A1", "C3")).cells, ("A1", "C3"))

    def test_explicit_region_rejects_duplicates(self) -> None:
        with self.assertRaisesRegex(ValueError, "distinct"):
            Region(RegionType.EXPLICIT, cells=("A1", "A1"))


class ClueTests(unittest.TestCase):
    def test_all_six_core_clue_contracts(self) -> None:
        clues = (
            Clue("F", ClueType.FACT, target="A1", status=Status.CRIMINAL),
            Clue("S", ClueType.SAME, characters=("A1", "B1")),
            Clue("D", ClueType.DIFFERENT, characters=("A1", "B1")),
            Clue("E", ClueType.EXACTLY, region=Region(RegionType.ROW, index=1), k=1),
            Clue("L", ClueType.AT_LEAST, region=Region(RegionType.COLUMN, index=1), k=0),
            Clue("M", ClueType.AT_MOST, region=Region(RegionType.NEIGHBORS, center="A1"), k=2),
        )
        self.assertEqual({clue.type for clue in clues}, set(ClueType))

    def test_invalid_count_and_binary_parameters(self) -> None:
        with self.assertRaisesRegex(ValueError, "non-negative"):
            Clue("bad", ClueType.EXACTLY, region=Region(RegionType.ROW, index=1), k=-1)
        with self.assertRaisesRegex(ValueError, "distinct"):
            Clue("bad", ClueType.SAME, characters=("A1", "A1"))
        with self.assertRaisesRegex(ValueError, "only define"):
            Clue(
                "bad",
                ClueType.FACT,
                target="A1",
                status=Status.CRIMINAL,
                characters=("A1", "B1"),
            )


class PuzzleTests(unittest.TestCase):
    def make_puzzle(self) -> Puzzle:
        cards = (
            make_card("A1", 1, 1, initial=True),
            make_card("B1", 1, 2),
            make_card("A2", 2, 1),
            make_card("B2", 2, 2),
        )
        return Puzzle("p", "Puzzle", 2, cards)

    def test_puzzle_orders_cards_row_major(self) -> None:
        puzzle = self.make_puzzle()
        self.assertEqual(tuple(card.character.id for card in puzzle.ordered_cards), ("A1", "B1", "A2", "B2"))
        self.assertEqual(puzzle.initially_revealed_ids, ("A1",))

    def test_puzzle_rejects_out_of_bounds_region_and_k(self) -> None:
        bad_clue = Clue("bad", ClueType.EXACTLY, region=Region(RegionType.ROW, index=3), k=0)
        cards = list(self.make_puzzle().cards)
        cards[0] = PuzzleCard(cards[0].character, Status.CRIMINAL, bad_clue, True)
        with self.assertRaisesRegex(ValueError, "outside"):
            Puzzle("bad", "Bad", 2, tuple(cards))

        too_large = Clue("bad", ClueType.AT_MOST, region=Region(RegionType.ROW, index=1), k=3)
        cards[0] = PuzzleCard(cards[0].character, Status.CRIMINAL, too_large, True)
        with self.assertRaisesRegex(ValueError, "greater"):
            Puzzle("bad", "Bad", 2, tuple(cards))


class PublicStateTests(unittest.TestCase):
    def test_public_state_is_immutable_and_has_no_hidden_fields(self) -> None:
        character = Character("A1", "Ada", "Analyst", 1, 1)
        clue = Clue("CL-1", ClueType.FACT, target="A1", status=Status.CRIMINAL)
        state = PublicKnowledgeState(
            "p", "Puzzle", 1, (character,), (RevealedClue("A1", clue),),
            (KnownVerdict("A1", Status.CRIMINAL),), True,
        )
        field_names = {field.name for field in fields(PublicKnowledgeState)}
        self.assertFalse({"solution", "hidden_statuses", "unrevealed_clues"} & field_names)
        with self.assertRaises(FrozenInstanceError):
            state.title = "Changed"  # type: ignore[misc]
        self.assertEqual(state.status_of("A1"), Status.CRIMINAL)
        self.assertEqual(state.clue_for("A1"), clue)


if __name__ == "__main__":
    unittest.main()
