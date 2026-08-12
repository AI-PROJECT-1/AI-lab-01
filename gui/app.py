"""Desktop application wiring for manual and SAT-assisted gameplay."""

from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from agent.logic_agent import LogicAgent
from core.enums import Status
from game.game_engine import AgentIntegrityError, GameEngine
from game.puzzle_loader import PuzzleFormatError, PuzzleLoader
from gui.board_view import BoardView
from gui.clue_panel import CluePanel
from gui.controller import GameController, SelectionRequiredError
from gui.controls import Controls
from gui.trace_panel import TracePanel
from gui.components import AppHeader, FeedbackBar
from gui.theme import SPACING, configure_theme


DEFAULT_PUZZLE = Path(__file__).parents[1] / "puzzles" / "sample_3x3.json"


class GriductiveApp(ttk.Frame):
    def __init__(self, root: tk.Tk, puzzle_path: str | Path = DEFAULT_PUZZLE) -> None:
        configure_theme(root)
        super().__init__(root, style="App.TFrame")
        root.title("Griductive Solver")
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = min(1180, max(920, screen_width - 80))
        window_height = min(800, max(640, screen_height - 60))
        root.geometry(f"{window_width}x{window_height}")
        root.minsize(min(920, window_width), min(640, window_height))
        self.grid(sticky="nsew")
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        puzzle = PuzzleLoader.load(puzzle_path)
        self._controller = GameController(GameEngine(puzzle, LogicAgent()))
        self._highlighted_ids: tuple[str, ...] = ()
        self._auto_running = False
        self._status = tk.StringVar(value="Ready. Select a character and submit a provable verdict.")
        AppHeader(self).grid(row=0, column=0, sticky="ew")

        title_area = ttk.Frame(self, style="App.TFrame", padding=(SPACING["xl"], SPACING["sm"], SPACING["xl"], 0))
        title_area.grid(row=1, column=0, sticky="ew")
        title_area.columnconfigure(0, weight=1)
        self._title = ttk.Label(title_area, style="PuzzleTitle.TLabel")
        self._title.grid(row=0, column=0, sticky="w")
        ttk.Label(title_area, text="Select a card, then submit only a logically forced verdict.", style="Muted.TLabel").grid(
            row=1, column=0, sticky="w", pady=(2, 0)
        )

        content = ttk.Frame(self, style="App.TFrame", padding=(SPACING["xl"], SPACING["sm"]))
        content.grid(row=2, column=0, sticky="nsew")
        content.columnconfigure(0, weight=3, minsize=520)
        content.columnconfigure(1, weight=2, minsize=320)
        content.rowconfigure(0, weight=1)

        self._board = BoardView(content, self._select_character)
        self._board.grid(row=0, column=0, sticky="nsew", padx=(0, SPACING["md"]))
        sidebar = ttk.Frame(content, style="App.TFrame")
        sidebar.grid(row=0, column=1, sticky="nsew")
        sidebar.columnconfigure(0, weight=1)
        sidebar.rowconfigure(0, weight=3)
        sidebar.rowconfigure(1, weight=2)
        self._clues = CluePanel(sidebar, self._select_clue)
        self._clues.grid(row=0, column=0, sticky="nsew", pady=(0, SPACING["sm"]))
        self._trace = TracePanel(sidebar)
        self._trace.grid(row=1, column=0, sticky="nsew")
        self._controls = Controls(
            self,
            on_load=self._load,
            on_restart=self._restart,
            on_criminal=lambda: self._submit(Status.CRIMINAL),
            on_innocent=lambda: self._submit(Status.INNOCENT),
            on_hint=self._hint,
            on_solve_next=self._solve_next,
            on_auto_solve=self._auto_solve,
        )
        self._controls.grid(row=3, column=0, sticky="ew", padx=SPACING["xl"])
        FeedbackBar(self, self._status).grid(
            row=4, column=0, sticky="ew", padx=SPACING["xl"], pady=(0, SPACING["sm"])
        )
        ttk.Label(
            self,
            text="SAT entailment agent · public clues and proved verdicts only",
            style="Muted.TLabel",
        ).grid(row=5, column=0, sticky="w", padx=SPACING["xl"], pady=(0, SPACING["sm"]))
        self._render()

    def _render(self) -> None:
        state = self._controller.state()
        completion = " - COMPLETE" if state.is_complete else ""
        self._title.configure(text=f"{state.title} ({state.size}x{state.size}){completion}")
        self._board.render(state, self._controller.selected_character_id, self._highlighted_ids)
        self._clues.render(state)
        self._trace.render(self._controller.trace())

    def _select_character(self, character_id: str) -> None:
        self._controller.select_character(character_id)
        self._status.set(f"Selected {character_id}.")

    def _select_clue(self, owner_id: str) -> None:
        clue = self._controller.state().clue_for(owner_id)
        self._highlighted_ids = self._controller.select_clue(owner_id)
        self._status.set(f"Selected {clue.id}: {clue.display_text()}")
        self._render()

    def _submit(self, status: Status) -> None:
        try:
            result = self._controller.submit_selected(status)
        except SelectionRequiredError as exc:
            self._status.set(str(exc))
            return
        except AgentIntegrityError as exc:
            messagebox.showerror("Agent integrity error", str(exc), parent=self)
            self._status.set("No state change: agent integrity check failed.")
            return
        self._status.set(f"{result.outcome.value}: {result.message}")
        self._render()

    def _restart(self) -> None:
        self._controller.restart()
        self._highlighted_ids = ()
        self._status.set("Puzzle restarted.")
        self._render()

    def _load(self) -> None:
        path = filedialog.askopenfilename(
            parent=self,
            title="Load Griductive puzzle",
            filetypes=(("JSON puzzle", "*.json"), ("All files", "*.*")),
        )
        if not path:
            return
        try:
            puzzle = PuzzleLoader.load(path)
            self._controller.load(puzzle)
        except PuzzleFormatError as exc:
            messagebox.showerror("Invalid puzzle", str(exc), parent=self)
            self._status.set("Load failed; current puzzle was not changed.")
            return
        self._highlighted_ids = ()
        self._status.set(f"Loaded {puzzle.title}.")
        self._render()

    def _hint(self) -> None:
        hint = self._controller.hint()
        self._status.set(f"HINT: {hint.message}")
        if hint.deduction:
            self._controller.select_character(hint.deduction.character_id)
        self._render()

    def _solve_next(self) -> None:
        try:
            result = self._controller.solve_next()
        except AgentIntegrityError as exc:
            messagebox.showerror("Agent integrity error", str(exc), parent=self)
            return
        if result is None:
            self._status.set("No unresolved verdict is currently forced.")
        else:
            self._status.set(f"SOLVE NEXT: {result.message}")
        self._render()

    def _auto_solve(self) -> None:
        if self._auto_running:
            return
        self._auto_running = True
        self._controls.set_auto_running(True)
        self._status.set("Auto Solve started.")
        self.after(1, self._auto_step)

    def _auto_step(self) -> None:
        try:
            result = self._controller.solve_next()
        except AgentIntegrityError as exc:
            self._finish_auto(f"Auto Solve stopped: {exc}")
            return
        self._render()
        if result is None:
            message = "Auto Solve complete." if self._controller.state().is_complete else "Auto Solve stopped: no forced verdict."
            self._finish_auto(message)
            return
        self._status.set(f"AUTO: {result.message}")
        self.after(120, self._auto_step)

    def _finish_auto(self, message: str) -> None:
        self._auto_running = False
        self._controls.set_auto_running(False)
        self._status.set(message)


def main() -> None:
    root = tk.Tk()
    try:
        GriductiveApp(root)
    except PuzzleFormatError as exc:
        messagebox.showerror("Cannot start Griductive Solver", str(exc), parent=root)
        root.destroy()
        return
    root.mainloop()
