# Requirements Audit

Source of truth: `[2526 HK3] IntroAI - Project 2.pdf` (9 pages), visually
reviewed on 2026-08-09. Recommendations from the development prompt are marked
as recommendations, not as course requirements.

## Mandatory course requirements

| ID | Requirement | Rubric | Planned module | Initial owner | Verification |
|---|---|---:|---|---|---|
| R-01 | Python source; main algorithms implemented by the team | General | all | Member A-D | source review; dependency audit |
| R-02 | Playable web or desktop GUI | 4.1 (10) | `gui/`, `game/` | Member D | GUI interaction + integration tests |
| R-03 | Show NxN grid, coordinates, names, professions, statuses, face-up clues, face-down cards | 4.1 | `gui/board_view.py` | Member D | widget/state tests and demo |
| R-04 | Submit CRIMINAL/INNOCENT; accept only entailed verdicts; reveal only after acceptance | 4.1 | `game/game_engine.py`, `agent/` | Member C | engine and integration tests |
| R-05 | Distinguish NOT_PROVABLE and CONTRADICTED; rejected verdict does not mutate state | 4.1 | `core/results.py`, `game/` | Member C | transition tests |
| R-06 | Select revealed clues and highlight referenced/counted cells | 4.1 | `gui/clue_panel.py`, canonical region resolver | Member D | region/GUI tests |
| R-07 | Controls: Load, Restart, Hint, Auto Solve | 4.1 | `gui/controls.py`, `agent/` | Member C/D | GUI/integration tests |
| R-08 | GameEngine owns hidden solution/unrevealed clues; agent receives public state only | 4.1 | `core/public_state.py`, `game/` | Member A/C | privacy/reflection tests |
| R-09 | Deterministic character-to-variable mapping; separate primary/auxiliary variables | 3.1, 4.2 (10) | `logic/variable_manager.py` | Member B | mapping tests |
| R-10 | Support FACT, SAME, DIFFERENT, EXACTLY, AT_LEAST, AT_MOST | 3.2, 4.2 | `core/clue.py`, `logic/` | Member B | semantic and CNF equivalence tests |
| R-11 | Support row, column, 8-neighbor, and distinct explicit-list regions | 2.1, 3.2 | `core/region.py`, `logic/region_resolver.py` | Member A/B | boundary/validation tests |
| R-12 | Implement at least two distinct clue extensions | 3.2 | `logic/extensions.py` | Member B | semantics/CNF/GUI tests |
| R-13 | Reusable automatic CNF; no puzzle-specific formulas; validate inputs; count variables/clauses | 3.3, 4.2 | `logic/cnf_encoder.py` | Member B | exhaustive small-instance equivalence |
| R-14 | KB contains only revealed clues and proved statuses | 2.2, 3.3, 4.2 | `logic/cnf_encoder.py` | Member B/C | privacy and KB-content tests |
| R-15 | Independent direct semantic evaluator for every required clue template | 4.2 | `logic/semantic_evaluator.py` | Member B | evaluator unit tests; no forbidden imports |
| R-16 | Team-built DPLL: propagation, conflict, deterministic branching, backtracking, complete SAT assignment, metrics | 4.3 (10) | `sat/` | Member A | independent SAT/UNSAT tests |
| R-17 | Entailment classification via UNSAT assumptions; UNKNOWN and INCONSISTENT states; never guess | 3.4, 4.4 (20) | `agent/logic_agent.py` | Member C | entailment tests |
| R-18 | Progressive deduction, deterministic forced choice, reveal protocol, trace | 2.2, 4.4 | `agent/`, `game/` | Member C | progressive integration tests |
| R-19 | Separate complete-clue-set uniqueness check | 4.4 | `agent/uniqueness.py` | Member C | unique/non-unique tests |
| R-20 | Experiments on several 3x3 and 4x4 puzzles with required metrics; preserve failures/timeouts | 4.5 (10) | `experiments/` | Member A | reproducible raw JSON outputs |
| R-21 | PDF report with planning, formulation, CNF derivations, algorithms, experiments, limitations, references, AI appendix | 4.6 (30) | final report, `docs/` evidence | Member A-D | report checklist |
| R-22 | 5-10 minute narrated/subtitled demo; Drive link; private-window permission check; no YouTube | 4.7 (10) | demo artifact | Member D | demo checklist |
| R-23 | Group archive named by student IDs; include `Source`, README, requirements, report; no post-deadline edits | Section 5 | release packaging | Member A | clean-room packaging check |
| R-24 | Honest contribution percentages and references; no plagiarism/misconduct | 4.6, Section 6 | project records | Member A-D | team review and Git evidence |

## Must not

- Guess, reveal after a rejected verdict, or infer a verdict from one arbitrary SAT model.
- Expose the hidden solution or unrevealed clue content to the logic agent.
- Hand-write puzzle-specific CNF or replace the required DPLL with a SAT library.
- Treat names, professions, or clue-owner status as logically meaningful unless a clue says so.
- Omit experiment failures/timeouts, fabricate results, fabricate Git history, or conceal AI use.
- Modify the final submission after the deadline.

## Optional or explicitly flexible

- Typical board sizes are 3, 4, or 5; a 5x5 experiment is optional.
- Any correct cardinality encoding is allowed; direct combinational encoding is acceptable.
- Pure-literal elimination and advanced DPLL heuristics are optional.
- Web or desktop GUI is acceptable; natural-language parsing is not required.
- Project organization is flexible if it remains professional and clear.

## Ambiguities and current interpretations

| Topic | Specification status | Conservative interpretation |
|---|---|---|
| Minimum board size | Only typical sizes are stated | Validate square boards; sample/test primarily 3x3 and 4x4 |
| Initially face-up cards | "A few" is not quantified | Require at least one initial public card in playable data |
| Complete-clue truth | Revealed statements are true; valid puzzle has one solution | Loader validates structure only; later validator checks semantics/uniqueness |
| Inconsistent manual verdict response | INCONSISTENT is defined for logic, not GUI wording | Preserve a distinct internal result and show a clear error |
| Hint clue selection details | May identify clue and/or forced character | Logic computes; GUI only displays |
| Extension choice | Examples only | Decide after comparing at least three candidates in Phase 12 |

## Hidden risks

- A public DTO can leak through nested mutable objects even if top-level fields look safe.
- A mock agent can accidentally become fake production reasoning; it must be labeled and replaced.
- GUI region highlighting can diverge from CNF semantics if it reimplements region resolution.
- JSON IDs, display coordinates, and variable order can drift without canonical validation.
- Tkinter availability/display servers vary in CI; business logic tests must remain headless.
- Self-referential Git hashes cannot be stored in the same commit; audit hashes are updated by a later documentation commit.

## Phase 01-04 acceptance map

- Phase 01: importable package tree, README, dependency declaration, audit/log files.
- Phase 02: immutable validated contracts, JSON schema/sample, round-trip/validation/privacy tests.
- Phase 03: loader, restartable engine, mutation-safe public snapshots, public-only agent protocol, transition tests.
- Phase 04: desktop GUI with required board display and manual controls; Hint/Auto Solve visibly deferred, never faked.
