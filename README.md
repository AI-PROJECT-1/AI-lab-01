# Griductive Solver

Course project for CSC14003 - Introduction to Artificial Intelligence.

This repository is developed in specification-gated phases. Phases 01-13 now
provide the domain and game foundation, canonical clue semantics, automatic CNF,
a team-implemented DPLL solver, a public-only entailment agent, progressive
deduction with trace/uniqueness checks, an integrated desktop GUI, two clue
extensions, and a validated 3x3/4x4 puzzle suite.

## Requirements

- Python 3.11 or newer
- Tkinter (normally included with CPython)

No third-party runtime or test package is required.

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

## Current scope

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

Experiments, final verification packaging, report support, and demo preparation
remain in Phases 14-17.

See `docs/REQUIREMENTS_AUDIT.md` and `docs/ARCHITECTURE.md` for the specification
mapping and security boundary.
