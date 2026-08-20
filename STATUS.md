# RIPPLE STATUS — 2026-08-20 (evening) — The whole warehouse is on one timeline

*One screen. Rewritten (never appended) at the end of every session. Sessions read
this at boot and brief Chris in chat — Chris never has to open it.*

**BROKE: two items, both carried in, neither touched today.** (1) The roll-call
vote mart still disagrees with its Python-built twin — standing since 2026-08-18.
(2) Twelve Python test modules fail to COLLECT on this machine for a missing
charting library, hiding ~1,400 tests, so "the suite passed" carries an asterisk
until it is reinstalled. **The Python suite was not run this session** — no
existing model, macro or test was modified. The dbt side WAS run: 435 new models
built green and the new guard test passes.

---

## TODAY, EVENING SESSION — two pieces of work

Chris picked "widen the sweep" first. Widening it produced the denominators for
free. He then picked the canonical-clock rollout, which is now built.

### Piece 1 — the widened time census

Four new shapes across every table with a trustworthy clock. **771 measurements,
zero failures, 14 minutes of warehouse time.** Reporting lag (83 tables), spans
(70), category mix (309), things arriving and leaving (329, of which 216 have a
repeating entity).

**The parked "denominators" branch turned out to be answerable for 75 tables with
no second table.** Where the same entity recurs across years, the population is
measurable inside that one table — present in a year if first seen on or before
it and last seen on or after it.

- **Nursing-home deficiencies — the 446x was mostly coverage.** Facilities went
  1,823 → 13,451. Per facility, 4.8 → 7.8: a real 62% rise, not 446x.
- **Mine accidents — the fall survives.** Mines roughly halved, accidents fell
  63%, per mine still down 32%.
- **Consumer complaints — survives strongly.** Companies only tripled while
  complaints rose 28x; per company, up 7x.
- **Water-pollution enforcement — the raw count and the rate point OPPOSITE
  ways.** Actions rose 11.8x, facilities covered rose 18.5x, so per facility
  enforcement FELL 35%.

**A metric that almost shipped wrong, fixed in code.** The first scorer ranked
"reporting got faster" and "things last shorter now" at the top of nearly every
table. Both are the same artifact — an old record has had years in which to be
reported or to run long, a recent one has not, so raw medians always fall toward
the present. Everything is now ranked on a fixed horizon, asked only of cohorts
old enough to answer, after waiting out the 90th-percentile tail. **After the fix
only 2 tables show a defensible change in reporting promptness.**

Mix flips worth a second look, all unverified and single-source: water
enforcement flipping federal → state (crossover 1987, settled by 2011); new power
generators flipping hydro → gas → solar (solar 56–66% of new units since 2014,
carries a survivorship caveat); judicial confirmations flipping voice vote →
roll call (crossover 2001).

### Piece 2 — the canonical clock, rolled out

**435 models, 92 seconds, zero failures. The guard test passes.**

Built as a VIEW layer, not by editing the marts — adding three columns to 600+
models would have meant rebuilding every mart. Views cost nothing to create or
store, leave the tables untouched, and regenerate in seconds when a clock label
is corrected, which matters because the labels are one day old.

| what | where |
|---|---|
| 403 canonical views | every original column plus `ripple_ts` / `ripple_grain` / `ripple_clock` / `ripple_source` |
| 31 domain rollups | one row per (source, clock, grain, day) with a count |
| the shared timeline | 1,160,701 rows standing in for 719,999,851 underlying rows across 403 sources |
| the control table | all 647 live tables and the clock chosen for each — runs on plain SQL, no AI at runtime |
| the guard | six ways the registry and the views can drift, all fatal to the build |

**Coverage stated honestly: 403 of 647 tables get a clock.** The other 244 are in
the registry too, each saying which kind of nothing it is — 165 never examined,
43 with time-shaped names holding no readable value, **20 carrying nothing but
Ripple's own download stamp**, 16 with no time data at all.

**Two rules the layer carries as tags rather than hoping people remember.** A
year-grain source snaps to Jan 1, so charting mixed grains without faceting on
grain invents a New Year's Day spike (121 of 403 sources are year-grain). And
summing a "happened" source with a "reported" source adds two different questions.

**Already answers:** what the whole warehouse saw in any month; which sources went
quiet and exactly when (Open Payments stops dead at 2023-12-31, 14.7M rows; the
FBI crime explorer at 2023-12-01; pandemic loans at 2021-07-19); whether any
source covers a date at all; and how many independent sources touch the same day.

## Live/open items

- **The timeline counts; it does not join.** Row detail lives in the per-table
  views, one source at a time. A row-level cross-warehouse timeline would be
  ~720M rows and has not been built.
- **20 tables carry only a download stamp.** These are the fixable ones — they
  need a real clock at ingest, upstream of the layer.
- **Whether a clock LABEL is correct is not tested.** The guard enforces that the
  registry and the warehouse agree; the labels themselves came from this
  morning's review pass and are revisable.
- **30 tables could not get a per-entity rate** because the count sweep and the
  cohort sweep picked different clocks. **113 tables have no repeating entity**,
  so they need an outside denominator.
- **13 tables have their two clocks in the wrong order** — the aircraft registry
  compares year-of-manufacture against last-registry-action, which is not a
  reporting gap. Those labels need revisiting.
- **The loader can still produce the microsecond bug.** Read side immune, write
  side untouched.
- Carried unchanged: opioid data covers 2006–2012 not 2006–2026; nobody has read
  the map (4,899 connections); 182 columns with literal 'nan' text; FAERS 76%
  dup; two FDA device tables raw; ~900 gated portal tables; DEA numbers
  single-source; roll-call mart rebuild; source-registry reconciliation; six
  unparseable polygon tables; table-count discrepancy.

**YOUR MOVE:** the clock work is done, so the two remaining warehouse options
from earlier are still open — push the denominator method outward to the tables
it could not reach, or chase the federal-to-state enforcement handoff into an
actual mechanism. Also still standing and untouched for two days: the front-door
website crash course queued 2026-08-19.

**NEXT SESSION (warehouse lane):** Chris's pick of those two.
**NEXT SESSION (website lane):** Webflow crash course per the 8/19 handoff doc.

**Tests:** dbt — 435 timeline models built green; the new registry guard passes;
this morning's two datetime guards were passing and were not modified. Python
suite not run (nothing in it was touched). Last full run: 1,671 passed, 2 skipped,
1 failed (the known roll-call mismatch), 12 collection errors.

**COST today (evening session):** under $3 of warehouse compute all in — the four
sweeps ran in 14 minutes, the 435-model build in 92 seconds. Quoted $12–20 for
the sweeps (actual ~$1–2) and $2–4 for the build (actual under $1). **Both
estimates ran high; the sweep one by roughly ten times.** All scoring and the
per-entity rates are local arithmetic, zero warehouse. Earlier session today:
~$6–8 warehouse plus ~$20–40 of agent tokens for the labelling pass.
