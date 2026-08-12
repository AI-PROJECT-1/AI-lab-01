"""Pure presentation-contract tests for composable character card states."""

from __future__ import annotations

import unittest

from core.enums import Status
from gui.character_card import appearance_for, avatar_color_for
from gui.view_model import (
    CardBaseState,
    CardModifiers,
    CardViewModel,
    CardVisualState,
    compose_card_visual_state,
)


def make_card(*, status: Status | None = None, clue_text: str | None = None) -> CardViewModel:
    return CardViewModel(
        character_id="B2",
        row=2,
        column=2,
        name="Eva Stone",
        profession="Environmental Engineer",
        status=status,
        face_up=clue_text is not None,
        clue_id="SECRET-ID" if clue_text is not None else None,
        clue_text=clue_text,
    )


class CharacterCardPresentationTests(unittest.TestCase):
    def test_unresolved_visible_text_contains_only_public_identity(self) -> None:
        card = make_card()
        text = card.visible_text()
        for expected in ("B2", "ES", "Eva Stone", "Environmental Engineer"):
            self.assertIn(expected, text)
        for forbidden in ("UNKNOWN", "FACE-DOWN", "Clue: hidden", "SECRET-ID"):
            self.assertNotIn(forbidden, text)

    def test_revealed_cards_keep_textual_verdict_badges(self) -> None:
        criminal = make_card(status=Status.CRIMINAL, clue_text="A public criminal clue.")
        innocent = make_card(status=Status.INNOCENT, clue_text="A public innocent clue.")
        self.assertIn("CRIMINAL", criminal.visible_text())
        self.assertIn("INNOCENT", innocent.visible_text())
        self.assertIn("A public criminal clue", criminal.visible_text())
        self.assertIn("A public innocent clue", innocent.visible_text())

    def test_clue_preview_is_public_safe_and_bounded(self) -> None:
        card = make_card(clue_text="Exactly two criminals are in the long explicitly named public region.")
        preview = card.clue_preview(32)
        self.assertLessEqual(len(preview), 32)
        self.assertTrue(preview.endswith("…"))
        self.assertNotIn("SECRET-ID", card.visible_text())

    def test_selection_and_highlight_compose_without_replacing_base_identity(self) -> None:
        card = make_card(status=Status.CRIMINAL, clue_text="Public clue.")
        base = appearance_for(compose_card_visual_state(card))
        combined_state = CardVisualState(
            CardBaseState.CRIMINAL,
            CardModifiers(selected=True, clue_highlighted=True, newly_revealed=True),
        )
        combined = appearance_for(combined_state)
        self.assertEqual(combined.surface, base.surface)
        self.assertEqual(combined.base_border, base.base_border)
        self.assertEqual(combined.badge_background, base.badge_background)
        self.assertIsNotNone(combined.selection_outline)
        self.assertIsNotNone(combined.highlight_outline)
        self.assertIsNotNone(combined.reveal_outline)

    def test_innocent_highlight_preserves_innocent_identity(self) -> None:
        state = CardVisualState(
            CardBaseState.INNOCENT,
            CardModifiers(clue_highlighted=True),
        )
        appearance = appearance_for(state)
        self.assertIsNotNone(appearance.highlight_outline)
        self.assertNotEqual(appearance.surface, appearance.highlight_outline)
        self.assertIsNotNone(appearance.badge_background)

    def test_avatar_color_is_deterministic(self) -> None:
        self.assertEqual(avatar_color_for("B2"), avatar_color_for("B2"))
        self.assertRegex(avatar_color_for("B2"), r"^#[0-9A-Fa-f]{6}$")


if __name__ == "__main__":
    unittest.main()
