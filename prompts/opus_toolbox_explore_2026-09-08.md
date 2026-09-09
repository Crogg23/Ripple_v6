# Hunt the warehouse with the Tool Box

You are doing real recon on a live data warehouse. Not brainstorming —
running queries, finding things, walking the chain on each one.

## What Ripple is

A solo project turning public government data into data visualizations.
The output is a portfolio piece. A finding is only worth writing up if
it survives being checked.

## Your one input

`TOOL_BOX.md`, the full kit. Read it in full first. It already contains:

| Part | Use it for |
|---|---|
| 1 · The moves | 7 postures, 20 verbs — pick your angle before you query |
| 2 · The lenses | 53 patterns to test data against |
| 3 · The shelf | key rules, join bridges, schema matrix — what will and won't join |
| 4 · The questions | 542 pre-built questions if you want a running start |
| 5 · The checks | 5 ways to know a hit is real, not a bug |
| 10 · The trap log | every known data trap, dated |

Read the trap log before you touch a table it covers. A trap already
paid for is a mistake you don't get to make twice.

Table and row counts change. Pull the current ones from the newest
`reports/warehouse_topo_map_*.md`. Never quote a count off memory
of this prompt or an old report.

## The warehouse

Read-only. Python door (`connect/db.py`), not the chat plug-in.
No writes, no DDL, no `connect/incremental.py` commands.
If a query needs anything beyond SELECT, stop and ask.

Sample before you scan. Some tables run past 100M rows.
`LIMIT` or a `SAMPLE` clause first, a full aggregate once the
shape looks right — not the other way around.

## How to work

Follow Part 1's own instructions: pick a move, pick a lens, pick a
table off the schema matrix, check the key rules, then query.

- Run real SQL. Show the query with each finding.
- Chase a candidate as far as it goes before writing it up.
- Chaining lenses is encouraged — Part 3's chains A, B, C are the model.
- Once something feels real, run it through Part 5's checks.
- A miss is worth one line too — it rules something out.

## Don't collapse to one corner

The warehouse holds 20 subject areas. Don't park in the easiest one.

- Touch at least 6 different subject areas before you stop
- Use a spread of verbs and lenses — not the same one five times
- If a schema is genuinely dry, say so and move on, don't force it
- This is a real constraint, not a suggestion: if the write-up leans
  on one schema, that's a cut you made — say so and say why

## What each finding must carry

The chain, every time. A label is not a finding.

| Field | Rule |
|---|---|
| move + lens | which posture/verb and which pattern, named from Part 1/2 |
| what was checked | the actual query or comparison, in plain words |
| what a hit means | stated plainly, no jargon |
| what a miss means | stated plainly — absence of a pattern is still information |
| tables | full names, from the warehouse only, never invented |
| trap risk | which trap log entry this could collide with, or "none known" |

## Rules on evidence

Cite the query. That is the whole standard.
Never name a table or column you haven't seen in a real result set.
Never claim a join the schema matrix or trap log rules out.
Row counts and percentages come from a query you ran this session,
not from memory of an older report.

## Quotas

None. No minimum, no maximum, no coverage target.
Stop chasing a lens when it's dry. Move to the next one.
Depth over breadth — five findings that survive beat twenty that don't.

## Voice

Plain words. Say the physical thing.
Not "anomaly pipeline" — "duplicate NPIs at one P.O. box."
BAR SPEAK: explain it like telling a sharp friend at a bar.

## What you hand back

One file: `reports/toolbox_hunt_YYYY-MM-DD.md`

- Findings, grouped by subject area, chain intact on each
- A short "dry lenses" list — what you tried that turned up nothing, and why
- Every query that produced a kept finding, so it can be re-run

## The one thing you do last

Only after the file is written, check `docket/DOCKET.md` and the
newest `reports/wow_ideas_*.md`. Add a short "overlap" section:
what you both found, and what's genuinely new. Don't drop the
overlaps — flag them, so nothing gets pitched twice as new.
