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
- Related commit: `2409aa7`; validation corrections are PENDING.

## DEC-005 - One standard-library test runner

- Context: The repository documented `unittest`, but the DPLL tests were written as pytest functions and were skipped by the documented command.
- Options considered: add pytest as a test dependency; convert DPLL tests to `unittest`; maintain two commands.
- Chosen option: Convert DPLL tests to `unittest` and keep one dependency-free discovery command.
- Reason: It prevents silent test omission and matches the existing repository policy.
- Consequences: All implemented phases are covered by `python -m unittest discover -s tests -v`.
- Related requirement: Master prompt sections 16, 24, and 25.
- Related commit: `48bea9d038c7425a691b09d2bd8a2049b3825d0e`.

## DEC-010 - Public contextual verdicts and semantic feedback

- Context: Manual verdict buttons were always active and verdict results appeared as raw status strings, while UI Phase 3 requires contextual actions and distinct feedback without changing engine semantics or inspecting hidden puzzle data.
- Options considered: let the GUI query hidden status; parse the engine message; change `SubmissionResult`; derive presentation from the outcome plus public snapshots and public card view models.
- Chosen option: Build `VerdictContext` exclusively from `CardViewModel`, map each existing `VerdictOutcome` to a typed `GameplayFeedback`, and detect a fresh reveal by comparing immutable public snapshots around the unchanged submission call.
- Reason: Button availability, wording, and transient emphasis remain testable presentation decisions while `GameEngine.submit_verdict()` stays the sole authority that can mutate public progress.
- Consequences: Buttons disable for no selection or a resolved selection; rejected/inconsistent results retain the public snapshot; accepted results refresh the board and add a temporary outline. Load/Restart clear all transient state.
- Privacy rule: Feedback never copies the engine's free-form verdict message, forced opposite status, hidden solution, or unrevealed clue. Accepted feedback refers to a clue only after it exists in the refreshed public state.
- Responsive rule: Context identity and feedback use compact single-row surfaces; 4x4 cards use a one-row identity header and horizontal public status/preview row.
- Related requirement: Griductive GUI fidelity refactor UI Phase 3 contextual verdict interaction and public feedback requirements.
- Related commit: PENDING.

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
- Related commit: PENDING.

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
- Related commit: PENDING.
