# Experiment Log

Final run: 2026-08-16, Python 3.14.0 on Windows, baseline
`4150d867b6f2ce03cf273ced9895c4dd06105445`.

Reproduce with:

```powershell
python -m experiments.run_experiments
```

Raw machine-readable output is retained at
`experiments/results/final_regression.json`. The runner discovers every puzzle
JSON except the schema, records exceptions as FAIL rows, and exits non-zero if
any case fails.

## Progressive solve results

| Puzzle | Size | Initial/complete clauses | Reveals / waves / trace | SAT calls | Decisions | Propagations | Backtracks | SAT query time (s) | Whole solve (s) | Unique |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| The Parity Gallery | 3x3 | 2 / 14 | 8 / 8 / 8 | 19 | 0 | 100 | 0 | 0.000460 | 0.001339 | yes |
| The Implication Archive | 4x4 | 2 / 19 | 15 / 15 / 15 | 36 | 0 | 314 | 0 | 0.001834 | 0.003511 | yes |
| The Museum Circuit | 4x4 | 2 / 16 | 15 / 15 / 15 | 38 | 0 | 327 | 0 | 0.001392 | 0.002968 | yes |
| The Gallery Shift | 3x3 | 2 / 9 | 8 / 8 / 8 | 20 | 0 | 100 | 0 | 0.000293 | 0.000963 | yes |

Each CNF has `N²` primary variables and 0 auxiliary variables under the direct
combinational encoding. "SAT query time" is the sum of DPLL runtimes recorded
on progressive entailment queries. "Whole solve" is the enclosing Auto Solve
wall clock. Reveal waves equal accepted progressive deductions for these chain
puzzles. Zero decisions/backtracks is an observed result: the distributable
chains become unit-propagation problems; dedicated DPLL tests independently
exercise branching and backtracking.

## Hint support diagnostic (25 fresh engines per puzzle)

| Puzzle | Target | Extraction SAT calls | Median Hint wall (s) | Median extraction (s) | Extraction min-max (s) |
|---|---|---:|---:|---:|---:|
| The Parity Gallery | B1 | 7 | 0.000182 | 0.000112 | 0.000110-0.000141 |
| The Implication Archive | B1 | 7 | 0.000210 | 0.000132 | 0.000129-0.000139 |
| The Museum Circuit | B1 | 9 | 0.000236 | 0.000148 | 0.000145-0.000156 |
| The Gallery Shift | B1 | 9 | 0.000202 | 0.000127 | 0.000125-0.000130 |

All 100 Hint runs returned the same target per puzzle and a
`deletion_irreducible` public support explanation. Timings are observations from
one machine, not performance guarantees.

## Outcome

- 4/4 puzzles PASS; 0 failures and 0 timeouts.
- 2/2 3x3 and 2/2 4x4 puzzles complete without guessing.
- 4/4 complete clue sets are consistent and unique; uniqueness used 2 SAT calls
  per puzzle.
- `IMPLIES` and `ODD` both occur in distributable 3x3 and 4x4 data.
- No failed case was removed. The JSON keeps an `error` field for every row and
  the runner retains future loader/solver exceptions as explicit failures.
