# Row 1 — Expected-count manifest: loads vs publisher reality

Built 2026-08-30. Warehouse counts via Python-scripts door (read-only, `scripts/row1_expected_count_sweep.py` → `landing_counts.json`, `orphans.json`).
Publisher numbers from two web-research passes (URLs in the notes below).
Landing total: 2,220 base tables, 1,327,505,327 rows.

Verdicts: **BROKEN** = large confirmed shortfall vs publisher · **SLICE** = deliberate/undeclared partial (years or cycles missing) · **OK** = reconciles · **NO-PUBLISHER-COUNT** = publisher states no total; unverifiable cheaply.

| Source | Landed | Publisher | Verdict |
|---|---|---|---|
| FED_FDA_MAUDE_FULL | 13,042 | 25,711,469 device events (openFDA) | **BROKEN — 0.05%** |
| FED_SENATE_LDA_FILINGS | 831,376 (1999–2010 + 2020–21) | 28 years of filings | **BROKEN — 14 years missing** |
| FED_USASPENDING_SUBAWARDS_FULL | 4,742,460 (stops 2019-05) | series runs to present | **BROKEN — 7 years missing** |
| FED_USASPENDING_CONTRACTS_FULL | exactly 20,000,000 (confirmed by COUNT(*)) | registry note: "expect 100M+" | **BROKEN — truncated; superseded by R2** |
| FED_USASPENDING_ASSISTANCE_FULL | 19,902,879 — **every FY2007–2026 lands at exactly 1,000,000 rows** (only FY2014 under, 902,879) | log claims "FY2007-FY2026, all agencies" | **BROKEN — zip extractor keeps only the LARGEST member of each per-FY zip (`infra/ddl/08_bulk_ingest.sql:179`); publisher splits each FY at ~1M rows/file. Same proc + specs (`server_side_specs.py:558,608`) explain CONTRACTS_FULL's 20,000,000** |
| FED_CMS_OPEN_PAYMENTS (+_2022,_2023) | 43,392,397 (PY2022–24 only) | 93.97M all years (CMS, Jul 2026 — all payment types; landed tables may be general-payments-only, which would raise the real coverage) | **SLICE — ~46% of all-types universe; PY2013–21 + 2025 not landed** |
| FED_DEA_ARCOS_FULL | 178,598,026 (2006–2012 only; 0 null dates) | ~760M transactions 2006–2019 (WaPo figure, third-party; DEA publishes none) | **SLICE — 2013–2019 missing (histogram-proven); the 23% ratio is estimate-derived** |
| FED_FEC_INDIV_CONTRIBUTIONS | 84,172,112 (2023–2026 only; 583 null dates) | ~268.8M rows 2004–2026 (3rd-party load; FEC states none) | **SLICE — recent 2 cycles only** |
| FED_CFPB_HMDA_HISTORIC | 19,136,434 (2015–2017 only; 0 null years) | historic files cover 2007–2017; ~14–16M LAR/yr those years (approximate) | **SLICE — 3 of 11 years (proven). Per-year shortfall vs LAR is ~40–50% *if* the approx figures hold; could be a benign filtered subset — unresolved** |
| FED_CMS_PARTD_PRESCRIBER_DRUG | 25,869,521 | ingest-log URL = `MUP_DPR_RY24..._DY22_NPIBN.csv` — **data year 2022 only** (receipt: LIBRARY_META.INGEST_LOGS.INGEST_RUNS run 431c13fc) | **SLICE — 1 of 12 annual files (DY2022), confirmed by load metadata** |
| FED_FDA_FAERS_DEMO (report grain) | 5,811,086 | 32.8M reports (AEMS, Mar 2026) | **SLICE — 18% of reports landed** (DRUG 20.9M / REAC 20.6M / INDI 9.8M are multi-row grains; known non-contiguous quarters) |
| FED_NOAA_AIS | 58,106,517 | 30B+ positions (MarineCadastre) | **SLICE — 0.2%; declared tap, but registry said 3.7M** |
| FED_USASPENDING_CONTRACTS_FULL_R2 | 93,153,424 (COUNT(*) not yet run; info_schema) | none found on-site; checkpoint total_loaded matches exactly, months contiguous 2006-10→2026-08 | **NO-PUBLISHER-COUNT — internally consistent (loader agreeing with itself, not a publisher check; contiguous months ≠ complete months)** |
| FED_FEMA_IA_HOUSING_REGISTRATIONS | 26,250,920 = mart | — | **OK** (closed earlier) |
| FED_CMS_NPPES | 9,606,683 | ~9.40M NPIs (3rd-party file tracker, Aug 2026) | **OK — plausibly complete** |
| FED_CPSC_NEISS | 9,794,977 | ~400K/yr (CPSC) × 27 yrs ≈ 10.8M | **OK-ish** (2026 sentinel issue still open, row 16) |
| UK_COMPANIES_HOUSE_PSC | 15,804,612 | no CH count; snapshot size + register size match | **OK — plausibly complete** |
| FED_CFPB_COMPLAINTS | 17,179,788 (11,501 dup IDs, 0.07%) | landing page says "6.8M+ sent to companies" but 6.6M received in 2025 alone — publisher metrics inconsistent | **OK-ish — landed exceeds stale publisher headline; minor dups** |
| FED_COURTLISTENER_DOCKETS | 71,677,647 | "hundreds of millions of docket entries"; ~60M cases (2021) | **plausible; NO-PUBLISHER-COUNT** |
| FED_SEC_13F_HOLDINGS | 101,261,252 | none published (2013Q2+) | NO-PUBLISHER-COUNT |
| FED_EOIR_CASE_DATA | 12,631,225 | none published | NO-PUBLISHER-COUNT |
| INTL_ELECTIONS_CANADA_CONTRIBUTIONS | 12,646,465 | none published | NO-PUBLISHER-COUNT |
| FED_FJC_IDB_* (civil/crim/bankr/appellate) | 25.1M total | none published | NO-PUBLISHER-COUNT |
| FED_EPA_SDWA / CAMPD / USGS NWIS / FRACFOCUS / MDS | — | none published (FracFocus counter is JS-only) | NO-PUBLISHER-COUNT |

## Orphan populations (skeptic's open item)

- 771 registry rows with no landing table; **16 INCLUDE=true** (a first pass said 23 — that was a
  truthiness bug on the 'Y'/'N' flag, caught by skeptic; script fixed, 16 confirmed on rerun).
- Registry-side orphans are mostly **naming mismatches, not missing loads** — data landed under a
  different name than UPPER(SOURCE_ID) (`corporate_registry_uk_companies_house_psc` →
  `UK_COMPANIES_HOUSE_PSC`, `fed_fjc_idb` → 4 `FED_FJC_IDB_*` tables, `fed_dea_arcos` →
  `FED_DEA_ARCOS_FULL`). Full registry dump persisted at `reports/row1/registry_dump.json` so the
  match is reproducible.
- Genuinely registered-but-never-landed (INCLUDE=true): `st_legiscan`, `st_openstates`,
  `xc_cspan_congress`, `fed_house_clerk_ptr`, `fed_oge_disclosures`, `fed_house_disbursements`.
  (`gap_*` buckets and `fed_cms_open_payments_gnrl` are INCLUDE=N; `fed_efta_statute` is
  vault-only by design.)
- **Landing-side is NOT resolved by renaming: ≥10 large tables look genuinely unregistered** —
  no candidate registry row at all, including `FED_FEMA_IA_HOUSING_REGISTRATIONS` (26.3M),
  `FED_CFPB_HMDA_HISTORIC` (19.1M — the flagship nationwide table, unregistered),
  `FED_EPA_CAMPD_EMISSIONS_DAILY`, `INTL_ELECTIONS_CANADA_CONTRIBUTIONS`, `FED_FRACFOCUS_REGISTRY`,
  `FED_FMCSA_COMPANY_CENSUS`, `FED_EPA_FRS_FRS_FACILITIES`, `FED_CMS_PECOS_PROVIDER_ENROLLMENT`,
  `FED_FDIC_SOD_BRANCH_DEPOSITS`, ICIJ copies. Registration work for Chris to scope.
- Dup registry match: `FED_FEC_INDEPENDENT_EXPENDITURES` matches 2 registry rows.

## New duplicate family + round-number theme

- **EPA RCRA tables are doubled — 5 pairs**: `FED_EPA_RCRA_RCRA_*` vs `FED_EPA_RCRA_*` for
  FACILITIES / EVALUATIONS / VIOLATIONS / VIOSNC_HISTORY / ENFORCEMENTS, identical row counts
  (metadata-level; content not diffed). Same disease as the ICIJ triplicate. Chris's canonical-name call.
- **399 tables have counts that are exact multiples of 1,000** (e.g. `FED_USASPENDING_BULK` 50,000,
  `FED_CDC_DATA_PORTAL` 15,000, a `PORTAL_CKA_*` family at exactly 10,000) — the 20,000,000 disease
  is a population, not one table. Not triaged this session.
- 3 zero-row landing tables: `FED_COURTLISTENER_CITATION_MAP`, `FED_COURTLISTENER_JUDGE_RETENTION_EVENTS`,
  `FED_FDA_DEVICE_ENFORCEMENT__STAGING`.

## Second-pass results (2026-08-31 "go" session)

- **ASSISTANCE_FULL: truncation mechanism found — and it's not a row cap.** A first write-up said
  "1M cap in the loader"; the skeptic pass found the real code: `RIPPLE_UNZIP_MEMBER_TO_STAGE`
  extracts **only the largest CSV member of each zip** (`infra/ddl/08_bulk_ingest.sql:179`), and
  USAspending splits each FY's CSV into ~1M-row parts. FY2014's 902,879 (a cap can't leak; a file
  slice varies) confirms the file-slice story. `scripts/usaspending_contracts_full_load.py:3-9`
  already documented the symptom. CONTRACTS_FULL and ASSISTANCE_FULL use the same proc + spec shape
  (`scripts/server_side_specs.py:558,608` — verified, not inferred). R2's month-chunked loader is a
  different path, unaffected.
- ⚠ **Blast radius: 18 of 27 specs in `server_side_specs.py` are `kind: zip`** and go through the
  largest-member extractor — any of them whose zip holds multiple members is silently truncated the
  same way. Only the two USAspending tables were checked. `.snowflake/cortex/plans/acquire-all-gap-data.plan.md:42`
  already proposes "extract all zip members" as a loader upgrade.
- **Part D confirmed DY2022-only** via ingest-log source URL (see table).
- **MDS Frequency = single quarterly snapshot** (all 31.4M rows REPORT_DATE "Q2, 2026", zero NULLs).
- **Round-number screen: no additional suspects** — of the 399 multiples-of-1,000, only 2 are ≥100K
  (portal filter turned out irrelevant): CONTRACTS_FULL (explained) and `FED_CDC_INJURY_VIOLENCE_COUNTY`
  (132,000, untriaged). ⚠ But this screen **cannot detect member-slice truncation** — ASSISTANCE_FULL's
  19,902,879 is invisible to it. It's a lower bound, not a clearance.
- Receipts for all of the above: `scripts/row1_second_pass_receipts.py` →
  `reports/row1/second_pass_receipts.json` (FY histogram, MDS histogram incl. NULLs, dialysis
  COUNT(*), Part D ingest-log row).

## CourtListener + extras (research pass, 2026-08-31)

- **CourtListener publishes no per-table counts** — bulk page has no numbers, v4 API count feature
  needs an auth token (anonymous = 401). A free account token would unlock exact live counts —
  cheapest future check.
- Suggestive: a third-party blog cites 18,123,971 citations; landed `FED_COURTLISTENER_CITATIONS` =
  18,123,788 (off by 183 — looks like the same snapshot). Unofficial, not a verdict.
- **`FED_CMS_MEDICARE_DIALYSIS_FACILITIES`: EXACT MATCH** — CMS's stats API (dataset
  f8610e87-ba25-43a3-a49e-927dbc8701ae) total_rows = 12,456,456 = landed COUNT(*) 12,456,456.
  **OK — count matches the publisher exactly.** Caveat: grain is facility-per-measure/period, not a
  facility list (~7.7K facilities exist; sibling `FED_CMS_DIALYSIS` holds 7,557).
- GUDID: AccessGUDID publishes 5,182,695 *device identifier records* (Aug 2026); landed
  `FED_FDA_GUDID_FULL_IDENTIFIERS` = 6,767,219 — different grain (identifiers table holds multiple
  IDs per device), not apples-to-apples. GUDID stays best-instrumented via its own checkpoint+sha256.

## Zip-spec sweep (the 18 `kind: zip` sources, 2026-08-31 — rewritten after skeptic pass)

Method: ingest-log rows + landing counts per spec. Read-only. Zips not opened.
Receipts: `scripts/row1_second_pass_receipts.py` → `second_pass_receipts.json`
(zip_spec_ingest_runs, zip_spec_landing_counts, shrunk_tables_count_star).

| Spec | State | Verdict |
|---|---|---|
| USASPENDING_CONTRACTS_FULL / ASSISTANCE_FULL | landed | **BROKEN — extractor truncation, proven** |
| FEC ×4 (masters) | 27K–60K | **SLICE — spec manifest lists only 2018/2020/2022/2024 cycles** (`server_side_specs.py:658+`); FEC publishes back to 1980 |
| NHTSA_RECALLS | 241,861 | **SLICE — URL is `FLAT_RCL_POST_2010.zip`** (`server_side_specs.py:205`); full file runs from 1966 |
| SEC_INSIDER | 4 per-member tables | **partial — 4 of SEC's ~8 members** (holdings, footnotes, signatures never extracted) **and manifest ends 2025Q1** — 5 quarters stale |
| CFPB_COMPLAINTS | 17.2M | no extractor-truncation signature |
| INTL_GLEIF | 3.38M | no signature — ≈ LEI universe size |
| MSHA ×3 | 3.09M / 274K / 92K | no signature — but `\.txt$` also matches the definition-file member; saved by size coincidence, not by design |
| NHTSA_COMPLAINTS / INVESTIGATIONS | 2.23M / 154K | no signature |
| OSHA zip specs | never ran | **inspections landed via data.dol.gov loader (dup-ridden, row 13); violations + accidents landed NOWHERE** |
| DOL_WHD_WHISARD | no LANDING table | **absent from LANDING — a repeatedly-FAILED fetch, not untried** (4 URL attempts across `tier1_bulk_batch_load.py`, `tier1_bulk_retry.py`, `tier1_bulk_retry2.py`, `_diagnose_fails2.py`) |

Method blind spots (named, per skeptic):
- Counts cannot see member loss; only opening zips (or logging `chosen_member`, which the proc already returns) proves single-member.
- `member_pattern` is not a guard: multiple matches → largest silently wins; zero matches → silent fallback to ALL members.

Shrunk tables — cause narrowed:
- FEC_CANDIDATES 27,095 vs 33,506 logged; FEC_COMMITTEES 60,031 vs 78,039; NHTSA_RECALLS 241,861 vs 242,993.
- Each has exactly ONE ingest run — so no re-run explains it. **Rows were removed after the only load.** Dedupe or manual delete; still untriaged.

## Row 16 — checkpoint-only recent loads (2026-08-31, rewritten after skeptic)

| Load | Checkpoint vs landing | Coverage finding |
|---|---|---|
| SEC 13F | exact — 101,261,252 both | **46 of 53 published zips.** Missing: 2021q3–q4, 2022q4–2023q4, Jun–Aug 2026. Run log says "53 zips, 49 to load"; killed mid-run |
| SEC 13F error log | warnings only | defused — pandas index noise |
| CAMPD daily | exact — 16,513,971 both | ⚠ **2015–2025 only. 1995–2014 never attempted.** Facility sibling proves EPA publishes to 1995. Missing chunks include MT + SD 2024 |
| CAMPD facility | exact — 128,525 both | 1995–2025 complete |
| NEISS | sums exact | 1999–2025 present; 2026 absent; 2025 = series high, worth a glance |
| FAERS | **4 of 5 tables EXCEED checkpoint** | non-contiguous CONFIRMED: 2014q1, q3, q4 missing. Surplus ~900K DRUG rows unexplained — dup loads or off-checkpoint partial |

Method lessons the skeptic forced in:
- Checkpoint-sum = landing proves nothing about never-attempted files. Both sides are zero.
- FDA_DT is receipt date. It smears quarter boundaries. Reconcile by run ID, not event date.

Receipts: `second_pass_receipts.json` row16 keys via `scripts/row1_second_pass_receipts.py`.

## Still not checked

`FED_USASPENDING_CONTRACTS` (6.3M — a third contracts copy alongside _FULL and _FULL_R2);
CourtListener exact counts (needs a free API token).

## Receipts

- `reports/row1/landing_counts.json` — all 2,220 tables with counts.
- `reports/row1/orphans.json` — both orphan populations, INCLUDE=true flagged.
- Histograms run 2026-08-30 (session transcripts): HMDA AS_OF_YEAR, ARCOS TRANSACTION_DATE year,
  FEC TRANSACTION_DT year, Open Payments PROGRAM_YEAR, CFPB distinct Complaint ID, Part D run IDs.
- Publisher URLs: openFDA (MAUDE), CMS Open Payments Jul-2026 publication, WaPo ARCOS 2023,
  MarineCadastre AIS hub, AEMS/FAERS PubMed 42078215, CFPB complaints landing + 2025 annual report,
  CFPB HMDA historic page, npipublicdata.org (NPPES), CPSC NEISS overview, fec.gov bulk data.
