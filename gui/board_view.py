"""Tkinter grid renderer for public card state."""

from __future__ import annotations

from collections.abc import Callable
import tkinter as tk
from tkinter import ttk

from core.character import column_label
from core.public_state import PublicKnowledgeState
from gui.view_model import build_card_views
from gui.theme import SPACING
from gui.character_card import CharacterCard
from gui.view_model import compose_card_visual_state


class BoardView(ttk.LabelFrame):
    def __init__(self, parent: tk.Misc, on_select: Callable[[str], None]) -> None:
        super().__init__(parent, text="BOARD", style="Panel.TLabelframe", padding=SPACING["sm"])
        self._on_select = on_select
        self._buttons: dict[str, CharacterCard] = {}
        self._selected_id: str | None = None

    def render(
        self,
        state: PublicKnowledgeState,
        selected_id: str | None = None,
        highlighted_ids: tuple[str, ...] = (),
        newly_revealed_id: str | None = None,
    ) -> None:
        for child in self.winfo_children():
            child.destroy()
        self._buttons.clear()
        self._selected_id = selected_id

        ttk.Label(self, text="", style="Muted.TLabel").grid(row=0, column=0, padx=SPACING["xs"], pady=SPACING["xs"])
        for column in range(1, state.size + 1):
            ttk.Label(self, text=column_label(column), anchor="center", style="Muted.TLabel").grid(
                row=0, column=column, sticky="ew", padx=SPACING["xs"], pady=SPACING["xs"]
            )
            self.columnconfigure(column, weight=1, uniform="board")

        for row in range(1, state.size + 1):
            ttk.Label(self, text=str(row), anchor="center", style="Muted.TLabel").grid(
                row=row, column=0, sticky="ns", padx=SPACING["xs"], pady=SPACING["xs"]
            )
            self.rowconfigure(row, weight=1, uniform="board")

        compact = state.size >= 4
        for card in build_card_views(state):
            visual_state = compose_card_visual_state(
                card,
                selected=card.character_id == selected_id,
                clue_highlighted=card.character_id in highlighted_ids,
                newly_revealed=card.character_id == newly_revealed_id,
            )
            widget = CharacterCard(
                self,
                card,
                visual_state,
                self._select,
                compact=compact,
            )
            widget.grid(
                row=card.row,
                column=card.column,
                sticky="nsew",
                padx=SPACING["xs"],
                pady=2,
            )
            self._buttons[card.character_id] = widget

    def _select(self, character_id: str) -> None:
        self._selected_id = character_id
        for current_id, card in self._buttons.items():
            selected = current_id == character_id
            card.set_modifiers(
                selected=selected,
                clue_highlighted=card.visual_state.modifiers.clue_highlighted,
                newly_revealed=card.visual_state.modifiers.newly_revealed,
            )
        self._on_select(character_id)
