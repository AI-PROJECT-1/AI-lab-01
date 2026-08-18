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
        "sample-3x3-fact-chain",
        "The Gallery Shift",
        3,
        "Tutorial",
        "Learn verdicts, reveals, and clue inspection through a direct chain.",
    ),
    PuzzleCatalogEntry(
        "standard-deduction-3x3",
        "The Atrium Ledger",
        3,
        "Standard",
        "Combine row counts and relationships; no deduction is a direct FACT step.",
    ),
    PuzzleCatalogEntry(
        "advanced-deduction-4x4",
        "The Meridian Conspiracy",
        4,
        "Advanced",
        "Layer regions, counting, implications, parity, and public verdicts.",
    ),
    PuzzleCatalogEntry(
        "extension-chain-3x3",
        "The Parity Gallery",
        3,
        "Standard",
        "A compact introduction to IMPLIES and ODD clues.",
    ),
    PuzzleCatalogEntry(
        "extension-chain-4x4",
        "The Implication Archive",
        4,
        "Standard",
        "Begin with extensions, then practice a longer reveal chain.",
    ),
    PuzzleCatalogEntry(
        "fact-chain-4x4",
        "The Museum Circuit",
        4,
        "Tutorial",
        "Practice the interface on a larger board with direct clues.",
    ),
)


_PUZZLE_FILES = {
    "sample-3x3-fact-chain": "sample_3x3.json",
    "standard-deduction-3x3": "standard_deduction_3x3.json",
    "advanced-deduction-4x4": "advanced_deduction_4x4.json",
    "extension-chain-3x3": "extension_chain_3x3.json",
    "extension-chain-4x4": "extension_chain_4x4.json",
    "fact-chain-4x4": "fact_chain_4x4.json",
}


def puzzle_path(puzzle_id: str) -> Path:
    try:
        filename = _PUZZLE_FILES[puzzle_id]
    except KeyError as exc:
        raise ValueError(f"unknown shipped puzzle id: {puzzle_id}") from exc
    return PUZZLE_DIR / filename


def catalog_entry(puzzle_id: str) -> PuzzleCatalogEntry | None:
    return next((entry for entry in PUZZLE_CATALOG if entry.puzzle_id == puzzle_id), None)
