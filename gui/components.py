"""Reusable presentation-only primitives shared by the desktop views."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from gui.feedback import FeedbackTone, GameplayFeedback
from gui.theme import SPACING


class AppHeader(ttk.Frame):
    def __init__(self, parent: tk.Misc) -> None:
        super().__init__(parent, style="Header.TFrame", padding=(SPACING["xl"], SPACING["sm"]))
        self.columnconfigure(0, weight=1)
        ttk.Label(self, text="GRIDUCTIVE", style="AppTitle.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(
            self,
            text="A public-clue deduction game",
            style="AppSubtitle.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(2, 0))


class FeedbackBar(ttk.Frame):
    """Reusable, semantic gameplay feedback surface."""

    _SYMBOLS = {
        FeedbackTone.NEUTRAL: "•",
        FeedbackTone.SUCCESS: "✓",
        FeedbackTone.INFO: "i",
        FeedbackTone.WARNING: "!",
        FeedbackTone.ERROR: "×",
    }

    def __init__(self, parent: tk.Misc, feedback: GameplayFeedback) -> None:
        super().__init__(parent, padding=(SPACING["md"], 6))
        self.columnconfigure(2, weight=1)
        self._symbol = ttk.Label(self)
        self._symbol.grid(row=0, column=0, padx=(0, SPACING["sm"]))
        self._title = ttk.Label(self, anchor="w")
        self._title.grid(row=0, column=1, sticky="w", padx=(0, SPACING["md"]))
        self._message = ttk.Label(self, anchor="w", wraplength=960)
        self._message.grid(row=0, column=2, sticky="ew")
        self.show(feedback)

    @property
    def feedback(self) -> GameplayFeedback:
        return self._feedback

    def show(self, feedback: GameplayFeedback) -> None:
        self._feedback = feedback
        prefix = f"Feedback{feedback.tone.value.title()}"
        self.configure(style=f"{prefix}.TFrame")
        self._symbol.configure(text=self._SYMBOLS[feedback.tone], style=f"{prefix}.Symbol.TLabel")
        self._title.configure(text=feedback.title, style=f"{prefix}.Title.TLabel")
        self._message.configure(text=feedback.message, style=f"{prefix}.TLabel")


class ControlGroup(ttk.LabelFrame):
    def __init__(self, parent: tk.Misc, title: str) -> None:
        super().__init__(
            parent,
            text=title,
            style="ControlGroup.TLabelframe",
            padding=(SPACING["sm"], 2),
        )
        self.rowconfigure(0, weight=1)
