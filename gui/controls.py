"""Application command buttons."""

from __future__ import annotations

import tkinter as tk
from collections.abc import Callable
from tkinter import ttk


class Controls(ttk.Frame):
    def __init__(
        self,
        parent: tk.Misc,
        *,
        on_load: Callable[[], None],
        on_restart: Callable[[], None],
        on_criminal: Callable[[], None],
        on_innocent: Callable[[], None],
    ) -> None:
        super().__init__(parent, padding=(0, 8))
        ttk.Button(self, text="Load", command=on_load).grid(row=0, column=0, padx=4)
        ttk.Button(self, text="Restart", command=on_restart).grid(row=0, column=1, padx=4)
        ttk.Separator(self, orient="vertical").grid(row=0, column=2, sticky="ns", padx=8)
        ttk.Button(self, text="CRIMINAL", command=on_criminal).grid(row=0, column=3, padx=4)
        ttk.Button(self, text="INNOCENT", command=on_innocent).grid(row=0, column=4, padx=4)
        ttk.Separator(self, orient="vertical").grid(row=0, column=5, sticky="ns", padx=8)
        ttk.Button(self, text="Hint (Phase 10)", state="disabled").grid(row=0, column=6, padx=4)
        ttk.Button(self, text="Auto Solve (Phase 10)", state="disabled").grid(row=0, column=7, padx=4)
