"""Small UI-only frame navigator for the single Tk root."""

from __future__ import annotations

from enum import StrEnum
import tkinter as tk


class ScreenName(StrEnum):
    GAME = "game"
    PUZZLES = "puzzles"


class ScreenManager:
    def __init__(self, screens: dict[ScreenName, tk.Misc], initial: ScreenName) -> None:
        if initial not in screens:
            raise ValueError("initial screen must be registered")
        self._screens = dict(screens)
        self._current = initial
        for name, screen in self._screens.items():
            if name is not initial:
                screen.grid_remove()

    @property
    def current(self) -> ScreenName:
        return self._current

    def show(self, name: ScreenName) -> None:
        if name not in self._screens:
            raise ValueError(f"unregistered screen: {name}")
        if name is self._current:
            return
        self._screens[self._current].grid_remove()
        self._screens[name].grid(row=0, column=0, sticky="nsew")
        self._screens[name].tkraise()
        self._current = name
