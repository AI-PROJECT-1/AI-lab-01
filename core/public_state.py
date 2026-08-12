"""Immutable DTOs that are safe to expose to agents and the GUI."""

from __future__ import annotations

from dataclasses import dataclass

from core.character import Character
from core.clue import Clue
from core.enums import Status


@dataclass(frozen=True, slots=True)
class KnownVerdict:
    character_id: str
    status: Status


@dataclass(frozen=True, slots=True)
class RevealedClue:
    owner_id: str
    clue: Clue


@dataclass(frozen=True, slots=True)
class PublicKnowledgeState:
    """Everything an agent may know, and nothing more."""

    puzzle_id: str
    title: str
    size: int
    characters: tuple[Character, ...]
    revealed_clues: tuple[RevealedClue, ...]
    known_verdicts: tuple[KnownVerdict, ...]
    is_complete: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "characters", tuple(self.characters))
        object.__setattr__(self, "revealed_clues", tuple(self.revealed_clues))
        object.__setattr__(self, "known_verdicts", tuple(self.known_verdicts))
        ids = [character.id for character in self.characters]
        if len(ids) != len(set(ids)):
            raise ValueError("public character ids must be unique")
        known_ids = [verdict.character_id for verdict in self.known_verdicts]
        if len(known_ids) != len(set(known_ids)):
            raise ValueError("known verdicts must be unique by character")
        if not set(known_ids).issubset(ids):
            raise ValueError("known verdicts must reference public characters")
        owner_ids = [item.owner_id for item in self.revealed_clues]
        if len(owner_ids) != len(set(owner_ids)):
            raise ValueError("only one revealed clue is allowed per owner")
        if not set(owner_ids).issubset(ids):
            raise ValueError("revealed clues must reference public characters")

    def status_of(self, character_id: str) -> Status | None:
        for verdict in self.known_verdicts:
            if verdict.character_id == character_id:
                return verdict.status
        return None

    def clue_for(self, owner_id: str) -> Clue | None:
        for revealed in self.revealed_clues:
            if revealed.owner_id == owner_id:
                return revealed.clue
        return None
