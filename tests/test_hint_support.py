"""Phase 6.5 contracts for grounded, irreducible Hint support."""

from __future__ import annotations

import unittest
from pathlib import Path
from unittest.mock import patch

from agent.deduction_trace import Deduction, DeductionTraceStep, HintExplanation, HintResult
from agent.entailment import classify_public_target
from agent.hint_explanation import extract_irreducible_support
from agent.logic_agent import LogicAgent
from core.character import Character
from core.clue import Clue
from core.enums import Classification, ClueType, Status
from core.public_state import KnownVerdict, PublicKnowledgeState, RevealedClue
from game.game_engine import GameEngine
from game.puzzle_loader import PuzzleLoader
from gui.character_card import appearance_for
from gui.hint_session import HintVisualState, begin_hint_session, can_advance_hint, progress_hint_session
from gui.view_model import CardBaseState, CardModifiers, CardVisualState


ROOT = Path(__file__).parents[1]
SAMPLE_3X3 = ROOT / "puzzles" / "sample_3x3.json"
SAMPLE_4X4 = ROOT / "puzzles" / "fact_chain_4x4.json"


def _characters() -> tuple[Character, ...]:
    return tuple(
        Character(
            f"{chr(ord('A') + column - 1)}{row}",
            f"Person {column}{row}",
            f"Role {column}{row}",
            row,
            column,
        )
        for row in range(1, 4)
        for column in range(1, 4)
    )


def _state(
    clues: tuple[RevealedClue, ...],
    verdicts: tuple[KnownVerdict, ...] = (),
) -> PublicKnowledgeState:
    return PublicKnowledgeState(
        "support-test",
        "Support Test",
        3,
        _characters(),
        clues,
        verdicts,
        False,
    )


def _fact(owner: str, clue_id: str, target: str, status: Status) -> RevealedClue:
    return RevealedClue(owner, Clue(clue_id, ClueType.FACT, target=target, status=status))


def _different(owner: str, clue_id: str, first: str, second: str) -> RevealedClue:
    return RevealedClue(owner, Clue(clue_id, ClueType.DIFFERENT, characters=(first, second)))


class HintSupportExtractionTests(unittest.TestCase):
    def test_single_supporting_clue(self) -> None:
        state = _state((_fact("A1", "CL-ONE", "B1", Status.INNOCENT),))
        result = extract_irreducible_support(state, "B1", Status.INNOCENT)
        self.assertEqual(result.supporting_clue_ids, ("CL-ONE",))
        self.assertEqual(result.supporting_verdict_ids, ())

    def test_irrelevant_public_clue_is_removed(self) -> None:
        state = _state(
            (
                _fact("A1", "CL-TARGET", "B1", Status.INNOCENT),
                _fact("C1", "CL-IRRELEVANT", "C2", Status.CRIMINAL),
            )
        )
        result = extract_irreducible_support(state, "B1", Status.INNOCENT)
        self.assertEqual(result.supporting_clue_ids, ("CL-TARGET",))

    def test_two_clues_remain_when_both_are_required(self) -> None:
        state = _state(
            (
                _fact("A2", "CL-FACT", "A1", Status.INNOCENT),
                _different("C2", "CL-LINK", "A1", "B1"),
            )
        )
        result = extract_irreducible_support(state, "B1", Status.CRIMINAL)
        self.assertEqual(result.supporting_clue_ids, ("CL-FACT", "CL-LINK"))
        self.assertEqual(result.supporting_verdict_ids, ())

    def test_public_known_verdict_and_clue_are_both_supported(self) -> None:
        state = _state(
            (_different("C2", "CL-LINK", "A1", "B1"),),
            (KnownVerdict("A1", Status.INNOCENT),),
        )
        result = extract_irreducible_support(state, "B1", Status.CRIMINAL)
        self.assertEqual(result.supporting_clue_ids, ("CL-LINK",))
        self.assertEqual(result.supporting_verdict_ids, ("A1",))

    def test_result_is_deterministic_and_ordered(self) -> None:
        state = _state(
            (
                _different("C2", "CL-Z-LINK", "A1", "B1"),
                _fact("A2", "CL-A-FACT", "A1", Status.INNOCENT),
            )
        )
        outputs = tuple(
            extract_irreducible_support(state, "B1", Status.CRIMINAL)
            for _ in range(6)
        )
        signatures = {
            (item.supporting_clue_ids, item.supporting_verdict_ids, item.method)
            for item in outputs
        }
        self.assertEqual(
            signatures,
            {(('CL-A-FACT', 'CL-Z-LINK'), (), 'deletion_irreducible')},
        )

    def test_final_support_preserves_the_same_verdict(self) -> None:
        state = _state(
            (
                _fact("A2", "CL-FACT", "A1", Status.INNOCENT),
                _different("C2", "CL-LINK", "A1", "B1"),
                _fact("C3", "CL-NOISE", "C1", Status.CRIMINAL),
            )
        )
        result = extract_irreducible_support(state, "B1", Status.CRIMINAL)
        reduced = _state(tuple(item for item in state.revealed_clues if item.clue.id in result.supporting_clue_ids))
        self.assertEqual(
            classify_public_target(reduced, "B1").classification,
            Classification.CRIMINAL,
        )

    def test_each_remaining_component_is_individually_required_irreducibility(self) -> None:
        state = _state(
            (_different("C2", "CL-LINK", "A1", "B1"),),
            (KnownVerdict("A1", Status.INNOCENT),),
        )
        result = extract_irreducible_support(state, "B1", Status.CRIMINAL)
        for clue_id in result.supporting_clue_ids:
            reduced = _state(
                tuple(item for item in state.revealed_clues if item.clue.id != clue_id),
                tuple(item for item in state.known_verdicts if item.character_id in result.supporting_verdict_ids),
            )
            self.assertNotEqual(classify_public_target(reduced, "B1").classification, Classification.CRIMINAL)
        for character_id in result.supporting_verdict_ids:
            reduced = _state(
                tuple(item for item in state.revealed_clues if item.clue.id in result.supporting_clue_ids),
                tuple(item for item in state.known_verdicts if item.character_id != character_id),
            )
            self.assertNotEqual(classify_public_target(reduced, "B1").classification, Classification.CRIMINAL)

    def test_baseline_must_be_unresolved_consistent_and_same_forced_verdict(self) -> None:
        state = _state((_fact("A1", "CL-ONE", "B1", Status.INNOCENT),))
        self.assertIsNone(extract_irreducible_support(state, "B1", Status.CRIMINAL))
        self.assertIsNone(extract_irreducible_support(state, "C1", Status.CRIMINAL))

        already_known = _state(
            state.revealed_clues,
            (KnownVerdict("B1", Status.INNOCENT),),
        )
        self.assertIsNone(extract_irreducible_support(already_known, "B1", Status.INNOCENT))

    def test_support_contains_only_public_ids_and_never_unrevealed_clue(self) -> None:
        visible = _fact("A1", "CL-VISIBLE", "B1", Status.INNOCENT)
        _unrevealed = Clue("CL-SECRET", ClueType.FACT, target="B1", status=Status.CRIMINAL)
        state = _state((visible,))
        result = extract_irreducible_support(state, "B1", Status.INNOCENT)
        public_clues = {item.clue.id for item in state.revealed_clues}
        public_verdicts = {item.character_id for item in state.known_verdicts}
        self.assertTrue(set(result.supporting_clue_ids).issubset(public_clues))
        self.assertTrue(set(result.supporting_verdict_ids).issubset(public_verdicts))
        self.assertNotIn("CL-SECRET", repr(result))

    def test_extraction_is_non_mutating_and_does_not_change_agent_trace(self) -> None:
        engine = GameEngine(PuzzleLoader.load(SAMPLE_3X3), LogicAgent())
        state = engine.public_state()
        before = state
        hint = engine.get_hint()
        self.assertEqual(engine.public_state(), before)
        self.assertEqual(len(engine.deduction_trace), 1)
        self.assertGreater(hint.explanation.support_extraction_sat_calls, 0)
        self.assertEqual(engine.deduction_trace[-1], hint.deduction.trace)

    def test_logic_agent_falls_back_if_explanation_diagnostics_fail(self) -> None:
        state = GameEngine(PuzzleLoader.load(SAMPLE_3X3), LogicAgent()).public_state()
        agent = LogicAgent()
        with patch("agent.logic_agent.extract_irreducible_support", side_effect=RuntimeError("diagnostic failure")):
            hint = agent.get_hint(state)
        self.assertEqual(hint.deduction.character_id, "B1")
        self.assertIsNone(hint.explanation)
        self.assertEqual(len(agent.last_trace), 1)

    def test_real_3x3_and_4x4_results_report_separate_cost(self) -> None:
        for path in (SAMPLE_3X3, SAMPLE_4X4):
            with self.subTest(path=path.name):
                hint = GameEngine(PuzzleLoader.load(path), LogicAgent()).get_hint()
                self.assertIsNotNone(hint.explanation)
                self.assertGreater(hint.explanation.support_extraction_sat_calls, 0)
                self.assertGreaterEqual(hint.explanation.support_extraction_runtime, 0.0)


class HintSupportPresentationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.state = _state(
            (
                _fact("A2", "CL-FACT", "A1", Status.INNOCENT),
                _different("C2", "CL-LINK", "A1", "B1"),
                _fact("C3", "CL-NOISE", "C1", Status.CRIMINAL),
            )
        )
        trace = DeductionTraceStep(
            1,
            ("CL-FACT", "CL-LINK", "CL-NOISE"),
            "B1",
            (),
            Classification.CRIMINAL,
        )
        explanation = HintExplanation(
            "B1",
            ("CL-FACT", "CL-LINK"),
            (),
            "deletion_irreducible",
            12,
            0.01,
        )
        self.result = HintResult(
            Deduction("B1", Status.CRIMINAL, trace),
            Classification.CRIMINAL,
            "hidden verdict message",
            explanation,
        )

    def test_stage_one_prefers_support_and_omits_irrelevant_active_clue(self) -> None:
        session, presentation = begin_hint_session(self.state, self.result, (self.result.deduction.trace,))
        self.assertTrue(session.has_grounded_support)
        self.assertEqual(presentation.active_clue_ids, ("CL-FACT", "CL-LINK"))
        self.assertNotIn("CL-NOISE", repr(presentation))

    def test_multiple_support_clues_and_public_known_verdict_can_be_presented(self) -> None:
        state = _state(
            (_different("C2", "CL-LINK", "A1", "B1"),),
            (KnownVerdict("A1", Status.INNOCENT),),
        )
        trace = DeductionTraceStep(1, ("CL-LINK",), "B1", (), Classification.CRIMINAL)
        explanation = HintExplanation("B1", ("CL-LINK",), ("A1",), "deletion_irreducible", 9, 0.01)
        result = HintResult(Deduction("B1", Status.CRIMINAL, trace), Classification.CRIMINAL, "", explanation)
        session, presentation = begin_hint_session(state, result, (trace,))
        self.assertEqual(session.supporting_verdict_ids, ("A1",))
        self.assertEqual(presentation.supporting_verdict_ids, ("A1",))
        self.assertIn("A1 = INNOCENT", presentation.message)

    def test_single_clue_wording_does_not_claim_unique_or_minimum_proof(self) -> None:
        state = _state((_fact("A1", "CL-ONE", "B1", Status.INNOCENT),))
        trace = DeductionTraceStep(1, ("CL-ONE",), "B1", (), Classification.INNOCENT)
        explanation = HintExplanation("B1", ("CL-ONE",), (), "deletion_irreducible", 6, 0.01)
        result = HintResult(Deduction("B1", Status.INNOCENT, trace), Classification.INNOCENT, "", explanation)
        _session, presentation = begin_hint_session(state, result, (trace,))
        self.assertEqual(presentation.active_clue_ids, ("CL-ONE",))
        for forbidden in ("alone proves", "unique proof", "minimum proof", "proof anchor"):
            self.assertNotIn(forbidden, presentation.message.casefold())

    def test_invalid_or_nonpublic_explanation_falls_back_to_phase_five_active_clues(self) -> None:
        invalid = HintExplanation("B1", ("CL-SECRET",), (), "deletion_irreducible", 3, 0.01)
        result = HintResult(self.result.deduction, Classification.CRIMINAL, "", invalid)
        session, presentation = begin_hint_session(self.state, result, (self.result.deduction.trace,))
        self.assertFalse(session.has_grounded_support)
        self.assertEqual(presentation.active_clue_ids, ("CL-FACT", "CL-LINK", "CL-NOISE"))
        self.assertIn("currently active revealed clues", presentation.message)
        self.assertNotIn("CL-SECRET", repr(presentation))

    def test_stage_two_remains_target_only_and_does_not_request_again(self) -> None:
        calls = 0
        trace = (self.result.deduction.trace,)

        def get_hint():
            nonlocal calls
            calls += 1
            return self.result

        session, _stage_one, requested = progress_hint_session(None, lambda: self.state, get_hint, lambda: trace)
        session, stage_two, requested_again = progress_hint_session(session, lambda: self.state, get_hint, lambda: trace)
        self.assertTrue(requested)
        self.assertFalse(requested_again)
        self.assertEqual(calls, 1)
        self.assertEqual(stage_two.target_character_id, "B1")
        self.assertEqual(stage_two.active_clue_ids, ())
        self.assertEqual(stage_two.supporting_verdict_ids, ())
        for hidden in ("CRIMINAL", "INNOCENT", "CL-FACT", "CL-LINK"):
            self.assertNotIn(hidden, stage_two.message)

    def test_public_state_change_invalidates_cached_support(self) -> None:
        session, _presentation = begin_hint_session(self.state, self.result, (self.result.deduction.trace,))
        changed = PublicKnowledgeState(
            self.state.puzzle_id,
            self.state.title,
            self.state.size,
            self.state.characters,
            self.state.revealed_clues,
            (KnownVerdict("C1", Status.CRIMINAL),),
            False,
        )
        self.assertFalse(can_advance_hint(session, changed))

    def test_restart_load_and_auto_invalidation_clear_support_visuals(self) -> None:
        session, presentation = begin_hint_session(
            self.state,
            self.result,
            (self.result.deduction.trace,),
        )
        for lifecycle in ("Restart", "Load", "Auto Solve"):
            with self.subTest(lifecycle=lifecycle):
                visual = HintVisualState()
                visual.apply(session, presentation)
                self.assertEqual(visual.active_clue_ids, ("CL-FACT", "CL-LINK"))
                visual.invalidate()
                self.assertIsNone(visual.session)
                self.assertEqual(visual.active_clue_ids, ())
                self.assertEqual(visual.supporting_verdict_ids, ())

    def test_supporting_verdict_modifier_composes_with_existing_character_states(self) -> None:
        appearance = appearance_for(
            CardVisualState(
                CardBaseState.INNOCENT,
                CardModifiers(
                    selected=True,
                    clue_highlighted=True,
                    newly_revealed=True,
                    hint_support=True,
                ),
            )
        )
        self.assertIsNotNone(appearance.hint_outline)
        self.assertIsNotNone(appearance.selection_outline)
        self.assertIsNotNone(appearance.highlight_outline)
        self.assertIsNotNone(appearance.reveal_outline)


if __name__ == "__main__":
    unittest.main()
