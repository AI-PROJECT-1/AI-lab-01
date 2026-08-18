# Decision Log

## DEC-001 - Immutable public snapshot boundary

- Context: The engine owns hidden labels and unrevealed clues while every agent must use public information only.
- Options considered: pass engine directly; pass mutable puzzle subset; construct immutable public DTOs.
- Chosen option: Construct a new immutable `PublicKnowledgeState` snapshot for every agent call.
- Reason: It makes hidden-data access structurally unavailable and easy to test.
- Consequences: Small copy cost; clearer interfaces; tests can inspect the DTO recursively.
- Related requirement: PDF sections 4.1 and 4.2.
- Related commit: `81e5882`, `bcf0393`

## DEC-002 - Standard-library desktop GUI for early phases

- Context: A GUI is mandatory, while Phases 01-04 should avoid unnecessary dependency setup.
- Options considered: Tkinter desktop, third-party desktop toolkit, web frontend.
- Chosen option: Tkinter desktop GUI.
- Reason: Ships with CPython, keeps the project Python-only, and allows business logic to remain headless-testable.
- Consequences: GUI visual checks require a display; styling is intentionally modest.
- Related requirement: PDF section 4.1.
- Related commit: `3dec8a9`

## DEC-003 - Development mock recognizes public FACT clues only

- Context: Phase 04 needs manual gameplay before the production agent exists.
- Options considered: inspect hidden solution; accept every verdict; scripted hidden answers; minimal public FACT classifier.
- Chosen option: A clearly named mock classifies only statuses explicitly present in public FACT clues or already proved verdicts.
- Reason: It enables honest manual-flow testing without guessing or reading hidden data.
- Consequences: The sample puzzle uses a FACT chain; general reasoning is deferred to Phases 05-10.
- Related requirement: PDF sections 2.2 and 4.1.
- Related commit: `bcf0393`, `3dec8a9`

## DEC-004 - Direct combinational cardinality encoding

- Context: Core puzzle regions are small and the PDF explicitly permits direct combinational encoding.
- Options considered: direct combinations; sequential counters with auxiliary variables; external SAT/cardinality library.
- Chosen option: Encode AT_LEAST and AT_MOST using combinations of primary literals; EXACTLY is their conjunction.
- Reason: It is dependency-free, explainable in an oral interview, and easy to verify exhaustively for 3x3 cases.
- Consequences: Auxiliary-variable count is zero; clause growth is combinatorial and may be slower for large regions.
- Related requirement: PDF sections 3.3 and 4.2.
- Related commit: `2409aa7`; validation corrections consolidated in `03584c3859a12e7a57385a7d860e48f084d0c210`.

## DEC-005 - One standard-library test runner

- Context: The repository documented `unittest`, but the DPLL tests were written as pytest functions and were skipped by the documented command.
- Options considered: add pytest as a test dependency; convert DPLL tests to `unittest`; maintain two commands.
- Chosen option: Convert DPLL tests to `unittest` and keep one dependency-free discovery command.
- Reason: It prevents silent test omission and matches the existing repository policy.
- Consequences: All implemented phases are covered by `python -m unittest discover -s tests -v`.
- Related requirement: Master prompt sections 16, 24, and 25.
- Related commit: `03584c3859a12e7a57385a7d860e48f084d0c210`.

## DEC-010 - Public contextual verdicts and semantic feedback

- Context: Manual verdict buttons were always active and verdict results appeared as raw status strings, while UI Phase 3 requires contextual actions and distinct feedback without changing engine semantics or inspecting hidden puzzle data.
- Options considered: let the GUI query hidden status; parse the engine message; change `SubmissionResult`; derive presentation from the outcome plus public snapshots and public card view models.
- Chosen option: Build `VerdictContext` exclusively from `CardViewModel`, map each existing `VerdictOutcome` to a typed `GameplayFeedback`, and detect a fresh reveal by comparing immutable public snapshots around the unchanged submission call.
- Reason: Button availability, wording, and transient emphasis remain testable presentation decisions while `GameEngine.submit_verdict()` stays the sole authority that can mutate public progress.
- Consequences: Buttons disable for no selection or a resolved selection; rejected/inconsistent results retain the public snapshot; accepted results refresh the board and add a temporary outline. Load/Restart clear all transient state.
- Privacy rule: Feedback never copies the engine's free-form verdict message, forced opposite status, hidden solution, or unrevealed clue. Accepted feedback refers to a clue only after it exists in the refreshed public state.
- Responsive rule: Context identity and feedback use compact single-row surfaces; 4x4 cards use a one-row identity header and horizontal public status/preview row.
- Related requirement: Griductive GUI fidelity refactor UI Phase 3 contextual verdict interaction and public feedback requirements.
- Related commit: `bd3926325795dce94afb9d719889e6071e823446`.

## DEC-006 - Extension selection: IMPLIES and ODD

- Context: The specification requires at least two distinct extensions and a formal review of at least three candidates before selection.
- Options considered:
  - `IMPLIES(A,B)`: low semantic complexity; one CNF clause; straightforward exhaustive tests; easy to explain as material implication.
  - `ODD(region)`: medium semantic complexity; truth-table blocking CNF grows exponentially with the region but remains practical for 3x3/4x4 clue regions; exhaustive tests are direct; demonstrates parity reasoning clearly.
  - `NOT_BOTH(A,B)`: low semantic/CNF/test complexity, but semantically duplicates `AT_MOST(1)` over a two-cell explicit region and adds little report value.
  - `MAJORITY(region)`: low-medium complexity, but reduces directly to an existing `AT_LEAST(ceil(|R|/2))` clue and is not sufficiently distinct.
- Chosen option: `IMPLIES` and `ODD`.
- Reason: They are semantically distinct from each other and from the six core templates; one demonstrates relational implication and the other parity over regions.
- Consequences: `IMPLIES` adds no auxiliary variables and one clause. `ODD` uses one blocking clause per even-parity assignment, so it is intentionally limited to puzzle-sized regions and documented as combinatorial.
- Related requirement: Master prompt sections 9, 15, and Phase 12; PDF extension requirement.
- Related commit: `03584c3859a12e7a57385a7d860e48f084d0c210`.

## DEC-007 - Progressive solving is orchestrated by GameEngine

- Context: Auto Solve must update the public KB and reveal a new clue only after a verdict is proved, while the LogicAgent must never receive hidden puzzle state.
- Options considered: give the agent the engine; let the agent mutate public state; compute all answers from one snapshot; let the engine request one public deduction per wave.
- Chosen option: `LogicAgent.solve_next(public_state)` returns one proof-backed deduction, and `GameEngine` verifies/reveals it before creating the next snapshot.
- Reason: This preserves the hidden/public boundary and ensures every wave includes only clues legitimately revealed by earlier proofs.
- Consequences: More SAT calls than a batch mutation approach, but deterministic traceability and correct progressive semantics.
- Related requirement: Master prompt sections 11-13, 17-18, and Phases 09-10.
- Related commit: `03584c3`.

## DEC-008 - Tokenized ttk visual foundation with semantic control groups

- Context: The functional Tkinter GUI needs a clearer game-oriented hierarchy, but UI Phase 1 may not change gameplay, reasoning, trace data, or hidden/public boundaries.
- Options considered: continue per-widget styling; adopt a third-party theme; replace Tkinter; define project-owned ttk design tokens and reusable presentation primitives.
- Chosen option: Keep Tkinter/ttk and centralize color, spacing, typography, button styles, header, feedback shell, and control-group primitives in `gui/theme.py` and `gui/components.py`.
- Reason: This creates a consistent visual language without adding dependencies, copying proprietary assets, or coupling presentation to AI/game state.
- Consequences: Existing card and clue content remain intentionally unchanged until their approved phases. Controls are visually grouped as GAME, PLAYER VERDICT, ASSISTANCE, and SOLVER while retaining the same callbacks. The trace remains visible and intact in Phase 1.
- Responsive rule: Default 1180x800 layout and size-aware board geometry must accommodate both current 3x3 and 4x4 puzzles; container columns retain flexible weights.
- Hint rule: The UI must not describe a latest or active clue as a unique deduction cause because the agent does not provide a proof anchor.
- Related requirement: Griductive GUI fidelity refactor sections 1-4, 13-16, 21-24; Project 2 GUI requirements.
- Related commit: `f6b5713`.

## DEC-009 - Public-only CharacterCard with composable base and modifier states

- Context: Board cards must feel like character cards, remove unresolved debug metadata, preserve accessible verdict text, and retain selection plus canonical clue highlighting without altering game or solver behavior.
- Options considered: continue rendering one multiline Button string; maintain one mutually exclusive style per state combination; use external portrait assets; introduce a reusable card component with deterministic initials and layered visual state.
- Chosen option: `CharacterCard` consumes only `CardViewModel`; `CardBaseState` controls unresolved/criminal/innocent identity while independent modifier outlines represent selected, clue-highlighted, and newly-revealed states.
- Reason: Layered state prevents highlight or selection from replacing verdict identity, and the public view-model boundary makes hidden-data leakage structurally unnecessary.
- Avatar decision: Derive initials from public names and choose from a project-owned palette using public character IDs. No network, image dependency, or copyrighted asset is required.
- Clue decision: Show a bounded preview only when `clue_text` exists publicly. Use 52 characters for 3x3 and 28 for 4x4; full public clue text remains in the existing clue panel.
- Responsive consequence: Character identity uses a horizontal avatar/name/profession/coordinate header. The default geometry is bounded to the current screen, and 4x4 card height is kept within its allocated board row.
- Accessibility consequence: Revealed cards always contain literal `CRIMINAL` or `INNOCENT` badges; color only reinforces the status.
- Related requirement: Griductive GUI fidelity refactor UI Phase 2; Project 2 board, coordinate, verdict, clue, and privacy requirements.
- Related commit: `48bea9d038c7425a691b09d2bd8a2049b3825d0e`.

## DEC-011 - Public-only scrollable ClueCards with canonical selection

- Context: The revealed-clue list exposed complete public data as raw log rows, but UI Phase 4 requires readable ownership, full text, selected/new states, and scalable inspection without changing clue semantics.
- Options considered: retain Listbox strings; parse rendered text to infer highlights; duplicate region handling in GUI; build public clue view models/cards and retain the controller's canonical resolver path.
- Chosen option: Build `ClueCardViewModel` only from `PublicKnowledgeState.revealed_clues`, render cards inside a scrollable Canvas, and compose selected/newly-revealed outlines independently.
- Reason: Public DTO construction structurally excludes unrevealed clues, full text is preserved without packing it into board cards, and selection continues through the already tested canonical `referenced_cells()` function.
- Consequences: Owner name/coordinate and full wrapped clue text are primary; clue ID remains secondary. Overflow scrolls without shrinking the board, and the newly public clue can auto-scroll into view.
- State-composition rule: Character selected, clue-highlighted, base verdict, and newly-revealed modifiers remain independent; clue selection does not replace Criminal/Innocent identity.
- Reset rule: Restart and successful Load clear clue selection, highlight, and new-clue emphasis through existing controller and app resets.
- Related requirement: Griductive GUI fidelity refactor UI Phase 4 revealed clue presentation, canonical highlighting, privacy, and responsive inspection requirements.
- Related commit: `dff07f05a003fa966c200fc925e5da600846ec54`.

## DEC-012 - Fingerprinted two-stage Hint presentation

- Context: Repeated Hint clicks called `get_hint()` repeatedly, duplicated reasoning trace entries, and risked overclaiming an active clue as the direct proof cause even though the current API establishes no unique proof anchor.
- Options considered: call reasoning on every click; expose the full existing Hint message/verdict; infer a causal clue from order; cache only public presentation fields and split assistance into active-clue review then target identity.
- Chosen option: Stage 1 calls the unchanged Hint API once and filters trace `active_clue_ids` through current public reveals. Stage 2 uses the cached public target only when the public-state fingerprint is unchanged.
- Reason: The first step guides review without causal invention; the second provides more assistance without another DPLL/trace request, verdict reveal, or game mutation.
- Fingerprint rule: Puzzle ID, ordered public known verdicts, public revealed owner/clue IDs, and completion identify knowledge. Character/clue selection is intentionally excluded because it is presentation-only.
- Privacy rule: Do not cache or display `HintResult.message`, deduction status, unrevealed clue content, Puzzle state, GameEngine fields, or solver internals. Active clues are not described as proof anchors.
- Invalidation rule: Manual accepted mutation, Solve Next, Auto Solve, Restart, Load, or any fingerprint mismatch clear/prevent cached target use; selection alone does not.
- Composition rule: Active clue and target hint outlines remain independent from selected clue/character, canonical clue highlight, newly revealed outline, and Criminal/Innocent base identity.
- Related requirement: Griductive GUI fidelity refactor UI Phase 5 progressive Hint UX and public-boundary requirements.
- Related commit: `d2682b3ebccdf087c417a90b50488def293c79ce`.

## DEC-013 - Secondary structured Solver Details with GUI-owned source metadata

- Context: The raw Solver Trace Listbox permanently consumed a large share of the gameplay sidebar, while Project 2 still requires complete deduction-step, active-clue, SAT-query, verdict, and reveal trace inspection.
- Options considered: retain the Listbox; collapse it inside the sidebar; add a tab that replaces gameplay; open a lazy secondary Toplevel containing structured scrollable step cards.
- Chosen option: Keep normal play board-first and dedicate the sidebar to Revealed Clues; expose Solver Details through an explicit SOLVER control that opens a lazy, independently scrollable Toplevel.
- Reason: A secondary window preserves the responsive 3x3/4x4 board and keeps technical detail accessible without making it the default game experience.
- Trace rule: Presentation copies only fields directly present in `DeductionTraceStep` and `SATQueryTrace`: step number, target ID, verdict, ordered active clue IDs, query purpose/assumption/result, per-query decisions/propagations/backtracks/runtime, and newly revealed clue ID. Missing fields are omitted or marked unavailable.
- Statistics rule: Solver statistics are labeled per SAT query. No cumulative totals or SAT-call meaning beyond the number of recorded query rows is inferred.
- Source rule: The GUI records the trace length immediately before an action and labels only the appended slice as HINT, MANUAL VERDICT, SOLVE NEXT, or AUTO SOLVE. Historical or otherwise unobserved steps have no source label; UNKNOWN is not fabricated.
- Privacy rule: The detail presenter receives solver trace records only. It does not inspect `Puzzle`, hidden status/solution, private `GameEngine` fields, or unrevealed clues, and does not generate stronger natural-language or clause-level proofs.
- Hint rule: Phase 5 Stage 1 can append the existing reasoning trace; Stage 2 only advances cached presentation and therefore cannot add a Solver Details step.
- Lifecycle rule: Auto Solve remains `after()`-driven. Restart and successful Load cancel the pending callback, clear source metadata with the engine trace reset, and keep an already open details window safely usable.
- Responsive rule: Main content and Board/Revealed Clues containers suppress oversized child requests so the bottom controls and feedback remain visible at the current 1180x660 low-screen geometry.
- Related requirement: Griductive GUI fidelity refactor UI Phase 6; Project 2 deduction-trace requirement.
- Related commit: `5673fe09c0cd1a47f10e3f75d7ac2344dec7820f`.

## DEC-014 - Trace-free deletion-irreducible Hint support

- Context: `active_clue_ids` describes every revealed clue in the current KB, so it is valid trace context but not a logically grounded explanation of which constraints are needed for a forced Hint target.
- Options considered: keep generic active clues; guess one recent clue; remove arbitrary CNF clauses; enumerate globally minimum component subsets; greedily delete structured public support components using the existing entailment path.
- Chosen option: Keep `solve_next()` as the sole target selector, then run deterministic deletion reduction over whole revealed clues and proved-verdict unit constraints using a shared pure SAT-classification helper.
- Shared-entailment rule: `agent.entailment.classify_public_target()` owns the existing KB consistency and two-assumption classification sequence. `LogicAgent` converts its query records into normal trace steps; support diagnostics consume the same result without generating steps.
- Baseline rule: The current public KB must be consistent, the target unresolved, and the exact existing Hint status still entailed. Otherwise no explanation is returned and presentation falls back safely.
- Component order: Revealed clues sort by `(clue.id, owner_id)` and are tested first; proved verdicts then sort by their character's `(row, column, id)`. Set iteration never controls result order.
- Grouping rule: Removing a clue removes its entire structured clue object and therefore every clause produced by its canonical encoder as one component. No displayed text or individual generated clause is interpreted independently.
- Same-verdict rule: A deletion is accepted only when the reduced public KB still classifies the target as the exact original `Classification`; UNKNOWN, opposite verdict, or INCONSISTENT never qualify.
- Irreducibility rule: After the deterministic pass, no remaining component can be individually deleted while retaining the same forced verdict. Monotonic removal from a consistent propositional KB makes a second pass unnecessary.
- Minimum distinction: Greedy deletion depends on stable removal order and establishes deletion irreducibility, not global minimum cardinality, uniqueness, or a proof anchor.
- Trace/metrics rule: Support diagnostics do not mutate `last_trace` or the step counter. Their SAT-call count and wall runtime are carried separately on `HintExplanation`; Solver Details remains a view of gameplay deduction trace only.
- UI/fallback rule: Stage 1 caches only fingerprint-bound public support IDs and highlights corresponding clue cards/known verdict cards. Unsupported, failed, empty, duplicate-ID, or nonpublic explanation data reuses Phase 5 active-clue wording. Stage 2 clears support visuals and shows only the cached target.
- Protected-scope rule: DPLL, CNF encoder/semantics, GameEngine, PublicKnowledgeState, puzzles, uniqueness, experiments, and Solver Details presentation remain unchanged.
- Related requirement: Phase 6.5 Hint explanation fidelity and Project 2 public-only entailment requirements.
- Related commit: `ba7912b1ea64487cde55ae198cae1a648e363036`.

## DEC-015 - Public card activation and derived completion state

- Context: UI Phase 7 requires revealed character cards to inspect their public clue and requires a clear end state without weakening the hidden/public boundary or changing gameplay deductions.
- Options considered: keep every card click as verdict selection; inspect the engine's private card; infer clue ownership from text; route clicks by public clue presence and derive completion from the public completion signal.
- Chosen option: Add `GameController.activate_character()`. If `PublicKnowledgeState.clue_for(character_id)` is absent, retain normal unresolved verdict selection. If present, clear verdict selection, select the exact public owner clue, and reuse the existing canonical `select_clue()` result.
- Highlight/scroll rule: The app stores only the returned canonical referenced IDs; `CluePanel` scrolls a selected owner card into view after layout. Existing base verdict, selection, Hint, support, newly revealed, and clue-highlight modifiers remain independent.
- Completion source: `CompletionPresentation` is derived exclusively from `PublicKnowledgeState.is_complete`. No GUI comparison with a solution or private engine status exists.
- Completion-control rule: Disable verdict, Hint, Solve Next, and Auto Solve while complete. Keep Load, Restart, Solver Details, the completed board, direct clue selection, and solved-card clue inspection available.
- Auto Solve rule: After a final reveal, render completion and stop without scheduling another callback. A monotonically increasing presentation generation invalidates callbacks captured before Restart or Load.
- Reset rule: Restart and successful Load clear controller selections, clue highlights, newly revealed emphasis, Hint session/support/target, trace-source metadata, completion display, and pending Auto Solve state. Completion itself is recomputed from the new public snapshot.
- Copy/branding rule: Completion says every character was logically resolved from public clues, never that guesses matched a hidden answer. The production title is `Griductive`; test-harness titles remain test-only.
- Rejected/deferred: private Puzzle access, unrevealed clue mapping, natural-language parsing, new reasoning calls on card inspection, solver or Hint rewrites, board-replacing overlay, counters, animations, and player marks.
- Related requirement: UI Phase 7 gameplay completion/final polish and Project 2 public/private isolation.
- Related commit: `4150d867b6f2ce03cf273ced9895c4dd06105445`.

## DEC-016 - Reproducible final evidence without submission fabrication

- Context: The Project 2 audit required actual experiments and submission-readiness evidence, but the repository contained only an empty results directory and a log stating that no experiment had run. Phase 8 explicitly prohibited report/video/archive/upload work and fabricated team data.
- Options considered: mark experiments as planned; hand-copy selected timings; install an external benchmark framework; add a standard-library discovery runner with raw failure-preserving output; generate all final submission artifacts automatically.
- Chosen option: Add one deterministic standard-library runner over every distributable puzzle and retain its raw JSON snapshot for the proposed Phase 8 commit. Keep failures/exceptions as rows and make them fail the process. Prepare report-support notes and a timed demo script, but classify absent artifacts honestly as PARTIAL/BLOCKED.
- Metric boundary: Progressive DPLL query statistics come only from existing trace DTOs. Whole-solve, uniqueness, and fresh-engine Hint support wall times are measured separately. Machine-specific runtimes are never represented as guarantees.
- Scope rule: No GameEngine, LogicAgent, CNF, DPLL, verdict, Hint, trace, completion, or puzzle semantics change is authorized. Tests may validate terminal behavior and experiment schema only.
- Attribution rule: Git hashes come from real history. Phase 8 was committed as `2c8ed1b` and Phase 8.5 as `8c8c77d`. Team names/IDs/percentages, references approval, video URL, report, and archive cannot be inferred or fabricated.
- Related requirement: Project 2 Sections 4.5-4.7 and Section 5; UI Phase 8 final audit/demo readiness.
- Related commit: `2c8ed1bd2f6edcdddd6583355110ccdd00470a6d`.

## DEC-017 - Design-category puzzles and same-root public catalog

- Context: The original shipped suite proved correctness but overrepresented direct FACT chains, so it did not visibly demonstrate counting, non-EXPLICIT regions, multi-clue support, or DPLL branching. Players also needed a native shipped-puzzle selector while external Load remained useful.
- Options considered: relabel old chains only; change solver target ordering; hard-code Hint support; replace Tutorial; add validated deduction-focused puzzles; open a second application/window; or switch two frames inside the existing root.
- Puzzle choice: Preserve Gallery Shift as an honest Tutorial. Add Atrium Ledger Standard and Meridian Conspiracy Advanced. Late FACT anchors may establish full-set uniqueness but must not participate in progressive direct-answer steps. Difficulty names are design categories, not calculated scores.
- Candidate gate: A puzzle is shipped only after loader/domain validation, all-clue semantic truth, complete-set consistency/uniqueness, progressive no-guess completion, deterministic support profile, and Hint compatibility. No hidden status is supplied to LogicAgent or support extraction.
- Advanced evidence: Initial B1 deduction requires public clues `A4-01`, `A4-04`, and known verdict A1. The same generic DPLL records 17 decisions and 1 backtrack across progressive queries; no puzzle ID branch exists.
- Navigation choice: Use one root and a small `ScreenManager`. Opening/Back only changes frame visibility and preserves public/game/UI state. Play loads through the existing loader/controller APIs, cancels stale Auto callbacks, clears transient presentation, and returns to Game.
- Catalog boundary: Presentation metadata is exactly ID, name, size, category, and description. File resolution is private; no status distribution, clue payload, future target, or solution enters the catalog.
- Related requirement: Phase 8.5 puzzle quality, real multi-component Hint, local screen navigation, and public/private isolation.
- Related commit: `8c8c77d326ceb65beaa7b5454bc0bcd49f9da355`.

## DEC-018 - Production-only deduction catalog and session-level manual lock

- Context: Phase 8.5 still exposed a direct Tutorial and retained one late FACT anchor in each deduction-focused puzzle. A contradicted manual verdict also allowed immediate opposite retry, turning rejection into a low-cost answer oracle.
- Production-set choice: Ship exactly Atrium Ledger Standard 3x3 and Meridian Conspiracy Advanced 4x4. Retain legacy chains intact as test fixtures so semantic coverage and history are preserved without representing them as gameplay difficulty.
- Puzzle gate: Production data must be deterministic, semantically true, consistent, unique, progressively solvable, FACT-free, scattered at initialization, non-linear in clue-owner reveal order, and have no support-size-1 deduction. Runtime code contains no generator, seed, target list, or puzzle-ID branch.
- Lock ownership: Store manually contradicted unresolved IDs in `GameController`, not GameEngine or PublicKnowledgeState. This is interaction state: it can disable manual verdict buttons and draw a neutral lock badge but cannot become a logical unit or reveal.
- Information rule: Feedback says only that public clues contradict the attempted verdict and that the character is locked. It must not name the forced opposite/correct status or inspect `forced_status` to construct presentation.
- Operation rule: Only manual verdict retry is blocked. NOT_PROVABLE, ACCEPTED, and INCONSISTENT do not create a lock. Hint, Solve Next, and Auto Solve remain unchanged and can resolve locked characters; Restart and Load clear the lock set.
- Experiment boundary: Production analysis follows the explicit catalog. Test fixtures are never discovered by glob, and generated JSON records the exact production manifest and real baseline hash.
- Rejected: changing GameEngine/verdict semantics, adding lock fields to public/domain models, puzzle-specific CNF/LogicAgent order, random runtime generation, disabling logical assistance, hiding Solver Trace, or showing the correct answer as a penalty.
- Related requirement: Phase 8.6 production hardening, public/private isolation, and no-guess gameplay.
- Related commit: UNCOMMITTED - approval required.
