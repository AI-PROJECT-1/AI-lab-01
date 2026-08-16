"""Public-state-driven completion presentation for the desktop UI."""

from __future__ import annotations

from dataclasses import dataclass
import tkinter as tk
from tkinter import ttk

from core.public_state import PublicKnowledgeState
from gui.theme import SPACING


@dataclass(frozen=True, slots=True)
class CompletionPresentation:
    visible: bool
    title: str
    message: str


def completion_presentation_for(state: PublicKnowledgeState) -> CompletionPresentation:
    """Build completion copy solely from the public completion signal."""

    if not state.is_complete:
        return CompletionPresentation(False, "", "")
    return CompletionPresentation(
        True,
        "Puzzle solved",
        "Every character has been logically resolved from the public clues.",
    )


class CompletionPanel(ttk.Frame):
    """Compact banner that leaves the completed board available for inspection."""

    def __init__(self, parent: tk.Misc) -> None:
        super().__init__(parent, style="Completion.TFrame", padding=(SPACING["md"], 2))
        self.columnconfigure(2, weight=1)
        ttk.Label(self, text="✓", style="CompletionSymbol.TLabel").grid(
            row=0, column=0, padx=(0, SPACING["sm"])
        )
        self._title = ttk.Label(self, style="CompletionTitle.TLabel")
        self._title.grid(row=0, column=1, sticky="w", padx=(0, SPACING["md"]))
        self._message = ttk.Label(self, style="Completion.TLabel")
        self._message.grid(row=0, column=2, sticky="w")
        self._visible = False

    @property
    def visible(self) -> bool:
        return self._visible

    def show_presentation(self, presentation: CompletionPresentation) -> None:
        self._visible = presentation.visible
        if presentation.visible:
            self._title.configure(text=presentation.title)
            self._message.configure(text=presentation.message)
            self.grid()
        else:
            self.grid_remove()
