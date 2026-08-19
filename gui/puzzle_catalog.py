"""Public presentation metadata for local shipped puzzles."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


PUZZLE_DIR = Path(__file__).parents[1] / "puzzles"


@dataclass(frozen=True, slots=True)
class PuzzleCatalogEntry:
    puzzle_id: str
    name: str
    size: int
    difficulty: str
    description: str


PUZZLE_CATALOG = (
    PuzzleCatalogEntry(
        "standard-deduction-3x3",
        "The Atrium Ledger",
        3,
        "Standard",
        "Relationships with row and column counting.",
    ),
    PuzzleCatalogEntry(
        "intermediate-cipher-3x3",
        "The Cipher Courtyard",
        3,
        "Intermediate",
        "A compact relay of relation clues with a three-cell count anchor.",
    ),
    PuzzleCatalogEntry(
        "advanced-deduction-4x4",
        "The Meridian Conspiracy",
        4,
        "Advanced",
        "Regions, parity, conditional clues, and public verdicts.",
    ),
    PuzzleCatalogEntry(
        "advanced-lantern-4x4",
        "The Lantern Assembly",
        4,
        "Advanced",
        "A longer implication-and-relation chain grounded by a local count.",
    ),
    PuzzleCatalogEntry(
        "expert-orbit-5x5",
        "The Celestial Registry",
        5,
        "Expert",
        "A twenty-step case spanning row, column, neighborhood, implication, and parity logic.",
    ),
    PuzzleCatalogEntry(
        "expert-parity-5x5",
        "The Obsidian Concord",
        5,
        "Expert",
        "A distinct nineteen-step case with multi-cell opening deductions and non-linear reveals.",
    ),
)


_PUZZLE_FILES = {
    "standard-deduction-3x3": "standard_deduction_3x3.json",
    "intermediate-cipher-3x3": "intermediate_cipher_3x3.json",
    "advanced-deduction-4x4": "advanced_deduction_4x4.json",
    "advanced-lantern-4x4": "advanced_lantern_4x4.json",
    "expert-orbit-5x5": "expert_orbit_5x5.json",
    "expert-parity-5x5": "expert_parity_5x5.json",
}


def puzzle_path(puzzle_id: str) -> Path:
    try:
        filename = _PUZZLE_FILES[puzzle_id]
    except KeyError as exc:
        raise ValueError(f"unknown shipped puzzle id: {puzzle_id}") from exc
    return PUZZLE_DIR / filename


def catalog_entry(puzzle_id: str) -> PuzzleCatalogEntry | None:
    return next((entry for entry in PUZZLE_CATALOG if entry.puzzle_id == puzzle_id), None)
