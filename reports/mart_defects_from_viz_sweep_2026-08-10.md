# Mart defects surfaced by the viz brainstorm sweep — 2026-08-10

> **SUPERSEDED 2026-08-10 (late).** Every claim below was a read of model
> code with nothing checked against live data, and a good share of it turned
> out to be wrong. The verified verdicts are in
> `mart_defect_verdicts_2026-08-10.md`. Read that instead; this file is kept
> only as the raw input it was.


Found by 18 readers going source-by-source through every modeled mart's SQL on
disk (no warehouse queries). Nothing here was confirmed against live data — each
item is a read of the model code and should be verified before acting.

## 1. Marts that expose almost none of their source's columns
- `fed_eoir_case_data` — 12.6M immigration-court rows, mart selects only `case_type`.
  Every judge/court/date/outcome field is stranded in raw. Highest-value fix on this list.
- `fed_fdic_enforcement` — only `raw_text` and `order_url`; no bank, date, or penalty.
- Four FEC marts (`FED_FEC_CANDIDATES`, `FED_FEC_COMMITTEES`, `FED_FEC_CAND_CMTE_LINKAGE`,
  `FED_FEC_PAC_SUMMARY`) — positional column names `c1..c15` / `c1..c27`, unusable as-is.
  The `fed_fec_bulk_*` marts are the readable versions.
- NHTSA duplicates: the `transport/` copies are `c1..c51`; the `consumer_safety/` copies
  are named. One pair should probably be dropped.
- `hrsa_uds` Table 3A — columns are unlabeled line numbers (`t3a_l1_ca` …), no docs.

## 2. Text columns cast to numbers (silently nulls them)
Recurring generated-model bug: `try_to_number` / `try_to_double` applied to name-like
text. Reported on `country` / `country_territory` / `country_of_birth` /
`country_of_citizenship` across the international, sanctions and immigration marts
(`intl_wb_ids`, `intl_eu_sanctions`, `intl_fatf_ratings`, `intl_adb_data`,
`intl_opensanctions`, `intl_gem_hazard`, `intl_global_witness_defenders`,
`intl_eg_capmas`, `intl_freedomhouse`, GDELT's four country codes, UCDP, IPC, GFI),
plus `violator_name` and dates in MSHA violations, `latest_action_text`
(`fed_govinfo_billstatus`), `legislative_action` (`st_cannabis_policy_bundles`),
`counties` (`fed_usgs_topoview`), `county_name`, `incorporation_state`,
`population_name`, `update_frequency`, and MPV / EDGAR county-and-state fields.
MSHA county FIPS cast to a number also strips leading zeros and breaks the labor join.

## 3. Suspected partial loads / page caps
- Exactly 500,000 rows: Google political ads geo + creative, IRS revocations, IRS Pub 78,
  CourtListener investments, and the dialysis-facility mart's own header comment
  (catalog says 12.4M).
- Exactly 10,000 rows: Treasury daily deposits.
- FEMA individual assistance — documented ~12% truncated load (reload in flight tonight).
- UK Companies House PSC — ~7.0M of ~10M, truncated, not a random sample.
- CAL-ACCESS lobbying firm/employer tables (170 / 524 / 577 rows) against 525k cover pages.
- Catalog row count vs mart comment disagree: CFPB complaints (34M vs 17M),
  SEC EDGAR financials (55,635 vs 6,699), MSHA accidents (273k vs 547k),
  MSHA violations (3.1M vs 6.2M), NOAA storm events (69.8k vs 1.78M).

## 4. Self-labelled samples still carrying a full-source name
HMDA LAR (DC-2023 slice), FDIC BankFind (10k), SEC insider (2025Q1 only),
FFIEC call reports (302 rows, plus a `doctype_html` column suggesting the scrape
captured page markup), DHS HIFLD (500 rows, one layer), EPA Envirofacts (5,000 rows,
blank facility ids), USAspending bulk (50k) and subawards (5k), NSF awards (125),
Grants.gov (100), bioRxiv (432), Ensembl (643), OSF registrations (10), FARA (30 vs 48k
in its bulk twin), FEC API (500), NASA open data (54), ADB (41), and the wave-2d portal marts.
`intl_es_datosgob` is self-labelled defective (blank title/description from a parse bug).
Health Canada drugs — the loader consumed the first data row as a header, so columns are
positionally renamed and one record is lost.

## 5. Grain traps to respect before counting anything
- Safe-drinking-water tables are quarterly snapshots keyed by submission quarter —
  counts inflate without dedup (the 15.4M-row violations table especially).
- EU sanctions is one row per name-or-address variant; UK sanctions is 57,883 variants
  over ~6,315 real designations.
- FDA adverse events spans two id eras (legacy vs modern case ids) with duplicated
  outcome columns; two of its tables are views with no row count.
- Federal judges is a wide 1..6 appointment layout; the unpivoted service table is the
  one to use. Same wide-column problem in the judicial-salary and revolving-door marts.
- CDC drug-poisoning county rate is banded into 11 text ranges — ordinal only.

## 6. Filing / naming problems
- Environmental marts filed under the immigration folder (drinking-water service areas,
  all four ICIS-FEC enforcement tables); CMS hospice + fee-for-service enrollment also
  under immigration; full ARCOS under uncategorized; CFTC trader commitments under education.
- SEC 13F: the singular-named mart selects the *positions* column list — looks like a
  copy/paste twin of the positions mart. Confirm which one is live.

## 7. Catalog-level shape (from the catalog's own fields)
- 558 modeled sources, ~1.28B mart rows total.
- 249 have a blank primary domain; 67 are explicitly unclassified.
- 139 have no last-ingested timestamp.
- 404 of 558 are federal — the library is heavily federal-skewed.
- Most common declared join key is NAME (158 sources), ahead of ZIP (81) and
  EIN / NPI (33 each). A large share of the spine leans on name matching.
