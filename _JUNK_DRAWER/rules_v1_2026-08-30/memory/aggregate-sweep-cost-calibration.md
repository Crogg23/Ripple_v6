---
name: aggregate-sweep-cost-calibration
description: "2026-08-20 — a 771-query aggregate sweep over the whole warehouse took 14 minutes and ~$1-2, not the $12-20/3-6h quoted; scan-and-aggregate sweeps are far cheaper than they feel"
metadata: 
  node_type: memory
  type: project
  originSessionId: 13a9ae2d-fdfe-46b7-9279-ee7823dd5e94
  modified: 2026-08-20T17:57:14.249Z
---

**Whole-warehouse aggregate sweeps are roughly ten times cheaper and faster than
they feel when you price them.** Measured 2026-08-20: four sweeps issuing 771
queries — one to two full scans each of nearly every mart table, including
`GROUP BY` over a 20M-row table and `count(distinct)`-style entity grouping —
finished in **14 minutes total** and cost about **$1-2** of warehouse compute.
The price tag quoted to Chris beforehand was **$12-20 and 3-6 hours**.

**Why:** these workloads are pure aggregate-and-discard. Snowflake returns a
handful of rows per query, nothing is materialised, and small tables cost
essentially nothing however many of them there are. Cost tracks total bytes
scanned, which for the live marts is roughly a gigabyte-scale pass, not the
table COUNT that instinct anchors on.

**How to apply:** when quoting a read-only aggregate sweep under CLAUDE.md §8.7,
price it from *bytes scanned* (roughly: how many full passes over the biggest
tables) rather than from how many queries or how many tables. Anchor on this
measurement: ~1,400 aggregate scans over the live marts ≈ $1-2 and well under an
hour on the default warehouse. Reserve the multi-hour, multi-dollar quotes for
work that WRITES — rebuilds, materialisations, the spine rebuild (~4.5h, $10-15
per [[spine-full-rebuild-2026-08-08]]).

Still show a price tag first — the rule is not about the size of the number. But
an inflated quote is not "safe": it makes Chris decline cheap work, and it made
this session offer a needless cut-it-in-half option.

Related: [[silent-long-jobs-are-not-hung]] (the opposite failure — assuming a
quiet job is stuck), [[census-grid-built-2026-08-12]] (the $2 grid fill).
