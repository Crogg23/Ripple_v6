# The trend sweep — 2026-08-20

The census on the time axis. Every table with a trustworthy clock got the same
measurement, so the strange ones nominate themselves rather than being picked.

**371 series pulled, zero failures. 307 scored** (64 too short or too small for a
shape to mean anything). 136 of the scored series carry 100,000+ rows.

Nine shapes scored per series: pile-up, sudden stop, sudden start, collapse,
explosion, spike, level shift, gaps, seasonality.

---

## THE HEADLINE, AND IT IS UNCOMFORTABLE

**Most of the "weirdness" this sweep found is about how the data was COLLECTED,
not about what happened in the world.**

That was the parked question all along — is the line moving because reality moved
or because the counting moved — and the sweep has now demonstrated it at scale
rather than in the abstract. Of the top-ranked substantial series, the clear
majority are crawl artifacts, partial-year files, bulk backfills and per-cycle
tables that end when their cycle ends.

This is a real result, not a failure of the method. It means **any trend claim
out of this warehouse needs its denominator settled first.** The ranked list is
therefore best read as two lists, and they are separated below.

## THE CORRECTION THAT MATTERS MOST

**The opioid shipment data covers 2006–2012, not 2006–2026.**

This morning it was called "the best trend asset we own — 178.6M rows, 20.6
years." The 178.6M rows are real. The span is **seven years, not twenty**. The
2026 end date came from `_LOADED_AT` — Ripple's own download stamp — which the
old census had reported as the table's date range.

Measured now, on the transaction date itself:

| year | transactions |
|---|---:|
| 2006 | 20,918,026 |
| 2007 | 23,010,250 |
| 2008 | 24,542,457 |
| 2009 | 25,478,671 |
| 2010 | 27,388,779 |
| 2011 | 28,658,718 |
| 2012 | 28,601,120 |

Still an enormous asset, and the 37% rise across those seven years is real. But it
is a closed historical record, not a live feed — and every plan that assumed it
ran to the present needs revisiting. (This matches the public DEA release, which
covers 2006–2012.)

---

## SERIES WHERE THE WORLD APPEARS TO HAVE MOVED

Each of these still needs its denominator checked before anyone says it out loud.

**Bank failures — the crisis tail, clean.**
157 in 2010 → 92 → 51 → 24 → 18 → 8 … → 2 in 2026. One of the least ambiguous
shapes in the warehouse.

**Nursing-home deficiencies — a 446x rise, unexplained.**
273 (2017) → 3,353 → 13,783 → 4,492 (2020, the COVID dip) → 14,624 → 32,342 →
86,418 → **121,925 (2024)** → 107,508 (2025). This is the single most interesting
unexplained shape the sweep found. It is either a genuine enforcement surge or a
coverage change, and nothing in the table alone can tell you which.

**Mine-safety violations — a slow, steady decline.**
117,207 (2013) → 83,863 (2025), roughly -30% over twelve years. Consistent with
mine closures; consistent with fewer inspectors. Same fork.

**Rail crossing incidents — flat for fourteen years.**
Between 1,905 and 2,296 every single year since 2013. A safety number that has
not moved in over a decade is itself a finding.

**Consumer-finance complaints — 50x in twelve years.**
108,216 (2013) → 5,443,422 (2025); 2026 already at 4,485,349. Note: a July 2026
session investigated this and found one of its four supporting pillars was a
publication-lag artifact. The growth is real; the explanation is not settled.

**Pandemic loans — a program with a beginning and an end.**
659,440 in 2020, 309,084 in 2021, nothing after. Correct, and a useful sanity
check that the sweep reads real programme shapes properly.

## SERIES WHERE THE COLLECTION MOVED, NOT THE WORLD

Named so nobody mistakes them for findings later.

- **Vehicle-safety investigations** — 72,182 rows dated 2015 against 4,102 the
  year before and 342 the year after. A bulk load, not a year of investigations.
- **Open-data portal catalogues** (France, research-org registry) — "48x the
  historical norm" is a crawl schedule, not the world.
- **Partial-year workplace-injury files** — "791x the historical norm" is a file
  that only contains recent months.
- **Per-cycle campaign-finance tables** — each ends when its cycle ends. Correct
  by design; the sweep's "sudden stop" flag is doing its job but the answer is
  "as intended."
- **Insider derivative trades** — a handful of rows dated 2027 through 2047. Junk
  tail, tiny counts, below the repair threshold.

---

## WHAT THIS SWEEP CANNOT DO

Stated plainly so the ranked file is not over-read:

1. **It cannot tell reporting from reality.** Every shape above is consistent
   with both. Settling it needs a denominator per series — inspections per
   inspector, filings per filer, monitors online — which requires a second table
   and is the top parked branch.
2. **It is one shape per table.** Count over time, nothing else. No money sums,
   no per-entity rates, no cross-table comparison. Those are all parked.
3. **It ranks by strangeness, not importance.** A tiny scrape table with one
   pile-up period scores the same 1.00 as a genuine enforcement collapse. That is
   why the substantial-series file exists alongside the raw ranking.
4. **Seasonality is only scored on monthly series** — 25 of 307 came up strongly
   seasonal, but the year-grain tables cannot be tested for it at all.

## Files

| file | what it holds |
|---|---|
| `series.jsonl` | the raw series — one row per table, every period and its count |
| `series_ranked.csv` | all 307 scored, ranked by strangeness, with all nine sub-scores |
| `series_ranked_substantial.csv` | the 136 with 100,000+ rows — where the real findings live |
