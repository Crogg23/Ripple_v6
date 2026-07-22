# RECEIPT PARITY — 2026-07-21 (public SBA files vs. internal snapshot)

**Task (Chris, 2026-07-21):** the SBA page's SQL receipt referenced internal warehouse
tables — it looked like a receipt but a stranger couldn't run it. Rewritten to run on
the public SBA FOIA files, then BOTH queries were executed side by side. This file is
the comparison, cell by cell, nothing papered over.

## Method

- **Internal:** the page's master query, verbatim, on `LIBRARY_RAW.LANDING.FED_SBA_LOANS`
  (single load of the SBA FOIA file, ASOFDATE **2026-03-31**, 2,174,502 rows), run live
  2026-07-21 as `RIPPLE_READER` on `SERVE_WH`.
- **Public:** the new receipt query (DuckDB 1.4.5, `read_csv` with `all_varchar=true`,
  `TRY_CAST` mirroring the internal `TRY_TO_NUMBER`) over the two current public 7(a)
  FOIA files, downloaded 2026-07-21 from the migrated portal
  (https://data.sba.gov/dataset/7a-504-foia — the OLD `/dataset/7-a-504-foia` URL the
  page previously linked now 404s; link fixed on the page):
  `FOIA_7a_FY2010_FY2019_asof_260630.csv` (255.1 MB) and
  `FOIA_7a_FY2020_Present_asof_260630.csv` (181.1 MB) — **as-of 2026-06-30, one quarter
  NEWER than the internal snapshot.** Both queries are printed on the page.

## Result: FY2019–FY2025 — all 91 cells identical

| fy | n_total | b350 | a350 | at350 | b500 | a500 | at500 | b1000 | a1000 | at1000 | b2000 | a2000 | at2000 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2019 | 51907 | 2364 | 329 | 1874 | 546 | 288 | 285 | 298 | 92 | 179 | 114 | 26 | 80 |
| 2020 | 42298 | 1876 | 279 | 1435 | 568 | 271 | 313 | 291 | 86 | 203 | 119 | 29 | 87 |
| 2021 | 51856 | 2092 | 446 | 1445 | 994 | 401 | 631 | 651 | 165 | 453 | 195 | 55 | 145 |
| 2022 | 47678 | 2453 | 151 | 1872 | 835 | 293 | 563 | 263 | 95 | 156 | 112 | 35 | 77 |
| 2023 | 57362 | 2501 | 326 | 1937 | 1615 | 234 | 1182 | 480 | 38 | 304 | 147 | 29 | 109 |
| 2024 | 70242 | 1648 | 524 | 1237 | 2885 | 215 | 2394 | 752 | 31 | 485 | 291 | 11 | 227 |
| 2025 | 78078 | 2519 | 512 | 1951 | 4008 | 272 | 3407 | 737 | 72 | 466 | 166 | 44 | 117 |

Every value above was returned identically by both runs — **91 of 91 cells, to the loan.**
The headline instruments all reproduce from public data: FY24 $2M = 291/11 (ratio 26.5),
FY24 $1M = 752/31 with 485 at exactly $1,000,000, FY22 $350k = 2,453/151 (16.2).

## Result: FY2026 — differs, for the honest reason (13 of 13 cells)

The public file carries three more months of FY26 (through 6/30) than the internal
3/31 snapshot. Every delta is positive — a growing partial year, not a restatement:

| metric | internal (asof 3/31) | public (asof 6/30) | delta |
|---|---|---|---|
| n_total | 26467 | 40824 | +14357 |
| b350 | 1711 | 2756 | +1045 |
| a350 | 117 | 187 | +70 |
| at350 | 1465 | 2390 | +925 |
| b500 | 536 | 846 | +310 |
| a500 | 115 | 193 | +78 |
| at500 | 435 | 671 | +236 |
| b1000 | 157 | 237 | +80 |
| a1000 | 56 | 84 | +28 |
| at1000 | 97 | 143 | +46 |
| b2000 | 59 | 99 | +40 |
| a2000 | 14 | 21 | +7 |
| at2000 | 39 | 64 | +25 |

**The FY26 pattern holds in the newer quarter:** $350k below/above = 14.7
(page's 3/31 value: 14.6 — the underwriting-cutoff re-spike persists); $500k = 4.4
and $1M = 2.8 (both still collapsed, exactly as the mechanism predicts with no
zero-fee cliff at those lines in FY26). No page number changes — FY26 was already
labeled partial/provisional; the page's parity section now explains the quarterly drift.

## Verdict

**A stranger with DuckDB and the two public CSVs reproduces every complete-year number
on the page exactly.** The only divergence is FY2026, and it is a snapshot-age
difference in the expected direction, stated on the page. No mismatch was found in any
closed fiscal year; nothing required papering over.

## Grader discrimination test (same session)

**The question:** 46 fact / 1 lead across 47 marts is either an accurate bill of health or a grader that can't say no. **The test:** a throwaway mart joining two real marts on a NAME field — the canonical stranger-merge — pushed through the REAL pipeline (file on disk → `dbt parse` → the same `grade_model` the committed artifacts come from), not a unit-test fixture:

```
select a.npi, b.cik
from {{ ref('health__fed_cms_nppes') }} a
join {{ ref('economics__fed_sec_edgar_company_tickers') }} b
  on upper(a.provider_organization_name_legal_business_name) = upper(b.title)
```

**Verdict, verbatim:**

```
THROWAWAY VERDICT: UNVERIFIED
  receipt: name_join @ zz_throwaway_grader_test
           ON upper(a.provider_organization_name_legal_business_name) = upper(b.title)
```

The grader demoted it and named the exact clause. **Cleanup verified:** the throwaway was deleted, the manifest re-parsed clean, and a fresh `grade_marts()` run compared against the committed `honesty/mart_grades.json` — **47 marts, grade + receipt parity EXACT.** The 46-fact bill of health is a grader that can say no, saying yes.
