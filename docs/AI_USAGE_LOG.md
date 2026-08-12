# AI Usage Log

## AI-001

- Date: 2026-08-09
- AI tool: OpenAI Codex
- Model: GPT-5
- Developer/member: Unassigned team member (confirm before submission)
- Phase: Requirement audit and Phase 01
- Purpose: Audit the official PDF and establish a compliant repository foundation.
- Files affected: README, package structure, requirements, project documentation.
- Summary of AI suggestion: Use immutable public DTOs, explicit agent protocol, standard-library-first Phase 01-04 implementation, and atomic phase commits.
- Accepted: Public/hidden boundary, phase-gated architecture, audit mapping, no fake solver behavior.
- Rejected/deferred: Production SAT reasoning, extensions, experiments, and unsupported completion claims before their phases.
- Human verification performed: PENDING team review.
- Tests performed: `compileall`, unittest discovery (0 tests expected), and `git diff --check`; all passed.
- Related Prompt ID: PROMPT-001
- Related Git commit hash: 5a26cbe

## AI-002

- Date: 2026-08-09
- AI tool: OpenAI Codex
- Model: GPT-5
- Developer/member: Unassigned team member (confirm before submission)
- Phase: 02
- Purpose: Define validated shared contracts and a puzzle interchange format.
- Files affected: `core/`, `puzzles/schema.json`, `puzzles/sample_3x3.json`, `tests/test_core.py`.
- Summary of AI suggestion: Use frozen slotted dataclasses, stable coordinate IDs, structured clue variants, and a hidden `PuzzleCard` that never crosses the public boundary.
- Accepted: Immutable DTOs, validation at construction, tuple-based public collections, JSON Schema.
- Rejected/deferred: General region resolution and semantic truth evaluation before Phase 05.
- Human verification performed: PENDING team review.
- Tests performed: 9/9 unittests passed; schema/sample JSON syntax, compile, and diff checks passed.
- Related Prompt ID: PROMPT-001
- Related Git commit hash: 81e5882

## AI-003

- Date: 2026-08-09
- AI tool: OpenAI Codex
- Model: GPT-5
- Developer/member: Unassigned team member (confirm before submission)
- Phase: 03
- Purpose: Implement loading and a privacy-preserving progressive game engine.
- Files affected: `agent/protocols.py`, `agent/mock_logic_agent.py`, `game/`, `tests/test_game.py`, `core/character.py`.
- Summary of AI suggestion: Keep the agent input limited to immutable public snapshots and have the engine verify an accepted forced verdict against its authoritative hidden status before reveal.
- Accepted: Public-only protocol, strict loader, copy-on-snapshot, integrity error with no mutation.
- Rejected/deferred: Hidden-solution mock, accept-all mock, production entailment before its phase.
- Human verification performed: PENDING team review.
- Tests performed: Initial run 18/19 due to sandbox temp permission; test fixed to mock file input; final 20/20 passed plus compile/diff checks.
- Related Prompt ID: PROMPT-001
- Related Git commit hash: bcf0393

## AI-004

- Date: 2026-08-09
- AI tool: OpenAI Codex
- Model: GPT-5
- Developer/member: Unassigned team member (confirm before submission)
- Phase: 04
- Purpose: Build the desktop GUI skeleton and manual gameplay loop without fake production reasoning.
- Files affected: `main.py`, `gui/`, `tests/test_gui.py`, project logs.
- Summary of AI suggestion: Render only public view models, route actions through a headless controller, label the FACT-only development agent, and disable features whose real reasoning is not implemented.
- Accepted: Tkinter GUI, controller/view-model split, visible phase limitations, no direct hidden access.
- Rejected/deferred: GUI-side clue region resolver, fabricated Hint/Auto Solve behavior.
- Human verification performed: PENDING team visual review.
- Tests performed: 25/25 unittests passed, full compile/diff checks passed, and a real Tk widget/layout smoke test completed cleanly.
- Related Prompt ID: PROMPT-001
- Related Git commit hash: 3dec8a9

## AI-005

- Date: 2026-08-12
- AI tool: OpenAI Codex
- Model: GPT-5
- Developer/member: Trần Hữu Phước - 24127511
- Phase: Audit and debug of Phases 00-07
- Purpose: Compare the complete master prompt and official Project 2 PDF against merged code, reproduce deviations, fix root causes, and restore trustworthy phase/test evidence.
- Files affected: `logic/region_resolver.py`, `logic/cnf_encoder.py`, `logic/semantic_evaluator.py`, `sat/dpll.py`, `agent/mock_logic_agent.py`, tests, README, and audit documents.
- Summary of AI suggestion: Centralize region semantics, validate resolved region bounds and cardinality parameters, enforce integer-only DPLL inputs, make DPLL tests discoverable by the documented runner, use exhaustive CNF equivalence and brute-force SAT oracles, and distinguish implemented phases from final-project gaps.
- Accepted: All listed root-cause fixes and evidence updates.
- Rejected: Adding pytest only to preserve incompatible tests; claiming Phases 08-17 or final rubric completion; fabricating prior teammates' AI usage records.
- Human verification performed: PENDING team review of this audit and code diff.
- Tests performed: `python -m pytest -q` failed because pytest is not installed; existing DPLL functions then passed when invoked directly; 3,500 diagnostic DPLL cases passed against brute force; final discoverable regression and GUI smoke results are recorded in `TEST_LOG.md`.
- Related Prompt ID: PROMPT-002
- Related Git commit hash: `03584c3`

## AI-006

- Date: 2026-08-12
- AI tool: OpenAI Codex
- Model: GPT-5
- Developer/member: Trần Hữu Phước - 24127511
- Phase: 08-13
- Purpose: Implement the production deductive agent, progressive controls and trace, canonical highlighting, two required extensions, and validated 3x3/4x4 puzzles.
- Files affected: `agent/`, `game/game_engine.py`, `gui/`, core clue contracts, logic encoder/evaluator/resolver, puzzle schema/files, tests, and project documentation.
- Summary of AI suggestion: Use assumption-based entailment, keep progressive reveal orchestration in GameEngine, require clue-only states for uniqueness, share the canonical resolver with GUI highlighting, and select `IMPLIES` plus `ODD` after comparing four candidates.
- Accepted: Public-only LogicAgent, non-mutating Hint, deterministic Solve Next, wave-based Auto Solve, SAT trace, primary-model uniqueness blocking, canonical highlights, both extensions, four-puzzle validation gates.
- Rejected: Passing GameEngine to the agent; deriving verdicts from one satisfying model; batch-revealing from a stale snapshot; redundant extension candidates equivalent to existing clues.
- Human verification performed: PENDING team review and visual acceptance.
- Tests performed: 77/77 unittests passed; all JSON parsed; full compile passed; GUI smoke and boundary scans recorded in `TEST_LOG.md`.
- Related Prompt ID: PROMPT-003
- Related Git commit hash: `03584c3`

## AI-007

- Date: 2026-08-12
- AI tool: OpenAI Codex
- Model: GPT-5
- Developer/member: Trần Hữu Phước - 24127511
- Phase: Griductive GUI fidelity refactor, UI Phase 0-1
- Purpose: Audit the current presentation architecture, preserve Phase 08-13, create a real Git checkpoint, and establish a responsive visual foundation without changing gameplay or AI behavior.
- Files affected: `gui/app.py`, `gui/board_view.py`, `gui/clue_panel.py`, `gui/controls.py`, `gui/trace_panel.py`, new `gui/theme.py`, new `gui/components.py`, `tests/test_gui_foundation.py`, and audit logs.
- Summary of AI suggestion: Centralize project-owned color/spacing/type tokens, introduce reusable header/feedback/control-group primitives, establish a board-first responsive container, and organize existing controls into GAME, PLAYER VERDICT, ASSISTANCE, and SOLVER groups.
- Accepted: Standard-library ttk theme, reusable presentation primitives, semantic control grouping, responsive 3x3/4x4 sizing, and preservation of all callbacks and trace data.
- Rejected/deferred: Character-card redesign, clue-card redesign, collapsible trace, new Hint reasoning, completion metrics, and any LogicAgent/GameEngine/CNF/DPLL change; these are outside UI Phase 1.
- Hint fidelity: No clue is described as a unique cause. The current API exposes only `active_clue_ids`; no latest-clue causal claim was added.
- Human verification performed: UI Phase 0 plan approved by the user; Phase 1 visual acceptance is PENDING.
- Tests performed: pre-checkpoint 77/77 regression and boundary scan PASS; final 80/80 regression, compile, diff check, boundary scan, and Tkinter 3x3/4x4 smoke tests PASS.
- Phase 08-13 checkpoint: `03584c3859a12e7a57385a7d860e48f084d0c210` (`feat(project): checkpoint phases 08-13`).
- Related Prompt ID: PROMPT-004
- Related Git commit hash: `f6b5713`

## AI-008

- Date: 2026-08-12
- AI tool: OpenAI Codex
- Model: GPT-5
- Developer/member: Trần Hữu Phước - 24127511
- Phase: Griductive GUI fidelity refactor, UI Phase 2
- Purpose: Replace debug-style board buttons with responsive, game-style CharacterCard components while preserving public-only data and all existing gameplay behavior.
- Files affected: `gui/character_card.py`, `gui/board_view.py`, `gui/view_model.py`, `gui/theme.py`, minor responsive integration in `gui/app.py`, `tests/test_character_card.py`, `tests/test_gui.py`, and audit logs.
- Avatar strategy: Project-owned deterministic initials tiles. Initials derive only from the public name; palette choice derives deterministically from the public character ID. No downloaded, scraped, copyrighted, or generated external artwork is used.
- Visual-state architecture: `CardBaseState` (`UNRESOLVED`, `CRIMINAL`, `INNOCENT`) composes independently with `CardModifiers` (`selected`, `clue_highlighted`, `newly_revealed`). Nested outlines preserve base status surface and textual badge when modifiers overlap.
- Hidden/public isolation: CharacterCard accepts only `CardViewModel`, which is built from `PublicKnowledgeState`; unresolved visible text excludes verdict placeholders, face-state labels, clue placeholders, and unrevealed clue IDs.
- Responsive decisions: horizontal avatar/identity/coordinate header; compact fonts and 28-character public clue preview for 4x4; 52-character preview for 3x3; complete clue remains in the unchanged Revealed Clues panel; window geometry respects screen bounds.
- Accepted: deterministic initials avatars, textual status badges, independent modifier outlines, safe clue preview, size-aware composition, and visual QA at actual DPI.
- Rejected/deferred: external portraits, copyrighted assets, full clue text in every 4x4 card, contextual verdict actions, CluePanel redesign, Hint changes, Solver Details drawer, completion metrics, and any protected-module change.
- Human verification performed: DPI-aware screenshots inspected for unresolved, mixed revealed/unresolved, selected unresolved, Criminal, Innocent, highlighted revealed, and completed 4x4 states; UI Phase 2 was approved by the user.
- Tests performed: `python -m pytest -q` unavailable because pytest is not installed; supported full runner passed 87/87; compile, diff, boundary/external-solver/protected-module scans, 3x3 smoke, and 4x4 smoke passed.
- Related Prompt ID: PROMPT-005
- Related Git commit hash: `48bea9d038c7425a691b09d2bd8a2049b3825d0e`

## AI-009

- Date: 2026-08-12
- AI tool: OpenAI Codex
- Model: GPT-5
- Developer/member: Trần Hữu Phước - 24127511
- Phase: Griductive GUI fidelity refactor, UI Phase 3
- Purpose: Make manual verdict controls contextual, disable inappropriate submissions, present the four existing verdict outcomes distinctly, and emphasize a freshly accepted public reveal without changing game or solver semantics.
- Files affected: `gui/app.py`, `gui/board_view.py`, `gui/character_card.py`, `gui/components.py`, `gui/controls.py`, `gui/theme.py`, new `gui/feedback.py`, new `gui/verdict_panel.py`, new `tests/test_verdict_interaction.py`, and audit logs.
- Context architecture: `VerdictContext` derives button availability and selected identity only from `CardViewModel`; `VerdictPanel` owns the two player-verdict buttons and exposes their real enabled state. Resolved and absent selections disable both actions.
- Feedback architecture: `GameplayFeedback` separates neutral, success, information, warning, and error tones. `feedback_for_verdict()` maps `ACCEPTED`, `NOT_PROVABLE`, `CONTRADICTED`, and `INCONSISTENT` without copying the engine's free-form message, hidden solution, unrevealed clue payload, or opposite forced-status detail.
- Newly-revealed rule: The app compares immutable public snapshots before and after the existing submission API. A transient card outline is set only when an accepted result changes that character from unrevealed to a public verdict plus public clue. No game/public DTO is mutated by the effect.
- Reset rule: successful Load and Restart clear selected character, clue highlight, verdict feedback, newly-revealed emphasis, and stale interaction state. A cancelled or failed Load preserves the current puzzle.
- Responsive decision: PLAYER VERDICT and gameplay feedback use compact single-row layouts; 4x4 identity headers and badge/clue previews share horizontal space so all public content remains visible within the existing screen-aware window.
- Accepted: public-only context model, disabled buttons, semantic feedback tones, safe outcome wording, presentation-only reveal emphasis, compact responsive status rows, and generic integrity-error feedback.
- Rejected/deferred: engine/controller API changes, hidden-answer comparison in the GUI, contextual completion actions, clue-card redesign, two-stage Hint, Solver Details, trace redesign, completion screen, and any CNF/DPLL/LogicAgent change.
- Human verification performed: Tkinter screenshots inspected for no selection, selected unresolved, contradicted warning, accepted 3x3 reveal emphasis, and accepted 4x4 reveal emphasis. Iteration corrected clipped context text and vertically clipped 4x4 status/clue rows.
- Tests performed: supported full runner passed 96/96; compile, diff, boundary/external-solver/protected-module scans, 3x3 interaction/reset smoke, and 4x4 responsive smoke passed. `pytest` remains unavailable in this environment.
- Approved Phase 2 commit: `48bea9d038c7425a691b09d2bd8a2049b3825d0e` (`feat(gui): redesign public character cards`).
- Related Prompt ID: PROMPT-006
- Related Git commit hash: `bd3926325795dce94afb9d719889e6071e823446`

## AI-010

- Date: 2026-08-13
- AI tool: OpenAI Codex
- Model: GPT-5
- Developer/member: Trần Hữu Phước - 24127511
- Phase: Griductive GUI fidelity refactor, UI Phase 4
- Purpose: Replace the raw revealed-clue list with readable, selectable public clue cards while preserving canonical cell highlighting, full clue text, and all solver/game semantics.
- Files affected: new `gui/clue_card.py`, redesigned `gui/clue_panel.py`, presentation integration in `gui/app.py`, clue tokens in `gui/theme.py`, new `tests/test_clue_presentation.py`, and audit logs.
- Clue-card decision: `ClueCardViewModel` contains only owner name/coordinate, clue ID, and complete display text built from `PublicKnowledgeState.revealed_clues`. The ID is secondary, while owner and full wrapped text form the main hierarchy.
- Selection design: `ClueCardModifiers` composes independent selected and newly-revealed outlines over a stable clue surface. Selecting a card stores only the existing controller owner selection and never mutates public/game state.
- Canonical highlighting: The GUI continues to call `GameController.select_clue()`, which delegates to the existing `logic.region_resolver.referenced_cells()` path. No natural-language parsing or region reimplementation was added.
- Hidden/public verification: `build_clue_views()` iterates only `revealed_clues`; tests confirm an unrevealed clue ID/text is absent and full public text remains accessible. ClueCard has no Puzzle or GameEngine access.
- Newly-revealed presentation: Existing before/after public snapshot comparison supplies an owner ID to both CharacterCard and ClueCard modifiers. Manual verdict, Solve Next, and each Auto Solve step can emphasize the newly public clue; scrolling brings it into view. No DTO field was added.
- Responsive decision: A Canvas-backed vertical list preserves board allocation and supports overflow scrolling. Clue text wrap length follows the live canvas width, and 4x4 with all 16 clues scrolls to the newest clue.
- Accepted: reusable clue cards, owner-first hierarchy, secondary clue ID, complete responsive text, composable selection/new outlines, canonical resolver reuse, auto-scroll, and public empty state.
- Rejected/deferred: parsing display text, copying RegionResolver logic into GUI, hidden clue lookups, clue semantics changes, two-stage Hint, proof-anchor causality, Solver Trace redesign, completion UI, and protected-module changes.
- Human verification performed: DPI-aware screenshots inspected for empty, initial one clue, selected clue plus selected character, newly revealed clue, several clues, long text, highlighted Innocent/Criminal cards, and a completed scrolling 4x4 list.
- Tests performed: supported full runner passed 105/105; compile, diff, boundary/external-solver/protected-module scans, 3x3 smoke, and 4x4 scrolling smoke passed. `pytest` remains unavailable.
- Approved Phase 3 commit: `bd3926325795dce94afb9d719889e6071e823446` (`feat(gui): add contextual verdict feedback`).
- Related Prompt ID: PROMPT-007
- Related Git commit hash: `dff07f05a003fa966c200fc925e5da600846ec54`

## AI-011

- Date: 2026-08-13
- AI tool: OpenAI Codex
- Model: GPT-5
- Developer/member: Trần Hữu Phước - 24127511
- Phase: Griductive GUI fidelity refactor, UI Phase 5
- Purpose: Present Hint progressively in two stages while avoiding duplicate reasoning calls, hidden-data leakage, and unsupported proof-causality claims.
- Files affected: new `gui/hint_session.py`, presentation integration in `gui/app.py`, `gui/board_view.py`, `gui/character_card.py`, `gui/clue_card.py`, `gui/clue_panel.py`, `gui/controls.py`, `gui/theme.py`, new `tests/test_hint_ux.py`, and audit logs.
- Two-stage decision: Stage 1 performs exactly one existing `get_hint()` request and emphasizes only active clue IDs that also exist in current public reveals. Stage 2 reuses the cached target for an unchanged fingerprint and identifies only the public character name/coordinate without displaying a verdict.
- Solver-call rule: `progress_hint_session()` calls reasoning only when no matching Stage 1 session exists. Stage 2 is presentation-only, so it adds no solver/trace request; a later fresh cycle may call reasoning once again.
- Causality rule: `active_clue_ids` are described only as currently active revealed clues. The UI explicitly does not call any individual clue a cause or unique/direct proof anchor because the API does not establish that relationship.
- Session/fingerprint design: The cache stores only puzzle ID, public known verdict pairs, public revealed owner/clue-ID pairs, completion flag, public target ID, stage, and filtered active clue IDs. It does not cache `HintResult.message`, target verdict, unrevealed clue, Puzzle, GameEngine, or solver internals.
- Invalidation rule: ACCEPTED public mutation, Solve Next, Auto Solve start and every reveal, Restart, and successful Load clear the session plus clue/target modifiers and reset the button label. Fingerprint mismatch independently prevents stale Stage 2 use. Character/clue selection alone preserves the session.
- Modifier design: Character `hint_target` and clue `hint_active` are separate outline layers that compose with base verdict, selected, canonical highlight, and newly-revealed states.
- Accepted: public fingerprint, one-call two-stage cycle, safe trace slicing/filtering, generic no-anchor fallback, progressive button label, composable outlines, and defense against stale cached targets.
- Rejected/deferred: displaying the cached verdict, using `HintResult.message`, presenting the latest clue as causal, parsing clue text, additional DPLL calls for Stage 2, LogicAgent/trace changes, Solver Details, completion UI, and Phase 6 work.
- Human verification performed: DPI-aware screenshots inspected before Hint, Stage 1 with one/multiple active clues, generic no-anchor Stage 1, Stage 2 target, manual ACCEPTED, Solve Next, Auto Solve lifecycle, Restart, and Load. No stale hint modifier survived mutation/reset.
- Tests performed: supported full runner passed 117/117; compile, diff, boundary/external-solver/protected-module scans, 3x3 Hint lifecycle smoke, and 4x4 Auto Solve smoke passed. `pytest` remains unavailable.
- Approved Phase 4 commit: `dff07f05a003fa966c200fc925e5da600846ec54` (`feat(gui): redesign revealed clue inspection`).
- Related Prompt ID: PROMPT-008
- Related Git commit hash: PENDING
