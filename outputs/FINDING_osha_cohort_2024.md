# FINDING — OSHA workplace-safety peer-cohort outliers, 2024

**STATUS: READY FOR HUMAN REVIEW. NOT PUBLISHED.** Per CLAUDE.md's hard rule, auto-publish
is structurally blocked — every row below sits as a `pending` LEAD in
`LIBRARY_META.CONNECT.LEADS` until a human runs `connect review lead <LEAD_ID> confirmed`
and then `scripts/publish_lead.py` explicitly confirms it. This document and the LEADS
rows are the finding; neither is a publication.

## What this is, and is not

**The claim:** in 2024, these employers reported a DART (Days Away/Restricted/Transferred)
injury rate substantially higher than the POOLED rate of their own peer cohort — same
NAICS-4 industry, same employee-count band. "Substantially higher" means the establishment's
own rate divides out to 2x or more of the cohort's total-cases-over-total-hours rate, with
at least 5 DART cases (so a 1-2 case site can't top the list on a tiny denominator).

**What this does NOT claim:**
- **Not negligence, not wrongdoing, not a violation.** A peer-relative injury rate is a
  signal to look at, not a verdict. Whether any of these employers did something wrong is
  a taste/RED-lane question (CLAUDE.md §4) for a human, never this pipeline.
- **Not a ranking of "most dangerous jobs."** The cohort structure holds industry and size
  roughly constant on purpose — this ranks employers against employers doing the same kind
  of work at the same kind of scale, not against each other in the raw.
- **Not proof any specific injury was preventable.** OSHA 300A is a self-reported annual
  summary, not an incident investigation.

## The numbers

- 355,360 establishment-year filings in `FED_OSHA_ITA_300A_SUMMARY_2024`.
- 148,940 establishments survived every honesty filter and were scored against a peer
  cohort (63,474 distinct employers, 1,209 NAICS-4 × size-band cohorts).
- Of those, **16,215** cleared the outlier bar (≥5 DART cases, ≥2x the cohort's pooled
  rate) — this is the full finding set, persisted as `LEADS` rows and in
  `outputs/cohort_outliers_2024.csv`.
- Across the scored population: 48.67B hours worked, 777,862 DART cases, 462 deaths.

### Top 10 outliers (by fold vs. cohort pooled rate)

| Fold | DART rate | Cohort pooled | Cases | Employer (site) | NAICS-4 (industry) | Size band |
|---|---|---|---|---|---|---|
| 61.99x | 85.14 | 1.37 | 38 | NY-Presbyterian / Morgan Stanley Children's Hosp. (New York, NY) | 6221 (hospitals) | 50-99 |
| 58.35x | 82.64 | 1.42 | 12 | Quality Behavioral Outcomes LLC (Aurora, CO) | 6211 (ABA therapy) | 20-49 |
| 54.02x | 69.59 | 1.29 | 26 | BluSky Restoration Contractors (Waterville, OH) | 2362 (bldg construction) | 20-49 |
| 44.06x | 91.66 | 2.08 | 18 | Sunrun Inc (Rocky Hill, CT) | 2382 (solar install) | 20-49 |
| 43.86x | 96.05 | 2.19 | 18 | Renew It Group LLC (Charlevoix, MI) | 2383 (deck construction) | 20-49 |
| 42.47x | 23.57 | 0.55 | 55 | City of San Diego — Lifeguards Dispatch | 5611 (business mgmt) | 250-999 |
| 37.99x | 138.93 | 3.66 | 31 | J Polep Distribution Services (Wilmington, MA) | 4244 (grocery wholesale) | 20-49 |
| 36.96x | 47.62 | 1.29 | 10 | Smartsign (Oxford, NC) | 2362 (bldg construction) | 20-49 |
| 31.59x | 44.74 | 1.42 | 8 | Quality Behavioral Outcomes LLC (Aurora, CO) — 2nd site | 6211 (ABA therapy) | 20-49 |
| 31.44x | 28.53 | 0.91 | 15 | Prishaan & Priyam Logistics (Glastonbury, CT) | 5416 (customs consulting) | 100-249 |

Full ranked table (all 16,215): `outputs/cohort_outliers_2024.csv` and
`SELECT * FROM LIBRARY_META.CONNECT.LEADS WHERE RULE_NAME='osha_cohort_outlier_2024'`.

### Deaths — a separate list, never buried in the rate ranking

462 total deaths across the scored population. Top of the death list (deaths desc):

| Deaths | Employer (site) | DART rate | vs. cohort |
|---|---|---|---|
| 4 | Tri-County Metro Transportation Dist. of Oregon — Powell Maint. Bldg (Portland, OR) | 1.19 | 0.37x (below cohort) |
| 3 | Big D Builders, Inc. (Meridian, ID) | 16.97 | 13.17x |
| 2 | American Med Response — Weatherford, OK | 14.72 | 8.98x |
| 2 | Wyndham Vacation Ownership — Cathedral City, CA | 13.64 | 7.60x |
| 2 | Baltimore City DPW — Reedbird Yard | 30.00 | 6.97x |
| 2 | Penske Truck Leasing — Chesapeake, VA | 9.60 | 3.40x |
| 2 | Wilson Construction Co. — Canby, OR | 0.95 | 1.91x |
| 2 | Dairy Support Services Co. — Truxton, NY | 4.65 | 1.85x |
| 2 | Metro Govt. of Nashville & Davidson County | 4.89 | 1.68x |
| 2 | City of Burnsville, MN — Police | 6.21 | 1.57x |

A death that shows up with a LOW fold (e.g. the 4-death Portland transit site at 0.37x) is
NOT reassuring — it means the establishment's overall injury rate is unremarkable even
though it had 4 deaths. Deaths are reported here on their own terms, not folded into or
excused by the rate.

## Guard re-verification (Step 1 — CLAUDE.md §7: COUNT(DISTINCT), not COUNT)

All four checks were re-run against the CURRENT ranked output (16,215 rows), not read from
last session's comments:

1. **Plausibility gate** (hours/employee must be 800–3,500): `0` violations in the ranked set.
2. **Copy-pasted-denominator guard** (same EIN+employees+hours reused across ≥3 sites):
   `0` violating groups in the ranked set.
3. **Comparator audit**: every `WHERE`/`ORDER BY` in `connect/cohort.py` that ranks or
   filters uses `fold_vs_pooled` (cohort's total-cases/total-hours). `fold_vs_median` exists
   only as a reference column, never used to rank or gate — confirmed by grep, not inference.
4. **Top-10 raw spot-check**: hours/employee for the top 10 range 862–2,231 (all inside a
   real full-time-to-heavy-overtime band); no row is a repeat entity under a different name.

## Entity-quality gaps (Step 2)

**2a — ESTABLISHMENT_ID fallback**: `0` of 355,360 filings fell back to the address key —
`ESTABLISHMENT_ID` is fully populated and distinct-per-row in the 2024 file, so the
address-fallback risk documented in `cohort.py`'s grain comment does not materialize this
year. **However**, checking DIDN'T stop there (CLAUDE.md §7): a full-population `COUNT`
alone would have missed a different, real issue —

**Found and fixed**: 12 groups (24 of ~16,260 pre-fix ranked rows) were the SAME physical
establishment filed TWICE under two different `ESTABLISHMENT_ID` values — identical EIN,
name, city/state, employee count, and hours agreeing to within 5 (rounding). Examples:
Commodity Forwarders LAX-5814 (552,815 hours filed under two IDs), US Foods Norcross
(362,230 vs 362,231 hours). Ranking both would have counted one workplace as two entries.
**Fix applied**: added a `dup_site` guard to `connect/cohort.py` (same policy as the
existing `dup_denom` guard — exclude rather than guess which copy is authoritative). All
four guard checks above were re-run AFTER this fix and still pass. Net effect: outliers
dropped from 16,260 to 16,215; total deaths in the scored population dropped from 464 to 462
(2 death-reporting duplicate filings removed); the top-3 outliers are unchanged.

**2b — NAICS-4 granularity**: eyeballing the top 25's NAICS-4 codes (hospitals, ABA
therapy, building/deck/solar construction, staffing, nursing homes, groceries wholesale) —
these are genuinely comparable business types at NAICS-4. **One documented limitation**:
two top-25 entries (Wegmans' Rochester distribution site, UPS's St. Joseph regional office)
are filed under **NAICS 5511 "Corporate Managing Offices,"** a headquarters/management
classification, not a warehouse or logistics code. This is self-reported by the filer, not
something this pipeline can correct — a distribution or logistics site classified as a
management office would be compared against a cohort of desk-job management offices, which
could inflate its apparent outlier status relative to its real peers (other distribution
centers). Flagged here as a limitation on those two rows specifically; not fixed, because
correcting self-reported NAICS classification is out of this task's scope.

## The receipt (Step 3 — the run-it-yourself proof)

- **Frozen SQL**: `connect/cohort_leads.py::build_compiled_sql()` wraps `cohort.build_sql()`
  with the exact ranking filter (`dart_cases >= 5 AND fold_vs_pooled >= 2`). No
  `CURRENT_DATE` or other non-deterministic function anywhere in the query — re-running it
  against the same data snapshot reproduces identical numbers.
- **SQL_SHA256**: computed via `receipt.sql_sha256()`, stored per lead. Verified: hashing
  the stored `COMPILED_SQL` text reproduces the stored `SQL_SHA256` for every spot-checked
  lead.
- **AS_OF_DATE**: frozen to `2026-07-30` (the day this finding was built).
- **SOURCE_SNAPSHOTS**: pinned to `FED_OSHA_ITA_300A_SUMMARY_2024`'s `SOURCE_RUN_ID` /
  `SRC_SHA256` / `INGESTED_AT`. **Caveat, documented not silently fixed**: this table uses
  the non-underscore-prefixed provenance column names (like the already-documented
  `FED_IRS_BMF` case in `leads_specs.py`), and it has no matching row in
  `LIBRARY_META.INGEST_LOGS.INGEST_RUNS` — so `ingest_status` reads `None` rather than a
  real status. `receipt.resolve_snapshots()` was extended with a fallback for this naming
  convention (benefits this and the pre-existing IRS_BMF gap) so the pin is real (a genuine
  `SOURCE_RUN_ID` + content hash), just missing the INGEST_RUNS-sourced status field.
- **Persisted as**: 16,215 rows in `LIBRARY_META.CONNECT.LEADS`, `RULE_NAME =
  'osha_cohort_outlier_2024'`. This is the SAME table and the SAME persistence helpers
  (`leads._merge_leads`, `leads._ensure_leads_table`, `leads._expire_rule`,
  `safety.gate_rows`) every other cross-domain lead uses — no parallel finding format.
  `connect/cohort_leads.py` is the adapter: it does not go through `leads.compile_sql` /
  `leads_specs.JOBS` (that machinery assumes a hard-key LEFT⋈RIGHT intersection; this
  finding is a single-source aggregation, a different shape) — instead it registers a
  minimal stand-in spec (`COHORT_SPECS`) so `receipt.py`'s existing `assemble()` /
  `render()` / `_verify()` work unmodified for this rule too.
- **Verified**: `python -m connect receipt --id <LEAD_ID> --check` re-runs the stored SQL
  read-only and confirms reproduction, spot-checked on the #1 and #2 outliers:
  - `LEAD_4fbdcbe713f1d29f` (NY-Presbyterian) → `✓ reproduced — 16215 rows; entity
    133957095|1208757 present`
  - `LEAD_941ff7f9f8fc78c4` (Quality Behavioral Outcomes) → `✓ reproduced — 16215 rows;
    entity 943263409|1387182 present`

## How to review one of these leads yourself

```
python -m connect receipt --id LEAD_4fbdcbe713f1d29f          # full receipt, human-readable
python -m connect receipt --id LEAD_4fbdcbe713f1d29f --check  # re-runs the SQL, confirms it
python -m connect receipt --id LEAD_4fbdcbe713f1d29f --json   # machine-readable receipt
```

## Sign-off path (not taken here)

```
python -m connect review --kind lead --id LEAD_xxxx --decision confirmed --by <reviewer>
python scripts/publish_lead.py   # the ONLY path that can set PUBLISHED=True
```

Nothing above has been run. Every one of the 16,215 rows currently reads `REVIEW_STATE =
pending`, `PUBLISHED = False`.
