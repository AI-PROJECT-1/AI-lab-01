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
from gui.completion_panel import CompletionPanel, completion_presentation_for
from gui.controller import (
    CharacterInteractionKind,
    GameController,
    ManualVerdictLockedError,
    SelectionRequiredError,
)
from gui.controls import Controls
from gui.feedback import (
    FeedbackTone,
    feedback_for_verdict,
    manual_lock_feedback,
    newly_revealed_character,
    notice_feedback,
)
from gui.hint_session import (
    HintPresentation,
    HintVisualState,
    progress_hint_session,
)
from gui.puzzle_catalog import catalog_entry, puzzle_path
from gui.puzzle_select import PuzzleSelectScreen
from gui.screen_manager import ScreenManager, ScreenName
from gui.trace_panel import ActionSource, SolverDetailsModel, SolverDetailsWindow
from gui.components import AppHeader, FeedbackBar
from gui.theme import SPACING, configure_theme
from gui.view_model import CardViewModel, build_card_views


DEFAULT_PUZZLE = Path(__file__).parents[1] / "puzzles" / "standard_deduction_3x3.json"


class GriductiveApp(ttk.Frame):
    def __init__(self, root: tk.Tk, puzzle_path: str | Path = DEFAULT_PUZZLE) -> None:
        configure_theme(root)
        super().__init__(root, style="App.TFrame")
        root.title("Griductive")
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
        self._newly_revealed_id: str | None = None
        self._hint_state = HintVisualState()
        self._auto_running = False
        self._auto_after_id: str | None = None
        self._auto_generation = 0
        self._solver_details_model = SolverDetailsModel()
        self._solver_details_window: SolverDetailsWindow | None = None
        AppHeader(self).grid(row=0, column=0, sticky="ew")

        title_area = ttk.Frame(self, style="App.TFrame", padding=(SPACING["xl"], SPACING["sm"], SPACING["xl"], 0))
        title_area.grid(row=1, column=0, sticky="ew")
        title_area.columnconfigure(0, weight=1)
        self._title = ttk.Label(title_area, style="PuzzleTitle.TLabel")
        self._title.grid(row=0, column=0, sticky="w")
        self._instruction = ttk.Label(
            title_area,
            text="Select a card, then submit only a logically forced verdict.",
            style="Muted.TLabel",
        )
        self._instruction.grid(
            row=1, column=0, sticky="w", pady=(2, 0)
        )
        self._completion = CompletionPanel(title_area)
        self._completion.grid(row=2, column=0, sticky="ew", pady=(2, 0))

        content = ttk.Frame(self, style="App.TFrame", padding=(SPACING["xl"], SPACING["sm"]))
        content.grid(row=2, column=0, sticky="nsew")
        content.grid_propagate(False)
        content.columnconfigure(0, weight=3, minsize=520)
        content.columnconfigure(1, weight=2, minsize=320)
        content.rowconfigure(0, weight=1)

        self._board = BoardView(content, self._select_character)
        self._board.grid(row=0, column=0, sticky="nsew", padx=(0, SPACING["md"]))
        self._board.grid_propagate(False)
        sidebar = ttk.Frame(content, style="App.TFrame")
        sidebar.grid(row=0, column=1, sticky="nsew")
        sidebar.columnconfigure(0, weight=1)
        sidebar.rowconfigure(0, weight=1)
        self._clues = CluePanel(sidebar, self._select_clue)
        self._clues.grid(row=0, column=0, sticky="nsew")
        self._clues.grid_propagate(False)
        self._controls = Controls(
            self,
            on_puzzles=self._show_puzzles,
            on_load=self._load,
            on_restart=self._restart,
            on_criminal=lambda: self._submit(Status.CRIMINAL),
            on_innocent=lambda: self._submit(Status.INNOCENT),
            on_hint=self._hint,
            on_solve_next=self._solve_next,
            on_auto_solve=self._auto_solve,
            on_solver_details=self._toggle_solver_details,
        )
        self._controls.grid(row=3, column=0, sticky="ew", padx=SPACING["xl"])
        self._feedback = FeedbackBar(
            self,
            notice_feedback(
                "Ready",
                "Select an unresolved character and submit only a verdict forced by public clues.",
                FeedbackTone.NEUTRAL,
            ),
        )
        self._feedback.grid(
            row=4, column=0, sticky="ew", padx=SPACING["xl"], pady=(0, SPACING["sm"])
        )
        ttk.Label(
            self,
            text="SAT entailment agent · public clues and proved verdicts only",
            style="Muted.TLabel",
        ).grid(row=5, column=0, sticky="w", padx=SPACING["xl"], pady=(0, SPACING["sm"]))
        self._puzzle_select = PuzzleSelectScreen(root, self._play_shipped_puzzle, self._show_game)
        self._screen_manager = ScreenManager(
            {
                ScreenName.GAME: self,
                ScreenName.PUZZLES: self._puzzle_select,
            },
            ScreenName.GAME,
        )
        self._render()

    def _render(self) -> None:
        state = self._controller.state()
        if state.is_complete and (
            self._hint_state.session is not None
            or self._hint_state.active_clue_ids
            or self._hint_state.target_character_id is not None
            or self._hint_state.supporting_verdict_ids
        ):
            self._invalidate_hint_session()
        catalog = catalog_entry(state.puzzle_id)
        difficulty = f"  ·  {catalog.difficulty}" if catalog is not None else ""
        self._title.configure(text=f"{state.title} ({state.size}x{state.size}){difficulty}")
        if state.is_complete:
            self._instruction.grid_remove()
        else:
            self._instruction.grid()
        self._completion.show_presentation(completion_presentation_for(state))
        selected_card = self._card_for(state, self._controller.selected_character_id)
        self._board.render(
            state,
            self._controller.selected_character_id,
            self._highlighted_ids,
            self._newly_revealed_id,
            self._hint_state.target_character_id,
            self._hint_state.supporting_verdict_ids,
            self._controller.manual_locked_ids,
        )
        self._clues.render(
            state,
            self._controller.selected_clue_owner_id,
            self._newly_revealed_id,
            self._hint_state.active_clue_ids,
        )
        if self._solver_details_window is not None and self._solver_details_window.exists:
            self._solver_details_window.render(
                self._solver_details_model.presentations(self._controller.trace())
            )
        self._controls.set_verdict_context(
            selected_card,
            manual_locked=(
                selected_card is not None
                and self._controller.is_manual_locked(selected_card.character_id)
            ),
        )
        self._controls.set_completion_state(state.is_complete)

    @staticmethod
    def _card_for(state, character_id: str | None) -> CardViewModel | None:
        if character_id is None:
            return None
        return next((card for card in build_card_views(state) if card.character_id == character_id), None)

    def _select_character(self, character_id: str) -> None:
        self._newly_revealed_id = None
        interaction = self._controller.activate_character(character_id)
        state = self._controller.state()
        card = self._card_for(state, character_id)
        if interaction.kind is CharacterInteractionKind.INSPECT_PUBLIC_CLUE:
            self._highlighted_ids = interaction.referenced_character_ids
            self._feedback.show(
                notice_feedback(
                    "Public clue selected",
                    f"{card.name} ({card.coordinate}) owns {interaction.clue_id}; its referenced cells are highlighted.",
                    FeedbackTone.INFO,
                )
            )
            self._render()
            return

        self._highlighted_ids = ()
        if card is not None and self._controller.is_manual_locked(character_id):
            self._feedback.show(manual_lock_feedback(card))
            self._render()
            return
        self._feedback.show(
            notice_feedback(
                "Character selected",
                f"{card.name} ({card.coordinate}), {card.profession}." if card else character_id,
                FeedbackTone.NEUTRAL,
            )
        )
        self._render()

    def _select_clue(self, owner_id: str) -> None:
        self._newly_revealed_id = None
        clue = self._controller.state().clue_for(owner_id)
        self._highlighted_ids = self._controller.select_clue(owner_id)
        self._feedback.show(notice_feedback("Public clue selected", clue.display_text()))
        self._render()

    def _submit(self, status: Status) -> None:
        if self._controller.state().is_complete:
            self._feedback.show(
                notice_feedback("Puzzle already solved", "All character verdicts are already public.")
            )
            self._render()
            return
        before = self._controller.state()
        before_trace_count = len(self._controller.trace())
        try:
            result = self._controller.submit_selected(status)
        except SelectionRequiredError as exc:
            self._newly_revealed_id = None
            self._feedback.show(notice_feedback("Selection required", str(exc), FeedbackTone.WARNING))
            return
        except ManualVerdictLockedError:
            self._newly_revealed_id = None
            selected = self._card_for(self._controller.state(), self._controller.selected_character_id)
            if selected is not None:
                self._feedback.show(manual_lock_feedback(selected))
            self._render()
            return
        except AgentIntegrityError:
            self._record_new_trace(before_trace_count, ActionSource.MANUAL_VERDICT)
            self._newly_revealed_id = None
            safe_message = "The solver failed an internal integrity check. No public state was changed."
            messagebox.showerror("Agent integrity error", safe_message, parent=self)
            self._feedback.show(notice_feedback("Solver integrity error", safe_message, FeedbackTone.ERROR))
            self._render()
            return
        self._record_new_trace(before_trace_count, ActionSource.MANUAL_VERDICT)
        after = self._controller.state()
        self._newly_revealed_id = newly_revealed_character(result, before, after)
        if after != before:
            self._invalidate_hint_session()
        card = self._card_for(after, result.character_id)
        if card is None:
            raise RuntimeError("verdict result references a character outside public state")
        self._feedback.show(
            feedback_for_verdict(
                result,
                card,
                manual_locked=self._controller.is_manual_locked(result.character_id),
            )
        )
        self._render()

    def _restart(self) -> None:
        self._cancel_auto()
        self._controller.restart()
        self._solver_details_model.clear_trace_metadata()
        self._clear_transient_presentation()
        self._feedback.show(
            notice_feedback("Puzzle restarted", "Selection and transient feedback were cleared.", FeedbackTone.NEUTRAL)
        )
        self._render()

    def _show_puzzles(self) -> None:
        if self._auto_running:
            self._feedback.show(
                notice_feedback(
                    "Auto Solve in progress",
                    "Wait for Auto Solve to finish before changing screens.",
                    FeedbackTone.WARNING,
                )
            )
            return
        self._puzzle_select.render(self._controller.state().puzzle_id)
        self._screen_manager.show(ScreenName.PUZZLES)

    def _show_game(self) -> None:
        self._screen_manager.show(ScreenName.GAME)

    def _play_shipped_puzzle(self, puzzle_id: str) -> None:
        try:
            puzzle = PuzzleLoader.load(puzzle_path(puzzle_id))
        except (PuzzleFormatError, ValueError) as exc:
            messagebox.showerror("Cannot load shipped puzzle", str(exc), parent=self.winfo_toplevel())
            return
        self._cancel_auto()
        self._controller.load(puzzle)
        self._solver_details_model.clear_trace_metadata()
        self._clear_transient_presentation()
        self._feedback.show(
            notice_feedback(
                "Puzzle selected",
                f"Now playing {puzzle.title}. Gameplay state was reset.",
                FeedbackTone.NEUTRAL,
            )
        )
        self._render()
        self._puzzle_select.render(puzzle.id)
        self._screen_manager.show(ScreenName.GAME)

    def _load(self) -> None:
        self._cancel_auto()
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
            self._feedback.show(
                notice_feedback("Load failed", "The current puzzle was not changed.", FeedbackTone.ERROR)
            )
            return
        self._solver_details_model.clear_trace_metadata()
        self._clear_transient_presentation()
        self._feedback.show(
            notice_feedback("Puzzle loaded", f"Loaded {puzzle.title}. Selection was cleared.", FeedbackTone.NEUTRAL)
        )
        self._render()

    def _hint(self) -> None:
        if self._controller.state().is_complete:
            self._invalidate_hint_session()
            self._feedback.show(
                notice_feedback("Puzzle already solved", "No further Hint is needed.")
            )
            self._render()
            return
        before_trace_count = len(self._controller.trace())
        session, presentation, reasoning_requested = progress_hint_session(
            self._hint_state.session,
            self._controller.state,
            self._controller.hint,
            self._controller.trace,
        )
        if reasoning_requested:
            self._record_new_trace(before_trace_count, ActionSource.HINT)
        self._hint_state.apply(session, presentation)
        self._apply_hint_presentation(presentation)
        self._render()

    def _apply_hint_presentation(self, presentation: HintPresentation) -> None:
        self._controls.set_hint_button_text(presentation.next_button_text)
        self._feedback.show(notice_feedback(presentation.title, presentation.message, FeedbackTone.INFO))

    def _invalidate_hint_session(self) -> None:
        self._hint_state.invalidate()
        if hasattr(self, "_controls"):
            self._controls.set_hint_button_text("Hint")

    def _clear_transient_presentation(self) -> None:
        self._highlighted_ids = ()
        self._newly_revealed_id = None
        self._invalidate_hint_session()

    def _solve_next(self) -> None:
        if self._controller.state().is_complete:
            self._feedback.show(
                notice_feedback("Puzzle already solved", "No further forced verdict is needed.")
            )
            self._render()
            return
        self._newly_revealed_id = None
        self._invalidate_hint_session()
        before = self._controller.state()
        before_trace_count = len(self._controller.trace())
        try:
            result = self._controller.solve_next()
        except AgentIntegrityError:
            self._record_new_trace(before_trace_count, ActionSource.SOLVE_NEXT)
            safe_message = "The solver failed an internal integrity check. No public state was changed."
            messagebox.showerror("Agent integrity error", safe_message, parent=self)
            self._feedback.show(notice_feedback("Solver integrity error", safe_message, FeedbackTone.ERROR))
            self._render()
            return
        self._record_new_trace(before_trace_count, ActionSource.SOLVE_NEXT)
        if result is None:
            self._feedback.show(notice_feedback("No forced verdict", "No unresolved verdict is currently forced."))
        else:
            self._newly_revealed_id = newly_revealed_character(result, before, self._controller.state())
            self._invalidate_hint_session()
            self._feedback.show(notice_feedback("Solve Next", result.message, FeedbackTone.SUCCESS))
        self._render()

    def _auto_solve(self) -> None:
        if self._auto_running or self._controller.state().is_complete:
            if self._controller.state().is_complete:
                self._feedback.show(
                    notice_feedback("Puzzle already solved", "Auto Solve has no remaining steps.")
                )
                self._render()
            return
        self._newly_revealed_id = None
        self._invalidate_hint_session()
        self._auto_running = True
        self._auto_generation += 1
        generation = self._auto_generation
        self._controls.set_auto_running(True)
        self._feedback.show(notice_feedback("Auto Solve", "Progressive solving started."))
        self._auto_after_id = self.after(1, lambda: self._auto_step(generation))

    def _auto_step(self, generation: int | None = None) -> None:
        if generation is None:
            generation = self._auto_generation
        if not self._auto_running or generation != self._auto_generation:
            return
        self._auto_after_id = None
        before = self._controller.state()
        before_trace_count = len(self._controller.trace())
        try:
            result = self._controller.solve_next()
        except AgentIntegrityError:
            self._record_new_trace(before_trace_count, ActionSource.AUTO_SOLVE)
            self._finish_auto("Auto Solve stopped after an internal integrity check failed.")
            return
        self._record_new_trace(before_trace_count, ActionSource.AUTO_SOLVE)
        if result is None:
            self._render()
            message = "Auto Solve complete." if self._controller.state().is_complete else "Auto Solve stopped: no forced verdict."
            self._finish_auto(message)
            return
        self._newly_revealed_id = newly_revealed_character(result, before, self._controller.state())
        self._invalidate_hint_session()
        self._render()
        self._feedback.show(notice_feedback("Auto Solve", result.message, FeedbackTone.SUCCESS))
        if self._controller.state().is_complete:
            self._finish_auto("Puzzle solved. Every character verdict is now public.")
            return
        self._auto_after_id = self.after(120, lambda: self._auto_step(generation))

    def _finish_auto(self, message: str) -> None:
        self._auto_after_id = None
        self._auto_running = False
        self._controls.set_auto_running(False)
        self._feedback.show(notice_feedback("Auto Solve", message))

    def _cancel_auto(self) -> None:
        if self._auto_after_id is not None:
            try:
                self.after_cancel(self._auto_after_id)
            except tk.TclError:
                pass
        self._auto_after_id = None
        self._auto_running = False
        self._auto_generation += 1
        if hasattr(self, "_controls"):
            self._controls.set_auto_running(False)

    def _record_new_trace(self, before_count: int, source: ActionSource) -> None:
        self._solver_details_model.record_new_steps(
            before_count,
            self._controller.trace(),
            source,
        )

    def _toggle_solver_details(self) -> None:
        if self._solver_details_model.is_open and self._solver_details_window is not None:
            self._solver_details_window.close()
            return
        if self._solver_details_window is None or not self._solver_details_window.exists:
            self._solver_details_window = SolverDetailsWindow(
                self.winfo_toplevel(),
                self._solver_details_model,
            )
        self._solver_details_window.render(
            self._solver_details_model.presentations(self._controller.trace())
        )
        self._solver_details_window.open()


def main() -> None:
    root = tk.Tk()
    try:
        GriductiveApp(root)
    except PuzzleFormatError as exc:
        messagebox.showerror("Cannot start Griductive", str(exc), parent=root)
        root.destroy()
        return
    root.mainloop()
