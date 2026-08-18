# Architecture

## Security boundary

```text
Puzzle JSON
    |
    v
PuzzleLoader --> Puzzle (contains hidden solution and every clue)
                    |
                    v
               GameEngine  ---- private authoritative state
                    |
                    | creates immutable copy
                    v
          PublicKnowledgeState
                    |
                    v
          SAT-backed LogicAgent
              |          |
              v          v
          CNFEncoder   deduction trace
              |
              v
             DPLL
```

Only `GameEngine` and loader-side domain objects may hold hidden labels and
unrevealed clue objects. Agents receive a freshly constructed immutable
`PublicKnowledgeState`; they never receive `Puzzle` or `GameEngine`.

The GUI calls engine methods and renders public snapshots. It does not inspect
private puzzle state. The production `LogicAgent` receives only those snapshots;
the mock remains isolated to legacy tests.

## Dependency direction

- `core` depends only on the standard library.
- `game` depends on `core` and an agent protocol.
- `agent` depends on public `core` contracts; it must not import `game`.
- `gui` depends on public contracts and game commands.
- `logic` and `sat` remain independent of the GUI.

## Shared interface proposal

- `PuzzleLoader.load(path) -> Puzzle`
- `GameEngine.public_state() -> PublicKnowledgeState`
- `GameEngine.submit_verdict(character_id, status) -> VerdictResult`
- `GameEngine.restart() -> PublicKnowledgeState`
- `LogicAgentProtocol.classify(public_state, character_id) -> Classification`
- `GameEngine.get_hint() -> HintResult` (non-mutating)
- `GameEngine.solve_next() -> VerdictResult | None`
- `GameEngine.auto_solve() -> tuple[VerdictResult, ...]`
- `LogicAgent.check_uniqueness(complete_clue_state) -> UniquenessResult`

Auto Solve is progressive: after each proved verdict, `GameEngine` reveals that
card and calls the agent again with a fresh public snapshot. Puzzle uniqueness is
a separate clue-only operation that requires every clue and rejects verdict unit
clauses.

## Deduction versus Hint explanation

Deduction asks whether a character's verdict is logically entailed by the full
current `PublicKnowledgeState`. It produces the normal `DeductionTraceStep` used
by Solver Details.

Hint explanation runs only after the existing deduction workflow has selected a
forced target. It treats each revealed structured clue and each proved-verdict
unit as one public support component, then uses deterministic deletion checks to
find a deletion-irreducible supporting set. These checks reuse the same SAT
entailment helper but do not produce gameplay deduction steps. The result is not
claimed to be a globally minimum or unique proof, and it is not part of DPLL.

## Public interaction and completion presentation

Board-card activation is routed entirely from the current public snapshot. A
card without a public clue remains a verdict-selection target. A card whose clue
is already present in `revealed_clues` selects that exact public clue and reuses
the canonical region resolver to spotlight referenced cells; it performs no new
reasoning or gameplay command.

The completion banner and completed control state are derived only from
`PublicKnowledgeState.is_complete`. Completion leaves the board, public clues,
and Solver Details inspectable while disabling verdict, Hint, Solve Next, and
Auto Solve actions. Restart and Load replace the public snapshot and clear all
GUI-owned transient state; an Auto Solve generation token prevents a callback
from an earlier lifecycle from acting on the replacement puzzle.

## JSON design

The schema uses stable cell IDs such as `A1`, explicit `row`/`column` integers,
structured clue objects, and separate initial visibility. Hidden `status` is
loader/engine-only and is removed when public DTOs are created.

## Final evidence pipeline

`experiments.run_experiments` is an external observer of the existing public
game/agent contracts. It loads each distributable puzzle, records initial and
complete-clue CNF reports, executes the unchanged progressive solve, aggregates
existing trace metrics, runs the separate uniqueness check, and benchmarks
fresh-engine Hint support. It writes raw JSON and turns any exception or failed
completion/uniqueness result into a retained FAIL row and non-zero exit status.

This Phase 8 layer adds no edge to the production path: `main.py -> GUI ->
GameEngine -> LogicAgent -> CNFEncoder -> DPLL` remains unchanged. Documentation
and audit tests consume the evidence output; the game never consumes it.

## Puzzle catalog and UI-only navigation

`PuzzleCatalogEntry` contains only puzzle ID, display name, size, a human design
category, and short description. A private ID-to-local-file mapping resolves a
Play action; the catalog never loads or exposes solution labels, clue payloads,
or deduction sequences.

`ScreenManager` switches exactly two frames inside the existing Tk root:
`GriductiveApp` (Game) and `PuzzleSelectScreen`. Opening/closing Puzzle Select
only changes frame visibility. Play loads the selected file through
`PuzzleLoader` and the existing `GameController.load()` path, then reuses the
same lifecycle cleanup as external Load. Navigation state never enters
GameEngine, LogicAgent, or PublicKnowledgeState.

The experiment observer now also invokes `analyze_puzzle()` to record the public
support components immediately before each normal progressive deduction. This
profile uses fresh public snapshots and never reads hidden status to create Hint
support; hidden solution remains confined to the engine's existing integrity
check and the independent semantic-validity tests.

## Phase 8.6 production manifest and manual lock boundary

The production manifest is the explicit two-entry `PUZZLE_CATALOG`: Standard
3x3 and Advanced 4x4. Puzzle selection and both experiment runners share this
manifest/order. Legacy chain files live under `tests/fixtures/puzzles/`, so file
discovery cannot silently reclassify them as shipped gameplay or benchmark data.

`GameController` owns a set of unresolved character IDs whose manual attempt
returned CONTRADICTED. The controller rejects later manual submissions for such
an ID before invoking GameEngine. GUI view models receive only a boolean
modifier used for disabled actions, warning outline, and a neutral `LOCKED`
badge. The set is cleared on Restart/Load and is not serialized.

This creates no production dependency from domain/reasoning layers back to the
GUI. GameEngine, PublicKnowledgeState, LogicAgent, CNF, DPLL, Hint support, and
trace DTOs know nothing about locks. Hint, Solve Next, and Auto Solve continue
to consume the same public snapshot and may resolve a locked character normally.
