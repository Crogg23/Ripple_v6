# The investigation catalog — everything to throw at the warehouse

Three layers. Lenses find candidates. Postures decide how you walk in.
Verification decides which candidates are real. Use all three, in that order.

---

## Layer 1 — Lenses (52)

Patterns borrowed from math, forensics, and science. Each one: pick a table,
pick a pattern, ask if real data fits or fights it.

Full list with worked chains: `reports/detective_toolkit_warehouse_map_2026-09-07.md`

Categories: math laws, forensic tricks, cheap tells, network science,
stats of fraud, anomaly hunting, physics/bio analogies, game theory,
text/language, time series, geospatial, causal/bias traps, epidemiology,
info theory.

---

## Layer 2 — Postures (7)

Not patterns — stances. How you walk into the data before picking a lens.

| Posture | The move | What it surfaces |
|---|---|---|
| Follow one entity | pick a name, pull every table it touches | a life story, not a stat |
| Reverse the question | start from an outcome, walk back | the actor everyone missed |
| Chase a random row | follow every foreign key three hops out | blind spots you'd never search |
| Assume guilt first | take the top-10, try to prove it's clean | forces rigor on the "normal" ones |
| Absence hunting | ask what should be there and isn't | the gap is the finding |
| Cross-domain collision | join two schemas with no business relation | correlations nobody built for |
| Outsider's question | ask what a journalist or lawyer asks first | plain beats clever |

---

## Layer 3 — Verification, the missing piece

A lens plus a posture finds a candidate. This layer decides if it's real.
Skip this layer and every finding is a guess dressed as a fact.

**Provenance skepticism**
- Check: who collected this table, what's their incentive to shade it
- Hit: source is neutral, third-party, no stake in the number
- Miss: source benefits from the number looking a certain way — treat the finding as soft

**External baseline**
- Check: does an outside source confirm the same fact independently
- Hit: matches a second, unrelated source
- Miss: only your warehouse shows it — could be a load bug, not a real pattern

**Replication check**
- Check: does the finding hold in a second year, state, or dataset
- Hit: holds across at least one more slice
- Miss: one-off — likely noise, not a pattern

**Red-team your own pipeline**
- Check: could the load script or a join be the actual cause, not the data
- Hit: pipeline reviewed, finding survives
- Miss: a script bug or duplicate join explains it — not a warehouse finding, a code bug

**The story test**
- Check: is this true AND does it explain something someone would care about
- True and boring: log it, move on
- True and explains something: that's the portfolio piece

---

## The full loop, one sentence each step

- Pick a posture — how am I walking in
- Pick a lens — what pattern am I testing
- Get a candidate — a table, a row, a number that stands out
- Run it through all five verification checks
- Only then: write it up

**→ Nothing here is ranked. Pick one posture, one lens, one table, and run the loop once.**
