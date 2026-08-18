# Experiment Log

Phase 8.6 production-hardening run: 2026-08-18, Python 3.14.0 on Windows,
baseline commit `8c8c77d326ceb65beaa7b5454bc0bcd49f9da355`.

## Reproduction

```text
python -m experiments.analyze_puzzles --output experiments/results/puzzle_quality.json
python -m experiments.run_experiments --output experiments/results/final_regression.json
```

Both commands read the explicit production catalog in catalog order. They do
not glob test fixtures. The former Tutorial/direct-chain JSON files are retained
under `tests/fixtures/puzzles/` for regression coverage only.

## Production progressive-solve results

| Puzzle | Tier | Size | Initial/full clauses | Reveals | SAT calls | Decisions | Propagations | Backtracks | SAT-query time (s) | Whole solve (s) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| The Atrium Ledger | Standard | 3x3 | 9 / 23 | 7 | 34 | 6 | 208 | 0 | 0.001593 | 0.002944 |
| The Meridian Conspiracy | Advanced | 4x4 | 13 / 60 | 13 | 66 | 92 | 804 | 1 | 0.019911 | 0.024452 |

The counts come from the unchanged generic CNF/DPLL/LogicAgent path. Runtime is
machine-specific. No random generation, target-order override, puzzle-specific
formula, or hidden answer is consumed at runtime.

## Public support quality profile

| Puzzle | Initial public cells | Steps | Average/max support | Size-1 steps | Size >=2 steps | FACT clues |
|---|---|---:|---:|---:|---:|---:|
| The Atrium Ledger | A1, C1 | 7 | 2.000 / 2 | 0 | 7 | 0 |
| The Meridian Conspiracy | A1, D1, A4 | 13 | 2.308 / 4 | 0 | 13 | 0 |

Standard deduction targets are `B1 -> C2 -> A3 -> A2 -> C3 -> B2 -> B3`.
Advanced targets are `B1 -> C1 -> A2 -> A3 -> C2 -> B3 -> B2 -> C3 -> D3
-> B4 -> C4 -> D4 -> D2`. The corresponding clue-owner sequences are retained
in `puzzle_quality.json`. Neither sequence is a row-major direct-answer chain.

Support size counts public clue components and proved public-verdict components
in the deterministic deletion-irreducible Hint explanation. It is not claimed
to be globally minimum, unique, or a calibrated difficulty score.

## Initial Hint benchmark (25 fresh engines per production puzzle)

| Puzzle | Extraction SAT calls | Median Hint wall (s) | Median extraction (s) | Extraction min/max (s) |
|---|---:|---:|---:|---:|
| The Atrium Ledger | 12 | 0.000499 | 0.000370 | 0.000351 / 0.000412 |
| The Meridian Conspiracy | 21 | 0.001686 | 0.001367 | 0.001252 / 0.002401 |

All 50 fresh-engine Hint runs returned a grounded
`deletion_irreducible` explanation.

## Phase 8.5 comparison

The Phase 8.5 baseline recorded Standard at 16 SAT calls, 0 decisions, 105
propagations, and 0 backtracks; Advanced at 33 calls, 17 decisions, 356
propagations, and 1 backtrack. Removing late direct FACT anchors and remapping
public clue ownership increased actual generic-solver work to the Phase 8.6
figures above while preserving fast completion.

## Outcome

- 2/2 production puzzles PASS; 0 failures/timeouts.
- One 3x3 and one 4x4 complete progressively without guessing.
- Both complete clue sets are consistent and unique.
- Both production puzzles contain zero direct FACT clues and zero support-size-1
  deductions.
- Legacy direct-chain files remain test fixtures and are excluded from the
  production catalog and experiment manifest.
