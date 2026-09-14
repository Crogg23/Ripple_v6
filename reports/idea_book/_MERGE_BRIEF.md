# Merge brief — The Idea Book

Chris's words, verbatim: "organize all of these into an easy to read, understand,
and reference, singular source. We are going to call it 'The Idea Book'" and
"I want no information or ideas lost, but I dont want redundancy — merge and
refine where you can."

Five extract files sit in this folder, one per family:
extract_toolbox.md (TB), extract_wonder.md (WN), extract_hunch_docket.md (HD),
extract_laboratory.md (LB), extract_lens_frontier.md (LF).
Each has sections ### IDEAS, ### METHODS, ### RULES, ### FINDINGS, ### DEAD ENDS, ### LOOSE.

You are assigned ONE chapter. Read the matching section(s) in ALL FIVE extracts, fully.
Merge across families: the same idea in two families becomes ONE row.
Refine wording: BAR SPEAK, plain words, short. Every fact survives — numbers,
table names, keys, statuses, caveats. Compress by word choice, never by omission.
If two sources disagree on a number, keep both, say which said what.

## Two outputs

1. The chapter, markdown, at the path you are given. Tables only, no prose blocks
   over three lines. Group rows under #### sub-headings that make it scannable.
   Book ids: chapter letter + number, e.g. H-001. Sequential, no gaps.
   Do NOT put TB-/WN-/HD-/LB-/LF- ids in the chapter. Cite original source files
   by short name in the last column, e.g. "tool box; docket v2; wonder 14".

2. A crosswalk CSV at the path you are given: `book_id,extract_id` one line per pair.
   EVERY extract row in your section(s) must appear at least once. If you judge an
   extract row to be pure noise with nothing to keep, it still gets a crosswalk line
   with book_id = DROP and a third column saying why. Expect near-zero DROPs.

## Known overlaps to expect
- TB IDEAS holds all 542 docket questions; HD IDEAS holds the same 542 as 150 hunches
  plus 392 docket v2 lines, with richer status. Merge on the docket/hunch number.
- TB RULES copies the dated trap log that also lives in .claude/traps.md; HD RULES holds
  the same traps from the hunch cards. Merge by the trap's mechanism, keep the newest date.
- WN wonders and HD hunches often restate each other. Merge only when it is the same
  question on the same tables; otherwise cross-reference in the last column.
- Wonder Wall rankings exist only in WN. Keep every score.

## Rules
- Table cells are fragments. Max ~20 words per cell, except the idea line itself, max 30.
- At the top of the chapter: a one-line count of rows, and a two-line "how to use this chapter".
- Use Bash to read files in chunks; do not stop early. Write with heredocs or Write, appending.
