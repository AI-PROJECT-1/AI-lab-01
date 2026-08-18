# Known Limitations

These are verified limitations, not hidden defects or promised features.

## Reasoning and scale

- Hint support is deterministic and deletion-irreducible under a fixed removal
  order. It is not guaranteed globally smallest, unique, or a clause-level proof.
- Solver Details preserves per-query statistics rather than inventing cumulative
  statistics for older trace records.
- Direct combinational cardinality encoding is simple and auditable but can grow
  quickly for large regions. Performance beyond the required 3x3/4x4 scope is
  not claimed.

## Production puzzle scope

- The production catalog intentionally contains exactly two deduction-focused
  puzzles: Standard 3x3 and Advanced 4x4. No Tutorial or optional 5x5 is shipped.
- The four previous direct-chain JSON files remain under
  `tests/fixtures/puzzles/` solely to preserve unit/regression coverage. They are
  not selectable and are not included in production experiments.
- Both production puzzles contain zero FACT clues. Every recorded progressive
  deduction has support size at least 2, but this remains a support-component
  measurement rather than a calibrated player difficulty score.
- Standard uses ROW/COLUMN counting and SAME/DIFFERENT but not NEIGHBORS or clue
  extensions. Advanced supplies ROW/COLUMN/NEIGHBORS/EXPLICIT and IMPLIES/ODD.
- The observed final Advanced run made 92 decisions and 1 backtrack; exact work
  and timings are observations, not cross-platform guarantees.

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
  flow remains usable, though the 4x4 board and long clue text are necessarily
  compact and use existing scrolling/truncation behavior.
- Optional portraits, animations, timers, player notes, scoring, accounts, and
  cloud progression are outside the project scope.
- Runtime measurements depend on the Python build, operating system, and
  machine; raw JSON is reproducible evidence, not a performance guarantee.

## Submission artifacts still owned by the team

- `Report.pdf`, the 5-10 minute narrated/subtitled Drive video and verified link,
  and the final student-ID archive have not been fabricated or generated.
- Real member identities, ownership confirmation, honest contribution
  percentages, and final reference review require team input.
- Phase 8.6 is intentionally uncommitted pending approval and no remote push is
  claimed.
