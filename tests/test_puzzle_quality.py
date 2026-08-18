"""Phase 8.5 quality gates for Tutorial, Standard, and Advanced puzzles."""

from __future__ import annotations

import unittest

from core.enums import ClueType, RegionType
from experiments.analyze_puzzles import analyze_puzzle
from game.puzzle_loader import PuzzleLoader
from gui.puzzle_catalog import puzzle_path


TUTORIAL_ID = "sample-3x3-fact-chain"
STANDARD_ID = "standard-deduction-3x3"
ADVANCED_ID = "advanced-deduction-4x4"


class PuzzleQualityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tutorial = analyze_puzzle(puzzle_path(TUTORIAL_ID))
        cls.standard = analyze_puzzle(puzzle_path(STANDARD_ID))
        cls.advanced = analyze_puzzle(puzzle_path(ADVANCED_ID))

    def test_tutorial_intentionally_preserves_direct_fact_chain(self) -> None:
        self.assertEqual(self.tutorial["size"], 3)
        self.assertEqual(self.tutorial["fact_clues"], 9)
        self.assertEqual(self.tutorial["direct_single_fact_deductions"], 8)

    def test_standard_is_unique_progressive_and_not_a_direct_fact_chain(self) -> None:
        self.assertEqual(self.standard["size"], 3)
        self.assertTrue(self.standard["consistent"])
        self.assertTrue(self.standard["unique"])
        self.assertTrue(self.standard["progressively_solvable"])
        self.assertEqual(self.standard["deduction_steps"], 7)
        self.assertEqual(self.standard["direct_single_fact_deductions"], 0)
        self.assertGreaterEqual(self.standard["average_support_size"], 2)
        self.assertGreaterEqual(self.standard["maximum_support_size"], 2)

    def test_standard_uses_relations_counting_and_real_regions(self) -> None:
        puzzle = PuzzleLoader.load(puzzle_path(STANDARD_ID))
        types = {card.clue.type for card in puzzle.cards}
        regions = {
            card.clue.region.kind
            for card in puzzle.cards
            if card.clue.region is not None
        }
        self.assertTrue({ClueType.SAME, ClueType.DIFFERENT, ClueType.EXACTLY}.issubset(types))
        self.assertTrue({RegionType.ROW, RegionType.COLUMN}.issubset(regions))

    def test_advanced_is_unique_progressive_and_has_real_multi_component_support(self) -> None:
        self.assertEqual(self.advanced["size"], 4)
        self.assertTrue(self.advanced["consistent"])
        self.assertTrue(self.advanced["unique"])
        self.assertTrue(self.advanced["progressively_solvable"])
        self.assertEqual(self.advanced["deduction_steps"], 13)
        self.assertGreaterEqual(self.advanced["maximum_support_size"], 2)
        self.assertTrue(any(step["support_size"] >= 2 for step in self.advanced["steps"]))
        self.assertEqual(self.advanced["direct_single_fact_deductions"], 0)

    def test_advanced_uses_counting_regions_relations_and_both_extensions(self) -> None:
        puzzle = PuzzleLoader.load(puzzle_path(ADVANCED_ID))
        types = {card.clue.type for card in puzzle.cards}
        regions = {
            card.clue.region.kind
            for card in puzzle.cards
            if card.clue.region is not None
        }
        self.assertTrue(
            {
                ClueType.SAME,
                ClueType.DIFFERENT,
                ClueType.EXACTLY,
                ClueType.AT_LEAST,
                ClueType.AT_MOST,
                ClueType.IMPLIES,
                ClueType.ODD,
            }.issubset(types)
        )
        self.assertEqual(
            regions,
            {RegionType.ROW, RegionType.COLUMN, RegionType.NEIGHBORS, RegionType.EXPLICIT},
        )

    def test_quality_profile_records_public_support_ids_without_answers(self) -> None:
        first = self.advanced["steps"][0]
        self.assertEqual(first["target"], "B1")
        self.assertGreaterEqual(first["support_size"], 2)
        self.assertEqual(first["supporting_clue_ids"], ["A4-01", "A4-04"])
        self.assertEqual(first["supporting_known_verdict_ids"], ["A1"])
        self.assertNotIn("hidden", repr(first).casefold())


if __name__ == "__main__":
    unittest.main()
