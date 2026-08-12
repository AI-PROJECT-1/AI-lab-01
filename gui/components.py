"""Reusable presentation-only primitives shared by the desktop views."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

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
    """A visual shell for the existing status text; semantics stay in GriductiveApp."""

    def __init__(self, parent: tk.Misc, textvariable: tk.StringVar) -> None:
        super().__init__(parent, style="Feedback.TFrame", padding=(SPACING["md"], 6))
        self.columnconfigure(1, weight=1)
        ttk.Label(self, text="●", style="Feedback.TLabel").grid(row=0, column=0, padx=(0, SPACING["sm"]))
        ttk.Label(
            self,
            textvariable=textvariable,
            style="Feedback.TLabel",
            anchor="w",
            wraplength=960,
        ).grid(row=0, column=1, sticky="ew")


class ControlGroup(ttk.LabelFrame):
    def __init__(self, parent: tk.Misc, title: str) -> None:
        super().__init__(
            parent,
            text=title,
            style="ControlGroup.TLabelframe",
            padding=(SPACING["sm"], 2),
        )
        self.rowconfigure(0, weight=1)
