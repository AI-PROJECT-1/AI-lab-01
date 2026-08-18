# Final Requirements Audit

Source of truth: `[2526 HK3] IntroAI - Project 2 (1).pdf`, all 9 pages
textually and visually reviewed on 2026-08-16. Statuses describe repository
evidence, not intended future work.

## Mandatory requirement matrix

| ID | Requirement | Project section | Implementation files | Tests | Status | Evidence | Notes / limitation |
|---|---|---|---|---|---|---|---|
| R-01 | Python source; main algorithms implemented by the team | General | `main.py`, `logic/`, `sat/`, `agent/` | dependency/boundary scan, 179-test suite | PASS | Standard-library implementation; no external SAT package | Team must review authorship records before submission |
| R-02 | Playable desktop or web GUI | 4.1 | `gui/app.py`, `gui/board_view.py`, `gui/puzzle_select.py`, `main.py` | GUI/navigation/E2E smoke | PASS | Clean launch plus same-root Game/Puzzle Select navigation | Desktop display and Tkinter are required |
| R-03 | NxN board, coordinates, public identity/status, face-up clues and face-down cards | 4.1 | `gui/board_view.py`, `gui/character_card.py`, `gui/clue_panel.py` | GUI/card/clue/completion tests | PASS | Tutorial/Standard/Advanced visual audit; all 16 low-height status badges visible | No external portraits are required |
| R-04 | Submit CRIMINAL/INNOCENT; accept only entailed verdicts; reveal after acceptance | 4.1 | `game/game_engine.py`, `gui/verdict_panel.py`, `agent/logic_agent.py` | verdict and engine tests | PASS | ACCEPTED alone mutates public state through `GameEngine` | GUI never compares against hidden status |
| R-05 | Distinct NOT_PROVABLE and CONTRADICTED; rejected submissions do not mutate | 4.1 | `core/results.py`, `game/game_engine.py`, `gui/feedback.py` | verdict interaction tests | PASS | Both rejection paths preserve public snapshot; INCONSISTENT is distinct | Feedback uses public/result contracts only |
| R-06 | Select a revealed clue and highlight referenced/counted cells | 4.1 | `gui/clue_panel.py`, `gui/controller.py`, `logic/region_resolver.py` | clue presentation and E2E tests | PASS | Canonical resolver drives explicit, row, column, and neighbor highlights | Standard/Advanced shipped data visibly exercises real regions |
| R-07 | Load, Restart, Hint, Auto Solve controls | 4.1 | `gui/app.py`, `gui/controls.py`, `gui/puzzle_select.py`, `game/game_engine.py` | lifecycle, navigation, Hint, completion tests | PASS | E2E covered Puzzles/Back/Play, external Load, Restart, Hint, Solve Next, Auto Solve | Puzzle navigation is UI-only; Solve Next/Solver Details are additional affordances |
| R-08 | Engine owns hidden data; agent sees immutable public state only | 4.1 | `core/public_state.py`, `game/game_engine.py`, `agent/logic_agent.py` | privacy/reflection/source scans | PASS | Public DTO has no solution/unrevealed fields; GUI/agent scans are clean | Loader/domain objects legitimately retain authoritative hidden data |
| R-09 | Deterministic primary mapping and auxiliary separation | 3.1, 4.2 | `logic/cnf_encoder.py` | mapping/CNF tests | PASS | Row-major IDs; reports separate primary/auxiliary counts | Current direct encoding uses zero auxiliary variables |
| R-10 | FACT, SAME, DIFFERENT, EXACTLY, AT_LEAST, AT_MOST | 3.2, 4.2 | `core/clue.py`, `logic/cnf_encoder.py`, `logic/semantic_evaluator.py` | exhaustive semantics/CNF and puzzle-quality tests | PASS | All six templates have independent evaluator/CNF coverage and occur in shipped Tutorial/Standard/Advanced data | FACT remains late/non-progressive in deduction-focused puzzles |
| R-11 | ROW, COLUMN, 8-NEIGHBORS excluding self, and EXPLICIT regions | 2.1, 3.2 | `core/region.py`, `logic/region_resolver.py` | edge/corner/interior/explicit plus puzzle-quality tests | PASS | One canonical resolver is reused by CNF, evaluator, GUI, and real Advanced data | Advanced visibly uses all four region families |
| R-12 | At least two distinct clue extensions | 3.2 | `core/clue.py`, `logic/cnf_encoder.py`, `logic/semantic_evaluator.py` | extension equivalence/puzzle tests | PASS | `IMPLIES` and `ODD` are both implemented and used in 3x3 and 4x4 puzzle files | Both participate in real progressive solves |
| R-13 | Automatic reusable CNF, validation, variable/clause counts | 3.3, 4.2 | `logic/cnf_encoder.py` | exhaustive small-instance equivalence | PASS | No puzzle-specific formula; experiment JSON records counts | Direct combinational cardinality can grow quickly on larger boards |
| R-14 | Public KB contains revealed clues and proved verdict units only | 2.2, 3.3, 4.2 | `logic/cnf_encoder.py`, `core/public_state.py` | KB/privacy tests | PASS | Encoder input is public snapshot only | Hidden solution is not an encoder input |
| R-15 | Independent direct semantic evaluator | 4.2 | `logic/semantic_evaluator.py` | evaluator truth-table tests | PASS | All core and extension types checked independently of CNF | Evaluator is validation/test infrastructure, not the solver |
| R-16 | Team DPLL: propagation, conflicts, branching, backtracking, assignment, metrics | 4.3 | `sat/dpll.py`, `sat/sat_result.py`, `sat/statistics.py` | SAT/UNSAT plus 500 brute-force-oracle cases | PASS | Deterministic first-unassigned search and per-call statistics | Shipped progressive chains solve by propagation, so experiment decisions/backtracks are zero; dedicated tests exercise both |
| R-17 | Entailment via UNSAT assumptions; four states; no guessing | 3.4, 4.4 | `agent/entailment.py`, `agent/logic_agent.py` | classification/entailment tests | PASS | Both opposite assumptions are queried; UNKNOWN and INCONSISTENT are explicit | A single satisfying model is never treated as proof |
| R-18 | Progressive deterministic deductions, reveal protocol, and trace | 2.2, 4.4 | `agent/logic_agent.py`, `agent/deduction_trace.py`, `game/game_engine.py` | agent/game/completion tests | PASS | Row-major forced choice; trace records exact SAT queries and public reveals | Solver Details reports per-query, not invented cumulative, evidence |
| R-19 | Separate complete-clue-set uniqueness check | 4.4 | `agent/uniqueness.py` | unique and non-unique tests | PASS | Primary-model blocking plus a second SAT call; separate from public play KB | Complete clue set is used only for validation |
| R-20 | Several 3x3/4x4 experiments with counts, SAT work, runtime, reveal waves, failures retained | 4.5 | `experiments/run_experiments.py`, `experiments/analyze_puzzles.py`, raw result JSON | experiment/final/puzzle-quality tests | PASS | Six puzzles, 0 failures; real support profiles and raw metrics retained reproducibly | Runtime is machine-specific; no optional 5x5 experiment |
| R-21 | PDF report covering formulation, CNF, algorithms, experiments, limitations, references, AI appendix | 4.6 | `docs/REPORT_SUPPORT.md`, audit/log documents | documentation audit | PARTIAL | Required technical material and real measurements are prepared | Final `Report.pdf`, references review, layout and team approval remain outside Phase 8 |
| R-22 | 5-10 minute narrated/subtitled demo, Drive link, permission check, no YouTube | 4.7 | `docs/DEMO_SCRIPT.md` | deterministic E2E rehearsal | PARTIAL | Timed script and verified interaction path exist | Video, narration/subtitles, hosted Drive link and incognito permission check remain |
| R-23 | Student-ID archive containing Source, README, requirements, report; deadline integrity | Section 5 | `README.md`, `requirements.txt`, source tree | clean-entrypoint/git audit | PARTIAL | Source/run/test paths are ready | Student-ID filename, final PDF, clean archive and deadline freeze remain; Phase 8 intentionally did not package |
| R-24 | Honest contributions, references, no plagiarism/misconduct | 4.6, Section 6 | `docs/TASK_DISTRIBUTION.md`, `docs/AI_USAGE_LOG.md`, Git history | history/audit review | BLOCKED | AI and commit history are recorded without fabricated hashes | Real names/IDs, ownership confirmation, percentages and final reference review require team input |

## Gameplay checklist and exact evidence

| Capability | Exact evidence | Status |
|---|---|---|
| NxN/coordinates/names/professions/public status/face state | `test_cards_show_public_metadata_and_face_state`; 3x3/4x4 E2E | PASS |
| CRIMINAL and INNOCENT manual actions | `test_manual_selection_and_verdict_flow`; deterministic E2E submitted both | PASS |
| ACCEPTED and exact reveal | `test_accepted_uses_engine_api_and_reveals_exact_public_clue` | PASS |
| NOT_PROVABLE without reveal | `test_not_provable_preserves_public_state`; 3x3 C1 CRIMINAL E2E | PASS |
| CONTRADICTED without reveal | `test_contradicted_preserves_state_and_reports_only_opposite`; 3x3 B1 CRIMINAL E2E | PASS |
| INCONSISTENT handling | `test_inconsistent_does_not_reveal_and_has_error_feedback` | PASS |
| Clue selection and canonical highlight | `test_canonical_clue_highlighting`; `test_revealed_click_selects_exact_public_owner_clue_and_canonical_cells` | PASS |
| Load and Restart | `test_restart_and_load_clear_selection_and_prevent_stale_submission`; completion lifecycle tests | PASS |
| Puzzles / Back / Play navigation | `tests/test_puzzle_navigation.py`; same-state Back and lifecycle-safe Play E2E | PASS |
| Hint Stage 1/2 | `test_stage_one_prefers_support_and_omits_irrelevant_active_clue`; `test_stage_two_remains_target_only_and_does_not_request_again` | PASS |
| Solve Next and Auto Solve | `test_progressive_controls_use_real_agent`; `test_auto_solve_stops_on_final_reveal_without_extra_step` | PASS |
| Completion through all final actions | `test_final_manual_accepted_verdict_triggers_completion`, `test_final_solve_next_step_triggers_completion`, Auto test above | PASS |

## Clue, region, and extension evidence

| Type / region | Model and evaluator | Automatic CNF | Test and representative data | Status |
|---|---|---|---|---|
| FACT | `core/clue.py`, `logic/semantic_evaluator.py` | unit clause in `logic/cnf_encoder.py` | `test_fact_clue`; every shipped puzzle | PASS |
| SAME | same shared files | bidirectional equivalence clauses | `test_same_clue`; both extension puzzles | PASS |
| DIFFERENT | same shared files | two exclusive-value clauses | `test_different_clue`; extension puzzles | PASS |
| EXACTLY | structured `k` + canonical region | AT_LEAST + AT_MOST | row tests; Standard/Advanced production clues | PASS |
| AT_LEAST | structured `k` + canonical region | direct positive subset clauses | tests; Standard/Advanced production clues | PASS |
| AT_MOST | structured `k` + canonical region | direct negative subset clauses | tests; Advanced column/neighbor clues | PASS |
| ROW | `RegionResolver.referenced_cells` | same resolver used by encoder | boundary tests; Standard/Advanced visual highlights | PASS |
| COLUMN | same canonical resolver | same resolver used by encoder | tests; Standard/Advanced shipped clues | PASS |
| NEIGHBORS | excludes owner; clips at board boundary | same resolver used by encoder | boundary tests; Advanced A4-neighbor clue | PASS |
| EXPLICIT | duplicate/reference validation | exact listed variables | explicit-region/clue tests; shipped puzzle data | PASS |
| Extension 1: IMPLIES | enum/model/parser + direct implication semantics | `(not antecedent or consequent)` | exhaustive 512-assignment equivalence; both extension puzzles | PASS |
| Extension 2: ODD | enum/model/parser + direct parity semantics | blocks every even assignment | exhaustive 512-assignment equivalence; both extension puzzles | PASS |

Shipped Standard/Advanced data now demonstrates all core clue families and all
region families across the catalog. Exhaustive/boundary tests remain the source
of complete combinational coverage; production presence is not treated as a
substitute for semantic/CNF verification.

## Final gameplay and reasoning checks

- Required controls and verdict outcomes are reachable without hidden-state
  access. ACCEPTED refreshes the public snapshot and reveals exactly one clue;
  all rejection/error outcomes leave it unchanged.
- Hint Stage 1 displays a deterministic deletion-irreducible support extracted
  from public clues and proved public verdicts. It does not claim unique or
  globally minimum proof causality. Stage 2 reuses the cached target and makes
  no second reasoning request.
- Solve Next and Auto Solve repeatedly rebuild from the newly public state,
  stop on completion, and do not repeat a resolved target. The completed-state
  audit confirms `classify_all == {}`, `solve_next is None`, and an empty new
  trace.
- Solver Details preserves structured query purpose, assumptions, SAT result,
  decisions, propagations, backtracks, runtime, and public reveal ID. It does
  not invent clause-level proofs or final hidden assignments.
- The 6-puzzle suite contains three 3x3 and three 4x4 puzzles. All six are
  consistent, unique, progressively solvable without guesses, and complete.
  Standard has average/max support 2/2; Advanced has 2.308/4 and begins with
  two real supporting clues plus one public verdict.

## Blocker classification

- **No implementation blocker:** gameplay, public/private isolation, clue/CNF,
  DPLL, entailment, trace, puzzle suite, experiment runner, and clean launch all
  pass.
- **Submission blockers:** final team identity/contribution data, final
  references review, authored `Report.pdf`, recorded/hosted 5-10 minute demo,
  permission validation, and final student-ID archive are still required.
- **Major/minor defects found in Phase 8:** the missing experiment runner and
  stale experiment documentation were MAJOR release-readiness defects and were
  corrected. No gameplay/solver blocker was found. Coverage limitations are
  documented in `KNOWN_LIMITATIONS.md` rather than disguised as passes.

## Prohibited shortcuts verified absent

- No external SAT solver or puzzle-specific CNF.
- No hidden-solution/unrevealed-clue access by agent or GUI.
- No guess-based reveal and no arbitrary-model verdict.
- No fabricated Git hash, experiment, team percentage, report, video, or link.
