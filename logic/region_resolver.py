"""Canonical resolution of structured regions to deterministic cell identifiers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from core.character import Character, parse_cell_id
from core.clue import Clue
from core.enums import ClueType, RegionType
from core.region import Region


@dataclass(frozen=True, slots=True)
class _CellCoordinate:
    id: str
    row: int
    column: int


class RegionResolver:
    """Resolve every core region through one shared implementation.

    Character objects are used by the encoder and GUI. A complete sequence of
    cell identifiers may be used by the independent semantic evaluator.
    """

    def __init__(self, cells: Sequence[Character | str]) -> None:
        normalized: list[_CellCoordinate] = []
        for cell in cells:
            if isinstance(cell, Character):
                normalized.append(_CellCoordinate(cell.id, cell.row, cell.column))
            elif isinstance(cell, str):
                row, column = parse_cell_id(cell)
                normalized.append(_CellCoordinate(cell, row, column))
            else:
                raise TypeError("region cells must be Character objects or cell identifiers")

        ids = [cell.id for cell in normalized]
        coordinates = [(cell.row, cell.column) for cell in normalized]
        if len(ids) != len(set(ids)):
            raise ValueError("region resolver cell identifiers must be unique")
        if len(coordinates) != len(set(coordinates)):
            raise ValueError("region resolver coordinates must be unique")

        self._cells = tuple(sorted(normalized, key=lambda cell: (cell.row, cell.column, cell.id)))
        self._cells_by_id = {cell.id: cell for cell in self._cells}

    def resolve(self, region: Region) -> tuple[str, ...]:
        if region.kind is RegionType.ROW:
            return self._require_non_empty(
                tuple(cell.id for cell in self._cells if cell.row == region.index),
                f"row {region.index} is outside the board",
            )
        if region.kind is RegionType.COLUMN:
            return self._require_non_empty(
                tuple(cell.id for cell in self._cells if cell.column == region.index),
                f"column {region.index} is outside the board",
            )
        if region.kind is RegionType.NEIGHBORS:
            return self._resolve_neighbors(region.center)
        if region.kind is RegionType.EXPLICIT:
            return self._resolve_explicit(region.cells)
        raise ValueError(f"unsupported region kind: {region.kind!r}")

    def _resolve_neighbors(self, center_id: str) -> tuple[str, ...]:
        try:
            center = self._cells_by_id[center_id]
        except KeyError as exc:
            raise ValueError(f"unknown neighbor center: {center_id}") from exc
        return tuple(
            cell.id
            for cell in self._cells
            if cell.id != center.id
            and abs(cell.row - center.row) <= 1
            and abs(cell.column - center.column) <= 1
        )

    def _resolve_explicit(self, cell_ids: tuple[str, ...]) -> tuple[str, ...]:
        if not cell_ids:
            raise ValueError("explicit region must contain at least one cell")
        if len(cell_ids) != len(set(cell_ids)):
            raise ValueError("explicit region cell identifiers must be distinct")
        for cell_id in cell_ids:
            if cell_id not in self._cells_by_id:
                raise ValueError(f"unknown explicit region cell: {cell_id}")
        return cell_ids

    @staticmethod
    def _require_non_empty(cell_ids: tuple[str, ...], message: str) -> tuple[str, ...]:
        if not cell_ids:
            raise ValueError(message)
        return cell_ids


def referenced_cells(clue: Clue, characters: Sequence[Character | str]) -> tuple[str, ...]:
    """Resolve every board cell directly referenced or counted by a clue."""

    resolver = RegionResolver(characters)
    if clue.type is ClueType.FACT:
        return resolver.resolve(Region(RegionType.EXPLICIT, cells=(clue.target,)))
    if clue.type in (ClueType.SAME, ClueType.DIFFERENT, ClueType.IMPLIES):
        return resolver.resolve(Region(RegionType.EXPLICIT, cells=clue.characters))
    return resolver.resolve(clue.region)
