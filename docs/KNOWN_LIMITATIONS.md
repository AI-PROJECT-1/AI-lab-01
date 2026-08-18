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

- The distributable suite is three 3x3 and three 4x4 puzzles. No optional 5x5
  puzzle/experiment is included.
- The Gallery Shift and Museum Circuit intentionally remain direct Tutorial
  chains. They teach interface mechanics and are not presented as representative
  solver difficulty.
- The Atrium Ledger is a Standard 3x3 combining SAME/DIFFERENT relationships,
  EXACTLY/AT_LEAST counts, ROW/COLUMN regions, and public verdicts. Its seven
  deductions all have support size 2, but it does not use NEIGHBORS or extensions.
- The Meridian Conspiracy is the Advanced 4x4 and resolves the former shipped
  coverage gap: it uses counting, ROW/COLUMN/NEIGHBORS/EXPLICIT regions,
  IMPLIES/ODD, and real two-clue-plus-verdict initial Hint support.
- Direct FACT is still present once in each deduction-focused puzzle to anchor
  complete-clue uniqueness, but neither late FACT participates in a progressive
  direct-answer step.
- Standard still solves with unit propagation in its observed experiment. The
  Advanced run performed 17 decisions and 1 backtrack; these are observations,
  not a calibrated difficulty score or guaranteed counts across implementations.

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
