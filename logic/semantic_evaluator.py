"""Direct semantic evaluator for core clue types."""

from __future__ import annotations

from core.character import parse_cell_id
from core.clue import Clue
from core.enums import ClueType, RegionType, Status
from core.region import Region
from typing import Mapping

Assignment = Mapping[str, bool]


def evaluate(clue: Clue, assignment: Assignment) -> bool:
    if clue.type is ClueType.FACT:
        return _evaluate_fact(clue, assignment)
    if clue.type is ClueType.SAME:
        return _evaluate_same(clue, assignment)
    if clue.type is ClueType.DIFFERENT:
        return _evaluate_different(clue, assignment)
    if clue.type is ClueType.EXACTLY:
        return _evaluate_exactly(clue, assignment)
    if clue.type is ClueType.AT_LEAST:
        return _evaluate_at_least(clue, assignment)
    if clue.type is ClueType.AT_MOST:
        return _evaluate_at_most(clue, assignment)
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


def _assignment_count(region: Region, assignment: Assignment) -> int:
    if region.kind is RegionType.EXPLICIT:
        ids = region.cells
    elif region.kind is RegionType.ROW:
        ids = tuple(
            character_id
            for character_id in assignment
            if parse_cell_id(character_id)[0] == region.index
        )
    elif region.kind is RegionType.COLUMN:
        ids = tuple(
            character_id
            for character_id in assignment
            if parse_cell_id(character_id)[1] == region.index
        )
    elif region.kind is RegionType.NEIGHBORS:
        center_row, center_column = parse_cell_id(region.center)
        ids = tuple(
            character_id
            for character_id in assignment
            if character_id != region.center
            and abs(parse_cell_id(character_id)[0] - center_row) <= 1
            and abs(parse_cell_id(character_id)[1] - center_column) <= 1
        )
    else:
        raise ValueError(f"unsupported region kind: {region.kind!r}")
    return sum(1 for character_id in ids if assignment[character_id])


def _evaluate_exactly(clue: Clue, assignment: Assignment) -> bool:
    return _assignment_count(clue.region, assignment) == clue.k


def _evaluate_at_least(clue: Clue, assignment: Assignment) -> bool:
    return _assignment_count(clue.region, assignment) >= clue.k


def _evaluate_at_most(clue: Clue, assignment: Assignment) -> bool:
    return _assignment_count(clue.region, assignment) <= clue.k
