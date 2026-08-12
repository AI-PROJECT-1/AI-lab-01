# AI Usage Log

## AI-001

- Date: 2026-08-09
- AI tool: OpenAI Codex
- Model: GPT-5
- Developer/member: Unassigned team member (confirm before submission)
- Phase: Requirement audit and Phase 01
- Purpose: Audit the official PDF and establish a compliant repository foundation.
- Files affected: README, package structure, requirements, project documentation.
- Summary of AI suggestion: Use immutable public DTOs, explicit agent protocol, standard-library-first Phase 01-04 implementation, and atomic phase commits.
- Accepted: Public/hidden boundary, phase-gated architecture, audit mapping, no fake solver behavior.
- Rejected/deferred: Production SAT reasoning, extensions, experiments, and unsupported completion claims before their phases.
- Human verification performed: PENDING team review.
- Tests performed: `compileall`, unittest discovery (0 tests expected), and `git diff --check`; all passed.
- Related Prompt ID: PROMPT-001
- Related Git commit hash: 5a26cbe

## AI-002

- Date: 2026-08-09
- AI tool: OpenAI Codex
- Model: GPT-5
- Developer/member: Unassigned team member (confirm before submission)
- Phase: 02
- Purpose: Define validated shared contracts and a puzzle interchange format.
- Files affected: `core/`, `puzzles/schema.json`, `puzzles/sample_3x3.json`, `tests/test_core.py`.
- Summary of AI suggestion: Use frozen slotted dataclasses, stable coordinate IDs, structured clue variants, and a hidden `PuzzleCard` that never crosses the public boundary.
- Accepted: Immutable DTOs, validation at construction, tuple-based public collections, JSON Schema.
- Rejected/deferred: General region resolution and semantic truth evaluation before Phase 05.
- Human verification performed: PENDING team review.
- Tests performed: 9/9 unittests passed; schema/sample JSON syntax, compile, and diff checks passed.
- Related Prompt ID: PROMPT-001
- Related Git commit hash: 81e5882

## AI-003

- Date: 2026-08-09
- AI tool: OpenAI Codex
- Model: GPT-5
- Developer/member: Unassigned team member (confirm before submission)
- Phase: 03
- Purpose: Implement loading and a privacy-preserving progressive game engine.
- Files affected: `agent/protocols.py`, `agent/mock_logic_agent.py`, `game/`, `tests/test_game.py`, `core/character.py`.
- Summary of AI suggestion: Keep the agent input limited to immutable public snapshots and have the engine verify an accepted forced verdict against its authoritative hidden status before reveal.
- Accepted: Public-only protocol, strict loader, copy-on-snapshot, integrity error with no mutation.
- Rejected/deferred: Hidden-solution mock, accept-all mock, production entailment before its phase.
- Human verification performed: PENDING team review.
- Tests performed: Initial run 18/19 due to sandbox temp permission; test fixed to mock file input; final 20/20 passed plus compile/diff checks.
- Related Prompt ID: PROMPT-001
- Related Git commit hash: bcf0393

## AI-004

- Date: 2026-08-09
- AI tool: OpenAI Codex
- Model: GPT-5
- Developer/member: Unassigned team member (confirm before submission)
- Phase: 04
- Purpose: Build the desktop GUI skeleton and manual gameplay loop without fake production reasoning.
- Files affected: `main.py`, `gui/`, `tests/test_gui.py`, project logs.
- Summary of AI suggestion: Render only public view models, route actions through a headless controller, label the FACT-only development agent, and disable features whose real reasoning is not implemented.
- Accepted: Tkinter GUI, controller/view-model split, visible phase limitations, no direct hidden access.
- Rejected/deferred: GUI-side clue region resolver, fabricated Hint/Auto Solve behavior.
- Human verification performed: PENDING team visual review.
- Tests performed: 25/25 unittests passed, full compile/diff checks passed, and a real Tk widget/layout smoke test completed cleanly.
- Related Prompt ID: PROMPT-001
- Related Git commit hash: 3dec8a9

## AI-005

- Date: 2026-08-12
- AI tool: OpenAI Codex
- Model: GPT-5
- Developer/member: Trần Hữu Phước - 24127511
- Phase: Audit and debug of Phases 00-07
- Purpose: Compare the complete master prompt and official Project 2 PDF against merged code, reproduce deviations, fix root causes, and restore trustworthy phase/test evidence.
- Files affected: `logic/region_resolver.py`, `logic/cnf_encoder.py`, `logic/semantic_evaluator.py`, `sat/dpll.py`, `agent/mock_logic_agent.py`, tests, README, and audit documents.
- Summary of AI suggestion: Centralize region semantics, validate resolved region bounds and cardinality parameters, enforce integer-only DPLL inputs, make DPLL tests discoverable by the documented runner, use exhaustive CNF equivalence and brute-force SAT oracles, and distinguish implemented phases from final-project gaps.
- Accepted: All listed root-cause fixes and evidence updates.
- Rejected: Adding pytest only to preserve incompatible tests; claiming Phases 08-17 or final rubric completion; fabricating prior teammates' AI usage records.
- Human verification performed: PENDING team review of this audit and code diff.
- Tests performed: `python -m pytest -q` failed because pytest is not installed; existing DPLL functions then passed when invoked directly; 3,500 diagnostic DPLL cases passed against brute force; final discoverable regression and GUI smoke results are recorded in `TEST_LOG.md`.
- Related Prompt ID: PROMPT-002
- Related Git commit hash: PENDING

## AI-006

- Date: 2026-08-12
- AI tool: OpenAI Codex
- Model: GPT-5
- Developer/member: Trần Hữu Phước - 24127511
- Phase: 08-13
- Purpose: Implement the production deductive agent, progressive controls and trace, canonical highlighting, two required extensions, and validated 3x3/4x4 puzzles.
- Files affected: `agent/`, `game/game_engine.py`, `gui/`, core clue contracts, logic encoder/evaluator/resolver, puzzle schema/files, tests, and project documentation.
- Summary of AI suggestion: Use assumption-based entailment, keep progressive reveal orchestration in GameEngine, require clue-only states for uniqueness, share the canonical resolver with GUI highlighting, and select `IMPLIES` plus `ODD` after comparing four candidates.
- Accepted: Public-only LogicAgent, non-mutating Hint, deterministic Solve Next, wave-based Auto Solve, SAT trace, primary-model uniqueness blocking, canonical highlights, both extensions, four-puzzle validation gates.
- Rejected: Passing GameEngine to the agent; deriving verdicts from one satisfying model; batch-revealing from a stale snapshot; redundant extension candidates equivalent to existing clues.
- Human verification performed: PENDING team review and visual acceptance.
- Tests performed: 77/77 unittests passed; all JSON parsed; full compile passed; GUI smoke and boundary scans recorded in `TEST_LOG.md`.
- Related Prompt ID: PROMPT-003
- Related Git commit hash: PENDING
