# Threshold-Bunching Detector v2 — Calibration Battery (2026-07-13)

Harness: `scripts/detector_bunching_battery.py` (C-shaped: effective-dated line registry,
`(table, amount_col, instrument, center, time_window)` signature, metric computed per fiscal
year). Data: `LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS`, FY2025, base awards only.
Chart: `outputs/detector_bunching_battery_2026-07-13.html`.

## Metric v2 — plateau shift

`median(bins 2..9 below center) / median(bins 2..9 above center)`, $5k bins, right-closed.
The two bins adjacent to the center are excluded — that's where exact-at-line and
exact-round-value mass lives, which is what confounded v1 (single-bin ratio fired at $500k
harder than at the real line). Density floor: both plateau medians ≥ 30 or the score is n/a.

## Fire threshold — from a null, not from taste

40 seeded-random centers (seed 20260713), $5k multiples, not $25k multiples, > $60k from
every registered line value, drawn from $100k–$690k on DELIVERY ORDER. All 40 usable.

- null: min 1.072 · p50 1.151 · p90 1.340 · **p95 1.392** · max 1.431
- **Fire = score > 1.392**, because 95% of nowhere-in-particular scores below it.

## Battery results (FY2025)

| Test | Instrument | v2 | v1 | Expectation | Result | Blind? |
|---|---|---|---|---|---|---|
| P1 SAT $250k (in force, binds) | DELIVERY ORDER | **1.508** | 2.090 | fire | **fired** — above null p95 and above null MAX (1.431) | seen 07-12 |
| N1 $450k (no line) | DELIVERY ORDER | 1.111 | 1.267 | silent | silent | seen 07-12 |
| N2 $350k (SAT value effective 2025-10-01, after window) | DELIVERY ORDER | 1.320 | 1.335 | silent | silent | blind |
| N3 $750k (line binds on definitive contracts, not orders) | DELIVERY ORDER | 1.058 | 1.697 | silent | silent | blind |
| PROBE $750k subK plan | DEFINITIVE CONTRACT | 0.949 | 3.559 | spike w/o level shift | as described | **post-hoc** — shape seen in density check |

Note v1 vs v2 on N3 and the PROBE: v1 (single-bin) scores 1.697 and 3.559 there — it reacts
to at-value spikes. v2 stays at 1.058 and 0.949. That is the round-number/spike immunity the
plateau design was for.

## Per-slice computability (the C prerequisite)

P1 per fiscal quarter: Q1 1.485 · Q2 1.576 · Q3 1.514 · Q4 1.459 — every quarter clears the
threshold on ~¼ of the data. FY grain (what C will use per era) has 4× that volume. The
metric survives slicing.

## Dropped / excluded — with reasons, before running

- **TINA $2M** — binds on a pricing-basis subset (negotiated, no adequate competition); the
  table has no competition/pricing-basis column, so the bound population can't be filtered.
  Not instrument-boundable → dropped, not run.
- **PURCHASE ORDER × SAT** — mechanically capped at the SAT: no above-line population
  (plateau metric undefined) and no clean null range below the cap. Excluded.
- **Micro-purchase $10k** — the distribution below it is a reporting artifact (purchase-card
  coverage), predicted shape is inverted/unclear. Excluded.

## Known limitations (carry into v3 / C)

1. **Null scores trend with center magnitude** (1.07 at $415k → 1.43 at $685k — decay
   steepens as amounts rise). The pooled p95 is dominated by the high band: conservative for
   low centers, marginal for high ones. Fix: magnitude-matched null buckets or a detrended
   metric.
2. **Null coverage gap $100k–$410k**: the ±$60k buffers around $150k/$250k/$350k excluded the
   entire low band, so no null center sits near P1's or N2's magnitude. Given limitation 1,
   the low-band null would likely score *lower*, making the P1 fire conservative — but N2's
   1.320 against a magnitude-matched null is untested. Buffering $350k (a not-yet-effective
   value) was a pre-registered choice; it cost coverage.
3. **Two signatures observed**: procedures lines (SAT) produce a *level shift*; the
   plan-paperwork line ($750k) produced an *at-line spike with no shift* (v1 3.56, v2 0.95).
   v2 detects only the first kind by design. A production detector wanting both needs two
   scores — but the spike score must carry the round-number caveat v1 demonstrated.
4. **Pre-registration honesty**: P1/N1 distributions were seen on 07-12 (v1 run); the PROBE
   shape was seen in the density check. Only N2, N3, and the null were blind to this run.
5. SAT pre-2020 era boundary dates in the registry are marked UNVERIFIED — verify before C's
   pour, do not trust them as stored.

## Verdict

**CALIBRATED** — P1 fired (1.508 > 1.392, above every one of 40 null scores); N1/N2/N3 all
silent; threshold set from the null, not post-hoc; metric survives per-quarter slicing, so
the per-era loop C needs is already supported.

Innocent-explanations list (unchanged, still standing): 
`outputs/DETECTOR_CAL_innocent_explanations_2026-07-12.md`.
