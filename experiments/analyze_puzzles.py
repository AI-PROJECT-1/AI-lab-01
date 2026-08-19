"""Public-reasoning quality profiles for distributable Griductive puzzles."""

from __future__ import annotations

import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path

from agent.logic_agent import LogicAgent
from core.enums import Classification, ClueType, RegionType, Status
from core.public_state import PublicKnowledgeState, RevealedClue
from game.game_engine import GameEngine
from game.puzzle_loader import PuzzleLoader
from gui.puzzle_catalog import PUZZLE_CATALOG, puzzle_path


ROOT = Path(__file__).parents[1]
DEFAULT_OUTPUT = ROOT / "experiments" / "results" / "puzzle_quality.json"


def puzzle_paths() -> tuple[Path, ...]:
    """Return the explicit public production set in catalog order."""

    return tuple(puzzle_path(entry.puzzle_id) for entry in PUZZLE_CATALOG)


def complete_clue_state(puzzle) -> PublicKnowledgeState:
    return PublicKnowledgeState(
        puzzle.id,
        puzzle.title,
        puzzle.size,
        tuple(card.character for card in puzzle.ordered_cards),
        tuple(RevealedClue(card.character.id, card.clue) for card in puzzle.ordered_cards),
        (),
        False,
    )


def analyze_puzzle(path: Path) -> dict[str, object]:
    puzzle = PuzzleLoader.load(path)
    engine = GameEngine(puzzle, LogicAgent())
    steps: list[dict[str, object]] = []
    clue_types_by_id = {card.clue.id: card.clue.type.value for card in puzzle.cards}

    while not engine.public_state().is_complete:
        state = engine.public_state()
        classifications = LogicAgent().classify_all(state)
        unresolved_ids = [
            character.id
            for character in state.characters
            if state.status_of(character.id) is None
        ]
        forced_ids = [
            character_id
            for character_id in unresolved_ids
            if classifications[character_id]
            in (Classification.CRIMINAL, Classification.INNOCENT)
        ]
        hint = LogicAgent().get_hint(state)
        if hint.deduction is None:
            break
        explanation = hint.explanation
        clue_ids = explanation.supporting_clue_ids if explanation else ()
        verdict_ids = explanation.supporting_verdict_ids if explanation else ()
        result = engine.solve_next()
        if result is None:
            break
        if result.character_id != hint.deduction.character_id or result.forced_status is not hint.deduction.status:
            raise RuntimeError("Hint and Solve Next disagree on the deterministic target")
        direct_fact = (
            len(clue_ids) == 1
            and not verdict_ids
            and clue_types_by_id[clue_ids[0]] == "FACT"
        )
        steps.append(
            {
                "step": len(steps) + 1,
                "unresolved_ids": unresolved_ids,
                "forced_character_ids": forced_ids,
                "target": result.character_id,
                "verdict": result.forced_status.value,
                "supporting_clue_count": len(clue_ids),
                "supporting_known_verdict_count": len(verdict_ids),
                "support_size": len(clue_ids) + len(verdict_ids),
                "supporting_clue_ids": list(clue_ids),
                "supporting_known_verdict_ids": list(verdict_ids),
                "direct_single_fact": direct_fact,
            }
        )

    support_sizes = [step["support_size"] for step in steps]
    clue_types = sorted({card.clue.type.value for card in puzzle.cards})
    regions = sorted(
        {
            card.clue.region.kind.value
            for card in puzzle.cards
            if card.clue.region is not None
        }
    )
    extensions = sorted(set(clue_types) & {"IMPLIES", "ODD"})
    uniqueness = LogicAgent().check_uniqueness(complete_clue_state(puzzle))
    solution_fingerprint = "".join(
        "C" if card.hidden_status is Status.CRIMINAL else "I"
        for card in puzzle.ordered_cards
    )
    clue_counts = Counter(card.clue.type.value for card in puzzle.cards)
    clue_type_histogram = {clue_type.value: clue_counts[clue_type.value] for clue_type in ClueType}
    region_counts = Counter(
        card.clue.region.kind.value
        for card in puzzle.cards
        if card.clue.region is not None
    )
    region_type_histogram = {region.value: region_counts[region.value] for region in RegionType}
    return {
        "puzzle_file": path.name,
        "puzzle_id": puzzle.id,
        "display_name": puzzle.title,
        "size": puzzle.size,
        "characters": len(puzzle.cards),
        "clues": len(puzzle.cards),
        "initial_revealed_clues": len(puzzle.initially_revealed_ids),
        "initial_revealed_cells": list(puzzle.initially_revealed_ids),
        "clue_types": clue_types,
        "regions": regions,
        "extensions": extensions,
        "solution_fingerprint": solution_fingerprint,
        "clue_type_histogram": clue_type_histogram,
        "region_type_histogram": region_type_histogram,
        "clue_ownership_map": {
            card.character.id: card.clue.id for card in puzzle.ordered_cards
        },
        "fact_clues": sum(card.clue.type.value == "FACT" for card in puzzle.cards),
        "direct_answer_fact_ids": [
            card.clue.id for card in puzzle.cards if card.clue.type.value == "FACT"
        ],
        "deduction_steps": len(steps),
        "deduction_target_sequence": [step["target"] for step in steps],
        "reveal_owner_sequence": [
            *puzzle.initially_revealed_ids,
            *(step["target"] for step in steps),
        ],
        "average_support_size": sum(support_sizes) / len(support_sizes) if support_sizes else 0.0,
        "maximum_support_size": max(support_sizes, default=0),
        "single_component_deductions": sum(size == 1 for size in support_sizes),
        "support_size_1_count": sum(size == 1 for size in support_sizes),
        "support_size_gte_2_count": sum(size >= 2 for size in support_sizes),
        "support_size_sequence": support_sizes,
        "supporting_component_sequence": [
            {
                "clue_ids": step["supporting_clue_ids"],
                "known_verdict_ids": step["supporting_known_verdict_ids"],
            }
            for step in steps
        ],
        "direct_single_fact_deductions": sum(step["direct_single_fact"] for step in steps),
        "unique": uniqueness.is_unique,
        "consistent": uniqueness.is_consistent,
        "progressively_solvable": engine.public_state().is_complete,
        "steps": steps,
    }


def _pairwise_fingerprints(profiles: list[dict[str, object]]) -> list[dict[str, object]]:
    comparisons: list[dict[str, object]] = []
    for left, right in combinations(profiles, 2):
        if left["size"] != right["size"]:
            continue
        left_solution = str(left["solution_fingerprint"])
        right_solution = str(right["solution_fingerprint"])
        comparison = {
            "left": left["puzzle_id"],
            "right": right["puzzle_id"],
            "size": left["size"],
            "solution_hamming_distance": sum(
                a != b for a, b in zip(left_solution, right_solution, strict=True)
            ),
            "solutions_are_full_complements": all(
                a != b for a, b in zip(left_solution, right_solution, strict=True)
            ),
            "same_initial_reveals": left["initial_revealed_cells"] == right["initial_revealed_cells"],
            "same_extensions": left["extensions"] == right["extensions"],
            "same_clue_ownership_map": left["clue_ownership_map"] == right["clue_ownership_map"],
            "same_target_sequence": left["deduction_target_sequence"] == right["deduction_target_sequence"],
            "same_reveal_owner_sequence": left["reveal_owner_sequence"] == right["reveal_owner_sequence"],
            "same_support_sequence": left["support_size_sequence"] == right["support_size_sequence"],
            "same_supporting_components": left["supporting_component_sequence"]
            == right["supporting_component_sequence"],
            "same_clue_type_histogram": left["clue_type_histogram"] == right["clue_type_histogram"],
            "same_region_type_histogram": left["region_type_histogram"] == right["region_type_histogram"],
        }
        comparison["suspicious_structural_duplicate"] = (
            comparison["solution_hamming_distance"] == 0
            or (
                comparison["solutions_are_full_complements"]
                and all(
                    comparison[field]
                    for field in (
                        "same_initial_reveals",
                        "same_extensions",
                        "same_target_sequence",
                        "same_support_sequence",
                        "same_clue_type_histogram",
                        "same_region_type_histogram",
                    )
                )
            )
            or all(
                comparison[field]
                for field in (
                    "same_initial_reveals",
                    "same_target_sequence",
                    "same_reveal_owner_sequence",
                    "same_support_sequence",
                    "same_clue_type_histogram",
                    "same_region_type_histogram",
                )
            )
        )
        comparisons.append(comparison)
    return comparisons


def analyze_suite() -> dict[str, object]:
    profiles = [analyze_puzzle(path) for path in puzzle_paths()]
    return {
        "schema_version": 2,
        "puzzles": profiles,
        "same_size_pairwise_fingerprints": _pairwise_fingerprints(profiles),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args(argv)
    result = analyze_suite()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    failed = [
        puzzle
        for puzzle in result["puzzles"]
        if not puzzle["unique"] or not puzzle["progressively_solvable"]
    ]
    print(f"Wrote {args.output} ({len(result['puzzles'])} puzzles, {len(failed)} failures).")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
