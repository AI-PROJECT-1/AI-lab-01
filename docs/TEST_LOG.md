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
| 2026-08-12 | UI Phase 3 | `python -m pytest -q` | UNAVAILABLE | Environment still reports `No module named pytest`; no dependency was added |
| 2026-08-12 | UI Phase 3 | `python -m unittest discover -s tests` | PASS | 96/96 tests; 9 Phase 3 tests cover contextual enablement, selection immutability, accepted reveal, all rejected outcomes, safe feedback, resets/stale submission, and presentation-only emphasis |
| 2026-08-12 | UI Phase 3 | `python -m compileall -q .` | PASS | Full repository compiles after contextual verdict refactor |
| 2026-08-12 | UI Phase 3 | boundary and external SAT solver scans | PASS | Feedback/context code consumes only existing result contracts and public presentation data; no forbidden production imports or external solver dependency found |
| 2026-08-12 | UI Phase 3 | protected-module diff from `48bea9d` | PASS | No changes in `agent/`, `game/`, `core/`, `logic/`, `sat/`, or `puzzles/` |
| 2026-08-12 | UI Phase 3 | Tkinter 3x3 verdict/reset smoke | PASS | Disabled without selection; selected identity enabled actions; NOT_PROVABLE and CONTRADICTED preserved state; ACCEPTED revealed B1/CL-02; Restart and Load cleared transient state |
| 2026-08-12 | UI Phase 3 | Tkinter 4x4 responsive smoke | PASS | 16 cards; accepted B1 emphasis and feedback rendered; verdict controls disabled after reveal; every board descendant remained within bounds |
| 2026-08-12 | UI Phase 3 | DPI-aware visual inspection | PASS | Inspected no-selection, selected, contradicted, accepted 3x3, and accepted 4x4 views; corrected clipped context and compact status/clue presentation |
| 2026-08-12 | UI Phase 3 | `git diff --check` | PASS | No whitespace errors; line-ending conversion warnings only |
| 2026-08-13 | UI Phase 4 | `python -m pytest -q` | UNAVAILABLE | Environment reports `No module named pytest`; no external test dependency was added |
| 2026-08-13 | UI Phase 4 | `python -m unittest discover -s tests` | PASS | 105/105 tests; 9 new tests cover public-only views, full text/owner/ID, clue state composition, canonical clue/region families, character-state composition, and reset/load selection clearing |
| 2026-08-13 | UI Phase 4 | `python -m compileall -q .` | PASS | Full repository compiles after ClueCard refactor |
| 2026-08-13 | UI Phase 4 | boundary and external SAT solver scans | PASS | Clue presentation iterates public reveals only; canonical resolver remains the sole cell-reference path; no forbidden import or external solver dependency found |
| 2026-08-13 | UI Phase 4 | protected-module diff from `bd39263` | PASS | No changes in `agent/`, `game/`, `core/`, `logic/`, `sat/`, or `puzzles/` |
| 2026-08-13 | UI Phase 4 | Tkinter 3x3 clue interaction smoke | PASS | Initial/selected/new/multiple clues rendered; selected character and canonical clue highlight coexisted; revealed Innocent and Criminal highlight identities remained visible |
| 2026-08-13 | UI Phase 4 | Tkinter 4x4 scrolling smoke | PASS | All 16 public clue cards rendered; overflow scroll enabled and auto-scrolled to newly emphasized D4; board descendants remained within bounds |
| 2026-08-13 | UI Phase 4 | DPI-aware visual inspection | PASS | Inspected empty, one/several, selected, long, newly revealed, Criminal/ Innocent highlighted, and scrolling 4x4 states; corrected fixed-width wrapping |
| 2026-08-13 | UI Phase 4 | `git diff --check` | PASS | No whitespace errors; line-ending conversion warnings only |
| 2026-08-13 | UI Phase 5 | `python -m pytest -q` | UNAVAILABLE | Environment reports `No module named pytest`; no package was installed |
| 2026-08-13 | UI Phase 5 | `python -m unittest discover -s tests` | PASS | 117/117 tests; 12 new tests cover call/trace counts, public filtering, no causal/hidden wording, cached target, fingerprint invalidation, selection stability, and modifier composition |
| 2026-08-13 | UI Phase 5 | `python -m compileall -q .` | PASS | Full repository compiles after progressive Hint presentation refactor |
| 2026-08-13 | UI Phase 5 | boundary and external SAT solver scans | PASS | Hint cache contains public identifiers/fingerprint only; no protected boundary change or external solver dependency found |
| 2026-08-13 | UI Phase 5 | protected-module diff from `dff07f0` | PASS | No changes in `agent/`, `game/`, `core/`, `logic/`, `sat/`, or `puzzles/` |
| 2026-08-13 | UI Phase 5 | Tkinter 3x3 progressive Hint smoke | PASS | Stage 1 called reasoning once; Stage 2 kept trace count unchanged and did not reveal B1; manual ACCEPTED, Solve Next, Restart, and Load cleared Hint state |
| 2026-08-13 | UI Phase 5 | Tkinter 4x4 Auto Solve smoke | PASS | Hint session cleared on Auto Solve/reveal lifecycle; completed 16-card board had no stale clue/target Hint modifier |
| 2026-08-13 | UI Phase 5 | DPI-aware visual inspection | PASS | Inspected pre-Hint, one/multiple/no-anchor Stage 1, Stage 2, manual accepted, Solve Next, Auto Solve, Restart, and Load states |
| 2026-08-13 | UI Phase 5 | `git diff --check` | PASS | No whitespace errors; line-ending conversion warnings only |
| 2026-08-13 | UI Phase 6 | `python -m pytest -q` | UNAVAILABLE | Environment reports `No module named pytest`; no package was installed |
| 2026-08-13 | UI Phase 6 | `python -m unittest discover -s tests` | PASS | 135/135 tests; 18 new tests cover default visibility, state immutability, exact trace fields, query metrics, Hint call counts, manual/solver source labels, progressive steps, reset/load behavior, and private-data exclusion |
| 2026-08-13 | UI Phase 6 | `python -m compileall -q .` | PASS | Full repository compiles after structured Solver Details refactor |
| 2026-08-13 | UI Phase 6 | boundary and external SAT solver scans | PASS | No production external solver; agent/logic/sat boundary clean; Solver Details contains no Puzzle, hidden solution/status, private engine, or unrevealed lookup |
| 2026-08-13 | UI Phase 6 | protected-module diff from `d2682b3` | PASS | No changes in `agent/`, `game/`, `core/`, `logic/`, `sat/`, or `puzzles/` |
| 2026-08-13 | UI Phase 6 | Tkinter 3x3 Solver Details smoke and DPI-aware visual review | PASS | Details closed by default; empty, Hint, Solve Next, multi-step Auto Solve, long active-clue/query, open Restart, and source-label states rendered; Hint Stage 2 kept one trace step |
| 2026-08-13 | UI Phase 6 | Tkinter 4x4 responsive smoke and DPI-aware visual review | PASS | 1180x800 board-first layout retained full controls; opening details preserved board/game state; Load while open reset stale trace/source presentation and left Auto Solve cancelled |
| 2026-08-13 | UI Phase 6 | low-height 1180x660 Tkinter boundary measurement | PASS | Board, Revealed Clues, controls, and feedback remained inside the window; maximum checked bottom edge was 625/660 px |
| 2026-08-13 | UI Phase 6 | `git diff --check` | PASS | No whitespace errors; line-ending conversion warnings only |
| 2026-08-16 | Phase 6.5 | `python -m pytest -q` | UNAVAILABLE | Environment reports `No module named pytest`; no package was installed |
| 2026-08-16 | Phase 6.5 | `python -m unittest discover -s tests` | PASS | 155/155 tests; 20 new support tests cover one/two-clue support, irrelevant deletion, proved-verdict units, determinism, same verdict, irreducibility, baseline failure, privacy, trace isolation, fallback, Stage 1/2, modifier composition, fingerprint and lifecycle invalidation |
| 2026-08-16 | Phase 6.5 | `python -m compileall -q .` | PASS | Full repository compiles with shared pure entailment and Hint support modules |
| 2026-08-16 | Phase 6.5 | 25-run fresh-engine Hint timing harness | PASS | 3x3 median Hint 0.000223900s, extraction 0.000138700s (range 0.000135700-0.000414100s); 4x4 median Hint 0.000276600s, extraction 0.000173200s (range 0.000162200-0.000230600s); 9 extraction SAT calls in both initial states |
| 2026-08-16 | Phase 6.5 | public-boundary, forbidden-hidden/import, external SAT solver scans | PASS | New agent modules import only public state/structured DTOs and existing CNF/DPLL infrastructure; no Puzzle, GameEngine, hidden status/solution, unrevealed lookup, or external solver dependency |
| 2026-08-16 | Phase 6.5 | expected logic diff from `5673fe0` | PASS | Approved changes limited to `agent/deduction_trace.py`, `agent/logic_agent.py`, new `agent/entailment.py`, and new `agent/hint_explanation.py`; no change to still-protected files |
| 2026-08-16 | Phase 6.5 | Tkinter 3x3 DPI-aware visual review | PASS | Single clue, two-clue support, clue plus public known verdict, Stage 2 target-only, forced diagnostic fallback, and stale-support Restart states rendered correctly |
| 2026-08-16 | Phase 6.5 | Tkinter 4x4 DPI-aware visual review | PASS | Two supporting clue cards in a 10-clue scrolling panel, real extension clue plus solved character, Stage 2 target-only, and Auto Solve/Restart clearing passed at 1180x800; checked bottom edge 755/800 px |
| 2026-08-16 | Phase 6.5 | `git diff --check` | PASS | No whitespace errors; line-ending conversion warnings only |
| 2026-08-16 | UI Phase 7 | `python -m pytest -q` | UNAVAILABLE | Environment reports `No module named pytest`; no package was installed |
| 2026-08-16 | UI Phase 7 | `python -m unittest discover -s tests` | PASS | 174/174 tests; 19 new tests cover unresolved/revealed card routing, exact public clue mapping, canonical references, no solver/Hint/submission calls, public completion copy/source, final manual/Solve Next/Auto completion, completed controls, Hint reset, board/details/clue availability, Restart/Load cleanup, and stale Auto callback rejection |
| 2026-08-16 | UI Phase 7 | `python -m compileall -q .` | PASS | Full repository compiles after completion and public card-activation presentation work |
| 2026-08-16 | UI Phase 7 | protected-module diff from `ba7912b` | PASS | No changes in `sat/`, `logic/`, `agent/`, `game/`, `core/`, or `puzzles/` |
| 2026-08-16 | UI Phase 7 | external-solver, GUI hidden-data, and production-title scans | PASS | No external SAT solver reference; no GUI hidden solution/status/private-puzzle lookup; no Capture/Smoke/Debug/Test Harness production title; window title is `Griductive` |
| 2026-08-16 | UI Phase 7 | Tkinter 3x3 gameplay/completion smoke and visual review | PASS | Initial state, unresolved selection, solved-card public clue spotlight, canonical highlight, grounded Hint Stage 1, target Stage 2, final manual verdict, completion, Solver Details, Restart, and Load were exercised without reopening the app |
| 2026-08-16 | UI Phase 7 | Tkinter 4x4 scrolling/solver/completion smoke and visual review | PASS | Partial board, solved-card clue auto-scroll/spotlight, Hint, Solve Next, non-blocking Auto Solve completion, completed board, and Solver Details remained coherent and inspectable |
| 2026-08-16 | UI Phase 7 | 1180x660 completion boundary review | PASS | Completion banner stayed textual and compact; all 9 completed 3x3 cards retained visible CRIMINAL/INNOCENT badges; maximum checked bottom edge was 625/660 px |
| 2026-08-16 | UI Phase 7 | `git diff --check` | PASS | No whitespace errors; line-ending conversion warnings only |
| 2026-08-16 | UI Phase 8 | `python -m unittest discover -s tests` | PASS | 179/179 tests; 5 new final-audit tests cover experiment schema/CLI, all distributable puzzle metrics, complete-state terminal behavior, explicit non-uniqueness, and shipped extension use |
| 2026-08-16 | UI Phase 8 | `python -m pytest -q` | UNAVAILABLE | Environment reports `No module named pytest`; supported standard-library runner passed and no package was installed |
| 2026-08-16 | UI Phase 8 | `python -m experiments.run_experiments` | PASS | 4/4 puzzles (2x 3x3, 2x 4x4), 0 failures/timeouts; all complete without guesses and all complete clue sets are consistent/unique; raw JSON retained |
| 2026-08-16 | UI Phase 8 | complete-state/no-repeat and explicit non-unique audit | PASS | Completed public state returns no classifications, no Solve Next target, and no new trace; separate underconstrained complete-clue state is detected non-unique |
| 2026-08-16 | UI Phase 8 | `python -m compileall -q .` and `git diff --check` | PASS | Repository compiles; no whitespace errors at audit point |
| 2026-08-16 | UI Phase 8 | boundary/external-solver/production-string scan | PASS | No external SAT dependency, GUI/agent hidden-data access, puzzle-specific formula, or production debug/test-harness title; legitimate internal trace capture and labeled MockLogicAgent test double remain |
| 2026-08-16 | UI Phase 8 | clean `python main.py` entrypoint | PASS | Process remained live after startup and exposed window title `Griductive` (PID 7892 stopped after verification) |
| 2026-08-16 | UI Phase 8 | continuous 3x3/4x4 Tkinter E2E and visual review | PASS | 18 states covered all verdict outcomes, public clue inspection/highlight, grounded Hint, Solve Next, Solver Details, Auto completion, Restart/Load, 4x4 scrolling and completion; no debug metadata/clipping observed |
| 2026-08-16 | UI Phase 8 | 1180x660 responsive boundary measurement | PASS | All 16 4x4 textual verdict badges visible and maximum checked content bottom was 625/660 px |
| 2026-08-16 | UI Phase 8 | `git fetch --all --prune` and branch audit | PASS | Fetch succeeded; local `main` is ahead of `origin/main` by 9 and behind by 0; no push/upload claimed |
| 2026-08-16 | Phase 8.5 | Phase 8 checkpoint and worktree audit | PASS | Verified real checkpoint `2c8ed1bd2f6edcdddd6583355110ccdd00470a6d`; Phase 8.5 remains uncommitted as required; local `main` is ahead of `origin/main` by 10 |
| 2026-08-16 | Phase 8.5 | `python -m unittest discover -s tests` | PASS | 196/196 tests; final repeat 7.496s (earlier full run 7.989s); includes six-puzzle validity/quality plus 11 navigation and state-boundary tests |
| 2026-08-16 | Phase 8.5 | `python -m pytest -q` | UNAVAILABLE | Environment reports `No module named pytest`; no package was installed; supported standard-library suite passed |
| 2026-08-16 | Phase 8.5 | `python -m experiments.analyze_puzzles --output experiments/results/puzzle_quality.json` | PASS | 6/6 shipped puzzles unique, consistent, progressively solvable; exact public support sequence retained; 0 failures |
| 2026-08-16 | Phase 8.5 | `python -m experiments.run_experiments --output experiments/results/final_regression.json` | PASS | 6/6 puzzles, 0 failures/timeouts; raw solver/runtime/quality data regenerated from baseline `2c8ed1b` |
| 2026-08-16 | Phase 8.5 | Standard/Advanced performance audit | PASS | Standard solve 0.001696s, median support 0.000373s, 0 decisions/0 backtracks; Advanced solve 0.012332s, median support 0.002301s, 17 decisions/1 backtrack |
| 2026-08-16 | Phase 8.5 | `python -m compileall -q agent core experiments game gui logic sat tests` | PASS | All production, experiment, and test modules compile under Python 3.14.0 |
| 2026-08-16 | Phase 8.5 | protected-module diff and boundary scans | PASS | No diff in `agent/core/game/logic/sat`; no external solver, GUI hidden solution, forbidden boundary import, puzzle-specific CNF, or hard-coded Hint support found |
| 2026-08-16 | Phase 8.5 | `git diff --check` | PASS | No whitespace errors; Git emitted line-ending conversion warnings only |
| 2026-08-16 | Phase 8.5 | DPI-aware Tkinter Tutorial/Standard/Advanced/Puzzle Select review | PASS | 21 captures at 1180x800/1180x660; catalog scroll/current badge, verdict outcomes, canonical highlights, Stage 1/2 Hint, Solver Details, Auto completion, and Back state preservation passed |
| 2026-08-16 | Phase 8.5 | Standard and Advanced continuous E2E | PASS | Standard manual verdict/reveal/Hint/Solve Next/Auto/completion/navigation passed; Advanced real support `A4-01` + `A4-04` + public `A1`, region inspection, Hint stages, Solver Details, Auto and completion passed |
| 2026-08-16 | Phase 8.5 | clean `python main.py` entrypoint | PASS | Current-code process remained live and exposed window title `Griductive`; exact smoke PID 17992 was stopped after verification |
| 2026-08-18 | Phase 8.5 revalidation | `python -m unittest discover -s tests` | PASS | Repeated unchanged Phase 8.5 worktree: 196/196 tests in 8.012s; CLI fixture observed all six puzzles with zero failures |
| 2026-08-18 | Phase 8.5 revalidation | compile, JSON, protected-module, boundary and `git diff --check` scans | PASS | Compile passed; 7/7 puzzle JSON files parsed; Phase 8 protected diff stayed empty; no external solver, hidden GUI access, forbidden import, puzzle-specific CNF/Hint, or whitespace error found |
| 2026-08-18 | Phase 8.5 revalidation | existing raw experiment result audit | PASS | `final_regression.json` and `puzzle_quality.json` still contain 6/6 PASS and zero quality/regression failures; generated outputs were not rewritten because production/puzzle code was unchanged |
| 2026-08-18 | Phase 8.6 checkpoint | Git history and clean separation | PASS | Verified real Phase 8.5 commit `8c8c77d326ceb65beaa7b5454bc0bcd49f9da355`; worktree was clean; local `main` was 11 ahead/0 behind origin; Phase 8.6 remains uncommitted |
| 2026-08-18 | Phase 8.6 | `python -m unittest discover -s tests` | PASS | 212/212 tests in 7.146s; 16 new hardening tests plus updated fixture/catalog/verdict expectations |
| 2026-08-18 | Phase 8.6 | `python -m pytest -q` | UNAVAILABLE | `No module named pytest`; no package was installed; supported standard-library suite passed |
| 2026-08-18 | Phase 8.6 | production puzzle quality runner | PASS | 2/2 catalog puzzles; 0 FACT/direct-answer IDs; 20/20 steps support >=2; both consistent, unique, progressive; actual target/owner sequences retained |
| 2026-08-18 | Phase 8.6 | production experiment runner | PASS | 2/2 PASS, zero failures; baseline `8c8c77d`; Standard 34 calls/6 decisions/208 propagations/0 backtracks, Advanced 66/92/804/1 |
| 2026-08-18 | Phase 8.6 | manual-lock functional tests | PASS | CONTRADICTED/no-mutation/lock/retry block, NOT_PROVABLE/ACCEPTED/INCONSISTENT no-lock, Restart/Load/switch reset, neutral presentation, Hint/Solve/Auto compatibility |
| 2026-08-18 | Phase 8.6 | `python -m compileall -q agent core experiments game gui logic sat tests` | PASS | All production, experiment, and test modules compile under Python 3.14.0 |
| 2026-08-18 | Phase 8.6 | protected-module diff | PASS | Empty diff from `8c8c77d` for `core/`, `game/`, `agent/`, `logic/`, and `sat/`; LogicAgent/GameEngine/CNF/DPLL/Hint/uniqueness unchanged |
| 2026-08-18 | Phase 8.6 | source and boundary scans | PASS | No external SAT imports, GUI/agent hidden access, forbidden upward imports, puzzle-specific reasoning, random runtime selection, lock in protected layers, or coordinate verdict literals |
| 2026-08-18 | Phase 8.6 | JSON and production-manifest scan | PASS | 3 production JSON files parse (2 puzzles plus schema); 4 legacy fixture JSON files parse; experiments consume only the two catalog puzzles |
| 2026-08-18 | Phase 8.6 | 12-state Tkinter visual E2E | PASS | Catalog/Standard/Advanced, manual lock, grounded Hint, Solve Next, Solver Details, Auto completion at 1180x800 and 1180x660; max checked bottom 652/660; 12 temporary captures removed after inspection |
| 2026-08-18 | Phase 8.6 | clean `python main.py` entrypoint | PASS | Process remained live with title `Griductive`; exact smoke PID 15304 was stopped after verification |
| 2026-08-18 | Phase 8.6 | `git diff --check` | PASS | No whitespace errors; line-ending conversion warnings only |
