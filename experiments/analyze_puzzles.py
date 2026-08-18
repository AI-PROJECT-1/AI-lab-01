"""Public-reasoning quality profiles for distributable Griductive puzzles."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from agent.logic_agent import LogicAgent
from core.public_state import PublicKnowledgeState, RevealedClue
from game.game_engine import GameEngine
from game.puzzle_loader import PuzzleLoader


ROOT = Path(__file__).parents[1]
PUZZLE_DIR = ROOT / "puzzles"
DEFAULT_OUTPUT = ROOT / "experiments" / "results" / "puzzle_quality.json"


def puzzle_paths() -> tuple[Path, ...]:
    return tuple(
        path
        for path in sorted(PUZZLE_DIR.glob("*.json"))
        if path.name != "schema.json"
    )


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
    return {
        "puzzle_file": path.name,
        "puzzle_id": puzzle.id,
        "display_name": puzzle.title,
        "size": puzzle.size,
        "characters": len(puzzle.cards),
        "clues": len(puzzle.cards),
        "initial_revealed_clues": len(puzzle.initially_revealed_ids),
        "clue_types": clue_types,
        "regions": regions,
        "extensions": extensions,
        "fact_clues": sum(card.clue.type.value == "FACT" for card in puzzle.cards),
        "deduction_steps": len(steps),
        "average_support_size": sum(support_sizes) / len(support_sizes) if support_sizes else 0.0,
        "maximum_support_size": max(support_sizes, default=0),
        "single_component_deductions": sum(size == 1 for size in support_sizes),
        "direct_single_fact_deductions": sum(step["direct_single_fact"] for step in steps),
        "unique": uniqueness.is_unique,
        "consistent": uniqueness.is_consistent,
        "progressively_solvable": engine.public_state().is_complete,
        "steps": steps,
    }


def analyze_suite() -> dict[str, object]:
    return {
        "schema_version": 1,
        "puzzles": [analyze_puzzle(path) for path in puzzle_paths()],
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
