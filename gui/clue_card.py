"""Reusable presentation for one publicly revealed clue."""

from __future__ import annotations

from dataclasses import dataclass
import tkinter as tk
from collections.abc import Callable

from core.public_state import PublicKnowledgeState
from gui.theme import COLORS, FONTS, SPACING


@dataclass(frozen=True, slots=True)
class ClueCardViewModel:
    owner_id: str
    owner_name: str
    owner_coordinate: str
    clue_id: str
    clue_text: str

    def visible_text(self) -> str:
        return "\n".join((self.owner_name, self.owner_coordinate, self.clue_id, self.clue_text))


@dataclass(frozen=True, slots=True)
class ClueCardModifiers:
    selected: bool = False
    newly_revealed: bool = False


@dataclass(frozen=True, slots=True)
class ClueCardAppearance:
    surface: str
    border: str
    selection_outline: str | None
    reveal_outline: str | None


def clue_appearance_for(modifiers: ClueCardModifiers) -> ClueCardAppearance:
    return ClueCardAppearance(
        surface=COLORS["clue_surface"],
        border=COLORS["clue_border"],
        selection_outline=COLORS["accent"] if modifiers.selected else None,
        reveal_outline=COLORS["focus"] if modifiers.newly_revealed else None,
    )


def build_clue_views(state: PublicKnowledgeState) -> tuple[ClueCardViewModel, ...]:
    """Build clue cards from public reveals only, preserving full display text."""

    characters = {character.id: character for character in state.characters}
    return tuple(
        ClueCardViewModel(
            owner_id=item.owner_id,
            owner_name=characters[item.owner_id].name,
            owner_coordinate=characters[item.owner_id].id,
            clue_id=item.clue.id,
            clue_text=item.clue.display_text(),
        )
        for item in state.revealed_clues
    )


class ClueCard(tk.Frame):
    """Selectable card that consumes only a public clue view model."""

    def __init__(
        self,
        parent: tk.Misc,
        clue: ClueCardViewModel,
        modifiers: ClueCardModifiers,
        on_select: Callable[[str], None],
        *,
        wraplength: int = 260,
    ) -> None:
        super().__init__(parent, borderwidth=0, highlightthickness=0, cursor="hand2")
        self.clue = clue
        self.modifiers = modifiers
        self._on_select = on_select

        self._reveal_frame = tk.Frame(self, borderwidth=0, highlightthickness=0)
        self._reveal_frame.pack(fill="both", expand=True)
        self._content = tk.Frame(self._reveal_frame, borderwidth=0, highlightthickness=0)
        self._content.pack(fill="both", expand=True)
        self._content.columnconfigure(0, weight=1)

        self._owner = tk.Label(
            self._content,
            text=f"{clue.owner_name}  ·  {clue.owner_coordinate}",
            anchor="w",
            font=FONTS["section"],
        )
        self._owner.grid(row=0, column=0, sticky="ew")
        self._id = tk.Label(
            self._content,
            text=clue.clue_id,
            anchor="e",
            font=FONTS["small"],
        )
        self._id.grid(row=0, column=1, sticky="e", padx=(SPACING["sm"], 0))
        self._text = tk.Label(
            self._content,
            text=f"“{clue.clue_text}”",
            anchor="w",
            justify="left",
            wraplength=wraplength,
            font=("Segoe UI", 9, "italic"),
        )
        self._text.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(SPACING["xs"], 0))

        self._apply_appearance()
        self._bind_click_tree(self)

    @property
    def appearance(self) -> ClueCardAppearance:
        return clue_appearance_for(self.modifiers)

    def set_wraplength(self, width: int) -> None:
        self._text.configure(wraplength=max(180, width))

    def _apply_appearance(self) -> None:
        appearance = self.appearance
        self.configure(
            background=appearance.selection_outline or COLORS["surface"],
            padx=3 if appearance.selection_outline else 1,
            pady=3 if appearance.selection_outline else 1,
        )
        self._reveal_frame.configure(
            background=appearance.reveal_outline or appearance.border,
            padx=2 if appearance.reveal_outline else 1,
            pady=2 if appearance.reveal_outline else 1,
        )
        self._content.configure(background=appearance.surface, padx=SPACING["sm"], pady=SPACING["sm"])
        self._owner.configure(background=appearance.surface, foreground=COLORS["ink"])
        self._id.configure(background=appearance.surface, foreground=COLORS["muted"])
        self._text.configure(background=appearance.surface, foreground=COLORS["ink"])

    def _bind_click_tree(self, widget: tk.Misc) -> None:
        widget.bind("<Button-1>", self._selected)
        for child in widget.winfo_children():
            self._bind_click_tree(child)

    def _selected(self, _event: tk.Event | None = None) -> None:
        self._on_select(self.clue.owner_id)
