"""Character metadata and canonical grid coordinates."""

from __future__ import annotations

import re
from dataclasses import dataclass


CELL_ID_PATTERN = re.compile(r"^[A-Z]+[1-9][0-9]*$")


def column_label(column: int) -> str:
    """Convert a one-based column number to spreadsheet-style letters."""
    if isinstance(column, bool) or not isinstance(column, int) or column < 1:
        raise ValueError("column must be a positive integer")
    label = ""
    current = column
    while current:
        current, remainder = divmod(current - 1, 26)
        label = chr(ord("A") + remainder) + label
    return label


def cell_id_for(row: int, column: int) -> str:
    if isinstance(row, bool) or not isinstance(row, int) or row < 1:
        raise ValueError("row must be a positive integer")
    return f"{column_label(column)}{row}"


def validate_cell_id(cell_id: str) -> None:
    if not isinstance(cell_id, str) or not CELL_ID_PATTERN.fullmatch(cell_id):
        raise ValueError("cell_id must use uppercase column letters and a positive row, e.g. A1")


@dataclass(frozen=True, slots=True)
class Character:
    """Public metadata for the character occupying one grid cell."""

    id: str
    name: str
    profession: str
    row: int
    column: int

    def __post_init__(self) -> None:
        validate_cell_id(self.id)
        if self.id != cell_id_for(self.row, self.column):
            raise ValueError("character id must match its row and column")
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("character name must be non-empty")
        if not isinstance(self.profession, str) or not self.profession.strip():
            raise ValueError("character profession must be non-empty")
