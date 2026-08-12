"""Direct semantic evaluator for core clue types."""

from __future__ import annotations

from core.clue import Clue
from core.enums import ClueType, Status
from logic.region_resolver import RegionResolver
from typing import Mapping

Assignment = Mapping[str, bool]


def evaluate(clue: Clue, assignment: Assignment) -> bool:
    if clue.type is ClueType.FACT:
        return _evaluate_fact(clue, assignment)
    if clue.type is ClueType.SAME:
        return _evaluate_same(clue, assignment)
    if clue.type is ClueType.DIFFERENT:
        return _evaluate_different(clue, assignment)
    if clue.type is ClueType.IMPLIES:
        return _evaluate_implies(clue, assignment)
    if clue.type is ClueType.EXACTLY:
        return _evaluate_exactly(clue, assignment)
    if clue.type is ClueType.AT_LEAST:
        return _evaluate_at_least(clue, assignment)
    if clue.type is ClueType.AT_MOST:
        return _evaluate_at_most(clue, assignment)
    if clue.type is ClueType.ODD:
        return _assignment_count(clue, assignment) % 2 == 1
    raise ValueError(f"unsupported clue type: {clue.type!r}")


def _evaluate_fact(clue: Clue, assignment: Assignment) -> bool:
    value = assignment[clue.target]
    expected = clue.status is Status.CRIMINAL
    return value is expected


def _evaluate_same(clue: Clue, assignment: Assignment) -> bool:
    first, second = clue.characters
    return assignment[first] == assignment[second]


def _evaluate_different(clue: Clue, assignment: Assignment) -> bool:
    first, second = clue.characters
    return assignment[first] != assignment[second]


def _evaluate_implies(clue: Clue, assignment: Assignment) -> bool:
    antecedent, consequent = clue.characters
    return not assignment[antecedent] or assignment[consequent]


def _assignment_count(clue: Clue, assignment: Assignment) -> int:
    region = clue.region
    ids = RegionResolver(tuple(assignment)).resolve(region)
    if clue.k is not None and clue.k > len(ids):
        raise ValueError(
            f"clue {clue.id} has k={clue.k} greater than region size {len(ids)}"
        )
    return sum(1 for character_id in ids if assignment[character_id])


def _evaluate_exactly(clue: Clue, assignment: Assignment) -> bool:
    return _assignment_count(clue, assignment) == clue.k


def _evaluate_at_least(clue: Clue, assignment: Assignment) -> bool:
    return _assignment_count(clue, assignment) >= clue.k


def _evaluate_at_most(clue: Clue, assignment: Assignment) -> bool:
    return _assignment_count(clue, assignment) <= clue.k
