"""Application command buttons."""

from __future__ import annotations

import tkinter as tk
from collections.abc import Callable
from tkinter import ttk

from gui.components import ControlGroup
from gui.theme import SPACING


CONTROL_GROUP_ORDER = ("GAME", "PLAYER VERDICT", "ASSISTANCE", "SOLVER")


class Controls(ttk.Frame):
    def __init__(
        self,
        parent: tk.Misc,
        *,
        on_load: Callable[[], None],
        on_restart: Callable[[], None],
        on_criminal: Callable[[], None],
        on_innocent: Callable[[], None],
        on_hint: Callable[[], None],
        on_solve_next: Callable[[], None],
        on_auto_solve: Callable[[], None],
    ) -> None:
        super().__init__(parent, style="App.TFrame", padding=(0, SPACING["xs"]))
        for column, weight in enumerate((1, 2, 1, 2)):
            self.columnconfigure(column, weight=weight)

        game = ControlGroup(self, CONTROL_GROUP_ORDER[0])
        game.grid(row=0, column=0, sticky="nsew", padx=(0, SPACING["sm"]))
        ttk.Button(game, text="Load", command=on_load, style="Game.TButton").grid(row=0, column=0, padx=2)
        ttk.Button(game, text="Restart", command=on_restart, style="Game.TButton").grid(row=0, column=1, padx=2)

        player = ControlGroup(self, CONTROL_GROUP_ORDER[1])
        player.grid(row=0, column=1, sticky="nsew", padx=(0, SPACING["sm"]))
        ttk.Button(player, text="INNOCENT", command=on_innocent, style="Primary.TButton").grid(
            row=0, column=0, sticky="ew", padx=2
        )
        ttk.Button(player, text="CRIMINAL", command=on_criminal, style="Danger.TButton").grid(
            row=0, column=1, sticky="ew", padx=2
        )
        player.columnconfigure(0, weight=1)
        player.columnconfigure(1, weight=1)

        assistance = ControlGroup(self, CONTROL_GROUP_ORDER[2])
        assistance.grid(row=0, column=2, sticky="nsew", padx=(0, SPACING["sm"]))
        ttk.Button(assistance, text="Hint", command=on_hint, style="Assist.TButton").grid(
            row=0, column=0, sticky="ew", padx=2
        )
        assistance.columnconfigure(0, weight=1)

        solver = ControlGroup(self, CONTROL_GROUP_ORDER[3])
        solver.grid(row=0, column=3, sticky="nsew")
        ttk.Button(solver, text="Solve Next", command=on_solve_next, style="Solver.TButton").grid(
            row=0, column=0, sticky="ew", padx=2
        )
        self._auto_button = ttk.Button(solver, text="Auto Solve", command=on_auto_solve, style="Solver.TButton")
        self._auto_button.grid(row=0, column=1, sticky="ew", padx=2)
        solver.columnconfigure(0, weight=1)
        solver.columnconfigure(1, weight=1)

    def set_auto_running(self, running: bool) -> None:
        self._auto_button.configure(state="disabled" if running else "normal")
