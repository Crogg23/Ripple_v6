# Warehouse state review — 2026-09-01

Door: Python scripts (connect/db.py). Chat plug-in door still 401.
Read-only queries on X-Small. Cost by query-log precedent: ~$0.
Scope: the warehouse itself — tables, wiring, mass. Code reviewed separately 2026-09-01.

Scratch scripts: session scratchpad `wh_recon_1..8`. Full gap list: scratchpad `hard_gap.json`, `gap_tables.json`.

---

## SKEPTIC PASS — the headline was wrong as first written

A fresh-context skeptic re-ran the checks. Its verdict, verified live:

- SPINE_KEYSET_LIVE is the DISPLAY_SPECS slice — 272 tables, exact set match.
  "Zero rows there" restates "not spec'd for display," not "never ingested."
- The discover keyset is KEYSET_LIVE (290.6M rows, live production, written
  2026-08-31 — incremental.py:73-74). 25 of the 633 "gap" tables ARE in it,
  covering 34.2M of the 62.8M rows (54%) — including OPINION_CLUSTERS (9.77M),
  USASPENDING_CONTRACTS (6.01M), FCC_LICENSING (1.54M).
- Value check (CLAUDE.md rule, skipped in the first pass): FCC_LICENSING's EIN
  column is 100% empty string (1 distinct value). SAM_EXCLUSIONS NPI: 33
  distinct in 10,000 rows. 13F CUSIPs are real — but POSITIONS and SUBMISSION
  have identical row and distinct counts, likely the same data twice.
- Backup/scratch mass is ~54.5 GB / 26.6%, not 57.6 GB — KEYSET_LIVE and
  MATCH_PAIRS are live, not scratch.
- Everything else held: 20,000,000 cap, ENTITY_MAP clean, 8 never-landed
  sources, AUDIT/BUILD frozen. ENTITY_INDEX dups are ALL n=2, all one FEC table.

Corrected residual: ~608 tables with name-detected hard keys, in neither
keyset, ~28.6M rows — and each needs a count-distinct value check before it
counts as real backlog. Section 1 below is the original, kept for the record;
read it through this lens.

---

## 1. The wiring gap — the watermark trap confirmed at scale

What was checked: every table in `CONNECT_WATERMARK` (2,132 distinct) joined
against per-table row counts in `SPINE_KEYSET_LIVE` (272 tables have rows).
For each zero-keyset table, connect's own `detect_key` + `TABLE_COLUMN_KEYS`
was run over its actual landing columns — the same code the pipeline runs.

- Watermark tables: 2,132
- Keyset-covered tables: 272
- Zero keyset, no detectable key — expected absence: 255
- Zero keyset, any detectable key: 1,683 (173.2M rows) — most are GEO/NAME only, which never enter the keyset by design
- **Zero keyset, HARD key (STEEL/STRONG/scoped): 633 tables, 62,841,041 rows**

A hit means: the table landed, the watermark recorded it, hard-ID columns exist,
and the identity layer has never ingested it. A miss (the 255) means the table
genuinely has nothing keyable — correct absence.

Top of the hard gap (full list in hard_gap.json):

| table | rows | hard keys |
|---|---|---|
| FED_USASPENDING_CONTRACTS_FULL | 20,000,000 | DUNS, UEI, NAICS |
| FED_COURTLISTENER_FJC_IDB_CL_LINKED | 10,323,280 | DOCKET |
| FED_COURTLISTENER_OPINION_CLUSTERS | 10,070,727 | DOCKET |
| FED_USASPENDING_CONTRACTS | 6,325,622 | DUNS, UEI, NAICS |
| FED_USASPENDING_SUBAWARDS_FULL | 4,742,460 | AWARD_KEY, DUNS, UEI |
| FED_SEC_13F_POSITIONS | 3,822,885 | CUSIP |
| FED_SEC_13F_SUBMISSION | 3,822,885 | CUSIP |
| FED_FCC_LICENSING | 1,689,338 | EIN |
| FED_SEC_FTD_CUSIP_BRIDGE | 128,303 | CUSIP |
| FED_FOREIGNASSISTANCE | 95,658 | EIN |
| FED_US_SEC_EDGAR | 48,990 | CIK, EIN, SIC |
| FED_DOL_FORM5500 | 33,484 | EIN |
| FED_SAM_EXCLUSIONS | 10,000 | NPI, UEI |
| XC_UK_SANCTIONS_LIST | 57,883 | IMO |

Caveat: "detectable" means the detector fires on the column name. Some of these
may be deliberate exclusions (bad ID quality in that source). But 633 tables of
deliberate exclusion with no written record is not plausible; most of this is
unwired backlog.

## 2. USASPENDING_CONTRACTS_FULL is a suspiciously round 20,000,000

What was checked: `count(*)` directly — exactly 20,000,000. That is a cap, not
a dataset size. `FED_USASPENDING_CONTRACTS_FULL_R2` holds 93,153,424 rows,
has a watermark row, and has 1,338,434 keyset rows — R2 is the wired, real one.
A hit here means the non-R2 FULL table is a truncated superseded load still
sitting in LANDING and still in the watermark. Candidate for RETIRED.
Same family, unclear status: FED_USASPENDING_ASSISTANCE_FULL (19,902,879 —
also close to a round cap; not verified either way).

## 3. Eight INCLUDE='Y' sources never landed

What was checked: registry `INCLUDE='Y'` (1,895 rows) vs distinct SOURCE_ID in
the watermark. 8 have no landing evidence at all:

- intl_opensanctions_default — OpenSanctions default collection
- fed_fec_bulk_contributions — FEC individual + committee contributions
- fed_house_clerk_ptr — STOCK Act periodic transaction reports
- fed_oge_disclosures — OGE Form 278e financial disclosures
- fed_house_disbursements — House statement of disbursements
- st_legiscan — LegiScan 50 states + Congress
- st_openstates — Open States legislators/bills/votes
- xc_cspan_congress — C-SPAN video/transcripts

For a money-and-politics platform, fec_bulk_contributions and the disclosure
sources being absent is the loudest single row in this review.

Registry hygiene note: INCLUDE is 'Y' (1,895), '' (752), NULL (125), 'N' (14).
752 empty-string + 125 NULL rows are neither included nor excluded — undecided
mass, three years of triage debt if left implicit.

## 4. Identity layer internals — clean where it matters

- ENTITY_MAP duplicate (KEY_TYPE, KEY_VALUE) groups: **0** — the map is one
  entity per key, as designed. The cross-key merge fix has nothing latent here.
- ENTITY_INDEX duplicate (SOURCE_TABLE, KEY_TYPE, KEY_VALUE) groups: 690, all
  n=2 in the sample, all FED_FEC_COMMITTEE_TO_CANDIDATE / FEC_CMTE_ID.
  Cosmetic double-entry in the browse index, not an identity error.
- Keyset tables that no longer exist in LANDING: 0. No ghosts.
- SPINE_KEYSET (92.6M, 2026-08-28) vs SPINE_KEYSET_LIVE (96.4M, 2026-08-31):
  the scratch twin is 3 days and ~3.8M rows behind live — consistent with the
  known validate() gap (scratch only written by the retired full rebuild).

## 5. Mass — 28% of the warehouse is backups and scratch

| bucket | GB | tables |
|---|---|---|
| LIBRARY_RAW total | 96.87 | 2,205 landing |
| LIBRARY_MARTS live | 53.15 − 9.18 restore | |
| LIBRARY_MARTS_PREDBT_20260729 (whole DB) | 34.39 | 318 |
| MARTS _RESTORE_20260701 / _RESTORE_20260731 | 9.18 | 40 |
| META CONNECT_BAK + CONNECT_PRESPINE (20260730) | 7.58 | 58 |
| CONNECT scratch (KEYSET_SCRATCH, KEYSET_LIVE, MATCH_PAIRS, GOLD_PAIRS, CROSSWALK_SCRATCH, SPINE_KEYSET) | 5.17 | 6 |
| RAW RETIRED schema | 1.26 | 4 |
| REGISTRY _BAK tables (7 copies of SOURCE_REGISTRY) | 0.01 | 8 |

~57.6 GB of ~205 GB total is backup/scratch/retired. Storage is cheap; the
navigation cost is not — 7 registry backups and 2 full pre-dbt copies is the
zip-drawer pattern. Dropping any of it is a destroy-gated decision, not done here.

Orphan tables in CONNECT with unclear status: KEYSET_LIVE (290.6M rows — 3× the
spine keyset, nothing in this review explains it), KEYSET_SCRATCH (181M),
MATCH_PAIRS (187M, last altered 2026-08-31 so still being written),
GOLD_PAIRS (6.5M, untouched since June).

## 6. Small stuff

- Zero-row landing tables: 3 — FED_COURTLISTENER_CITATION_MAP,
  FED_COURTLISTENER_JUDGE_RETENTION_EVENTS, FED_FDA_DEVICE_ENFORCEMENT__STAGING.
- 1,842 of 2,205 landing tables untouched 30+ days — mostly fine for static
  datasets; SOURCE_FRESHNESS exists but was last written 2026-07-12.
- AUDIT schema (COLUMN_HEALTH, TABLE_VITALS) frozen at 2026-07-28 — the audit
  layer stopped running five weeks ago.
- BUILD schema frozen mid-July — DEFECTS/PENDING_ACTIONS are stale state.

## 7. Pass 9 — the value check the skeptic demanded (2026-09-01, second run)

What was checked: all 608 residual tables — hard key by column name, in
NEITHER keyset. Every candidate key column (1,166 columns) measured live:
row count, nonblank count, approx distinct. The CLAUDE.md rule applied at scale.

- 546 tables pass mechanically (nonblank, >1 distinct, ≥50% fill): 8,423,560 rows
- 61 tables have blank or near-constant key columns — fake IDs by value
- BUT: most "passes" are NAICS codes and DOCKET_TYPE labels — classifications,
  not entity identities. NAICS distinct 15 on 8,402 rows is a category column.
- The real identity backlog after reading the values:

| what | rows | key | note |
|---|---|---|---|
| FED_SEC_13F_POSITIONS | 3,822,885 | CUSIP | real, 36,125 distinct, 100% fill |
| FED_SEC_13F_SUBMISSION | 3,822,885 | CUSIP | identical counts to POSITIONS — likely same data twice |
| FED_SEC_FTD_CUSIP_BRIDGE | 128,303 | CUSIP | real |
| FED_US_SEC_EDGAR | 48,990 | CIK | only 25 distinct CIKs — sample-sized |

So the "62.8M unwired" of the first pass collapses to: one CUSIP family,
~4M deduplicated rows, needing a CUSIP key type decision. Everything else is
either already in KEYSET_LIVE, a classification code, or a blank column.

Failed to measure: FED_USASPENDING_CONTRACTS_FULL's columns are lowercase
identifiers; quoted-uppercase probes erred. Moot — it is the truncated 20M
table superseded by R2, which is wired.

Receipts: scratchpad value_check.json, residual_verdict.json.

## 8. The FEC load that wasn't — two of the eight are registry doubles

What was checked: on "go" to land fed_fec_bulk_contributions, the landing
layer was searched by table pattern before building anything.

- FED_FEC_INDIV_CONTRIBUTIONS already holds 84,172,112 rows.
  Cycles 2023-2026 dense (18.1M / 40.1M / 21.0M / 5.0M), wired: 5.3M
  KEYSET_LIVE rows, 12,291 display keyset rows. Watermark source_id:
  fed_fec_indiv_contributions. The registry row fed_fec_bulk_contributions
  is a second row for the same dataset — INCLUDE='Y' on both.
- INTL_OPENSANCTIONS_DEFAULT already holds 1,281,846 rows. The registry row
  intl_opensanctions_default likewise never matched because the watermark
  credits a different source_id casing/name.
- A hit here means: "never landed" in section 3 was measured by
  registry-source_id vs watermark-source_id equality. Two rows failed that
  join for bookkeeping reasons, not missing data. The landing-name trap,
  registry-vs-registry edition.
- Date dirt noted in passing: 583 blank TRANSACTION_DT, stray years 3312,
  2036, 2029 — upstream FEC dirt, small counts.

Truly never landed, still six:

| source | note |
|---|---|
| fed_house_clerk_ptr | House STOCK Act PTRs; Senate side exists as FED_SENATE_STOCK_WATCHER |
| fed_oge_disclosures | OGE Form 278e |
| fed_house_disbursements | House spending on itself |
| st_legiscan | bills and votes, 50 states |
| st_openstates | legislators, 50 states |
| xc_cspan_congress | video transcripts |

Registry fix applied 2026-09-01, then corrected after a skeptic pass:

- fed_fec_bulk_contributions: INCLUDE='N', note says PARTIAL-DUPLICATE.
  Skeptic proved by transaction-type census: itcont landed (84.2M, 99.92%
  ENTITY_TP=IND), itpas2 partial (867K, cycles 2024+2026 only), **itoth —
  committee-to-committee, PAC-to-PAC transfers — landed NOWHERE**. No 16C/16F/
  18G/18J/24A/24E codes anywhere in the account. The row now points at that
  missing piece explicitly. itoth joins the truly-missing list: seven, not six.
- intl_opensanctions_default: my first write marked it duplicate OF ITSELF —
  its own landed table has 1,281,846 rows; intl_opensanctions (71K) is a
  different, narrower product. Reverted to INCLUDE='Y', original note restored
  verbatim. The review's "never landed" for this row was a watermark credit
  gap, not missing data.
- Mechanics verified by read-back both times; one row touched per UPDATE.

## 9. itoth landed — FED_FEC_COMMITTEE_TO_COMMITTEE, 2026-09-01

What was done: scripts/fec_itoth_load.py, a mirror of the itcont stream loader.
Smoke run first, then full load, atomic swap, never-shrink floor, one-member
zip rule. 28,558,310 rows, 0 quarantined, staging cleaned, INGEST_RUNS holds
labeled smoke + success rows. Skeptic verified every count to the row.

What the skeptic added, both loader fixes applied:

- 93% of the table is 15J earmark memos, MEMO_CD='X' — money already counted
  in itcont. The true PAC-to-PAC layer is ~1.9M non-15J rows: 24K 1,613,888,
  18K 103,896, 24E 71,619, 18G 44,016, 16C 8,533, more. Docstring now says so;
  trap saved to memory: filter MEMO_CD <> 'X' before any cross-table money sum.
- SUB_ID is a perfect natural key: 28,558,310 distinct, zero itcont overlap.
- The smoke cap overshot 2.5x — cap checked only per 500K chunk. Fixed: buffer
  trimmed to the exact cap before the write.
- Unproven by design: whether FEC's zips were fully streamed — zips are deleted
  post-run, so completeness rests on the never-shrink floor and future re-runs.
- Cost: ~21 minutes on X-Small, well under the itcont precedent of ~$1.70.

## 10. Open-list follow-ups, 2026-09-01 second sitting

- **13F twins resolved: same data twice.** Same 18 columns, same 3,822,885
  rows, same 9,716 ACCESSION_NUMBERs, same 3,822,885 INFOTABLE_SKs — full
  intersect both ways. Row hashes differ, so some value column drifted between
  the two loads, but the key coverage is identical. One table is redundant.
  Dropping either is destroy-gated — Chris's call which name survives.
- **AUDIT/BUILD frozen has a cause, not a fault.** No live code writes
  COLUMN_HEALTH / TABLE_VITALS / DEFECTS — their writers went into the junk
  drawer with the July-era audit workflow (LEDGER rows retired_2026-08-30).
  The tables are relics of a retired process, last written 2026-07-28.
  Options: drop the schemas (destroy-gated) or leave as inert history.
- **Registry limbo sized: 877 rows, only 18 ever landed.** By prefix:
  fed_* 293 (17 landed), other 258, intl_* 230 (1 landed), st_* 96.
  859 rows are pure wishlist — registered, never loaded, never decided.
  Proposed mechanical fix: stamp the 18 landed rows INCLUDE='Y' (convention:
  landed sources carry Y). BLOCKED by the auto-mode classifier — script staged
  at scratchpad limbo_stamp.py, needs a non-auto run.
- Committed: c19036ec — loader + this report. settings.json session cruft
  left uncommitted deliberately.

## Verdicts not reached

- Whether the 633-table hard gap is backlog or policy — needs the wiring
  decision log, which doesn't exist in the warehouse.
- ASSISTANCE_FULL truncation — not verified.
- KEYSET_LIVE's 290M rows — purpose unidentified from warehouse alone.
