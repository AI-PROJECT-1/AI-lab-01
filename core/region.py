"""Structured region contracts; resolution is implemented once in Phase 05."""

from __future__ import annotations

from dataclasses import dataclass

from core.character import validate_cell_id
from core.enums import RegionType


@dataclass(frozen=True, slots=True)
class Region:
    kind: RegionType
    index: int | None = None
    center: str | None = None
    cells: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "cells", tuple(self.cells))
        if self.kind in (RegionType.ROW, RegionType.COLUMN):
            if isinstance(self.index, bool) or not isinstance(self.index, int) or self.index < 1:
                raise ValueError("row/column region index must be a positive integer")
            if self.center is not None or self.cells:
                raise ValueError("row/column regions may only define index")
        elif self.kind is RegionType.NEIGHBORS:
            if self.center is None:
                raise ValueError("neighbor region requires center")
            validate_cell_id(self.center)
            if self.index is not None or self.cells:
                raise ValueError("neighbor regions may only define center")
        elif self.kind is RegionType.EXPLICIT:
            if not self.cells:
                raise ValueError("explicit region requires at least one cell")
            for cell_id in self.cells:
                validate_cell_id(cell_id)
            if len(self.cells) != len(set(self.cells)):
                raise ValueError("explicit region cell identifiers must be distinct")
            if self.index is not None or self.center is not None:
                raise ValueError("explicit regions may only define cells")
        else:
            raise ValueError(f"unsupported region kind: {self.kind!r}")

    def describe(self) -> str:
        if self.kind is RegionType.ROW:
            return f"row {self.index}"
        if self.kind is RegionType.COLUMN:
            return f"column {self.index}"
        if self.kind is RegionType.NEIGHBORS:
            return f"neighbors of {self.center}"
        return ", ".join(self.cells)
