"""Scrollable cards for currently revealed public clues."""

from __future__ import annotations

import tkinter as tk
from collections.abc import Callable
from tkinter import ttk

from core.public_state import PublicKnowledgeState
from gui.clue_card import ClueCard, ClueCardModifiers, build_clue_views
from gui.theme import COLORS, SPACING


class CluePanel(ttk.LabelFrame):
    def __init__(self, parent: tk.Misc, on_select: Callable[[str], None]) -> None:
        super().__init__(parent, text="REVEALED CLUES", style="Panel.TLabelframe", padding=SPACING["sm"])
        self._on_select = on_select
        self._cards: dict[str, ClueCard] = {}

        self._canvas = tk.Canvas(
            self,
            background=COLORS["surface"],
            borderwidth=0,
            highlightthickness=0,
        )
        self._scrollbar = ttk.Scrollbar(self, orient="vertical", command=self._canvas.yview)
        self._canvas.configure(yscrollcommand=self._scrollbar.set)
        self._canvas.grid(row=0, column=0, sticky="nsew")
        self._scrollbar.grid(row=0, column=1, sticky="ns")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self._content = tk.Frame(self._canvas, background=COLORS["surface"])
        self._window = self._canvas.create_window((0, 0), window=self._content, anchor="nw")
        self._content.bind("<Configure>", self._update_scrollregion)
        self._canvas.bind("<Configure>", self._resize_content)
        self._canvas.bind("<MouseWheel>", self._mousewheel)

    def render(
        self,
        state: PublicKnowledgeState,
        selected_owner_id: str | None = None,
        newly_revealed_owner_id: str | None = None,
        hint_active_clue_ids: tuple[str, ...] = (),
    ) -> None:
        for child in self._content.winfo_children():
            child.destroy()
        self._cards.clear()

        clues = build_clue_views(state)
        if not clues:
            tk.Label(
                self._content,
                text="No public clues have been revealed yet.",
                background=COLORS["surface"],
                foreground=COLORS["muted"],
                anchor="center",
            ).grid(row=0, column=0, sticky="ew", padx=SPACING["md"], pady=SPACING["xl"])
        for row, clue in enumerate(clues):
            card = ClueCard(
                self._content,
                clue,
                ClueCardModifiers(
                    selected=clue.owner_id == selected_owner_id,
                    newly_revealed=clue.owner_id == newly_revealed_owner_id,
                    hint_active=clue.clue_id in hint_active_clue_ids,
                ),
                self._on_select,
            )
            card.grid(row=row, column=0, sticky="ew", pady=(0, SPACING["xs"]))
            self._bind_mousewheel_tree(card)
            self._cards[clue.owner_id] = card
        self._content.columnconfigure(0, weight=1)
        self._content.update_idletasks()
        self._update_scrollregion()
        self._update_card_wraplength(self._canvas.winfo_width())
        if newly_revealed_owner_id in self._cards:
            self.after_idle(lambda: self._scroll_to(newly_revealed_owner_id))

    def _update_scrollregion(self, _event: tk.Event | None = None) -> None:
        self._canvas.configure(scrollregion=self._canvas.bbox("all"))

    def _resize_content(self, event: tk.Event) -> None:
        self._canvas.itemconfigure(self._window, width=event.width)
        self._update_card_wraplength(event.width)

    def _update_card_wraplength(self, canvas_width: int) -> None:
        for card in self._cards.values():
            card.set_wraplength(canvas_width - 48)

    def _scroll_to(self, owner_id: str) -> None:
        card = self._cards.get(owner_id)
        if card is None:
            return
        self._content.update_idletasks()
        overflow = self._content.winfo_height() - self._canvas.winfo_height()
        if overflow > 0:
            self._canvas.yview_moveto(min(1.0, card.winfo_y() / overflow))

    def _mousewheel(self, event: tk.Event) -> None:
        self._canvas.yview_scroll(-1 if event.delta > 0 else 1, "units")

    def _bind_mousewheel_tree(self, widget: tk.Misc) -> None:
        widget.bind("<MouseWheel>", self._mousewheel, add="+")
        for child in widget.winfo_children():
            self._bind_mousewheel_tree(child)
