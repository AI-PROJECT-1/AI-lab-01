"""Authoritative puzzle aggregate containing hidden card data."""

from __future__ import annotations

from dataclasses import dataclass

from core.character import Character, cell_id_for
from core.clue import Clue
from core.enums import ClueType, RegionType, Status


@dataclass(frozen=True, slots=True)
class PuzzleCard:
    """One complete card; this object must never cross the public boundary."""

    character: Character
    hidden_status: Status
    clue: Clue
    initially_revealed: bool = False


@dataclass(frozen=True, slots=True)
class Puzzle:
    id: str
    title: str
    size: int
    cards: tuple[PuzzleCard, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "cards", tuple(self.cards))
        if not isinstance(self.id, str) or not self.id.strip():
            raise ValueError("puzzle id must be non-empty")
        if not isinstance(self.title, str) or not self.title.strip():
            raise ValueError("puzzle title must be non-empty")
        if isinstance(self.size, bool) or not isinstance(self.size, int) or self.size < 1:
            raise ValueError("puzzle size must be a positive integer")
        if len(self.cards) != self.size * self.size:
            raise ValueError("puzzle must contain exactly size squared cards")

        ids = [card.character.id for card in self.cards]
        if len(ids) != len(set(ids)):
            raise ValueError("character ids must be unique")
        expected_ids = {
            cell_id_for(row, column)
            for row in range(1, self.size + 1)
            for column in range(1, self.size + 1)
        }
        if set(ids) != expected_ids:
            raise ValueError("cards must cover every grid cell exactly once")
        names = [card.character.name.casefold() for card in self.cards]
        if len(names) != len(set(names)):
            raise ValueError("character names must be unique")
        clue_ids = [card.clue.id for card in self.cards]
        if len(clue_ids) != len(set(clue_ids)):
            raise ValueError("clue ids must be unique")
        if not any(card.initially_revealed for card in self.cards):
            raise ValueError("playable puzzle requires at least one initially revealed card")

        for card in self.cards:
            self._validate_clue_references(card.clue, expected_ids)

    def _validate_clue_references(self, clue: Clue, valid_ids: set[str]) -> None:
        if clue.type is ClueType.FACT and clue.target not in valid_ids:
            raise ValueError(f"clue {clue.id} references unknown target {clue.target}")
        if clue.type in (ClueType.SAME, ClueType.DIFFERENT, ClueType.IMPLIES):
            unknown = set(clue.characters) - valid_ids
            if unknown:
                raise ValueError(f"clue {clue.id} references unknown characters: {sorted(unknown)}")
        if clue.region is None:
            return
        region = clue.region
        region_size: int
        if region.kind in (RegionType.ROW, RegionType.COLUMN):
            if region.index > self.size:
                raise ValueError(f"clue {clue.id} region index is outside the board")
            region_size = self.size
        elif region.kind is RegionType.NEIGHBORS:
            if region.center not in valid_ids:
                raise ValueError(f"clue {clue.id} neighbor center is outside the board")
            center = self.character_by_id(region.center)
            region_size = sum(
                1
                for row in range(max(1, center.row - 1), min(self.size, center.row + 1) + 1)
                for column in range(max(1, center.column - 1), min(self.size, center.column + 1) + 1)
                if (row, column) != (center.row, center.column)
            )
        else:
            unknown = set(region.cells) - valid_ids
            if unknown:
                raise ValueError(f"clue {clue.id} explicit region has unknown cells: {sorted(unknown)}")
            region_size = len(region.cells)
        if clue.k is not None and clue.k > region_size:
            raise ValueError(f"clue {clue.id} has k greater than its region size")

    def character_by_id(self, character_id: str) -> Character:
        for card in self.cards:
            if card.character.id == character_id:
                return card.character
        raise KeyError(character_id)

    def card_by_id(self, character_id: str) -> PuzzleCard:
        for card in self.cards:
            if card.character.id == character_id:
                return card
        raise KeyError(character_id)

    @property
    def ordered_cards(self) -> tuple[PuzzleCard, ...]:
        return tuple(sorted(self.cards, key=lambda card: (card.character.row, card.character.column)))

    @property
    def initially_revealed_ids(self) -> tuple[str, ...]:
        return tuple(card.character.id for card in self.ordered_cards if card.initially_revealed)
