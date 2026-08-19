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
- Related Git commit hash: `d2682b3ebccdf087c417a90b50488def293c79ce`

## AI-012

- Date: 2026-08-13
- AI tool: OpenAI Codex
- Model: GPT-5
- Developer/member: Tran Huu Phuoc - 24127511
- Phase: Griductive GUI fidelity refactor, UI Phase 6
- Purpose: Move technical solver trace out of the default game-first layout while preserving every existing trace field in a structured secondary interface.
- Files affected: redesigned `gui/trace_panel.py`, presentation integration and reset-safe Auto Solve scheduling in `gui/app.py`, `gui/controls.py`, `gui/theme.py`, new `tests/test_solver_details.py`, and audit logs.
- Presentation decision: Use a lazy secondary `Toplevel` with scrollable structured step cards. The main sidebar now belongs entirely to Revealed Clues; Solver Details is opened explicitly from the SOLVER control group.
- Direct trace fields: Step number, character target ID, verdict, exact active clue IDs, every SAT query purpose/assumption/result, per-query decisions/propagations/backtracks/runtime, and newly revealed clue ID are copied from `DeductionTraceStep`/`SATQueryTrace` without another reasoning call.
- Non-inference rule: Missing target/query/reveal fields remain absent or unavailable. The UI does not infer clause-level proofs, cumulative statistics, hidden assignments, clue causality, or action sources for historical steps.
- Action-source decision: A GUI-only ledger labels exactly the new trace slice observed around HINT, MANUAL VERDICT, SOLVE NEXT, or AUTO SOLVE callbacks. Unlabeled history remains source-less rather than being guessed.
- Hint behavior: Stage 1 may add its one real reasoning slice; Stage 2 consumes the cached Phase 5 session and creates no extra trace or detail step.
- Lifecycle behavior: Restart and successful Load cancel a pending `after()` Auto Solve callback, reset trace-source metadata, and re-render an open details window with the engine's cleared trace.
- Hidden/public verification: Solver Details consumes only public report records already returned by `controller.trace()`; it has no Puzzle, hidden solution, private GameEngine, or unrevealed-clue lookup.
- Accepted: game-first default layout, lazy secondary details window, structured cards, exact trace data, per-query metrics, reliable source metadata, progressive Auto Solve refresh, and reset-safe open-window behavior.
- Rejected/deferred: natural-language proof generation, clause-level proof invention, final assignment display, completion screen/statistics, player marks, animation, protected-module changes, and all UI Phase 7 work.
- Human verification performed: DPI-aware visual review covered closed 3x3/4x4 gameplay, empty/open details, Hint, Solve Next, multiple Auto Solve steps, long active-clue/query data, Restart, and Load while details remained open.
- Tests performed: supported full runner passed 135/135; compile, diff, public-boundary/external-solver/protected-module scans, and Tkinter 3x3/4x4 smoke passed. `pytest` remains unavailable and was not installed.
- Approved Phase 5 commit: `d2682b3ebccdf087c417a90b50488def293c79ce` (`feat(gui): add progressive two-stage hints`).
- Related Prompt ID: PROMPT-009
- Related Git commit hash: `5673fe09c0cd1a47f10e3f75d7ac2344dec7820f`

## AI-013

- Date: 2026-08-16
- AI tool: OpenAI Codex
- Model: GPT-5
- Developer/member: Tran Huu Phuoc - 24127511
- Phase: Phase 6.5 Hint explanation fidelity / support extraction
- Purpose: Replace Stage 1's broad active-clue guidance with a logically grounded public support set for the target already selected by the existing Hint deduction.
- Files affected: new `agent/entailment.py`, new `agent/hint_explanation.py`, `agent/deduction_trace.py`, `agent/logic_agent.py`, `gui/hint_session.py`, `gui/app.py`, `gui/board_view.py`, `gui/character_card.py`, `gui/view_model.py`, new `tests/test_hint_support.py`, architecture/report-support notes, and audit logs.
- Integration strategy: Extract the existing SAT classification path into a pure public-state helper. Normal deduction wraps its returned queries in the existing trace step; Hint support diagnostics call the same helper without incrementing the trace step counter or modifying `last_trace`.
- Target rule: `LogicAgent.get_hint()` continues to call the existing `solve_next()` first. Support extraction runs only after that method returns a forced target/status and does not search for a target independently.
- Component model: Each revealed clue is one indivisible component even when it encodes many CNF clauses. Every previously proved public verdict is a separate unit-constraint component.
- Reduction decision: Verify consistent baseline entailment of the same target verdict, then greedily test removal in clue-ID order followed by row-major verdict order. Keep a component only when deleting it stops forcing the same verdict.
- Terminology: The result is a deterministic deletion-irreducible supporting set. It is not claimed to be a unique proof or globally minimum-cardinality proof.
- Privacy rule: The DTO contains public target/clue/verdict IDs plus separate diagnostic cost only. No Puzzle, GameEngine, hidden status, unrevealed clue, natural-language parsing, or private state is used.
- Hint UI: Stage 1 prefers verified supporting clue IDs and may emphasize supporting solved characters; Stage 2 remains cached target-only and creates no second solver request. Invalid, empty, or failed explanations fall back to Phase 5 active-clue guidance.
- Trace/metrics rule: Support ablation SAT work is measured separately (`support_extraction_sat_calls`, `support_extraction_runtime`) and never becomes normal deduction steps or changes historical experiment numbers.
- Performance measured: 25 fresh-engine runs produced 3x3 median Hint 0.000223900s / extraction 0.000138700s and 4x4 median Hint 0.000276600s / extraction 0.000173200s; both initial states used 9 extraction SAT calls.
- Accepted suggestions: pure shared entailment helper, public structured explanation DTO, grouped clue ablation, proved-verdict components, deterministic ordering, safe fallback, fingerprint-bound caching, and explicit diagnostic cost.
- Rejected/deferred: global minimum search, proof-anchor wording, clause-level ablation, clue-text parsing, DPLL/CNF/game changes, Solver Details redesign, experiment rewrites, solved-card click behavior, and all Phase 7 work.
- Human verification performed: DPI-aware review covered all required 3x3/4x4 single/multiple/clue-plus-verdict, Stage 2, fallback, scrolling, Auto Solve, Restart, and stale-state cases; public synthetic states were used only for multi-clue layouts absent from the distributable chain puzzles.
- Tests performed: supported full runner passed 155/155; compile, diff, boundary/external-solver/hidden-import/still-protected-file scans and Tkinter visual smoke passed. `pytest` remains unavailable and was not installed.
- Approved Phase 6 commit: `5673fe09c0cd1a47f10e3f75d7ac2344dec7820f` (`feat(gui): add structured solver details`).
- Related Prompt ID: PROMPT-010
- Related Git commit hash: `ba7912b1ea64487cde55ae198cae1a648e363036`

## AI-014

- Date: 2026-08-16
- AI tool: OpenAI Codex
- Model: GPT-5
- Developer/member: Tran Huu Phuoc - 24127511
- Phase: Griductive GUI fidelity refactor, UI Phase 7
- Purpose: Finalize the public gameplay loop with solved-card clue inspection, a public-state-driven completion presentation, coherent completed controls, and reset-safe transient state.
- Files affected: `gui/app.py`, `gui/clue_panel.py`, `gui/controller.py`, `gui/controls.py`, `gui/theme.py`, `gui/verdict_panel.py`, new `gui/completion_panel.py`, new `tests/test_gameplay_completion.py`, architecture/report-support notes, and audit logs.
- Solved-card decision: `GameController.activate_character()` checks only `PublicKnowledgeState.clue_for()`. An unresolved card remains verdict selection; a card with a revealed public clue clears verdict selection, selects that exact owner clue, and reuses `select_clue()` plus the canonical region resolver for board highlights.
- Interaction isolation: Solved-card inspection invokes no Hint, Solve Next, verdict submission, CNF build, or DPLL call. Tests use a fail-fast engine stub to verify those methods are never reached.
- Completion decision: `completion_presentation_for()` consumes only `PublicKnowledgeState.is_complete`. The compact banner preserves the board, clue list, solved-card inspection, Load, Restart, and Solver Details.
- Completed-control rule: Player verdict, Hint, Solve Next, and Auto Solve are disabled. Programmatic handler guards also prevent stale or meaningless reasoning calls after completion; Solver Details remains enabled.
- Auto Solve rule: Each scheduled callback carries a GUI lifecycle generation. Completion stops immediately after the final accepted reveal, schedules no next step, and Restart/Load invalidate any stale generation after cancelling the known callback.
- Lifecycle rule: Restart and successful Load clear character/clue selection through the controller, and clear clue highlights, newly revealed emphasis, Hint session/support/target, trace-source metadata, completion presentation, and pending Auto Solve state in the app.
- Public/private verification: completion and clue inspection use public snapshots and stable public IDs only. No private Puzzle field, hidden status/solution, unrevealed clue lookup, clue-text parser, or new resolver was introduced.
- Branding decision: The production window title is consistently `Griductive`; no capture/smoke/debug/test-harness title exists in production GUI code.
- Accepted suggestions: public interaction DTO, canonical resolver reuse, selected-clue auto-scroll, persistent completed board, compact textual completion banner, completion-aware controls, handler guards, and generation-token callback invalidation.
- Rejected/deferred: hidden-solution comparison, unrevealed clue lookup, clue text inference, new solver semantics, completion overlay replacing the board, timed animation, player marks, optional counters, and all Phase 8 work.
- Human verification performed: Foreground screenshots were inspected for initial/partial states, unresolved selection, solved-card clue spotlight, grounded Hint Stage 1, target-only Stage 2, manual completion, Auto Solve completion, Solver Details after completion, Restart, Load, long 4x4 clue scrolling, and low-height completion. The first capture attempt was rejected because another window covered Tkinter; the corrected foreground run produced 16 valid captures. A clipped low-height status presentation was found and corrected by compacting the completion banner and hiding the now-obsolete verdict instruction while complete.
- Tests performed: supported full runner passed 174/174 (155 existing plus 19 Phase 7 tests); compile, diff, protected-file, external-solver, GUI-hidden-data, and production-title scans passed. Tkinter smoke covered 3x3/4x4 at 1180x800 and 1180x660; the final low-height check reported 9/9 visible textual verdict badges and bottom edge 625/660. `pytest` remains unavailable with `No module named pytest` and was not installed.
- Approved Phase 6.5 commit: `ba7912b1ea64487cde55ae198cae1a648e363036` (`feat(agent): add grounded hint support extraction`).
- Related Prompt ID: PROMPT-011
- Related Git commit hash: `4150d867b6f2ce03cf273ced9895c4dd06105445`

## AI-015

- Date: 2026-08-16
- AI tool: OpenAI Codex
- Model: GPT-5
- Developer/member: Tran Huu Phuoc - 24127511
- Phase: UI Phase 8 final regression, requirement audit, and demo readiness
- Purpose: Perform an evidence-first final source audit against the 9-page Project 2 PDF, repair verified release-readiness defects, and prepare reproducible experiment/demo/report evidence without creating or uploading final submission artifacts.
- Files affected: `README.md`; new `experiments/run_experiments.py`, `experiments/results/final_regression.json`, and `tests/test_final_audit.py`; final audit/demo/limitations/report-support documents; and project logs.
- Audit decision: Preserve solver/gameplay behavior. Classify requirements from source/tests/runtime evidence as PASS, PARTIAL, or BLOCKED. Do not convert missing report/video/archive/team data into fabricated completion claims.
- Verified defect: The repository had four validated puzzles but no runnable experiment harness and `EXPERIMENT_LOG.md` said no experiments had run. Added a standard-library runner that discovers all puzzle JSON files, records required counts/work/runtime/reveal/uniqueness/Hint metrics, retains exceptions as FAIL rows, writes raw JSON, and returns non-zero on failure.
- Experiment result: 4/4 puzzles PASS (two 3x3, two 4x4); all complete without guessing and all complete clue sets are consistent/unique. The raw snapshot records 19-38 progressive SAT calls and 100-327 propagations; these unit-propagation chains produced 0 decisions/backtracks, while dedicated DPLL tests exercise both.
- UI verification: One continuous 3x3/4x4 rehearsal covered NOT_PROVABLE, CONTRADICTED, ACCEPTED, solved-card clue inspection/highlight, grounded Hint stages, Solve Next, Auto Solve, completion, Solver Details, Restart, Load, scrolling, and 1180x660 layout. Eighteen captures were visually inspected and temporary evidence was removed after review.
- Git verification: Approved Phase 7 was committed exactly as `4150d86`. After fetch, local `main` was 9 commits ahead of and 0 behind `origin/main`; no push/upload is claimed.
- Accepted: reproducible raw experiments, five narrow release-audit tests, final requirement matrix, report technical support, timed demo script, honest limitations, clean entrypoint/visual/boundary validation, and explicit submission blockers.
- Rejected/deferred: new solver/gameplay semantics, optional 5x5, external test/SAT packages, globally minimum Hint proof, final PDF generation, video recording/hosting, archive creation, pushing, submission, invented team percentages, and fake links/hashes.
- Tests performed: 179/179 supported unittests PASS; compile and diff checks PASS; external-solver/public-boundary scans PASS; four-puzzle experiment run PASS; clean `python main.py` window launch PASS; 3x3/4x4 E2E/visual and low-height checks PASS. `pytest` remains unavailable with `No module named pytest` and was not installed.
- Approved Phase 7 commit: `4150d867b6f2ce03cf273ced9895c4dd06105445` (`feat(gui): finalize gameplay completion experience`).
- Related Prompt ID: PROMPT-012
- Related Git commit hash: `2c8ed1bd2f6edcdddd6583355110ccdd00470a6d`

## AI-016

- Date: 2026-08-16
- AI tool: OpenAI Codex
- Model: GPT-5
- Developer/member: Tran Huu Phuoc - 24127511
- Phase: Phase 8.5 puzzle quality, deduction difficulty, and screen navigation
- Purpose: Replace the shipped-set demonstration gap with validated Standard/Advanced reasoning puzzles and add a same-root public-only puzzle catalog without altering protected solver semantics.
- Initial audit: Gallery Shift and Museum Circuit were pure direct FACT chains (8/8 and 15/15 direct deductions). Implication Archive still had 11 direct FACT steps. Parity Gallery averaged support 1.75/max 2 but lacked counting and non-EXPLICIT regions.
- Puzzle design decision: Retain Gallery Shift as an explicit Tutorial. Add The Atrium Ledger Standard 3x3 with row counts/relations and The Meridian Conspiracy Advanced 4x4 with counting, all four regions, IMPLIES/ODD, and real multi-component support. Candidate data was accepted only after semantic truth, uniqueness, progressive completion, and Hint analysis passed.
- Standard evidence: 2 initial clues; 7/7 progressive deductions; average/max support 2/2; 1 late FACT anchor; 0 direct single-FACT deductions; complete CNF 24 clauses; final recorded whole solve 0.001696s.
- Advanced evidence: 3 initial clues; 13/13 progressive deductions; average/max support 2.308/4; initial support `A4-01 + A4-04 + known A1`; all region kinds plus both extensions; 1 late FACT anchor; 0 direct single-FACT deductions; 54 clauses; 17 decisions/1 backtrack; final recorded whole solve 0.012332s.
- Navigation design: `ScreenManager` switches Game/PuzzleSelect frames in one root. Catalog DTOs contain only ID/name/size/category/description. Open/Back is presentation-only; Play resolves a local file, then reuses `PuzzleLoader` and `GameController.load()` plus existing transient/Auto generation cleanup. External Load remains.
- Accepted: Tutorial/Standard/Advanced catalog, public current-puzzle badge, scrollable 1180x660 layout, development-time public support profiler, updated six-puzzle experiments, and explicit design-category wording.
- Rejected: puzzle-specific CNF/Hint/target order, hidden-data catalog fields, solver/DPLL/support algorithm changes, random unvalidated puzzle retention, arbitrary numeric difficulty score, accounts/unlocks/stars/cloud, and Phase 9/report generation.
- Tests performed: 196/196 supported unittests PASS at implementation checkpoint; 17 new tests cover puzzle quality/support and 14 navigation/privacy/lifecycle requirements. Six-puzzle quality/experiment runs passed with 0 failures. DPI-aware 21-capture visual E2E passed Tutorial, Puzzle Select, Standard, Advanced, Solver Details, completion, scrolling, and 1180x660.
- Revalidation: Repeated on 2026-08-18 after the Phase 8.5 prompt was supplied again. The unchanged worktree passed 196/196 tests in 8.012s, compile, protected-module diff, JSON parsing, public/private, hidden-data, external-solver, puzzle-specific logic, and whitespace scans. No production file or generated experiment result was rewritten.
- Approved Phase 8 commit: `2c8ed1bd2f6edcdddd6583355110ccdd00470a6d` (`chore(project): complete final requirement audit`).
- Related Prompt ID: PROMPT-013
- Related Git commit hash: `8c8c77d326ceb65beaa7b5454bc0bcd49f9da355`

## AI-017

- Date: 2026-08-18
- AI tool: OpenAI Codex
- Model: GPT-5
- Developer/member: Tran Huu Phuoc - 24127511
- Phase: Phase 8.6 production puzzle hardening, non-linear reveals, and anti-guess lock
- Purpose: Convert the Phase 8.5 showcase into a strict two-puzzle production set, remove direct answer anchors, make public reveal ownership non-linear, and prevent repeated manual opposite-verdict guessing without changing protected reasoning semantics.
- Checkpoint: Verified and preserved real Phase 8.5 commit `8c8c77d326ceb65beaa7b5454bc0bcd49f9da355` before edits; Phase 8.6 was committed only after approval as `96cd8ae68a0592e456547f6cccde3789f7a61163`.
- Puzzle result: Production catalog now contains only Atrium Ledger Standard 3x3 and Meridian Conspiracy Advanced 4x4. Both have zero FACT clues, deterministic scattered initial cells, non-linear reveal owners, complete-set uniqueness, progressive completion, and zero support-size-1 steps.
- Legacy handling: Four former direct-chain puzzle JSON files were moved intact to `tests/fixtures/puzzles/`; test path imports were centralized in `tests/fixture_paths.py`; production experiments derive only from the explicit catalog.
- Anti-guess design: A CONTRADICTED manual submission adds the unresolved ID to controller-owned per-run state. Retry is blocked before the engine call. The lock is neutral, reveals neither correct status nor clue, and is ignored by Hint/Solve Next/Auto Solve. Restart/Load clear it.
- Accepted AI-assisted changes: explicit production manifest, deterministic design-time clue remapping saved as static JSON, zero-FACT production data, legacy fixture separation, controller-owned manual locks, public-only neutral presentation, stronger metrics/tests, and reproducible reruns.
- Rejected/deferred suggestions: runtime/random shuffling, puzzle-specific target/support/CNF branches, hidden-answer comparison, placing locks in public or solver state, locking NOT_PROVABLE/INCONSISTENT, exposing the opposite answer, weakening solver assistance, deleting FACT engine support, optional 5x5, and Phase 9 work.
- Protected scope: No changes to `game/`, `core/`, `agent/`, `logic/`, or `sat/`; no random runtime generation, hidden-answer inspection, puzzle-specific solver path, or verdict semantic change.
- Evidence: 212 supported unittests, production quality/experiment runners, protected/boundary scans, and a 12-state Tkinter Standard/Advanced visual E2E are the Phase 8.6 gates; exact final results are recorded in `TEST_LOG.md`.
- Related Prompt ID: PROMPT-014
- Related Git commit hash: `96cd8ae68a0592e456547f6cccde3789f7a61163`

## AI-018

- Date: 2026-08-19
- AI tool: OpenAI Codex
- Model: GPT-5
- Developer/member: Tran Huu Phuoc - 24127511
- Phase: Phase 8.7 production puzzle expansion
- Purpose: Add exactly four validated main puzzles (1x3x3, 1x4x4, 2x5x5), establish objective non-clone evidence, and make the existing GUI readable at 5x5 without changing solver semantics.
- Checkpoint: Verified clean real starting commit `c347ef05f808a94c90f5529139f80cf10abca8cf`; no amend/rebase/squash or Phase 8.7 commit was made.
- Candidate process: Offline construction used complete assignments only for semantic/uniqueness validation. Two early 3x3/4x4 candidates were repaired after the uniqueness checker found secondary models. The original unique Obsidian chain was rejected as too similar in dependency shape to Celestial; its first branched revision exposed a second model; the accepted revision is a connected, unique branched forced-frontier DAG.
- Accepted puzzles: `intermediate-cipher-3x3` / The Cipher Courtyard; `advanced-lantern-4x4` / The Lantern Assembly; `expert-orbit-5x5` / The Celestial Registry; `expert-parity-5x5` / The Obsidian Concord.
- Quality evidence: All four are FACT-free, unique, consistent, and fully progressive. New step counts are 7/13/20/19; every support is >=2; 5x5 maximum supports are 5 and 4. Same-size final-solution Hamming distances across the six-puzzle catalog are 5/11/16 and no comparison is flagged suspicious.
- GUI decision: Added presentation-only standard/compact/dense tiers and dense button styles. 5x5 retains identity, profession, coordinate, status badge, selection/modifiers, complete clue panel data, controls, trace, and completion; only the redundant in-card clue preview is suppressed.
- Protected scope: No diff in DPLL, CNF encoder, semantic evaluator, Hint support extractor, uniqueness checker, or LogicAgent. No external solver, puzzle-ID reasoning branch, hidden GUI/agent dependency, or runtime puzzle generation was introduced.
- Evidence: 228/228 supported unittests PASS; 6/6 experiment runs PASS; compile, whitespace, schema, boundary, external-solver, and puzzle-specific scans PASS; DPI-aware 3x3/4x4/5x5/Puzzle Select/Solver Details/completion review PASS. The audit display capped requested 800 height at 701; the stricter 1180x660 target rendered exactly and passed.
- Rejected/deferred: unreadable card shrink, board data removal, solver optimization, direct FACT anchors, cloned 5x5 dependency paths, final PDF/report generation, commit, push, video, and Phase 9.
- Related Prompt ID: PROMPT-015
- Related Git commit hash: uncommitted; previous checkpoint `c347ef05f808a94c90f5529139f80cf10abca8cf`
