from __future__ import annotations

from time import perf_counter
from typing import Iterable, Sequence

from sat.sat_result import SATResult, SATStatus
from sat.statistics import SATStatistics


Clause = tuple[int, ...]
CNF = tuple[Clause, ...]


class DPLLSolver:
    """Deterministic DPLL SAT solver."""

    def __init__(self) -> None:
        self.statistics = SATStatistics()
        self._variable_count = 0

    def solve(
        self,
        clauses: Sequence[Sequence[int]],
        variable_count: int,
        assumptions: Iterable[int] = (),
    ) -> SATResult:

        if variable_count < 0:
            raise ValueError("variable_count must be non-negative")

        normalized_clauses = tuple(
            tuple(clause)
            for clause in clauses
        )

        normalized_assumptions = tuple(assumptions)

        self._validate_literals(
            normalized_clauses,
            variable_count,
        )

        self._validate_assumptions(
            normalized_assumptions,
            variable_count,
        )

        working_clauses = normalized_clauses + tuple(
            (literal,)
            for literal in normalized_assumptions
        )

        self.statistics = SATStatistics()
        self._variable_count = variable_count

        start_time = perf_counter()

        assignment = self._dpll(
            working_clauses,
            {},
        )

        self.statistics.runtime = (
            perf_counter() - start_time
        )

        if assignment is None:
            return SATResult(
                status=SATStatus.UNSAT,
                assignment=None,
                statistics=self.statistics,
            )

        complete_assignment = (
            self._complete_assignment(assignment)
        )

        return SATResult(
            status=SATStatus.SAT,
            assignment=complete_assignment,
            statistics=self.statistics,
        )

    def _dpll(
        self,
        clauses: CNF,
        assignment: dict[int, bool],
    ) -> dict[int, bool] | None:

        current_assignment = assignment.copy()

        if not self._unit_propagate(
            clauses,
            current_assignment,
        ):
            return None

        if self._has_conflict(
            clauses,
            current_assignment,
        ):
            return None

        if self._all_clauses_satisfied(
            clauses,
            current_assignment,
        ):
            return current_assignment

        variable = self._choose_variable(
            current_assignment
        )

        if variable is None:
            return None

        self.statistics.decisions += 1

        true_assignment = current_assignment.copy()
        true_assignment[variable] = True

        result = self._dpll(
            clauses,
            true_assignment,
        )

        if result is not None:
            return result

        self.statistics.backtracks += 1

        false_assignment = current_assignment.copy()
        false_assignment[variable] = False

        return self._dpll(
            clauses,
            false_assignment,
        )

    def _unit_propagate(
        self,
        clauses: CNF,
        assignment: dict[int, bool],
    ) -> bool:

        while True:
            unit_literal = self._find_unit_literal(
                clauses,
                assignment,
            )

            if unit_literal is None:
                return True

            variable = abs(unit_literal)
            value = unit_literal > 0

            if variable in assignment:
                if assignment[variable] != value:
                    return False

                continue

            assignment[variable] = value
            self.statistics.propagations += 1

            if self._has_conflict(
                clauses,
                assignment,
            ):
                return False

    def _find_unit_literal(
        self,
        clauses: CNF,
        assignment: dict[int, bool],
    ) -> int | None:

        for clause in clauses:
            satisfied = False
            unassigned_literals = []

            for literal in clause:
                variable = abs(literal)

                if variable not in assignment:
                    unassigned_literals.append(
                        literal
                    )
                    continue

                if self._literal_is_true(
                    literal,
                    assignment[variable],
                ):
                    satisfied = True
                    break

            if satisfied:
                continue

            if len(unassigned_literals) == 1:
                return unassigned_literals[0]

        return None

    def _has_conflict(
        self,
        clauses: CNF,
        assignment: dict[int, bool],
    ) -> bool:

        for clause in clauses:
            satisfied = False
            has_unassigned = False

            for literal in clause:
                variable = abs(literal)

                if variable not in assignment:
                    has_unassigned = True
                    continue

                if self._literal_is_true(
                    literal,
                    assignment[variable],
                ):
                    satisfied = True
                    break

            if not satisfied and not has_unassigned:
                return True

        return False

    def _all_clauses_satisfied(
        self,
        clauses: CNF,
        assignment: dict[int, bool],
    ) -> bool:

        for clause in clauses:
            clause_satisfied = False

            for literal in clause:
                variable = abs(literal)

                if variable not in assignment:
                    continue

                if self._literal_is_true(
                    literal,
                    assignment[variable],
                ):
                    clause_satisfied = True
                    break

            if not clause_satisfied:
                return False

        return True

    def _choose_variable(
        self,
        assignment: dict[int, bool],
    ) -> int | None:

        for variable in range(
            1,
            self._variable_count + 1,
        ):
            if variable not in assignment:
                return variable

        return None

    def _complete_assignment(
        self,
        assignment: dict[int, bool],
    ) -> dict[int, bool]:

        complete = assignment.copy()

        for variable in range(
            1,
            self._variable_count + 1,
        ):
            if variable not in complete:
                complete[variable] = False

        return complete

    @staticmethod
    def _literal_is_true(
        literal: int,
        value: bool,
    ) -> bool:

        if literal > 0:
            return value

        return not value

    @staticmethod
    def _validate_literals(
        clauses: CNF,
        variable_count: int,
    ) -> None:

        for clause in clauses:
            for literal in clause:
                if literal == 0:
                    raise ValueError(
                        "literal 0 is invalid"
                    )

                if abs(literal) > variable_count:
                    raise ValueError(
                        f"literal {literal} exceeds "
                        f"variable_count={variable_count}"
                    )

    @staticmethod
    def _validate_assumptions(
        assumptions: tuple[int, ...],
        variable_count: int,
    ) -> None:

        for literal in assumptions:
            if literal == 0:
                raise ValueError(
                    "assumption literal cannot be 0"
                )

            if abs(literal) > variable_count:
                raise ValueError(
                    f"assumption {literal} exceeds "
                    f"variable_count={variable_count}"
                )