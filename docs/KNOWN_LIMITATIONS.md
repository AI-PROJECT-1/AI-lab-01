# Known Limitations

These are verified limitations, not hidden defects or promised features.

## Reasoning and scale

- Hint support extraction is deterministic and deletion-irreducible under its
  fixed removal order. It is not guaranteed to be the globally smallest or the
  only valid support set.
- Supporting clues are indivisible components. The system does not extract or
  narrate a clause-level proof.
- Solver Details preserves per-query statistics. It does not invent cumulative
  statistics for historical records that do not contain them.
- The direct combinational cardinality encoding is simple and auditable but can
  grow combinatorially for large regions. The required 3x3/4x4 suite is fast;
  large-board performance is not claimed.

## Puzzle and coverage scope

- The distributable suite is two 3x3 and two 4x4 puzzles. No optional 5x5
  puzzle/experiment is included.
- Shipped chain puzzles primarily exercise FACT, SAME, DIFFERENT and the
  `IMPLIES`/`ODD` extensions with EXPLICIT regions. EXACTLY, AT_LEAST, AT_MOST,
  ROW, COLUMN, and NEIGHBORS are implemented and exhaustively/synthetically
  tested, but are not broadly represented in the four demo puzzles.
- No shipped puzzle's initial Hint requires two clue components simultaneously.
  The 4x4 extension chain does exercise a public clue plus a previously proved
  verdict; multi-clue support is covered by valid synthetic public-state tests.
- The shipped progressive chains are deliberately deduction-friendly and solve
  by unit propagation, so their measured DPLL decisions/backtracks are zero.
  Independent SAT and brute-force-oracle tests exercise branching/backtracking.

## Presentation and environment

- Tkinter requires a graphical desktop/display and is not intended as a web or
  headless application.
- Statuses and completion are textual and accessible; optional artwork,
  animations, timers, player notes, and completion counters are not included.
- Runtime measurements depend on the local Python build, operating system, and
  machine. The raw JSON is reproducible evidence, not a performance guarantee.

## Submission artifacts still owned by the team

- `Report.pdf`, the 5-10 minute narrated/subtitled Drive video, its verified
  share link, and the final student-ID-named archive have not been fabricated or
  generated during Phase 8.
- Real member names/student IDs, ownership confirmation, honest contribution
  percentages, and final reference review require team input before submission.
- Local `main` is ahead of `origin/main`; the Phase 8 audit does not claim a
  remote backup or submission upload.
