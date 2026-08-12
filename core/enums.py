"""Enumerations shared by the domain, game, logic, and GUI layers."""

from __future__ import annotations

from enum import StrEnum


class Status(StrEnum):
    """A character's binary status."""

    CRIMINAL = "CRIMINAL"
    INNOCENT = "INNOCENT"

    @property
    def opposite(self) -> "Status":
        return Status.INNOCENT if self is Status.CRIMINAL else Status.CRIMINAL


class ClueType(StrEnum):
    FACT = "FACT"
    SAME = "SAME"
    DIFFERENT = "DIFFERENT"
    EXACTLY = "EXACTLY"
    AT_LEAST = "AT_LEAST"
    AT_MOST = "AT_MOST"
    IMPLIES = "IMPLIES"
    ODD = "ODD"


class RegionType(StrEnum):
    ROW = "ROW"
    COLUMN = "COLUMN"
    NEIGHBORS = "NEIGHBORS"
    EXPLICIT = "EXPLICIT"


class Classification(StrEnum):
    CRIMINAL = "CRIMINAL"
    INNOCENT = "INNOCENT"
    UNKNOWN = "UNKNOWN"
    INCONSISTENT = "INCONSISTENT"

    @classmethod
    def from_status(cls, status: Status) -> "Classification":
        return cls(status.value)

    def as_status(self) -> Status | None:
        if self in (Classification.CRIMINAL, Classification.INNOCENT):
            return Status(self.value)
        return None


class VerdictOutcome(StrEnum):
    ACCEPTED = "ACCEPTED"
    NOT_PROVABLE = "NOT_PROVABLE"
    CONTRADICTED = "CONTRADICTED"
    INCONSISTENT = "INCONSISTENT"
