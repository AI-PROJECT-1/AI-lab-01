"""Level 3 engine/loader tests, including the hidden/public boundary."""

from __future__ import annotations

import json
import unittest
from dataclasses import fields
from pathlib import Path
from unittest.mock import mock_open, patch

from agent.mock_logic_agent import MockLogicAgent
from core.enums import Classification, Status, VerdictOutcome
from core.public_state import KnownVerdict, PublicKnowledgeState
from game.game_engine import AgentIntegrityError, GameEngine
from game.puzzle_loader import PuzzleFormatError, PuzzleLoader
from tests.fixture_paths import PUZZLE_FIXTURES


SAMPLE_PATH = PUZZLE_FIXTURES / "sample_3x3.json"


class PuzzleLoaderTests(unittest.TestCase):
    def test_loads_sample_into_validated_domain(self) -> None:
        puzzle = PuzzleLoader.load(SAMPLE_PATH)
        self.assertEqual((puzzle.size, len(puzzle.cards)), (3, 9))
        self.assertEqual(puzzle.initially_revealed_ids, ("A1",))
        self.assertEqual(puzzle.card_by_id("B1").hidden_status, Status.INNOCENT)

    def test_rejects_unknown_fields_and_invalid_json(self) -> None:
        data = json.loads(SAMPLE_PATH.read_text(encoding="utf-8"))
        data["unexpected"] = True
        with self.assertRaisesRegex(PuzzleFormatError, "unknown fields"):
            PuzzleLoader.from_dict(data)

        with patch("pathlib.Path.open", mock_open(read_data="{not-json")):
            with self.assertRaisesRegex(PuzzleFormatError, "invalid JSON"):
                PuzzleLoader.load("bad.json")

    def test_rejects_invalid_status(self) -> None:
        data = json.loads(SAMPLE_PATH.read_text(encoding="utf-8"))
        data["cards"][0]["status"] = "MAYBE"
        with self.assertRaisesRegex(PuzzleFormatError, "CRIMINAL, INNOCENT"):
            PuzzleLoader.from_dict(data)


class CapturingAgent:
    def __init__(self, classification: Classification = Classification.UNKNOWN) -> None:
        self.classification = classification
        self.seen_states: list[PublicKnowledgeState] = []

    def classify(self, public_state: PublicKnowledgeState, character_id: str) -> Classification:
        self.seen_states.append(public_state)
        return self.classification


class GameEngineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.puzzle = PuzzleLoader.load(SAMPLE_PATH)
        self.engine = GameEngine(self.puzzle, MockLogicAgent())

    def test_initial_public_state_contains_only_face_up_data(self) -> None:
        state = self.engine.public_state()
        self.assertEqual(tuple(item.character_id for item in state.known_verdicts), ("A1",))
        self.assertEqual(tuple(item.owner_id for item in state.revealed_clues), ("A1",))
        self.assertNotIn("CL-02", repr(state))
        field_names = {field.name.casefold() for field in fields(PublicKnowledgeState)}
        self.assertFalse(any("hidden" in name or "solution" in name for name in field_names))

    def test_agent_receives_only_public_snapshot(self) -> None:
        agent = CapturingAgent()
        engine = GameEngine(self.puzzle, agent)
        result = engine.submit_verdict("C1", Status.CRIMINAL)
        self.assertEqual(result.outcome, VerdictOutcome.NOT_PROVABLE)
        self.assertEqual(len(agent.seen_states), 1)
        self.assertIsInstance(agent.seen_states[0], PublicKnowledgeState)
        self.assertNotIn("CL-02", repr(agent.seen_states[0]))

    def test_accept_reveals_and_reject_does_not_mutate(self) -> None:
        before = self.engine.public_state()
        rejected = self.engine.submit_verdict("B1", Status.CRIMINAL)
        self.assertEqual(rejected.outcome, VerdictOutcome.CONTRADICTED)
        self.assertEqual(self.engine.public_state(), before)

        accepted = self.engine.submit_verdict("B1", Status.INNOCENT)
        self.assertEqual(accepted.outcome, VerdictOutcome.ACCEPTED)
        self.assertEqual(accepted.revealed_clue.id, "CL-02")
        self.assertEqual(self.engine.public_state().status_of("B1"), Status.INNOCENT)

    def test_unknown_verdict_does_not_reveal(self) -> None:
        result = self.engine.submit_verdict("C1", Status.CRIMINAL)
        self.assertEqual(result.outcome, VerdictOutcome.NOT_PROVABLE)
        self.assertIsNone(self.engine.public_state().clue_for("C1"))

    def test_restart_restores_only_initial_cards(self) -> None:
        self.engine.submit_verdict("B1", Status.INNOCENT)
        old_snapshot = self.engine.public_state()
        restarted = self.engine.restart()
        self.assertEqual(tuple(v.character_id for v in restarted.known_verdicts), ("A1",))
        self.assertEqual(old_snapshot.status_of("B1"), Status.INNOCENT)
        self.assertIsNone(restarted.status_of("B1"))

    def test_load_replaces_state_and_restarts(self) -> None:
        self.engine.submit_verdict("B1", Status.INNOCENT)
        loaded = self.engine.load(self.puzzle)
        self.assertEqual(loaded.puzzle_id, self.puzzle.id)
        self.assertIsNone(loaded.status_of("B1"))
        self.assertEqual(tuple(item.owner_id for item in loaded.revealed_clues), ("A1",))

    def test_fact_chain_can_complete_without_guessing(self) -> None:
        verdicts = (
            ("B1", Status.INNOCENT), ("C1", Status.CRIMINAL),
            ("A2", Status.INNOCENT), ("B2", Status.CRIMINAL),
            ("C2", Status.INNOCENT), ("A3", Status.CRIMINAL),
            ("B3", Status.INNOCENT), ("C3", Status.CRIMINAL),
        )
        for character_id, status in verdicts:
            self.assertEqual(
                self.engine.submit_verdict(character_id, status).outcome,
                VerdictOutcome.ACCEPTED,
            )
        self.assertTrue(self.engine.public_state().is_complete)

    def test_agent_integrity_failure_never_reveals(self) -> None:
        engine = GameEngine(self.puzzle, CapturingAgent(Classification.CRIMINAL))
        before = engine.public_state()
        with self.assertRaises(AgentIntegrityError):
            engine.submit_verdict("B1", Status.CRIMINAL)
        self.assertEqual(engine.public_state(), before)

    def test_mock_agent_detects_conflicting_public_fact_and_verdict(self) -> None:
        state = self.engine.public_state()
        conflicting = PublicKnowledgeState(
            state.puzzle_id,
            state.title,
            state.size,
            state.characters,
            state.revealed_clues,
            (*state.known_verdicts, KnownVerdict("B1", Status.CRIMINAL)),
            False,
        )
        self.assertEqual(
            MockLogicAgent().classify(conflicting, "B1"),
            Classification.INCONSISTENT,
        )


if __name__ == "__main__":
    unittest.main()
