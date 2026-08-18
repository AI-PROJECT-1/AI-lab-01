"""Pure public-state-to-view transformations used by the Tkinter layer."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from core.character import column_label
from core.enums import Status
from core.public_state import PublicKnowledgeState


@dataclass(frozen=True, slots=True)
class CardViewModel:
    character_id: str
    row: int
    column: int
    name: str
    profession: str
    status: Status | None
    face_up: bool
    clue_id: str | None
    clue_text: str | None

    @property
    def coordinate(self) -> str:
        return f"{column_label(self.column)}{self.row}"

    @property
    def initials(self) -> str:
        words = tuple(part for part in self.name.split() if part)
        if len(words) >= 2:
            return f"{words[0][0]}{words[-1][0]}".upper()
        return self.name[:2].upper()

    @property
    def base_state(self) -> "CardBaseState":
        if self.status is Status.CRIMINAL:
            return CardBaseState.CRIMINAL
        if self.status is Status.INNOCENT:
            return CardBaseState.INNOCENT
        return CardBaseState.UNRESOLVED

    def clue_preview(self, max_length: int) -> str | None:
        if self.clue_text is None:
            return None
        normalized = " ".join(self.clue_text.split())
        if len(normalized) <= max_length:
            return normalized
        shortened = normalized[: max_length - 1].rsplit(" ", 1)[0]
        return f"{shortened or normalized[: max_length - 1]}…"

    def visible_text(self, max_clue_length: int = 84) -> str:
        """Return only text that is safe to present from this public view model."""

        parts = [self.coordinate, self.initials, self.name, self.profession]
        if self.status is not None:
            parts.append(self.status.value)
        preview = self.clue_preview(max_clue_length)
        if preview is not None:
            parts.append(preview)
        return "\n".join(parts)


class CardBaseState(StrEnum):
    UNRESOLVED = "UNRESOLVED"
    CRIMINAL = "CRIMINAL"
    INNOCENT = "INNOCENT"


@dataclass(frozen=True, slots=True)
class CardModifiers:
    selected: bool = False
    clue_highlighted: bool = False
    newly_revealed: bool = False
    hint_target: bool = False
    hint_support: bool = False
    manual_locked: bool = False


@dataclass(frozen=True, slots=True)
class CardVisualState:
    base: CardBaseState
    modifiers: CardModifiers = CardModifiers()


def compose_card_visual_state(
    card: CardViewModel,
    *,
    selected: bool = False,
    clue_highlighted: bool = False,
    newly_revealed: bool = False,
    hint_target: bool = False,
    hint_support: bool = False,
    manual_locked: bool = False,
) -> CardVisualState:
    return CardVisualState(
        card.base_state,
        CardModifiers(selected, clue_highlighted, newly_revealed, hint_target, hint_support, manual_locked),
    )


def build_card_views(state: PublicKnowledgeState) -> tuple[CardViewModel, ...]:
    """Build deterministic row-major card models without hidden data access."""
    views: list[CardViewModel] = []
    for character in sorted(state.characters, key=lambda item: (item.row, item.column)):
        clue = state.clue_for(character.id)
        status = state.status_of(character.id)
        views.append(
            CardViewModel(
                character_id=character.id,
                row=character.row,
                column=character.column,
                name=character.name,
                profession=character.profession,
                status=status,
                face_up=clue is not None,
                clue_id=clue.id if clue else None,
                clue_text=clue.display_text() if clue else None,
            )
        )
    return tuple(views)
