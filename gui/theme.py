"""Design tokens and ttk configuration for the Griductive desktop UI."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk


COLORS = {
    "canvas": "#F4F1EA",
    "surface": "#FFFDF8",
    "surface_alt": "#ECE7DC",
    "ink": "#25231F",
    "muted": "#6D685F",
    "line": "#D6CFC2",
    "accent": "#315B52",
    "accent_hover": "#274A43",
    "accent_soft": "#DCE9E4",
    "danger": "#8F3F3A",
    "danger_hover": "#74332F",
    "danger_soft": "#F3E0DD",
    "focus": "#C58A2C",
    "focus_soft": "#F7E9C7",
    "success": "#356247",
    "info": "#365C78",
    "card_unresolved": "#F2EEE6",
    "card_unresolved_border": "#B8AFA1",
    "card_criminal": "#F8E6E3",
    "card_criminal_border": "#A94D47",
    "card_innocent": "#E3EFEA",
    "card_innocent_border": "#3F7460",
    "avatar_1": "#547A72",
    "avatar_2": "#6E6688",
    "avatar_3": "#8A684D",
    "avatar_4": "#526F8A",
}

SPACING = {
    "xs": 4,
    "sm": 8,
    "md": 12,
    "lg": 18,
    "xl": 24,
}

FONTS = {
    "display": ("Segoe UI Semibold", 20),
    "title": ("Segoe UI Semibold", 14),
    "section": ("Segoe UI Semibold", 10),
    "body": ("Segoe UI", 10),
    "small": ("Segoe UI", 9),
    "button": ("Segoe UI Semibold", 10),
}


def configure_theme(root: tk.Misc) -> ttk.Style:
    """Apply the project-owned visual language without changing application behavior."""

    style = ttk.Style(root)
    if "clam" in style.theme_names():
        style.theme_use("clam")

    root.configure(background=COLORS["canvas"])

    style.configure("App.TFrame", background=COLORS["canvas"])
    style.configure("Header.TFrame", background=COLORS["accent"])
    style.configure("Surface.TFrame", background=COLORS["surface"])
    style.configure("Feedback.TFrame", background=COLORS["accent_soft"])

    style.configure(
        "AppTitle.TLabel",
        background=COLORS["accent"],
        foreground="#FFFFFF",
        font=FONTS["display"],
    )
    style.configure(
        "AppSubtitle.TLabel",
        background=COLORS["accent"],
        foreground="#DDEBE7",
        font=FONTS["small"],
    )
    style.configure(
        "PuzzleTitle.TLabel",
        background=COLORS["canvas"],
        foreground=COLORS["ink"],
        font=FONTS["title"],
    )
    style.configure(
        "Muted.TLabel",
        background=COLORS["canvas"],
        foreground=COLORS["muted"],
        font=FONTS["small"],
    )
    style.configure(
        "Feedback.TLabel",
        background=COLORS["accent_soft"],
        foreground=COLORS["ink"],
        font=FONTS["body"],
    )

    for style_name in ("Panel.TLabelframe", "ControlGroup.TLabelframe"):
        style.configure(
            style_name,
            background=COLORS["surface"],
            bordercolor=COLORS["line"],
            lightcolor=COLORS["line"],
            darkcolor=COLORS["line"],
            relief="solid",
            borderwidth=1,
        )
        style.configure(
            f"{style_name}.Label",
            background=COLORS["surface"],
            foreground=COLORS["ink"],
            font=FONTS["section"],
        )

    _configure_button(style, "Game.TButton", COLORS["surface_alt"], COLORS["ink"], "#DDD6C9")
    _configure_button(style, "Primary.TButton", COLORS["accent"], "#FFFFFF", COLORS["accent_hover"])
    _configure_button(style, "Danger.TButton", COLORS["danger"], "#FFFFFF", COLORS["danger_hover"])
    _configure_button(style, "Assist.TButton", COLORS["focus_soft"], COLORS["ink"], "#EBD69D")
    _configure_button(style, "Solver.TButton", COLORS["accent_soft"], COLORS["ink"], "#CADDD6")
    return style


def _configure_button(
    style: ttk.Style,
    name: str,
    background: str,
    foreground: str,
    active_background: str,
) -> None:
    style.configure(
        name,
        background=background,
        foreground=foreground,
        bordercolor=background,
        focusthickness=2,
        focuscolor=COLORS["focus"],
        font=FONTS["button"],
        padding=(12, 8),
    )
    style.map(
        name,
        background=[("active", active_background), ("disabled", COLORS["surface_alt"])],
        foreground=[("disabled", COLORS["muted"])],
    )
