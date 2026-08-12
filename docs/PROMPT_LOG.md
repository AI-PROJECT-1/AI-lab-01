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
- Decision: ACCEPTED FOR UI PHASE 4 ONLY; final Phase 4 approval PENDING
- Related AI Usage ID: AI-010
- Related commits: UI Phase 3 `bd39263`; UI Phase 4 PENDING
