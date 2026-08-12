"""Tkinter grid renderer for public card state."""

from __future__ import annotations

import tkinter as tk
from collections.abc import Callable
from tkinter import ttk

from core.character import column_label
from core.public_state import PublicKnowledgeState
from gui.view_model import build_card_views
from gui.theme import SPACING


class BoardView(ttk.LabelFrame):
    def __init__(self, parent: tk.Misc, on_select: Callable[[str], None]) -> None:
        super().__init__(parent, text="BOARD", style="Panel.TLabelframe", padding=SPACING["sm"])
        self._on_select = on_select
        self._buttons: dict[str, tk.Button] = {}
        self._selected_id: str | None = None

    def render(
        self,
        state: PublicKnowledgeState,
        selected_id: str | None = None,
        highlighted_ids: tuple[str, ...] = (),
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

        for card in build_card_views(state):
            background = "#d8f3dc" if card.face_up else "#e9ecef"
            if card.status is not None:
                background = "#f8d7da" if card.status.value == "CRIMINAL" else "#dbeafe"
            if card.character_id in highlighted_ids:
                background = "#fff3a3"
            relief = tk.SUNKEN if card.character_id == selected_id else tk.RAISED
            card_width = 14 if state.size >= 4 else 18
            card_font = ("Segoe UI", 8 if state.size >= 4 else 9)
            button = tk.Button(
                self,
                text=card.button_text,
                command=lambda item=card.character_id: self._select(item),
                justify="center",
                wraplength=125 if state.size >= 4 else 150,
                width=card_width,
                height=6,
                font=card_font,
                background=background,
                relief=relief,
                borderwidth=3 if card.character_id == selected_id else 1,
            )
            button.grid(
                row=card.row,
                column=card.column,
                sticky="nsew",
                padx=SPACING["xs"],
                pady=2,
            )
            self._buttons[card.character_id] = button

    def _select(self, character_id: str) -> None:
        self._selected_id = character_id
        for current_id, button in self._buttons.items():
            selected = current_id == character_id
            button.configure(relief=tk.SUNKEN if selected else tk.RAISED, borderwidth=3 if selected else 1)
        self._on_select(character_id)
