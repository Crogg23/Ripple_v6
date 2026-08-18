# The Census Grid — FILLED — 2026-08-17

*The fill phase of the census grid: measured reality attached to every mart-layer
model. Sources: warehouse catalog metadata (Tier A, pennies), the 2026-08-11
verification scan reused for 562 tables ($0 new), and 27 fresh table scans
(Tier B, the new court tables + the mart views over large raw tables).
All queries read-only aggregates. Builders: `scripts/census/fill_tier_a.py`,
`fill_tier_b.py`, `staging_raw_crosswalk.py`, `merge_fill.py`.*

## The one-screen picture

- **All 589 mart-layer models measured. Zero unscanned. 1,227,375,627 total rows.**
- **349 models carry a real date range**; **306 are fresh into 2026**; 12 are
  stale (nothing after 2024-01-01) — list below.
- **1,170 of 1,172 staging models** now carry a measured row count via a parsed
  staging→raw reference crosswalk (`staging_to_raw.csv`) — the first hard key in
  the source-bookkeeping reconciliation. **2 staging views are broken**: their
  raw tables no longer exist (college-scorecard institutions, OSHA inspections
  — check whether re-pulls landed under new table names, the known spine-spec
  drift pattern).
- The pension tax-ID check is **PASSED**: 5,176 rows, 100% filled, 4,431
  distinct employers, zero sentinel masking, real sponsor names on sample.
  **Join trap:** values run 4–9 digits — leading zeros stripped; always join on
  a 9-digit zero-padded cast.

## What the fill found (the data-trap census, now with numbers)

These are hypotheses ranked by measured size, not verdicts — each needs a look
before repair (completeness-check trap rule).

**Duplicate-heavy tables (>5% identical full rows):** 11 models. Worst:
immigration USCIS data 94.5% dup, DHS OHSS 77.2%, **FAERS drug reactions 76.2%
dup of 20.6M rows** (if real, the adverse-event reaction table is ~4× smaller
than it looks), FEC committees 23.1%, FEC candidates 19.1%.

**Epoch-1970 date poisoning (>1k rows):** 20 models. Worst: **federal contracts
— all 20M rows carry at least one 1970 date column**, the 990 e-file index 3.2M,
FAA registry 1.2M, union filings 589k. Same TRY_TO_DATE epoch trap as the FAA
find on 2026-08-11.

**Far-future dates (>100 rows):** 23 models. Worst: consumer-product injuries
(NEISS) 9.8M rows, ICIJ offshore-leaks relationship dates 3.3M, NIH grants 2.1M,
ICE detainers 610k.

**Garbage year-zero dates:** two SEC fund tables whose newest "date" is year
0095/0099 — date parsing broken outright.

**Degenerate keys (≤1 distinct value):** 19 models whose best ID-shaped column
is a constant — 10 are aggregate tables whose only "ID" is the loader's run ID
(fine), but foreign-assistance's EIN column has exactly ONE distinct value
across 95k+ rows (a sentinel posing as a key — the NPPES pattern again).

**Sentinel-heavy keys (>1% masked):** 38 models, incl. 9.6M masked license
numbers in the provider registry and 334k literal-text VINs in vehicle
complaints.

**Stale tables (newest date before 2024):** the 990 e-file index stops
2020-01-28 (5.5M rows); Senate lobbying stops 2021 (the known 9% load);
OpenSanctions stops 2022-06; FAA registry's max date is 1970 (epoch);
judge financial-disclosure tables stop 2023-08 (likely source-side lag).

**The new court tables are join-ready internally:** docket IDs ~unique at 71.7M
rows, 7.8M distinct opinion clusters under 18.1M citations, 9.9M dockets
referenced by opinion clusters — high-cardinality real keys, still zero edges
to the entity map (registration remains the unlock).

## CourtListener key registration (2026-08-17, staged — the follow-on "just go")

The court tables' internal IDs are now **measured, wired, and staged** as two
new spine key axes — judge (person) and court (organization):

- **19 of 20 join surfaces verified at 99.2–100% referential match**
  (evidence: `courtlistener_edges.json`). Highlights: court → docket **100.0%
  on all 71.7M dockets**; judge → assigned docket 100.0% on 32.4M; judge →
  financial disclosure 99.8%; the whole disclosure money chain (1.9M investment
  lines) 99.4–99.6%.
- **One defect found and excluded:** the "appointing judge" column on
  judgeships matches the judge table only 47.2% — it references a different
  record type. Not wired; wiring it would manufacture false person entities.
- 16,057 distinct judges (394 alias rows — thin duplicates, zero false merges),
  3,361 named courts. 200 courts carry a Federal Judicial Center bridge ID —
  a future crosswalk out of the CourtListener namespace.
- **Why staged, not live:** flipping the new keys on changes the spine's config
  fingerprint, which (by design) freezes incremental spine updates until a
  FULL rebuild re-pins it — and the full rebuild is the parked ~$10–15
  decision. The wiring ships dark behind a single flag
  (`connect/keys.py: ENABLE_SPINE_BATCH_2026_08`); flip it in the same session
  that runs the full rebuild. Config verified both ways: flag off = fingerprint
  unchanged, flag on = specs/normalization/entity-typing all live.

**What goes live at that rebuild:** the judge dossier (career + education +
politics + disclosures + investments + caseload on one hard ID), court-grain
caseload ledgers over 71.7M dockets, and the judges-money-cases lane the
ladder ranked as the court domain's top unlock.

## The 2026-08 spine batch (staged with the court keys — "no bits and pieces")

Chris's call: batch everything that trips the same rebuild gate. A full column
sweep over all 2,216 live raw tables found every un-wired candidate; 41
candidates were then measured live (fill, distinct after the axis's own
normalization, overlap vs the live entity map / referential match vs the
family authority). Evidence: `spine_batch_verification.jsonl`.

**Staged — 39 new spec tables on existing axes + 3 new key families** (all
inside the same `ENABLE_SPINE_BATCH_2026_08` flag; full per-table numbers in
the spec file's comments):

- **Charity/tax axis:** the IRS exempt-org master file (1.98M charities,
  99.95% overlap — becomes the golden charity name source), the whole 527
  dark-money family (59k orgs, own money reports, directors, related
  entities), both failed-pension tables, pension actuarial filings, judges'
  schools.
- **Provider axis:** Medicare enrollment (2.5M providers, 100%), pharma-payment
  recipient profiles (1.7M, 100%), medical-equipment suppliers + referrers,
  community-health-center sites; hospital inpatient/outpatient price books on
  the facility axis.
- **Money axes:** NIH grants + small-business awards (first DUNS entities in
  the spine; each row also carries the modern UEI → old↔new federal-ID
  crosswalk for free), auditor-engagement issuer IDs (28.8k), fund registries,
  the listed-company ticker map, exchange-operator LEIs, UK-sanctioned hulls.
- **Environment:** the EPA facility registry itself (3.28M, 100%), air-program
  facilities, greenhouse-gas reporters, toxics reporters — plus the new
  **water-discharge permit family** (1.21M permitted facilities; violations,
  enforcement, inspections, quarterly noncompliance — 100.0% referential on
  all seven event tables).
- **New families:** credit unions (charter number: insured registry, call
  reports, merger ledger) and ICE detention facilities (2.6M stints, 100.0%
  to the 1,470-facility roster — detention outcomes by operator).

**Measured and REJECTED, on the record** (also in the spec file): the FCC
license EIN (fully masked, 0 of 1.69M), the FDIC bank LEI (empty), one dead
toxics FRS column, a 25-company SEC filings feed posing as a registry, three
retired-schema tables, one byte-identical twin load, and the in-house EPA
corporate crosswalk (98.6% unmatched/fuzzy name-matching — stays an overlay;
the spine is zero-false-merge). **Parked:** the legislator FEC-IDs column is
real but holds a JSON list per row — needs a tiny flatten build; still the
cheapest big politics unlock. The banking-ID family (FDIC certificate ↔ Fed
RSSD ↔ credit-union charter) parked as its own future axis study.

Also fixed in passing: the UK company-number key (wired 2026-08-05) never had
a collision-math entry — backfilled.

## Files

| file | what it holds |
|---|---|
| `fill_tables.csv` | one row per mart model: rows, bytes, dup ratio, date range, epoch/future counts, best key + fill/distinct/sentinels, provenance |
| `tier_a_tables.csv` | catalog metadata, all 4,276 tables across marts/raw/staging |
| `tier_a_columns.csv` | full column inventory (142k columns) — recovers the 12 models whose columns weren't reconstructable from SQL |
| `tier_b_new_scans.jsonl` | the 27 fresh scans, same schema as the 2026-08-11 scan |
| `staging_to_raw.csv` | staging model → raw landing table crosswalk with raw row counts |
