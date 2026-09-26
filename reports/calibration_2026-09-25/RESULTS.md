# Calibration test, full run results, 2026-09-26

209 frozen stories, searched against the press, judged blind, rules v3.
Every person or company named is a data match, not verified. Nothing is published.

## How the verdicts were made

- Packets: `judge_packets.py`, quote-check filtered, searcher notes stripped.
- Two independent judges per story, packets only, no web: `judge_a/`, `judge_b/`.
- They agreed on 172 of 190 newly judged stories, 90.5%.
- A third fresh judge broke the 18 ties: `judge_c/`. Every tie had a majority.
- Final set: `judge_final/` — 19 pilot verdicts kept, 190 added.
- Score: `python score.py judge_final`. Table: `scores.tsv`.

## The bins, all 209

| Bin | Count | Share | Plain meaning |
|---|---|---|---|
| Matched + more | 113 | 54% | press has it, we add a number it lacks |
| Known pattern | 58 | 28% | theme covered, our specifics aren't |
| Unreported | 19 | 9% | nobody has written it |
| Not comparable | 11 | 5% | press number differs by window or definition |
| Contradicted | 7 | 3% | a usable source says our lead is wrong |
| Matched | 1 | 0.5% | press has it, we add nothing |

## Headline rates

- Hit rate, any usable source: 114 of 209.
- Hit rate, news or trade press only: 88 of 209.
- Value added: 113 of the 114 matches carry a number the press lacks.
- Blind hits: 4 — matched only by post-cutoff coverage, not pre-known.
- Late coverage: 44 matches have some matching source after 2026-06-30.

## Novelty guess vs outcome

The 1-5 novelty guess tracked direction but not strength.
Guess 1 stories matched 11 of 13. Guess 4 stories went unreported 8 of 29.
Guess 3, the biggest group, split: 41 matched-plus-more, 23 known pattern.

## The 19 unreported

S017 S021 S032 S034 S065 S081 S088 S089 S096 S118
S129 S136 S146 S148 S182 S186 S192 S200 S205
Headlines in `stories.tsv`; verdicts with reasons in `judge_final/`.

## The 7 contradicted

S016 S059 S085 S098 S132 S139 S191
Each verdict names the claim that broke; these are lead-gen traps to study.

## Caveats carried from the search and quote check

- 50 stories had no verified source naming the entity; judges leaned on pattern bins.
- S080, S130: every naming source blocked; both landed Known pattern.
- 22 exact quotes under 8 words; weak evidence, judges warned.
- S034 had no sources at all and 8 queries logged: Unreported stands.
- Pilot note: the old single-judge pilot pass disagreed with the final
  two-judge verdicts on 5 of 19 — the two-judge process is the record.
