"""Tkinter grid renderer for public card state."""

from __future__ import annotations

import tkinter as tk
from collections.abc import Callable
from tkinter import ttk

from core.character import column_label
from core.public_state import PublicKnowledgeState
from gui.view_model import build_card_views


class BoardView(ttk.LabelFrame):
    def __init__(self, parent: tk.Misc, on_select: Callable[[str], None]) -> None:
        super().__init__(parent, text="Board", padding=8)
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

        ttk.Label(self, text="").grid(row=0, column=0, padx=3, pady=3)
        for column in range(1, state.size + 1):
            ttk.Label(self, text=column_label(column), anchor="center").grid(
                row=0, column=column, sticky="ew", padx=3, pady=3
            )
            self.columnconfigure(column, weight=1, uniform="board")

        for row in range(1, state.size + 1):
            ttk.Label(self, text=str(row), anchor="center").grid(
                row=row, column=0, sticky="ns", padx=3, pady=3
            )
            self.rowconfigure(row, weight=1, uniform="board")

        for card in build_card_views(state):
            background = "#d8f3dc" if card.face_up else "#e9ecef"
            if card.status is not None:
                background = "#f8d7da" if card.status.value == "CRIMINAL" else "#dbeafe"
            if card.character_id in highlighted_ids:
                background = "#fff3a3"
            relief = tk.SUNKEN if card.character_id == selected_id else tk.RAISED
            button = tk.Button(
                self,
                text=card.button_text,
                command=lambda item=card.character_id: self._select(item),
                justify="center",
                wraplength=150,
                width=18,
                height=7,
                background=background,
                relief=relief,
                borderwidth=3 if card.character_id == selected_id else 1,
            )
            button.grid(
                row=card.row,
                column=card.column,
                sticky="nsew",
                padx=3,
                pady=3,
            )
            self._buttons[card.character_id] = button

    def _select(self, character_id: str) -> None:
        self._selected_id = character_id
        for current_id, button in self._buttons.items():
            selected = current_id == character_id
            button.configure(relief=tk.SUNKEN if selected else tk.RAISED, borderwidth=3 if selected else 1)
        self._on_select(character_id)
