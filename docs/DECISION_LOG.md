# Decision Log

## DEC-001 - Immutable public snapshot boundary

- Context: The engine owns hidden labels and unrevealed clues while every agent must use public information only.
- Options considered: pass engine directly; pass mutable puzzle subset; construct immutable public DTOs.
- Chosen option: Construct a new immutable `PublicKnowledgeState` snapshot for every agent call.
- Reason: It makes hidden-data access structurally unavailable and easy to test.
- Consequences: Small copy cost; clearer interfaces; tests can inspect the DTO recursively.
- Related requirement: PDF sections 4.1 and 4.2.
- Related commit: PENDING

## DEC-002 - Standard-library desktop GUI for early phases

- Context: A GUI is mandatory, while Phases 01-04 should avoid unnecessary dependency setup.
- Options considered: Tkinter desktop, third-party desktop toolkit, web frontend.
- Chosen option: Tkinter desktop GUI.
- Reason: Ships with CPython, keeps the project Python-only, and allows business logic to remain headless-testable.
- Consequences: GUI visual checks require a display; styling is intentionally modest.
- Related requirement: PDF section 4.1.
- Related commit: PENDING

## DEC-003 - Development mock recognizes public FACT clues only

- Context: Phase 04 needs manual gameplay before the production agent exists.
- Options considered: inspect hidden solution; accept every verdict; scripted hidden answers; minimal public FACT classifier.
- Chosen option: A clearly named mock classifies only statuses explicitly present in public FACT clues or already proved verdicts.
- Reason: It enables honest manual-flow testing without guessing or reading hidden data.
- Consequences: The sample puzzle uses a FACT chain; general reasoning is deferred to Phases 05-10.
- Related requirement: PDF sections 2.2 and 4.1.
- Related commit: PENDING
