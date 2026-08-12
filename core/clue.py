"""Validated structured clues independent of CNF representation."""

from __future__ import annotations

from dataclasses import dataclass

from core.character import validate_cell_id
from core.enums import ClueType, Status
from core.region import Region


@dataclass(frozen=True, slots=True)
class Clue:
    id: str
    type: ClueType
    target: str | None = None
    status: Status | None = None
    characters: tuple[str, ...] = ()
    region: Region | None = None
    k: int | None = None
    text: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.id, str) or not self.id.strip():
            raise ValueError("clue id must be non-empty")
        object.__setattr__(self, "characters", tuple(self.characters))
        if self.text is not None and (not isinstance(self.text, str) or not self.text.strip()):
            raise ValueError("clue text must be non-empty when supplied")

        if self.type is ClueType.FACT:
            if self.target is None or self.status is None:
                raise ValueError("FACT requires target and status")
            validate_cell_id(self.target)
            if self.characters or self.region is not None or self.k is not None:
                raise ValueError("FACT may only define target and status")
        elif self.type in (ClueType.SAME, ClueType.DIFFERENT, ClueType.IMPLIES):
            if len(self.characters) != 2 or len(set(self.characters)) != 2:
                raise ValueError("SAME/DIFFERENT/IMPLIES require two distinct character ids")
            for character_id in self.characters:
                validate_cell_id(character_id)
            if self.target is not None or self.status is not None or self.region is not None or self.k is not None:
                raise ValueError("binary clues may only define characters")
        elif self.type in (ClueType.EXACTLY, ClueType.AT_LEAST, ClueType.AT_MOST):
            if self.region is None:
                raise ValueError("counting clue requires region")
            if isinstance(self.k, bool) or not isinstance(self.k, int) or self.k < 0:
                raise ValueError("counting clue k must be a non-negative integer")
            if self.target is not None or self.status is not None or self.characters:
                raise ValueError("counting clues may only define region and k")
        elif self.type is ClueType.ODD:
            if self.region is None:
                raise ValueError("ODD requires a region")
            if self.target is not None or self.status is not None or self.characters or self.k is not None:
                raise ValueError("ODD may only define a region")
        else:
            raise ValueError(f"unsupported clue type: {self.type!r}")

    def display_text(self) -> str:
        if self.text:
            return self.text
        if self.type is ClueType.FACT:
            return f"{self.target} is {self.status.value.lower()}."
        if self.type is ClueType.SAME:
            return f"{self.characters[0]} and {self.characters[1]} have the same status."
        if self.type is ClueType.DIFFERENT:
            return f"{self.characters[0]} and {self.characters[1]} have different statuses."
        if self.type is ClueType.IMPLIES:
            return f"If {self.characters[0]} is criminal, then {self.characters[1]} is criminal."
        if self.type is ClueType.ODD:
            return f"An odd number of criminals are in {self.region.describe()}."
        phrase = {
            ClueType.EXACTLY: "Exactly",
            ClueType.AT_LEAST: "At least",
            ClueType.AT_MOST: "At most",
        }[self.type]
        return f"{phrase} {self.k} criminals in {self.region.describe()}."
