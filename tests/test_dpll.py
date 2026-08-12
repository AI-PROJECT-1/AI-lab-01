from sat.dpll import DPLLSolver
from sat.sat_result import SATStatus


def test_trivial_sat():
    solver = DPLLSolver()

    result = solver.solve(
        [[1]],
        variable_count=1,
    )

    assert result.status is SATStatus.SAT
    assert result.assignment == {1: True}


def test_trivial_unsat():
    solver = DPLLSolver()

    result = solver.solve(
        [
            [1],
            [-1],
        ],
        variable_count=1,
    )

    assert result.status is SATStatus.UNSAT
    assert result.assignment is None


def test_unit_propagation():
    solver = DPLLSolver()

    result = solver.solve(
        [
            [1],
            [-1, 2],
        ],
        variable_count=2,
    )

    assert result.status is SATStatus.SAT
    assert result.assignment[1] is True
    assert result.assignment[2] is True
    assert result.statistics.propagations >= 2


def test_multiple_unit_propagations():
    solver = DPLLSolver()

    result = solver.solve(
        [
            [-3],
            [-1, 3],
            [1, 2],
        ],
        variable_count=3,
    )

    assert result.status is SATStatus.SAT

    assert result.assignment == {
        1: False,
        2: True,
        3: False,
    }


def test_conflict_detection():
    solver = DPLLSolver()

    result = solver.solve(
        [
            [1],
            [-1],
        ],
        variable_count=1,
    )

    assert result.status is SATStatus.UNSAT


def test_branching():
    solver = DPLLSolver()

    result = solver.solve(
        [
            [1, 2],
            [-1, 2],
        ],
        variable_count=2,
    )

    assert result.status is SATStatus.SAT
    assert result.assignment[2] is True
    assert result.statistics.decisions >= 1


def test_backtracking():
    solver = DPLLSolver()

    result = solver.solve(
        [
            [-1, 2],
            [-1, -2],
            [1, 2],
        ],
        variable_count=2,
    )

    assert result.status is SATStatus.SAT
    assert result.assignment[1] is False
    assert result.assignment[2] is True

    assert result.statistics.decisions >= 1
    assert result.statistics.backtracks >= 1

def test_complete_assignment():
    solver = DPLLSolver()

    result = solver.solve(
        [[1]],
        variable_count=3,
    )

    assert result.status is SATStatus.SAT

    assert set(result.assignment.keys()) == {
        1,
        2,
        3,
    }


def test_deterministic_behavior():
    clauses = [
        [1, 2],
        [-1, 2],
    ]

    solver1 = DPLLSolver()
    solver2 = DPLLSolver()

    result1 = solver1.solve(
        clauses,
        variable_count=2,
    )

    result2 = solver2.solve(
        clauses,
        variable_count=2,
    )

    assert result1.assignment == result2.assignment
    assert (
        result1.statistics.decisions
        == result2.statistics.decisions
    )


def test_assumption_sat():
    solver = DPLLSolver()

    result = solver.solve(
        [[1, 2]],
        variable_count=2,
        assumptions=[-1],
    )

    assert result.status is SATStatus.SAT
    assert result.assignment[1] is False
    assert result.assignment[2] is True


def test_assumption_unsat():
    solver = DPLLSolver()

    result = solver.solve(
        [[1]],
        variable_count=1,
        assumptions=[-1],
    )

    assert result.status is SATStatus.UNSAT