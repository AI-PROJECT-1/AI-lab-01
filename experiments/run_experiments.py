"""Reproducible Project 2 experiment runner for the distributable puzzle suite."""

from __future__ import annotations

import argparse
import json
import platform
import statistics
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter

from agent.logic_agent import LogicAgent
from core.public_state import PublicKnowledgeState, RevealedClue
from game.game_engine import GameEngine
from game.puzzle_loader import PuzzleLoader
from logic.cnf_encoder import CNFEncoder


ROOT = Path(__file__).parents[1]
PUZZLE_DIR = ROOT / "puzzles"
DEFAULT_OUTPUT = ROOT / "experiments" / "results" / "final_regression.json"


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
        tuple(
            RevealedClue(card.character.id, card.clue)
            for card in puzzle.ordered_cards
        ),
        (),
        False,
    )


def encoding_report(state: PublicKnowledgeState) -> dict[str, int]:
    return CNFEncoder(state).build_kb().report()


def _hint_support_benchmark(path: Path, runs: int) -> dict[str, object]:
    wall_times: list[float] = []
    extraction_times: list[float] = []
    sat_calls: list[int] = []
    methods: set[str] = set()
    target_ids: set[str] = set()

    for _ in range(runs):
        engine = GameEngine(PuzzleLoader.load(path), LogicAgent())
        started = perf_counter()
        result = engine.get_hint()
        wall_times.append(perf_counter() - started)
        explanation = result.explanation
        if explanation is None:
            continue
        extraction_times.append(explanation.support_extraction_runtime)
        sat_calls.append(explanation.support_extraction_sat_calls)
        methods.add(explanation.method)
        target_ids.add(explanation.target_character_id)

    available = len(extraction_times) == runs
    return {
        "runs": runs,
        "available_every_run": available,
        "method": next(iter(methods)) if len(methods) == 1 else None,
        "target_character_id": next(iter(target_ids)) if len(target_ids) == 1 else None,
        "support_extraction_sat_calls": sat_calls[0] if len(set(sat_calls)) == 1 and sat_calls else None,
        "median_hint_wall_runtime_seconds": statistics.median(wall_times),
        "median_support_runtime_seconds": statistics.median(extraction_times) if extraction_times else None,
        "minimum_support_runtime_seconds": min(extraction_times) if extraction_times else None,
        "maximum_support_runtime_seconds": max(extraction_times) if extraction_times else None,
    }


def run_puzzle(path: Path, *, hint_runs: int = 25) -> dict[str, object]:
    puzzle = PuzzleLoader.load(path)
    initial_engine = GameEngine(puzzle, LogicAgent())
    initial_state = initial_engine.public_state()
    complete_state = complete_clue_state(puzzle)

    engine = GameEngine(puzzle, LogicAgent())
    started = perf_counter()
    reveals = engine.auto_solve()
    wall_runtime = perf_counter() - started
    final_state = engine.public_state()
    trace = engine.deduction_trace
    queries = tuple(query for step in trace for query in step.sat_queries)

    uniqueness_started = perf_counter()
    uniqueness = LogicAgent().check_uniqueness(complete_state)
    uniqueness_runtime = perf_counter() - uniqueness_started

    return {
        "puzzle_file": path.name,
        "puzzle_id": puzzle.id,
        "title": puzzle.title,
        "size": puzzle.size,
        "status": "PASS" if final_state.is_complete and uniqueness.is_unique else "FAIL",
        "error": None,
        "initial_kb": encoding_report(initial_state),
        "complete_clue_set_cnf": encoding_report(complete_state),
        "progressive_solve": {
            "completed": final_state.is_complete,
            "initially_revealed": len(puzzle.initially_revealed_ids),
            "reveals": len(reveals),
            "reveal_waves": len(reveals),
            "trace_steps": len(trace),
            "sat_calls": len(queries),
            "decisions": sum(query.decisions for query in queries),
            "propagations": sum(query.propagations for query in queries),
            "backtracks": sum(query.backtracks for query in queries),
            "sat_query_runtime_seconds": sum(query.runtime for query in queries),
            "whole_puzzle_wall_runtime_seconds": wall_runtime,
        },
        "uniqueness": {
            "consistent": uniqueness.is_consistent,
            "unique": uniqueness.is_unique,
            "sat_calls": uniqueness.sat_calls,
            "wall_runtime_seconds": uniqueness_runtime,
        },
        "hint_support": _hint_support_benchmark(path, hint_runs),
    }


def _git_head() -> str | None:
    try:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def run_suite(*, hint_runs: int = 25) -> dict[str, object]:
    results: list[dict[str, object]] = []
    for path in puzzle_paths():
        try:
            results.append(run_puzzle(path, hint_runs=hint_runs))
        except Exception as exc:  # Retain failures instead of dropping cases.
            results.append(
                {
                    "puzzle_file": path.name,
                    "status": "FAIL",
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )
    return {
        "schema_version": 1,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "baseline_commit": _git_head(),
        "command": "python -m experiments.run_experiments",
        "python": platform.python_version(),
        "platform": platform.platform(),
        "hint_support_runs_per_puzzle": hint_runs,
        "puzzle_set": [path.name for path in puzzle_paths()],
        "results": results,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--hint-runs", type=int, default=25)
    args = parser.parse_args(argv)
    if args.hint_runs < 1:
        parser.error("--hint-runs must be at least 1")

    report = run_suite(hint_runs=args.hint_runs)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    failed = [result for result in report["results"] if result["status"] != "PASS"]
    print(f"Wrote {args.output} ({len(report['results'])} puzzles, {len(failed)} failures).")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
