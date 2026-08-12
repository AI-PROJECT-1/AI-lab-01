"""Selectable list of currently revealed clues."""

from __future__ import annotations

import tkinter as tk
from collections.abc import Callable
from tkinter import ttk

from core.public_state import PublicKnowledgeState
from gui.theme import COLORS, FONTS, SPACING


class CluePanel(ttk.LabelFrame):
    def __init__(self, parent: tk.Misc, on_select: Callable[[str], None]) -> None:
        super().__init__(parent, text="REVEALED CLUES", style="Panel.TLabelframe", padding=SPACING["md"])
        self._on_select = on_select
        self._owner_ids: list[str] = []
        self._listbox = tk.Listbox(
            self,
            height=12,
            exportselection=False,
            background=COLORS["surface"],
            foreground=COLORS["ink"],
            selectbackground=COLORS["accent_soft"],
            selectforeground=COLORS["ink"],
            borderwidth=0,
            highlightthickness=0,
            font=FONTS["body"],
            activestyle="none",
        )
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self._listbox.yview)
        self._listbox.configure(yscrollcommand=scrollbar.set)
        self._listbox.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self._listbox.bind("<<ListboxSelect>>", self._selected)

    def render(self, state: PublicKnowledgeState) -> None:
        self._listbox.delete(0, tk.END)
        self._owner_ids.clear()
        for item in state.revealed_clues:
            self._owner_ids.append(item.owner_id)
            self._listbox.insert(
                tk.END,
                f"{item.clue.id} ({item.owner_id}): {item.clue.display_text()}",
            )

    def _selected(self, _event: tk.Event) -> None:
        selection = self._listbox.curselection()
        if selection:
            self._on_select(self._owner_ids[selection[0]])
