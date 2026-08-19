# Griductive Demo Script

Target length: 8-9 minutes. The production catalog contains six cases. The
recommended live trio is **The Atrium Ledger** (3x3), **The Meridian
Conspiracy** (4x4), and **The Celestial Registry** (5x5). The other three should
be shown briefly in Puzzle Select, not fully played during the recording.

## Before recording

1. Run the full unittest suite and both experiment commands in
   `EXPERIMENT_LOG.md`.
2. Launch `python main.py` at 1180x800 or larger.
3. Close unrelated notifications. Do not display puzzle JSON or hidden statuses.

## 0:00-0:50 - Problem and architecture

- Introduce each character's Boolean Criminal/Innocent variable.
- Explain the pipeline: structured public clue -> automatic CNF -> team DPLL ->
  opposite assumptions -> forced verdict -> engine-controlled reveal.
- Emphasize that no arbitrary satisfying model or hidden answer drives play.

## 0:50-1:25 - Production puzzle selection

1. Open **Puzzles** and show two 3x3, two 4x4, and two 5x5 production cases.
2. Explain that direct Tutorial chains were moved to test fixtures and are not
   production choices or experiment inputs.
3. Show **Back to Game** preserving current state; external **Load** remains.

## 1:25-3:20 - Standard deduction and anti-guess lock

1. Play **The Atrium Ledger** and inspect the two scattered initial public cells
   A1 and C1. Select `S3-01` to show Row 1 highlighting.
2. Select C2 and submit a verdict that is currently **NOT_PROVABLE**. Confirm no
   reveal or lock.
3. Select B1 and deliberately submit the contradicted manual verdict. Confirm:
   no reveal, neutral `LOCKED` marker, selected-character lock context, and both
   manual verdict buttons disabled.
4. Do not narrate the opposite status. Explain that the result exposed only a
   public contradiction and created presentation/session state.
5. Click **Hint** twice: Stage 1 shows grounded public support; Stage 2 shows the
   target without revealing its status. The lock remains.
6. Click **Solve Next**. The real agent may resolve the locked character because
   lockout applies only to repeated manual guessing.

## 3:20-4:15 - Standard progression

- Show that new clue owners do not reveal in row-major order.
- Use **Auto Solve** to finish. Explain that all seven Standard steps have
  support size 2 and the production puzzle contains no FACT clue.
- Show completion controls and public clue inspection.

## 4:15-5:40 - Advanced multi-component reasoning

1. Play **The Meridian Conspiracy**. Point out scattered initial cells A1, D1,
   and A4.
2. Click **Hint** once. Stage 1 should emphasize `A4-01`, `A4-04`, and public
   known verdict A1 for the initial target; this support is extracted at runtime.
3. Click **Show target** and note that no answer is shown.
4. Mention ROW, COLUMN, NEIGHBORS, EXPLICIT, SAME/DIFFERENT, IMPLIES, ODD, and
   counting clues. There are no direct FACT anchors.

## 5:40-6:45 - Solver Details and real work

1. Click **Solve Next**, then open **Solver Details**.
2. Show target/verdict, active clue IDs, query purpose/assumption, SAT result,
   decisions, propagations, backtracks, runtime, and public reveal ID.
3. Explain that these are real trace DTO fields, not a fabricated clause proof.
4. Quote final experiment work only from `EXPERIMENT_LOG.md`: 66 progressive SAT
   calls, 92 decisions, 804 propagations, and 1 backtrack for this recorded run.

## 6:45-7:45 - Optional Expert 5x5

1. Play **The Celestial Registry**. Show its 25 readable dense cards and the
   scrollable Revealed Clues panel.
2. Click Hint Stage 1: initial support is EA-01 plus public verdicts A1, E3, B4,
   and D5 (five components). Stage 2 shows target B1 without its verdict.
3. Use Solve Next, open the long scrollable Solver Details trace, then Auto Solve.
4. Show 5x5 completion, clue inspection, Solver Details, Restart, and Puzzles.

## 7:45-8:30 - Lifecycle and evidence close

1. Demonstrate Restart or Play clearing old selection, feedback, emphasis, and
   manual locks.
2. Open Puzzles/Back once more to show same-root navigation.
3. State the final regression count and the 6/6 production experiment result
   from the latest logs.

## Hosting and submission checklist

- Export a 5-10 minute video with narration or subtitles.
- Upload to Google Drive, not YouTube; verify "Anyone with the link" in a signed-
  out/private window.
- Put only the real verified link in the report. Never commit a placeholder URL.
