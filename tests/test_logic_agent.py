from __future__ import annotations

import unittest
from pathlib import Path

from agent.logic_agent import LogicAgent
from core.enums import Classification, Status, VerdictOutcome
from core.public_state import KnownVerdict, PublicKnowledgeState, RevealedClue
from game.game_engine import GameEngine
from game.puzzle_loader import PuzzleLoader
from tests.fixture_paths import PUZZLE_FIXTURES


SAMPLE_PATH = PUZZLE_FIXTURES / "sample_3x3.json"


class LogicAgentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.puzzle = PuzzleLoader.load(SAMPLE_PATH)
        self.engine = GameEngine(self.puzzle, LogicAgent())
        self.agent = LogicAgent()

    def test_entailment_classifies_innocent_criminal_unknown_and_inconsistent(self) -> None:
        initial = self.engine.public_state()
        self.assertEqual(self.agent.classify(initial, "B1"), Classification.INNOCENT)
        self.assertEqual(self.agent.classify(initial, "C1"), Classification.UNKNOWN)

        self.engine.submit_verdict("B1", Status.INNOCENT)
        self.assertEqual(self.agent.classify(self.engine.public_state(), "C1"), Classification.CRIMINAL)

        inconsistent = PublicKnowledgeState(
            initial.puzzle_id,
            initial.title,
            initial.size,
            initial.characters,
            initial.revealed_clues,
            (*initial.known_verdicts, KnownVerdict("B1", Status.CRIMINAL)),
            False,
        )
        self.assertEqual(self.agent.classify(inconsistent, "C1"), Classification.INCONSISTENT)

    def test_check_verdict_and_classify_all_never_guess(self) -> None:
        state = self.engine.public_state()
        self.assertEqual(
            self.agent.check_verdict(state, "B1", Status.INNOCENT),
            VerdictOutcome.ACCEPTED,
        )
        self.assertEqual(
            self.agent.check_verdict(state, "B1", Status.CRIMINAL),
            VerdictOutcome.CONTRADICTED,
        )
        classifications = self.agent.classify_all(state)
        self.assertEqual(classifications["B1"], Classification.INNOCENT)
        self.assertTrue(all(value is Classification.UNKNOWN for key, value in classifications.items() if key != "B1"))

    def test_hint_is_non_mutating_and_trace_records_sat_queries(self) -> None:
        before = self.engine.public_state()
        hint = self.engine.get_hint()
        self.assertEqual(self.engine.public_state(), before)
        self.assertEqual((hint.deduction.character_id, hint.deduction.status), ("B1", Status.INNOCENT))
        trace = self.engine.deduction_trace[-1]
        self.assertEqual(trace.active_clue_ids, ("CL-01",))
        self.assertEqual(trace.verdict, Classification.INNOCENT)
        self.assertGreaterEqual(len(trace.sat_queries), 3)
        self.assertIsNone(trace.newly_revealed_clue)

    def test_solve_next_and_auto_solve_progressively_reveal(self) -> None:
        first = self.engine.solve_next()
        self.assertEqual((first.character_id, first.revealed_clue.id), ("B1", "CL-02"))
        self.assertEqual(self.engine.deduction_trace[-1].newly_revealed_clue, "CL-02")
        remaining = self.engine.auto_solve()
        self.assertEqual(len(remaining), 7)
        self.assertTrue(self.engine.public_state().is_complete)
        self.assertEqual(len(self.engine.public_state().revealed_clues), 9)

    def test_complete_clue_set_uniqueness_is_separate_from_public_kb(self) -> None:
        with self.assertRaisesRegex(ValueError, "complete clue set"):
            self.agent.check_uniqueness(self.engine.public_state())

        complete = PublicKnowledgeState(
            self.puzzle.id,
            self.puzzle.title,
            self.puzzle.size,
            tuple(card.character for card in self.puzzle.ordered_cards),
            tuple(
                RevealedClue(card.character.id, card.clue)
                for card in self.puzzle.ordered_cards
            ),
            (),
            False,
        )
        complete_result = self.agent.check_uniqueness(complete)
        self.assertTrue(complete_result.is_consistent)
        self.assertTrue(complete_result.is_unique)


if __name__ == "__main__":
    unittest.main()
