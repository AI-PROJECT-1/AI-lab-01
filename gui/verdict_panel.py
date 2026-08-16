"""Contextual player-verdict controls driven by public card data."""

from __future__ import annotations

from dataclasses import dataclass
import tkinter as tk
from collections.abc import Callable
from tkinter import ttk

from gui.components import ControlGroup
from gui.view_model import CardViewModel


@dataclass(frozen=True, slots=True)
class VerdictContext:
    identity: str
    detail: str
    can_submit: bool


def verdict_context_for(card: CardViewModel | None, *, is_complete: bool = False) -> VerdictContext:
    if is_complete:
        return VerdictContext(
            "Puzzle solved · all verdicts are public",
            "Verdict actions are no longer needed.",
            False,
        )
    if card is None:
        return VerdictContext(
            "Select an unresolved character",
            "Verdict actions are unavailable.",
            False,
        )
    if card.status is not None:
        return VerdictContext(
            f"{card.name} · {card.coordinate} · {card.profession}",
            f"Already public: {card.status.value}",
            False,
        )
    return VerdictContext(
        f"{card.name} · {card.coordinate} · {card.profession}",
        "Choose only a verdict forced by public clues.",
        True,
    )


class VerdictPanel(ControlGroup):
    def __init__(
        self,
        parent: tk.Misc,
        on_innocent: Callable[[], None],
        on_criminal: Callable[[], None],
    ) -> None:
        super().__init__(parent, "PLAYER VERDICT")
        self.rowconfigure(0, weight=0)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self._identity = ttk.Label(self, style="VerdictIdentity.TLabel", anchor="w")
        self._identity.grid(row=0, column=0, columnspan=2, sticky="ew", padx=2)
        self._innocent_button = ttk.Button(
            self,
            text="INNOCENT",
            command=on_innocent,
            style="VerdictPrimary.TButton",
        )
        self._innocent_button.grid(row=1, column=0, sticky="ew", padx=2, pady=(2, 0))
        self._criminal_button = ttk.Button(
            self,
            text="CRIMINAL",
            command=on_criminal,
            style="VerdictDanger.TButton",
        )
        self._criminal_button.grid(row=1, column=1, sticky="ew", padx=2, pady=(2, 0))
        self.set_context(None)

    @property
    def can_submit(self) -> bool:
        return str(self._innocent_button.cget("state")) == "normal"

    @property
    def context_text(self) -> str:
        return str(self._identity.cget("text"))

    def set_context(self, card: CardViewModel | None, *, is_complete: bool = False) -> None:
        context = verdict_context_for(card, is_complete=is_complete)
        identity = context.identity
        if card is not None and card.status is not None:
            identity = f"{identity} · {card.status.value}"
        self._identity.configure(text=identity)
        state = "normal" if context.can_submit else "disabled"
        self._innocent_button.configure(state=state)
        self._criminal_button.configure(state=state)
