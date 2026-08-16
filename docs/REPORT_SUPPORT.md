# Report Support Notes

This file supplies verified technical material for the team's final PDF. It is
not the final report and must be reviewed, attributed, referenced, and laid out
by the team.

## Problem formulation

For an `N x N` board, each character `i` has one primary Boolean variable
`C_i`: true means CRIMINAL and false means INNOCENT. Names and professions are
display metadata, not logical predicates. A public knowledge base contains only
CNF clauses from revealed clues plus unit clauses for verdicts already proved
and accepted. Hidden statuses and unrevealed clues remain inside the engine.

## Deterministic variables and regions

Characters are ordered row-major and mapped to variables `1..N²`. Auxiliary
IDs, if an encoding needs them, begin after the primary range; the current
direct combinational encoder needs zero auxiliaries. A single RegionResolver
defines ROW, COLUMN, eight-cell NEIGHBORS excluding the owner itself, and a
distinct EXPLICIT list. Encoder, evaluator, and highlighting reuse it.

## CNF derivations

- `FACT(C_i=true)` becomes `(C_i)`; false becomes `(not C_i)`.
- `SAME(C_i,C_j)` becomes `(not C_i or C_j) and (C_i or not C_j)`.
- `DIFFERENT(C_i,C_j)` becomes `(C_i or C_j) and (not C_i or not C_j)`.
- `IMPLIES(C_i,C_j)` becomes `(not C_i or C_j)`.
- `AT_MOST(k,S)` forbids every subset of `k+1` variables in `S` from all being
  true: one all-negative clause per such subset.
- `AT_LEAST(k,S)` requires every subset of `|S|-k+1` variables to contain a true
  member: one all-positive clause per such subset.
- `EXACTLY(k,S)` is the conjunction of AT_MOST and AT_LEAST.
- `ODD(S)` enumerates assignments of `S` and blocks every even-parity one. This
  is suitable for the small required boards and independently truth-table tested.

Input validation rejects malformed clue/region parameters. `CNFBuildResult`
reports primary variables, auxiliary variables, and clause count. A separate
direct semantic evaluator checks each clue without calling the encoder.

## DPLL pseudocode

```text
DPLL(clauses, assignment):
    repeat unit propagation
        if a clause is empty: return UNSAT
        assign each unit literal; reject a conflicting assignment
    if every clause is satisfied:
        complete all unassigned variables deterministically with false
        return SAT and the complete assignment
    choose the first unassigned primary/declared variable
    for value in [true, false]:
        increment decision/branch counters
        result = DPLL(simplified clauses, assignment plus value)
        if result is SAT: return result
        increment backtrack counter as appropriate
    return UNSAT
```

The implementation records decisions, propagations, backtracks, recursive
calls, and runtime. Correctness is checked on explicit SAT/UNSAT cases and 500
deterministic formulas compared with a brute-force oracle.

## Entailment and progressive deduction

For an unresolved variable `C_i`, the agent makes two fresh DPLL queries:

- if `KB and not C_i` is UNSAT, `C_i` is forced CRIMINAL;
- if `KB and C_i` is UNSAT, `C_i` is forced INNOCENT;
- if both are SAT, status is UNKNOWN;
- if both are UNSAT, the public KB is INCONSISTENT.

The agent scans unresolved characters row-major, returns the first forced
verdict, and records both queries. GameEngine accepts only a forced matching
verdict, verifies it against authoritative state, reveals that character's clue,
and creates a new public snapshot. Auto Solve repeats this one-wave transition
until complete or until no forced move exists; it never uses one arbitrary SAT
model as an answer.

## Hint explanation and trace

Hint target selection reuses normal `solve_next`. Support extraction then treats
each public revealed clue and each proved verdict as one component. It verifies
the same target verdict from the full public baseline and greedily removes
components in deterministic order, retaining a component when its deletion
would stop forcing that verdict. The result is deletion-irreducible, not claimed
globally minimum or unique. Its extra SAT calls/runtime are diagnostic and do
not become deduction trace steps.

The trace contains public target/verdict, active clue IDs, exact query purpose,
assumption, SAT result and per-query statistics, plus the newly revealed public
clue ID. It excludes hidden assignments and invented proof text.

## Uniqueness validation

Puzzle validation uses a separate state containing the complete clue set. After
the first satisfying primary assignment, a blocking clause negates that exact
primary model and DPLL runs again. UNSAT on the second call proves uniqueness;
SAT provides evidence of a second model. This complete-clue validation is never
used as the gameplay public KB.

## Final experiment summary

| Puzzle | Size | Complete clauses | Progressive SAT calls | Propagations | Solve wall (s) | Unique |
|---|---:|---:|---:|---:|---:|---|
| The Parity Gallery | 3x3 | 14 | 19 | 100 | 0.001339 | yes |
| The Gallery Shift | 3x3 | 9 | 20 | 100 | 0.000963 | yes |
| The Implication Archive | 4x4 | 19 | 36 | 314 | 0.003511 | yes |
| The Museum Circuit | 4x4 | 16 | 38 | 327 | 0.002968 | yes |

All four runs completed, remained consistent/unique, and recorded zero failures.
See `EXPERIMENT_LOG.md` and raw `experiments/results/final_regression.json` for
metric definitions, Hint benchmarks, exact floating-point values, environment,
and retained error fields.

## Report checklist

The final PDF still needs team-authored planning/contributions, screenshots or
diagrams, limitations, references/citations, the AI-use appendix, video link,
student identities, and formatting within the course constraints. Use
`REQUIREMENTS_AUDIT.md`, `KNOWN_LIMITATIONS.md`, `AI_USAGE_LOG.md`,
`DECISION_LOG.md`, `TEST_LOG.md`, and Git history as evidence; do not copy claims
without human verification.
