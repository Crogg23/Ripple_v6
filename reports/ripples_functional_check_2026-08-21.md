# Making Ripples functional — 2026-08-21

What this checks: does Chris's Game-of-Life thinking model (docs/RIPPLES.md) actually
hold up against the real warehouse? Four jobs from the handoff: how stale is each
stream (Box 0), does it go up or down (Box 1), where can one thing actually see
another (coverage overlay), and one real test case (pilot rule). Cost: negligible —
no full-table warehouse scans, one cached graph file plus small aggregate queries.

---

## Box 0 — staleness: ALREADY BUILT, not rebuilt today

Two things already answer this, both pre-existing:

1. **`reports/time_index/CLOCK_FINDINGS.md`, section 6** (built 2026-08-20) — the
   most complete answer. Of 482 tables with a usable clock: **301 (62%) are current
   to 2025 or 2026. 56 have no readable end date at all.** This is the real number —
   it excludes the "our own download stamp" bug that made the opioid-shipment file
   (2006-2012 real data) look current through 2026.
2. **`LIBRARY_META.REGISTRY.V_SOURCE_FRESHNESS`** — a live warehouse view, deployed
   2026-07-02, that buckets sources fresh/due/overdue/stale/dead. Queried it live
   today: of 102 tracked sources, **47 stale, 23 fresh, 22 unknown, 8 overdue, 2
   due.** Caveat: covers only 102 of ~650 tables, and its own measurement hasn't
   refreshed since **July 12** — before last week's clock repairs. Use it as a
   secondary cross-check, not the primary answer.

**Nothing new needed to be built here.** The Aug-20 clock work already did Box 0.

## Box 1 — direction (rising/falling/flat/seasonal): ALREADY BUILT

`reports/time_index/TREND_FINDINGS.md` + `series_ranked.csv` (2026-08-20): 371
series pulled, 307 scored (one per table — the rest were too short/small to score).
Checked today: **all 307 scored tables are inside the 403 tables that carry the 953
trendable columns** — so coverage is real, not partial. The honest limits are
already written down in that file and still hold: it can't tell "the world changed"
from "the paperwork changed" (opioid file looked like a 2026 rise, was actually a
2006-2012 closed record), and it's one shape per table, not cross-table.

**Nothing new needed to be built here either.**

---

## NEIGHBORS coverage overlay — NEW, built today

The question RIPPLES.md landmine 3 asks: where can the machine actually see one
thing next to another? Built from the existing connection graph
(`outputs/connect_graph.json`, 630 tables / 4,899 verified edges) — no new
warehouse spend, just re-sliced it by subject area.

| domain | tables | hard-ID wire | fuzzy name+zip | geo-only | can't see anything |
|---|---:|---:|---:|---:|---:|
| health | 86 | 49 | 1 | 1 | 35 |
| environment | 69 | 34 | 7 | 1 | 27 |
| politics/elections | 52 | 18 | 7 | 3 | 24 |
| justice/courts | 37 | 11 | 0 | 0 | 26 |
| energy | 33 | 0 | 4 | 0 | 29 |
| corporate registry | 7 | 2 | 0 | 0 | 5 |
| finance/banking | 20 | 8 | 0 | 0 | 12 |
| labor | 14 | 11 | 2 | 1 | 0 |
| housing | 12 | 0 | 3 | 0 | 9 |
| transport | 11 | 0 | 2 | 0 | 9 |
| immigration | 10 | 3 | 0 | 0 | 7 |
| sanctions/intl | 22 | 0 | 1 | 0 | 21 |
| law enforcement | 7 | 0 | 4 | 0 | 3 |

**The "hard-ID wire" column is misleading on its own — checked whether politics
actually reaches OUT.** It doesn't. Every one of politics' 18 wire-solid links is
politics-to-politics (FEC-to-FEC, Congress-to-Voteview). Its only links to
anything outside politics are 246 name+zip fuzzy matches and 51 bare zip-code
coincidences — **zero hard-ID links out.** That confirms the memory note
("politics has zero verified cross-family joins") with real, counted numbers
instead of a recollection.

**Caught and fixed one trap along the way:** my first pass matched EPA's internal
"ICIS_FEC" (enforcement/compliance) tables into the politics bucket because
"FEC" is a substring — the exact name-collision trap CLOCK_FINDINGS.md already
warned about (its Mechanism L). Corrected before these numbers went into this
report.

**Reading it:** health, environment, and labor are well-lit — most of their
tables connect somewhere by a real ID. Energy, sanctions, transport, housing are
almost entirely dark (their own island) even though the STATE data exists — a
rule running there would find nothing to compare against. Politics is
internally wired but sealed off from the rest of the warehouse.

---

## Pilot rule — NEW, run end to end, WEAK SIGNAL (not a clean win)

**The test:** healthcare, same-owner nursing homes. When one facility's
inspection citations spike, do its same-chain siblings also spike around the
same time — more than an unrelated group of facilities would by coincidence?

**Data used:** `HEALTH__FED_CMS_NURSING_HOME` (14,700 facilities, all carry a
CHAIN_ID — 636 distinct chains, 10,479 facilities belong to a multi-facility
chain) joined via CCN to `HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES` (418,479
citations, 2017-2026).

**First attempt was a wash by construction.** Loose spike definition (+3
citations, 1.5x prior) flagged 22.7% of every inspection as a "spike" — so
common that a random group of unrelated facilities matched a same-chain group
93% of the time. That's not a finding, that's the test failing to discriminate.
Tightened to a real spike (top 5%: +11 citations AND at least tripled) and
narrowed the coincidence window from 120 to 60 days.

**Result, tightened:** of 3,180 severe spikes at chain-affiliated facilities,
**67.1% had a same-chain sibling also spike within 60 days, vs. 58.1% for a
same-size group of unrelated facilities.** A real, statistically distinguishable
gap (~9 points, n=3,180) — but a **weak** one, nowhere near the worked example's
"7 of 11 siblings spiked while unrelated homes stayed flat."

**The honest reason it might not even be real:** state health inspectors survey
facilities in their territory on their own schedule. Same-chain facilities are
often clustered in the same state. Two sister facilities getting inspected 3
weeks apart — and both catching citations — could be the **surveyor's calendar**,
not the **owner's management**. This pilot can't tell those apart with the data
pulled today. That is exactly the kind of confound the mission wants surfaced,
not smoothed over.

**What this proves about the rules layer:** the mechanics work end-to-end —
spine key exists (CCN), same-owner grouping exists (CHAIN_ID, real and
populated), the query runs cheap and fast against the live warehouse. What it
does NOT yet prove is that "neighbor rules" find real signal rather than shared
scheduling — that needs a same-state control before anyone calls this a finding.

Full spike list: `reports/pilot_rule_healthcare_spikes.csv` (3,180 rows).

---

## Proposed addition to docs/RIPPLES.md (Chris's call, not made yet)

The pilot surfaced a confound that isn't one of the four existing landmines:
**shared administrative scheduling can fake a neighbor signal** (same surveyor,
same reporting cycle, same regional office — not same owner behavior). Worth a
5th landmine, or folding into landmine 1 (the ragged clock) since it's the same
family of "the paperwork's rhythm, not the world's rhythm" problem. Your call.
