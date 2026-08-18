# Experiment Log

Final Phase 8.5 run: 2026-08-16, Python 3.14.0 on Windows, baseline
`2c8ed1bd2f6edcdddd6583355110ccdd00470a6d`.

```powershell
python -m experiments.analyze_puzzles
python -m experiments.run_experiments
```

Raw outputs are `experiments/results/puzzle_quality.json` and
`experiments/results/final_regression.json`. Discovery includes every shipped
puzzle JSON except the schema. Exceptions remain explicit FAIL rows, cause a
non-zero exit, and are never dropped to make results cleaner. The previous
four-puzzle Phase 8 snapshot remains recoverable from commit `2c8ed1b`; it was
not represented as current after the puzzle set changed.

## Progressive solve results

| Puzzle | Category | Size | Initial/complete clauses | Reveals | SAT calls | Decisions | Propagations | Backtracks | SAT-query time (s) | Whole solve (s) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| The Gallery Shift | Tutorial | 3x3 | 2 / 9 | 8 | 20 | 0 | 100 | 0 | 0.000342 | 0.001141 |
| The Atrium Ledger | Standard | 3x3 | 8 / 24 | 7 | 16 | 0 | 105 | 0 | 0.000851 | 0.001696 |
| The Parity Gallery | Standard | 3x3 | 2 / 14 | 8 | 19 | 0 | 100 | 0 | 0.000642 | 0.001686 |
| The Museum Circuit | Tutorial | 4x4 | 2 / 16 | 15 | 38 | 0 | 327 | 0 | 0.001754 | 0.003923 |
| The Implication Archive | Standard | 4x4 | 2 / 19 | 15 | 36 | 0 | 314 | 0 | 0.002640 | 0.005233 |
| The Meridian Conspiracy | Advanced | 4x4 | 13 / 54 | 13 | 33 | 17 | 356 | 1 | 0.008557 | 0.012332 |

Every CNF reports `N²` primary variables and 0 auxiliary variables under the
current direct combinational encoding. SAT-query time is the sum of recorded
DPLL query runtimes; whole solve is the enclosing progressive Auto Solve wall
clock. Each reveal is one wave/trace deduction. The Advanced constraints caused
real branching/backtracking without puzzle-specific solver logic. Zero values in
other puzzles are retained observations, not hidden or normalized metrics.

## Public support quality profile

| Puzzle | Initial clues | Steps | Average support | Maximum support | FACT clues | Direct single-FACT deductions |
|---|---:|---:|---:|---:|---:|---:|
| The Gallery Shift | 1 | 8 | 1.000 | 1 | 9 | 8 |
| The Atrium Ledger | 2 | 7 | 2.000 | 2 | 1 | 0 |
| The Parity Gallery | 1 | 8 | 1.750 | 2 | 3 | 2 |
| The Museum Circuit | 1 | 15 | 1.000 | 1 | 16 | 15 |
| The Implication Archive | 1 | 15 | 1.267 | 2 | 12 | 11 |
| The Meridian Conspiracy | 3 | 13 | 2.308 | 4 | 1 | 0 |

Support size is the count of clue components plus proved public-verdict
components in the deletion-irreducible Hint explanation immediately before each
accepted deduction. It is not a mathematical difficulty score. The Advanced
first step forces B1 from clues `A4-01`, `A4-04`, and public verdict A1.

## Initial Hint benchmark (25 fresh engines per puzzle)

| Puzzle | Extraction SAT calls | Median Hint wall (s) | Median extraction (s) |
|---|---:|---:|---:|
| The Gallery Shift | 9 | 0.000243 | 0.000149 |
| The Atrium Ledger | 12 | 0.000497 | 0.000373 |
| The Parity Gallery | 7 | 0.000286 | 0.000163 |
| The Museum Circuit | 9 | 0.000265 | 0.000167 |
| The Implication Archive | 7 | 0.000282 | 0.000174 |
| The Meridian Conspiracy | 21 | 0.002833 | 0.002301 |

All 150 fresh-engine Hint runs returned a grounded
`deletion_irreducible` explanation. Timings are machine-specific observations,
not guarantees.

## Outcome

- 6/6 puzzles PASS; 0 failures/timeouts.
- 3/3 3x3 and 3/3 4x4 complete without guessing.
- 6/6 full clue sets are consistent and unique; uniqueness remains separate
  from the progressive public KB.
- Tutorial direct behavior is explicit. Standard and Advanced add real combined
  reasoning without modifying CNF, DPLL, LogicAgent, Hint reduction, or target order.
