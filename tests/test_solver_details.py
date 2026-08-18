"""UI Phase 6 contracts for secondary, structured solver details."""

from __future__ import annotations

import unittest
from pathlib import Path

from agent.deduction_trace import DeductionTraceStep, SATQueryTrace
from agent.logic_agent import LogicAgent
from core.enums import Classification, Status
from game.game_engine import GameEngine
from game.puzzle_loader import PuzzleLoader
from gui.controller import GameController
from gui.hint_session import progress_hint_session
from gui.trace_panel import (
    ActionSource,
    SolverDetailsModel,
    build_trace_presentations,
)
from tests.fixture_paths import PUZZLE_FIXTURES


ROOT = Path(__file__).parents[1]
SAMPLE_PATH = PUZZLE_FIXTURES / "sample_3x3.json"
EXTENSION_PATH = PUZZLE_FIXTURES / "extension_chain_3x3.json"


class SolverDetailsPresentationTests(unittest.TestCase):
    def setUp(self) -> None:
        puzzle = PuzzleLoader.load(SAMPLE_PATH)
        self.controller = GameController(GameEngine(puzzle, LogicAgent()))
        self.model = SolverDetailsModel()

    def _record_action(self, callback, source: ActionSource):
        before = len(self.controller.trace())
        result = callback()
        self.model.record_new_steps(before, self.controller.trace(), source)
        return result

    def test_details_are_closed_by_default(self) -> None:
        self.assertFalse(self.model.is_open)

    def test_open_and_close_do_not_mutate_public_state_or_trace(self) -> None:
        before_state = self.controller.state()
        before_trace = self.controller.trace()
        self.model.open()
        self.assertTrue(self.model.is_open)
        self.model.close()
        self.assertFalse(self.model.is_open)
        self.assertEqual(self.controller.state(), before_state)
        self.assertEqual(self.controller.trace(), before_trace)

    def test_existing_trace_data_is_accessible_as_structured_steps(self) -> None:
        self._record_action(self.controller.hint, ActionSource.HINT)
        trace = self.controller.trace()
        views = self.model.presentations(trace)
        self.assertEqual(len(views), len(trace))
        self.assertEqual(views[0].step_number, trace[0].step_number)
        self.assertEqual(views[0].target, trace[0].character_id)
        self.assertEqual(views[0].verdict, trace[0].verdict.value)

    def test_active_clue_ids_are_copied_exactly_and_in_order(self) -> None:
        step = DeductionTraceStep(
            41,
            ("CL-Z9", "CL-A1", "CL-LONG-003"),
            "B2",
            (),
            Classification.UNKNOWN,
        )
        view = build_trace_presentations((step,))[0]
        self.assertEqual(view.active_clue_ids, step.active_clue_ids)

    def test_sat_assumptions_results_and_per_query_statistics_are_not_invented(self) -> None:
        self.controller.hint()
        raw = self.controller.trace()[0]
        view = build_trace_presentations((raw,))[0]
        self.assertIsNone(view.sat_queries[0].assumption)
        self.assertEqual(view.sat_queries[0].result, raw.sat_queries[0].result)
        for query_view, query in zip(view.sat_queries, raw.sat_queries, strict=True):
            expected = query.assumption.value if query.assumption is not None else None
            self.assertEqual(query_view.assumption, expected)
            self.assertEqual(
                (
                    query_view.decisions,
                    query_view.propagations,
                    query_view.backtracks,
                    query_view.runtime,
                ),
                (query.decisions, query.propagations, query.backtracks, query.runtime),
            )

    def test_missing_sat_queries_remain_missing(self) -> None:
        step = DeductionTraceStep(1, (), None, (), Classification.UNKNOWN)
        self.assertEqual(build_trace_presentations((step,))[0].sat_queries, ())

    def test_newly_revealed_clue_is_preserved_from_real_trace(self) -> None:
        result = self._record_action(self.controller.solve_next, ActionSource.SOLVE_NEXT)
        latest = self.model.presentations(self.controller.trace())[-1]
        self.assertEqual(latest.newly_revealed_clue, result.revealed_clue.id)
        self.assertEqual(latest.newly_revealed_clue, self.controller.trace()[-1].newly_revealed_clue)

    def test_unrevealed_clue_content_and_hidden_solution_are_not_added(self) -> None:
        self._record_action(self.controller.hint, ActionSource.HINT)
        rendered_data = repr(self.model.presentations(self.controller.trace()))
        self.assertNotIn("CL-02", rendered_data)
        self.assertNotIn("C1 is criminal", rendered_data)
        source = (ROOT / "gui" / "trace_panel.py").read_text(encoding="utf-8")
        for forbidden in ("hidden_status", "hidden_solution", "core.puzzle", "game.game_engine"):
            self.assertNotIn(forbidden, source)

    def test_hint_stage_two_adds_no_trace_or_solver_detail_step(self) -> None:
        before = len(self.controller.trace())
        session, _presentation, requested = progress_hint_session(
            None,
            self.controller.state,
            self.controller.hint,
            self.controller.trace,
        )
        self.assertTrue(requested)
        self.model.record_new_steps(before, self.controller.trace(), ActionSource.HINT)
        stage_one_count = len(self.model.presentations(self.controller.trace()))

        session, _presentation, requested = progress_hint_session(
            session,
            self.controller.state,
            self.controller.hint,
            self.controller.trace,
        )
        self.assertFalse(requested)
        self.assertEqual(len(self.controller.trace()), stage_one_count)
        self.assertEqual(len(self.model.presentations(self.controller.trace())), stage_one_count)

    def test_hint_stage_one_adds_only_the_real_reasoning_slice(self) -> None:
        before = len(self.controller.trace())
        _session, _presentation, requested = progress_hint_session(
            None,
            self.controller.state,
            self.controller.hint,
            self.controller.trace,
        )
        after = self.controller.trace()
        self.assertTrue(requested)
        self.assertEqual(len(after) - before, 1)
        self.model.record_new_steps(before, after, ActionSource.HINT)
        self.assertTrue(all(view.source is ActionSource.HINT for view in self.model.presentations(after)))

    def test_solve_next_uses_real_trace_and_reveal(self) -> None:
        before_state = self.controller.state()
        result = self._record_action(self.controller.solve_next, ActionSource.SOLVE_NEXT)
        self.assertIsNone(before_state.status_of(result.character_id))
        self.assertIsNotNone(self.controller.state().status_of(result.character_id))
        latest = self.model.presentations(self.controller.trace())[-1]
        self.assertEqual(latest.source, ActionSource.SOLVE_NEXT)
        self.assertEqual(latest.target, result.character_id)
        self.assertEqual(latest.newly_revealed_clue, result.revealed_clue.id)

    def test_manual_verdict_labels_only_its_real_trace_slice(self) -> None:
        self.controller.select_character("B1")
        result = self._record_action(
            lambda: self.controller.submit_selected(Status.INNOCENT),
            ActionSource.MANUAL_VERDICT,
        )
        latest = self.model.presentations(self.controller.trace())[-1]
        self.assertEqual(latest.source, ActionSource.MANUAL_VERDICT)
        self.assertEqual(latest.target, result.character_id)
        self.assertEqual(latest.newly_revealed_clue, result.revealed_clue.id)

    def test_auto_solve_steps_progressively_extend_details(self) -> None:
        counts: list[int] = []
        for _ in range(3):
            self._record_action(self.controller.solve_next, ActionSource.AUTO_SOLVE)
            counts.append(len(self.model.presentations(self.controller.trace())))
        self.assertEqual(counts, sorted(counts))
        self.assertEqual(len(set(counts)), 3)
        self.assertTrue(
            all(view.source is ActionSource.AUTO_SOLVE for view in self.model.presentations(self.controller.trace()))
        )

    def test_restart_clears_trace_and_stale_source_metadata(self) -> None:
        self._record_action(self.controller.solve_next, ActionSource.SOLVE_NEXT)
        self.assertTrue(self.controller.trace())
        self.controller.restart()
        self.model.clear_trace_metadata()
        self.assertEqual(self.controller.trace(), ())
        self.assertEqual(self.model.presentations(self.controller.trace()), ())
        self.assertEqual(self.model._sources, {})

    def test_load_clears_trace_and_stale_source_metadata(self) -> None:
        self._record_action(self.controller.hint, ActionSource.HINT)
        self.controller.load(PuzzleLoader.load(EXTENSION_PATH))
        self.model.clear_trace_metadata()
        self.assertEqual(self.controller.trace(), ())
        self.assertEqual(self.model._sources, {})

    def test_action_source_is_present_only_when_reliably_recorded(self) -> None:
        self.controller.hint()
        unknown = self.model.presentations(self.controller.trace())
        self.assertTrue(unknown)
        self.assertTrue(all(view.source is None for view in unknown))

        before = len(self.controller.trace())
        self.controller.solve_next()
        self.model.record_new_steps(before, self.controller.trace(), ActionSource.SOLVE_NEXT)
        labeled = self.model.presentations(self.controller.trace())
        self.assertTrue(all(view.source is None for view in labeled[:before]))
        self.assertTrue(all(view.source is ActionSource.SOLVE_NEXT for view in labeled[before:]))

    def test_opening_details_does_not_affect_verdict_selection_or_hint_session(self) -> None:
        self.controller.select_character("B2")
        session, _presentation, _requested = progress_hint_session(
            None,
            self.controller.state,
            self.controller.hint,
            self.controller.trace,
        )
        state = self.controller.state()
        trace = self.controller.trace()
        self.model.open()
        self.model.close()
        self.assertEqual(self.controller.selected_character_id, "B2")
        self.assertEqual(self.controller.state(), state)
        self.assertEqual(self.controller.trace(), trace)
        self.assertIsNotNone(session)

    def test_raw_query_purpose_is_preserved_without_clause_level_proof(self) -> None:
        query = SATQueryTrace("custom purpose", Status.CRIMINAL, "UNSAT", 3, 4, 5, 0.125)
        step = DeductionTraceStep(7, ("CL-01",), "D4", (query,), Classification.INNOCENT)
        view = build_trace_presentations((step,))[0]
        self.assertEqual(view.sat_queries[0].purpose, "custom purpose")
        self.assertEqual(view.sat_queries[0].assumption, "CRIMINAL")
        self.assertEqual(view.sat_queries[0].result, "UNSAT")


if __name__ == "__main__":
    unittest.main()
