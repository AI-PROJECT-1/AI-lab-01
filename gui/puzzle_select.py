"""Scrollable public catalog for choosing shipped puzzles."""

from __future__ import annotations

from collections.abc import Callable
import tkinter as tk
from tkinter import ttk

from gui.components import AppHeader
from gui.puzzle_catalog import PUZZLE_CATALOG, PuzzleCatalogEntry
from gui.theme import COLORS, FONTS, SPACING


class PuzzleSelectScreen(ttk.Frame):
    def __init__(
        self,
        parent: tk.Misc,
        on_play: Callable[[str], None],
        on_back: Callable[[], None],
    ) -> None:
        super().__init__(parent, style="App.TFrame")
        self._on_play = on_play
        self._current_puzzle_id: str | None = None
        self._cards: dict[str, tk.Frame] = {}
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        AppHeader(self).grid(row=0, column=0, sticky="ew")
        heading = ttk.Frame(self, style="App.TFrame", padding=(SPACING["xl"], SPACING["lg"], SPACING["xl"], SPACING["sm"]))
        heading.grid(row=1, column=0, sticky="ew")
        heading.columnconfigure(0, weight=1)
        ttk.Label(heading, text="Choose a Puzzle", style="PuzzleSelectTitle.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(
            heading,
            text="Choose a deduction-focused case from Standard through Expert.",
            style="Muted.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(SPACING["xs"], 0))

        body = ttk.Frame(self, style="App.TFrame", padding=(SPACING["xl"], 0, SPACING["xl"], SPACING["sm"]))
        body.grid(row=2, column=0, sticky="nsew")
        body.columnconfigure(0, weight=1)
        body.rowconfigure(0, weight=1)
        self._canvas = tk.Canvas(body, background=COLORS["canvas"], borderwidth=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(body, orient="vertical", command=self._canvas.yview)
        self._canvas.configure(yscrollcommand=scrollbar.set)
        self._canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        self._content = tk.Frame(self._canvas, background=COLORS["canvas"])
        self._window = self._canvas.create_window((0, 0), window=self._content, anchor="nw")
        self._content.bind("<Configure>", self._update_scrollregion)
        self._canvas.bind("<Configure>", self._resize_content)
        self._canvas.bind("<MouseWheel>", self._mousewheel)

        footer = ttk.Frame(self, style="App.TFrame", padding=(SPACING["xl"], SPACING["sm"]))
        footer.grid(row=3, column=0, sticky="ew")
        ttk.Button(footer, text="Back to Game", command=on_back, style="Game.TButton").pack(side="left")

    @property
    def current_puzzle_id(self) -> str | None:
        return self._current_puzzle_id

    @property
    def card_count(self) -> int:
        return len(self._cards)

    def render(self, current_puzzle_id: str) -> None:
        self._current_puzzle_id = current_puzzle_id
        for child in self._content.winfo_children():
            child.destroy()
        self._cards.clear()
        for row, entry in enumerate(PUZZLE_CATALOG):
            card = self._build_card(entry, entry.puzzle_id == current_puzzle_id)
            card.grid(row=row, column=0, sticky="ew", pady=(0, SPACING["sm"]))
            self._bind_mousewheel_tree(card)
            self._cards[entry.puzzle_id] = card
        self._content.columnconfigure(0, weight=1)
        self._content.update_idletasks()
        self._update_scrollregion()

    def _build_card(self, entry: PuzzleCatalogEntry, current: bool) -> tk.Frame:
        border = COLORS["accent"] if current else COLORS["line"]
        outer = tk.Frame(self._content, background=border, padx=2 if current else 1, pady=2 if current else 1)
        card = tk.Frame(outer, background=COLORS["surface"], padx=SPACING["md"], pady=SPACING["sm"])
        card.pack(fill="both", expand=True)
        card.columnconfigure(0, weight=1)
        tk.Label(card, text=entry.name, anchor="w", background=COLORS["surface"], foreground=COLORS["ink"], font=FONTS["title"]).grid(row=0, column=0, sticky="w")
        badge_text = f"{entry.size}x{entry.size}  ·  {entry.difficulty}"
        tk.Label(card, text=badge_text, anchor="w", background=COLORS["surface"], foreground=COLORS["accent"], font=FONTS["section"]).grid(row=1, column=0, sticky="w", pady=(2, 0))
        tk.Label(card, text=entry.description, anchor="w", justify="left", wraplength=780, background=COLORS["surface"], foreground=COLORS["muted"], font=FONTS["body"]).grid(row=2, column=0, sticky="ew", pady=(SPACING["xs"], 0))
        if current:
            tk.Label(card, text="CURRENTLY PLAYING", background=COLORS["accent_soft"], foreground=COLORS["accent"], font=FONTS["small"], padx=8, pady=3).grid(row=0, column=1, sticky="e", padx=(SPACING["md"], 0))
        ttk.Button(card, text="Play", command=lambda puzzle_id=entry.puzzle_id: self._on_play(puzzle_id), style="Primary.TButton").grid(row=1, column=1, rowspan=2, sticky="e", padx=(SPACING["md"], 0))
        return outer

    def _update_scrollregion(self, _event: tk.Event | None = None) -> None:
        self._canvas.configure(scrollregion=self._canvas.bbox("all"))

    def _resize_content(self, event: tk.Event) -> None:
        self._canvas.itemconfigure(self._window, width=event.width)

    def _mousewheel(self, event: tk.Event) -> None:
        self._canvas.yview_scroll(-1 if event.delta > 0 else 1, "units")

    def _bind_mousewheel_tree(self, widget: tk.Misc) -> None:
        widget.bind("<MouseWheel>", self._mousewheel, add="+")
        for child in widget.winfo_children():
            self._bind_mousewheel_tree(child)
