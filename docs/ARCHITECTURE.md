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
