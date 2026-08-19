# Known Limitations

These are verified limitations, not hidden defects or promised features.

## Reasoning and scale

- Hint support is deterministic and deletion-irreducible under a fixed removal
  order. It is not guaranteed globally smallest, unique, or a clause-level proof.
- Solver Details preserves per-query statistics rather than inventing cumulative
  statistics for older trace records.
- Direct combinational cardinality encoding is simple and auditable but can grow
  quickly for large regions. The shipped 5x5 cases remain fast, but performance
  for arbitrary larger boards or much larger counting regions is not claimed.

## Production puzzle scope

- The production catalog contains exactly six deduction-focused puzzles: two
  3x3, two 4x4, and two 5x5. Tutorial remains excluded.
- The four previous direct-chain JSON files remain under
  `tests/fixtures/puzzles/` solely to preserve unit/regression coverage. They are
  not selectable and are not included in production experiments.
- All six production puzzles contain zero FACT clues. Every recorded progressive
  deduction has support size at least 2, but this remains a support-component
  measurement rather than a calibrated player difficulty score.
- The catalog collectively supplies ROW/COLUMN/NEIGHBORS/EXPLICIT plus both
  extensions. Individual puzzles intentionally use narrower profiles.
- Recorded 5x5 whole-solve times were 0.087805s and 0.019417s on the audit
  machine. Exact work and timings are observations, not cross-platform guarantees.

## Manual anti-guess lock

- A contradicted manual verdict locks that unresolved character against further
  manual verdict submissions for the current run. The lock is session/UI state,
  not a new logical fact, penalty score, or GameEngine mutation.
- Hint, Solve Next, and Auto Solve remain available and may logically resolve a
  locked character. Restart and Load clear all locks.
- The interface intentionally does not state the opposite/correct status after
  a contradiction; doing so would turn the penalty into an answer oracle.

## Presentation and environment

- Tkinter requires a graphical desktop/display. At 1180x660 the full control
  flow remains usable. 5x5 uses dense cards and controls; card clue previews are
  omitted at that density while full public clue text remains in the scrollable
  Revealed Clues panel.
- Optional portraits, animations, timers, player notes, scoring, accounts, and
  cloud progression are outside the project scope.
- Runtime measurements depend on the Python build, operating system, and
  machine; raw JSON is reproducible evidence, not a performance guarantee.

## Submission artifacts still owned by the team

- `Report.pdf`, the 5-10 minute narrated/subtitled Drive video and verified link,
  and the final student-ID archive have not been fabricated or generated.
- Real member identities, ownership confirmation, honest contribution
  percentages, and final reference review require team input.
- Phase 8.7 starts from real clean checkpoint
  `c347ef05f808a94c90f5529139f80cf10abca8cf`; its changes are intentionally
  uncommitted pending approval.
