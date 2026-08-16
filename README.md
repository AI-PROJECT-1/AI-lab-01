# Griductive Solver

Course project for CSC14003 - Introduction to Artificial Intelligence.

This repository contains a complete desktop implementation of Griductive for
CSC14003 Project 2: canonical clue semantics, automatic CNF, a team-implemented
DPLL solver, a public-only entailment agent, progressive deduction with trace
and uniqueness checks, two clue extensions, a responsive Tkinter GUI, and a
validated 3x3/4x4 puzzle suite.

## Requirements

- Python 3.11 or newer
- Tkinter (normally included with CPython)

No third-party runtime or test package is required.

```powershell
python -m pip install -r requirements.txt
```

## Run

```powershell
python main.py
```

The default puzzle is `puzzles/sample_3x3.json`. Use **Load** in the application
to choose another JSON puzzle.

## Test

```powershell
python -m unittest discover -s tests -v
```

`unittest` is the supported runner. `pytest` is not required or declared as a
dependency.

## Reproduce experiments

```powershell
python -m experiments.run_experiments
```

The command runs every distributable 3x3/4x4 puzzle and overwrites
`experiments/results/final_regression.json` with machine-readable raw results.
Failures are retained and cause a non-zero exit code.

## Implemented scope

- Phase 01: repository foundation
- Phase 02: immutable domain contracts and JSON puzzle schema
- Phase 03: loader, public-state boundary, restart/reveal game engine
- Phase 04: Tkinter grid, verdict controls, Load, and Restart
- Phase 05: canonical region resolution and direct semantic evaluator
- Phase 06: deterministic variable mapping, direct combinational CNF, and KB builder
- Phase 07: deterministic baseline DPLL with assumptions and solver statistics
- Phase 08: SAT-entailment LogicAgent (`CRIMINAL`, `INNOCENT`, `UNKNOWN`, `INCONSISTENT`)
- Phase 09: Hint, Solve Next, progressive Auto Solve, deduction trace, uniqueness
- Phase 10: production agent wired through GameEngine and GUI
- Phase 11: selectable clues with canonical referenced-cell highlighting
- Phase 12: `IMPLIES` and `ODD` clue extensions
- Phase 13: two validated 3x3 and two validated 4x4 puzzles

The final experiment runner, report-support notes, demo script, requirement
matrix, and known-limitations record are also included. The team must still
provide real member attribution/contribution percentages and produce the final
PDF report, hosted demo video, and submission archive; these artifacts are not
fabricated by the source audit.

See `docs/REQUIREMENTS_AUDIT.md`, `docs/DEMO_SCRIPT.md`,
`docs/KNOWN_LIMITATIONS.md`, and `docs/ARCHITECTURE.md` for final readiness and
the security boundary.
