# Griductive Demo Script

Target length: 7-8 minutes. Primary puzzle:
`puzzles/sample_3x3.json`. Extension backup:
`puzzles/extension_chain_4x4.json`.

## Before recording

1. Run `python -m unittest discover -s tests` and
   `python -m experiments.run_experiments`.
2. Launch from a clean terminal with `python main.py` at 1180x800 or larger.
3. Close unrelated windows and notifications. Use readable system scaling.
4. Prepare narration or accurate subtitles. Do not display hidden puzzle JSON.

## 0:00-0:45 — Problem and boundary

- Introduce Griductive: each character has a Boolean Criminal/Innocent status;
  public clues constrain the board.
- State that the engine owns hidden statuses and unrevealed clues. The agent
  receives only an immutable public snapshot and accepts a verdict only when
  public knowledge entails it.
- Point out board coordinates, character names/professions, face-down cards,
  public clues, verdict controls, and solver controls.

## 0:45-2:15 — Manual verdict outcomes

1. Select **C1** and submit **CRIMINAL**. Show **NOT_PROVABLE** and explain that
   current public information does not force that claim; no card is revealed.
2. Select **B1** and submit **CRIMINAL**. Show **CONTRADICTED**: public knowledge
   forces the opposite verdict, again with no reveal.
3. With **B1** selected, submit **INNOCENT**. Show **ACCEPTED**, the newly
   revealed badge/clue, and the presentation-only emphasis.
4. Click solved B1. Show its exact public clue selected in the clue panel and
   the canonical referenced cells highlighted on the board.

## 2:15-3:30 — Grounded two-stage Hint

1. Click **Hint** once. Explain that Stage 1 shows a deterministic
   deletion-irreducible supporting set made only from currently public clues
   and proved public verdicts.
2. Explicitly avoid calling it a unique, minimum, or clause-level proof.
3. Click **Show Target**. Show the cached target character and note that Stage 2
   performs no second reasoning request and reveals no verdict.

## 3:30-4:30 — Solve Next and Solver Details

1. Click **Solve Next**. Show exactly one accepted logical deduction and public
   reveal.
2. Open **Solver Details**. Point to the target/verdict, active public clue IDs,
   query purpose and assumption, SAT/UNSAT result, decisions, propagations,
   backtracks, runtime, and newly revealed clue ID.
3. Explain that these are recorded solver fields; the UI does not invent a
   clause proof or show a hidden assignment.

## 4:30-5:45 — Auto Solve and completion

1. Close or move Solver Details and click **Auto Solve**.
2. Let progressive public reveals finish. Point out that each step rebuilds
   from the new public snapshot and never guesses.
3. Show the compact completion banner, persistent completed board, disabled
   verdict/Hint/Solve/Auto controls, and still-enabled Solver Details.
4. Click another solved card to show that public clue inspection remains usable.

## 5:45-6:30 — Lifecycle safety

1. Click **Restart**. Show that completion, selections, feedback, Hint/support,
   clue highlights, new-reveal emphasis, and trace state are cleared.
2. Click **Load** and choose `puzzles/extension_chain_4x4.json`. Show the 4x4
   responsive board and all 16 coordinate/status areas.

## 6:30-7:30 — Extensions and architecture close

- Use **Solve Next**, then Hint Stage 1 on the 4x4 puzzle. Identify the shipped
  `IMPLIES` extension and mention that `ODD` is the second implemented extension;
  both have direct semantic and CNF encodings and occur in distributable data.
- Summarize the pipeline: public state -> automatic CNF -> team DPLL -> two
  opposite-assumption entailment queries -> forced verdict -> engine-verified
  reveal -> structured trace.
- State the final regression result: 179/179 tests and four reproducible puzzle
  experiments passing.

## Hosting and submission checklist

- Export a 5-10 minute video with narration or subtitles.
- Upload to Google Drive, not YouTube.
- Set the link to "Anyone with the link" and verify playback in a private/
  incognito window while signed out.
- Add the final link to the PDF report and test it again before the deadline.
- Do not invent or commit a placeholder video URL.
