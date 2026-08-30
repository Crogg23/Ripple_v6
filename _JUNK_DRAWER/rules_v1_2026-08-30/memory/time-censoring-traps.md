---
name: time-censoring-traps
description: "2026-08-20 — raw lag and raw duration ALWAYS shrink toward the present in any dataset; rank on fixed horizons instead, and the per-entity denominator is free inside single tables"
metadata: 
  node_type: memory
  type: project
  originSessionId: 13a9ae2d-fdfe-46b7-9279-ee7823dd5e94
  modified: 2026-08-20T17:57:31.727Z
---

**Any measurement of "how long until X" falls over time by construction, whether
or not anything changed.** An event from 1990 has had 35 years in which to be
reported; one from last month has had a month. Identically, a span that started
long ago has had time to run long, while a recent one is cut off at today. A
first-cut scorer built on 2026-08-20 ranked "reporting got faster" and "things
last shorter now" at the top of nearly *every* table in the warehouse. All of it
was this artifact.

**The fix, now in code rather than in a caveat** (`scripts/census/score_widened_shapes.py`):
- Never rank on a raw median lag or duration — report it as description only.
- Rank on a **fixed horizon**: "share reported within a year of happening",
  "share closed within a year of starting".
- Ask it only of cohorts old enough to answer, after waiting out the
  **90th-percentile** gap, not a fixed two years. A table of only-completed
  cases (e.g. retracted papers) is a survivor set at the recent end no matter
  how wide the buffer — flag it, don't trust it.
- Drop the first year of any birth curve (everyone is new) and the last year of
  any death curve (everyone looks like they just left).
- A live-at-once curve ramping from near-zero is the window opening, not growth;
  and it is meaningless at all when most rows never record an end.

**The other half, and the more valuable one: the denominator is free.** Where the
same entity recurs across years, the population is measurable *inside that one
table* — present in year Y if first seen ≤ Y and last seen ≥ Y. Dividing the
count series by that curve settles the reality-or-reporting fork with no join.
It worked for 75 tables and inverted at least one headline (water-pollution
enforcement: raw actions up 11.8x, facilities covered up 18.5x, so per facility
enforcement *fell* 35%). Caveat that must travel with it: it counts entities
VISIBLE IN THIS DATASET, a proxy for the population, never the population.

**How to apply:** before charting or claiming any time trend from this warehouse,
check which of these applies. The flags are already computed per table in
`reports/time_index/*_ranked.csv` and `rate_per_entity.csv`.

Related: [[census-date-numbers-are-unreliable]], [[warehouse-data-traps]],
[[completeness-check-traps]].
