"""Read-only presentation of public deduction traces."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from agent.deduction_trace import DeductionTraceStep
from gui.theme import COLORS, FONTS, SPACING


class TracePanel(ttk.LabelFrame):
    def __init__(self, parent: tk.Misc) -> None:
        super().__init__(parent, text="SOLVER TRACE", style="Panel.TLabelframe", padding=SPACING["md"])
        self._listbox = tk.Listbox(
            self,
            height=8,
            exportselection=False,
            background=COLORS["surface_alt"],
            foreground=COLORS["muted"],
            borderwidth=0,
            highlightthickness=0,
            font=FONTS["small"],
            activestyle="none",
        )
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self._listbox.yview)
        self._listbox.configure(yscrollcommand=scrollbar.set)
        self._listbox.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def render(self, steps: tuple[DeductionTraceStep, ...]) -> None:
        self._listbox.delete(0, tk.END)
        for step in steps:
            self._listbox.insert(tk.END, step.display_text())
        if steps:
            self._listbox.see(tk.END)
