"""Public-only, two-stage Hint presentation state."""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import StrEnum
from collections.abc import Callable
from typing import Sequence

from agent.deduction_trace import DeductionTraceStep, HintResult
from core.public_state import PublicKnowledgeState


class HintStage(StrEnum):
    ACTIVE_CLUES = "ACTIVE_CLUES"
    TARGET = "TARGET"


@dataclass(frozen=True, slots=True)
class PublicStateFingerprint:
    puzzle_id: str
    known_verdicts: tuple[tuple[str, str], ...]
    revealed_clues: tuple[tuple[str, str], ...]
    is_complete: bool


@dataclass(frozen=True, slots=True)
class HintSession:
    fingerprint: PublicStateFingerprint
    stage: HintStage
    target_character_id: str | None
    active_clue_ids: tuple[str, ...]
    supporting_verdict_ids: tuple[str, ...] = ()
    has_grounded_support: bool = False


@dataclass(frozen=True, slots=True)
class HintPresentation:
    title: str
    message: str
    active_clue_ids: tuple[str, ...] = ()
    target_character_id: str | None = None
    next_button_text: str = "Hint"
    supporting_verdict_ids: tuple[str, ...] = ()


@dataclass(slots=True)
class HintVisualState:
    """Mutable GUI-only holder; never part of public game knowledge."""

    session: HintSession | None = None
    active_clue_ids: tuple[str, ...] = ()
    target_character_id: str | None = None
    supporting_verdict_ids: tuple[str, ...] = ()

    def apply(self, session: HintSession, presentation: HintPresentation) -> None:
        self.session = session
        self.active_clue_ids = presentation.active_clue_ids
        self.target_character_id = presentation.target_character_id
        self.supporting_verdict_ids = presentation.supporting_verdict_ids

    def invalidate(self) -> None:
        self.session = None
        self.active_clue_ids = ()
        self.target_character_id = None
        self.supporting_verdict_ids = ()


def fingerprint_public_state(state: PublicKnowledgeState) -> PublicStateFingerprint:
    """Identify public knowledge without private puzzle data or object identity."""

    return PublicStateFingerprint(
        state.puzzle_id,
        tuple((item.character_id, item.status.value) for item in state.known_verdicts),
        tuple((item.owner_id, item.clue.id) for item in state.revealed_clues),
        state.is_complete,
    )


def begin_hint_session(
    state: PublicKnowledgeState,
    result: HintResult,
    request_trace: Sequence[DeductionTraceStep],
) -> tuple[HintSession, HintPresentation]:
    """Cache safe presentation fields from one completed reasoning request."""

    public_clue_ids = tuple(item.clue.id for item in state.revealed_clues)
    active_candidates: set[str] = set()
    for step in request_trace:
        active_candidates.update(step.active_clue_ids)
    if result.deduction is not None:
        active_candidates.update(result.deduction.trace.active_clue_ids)
    active_clue_ids = tuple(clue_id for clue_id in public_clue_ids if clue_id in active_candidates)

    public_character_ids = {character.id for character in state.characters}
    public_verdict_ids = {item.character_id for item in state.known_verdicts}
    target = result.deduction.character_id if result.deduction is not None else None
    if target not in public_character_ids or (target is not None and state.status_of(target) is not None):
        target = None

    explanation = result.explanation
    has_grounded_support = False
    supporting_verdict_ids: tuple[str, ...] = ()
    if (
        explanation is not None
        and explanation.target_character_id == target
        and explanation.method == "deletion_irreducible"
    ):
        proposed_clues = explanation.supporting_clue_ids
        proposed_verdicts = explanation.supporting_verdict_ids
        if (
            len(proposed_clues) == len(set(proposed_clues))
            and len(proposed_verdicts) == len(set(proposed_verdicts))
            and set(proposed_clues).issubset(public_clue_ids)
            and set(proposed_verdicts).issubset(public_verdict_ids)
            and (proposed_clues or proposed_verdicts)
        ):
            active_clue_ids = proposed_clues
            supporting_verdict_ids = proposed_verdicts
            has_grounded_support = True

    session = HintSession(
        fingerprint_public_state(state),
        HintStage.ACTIVE_CLUES,
        target,
        active_clue_ids,
        supporting_verdict_ids,
        has_grounded_support,
    )
    if has_grounded_support:
        clue_phrase = _clue_support_phrase(active_clue_ids)
        verdict_phrase = _verdict_support_phrase(state, supporting_verdict_ids)
        support_parts = tuple(part for part in (clue_phrase, verdict_phrase) if part)
        if len(active_clue_ids) == 1 and not supporting_verdict_ids:
            message = f"Take another look at this supporting public statement: {active_clue_ids[0]}."
        else:
            message = f"Review these supporting public constraints: {'; '.join(support_parts)}."
    elif active_clue_ids:
        message = "Review these currently active revealed clues. No single clue is claimed as the proof anchor."
    else:
        message = "Review the currently revealed public information. No specific proof anchor is available."
    return session, HintPresentation(
        "Hint · Stage 1",
        message,
        active_clue_ids=active_clue_ids,
        next_button_text="Show target",
        supporting_verdict_ids=supporting_verdict_ids,
    )


def _clue_support_phrase(clue_ids: tuple[str, ...]) -> str:
    if not clue_ids:
        return ""
    label = "clue" if len(clue_ids) == 1 else "clues"
    return f"{label} {', '.join(clue_ids)}"


def _verdict_support_phrase(
    state: PublicKnowledgeState,
    character_ids: tuple[str, ...],
) -> str:
    if not character_ids:
        return ""
    verdicts = tuple(
        f"{character_id} = {state.status_of(character_id).value}"
        for character_id in character_ids
    )
    label = "known verdict" if len(verdicts) == 1 else "known verdicts"
    return f"{label} {', '.join(verdicts)}"


def can_advance_hint(session: HintSession | None, state: PublicKnowledgeState) -> bool:
    return (
        session is not None
        and session.stage is HintStage.ACTIVE_CLUES
        and session.fingerprint == fingerprint_public_state(state)
    )


def advance_hint_session(
    session: HintSession,
    state: PublicKnowledgeState,
) -> tuple[HintSession, HintPresentation]:
    """Advance to target presentation without another reasoning request."""

    if not can_advance_hint(session, state):
        raise ValueError("hint session does not match current public knowledge")
    advanced = replace(session, stage=HintStage.TARGET)
    if session.target_character_id is None:
        return advanced, HintPresentation(
            "Hint · Stage 2",
            "No unresolved target can currently be identified from the cached public hint.",
        )

    character = next(item for item in state.characters if item.id == session.target_character_id)
    return advanced, HintPresentation(
        "Hint · Stage 2",
        f"Focus on {character.name} · {character.id}.",
        target_character_id=character.id,
    )


def progress_hint_session(
    session: HintSession | None,
    get_state: Callable[[], PublicKnowledgeState],
    get_hint: Callable[[], HintResult],
    get_trace: Callable[[], Sequence[DeductionTraceStep]],
) -> tuple[HintSession, HintPresentation, bool]:
    """Advance presentation, invoking reasoning only to begin a fresh cycle."""

    state = get_state()
    if can_advance_hint(session, state):
        advanced, presentation = advance_hint_session(session, state)
        return advanced, presentation, False

    trace_count = len(get_trace())
    result = get_hint()
    refreshed_state = get_state()
    request_trace = get_trace()[trace_count:]
    started, presentation = begin_hint_session(refreshed_state, result, request_trace)
    return started, presentation, True
