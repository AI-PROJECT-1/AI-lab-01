# Prompt Log

## PROMPT-001

- Date: 2026-08-09
- Tool: OpenAI Codex
- Model: GPT-5
- Member: Trần Hữu Phước - 24127511
- Phase: Requirement audit and Phases 01-04
- Goal: Read the official Project 2 PDF and master development prompt, then implement and publish Phases 01-04 to the supplied GitHub repository.
- Full prompt: User supplied `[2526 HK3] IntroAI - Project 2.pdf`, the Master Development Prompt attachment, repository `https://github.com/AI-PROJECT-1/AI-lab-01.git`, and requested careful execution from Phase 01 through Phase 04.
- Short summary of response: Audited the PDF, selected a privacy-preserving architecture, and implemented the approved Phase 01-04 scope.
- Decision: ACCEPTED
- Related AI Usage ID: AI-001 through AI-004
- Related commits: `5a26cbe`, `81e5882`, `bcf0393`, `3dec8a9`, `7e53661`, `d424c47`, `4742e10`

## PROMPT-002

- Date: 2026-08-12
- Tool: OpenAI Codex
- Model: GPT-5
- Member: Trần Hữu Phước - 24127511
- Phase: Audit of Phases 00-07
- Goal: Re-read the complete master prompt and official PDF, compare every phase with the current repository, debug confirmed code/logic/specification deviations, and report the work performed.
- Full prompt: "đọc lại toàn bộ prompt.txt, các phase, đối chiếu với các file hiện tại ở các phase đó xem có lỗi về mặt code, logic, sai lệch so với yêu cầu của intro-ai project 2 hay không. Debug nếu có, rồi báo cáo đã làm những gì"
- Short summary of response: Audited all 1,503 prompt lines and all 9 PDF pages; found test-discovery, region/count validation, DPLL input validation, mock inconsistency, and documentation drift; implemented root-cause fixes and expanded independent verification.
- Decision: ACCEPTED
- Related AI Usage ID: AI-005
- Related commits: PENDING

## PROMPT-003

- Date: 2026-08-12
- Tool: OpenAI Codex
- Model: GPT-5
- Member: Trần Hữu Phước - 24127511
- Phase: 08-13
- Goal: Implement a real LogicAgent, Hint/Solve Next/Auto Solve, deduction trace, clue highlighting, two mandatory extensions, and a 3x3/4x4 puzzle suite.
- Full prompt: "LogicAgent suy luận thật; Hint, Solve Next và Auto Solve; Trace suy luận; Highlight vùng clue; Hai extension bắt buộc; Bộ puzzle 3×3/4×4 — triển khai các phần này."
- Short summary of response: Added public-only SAT entailment and progressive engine integration, trace and uniqueness, canonical GUI highlighting, `IMPLIES`/`ODD`, and four automatically validated puzzles.
- Decision: ACCEPTED
- Related AI Usage ID: AI-006
- Related commits: PENDING
