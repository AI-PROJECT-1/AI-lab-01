# Test Log

Only commands actually executed are recorded here.

| Date | Phase | Command | Result | Notes |
|---|---|---|---|---|
| 2026-08-09 | 01 | `python -m compileall -q .` | PASS | Python 3.14.0; package skeleton compiles |
| 2026-08-09 | 01 | `python -m unittest discover -s tests -v` | PASS | Discovery completed; 0 tests expected before Phase 02 |
| 2026-08-09 | 01 | `git diff --check` | PASS | No whitespace errors |
| 2026-08-09 | 02 | `python -m unittest discover -s tests -v` | PASS | 9/9 domain contract tests |
| 2026-08-09 | 02 | `python -m json.tool` on schema and sample | PASS | Both JSON documents parsed |
| 2026-08-09 | 02 | `python -m compileall -q core tests` | PASS | Domain and test modules compile |
| 2026-08-09 | 03 | `python -m unittest discover -s tests -v` | FAIL | 18/19 passed; malformed-JSON test attempted to write to sandbox-denied system temp directory |
| 2026-08-09 | 03 | `python -m unittest discover -s tests -v` | PASS | 20/20 after making malformed-input test filesystem-independent |
| 2026-08-09 | 03 | `python -m compileall -q core agent game tests` | PASS | Engine, loader, agent protocol/mock, and tests compile |
| 2026-08-09 | 03 | `git diff --check` | PASS | No whitespace errors |
| 2026-08-09 | 04 | `python -m unittest discover -s tests -v` | PASS | 25/25 total tests; controller/view-model tests included |
| 2026-08-09 | 04 | `python -m compileall -q .` | PASS | Full repository compiles |
| 2026-08-09 | 04 | Tkinter widget/layout smoke script | PASS | Window title set; 900x640 layout; 6 app children; clean destroy |
| 2026-08-09 | 04 | `git diff --check` | PASS | No whitespace errors |
| 2026-08-12 | Audit | `python -m pytest -q` | FAIL | `pytest` is not installed; this exposed that the old free-function DPLL tests were not covered by the documented `unittest` runner |
| 2026-08-12 | 07 | Direct invocation of old DPLL tests plus 3,500 deterministic random CNFs checked against brute force | PASS | Diagnostic run before converting the tests to `unittest.TestCase` |
| 2026-08-12 | 00-07 | `python -m unittest discover -s tests` | PASS | 65/65 tests, including 13 discoverable DPLL tests, 500 brute-force oracle cases, exhaustive 3x3 clue equivalence, sample truth, and sample uniqueness |
| 2026-08-12 | 00-07 | `python -m compileall -q .` | PASS | Full repository compiles after audit fixes |
| 2026-08-12 | Boundary | `rg` checks for external solvers and forbidden game/hidden imports | PASS | No production external SAT library or forbidden boundary import found in `agent`, `logic`, or `sat` |
| 2026-08-12 | 04 | Tkinter application smoke script | PASS | `GriductiveApp` initialized and destroyed cleanly; requested size 649x568 |
| 2026-08-12 | Audit | `git diff --check` | PASS | No whitespace errors; Git only reported expected LF-to-CRLF conversion warnings |
| 2026-08-12 | 08-13 | `python -m unittest discover -s tests` | PASS | 77/77 tests; includes entailment, progressive deduction, trace, uniqueness, extensions, highlights, and four-puzzle validation |
| 2026-08-12 | 12-13 | `python -m json.tool` on every `puzzles/*.json` | PASS | Schema and all four distributable puzzles parse as valid JSON |
| 2026-08-12 | 08-13 | `python -m compileall -q .` | PASS | Full repository compiles after Phase 08-13 implementation |
| 2026-08-12 | Boundary | external-solver and forbidden-import scan | PASS | No external SAT solver; `agent`, `logic`, and `sat` do not import `game`, `Puzzle`, or hidden solution data |
| 2026-08-12 | 10-11 | Tkinter Hint + clue highlight + Auto Solve smoke test | PASS | Default puzzle reached COMPLETE; 9 trace entries displayed; FACT target highlighted; clean shutdown |
| 2026-08-12 | 08-13 | `git diff --check` | PASS | No whitespace errors; line-ending conversion warnings only |
| 2026-08-12 | Pre-UI checkpoint | `python -m unittest discover -s tests` | PASS | 77/77 tests before any GUI refactor; exact Phase 08-13 state preserved in `03584c3` |
| 2026-08-12 | Pre-UI checkpoint | external-solver and forbidden-import scan | PASS | Boundary remained clean immediately before checkpoint `03584c3` |
| 2026-08-12 | UI Phase 1 | `python -m unittest discover -s tests` | PASS | 80/80 tests: original 77 plus 3 visual-foundation contract tests |
| 2026-08-12 | UI Phase 1 | `python -m compileall -q .` | PASS | Full repository compiles; no non-GUI runtime dependency added |
| 2026-08-12 | UI Phase 1 | external-solver and forbidden-import scan | PASS | No AI/game boundary change introduced by presentation refactor |
| 2026-08-12 | UI Phase 1 | Tkinter 3x3/4x4 interaction and layout smoke script | PASS | Both requested 935x742 within 1180x800; 3x3 Hint/Solve Next and 4x4 Hint/Auto Solve passed; trace retained |
| 2026-08-12 | UI Phase 1 | `git diff --check` | PASS | No whitespace errors; line-ending conversion warnings only |
| 2026-08-12 | UI Phase 2 | `python -m pytest -q` | UNAVAILABLE | Command executed as requested; environment reports `No module named pytest`; no new external test dependency was added |
| 2026-08-12 | UI Phase 2 | `python -m unittest discover -s tests` | PASS | 87/87 tests, including unresolved-data exclusion, textual verdicts, public clue timing, preview bounds, deterministic avatars, and visual-state composition |
| 2026-08-12 | UI Phase 2 | `python -m compileall -q .` | PASS | Full repository compiles after CharacterCard refactor |
| 2026-08-12 | UI Phase 2 | boundary and external SAT solver scans | PASS | No hidden/Puzzle/GameEngine import entered agent/logic/sat and no external SAT dependency was found |
| 2026-08-12 | UI Phase 2 | protected-module diff from `f6b5713` | PASS | No changes in `agent/`, `game/`, `core/`, `logic/`, `sat/`, or `puzzles/` |
| 2026-08-12 | UI Phase 2 | Tkinter 3x3 state-composition smoke | PASS | 9 cards; selected B2 remained unresolved; highlighted C1 remained Criminal; B1 remained Innocent; all card and clue widgets stayed within bounds |
| 2026-08-12 | UI Phase 2 | Tkinter completed 4x4 smoke | PASS | 16 revealed cards; longest current name/profession rendered; every textual badge and compact public clue preview stayed within card/board bounds |
| 2026-08-12 | UI Phase 2 | DPI-aware visual inspection | PASS | Inspected unresolved, mixed, selected, Criminal, Innocent, clue-highlighted, and completed 4x4 states; coordinate omission found and corrected; clipped 4x4 preview found and corrected |
| 2026-08-12 | UI Phase 2 | `git diff --check` | PASS | No whitespace errors; line-ending conversion warnings only |
