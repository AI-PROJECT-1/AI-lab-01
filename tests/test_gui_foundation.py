"""Headless checks for the UI Phase 1 visual foundation contracts."""

from __future__ import annotations

import re
import unittest

from gui.controls import CONTROL_GROUP_ORDER
from gui.theme import COLORS, FONTS, SPACING


class VisualFoundationTests(unittest.TestCase):
    def test_semantic_control_groups_are_stable(self) -> None:
        self.assertEqual(
            CONTROL_GROUP_ORDER,
            ("GAME", "PLAYER VERDICT", "ASSISTANCE", "SOLVER"),
        )

    def test_palette_tokens_are_valid_hex_colors(self) -> None:
        required = {
            "canvas",
            "surface",
            "ink",
            "muted",
            "line",
            "accent",
            "danger",
            "focus",
        }
        self.assertTrue(required.issubset(COLORS))
        for name, value in COLORS.items():
            with self.subTest(token=name):
                self.assertRegex(value, re.compile(r"^#[0-9A-Fa-f]{6}$"))

    def test_spacing_and_type_scales_have_required_levels(self) -> None:
        self.assertEqual(tuple(SPACING), ("xs", "sm", "md", "lg", "xl"))
        self.assertEqual(tuple(SPACING.values()), tuple(sorted(SPACING.values())))
        self.assertTrue({"display", "title", "section", "body", "small", "button"}.issubset(FONTS))


if __name__ == "__main__":
    unittest.main()
