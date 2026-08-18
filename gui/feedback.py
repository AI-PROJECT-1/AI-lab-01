"""Public-only gameplay feedback models for GUI commands."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from core.enums import VerdictOutcome
from core.public_state import PublicKnowledgeState
from core.results import VerdictResult
from gui.view_model import CardViewModel


class FeedbackTone(StrEnum):
    NEUTRAL = "NEUTRAL"
    SUCCESS = "SUCCESS"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


@dataclass(frozen=True, slots=True)
class GameplayFeedback:
    tone: FeedbackTone
    title: str
    message: str


def notice_feedback(title: str, message: str, tone: FeedbackTone = FeedbackTone.INFO) -> GameplayFeedback:
    """Build reusable non-verdict feedback without domain-state access."""

    return GameplayFeedback(tone, title, message)


def feedback_for_verdict(
    result: VerdictResult,
    card: CardViewModel,
    *,
    manual_locked: bool = False,
) -> GameplayFeedback:
    """Describe a verdict using only its result category and public card data.

    The engine-provided free-form message and revealed clue payload are
    intentionally not copied into presentation feedback.
    """

    if result.character_id != card.character_id:
        raise ValueError("verdict result and public card must reference the same character")

    identity = f"{card.name} ({card.coordinate})"
    if result.outcome is VerdictOutcome.ACCEPTED:
        return GameplayFeedback(
            FeedbackTone.SUCCESS,
            "Verdict accepted",
            f"{identity} is now publicly confirmed {result.requested_status.value}. The public clue was revealed.",
        )
    if result.outcome is VerdictOutcome.NOT_PROVABLE:
        return GameplayFeedback(
            FeedbackTone.INFO,
            "Not provable yet",
            f"Current public information does not force {result.requested_status.value} for {identity}.",
        )
    if result.outcome is VerdictOutcome.CONTRADICTED:
        penalty = f" {identity} is locked for this run;" if manual_locked else ""
        return GameplayFeedback(
            FeedbackTone.WARNING,
            "Contradicted deduction",
            f"Public clues contradict that verdict.{penalty} clue stays hidden.",
        )
    return GameplayFeedback(
        FeedbackTone.ERROR,
        "Knowledge base inconsistent",
        "The public clues cannot be evaluated consistently. No character was revealed.",
    )


def manual_lock_feedback(card: CardViewModel) -> GameplayFeedback:
    return GameplayFeedback(
        FeedbackTone.WARNING,
        "Manual verdict locked",
        f"{card.name} ({card.coordinate}) is locked for this run; clue stays hidden.",
    )


def newly_revealed_character(
    result: VerdictResult,
    before: PublicKnowledgeState,
    after: PublicKnowledgeState,
) -> str | None:
    """Return a presentation emphasis target only for a fresh public reveal."""

    character_id = result.character_id
    if result.outcome is not VerdictOutcome.ACCEPTED:
        return None
    if before.status_of(character_id) is not None or before.clue_for(character_id) is not None:
        return None
    if after.status_of(character_id) is not result.requested_status:
        return None
    if after.clue_for(character_id) is None:
        return None
    return character_id
