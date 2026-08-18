# Prompt Log

## PROMPT-001

- Date: 2026-08-09
- Tool: OpenAI Codex
- Model: GPT-5
- Member: Trần Hữu Phước - 24127511
- Phase: Requirement audit and Phases 01-04
- Goal: Read the official Project 2 PDF and master development prompt, then implement and publish Phases 01-04 to the supplied GitHub repository.
- Full prompt: User supplied `[2526 HK3] IntroAI - Project 2.pdf`, the Master Development Prompt attachment, repository `https://github.com/AI-PROJECT-1/AI-lab-01.git`, and requested careful execution from Phase 01 through Phase 04.
- Short summary of response: Audited the PDF, selected a privacy-preserving architecture, and implemented the approved Phase 01-04 scope.
- Decision: ACCEPTED
- Related AI Usage ID: AI-001 through AI-004
- Related commits: `5a26cbe`, `81e5882`, `bcf0393`, `3dec8a9`, `7e53661`, `d424c47`, `4742e10`

## PROMPT-002

- Date: 2026-08-12
- Tool: OpenAI Codex
- Model: GPT-5
- Member: Trần Hữu Phước - 24127511
- Phase: Audit of Phases 00-07
- Goal: Re-read the complete master prompt and official PDF, compare every phase with the current repository, debug confirmed code/logic/specification deviations, and report the work performed.
- Full prompt: "đọc lại toàn bộ prompt.txt, các phase, đối chiếu với các file hiện tại ở các phase đó xem có lỗi về mặt code, logic, sai lệch so với yêu cầu của intro-ai project 2 hay không. Debug nếu có, rồi báo cáo đã làm những gì"
- Short summary of response: Audited all 1,503 prompt lines and all 9 PDF pages; found test-discovery, region/count validation, DPLL input validation, mock inconsistency, and documentation drift; implemented root-cause fixes and expanded independent verification.
- Decision: ACCEPTED
- Related AI Usage ID: AI-005
- Related commits: `03584c3`

## PROMPT-003

- Date: 2026-08-12
- Tool: OpenAI Codex
- Model: GPT-5
- Member: Trần Hữu Phước - 24127511
- Phase: 08-13
- Goal: Implement a real LogicAgent, Hint/Solve Next/Auto Solve, deduction trace, clue highlighting, two mandatory extensions, and a 3x3/4x4 puzzle suite.
- Full prompt: "LogicAgent suy luận thật; Hint, Solve Next và Auto Solve; Trace suy luận; Highlight vùng clue; Hai extension bắt buộc; Bộ puzzle 3×3/4×4 — triển khai các phần này."
- Short summary of response: Added public-only SAT entailment and progressive engine integration, trace and uniqueness, canonical GUI highlighting, `IMPLIES`/`ODD`, and four automatically validated puzzles.
- Decision: ACCEPTED
- Related AI Usage ID: AI-006
- Related commits: `03584c3`

## PROMPT-004

- Date: 2026-08-12
- Tool: OpenAI Codex
- Model: GPT-5
- Member: Trần Hữu Phước - 24127511
- Phase: Griductive GUI refactor audit and UI Phase 1
- Goal: Improve GUI/gameplay fidelity while preserving the Project 2 architecture, then execute only the approved visual-foundation phase after safely checkpointing Phase 08-13.
- Full prompt: User supplied `GRIDUCTIVE GUI & GAMEPLAY FIDELITY REFACTOR`, approved UI Phase 0 with corrections, required a real Git checkpoint, clarified that `active_clue_ids` do not prove a unique causal clue, and authorized only layout hierarchy, theme, spacing, typography, semantic control grouping, reusable primitives, and responsive containers.
- Short summary of response: Audited GUI/GameEngine/LogicAgent, diagnosed repeated B1 trace entries as separate requests rather than repeated solved selection, created checkpoint `03584c3`, and implemented a presentation-only ttk visual foundation with no AI/gameplay changes.
- Decision: ACCEPTED FOR UI PHASE 1 ONLY
- Related AI Usage ID: AI-007
- Related commits: Phase 08-13 checkpoint `03584c3`; UI Phase 1 `f6b5713`

## PROMPT-005

- Date: 2026-08-12
- Tool: OpenAI Codex
- Model: GPT-5
- Member: Trần Hữu Phước - 24127511
- Phase: Griductive GUI refactor, UI Phase 2 only
- Goal: Redesign board character cards using public presentation data, deterministic avatars, accessible verdict badges, composable visual states, and responsive 3x3/4x4 layouts without changing gameplay or protected modules.
- Full prompt: User approved UI Phase 1 and authorized only Character Card redesign, with explicit hidden/public isolation, no debug metadata on unresolved cards, textual Criminal/Innocent status, safe clue previews, composable selection/highlight/new-reveal modifiers, regression tests, visual inspection, and a stop before UI Phase 3.
- Short summary of response: Committed UI Phase 1 as `f6b5713`, introduced a reusable public-only CharacterCard, removed unresolved debug text, preserved canonical selection/highlighting, adapted card/window sizing to actual screen DPI, and verified all required visual states.
- Decision: ACCEPTED FOR UI PHASE 2 ONLY
- Related AI Usage ID: AI-008
- Related commits: UI Phase 1 `f6b5713`; UI Phase 2 `48bea9d`

## PROMPT-006

- Date: 2026-08-12
- Tool: OpenAI Codex
- Model: GPT-5
- Member: Trần Hữu Phước - 24127511
- Phase: Griductive GUI refactor, UI Phase 3 only
- Goal: Commit approved UI Phase 2, then implement contextual verdict controls, distinct public-only outcome feedback, reset-safe interaction state, and presentation-only newly-revealed emphasis without changing solver/game semantics.
- Full prompt: User approved UI Phase 2, required atomic commit `feat(gui): redesign public character cards` with its real hash recorded, and authorized only contextual verdict interaction plus feedback for `ACCEPTED`, `NOT_PROVABLE`, `CONTRADICTED`, and `INCONSISTENT`, including Load/Restart resets and 3x3/4x4 verification.
- Short summary of response: Created real Phase 2 commit `48bea9d038c7425a691b09d2bd8a2049b3825d0e`; added a public `VerdictContext`, reusable semantic `GameplayFeedback`, disabled submission without an unresolved selection, safe per-outcome wording, transient accepted-reveal emphasis, and reset-safe UI state.
- Decision: ACCEPTED FOR UI PHASE 3 ONLY; approved by the user
- Related AI Usage ID: AI-009
- Related commits: UI Phase 2 `48bea9d`; UI Phase 3 `bd39263`

## PROMPT-007

- Date: 2026-08-13
- Tool: OpenAI Codex
- Model: GPT-5
- Member: Trần Hữu Phước - 24127511
- Phase: Griductive GUI refactor, UI Phase 4 only
- Goal: Commit approved UI Phase 3, then redesign publicly revealed clue presentation and inspection with full text, public ownership, canonical highlighting, selection, new-clue emphasis, and responsive scrolling.
- Full prompt: User approved UI Phase 3, required atomic commit `feat(gui): add contextual verdict feedback` and its real hash, then authorized only revealed-clue cards and inspection while protecting all reasoning, solver, game, public-state, puzzle, Hint, and Solver Trace semantics.
- Short summary of response: Created real Phase 3 commit `bd3926325795dce94afb9d719889e6071e823446`; introduced public-only ClueCard models/components, scrollable responsive CluePanel, composable selected/newly-revealed states, canonical resolver reuse, full wrapped text, and presentation-only new-clue auto-scroll.
- Decision: ACCEPTED FOR UI PHASE 4 ONLY; approved by the user
- Related AI Usage ID: AI-010
- Related commits: UI Phase 3 `bd39263`; UI Phase 4 `dff07f0`

## PROMPT-008

- Date: 2026-08-13
- Tool: OpenAI Codex
- Model: GPT-5
- Member: Trần Hữu Phước - 24127511
- Phase: Griductive GUI refactor, UI Phase 5 only
- Goal: Commit approved UI Phase 4, then implement a public-only two-stage Hint UX with one reasoning request per unchanged-state cycle, safe active-clue wording, cached target presentation, and complete invalidation.
- Full prompt: User approved UI Phase 4, required atomic commit `feat(gui): redesign revealed clue inspection` and its real hash, then authorized only progressive Hint UX while explicitly prohibiting unique proof-anchor claims, Stage 2 solver calls, hidden verdict/clue exposure, solver/trace redesign, and protected-module changes.
- Short summary of response: Created real Phase 4 commit `dff07f05a003fa966c200fc925e5da600846ec54`; added a public fingerprinted HintSession, Stage 1 active-revealed-clue presentation, Stage 2 cached target-only emphasis, composable clue/card modifiers, progressive button text, and mutation/reset invalidation.
- Decision: ACCEPTED FOR UI PHASE 5 ONLY; approved by the user
- Related AI Usage ID: AI-011
- Related commits: UI Phase 4 `dff07f0`; UI Phase 5 `d2682b3`

## PROMPT-009

- Date: 2026-08-13
- Tool: OpenAI Codex
- Model: GPT-5
- Member: Tran Huu Phuoc - 24127511
- Phase: Griductive GUI refactor, UI Phase 6 only
- Goal: Commit approved UI Phase 5, then move raw Solver Trace out of normal gameplay into a secondary, structured Solver Details interface without changing trace generation or solver/game semantics.
- Full prompt: User approved UI Phase 5, required atomic commit `feat(gui): add progressive two-stage hints` and its real hash, then authorized only Solver Tools plus Solver Details presentation with exact trace fields, readable SAT queries/statistics, reliable GUI-only action sources, progressive Auto Solve updates, reset safety, public/private checks, full tests, and a stop before UI Phase 7.
- Short summary of response: Created real Phase 5 commit `d2682b3ebccdf087c417a90b50488def293c79ce`; replaced the always-visible raw Listbox with a lazy scrollable Toplevel of structured trace cards, preserved all existing trace records, labeled only reliably observed action slices, and kept Hint Stage 2 presentation-only.
- Decision: ACCEPTED FOR UI PHASE 6 ONLY; approved by the user
- Related AI Usage ID: AI-012
- Related commits: UI Phase 5 `d2682b3`; UI Phase 6 `5673fe0`

## PROMPT-010

- Date: 2026-08-16
- Tool: OpenAI Codex
- Model: GPT-5
- Member: Tran Huu Phuoc - 24127511
- Phase: Phase 6.5 Hint explanation fidelity only
- Goal: Commit approved UI Phase 6, then extract a deterministic, logically valid public supporting set for the already-forced Hint target while preserving two-stage UX, trace semantics, privacy, and solver boundaries.
- Full prompt: User required real Phase 6 checkpoint `feat(gui): add structured solver details`, grouped revealed-clue and proved-verdict support components, same-verdict deletion reduction, irreducibility tests, separate diagnostic SAT cost, safe Phase 5 fallback, Stage 1 support emphasis, unchanged cached Stage 2, performance/visual verification, audit updates, and a stop before Phase 7.
- Short summary of response: Created real Phase 6 commit `5673fe09c0cd1a47f10e3f75d7ac2344dec7820f`; introduced a shared trace-free entailment helper and deletion-irreducible public support extractor, enriched `HintResult` compatibly, highlighted supporting clues/verdicts in Stage 1, and retained target-only Stage 2 plus active-clue fallback.
- Decision: EXECUTED FOR PHASE 6.5 ONLY; approved by the user
- Related AI Usage ID: AI-013
- Related commits: UI Phase 6 `5673fe0`; Phase 6.5 `ba7912b`

## PROMPT-011

- Date: 2026-08-16
- Tool: OpenAI Codex
- Model: GPT-5
- Member: Tran Huu Phuoc - 24127511
- Phase: Griductive GUI refactor, UI Phase 7 only
- Goal: Commit approved Phase 6.5, then complete the player-facing loop with public solved-card clue inspection, public completion presentation, coherent completed controls, robust lifecycle cleanup, and final restrained polish.
- Full prompt: User approved Phase 6.5, required atomic commit `feat(agent): add grounded hint support extraction` and its real hash, then authorized only gameplay completion/final polish while protecting all solver, entailment, support-extraction, game-engine, public-state, and puzzle semantics. Required tests, scans, 3x3/4x4 visual review, audit updates, and a stop before Phase 8.
- Short summary of response: Created real Phase 6.5 commit `ba7912b1ea64487cde55ae198cae1a648e363036`; added a public card-interaction DTO, canonical solved-card clue spotlight/scroll, public `is_complete` banner, completion-aware controls and handler guards, generation-safe Auto Solve, comprehensive lifecycle cleanup, and production title consistency.
- Decision: EXECUTED FOR UI PHASE 7 ONLY; approved by the user
- Related AI Usage ID: AI-014
- Related commits: Phase 6.5 `ba7912b`; UI Phase 7 `4150d86`

## PROMPT-012

- Date: 2026-08-16
- Tool: OpenAI Codex
- Model: GPT-5
- Member: Tran Huu Phuoc - 24127511
- Phase: UI Phase 8 final regression, requirement audit, and demo readiness
- Goal: Commit approved Phase 7, audit all Project 2 requirements against actual implementation/evidence, correct only verified blocker/major defects, run final regression/experiments/E2E, and prepare honest demo/report support without producing submission artifacts.
- Full prompt: User approved UI Phase 7, required atomic commit `feat(gui): finalize gameplay completion experience` and its real hash, then authorized only final regression, requirement audit, experiment/demo readiness, audit-document updates, repository/entrypoint validation, and a 46-item completion gate. Report generation, video recording, archive/upload/submission, feature creep, fabricated metrics/history, and new gameplay/AI semantics were prohibited.
- Short summary of response: Created real Phase 7 commit `4150d867b6f2ce03cf273ced9895c4dd06105445`; found and corrected the missing reproducible experiment runner/documentation, added five release-audit tests, generated a four-puzzle raw result, rehearsed the deterministic 3x3/4x4 UI path, and converted the planned audit into an evidence/status matrix. Final submission artifacts and team attribution remain explicitly blocked rather than fabricated.
- Decision: EXECUTED FOR UI PHASE 8 ONLY; approved by the user
- Related AI Usage ID: AI-015
- Related commits: UI Phase 7 `4150d86`; UI Phase 8 `2c8ed1b`

## PROMPT-013

- Date: 2026-08-16
- Tool: OpenAI Codex
- Model: GPT-5
- Member: Tran Huu Phuoc - 24127511
- Phase: Phase 8.5 puzzle quality, deduction difficulty, and screen navigation
- Goal: Preserve the solver while creating genuine Tutorial/Standard/Advanced experiences and same-window shipped-puzzle navigation with public-only metadata, reset-safe Play, Back-without-reset, quality profiles, rerun experiments, and complete verification.
- Full prompt: User approved Phase 8, required its exact atomic commit and real hash, then authorized puzzle data, GUI navigation, tests, experiments, and documentation only. Required a Standard 3x3 with relations/counting/regions, an Advanced 4x4 with extensions and real support size >=2, a scrollable Puzzle Select screen, public/private gates, actual metrics, visual E2E, and a stop before Phase 9.
- Short summary of response: Verified Phase 8 commit `2c8ed1b`; retained the direct Gallery Shift as Tutorial; added unique/progressive deduction-focused Standard and Advanced puzzles; added a safe catalog plus ScreenManager/PuzzleSelect; added public support analysis and 17 tests; reran six-puzzle experiments; and updated demo/report/audit evidence.
- Decision: EXECUTED FOR PHASE 8.5 ONLY; approved and committed as `8c8c77d`
- Revalidation: The same Phase 8.5 prompt was supplied again on 2026-08-18. Existing uncommitted work was preserved rather than duplicated; 196/196 tests and all required static boundaries passed again. Phase 9 was not started.
- Related AI Usage ID: AI-016
- Related commits: Phase 8 `2c8ed1b`; Phase 8.5 `8c8c77d`

## PROMPT-014

- Date: 2026-08-18
- Tool: OpenAI Codex
- Model: GPT-5
- Member: Tran Huu Phuoc - 24127511
- Phase: Phase 8.6 production puzzle hardening, non-linear reveals, and anti-guess lock
- Goal: Commit no unapproved Phase 8.6 work; harden the production catalog to genuine Standard/Advanced deduction puzzles; remove Tutorial/direct FACT anchors; make reveal progression non-linear; add a public-only manual contradiction lock; rerun experiments, regression, boundary, and GUI review; update audit records; stop before Phase 9.
- Full prompt: The user supplied the attached Phase 8.6 master prompt requiring a real Phase 8.5 checkpoint, production/test-fixture separation, deterministic validated puzzle data, no hidden-solution or protected-solver changes, one-run per-character manual lockout after CONTRADICTED, unchanged Hint/Solve/Auto semantics, complete test and visual evidence, and a fixed 72-item final gate report.
- Short summary of response: Preserved `8c8c77d`; reduced production to two explicit catalog entries; moved four legacy chains to fixtures; removed all production FACT clues; remapped deterministic reveal ownership; added controller/presentation-only lockout; extended quality metrics and 16 Phase 8.6 tests; regenerated two-puzzle evidence and documentation.
- Decision: EXECUTED FOR PHASE 8.6 ONLY; intentionally uncommitted pending approval
- Related AI Usage ID: AI-017
- Related commits: Phase 8.5 checkpoint `8c8c77d`; Phase 8.6 UNCOMMITTED
