"""Pure public-state-to-view transformations used by the Tkinter layer."""

from __future__ import annotations

from dataclasses import dataclass

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
    def button_text(self) -> str:
        face = "FACE-UP" if self.face_up else "FACE-DOWN"
        status = self.status.value if self.status else "UNKNOWN"
        clue = f"Clue: {self.clue_id}" if self.clue_id else "Clue: hidden"
        return "\n".join((self.coordinate, self.name, self.profession, status, face, clue))


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
