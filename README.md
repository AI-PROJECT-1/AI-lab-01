# Griductive Solver

Course project for CSC14003 - Introduction to Artificial Intelligence.

This repository is being developed in specification-gated phases. Phases 01-04
provide the repository foundation, shared domain contracts, a privacy-preserving
game engine, and a desktop GUI for manual gameplay. The production CNF encoder,
DPLL solver, and deductive logic agent belong to later phases and are not faked
here.

## Requirements

- Python 3.11 or newer
- Tkinter (normally included with CPython)

No third-party runtime package is required for Phases 01-04.

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

Hint, Auto Solve, general clue semantics, CNF, DPLL, and the production logic
agent remain intentionally unavailable until their scheduled phases.

See `docs/REQUIREMENTS_AUDIT.md` and `docs/ARCHITECTURE.md` for the specification
mapping and security boundary.
