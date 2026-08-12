"""Command result contracts shared by the engine and presentation layer."""

from __future__ import annotations

from dataclasses import dataclass

from core.clue import Clue
from core.enums import Status, VerdictOutcome


@dataclass(frozen=True, slots=True)
class VerdictResult:
    outcome: VerdictOutcome
    character_id: str
    requested_status: Status
    forced_status: Status | None = None
    revealed_clue: Clue | None = None
    message: str = ""
