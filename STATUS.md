# RIPPLE STATUS — 2026-08-20 (evening) — The denominator turned out to be free

*One screen. Rewritten (never appended) at the end of every session. Sessions read
this at boot and brief Chris in chat — Chris never has to open it.*

**BROKE: two items, both carried in, neither touched today.** (1) The roll-call
vote mart still disagrees with its Python-built twin — standing since 2026-08-18.
(2) Twelve Python test modules fail to COLLECT on this machine for a missing
charting library. That hides ~1,400 tests, so "the suite passed" carries an
asterisk until it is reinstalled. **Nothing today ran the Python suite** — this
session added new standalone scripts and report files, and touched no model,
macro or test.

---

## TODAY, SECOND SESSION — the widened time census

Chris picked "widen the sweep" over the two alternatives (denominators first, or
the canonical-column rollout). The irony is that widening it produced the
denominators anyway, for free.

### What ran

Four new shapes across every table with a trustworthy clock. **771 measurements,
zero failures, 14 minutes of warehouse time.**

| shape | tables | what it asks |
|---|---:|---|
| reporting lag | 83 | how long between a thing happening and being told |
| spans | 70 | what was live at once, how long things last, what never closed |
| category mix | 309 | whether the make-up changed, not just the amount |
| entity cohorts | 329 | things arriving and leaving; 216 had a repeating entity |

### The result that changes the plan

**The parked "denominators" branch is answered for 75 tables with no second
table and no extra warehouse spend.** Where the same entity recurs across years,
the population is measurable inside that one table — an entity is present in a
year if it was first seen on or before it and last seen on or after it. Dividing
the count sweep's series by that curve settles the reality-or-reporting fork:

- **Nursing-home deficiencies — the 446x was mostly coverage.** Facilities went
  1,823 → 13,451. Per facility, deficiencies went 4.8 → 7.8. A real 62% rise,
  not a 446x one.
- **Mine accidents — the fall survives.** Mines roughly halved, accidents fell
  63%, and per mine it is still down 32%.
- **Mine violations — smaller than it looked.** Mine count barely moved (0.94x),
  violations fell 21%, per mine down 18%.
- **Consumer complaints — survives strongly.** Companies complained about only
  tripled while complaints rose 28x; per company, up 7x.
- **Water-pollution enforcement — the raw count and the rate point OPPOSITE
  ways.** Informal enforcement actions rose 11.8x, but the facilities covered
  rose 18.5x, so per facility enforcement FELL 35%.

### The trap that almost shipped

The first version of the scorer ranked "reporting got faster" and "things last
shorter now" at the top of nearly every table. Both are the same artifact: an
old record has had years in which to be reported or to run long, a recent one
has not, so a raw median always falls toward the present. Nothing is ranked on
a raw median any more. Everything is ranked on a fixed horizon — share reported
within a year, share closed within a year — asked only of cohorts old enough to
answer, after waiting out the 90th-percentile tail. **After the fix, only 2
tables show a defensible change in reporting promptness.**

### Mix findings worth a second look (unverified, single-source)

- Water-pollution enforcement actions flip from federal (99%) to state (99%),
  crossing over in 1987 and settled by 2011.
- New power generators flip hydro → oil/gas → solar; solar holds 56–66% of new
  units since 2014. Carries a survivorship caveat — the register only holds what
  still stands.
- Judicial confirmations flip from voice vote (90–100% for two centuries) to
  roll call (97–100% since 2019), crossing over in 2001.

### Named so nobody mistakes them for findings later

Fields arriving mid-series (blank in the old records), lifecycle status columns
that read as of today rather than as of the row's year, registers dated by birth
where early years are a survivor list, populations that are really a coverage
ramp, and **13 tables whose two clocks run in the wrong order** — the aircraft
registry compares year-of-manufacture against last-registry-action, which is not
a reporting gap at all. Those clock labels need revisiting.

## Live/open items

- **The canonical column is still not rolled out.** Standard, calendar and guard
  exist; the 686 tables do not each expose one canonical timestamp with grain and
  clock tags. Unchanged from this morning.
- **30 tables could not get a per-entity rate** because the count sweep and the
  cohort sweep picked different clocks. Reconciling that would add them.
- **113 tables had no repeating entity**, so they get no denominator this way.
- **The loader can still produce the microsecond bug.** Read side immune, write
  side untouched.
- **The scanner still sweeps 40 July backup-schema tables by default.** The new
  sweeps filter them; the older scan did not.
- Carried unchanged: opioid data covers 2006–2012 not 2006–2026; nobody has read
  the map (4,899 connections); 182 columns with literal 'nan' text; FAERS 76%
  dup; two FDA device tables raw; ~900 gated portal tables; DEA numbers
  single-source; roll-call mart rebuild; source-registry reconciliation; six
  unparseable polygon tables; table-count discrepancy.

**YOUR MOVE:** three ways forward. (1) Push the denominator work outward — the
30 clock-mismatched tables plus real external denominators for the ones with no
repeating entity. (2) Chase one of the mix flips into a mechanism, starting with
the federal-to-state enforcement handoff, which is the most mission-shaped thing
the sweep found. (3) The canonical-column rollout, still standing. Also still
standing: the front-door website crash course, queued 2026-08-19 and untouched.

**NEXT SESSION (warehouse lane):** Chris's pick from the three above.
**NEXT SESSION (website lane):** Webflow crash course per the 8/19 handoff doc.

**Tests:** not run this session — nothing in the build was touched. The dbt
datetime guards were passing as of this morning's session and were not modified.
Last full Python run: 1,671 passed, 2 skipped, 1 failed (the known roll-call
mismatch), 12 collection errors (missing charting library).

**COST today (this session):** ~$1–2 of warehouse compute — the four sweeps ran
in 14 minutes total. **Quoted $12–20 and 3–6 hours; the estimate was roughly ten
times too high.** All scoring and the per-entity rates are pure local arithmetic,
zero warehouse. Earlier session today: ~$6–8 warehouse plus ~$20–40 of agent
tokens for the labelling pass.
