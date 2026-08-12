"""Reusable, public-only character card presentation."""

from __future__ import annotations

import tkinter as tk
from dataclasses import dataclass

from gui.theme import COLORS, FONTS, SPACING
from gui.view_model import (
    CardBaseState,
    CardModifiers,
    CardViewModel,
    CardVisualState,
)


@dataclass(frozen=True, slots=True)
class CardAppearance:
    surface: str
    base_border: str
    badge_background: str | None
    badge_foreground: str | None
    selection_outline: str | None
    highlight_outline: str | None
    reveal_outline: str | None
    hint_outline: str | None


def appearance_for(state: CardVisualState) -> CardAppearance:
    """Compose base identity with independent modifier outlines."""

    if state.base is CardBaseState.CRIMINAL:
        surface = COLORS["card_criminal"]
        base_border = COLORS["card_criminal_border"]
        badge_background = COLORS["danger"]
        badge_foreground = "#FFFFFF"
    elif state.base is CardBaseState.INNOCENT:
        surface = COLORS["card_innocent"]
        base_border = COLORS["card_innocent_border"]
        badge_background = COLORS["success"]
        badge_foreground = "#FFFFFF"
    else:
        surface = COLORS["card_unresolved"]
        base_border = COLORS["card_unresolved_border"]
        badge_background = None
        badge_foreground = None

    modifiers = state.modifiers
    return CardAppearance(
        surface=surface,
        base_border=base_border,
        badge_background=badge_background,
        badge_foreground=badge_foreground,
        selection_outline=COLORS["accent"] if modifiers.selected else None,
        highlight_outline=COLORS["focus"] if modifiers.clue_highlighted else None,
        reveal_outline=COLORS["info"] if modifiers.newly_revealed else None,
        hint_outline=COLORS["hint"] if modifiers.hint_target else None,
    )


def avatar_color_for(character_id: str) -> str:
    palette = (
        COLORS["avatar_1"],
        COLORS["avatar_2"],
        COLORS["avatar_3"],
        COLORS["avatar_4"],
    )
    stable_index = sum((index + 1) * ord(character) for index, character in enumerate(character_id))
    return palette[stable_index % len(palette)]


class CharacterCard(tk.Frame):
    """Game-style card whose contents are exclusively a CardViewModel."""

    def __init__(
        self,
        parent: tk.Misc,
        card: CardViewModel,
        visual_state: CardVisualState,
        on_select,
        *,
        compact: bool,
    ) -> None:
        super().__init__(parent, borderwidth=0, highlightthickness=0, cursor="hand2")
        self.card = card
        self.visual_state = visual_state
        self._on_select = on_select
        self._compact = compact

        self._outline = tk.Frame(self, borderwidth=0, highlightthickness=0)
        self._outline.pack(fill="both", expand=True)
        self._hint_outline = tk.Frame(self._outline, borderwidth=0, highlightthickness=0)
        self._hint_outline.pack(fill="both", expand=True)
        self._reveal_outline = tk.Frame(self._hint_outline, borderwidth=0, highlightthickness=0)
        self._reveal_outline.pack(fill="both", expand=True)
        self._content = tk.Frame(self._reveal_outline, borderwidth=0, highlightthickness=0)
        self._content.pack(fill="both", expand=True)
        self._content.columnconfigure(0, weight=1)
        self._content.columnconfigure(1, weight=1)

        self._header = tk.Frame(self._content, borderwidth=0, highlightthickness=0)
        self._header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=SPACING["xs"])
        self._header.columnconfigure(1, weight=1)

        self._coordinate = tk.Label(
            self._header,
            text=card.coordinate,
            anchor="e",
            font=("Segoe UI", 7) if compact else FONTS["small"],
        )
        self._coordinate.grid(row=0, column=2, sticky="e")

        avatar_size = 2 if compact else 3
        self._avatar = tk.Label(
            self._header,
            text=card.initials,
            font=("Segoe UI Semibold", 8 if compact else 13),
            foreground="#FFFFFF",
            background=avatar_color_for(card.character_id),
            width=avatar_size,
            height=1,
            relief="flat",
        )
        self._avatar.grid(
            row=0,
            column=0,
            rowspan=1 if compact else 2,
            sticky="w",
            padx=(0, SPACING["xs"]),
        )

        self._identity = tk.Frame(self._header, borderwidth=0, highlightthickness=0)
        self._identity.grid(row=0, column=1, rowspan=2, sticky="ew")
        self._identity.columnconfigure(0, weight=1)

        self._name = tk.Label(
            self._identity,
            text=card.name,
            font=("Segoe UI Semibold", 8 if compact else 10),
            anchor="w",
        )
        self._name.grid(row=0, column=0, sticky="w" if compact else "ew")

        self._profession = tk.Label(
            self._identity,
            text=card.profession,
            font=("Segoe UI", 7 if compact else 8),
            anchor="w",
        )
        if compact:
            self._profession.grid(row=0, column=1, sticky="w", padx=(SPACING["xs"], 0))
        else:
            self._profession.grid(row=1, column=0, sticky="ew")

        self._badge: tk.Label | None = None
        if card.status is not None:
            badge_symbol = "!" if card.status.value == "CRIMINAL" else "✓"
            badge_gap = " " if compact else "  "
            self._badge = tk.Label(
                self._content,
                text=f"{badge_symbol}{badge_gap}{card.status.value}",
                font=("Segoe UI Semibold", 7 if compact else 8),
                padx=0 if compact else SPACING["sm"],
                pady=1,
            )
            self._badge.grid(row=1, column=0, sticky="e", padx=(SPACING["xs"], 2))

        self._clue: tk.Label | None = None
        preview = card.clue_preview(16 if compact else 20)
        if preview is not None:
            self._clue = tk.Label(
                self._content,
                text=preview if compact else f"“{preview}”",
                font=("Segoe UI", 6 if compact else 8, "italic"),
                justify="left",
            )
            self._clue.grid(row=1, column=1, sticky="w", padx=(2, SPACING["xs"]))

        self._apply_appearance()
        self._bind_click_tree(self)

    @property
    def appearance(self) -> CardAppearance:
        return appearance_for(self.visual_state)

    def set_modifiers(
        self,
        *,
        selected: bool,
        clue_highlighted: bool,
        newly_revealed: bool = False,
        hint_target: bool = False,
    ) -> None:
        self.visual_state = CardVisualState(
            self.visual_state.base,
            CardModifiers(selected, clue_highlighted, newly_revealed, hint_target),
        )
        self._apply_appearance()

    def _apply_appearance(self) -> None:
        appearance = self.appearance
        self.configure(
            background=appearance.selection_outline or COLORS["surface"],
            padx=2 if appearance.selection_outline else 0,
            pady=2 if appearance.selection_outline else 0,
        )
        self._outline.configure(
            background=appearance.highlight_outline or appearance.base_border,
            padx=2 if appearance.highlight_outline else 1,
            pady=2 if appearance.highlight_outline else 1,
        )
        self._hint_outline.configure(
            background=appearance.hint_outline or appearance.surface,
            padx=2 if appearance.hint_outline else 0,
            pady=2 if appearance.hint_outline else 0,
        )
        self._reveal_outline.configure(
            background=appearance.reveal_outline or appearance.surface,
            padx=1 if appearance.reveal_outline else 0,
            pady=1 if appearance.reveal_outline else 0,
        )
        self._content.configure(background=appearance.surface)
        self._header.configure(background=appearance.surface)
        self._identity.configure(background=appearance.surface)

        for label in (self._coordinate, self._name, self._profession, self._clue):
            if label is not None:
                label.configure(background=appearance.surface)
        self._coordinate.configure(foreground=COLORS["muted"])
        self._name.configure(foreground=COLORS["ink"])
        self._profession.configure(foreground=COLORS["muted"])
        if self._clue is not None:
            self._clue.configure(foreground=COLORS["ink"])
        if self._badge is not None:
            self._badge.configure(
                background=appearance.badge_background,
                foreground=appearance.badge_foreground,
            )

    def _bind_click_tree(self, widget: tk.Misc) -> None:
        widget.bind("<Button-1>", self._selected)
        for child in widget.winfo_children():
            self._bind_click_tree(child)

    def _selected(self, _event: tk.Event | None = None) -> None:
        self._on_select(self.card.character_id)
