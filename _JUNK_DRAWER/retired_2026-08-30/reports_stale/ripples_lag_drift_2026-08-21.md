# The lag-drift pass — the reporting lag as its own indicator (2026-08-21)

**What this is:** Chris's 2026-08-21 reframing, built: the gap between "when it
happened" and "when it was reported" is a vital sign of the institution doing
the reporting. This pass reads the per-cohort lag curves the 2026-08-20 lag
sweep already computed (`reports/time_index/lag.jsonl`) and scores each pipe's
DRIFT — slower, faster, or steady — instead of just its level.
Script: `scripts/ripples/lag_drift_pass.py`,
raw output: `reports/ripples_lag_drift_2026-08-21.json`. Zero warehouse cost —
computed entirely from files on disk.

## Method, and the trap it guards against

- Impartial by construction: all 83 measured pipes get the identical
  treatment; 43 survive the qualification bar (>=6 cohorts of >=20 rows with
  a non-negative median lag).
- **Censoring guard:** each table's newest cohorts are dropped before the fit
  — the buffer is that table's own median p90 lag in whole years (so a pipe
  whose slow reports take 15 years loses its last 15 cohort-years). Without
  this, every pipe on Earth looks like it is speeding up, because slow
  reports for recent events haven't arrived yet (the 2026-08-20
  time-censoring memory).
- Verdict: early-vs-late shift of the median lag across the surviving
  cohorts (late third vs. early third): >=+20% = stretching, <=-20% =
  shrinking, else steady. (The first rule was different and wrong — see the
  validation note below.)

## Validation note (2026-08-21, same session, AFTER first publication)

A planted-signal test caught a miscalibration in the first verdict rule: a
pipe whose lag QUADRUPLED over its span could read "steady," because the
drift slope was divided by the whole-span mean. The verdict now uses the
early-vs-late shift (>=+20% = stretching, <=-20% = shrinking). The detector
now passes all planted cases (stretch/shrink/steady/mild-drift). Numbers
below are the corrected run; the first run's "0 stretching" was wrong.

## Result (corrected): 36 shrinking, 4 stretching, 1 steady, 2 unscored

**The four stretching pipes the first rule missed:**

| pipe | early -> late median lag | plain reading |
|---|---|---|
| science paper -> retraction (both copies of the retraction database) | 1,562d -> 2,031d | retractions take ever longer to happen |
| CMS provider-of-services certification pipe | 594d -> 1,738d | tripled over 1982-2013 |
| Supreme Court argument -> decision | 55d -> 85d | slower deciding, measured across 1945-2025 |

**On the shrink majority, the survivor-set caveat applies in full — a
shrink verdict is NOT proof the institution got healthier, and four
stretchers on 43 pipes is a floor, not a census of slowdowns:

1. The lag sweep's own caution applies — most of these tables hold only
   *finished* cases (every row already has its reported date), so recent
   cohorts are a survivor set biased fast.
2. Censoring masks stretching specifically: a pipe getting slower pushes its
   newest reports past the horizon, which *removes* them from the measurement
   instead of showing up as a longer lag.
3. Sensitivity check (run under the first verdict rule): doubling and
   tripling the censoring buffer kept the shrink majority intact, so the
   *shrinking* signal is robust to the buffer choice. Stretching remains
   under-counted by construction — censoring plus survivor-set both bias
   against seeing it.

## The shrink list worth believing (short lags, live spans, small buffers)

These have day-to-month scale lags and cohort spans running to the present,
so the censoring guard actually bites and the drift is measured on completed
cohorts:

| pipe | median lag | drift | plain reading |
|---|---:|---:|---|
| FDA drug recall → public enforcement report | 64d | −13%/yr | the drug-recall pipe genuinely got faster over 2011–2024 |
| FDA device recall → public enforcement report | 93d | −6%/yr | same, for devices |
| NHTSA vehicle-safety complaints → filing | 603d | −22%/yr | electronic filing era visible |
| CA lobbying change-log | 155d | −17%/yr | disclosure pipeline speeding up |
| NIH grant reporting | 899d | −16%/yr | |
| EPA water-permit single-event violations → report | 46d | −6%/yr | already fast, still tightening |

**The finding shape these carry:** "the public record is getting *faster* in
these lanes" is itself publishable context — and it sharpens every future
lead-lag claim, because a shrinking reporting lag can impersonate a
real-world acceleration in any downstream stream.

## Junk caught by doing this impartially

- Several qualifying "pipes" pair clocks that aren't an event-to-report
  pipeline at all (EU sanctions pairs *date of birth* against publication;
  the dams file pairs construction year against inspection). Their
  decade-scale "lags" are real numbers about nothing. The lag sweep's pair
  selection needs a semantic filter before this list is read as a league
  table — noted for the next pass, not fixed here.
- The two retraction-watch tables are the same data landed twice (identical
  curves to the digit) — a dedup candidate for the catalog.

## What this unlocks next

Per-entity drift (which *company's* reporting is slowing, not which table's)
is the natural deepening — same math, grouped by manufacturer/operator
instead of by table. Parked: needs per-entity queries against the warehouse,
one tick beyond this zero-cost pass.
