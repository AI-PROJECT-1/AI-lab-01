"""Application command buttons."""

from __future__ import annotations

import tkinter as tk
from collections.abc import Callable
from tkinter import ttk

from gui.components import ControlGroup
from gui.theme import SPACING
from gui.verdict_panel import VerdictPanel
from gui.view_model import CardViewModel


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
        on_solver_details: Callable[[], None],
    ) -> None:
        super().__init__(parent, style="App.TFrame", padding=(0, SPACING["xs"]))
        for column, weight in enumerate((1, 2, 1, 2)):
            self.columnconfigure(column, weight=weight)

        game = ControlGroup(self, CONTROL_GROUP_ORDER[0])
        game.grid(row=0, column=0, sticky="nsew", padx=(0, SPACING["sm"]))
        ttk.Button(game, text="Load", command=on_load, style="Game.TButton").grid(row=0, column=0, padx=2)
        ttk.Button(game, text="Restart", command=on_restart, style="Game.TButton").grid(row=0, column=1, padx=2)

        self._verdict_panel = VerdictPanel(self, on_innocent, on_criminal)
        self._verdict_panel.grid(row=0, column=1, sticky="nsew", padx=(0, SPACING["sm"]))

        assistance = ControlGroup(self, CONTROL_GROUP_ORDER[2])
        assistance.grid(row=0, column=2, sticky="nsew", padx=(0, SPACING["sm"]))
        self._hint_button = ttk.Button(assistance, text="Hint", command=on_hint, style="Assist.TButton")
        self._hint_button.grid(row=0, column=0, sticky="ew", padx=2)
        assistance.columnconfigure(0, weight=1)

        solver = ControlGroup(self, CONTROL_GROUP_ORDER[3])
        solver.grid(row=0, column=3, sticky="nsew")
        self._solve_next_button = ttk.Button(
            solver, text="Solve Next", command=on_solve_next, style="Solver.TButton"
        )
        self._solve_next_button.grid(
            row=0, column=0, sticky="ew", padx=2
        )
        self._auto_button = ttk.Button(solver, text="Auto Solve", command=on_auto_solve, style="Solver.TButton")
        self._auto_button.grid(row=0, column=1, sticky="ew", padx=2)
        self._details_button = ttk.Button(
            solver,
            text="Solver Details",
            command=on_solver_details,
            style="Solver.TButton",
        )
        self._details_button.grid(row=1, column=0, columnspan=2, sticky="ew", padx=2, pady=(4, 0))
        solver.columnconfigure(0, weight=1)
        solver.columnconfigure(1, weight=1)
        self._current_card: CardViewModel | None = None
        self._is_complete = False
        self._auto_running = False

    def set_auto_running(self, running: bool) -> None:
        self._auto_running = running
        self._sync_solver_controls()

    @property
    def verdict_panel(self) -> VerdictPanel:
        return self._verdict_panel

    def set_verdict_context(self, card: CardViewModel | None) -> None:
        self._current_card = card
        self._verdict_panel.set_context(card, is_complete=self._is_complete)

    def set_completion_state(self, is_complete: bool) -> None:
        self._is_complete = is_complete
        self._verdict_panel.set_context(self._current_card, is_complete=is_complete)
        if is_complete:
            self.set_hint_button_text("Hint")
        self._hint_button.configure(state="disabled" if is_complete else "normal")
        self._sync_solver_controls()

    def _sync_solver_controls(self) -> None:
        self._solve_next_button.configure(state="disabled" if self._is_complete else "normal")
        self._auto_button.configure(
            state="disabled" if self._is_complete or self._auto_running else "normal"
        )

    @property
    def hint_available(self) -> bool:
        return str(self._hint_button.cget("state")) == "normal"

    @property
    def solve_next_available(self) -> bool:
        return str(self._solve_next_button.cget("state")) == "normal"

    @property
    def auto_solve_available(self) -> bool:
        return str(self._auto_button.cget("state")) == "normal"

    @property
    def hint_button_text(self) -> str:
        return str(self._hint_button.cget("text"))

    def set_hint_button_text(self, text: str) -> None:
        self._hint_button.configure(text=text)
