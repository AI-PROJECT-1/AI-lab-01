"""Deterministic public-only extraction of irreducible Hint support."""

from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter

from agent.deduction_trace import HintExplanation
from agent.entailment import classify_public_target
from core.enums import Classification, Status
from core.public_state import KnownVerdict, PublicKnowledgeState, RevealedClue


@dataclass(frozen=True, slots=True)
class _SupportComponent:
    kind: str
    identifier: str


def extract_irreducible_support(
    public_state: PublicKnowledgeState,
    target_character_id: str,
    target_status: Status,
) -> HintExplanation | None:
    """Return deterministic deletion-irreducible public support, if verified.

    Components are tested in stable clue-ID order followed by proved verdicts
    in row-major character order. Each clue remains an indivisible component,
    regardless of how many CNF clauses encode it. The result is irreducible
    under single-component deletion; it is not a globally minimum-cardinality
    proof and must not be presented as one.
    """

    started = perf_counter()
    if public_state.status_of(target_character_id) is not None:
        return None
    if target_character_id not in {character.id for character in public_state.characters}:
        return None
    if not isinstance(target_status, Status):
        return None

    expected = Classification.from_status(target_status)
    baseline = classify_public_target(public_state, target_character_id)
    sat_calls = baseline.sat_calls
    if baseline.classification is not expected:
        return None

    clues = tuple(
        sorted(
            public_state.revealed_clues,
            key=lambda item: (item.clue.id, item.owner_id),
        )
    )
    if len(clues) != len({item.clue.id for item in clues}):
        return None
    position = {
        character.id: (character.row, character.column, character.id)
        for character in public_state.characters
    }
    verdicts = tuple(
        sorted(
            public_state.known_verdicts,
            key=lambda item: position[item.character_id],
        )
    )
    components = [
        *(_SupportComponent("clue", item.clue.id) for item in clues),
        *(_SupportComponent("verdict", item.character_id) for item in verdicts),
    ]

    index = 0
    while index < len(components):
        candidate = components[index]
        reduced_components = components[:index] + components[index + 1 :]
        reduced_state = _state_for_components(
            public_state,
            clues,
            verdicts,
            reduced_components,
        )
        check = classify_public_target(reduced_state, target_character_id)
        sat_calls += check.sat_calls
        if check.classification is expected:
            components = reduced_components
        else:
            index += 1

    supporting_clue_ids = tuple(
        component.identifier for component in components if component.kind == "clue"
    )
    supporting_verdict_ids = tuple(
        component.identifier for component in components if component.kind == "verdict"
    )
    if not supporting_clue_ids and not supporting_verdict_ids:
        return None
    return HintExplanation(
        target_character_id=target_character_id,
        supporting_clue_ids=supporting_clue_ids,
        supporting_verdict_ids=supporting_verdict_ids,
        method="deletion_irreducible",
        support_extraction_sat_calls=sat_calls,
        support_extraction_runtime=perf_counter() - started,
    )


def _state_for_components(
    original: PublicKnowledgeState,
    clues: tuple[RevealedClue, ...],
    verdicts: tuple[KnownVerdict, ...],
    components: list[_SupportComponent],
) -> PublicKnowledgeState:
    clue_ids = {
        component.identifier for component in components if component.kind == "clue"
    }
    verdict_ids = {
        component.identifier for component in components if component.kind == "verdict"
    }
    included_clues = tuple(item for item in clues if item.clue.id in clue_ids)
    included_verdicts = tuple(item for item in verdicts if item.character_id in verdict_ids)
    return PublicKnowledgeState(
        puzzle_id=original.puzzle_id,
        title=original.title,
        size=original.size,
        characters=original.characters,
        revealed_clues=included_clues,
        known_verdicts=included_verdicts,
        is_complete=len(included_verdicts) == len(original.characters),
    )
