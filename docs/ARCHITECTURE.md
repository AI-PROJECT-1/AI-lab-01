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
              LogicAgent protocol
```

Only `GameEngine` and loader-side domain objects may hold hidden labels and
unrevealed clue objects. Agents receive a freshly constructed immutable
`PublicKnowledgeState`; they never receive `Puzzle` or `GameEngine`.

The GUI calls engine methods and renders public snapshots. It does not inspect
private puzzle state. In later phases the mock agent is replaced behind the same
protocol by the CNF/DPLL-backed agent.

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

## JSON design

The schema uses stable cell IDs such as `A1`, explicit `row`/`column` integers,
structured clue objects, and separate initial visibility. Hidden `status` is
loader/engine-only and is removed when public DTOs are created.
