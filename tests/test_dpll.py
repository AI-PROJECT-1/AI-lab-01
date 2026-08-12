"""Level 5 tests for the team-implemented deterministic DPLL solver."""

from __future__ import annotations

import itertools
import random
import unittest

from sat.dpll import DPLLSolver
from sat.sat_result import SATStatus


class DPLLSolverTests(unittest.TestCase):
    def test_trivial_sat(self) -> None:
        result = DPLLSolver().solve([[1]], variable_count=1)
        self.assertIs(result.status, SATStatus.SAT)
        self.assertEqual(result.assignment, {1: True})

    def test_trivial_unsat(self) -> None:
        result = DPLLSolver().solve([[1], [-1]], variable_count=1)
        self.assertIs(result.status, SATStatus.UNSAT)
        self.assertIsNone(result.assignment)

    def test_unit_propagation(self) -> None:
        result = DPLLSolver().solve([[1], [-1, 2]], variable_count=2)
        self.assertIs(result.status, SATStatus.SAT)
        self.assertEqual(result.assignment, {1: True, 2: True})
        self.assertGreaterEqual(result.statistics.propagations, 2)

    def test_multiple_unit_propagations(self) -> None:
        result = DPLLSolver().solve([[-3], [-1, 3], [1, 2]], variable_count=3)
        self.assertIs(result.status, SATStatus.SAT)
        self.assertEqual(result.assignment, {1: False, 2: True, 3: False})

    def test_empty_clause_is_an_immediate_conflict(self) -> None:
        result = DPLLSolver().solve([[]], variable_count=0)
        self.assertIs(result.status, SATStatus.UNSAT)

    def test_branching(self) -> None:
        result = DPLLSolver().solve([[1, 2], [-1, 2]], variable_count=2)
        self.assertIs(result.status, SATStatus.SAT)
        self.assertTrue(result.assignment[2])
        self.assertGreaterEqual(result.statistics.decisions, 1)

    def test_backtracking(self) -> None:
        result = DPLLSolver().solve([[-1, 2], [-1, -2], [1, 2]], variable_count=2)
        self.assertIs(result.status, SATStatus.SAT)
        self.assertEqual(result.assignment, {1: False, 2: True})
        self.assertGreaterEqual(result.statistics.decisions, 1)
        self.assertGreaterEqual(result.statistics.backtracks, 1)

    def test_complete_assignment(self) -> None:
        result = DPLLSolver().solve([[1]], variable_count=3)
        self.assertIs(result.status, SATStatus.SAT)
        self.assertEqual(set(result.assignment), {1, 2, 3})
        self.assertTrue(result.assignment[1])

    def test_deterministic_behavior(self) -> None:
        clauses = [[1, 2], [-1, 2]]
        first = DPLLSolver().solve(clauses, variable_count=2)
        second = DPLLSolver().solve(clauses, variable_count=2)
        self.assertEqual(first.assignment, second.assignment)
        self.assertEqual(first.statistics.decisions, second.statistics.decisions)
        self.assertEqual(first.statistics.propagations, second.statistics.propagations)
        self.assertEqual(first.statistics.backtracks, second.statistics.backtracks)

    def test_assumptions(self) -> None:
        sat_result = DPLLSolver().solve([[1, 2]], variable_count=2, assumptions=[-1])
        self.assertIs(sat_result.status, SATStatus.SAT)
        self.assertEqual(sat_result.assignment, {1: False, 2: True})

        unsat_result = DPLLSolver().solve([[1]], variable_count=1, assumptions=[-1])
        self.assertIs(unsat_result.status, SATStatus.UNSAT)

    def test_rejects_invalid_variable_count_and_literals(self) -> None:
        invalid_cases = (
            (([[1]], True), TypeError),
            (([[1]], 1.0), TypeError),
            (([[True]], 1), TypeError),
            (([[1.5]], 2), TypeError),
            (([[0]], 1), ValueError),
            (([[2]], 1), ValueError),
        )
        for (clauses, variable_count), error_type in invalid_cases:
            with self.subTest(clauses=clauses, variable_count=variable_count):
                with self.assertRaises(error_type):
                    DPLLSolver().solve(clauses, variable_count)

        with self.assertRaises(TypeError):
            DPLLSolver().solve([[1]], 1, assumptions=[True])

    def test_metrics_are_fresh_for_each_solve(self) -> None:
        solver = DPLLSolver()
        first = solver.solve([[-1, 2], [-1, -2], [1, 2]], 2)
        second = solver.solve([[1]], 1)
        self.assertGreaterEqual(first.statistics.backtracks, 1)
        self.assertEqual(second.statistics.backtracks, 0)
        self.assertGreaterEqual(first.statistics.runtime, 0.0)
        self.assertGreaterEqual(second.statistics.runtime, 0.0)

    def test_against_independent_brute_force_oracle(self) -> None:
        randomizer = random.Random(14003)
        for variable_count in range(0, 6):
            literals = [
                literal
                for variable in range(1, variable_count + 1)
                for literal in (variable, -variable)
            ]
            for case_number in range(100):
                clauses = [
                    [randomizer.choice(literals) for _ in range(randomizer.randrange(0, 4))]
                    if literals
                    else []
                    for _ in range(randomizer.randrange(0, 7))
                ]
                expected = self._brute_force_model(clauses, variable_count)
                actual = DPLLSolver().solve(clauses, variable_count)
                with self.subTest(variable_count=variable_count, case=case_number):
                    self.assertEqual(actual.is_sat, expected is not None)
                    if actual.assignment is not None:
                        self.assertTrue(self._satisfies(clauses, actual.assignment))
                        self.assertEqual(
                            set(actual.assignment),
                            set(range(1, variable_count + 1)),
                        )

    @classmethod
    def _brute_force_model(
        cls, clauses: list[list[int]], variable_count: int
    ) -> dict[int, bool] | None:
        for values in itertools.product((False, True), repeat=variable_count):
            assignment = {
                variable: values[variable - 1]
                for variable in range(1, variable_count + 1)
            }
            if cls._satisfies(clauses, assignment):
                return assignment
        return None

    @staticmethod
    def _satisfies(clauses: list[list[int]], assignment: dict[int, bool]) -> bool:
        return all(
            any((literal > 0) == assignment[abs(literal)] for literal in clause)
            for clause in clauses
        )


if __name__ == "__main__":
    unittest.main()
