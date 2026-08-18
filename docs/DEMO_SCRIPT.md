# Griductive Demo Script

Target length: 8-9 minutes. Primary reasoning puzzle: **The Meridian
Conspiracy** (`advanced-deduction-4x4`). Manual-flow puzzle: **The Atrium
Ledger** (`standard-deduction-3x3`). **The Gallery Shift** is shown only as the
clearly labeled Tutorial, not as representative solver difficulty.

## Before recording

1. Run `python -m unittest discover -s tests`,
   `python -m experiments.analyze_puzzles`, and
   `python -m experiments.run_experiments`.
2. Launch with `python main.py` at 1180x800 or larger.
3. Close unrelated windows/notifications. Prepare narration or accurate
   subtitles. Do not display puzzle JSON or hidden status data.

## 0:00-0:50 — Problem and architecture

- Introduce each character's Boolean Criminal/Innocent variable and explain
  that only public clues and proved verdicts enter the knowledge base.
- State the pipeline: structured clue -> automatic CNF -> team DPLL -> opposite
  assumptions -> forced verdict -> engine-verified reveal.
- Emphasize that no arbitrary satisfying model is used as an answer.

## 0:50-1:35 — Puzzle Select and three experiences

1. Click **Puzzles**.
2. Show Tutorial, Standard, and Advanced labels plus the current-puzzle badge.
3. Explain that Tutorial teaches mechanics through direct facts; Standard adds
   counts/relationships; Advanced combines regions and extensions.
4. Point out that **Back to Game** preserves current progress and **Load** still
   supports an external local JSON file.

## 1:35-3:15 — Standard manual deduction

1. Play **The Atrium Ledger**. Inspect A1's `S3-01`; Row 1 highlights A1/B1/C1.
2. Note the two initial public clues and verdicts: the next answer is not written
   directly by a FACT clue.
3. Select C2 and submit CRIMINAL to show **NOT_PROVABLE** with no reveal.
4. Select B1 and submit INNOCENT to show **CONTRADICTED** with no reveal.
5. Submit B1 as CRIMINAL. Show **ACCEPTED**, new clue, and presentation-only
   reveal emphasis.
6. Click the solved B1 card to select its public relation and spotlight A2/B2.

## 3:15-4:15 — Standard grounded Hint

1. Click **Hint**. Stage 1 should show a real public clue plus a proved public
   verdict; every Standard step has support size 2.
2. Explain that support is deterministic and deletion-irreducible, not claimed
   globally minimum or unique.
3. Click **Show target**. Stage 2 highlights only the cached character and makes
   no second reasoning call or verdict reveal.

## 4:15-5:20 — Advanced multi-component reasoning

1. Open **Puzzles**, choose **The Meridian Conspiracy**.
2. Inspect `A4-01` and show exact Row 1 highlighting.
3. Click **Hint** once. Stage 1 should visibly emphasize clues `A4-01` and
   `A4-04` plus known public verdict A1. This is a real shipped-puzzle result,
   not supplied UI metadata.
4. Click **Show target** to focus B1 without showing its verdict.

## 5:20-6:30 — Solve Next and Solver Details

1. Click **Solve Next** for one accepted deduction.
2. Open **Solver Details**. Point out target/verdict, active clue IDs, query
   purpose/assumption, SAT result, decisions, propagations, backtracks, runtime,
   and newly revealed public clue ID.
3. Explain that fields are copied from real trace records. No clause proof,
   hidden assignment, or historical action source is invented.

## 6:30-7:35 — Regions, extensions, and Auto Solve

- Mention the Advanced puzzle's ROW, COLUMN, NEIGHBORS, and EXPLICIT regions;
  counting clues; SAME/DIFFERENT; and both IMPLIES/ODD extensions.
- Continue with **Auto Solve**. Explain that each reveal causes a fresh public KB
  and solver call. The recorded final run used 17 decisions and 1 backtrack; the
  numbers are observations, not a fabricated difficulty score.

## 7:35-8:20 — Completion and navigation safety

1. Show the completed board and still-available clue inspection/Solver Details.
2. Show disabled verdict/Hint/Solve/Auto controls.
3. Open **Puzzles**, then **Back to Game**, showing the same completed state.
4. Select Standard or Tutorial and show that Play performs a legitimate fresh
   load and clears completion/transient state.

## 8:20-8:50 — Evidence close

- State the final real regression/experiment counts from `TEST_LOG.md` and
  `EXPERIMENT_LOG.md` immediately before recording.
- Summarize: Tutorial teaches, Standard combines two public components per step,
  and Advanced demonstrates multi-clue support, extensions, branching, and
  progressive no-guess completion.

## Hosting and submission checklist

- Export a 5-10 minute video with narration or subtitles.
- Upload to Google Drive, not YouTube.
- Set "Anyone with the link" and verify playback in a private/incognito window.
- Add the real link to the final report and test it again before submission.
- Never commit a placeholder or fabricated URL.
