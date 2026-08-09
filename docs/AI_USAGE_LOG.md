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
- Related Git commit hash: PENDING
