# Library Entity-Resolution Spine — Join-Integrity & Data-Quality Audit

**2026-07-28. Report-only.** All numbers below came from live `SELECT`-only queries against the warehouse this session (no writes, no schema changes, no repo edits), except Section 3 which is a local join between `reports/table_inventory.md` and verified dbt `source()`/`ref()` lineage (also no live queries needed). Every ratio/pct is computed from an actual `COUNT(*)` this session, not cached `INFORMATION_SCHEMA` metadata.

---

## 1. Entity Spine Health

### 1a. Required-key null/empty rate per table

| Table | Total Rows | Bad Required-Key Rows | Bad % | Why it matters |
|---|---:|---:|---:|---|
| CONNECT_EDGES | 11,206 | 0 | 0.0% | clean |
| ENTITY_MAP | 16,410,088 | 0 | 0.0% | clean |
| ENTITY_INDEX | 23,031,110 | 0 | 0.0% | clean |
| ENTITY_GOLDEN | 16,410,088 | 0 | 0.0% | clean |
| MATCH_PAIRS | 16,198,711 | 0 | 0.0% | clean |

No table has a null/empty ENTITY_ID, KEY_TYPE, KEY_VALUE, TABLE_A/B, or A/B/KEY. Two secondary (non-required) attribute gaps worth flagging separately:

| Table.Column | Total | Null/Empty | % | Why it matters |
|---|---:|---:|---:|---|
| CONNECT_EDGES.A_COL / B_COL | 11,206 | 272 | 2.4% | these edges predate the 2026-07-02 A_COL/B_COL addition (known legacy gap per `store.py`) — can't be turned into a real SQL join |
| ENTITY_GOLDEN.CANONICAL_NAME | 16,410,088 | 347,493 | 2.1% | entity has no name from any source (falls back to bare key value in dossiers) |

### 1b. Orphan / referential-integrity checks (sorted worst first)

| Check | Total | Orphan Rows | Orphan % | Why it matters |
|---|---:|---:|---:|---|
| CONNECT_EDGES: A or B table never entity-indexed | 11,206 | 11,004 | **98.2%** | **the loudest finding in this audit.** Almost the entire connection graph references tables ENTITY_INDEX has never seen — the edge-discovery universe and the entity-indexing universe are out of sync. |
| CONNECT_EDGES: B table never entity-indexed | 11,206 | 10,890 | 97.2% | see above, B-side alone |
| CONNECT_EDGES: A table never entity-indexed | 11,206 | 9,064 | 80.9% | see above, A-side alone |
| CONNECT_EDGES: A or B table dropped/renamed from LIBRARY_RAW.LANDING | 11,206 | 9 (each side) | 0.1% | negligible — the 98.2% above is NOT dead tables, the tables still physically exist |
| ENTITY_INDEX rows with no matching ENTITY_MAP row | 23,031,110 | 0 | 0.0% | clean FK |
| ENTITY_GOLDEN rows with no matching ENTITY_MAP row | 16,410,088 | 0 | 0.0% | clean FK |

Note on methodology: `CONNECT_EDGES.A`/`.B` are landing **table names**, not entity IDs — there is no entity-ID column on that table, so "orphaned edges vs. entity ID" doesn't literally apply to this schema. The checks above are the closest real analogs (table-reference orphaning against the entity layer, and against physical existence).

### 1c. Entity-ID hash-collision sanity (ENTITY_MAP)

| Total Rows | Distinct ENTITY_ID | Distinct (KEY_TYPE\|KEY_VALUE) | Collisions |
|---:|---:|---:|---:|
| 16,410,088 | 16,410,088 | 16,410,088 | **0** |

Clean — confirmed independently by both the Section 1 and Section 4 agents.

### 1d. Unmatched rate (source rows never matched into an entity)

**Overall, across all 34 DISPLAY_SPECS source tables: 275,206,812 / 309,192,210 rows matched → 10.99% unmatched.** This number is driven almost entirely by 4 tables (see Section 2 for the per-table breakdown) — most tables individually sit at 0.0–0.4% unmatched.

### 1e. Freshness / run-id consistency

| Table | Max BUILT_AT | Distinct RUN_IDs | Note |
|---|---|---:|---|
| ENTITY_MAP | 2026-07-27 09:47:41 | 1 | same pipeline run |
| CONNECT_NODES | 2026-07-27 09:47:24 | 1 | same pipeline run |
| MATCH_PAIRS | 2026-07-27 09:47:32 | 1 | same pipeline run |
| ENTITY_GOLDEN | 2026-07-27 09:48:00 | 1 | same pipeline run — all 4 built in one ~36-second window |
| CONNECT_EDGES | **NULL** | 1 | BUILT_AT is null on every row despite a stamped RUN_ID — metadata gap |
| ENTITY_INDEX | n/a | n/a | table has no BUILT_AT/RUN_ID column at all — freshness can't be checked this way |

---

## 2. Key Coverage Per Source Table

Every (table, key) pair in `connect/entity_index_specs.py`'s `DISPLAY_SPECS` — the codebase's own canonical list of tables feeding the connection engine. Sorted worst first. **4 of 36 pairs are below the 90% flag threshold:**

| Table | Key | Key Column | Total Rows | Usable Rows | Usable % | Flag |
|---|---|---|---:|---:|---:|---|
| FED_HHS_OIG_LEIE | NPI | NPI | 83,464 | 8,684 | **10.4%** | 🔴 the federal exclusions list — 89.6% can't be joined to a provider by NPI at all |
| FED_OFAC_SDN | IMO | IMO | 19,115 | 2,032 | **10.6%** | 🔴 expected-ish: most sanctioned *entities* aren't ships, so most rows have no IMO by design — still worth a real denominator check |
| FED_SAM_EXCLUSIONS | UEI | UEI | 9,000 | 3,208 | **35.6%** | 🔴 federal debarment list — most rows can't be joined by UEI |
| FED_NOAA_AIS | IMO | IMO | 58,106,517 | 24,362,209 | **41.9%** | 🔴 58% of vessel-position pings have no usable IMO (smaller craft don't broadcast one — plausible, still flagged) |
| FED_VOTEVIEW_MEMBERS | BIOGUIDE | BIOGUIDE_ID | 51,061 | 50,993 | 99.9% | — |
| FED_CONGRESS_LEGISLATORS | BIOGUIDE | BIOGUIDE | 12,847 | 12,834 | 99.9% | — |
| FED_CMS_OPEN_PAYMENTS_2022 | NPI | NPI | 13,250,000 | 13,198,870 | 99.6% | — |
| FED_CMS_OPEN_PAYMENTS | NPI | NPI | 15,385,047 | 15,336,988 | 99.7% | — |
| FED_CMS_OPEN_PAYMENTS_2023 | NPI | NPI | 14,700,786 | 14,656,553 | 99.7% | — |
| *(all remaining 27 pairs)* | — | — | — | — | **100.0%** | — |

Remaining 100.0% tables (for the record): FED_CMS_NPPES, FED_CMS_FACILITY_AFFILIATION, FED_CMS_HOSPITAL_GENERAL, FED_CMS_HOSPICE, FED_CMS_HOME_HEALTH, FED_CMS_IRF, FED_CMS_LTCH, FED_CMS_DIALYSIS, FED_CMS_POS_OTHER, FED_NURSINGHOME411, FED_CMS_MEDICARE_PROVIDER, FED_CMS_PART_D_PRESCRIBERS, FED_IRS_BMF, FED_IRS_990, FED_DOL_FORM5500, FED_IRS_REVOCATION, INTL_GLEIF, FED_CFPB_HMDA, FED_VOTEVIEW_ROLLCALLS, FED_SEC_EDGAR_FINANCIALS, FED_SEC_13F_SUBMISSIONS, FED_USASPENDING_CONTRACTS, FED_SEC_EDGAR_COMPANY_TICKERS, FED_DEA_ARCOS_FULL (both REPORTER_DEA_NO and BUYER_DEA_NO), FED_CONGRESS_COMMITTEE_MEMBERSHIP, FED_VOTEVIEW_MEMBERS (ICPSR).

**Critical caveat surfaced in Section 5 and worth repeating here:** this check used `COUNT(normalized_key)`, which correctly nulls out zero-filled placeholders per `connect/keys.py`'s `NORM_RULES` — but a *raw*, naive `COUNT(col)` on NPPES's `EIN` column would have shown 100% populated while the real usable rate is ~0% (see Section 5). The 4 flagged rows above are real; don't assume anything showing 100% here is safe from a similar sentinel-masking trap on non-DISPLAY_SPECS columns.

---

## 3. Mart vs. Raw Row Parity (dbt-lineage-verified, not name-guessed)

Methodology note: an initial pass matched mart names to raw tables by string-guessing (`SCHEMA__RAW_NAME` → strip prefix) and produced 2 absurd false positives (a mart showing "43,666,999% of raw" and one at "500,000%"). Both were guessing the wrong raw table. This table instead traces every mart's actual `{{ source() }}` / `{{ ref() }}` calls in its dbt SQL (one hop through staging models) to find the **true** raw source(s) — 96 mart files resolved, 90 to raw table(s), 6 to other marts (excluded, not raw-comparable). Backup/restore-schema shadow copies (`_RESTORE_20260701`, `RETIRED`) excluded from raw lookups since they're already known-stale snapshots.

**13 marts flagged (ratio < 50% or > 150% of their true raw source), sorted worst first:**

| Mart | Mart Rows | True Raw Source | Raw Rows | Ratio | Why it matters |
|---|---:|---|---:|---:|---|
| CONSUMER_PROTECTION__FED_CFPB_COMPLAINTS | 500 | FED_CFPB_COMPLAINTS | 17,179,788 | **0.0%** | mart last built 06-20/07-12, a month before the real 17.2M-row load landed 07-23 — biggest gap in the warehouse |
| REF__DIM_GEOGRAPHY | 7,429 | FED_EPA_FRS_FULL | 5,300,149 | **0.1%** | this is a legitimate dimension-rollup (distinct FIPS/geo), so low ratio is *expected* for a dim table — flagging for eyes-on confirmation, not as a clear defect like the others |
| MONEY__DEBT_REPAYMENT_CLIFF | 938 | INTL_WB_IDS | 62,983 | 1.5% | check whether this is an intentional filtered view (e.g. a specific country/debt-cliff cohort) or a broken join |
| POLITICS__MEMBER_VOTING_RECORD | 1,105 | FED_VOTEVIEW_MEMBERS | 51,061 | 2.2% | only ~1,105 of 51,061 member-records have a voting-record row — looks like a broken join, not a rollup |
| FOREIGN_INFLUENCE__FED_FARA_BULK | 21,326 | FED_FARA_BULK | 221,900 | 9.6% | 90% of foreign-agent registrations missing from the mart |
| HOUSING__FED_MAPPING_INEQUALITY | 1,155 | FED_MAPPING_INEQUALITY | 10,154 | 11.4% | |
| MARITIME__FED_NOAA_AIS | 7,296,017 | FED_NOAA_AIS | 58,106,517 | 12.6% | mart likely pre-filters to a subset (e.g. one time window) of AIS pings — confirm intent |
| CONSUMER_SAFETY__FED_NHTSA_INVESTIGATIONS | 30,748 | FED_NHTSA_INVESTIGATIONS | 154,209 | 19.9% | ~80% of rows dropped between raw and mart — matches the prior table-inventory audit's flag, still unresolved |
| POLITICS__MEMBER_SPINE | 12,794 | FED_VOTEVIEW_MEMBERS | 51,061 | 25.1% | member spine only covers ~1 in 4 raw member-records |
| ECONOMICS__INTL_IT_ISTAT | 56,096 | INTL_IT_ISTAT | 213,284 | 26.3% | |
| ENERGY__INTL_EMBER_ELEC | 118,463 | INTL_EMBER_ELEC | 369,264 | 32.1% | |
| POLITICS__FED_FEC_PAC_SUMMARY | 22,899 | FED_FEC_PAC_SUMMARY | 48,395 | 47.3% | just under the 50% line |
| HEALTH__FED_FDA_DRUG_ENFORCEMENT | 5,000 | FED_FDA_DRUG_ENFORCEMENT | 1 | 500,000% | **not a real defect** — the raw landing table is 1 row containing an unflattened JSON blob (6.3MB); the mart's staging model correctly flattens it into 5,000 real recall records. Row-count parity math doesn't apply to unflattened-JSON raw landings. Flagging so the number doesn't get miscopied elsewhere without this context. |

**83 marts (of 96 checked) are within normal parity** — including `HEALTH__FED_DEA_ARCOS` (178,598,026 / 178,598,026 = 100.0%, confirmed via lineage after correcting the earlier name-guess false positive) and 3 legitimate multi-source join/aggregate marts (`JUSTICE__COUNTY_DOUBLE_BURDEN`, `POLITICS__BILLS`, `LEAD_QUEUE`) whose low ratio-vs-sum is expected for an aggregation and not comparable to a 1:1 check.

---

## 4. Duplicate / Conflict Detection

### 4a. Duplicate key values within the 8 largest entity-bearing raw tables

| Table | Key Col (type) | Total Rows | Keyed Rows | Rows in Dup Groups | Dup % of Keyed | Grain | Real defect signal? |
|---|---|---:|---:|---:|---:|---|---|
| FED_CMS_NPPES | NPI (NPI) | 9,606,683 | 9,606,683 | 0 | **0.00%** | registry (should be ~1/NPI) | ✅ clean — no defect |
| INTL_GLEIF | LEI (LEI) | 3,382,301 | 3,382,301 | 0 | **0.00%** | registry (should be ~1/LEI) | ✅ clean — no defect |
| FED_DEA_ARCOS_FULL | REPORTER_DEA_NO (DEA_NO) | 178,598,026 | 178,598,026 | 178,597,991 | 100.00% | transaction | normal — many transactions per distributor |
| FED_NOAA_AIS | IMO (IMO) | 58,106,517 | 24,362,209 | 24,362,145 | 100.00% | broadcast ping | normal — many pings per vessel |
| FED_CMS_OPEN_PAYMENTS_2023 | NPI (NPI) | 14,700,786 | 14,656,553 | 14,406,879 | 98.30% | payment record | normal — many payments per provider |
| FED_CMS_OPEN_PAYMENTS | NPI (NPI) | 15,385,047 | 15,336,988 | 15,073,815 | 98.28% | payment record | normal |
| FED_CMS_OPEN_PAYMENTS_2022 | NPI (NPI) | 13,250,000 | 13,198,870 | 12,962,770 | 98.21% | payment record | normal |
| FED_USASPENDING_CONTRACTS | RECIPIENT_UEI (UEI) | 6,325,622 | 6,325,622 | 6,297,177 | 99.55% | award transaction | normal — many awards per recipient |
| FED_DEA_ARCOS_FULL | BUYER_DEA_NO (DEA_NO) | 178,598,026 | 178,598,026 | 178,584,241 | 99.99% | transaction | normal — many transactions per buyer |

Only the two **registry-grain** tables (NPPES, GLEIF) are meaningful for "duplicate entity" purposes — both are clean. The other 7 rows show 98–100% "duplication" by design (transaction/ping/payment logs where many legitimate rows share one entity key) — not a data-quality defect, included per spec but don't read the high percentages as broken.

### 4b. ENTITY_GOLDEN — contradictory attributes across sources

| Check | Result | Why it matters |
|---|---:|---|
| Hash-collision (distinct ENTITY_ID vs distinct KEY_TYPE\|KEY_VALUE, both on 16,410,088 rows) | **0 collisions** | confirms content-addressing works — one ENTITY_ID literally cannot hold two different key values by construction, so a classic "two EINs on one entity" check doesn't apply to this schema |
| Multi-source entities with a non-null place string | 2,296,220 | denominator for the row below |
| Entities where sources disagree on place string | 2,219,249 → **96.65%** | 🔴 flagged, but likely a string-normalization artifact (e.g. "123 Main St, Springfield, IL" vs "123 MAIN STREET SPRINGFIELD IL" counted as different places), not necessarily 96.65% of entities truly operating from different addresses — needs the normalization checked before treating this as a geography-mismatch finding |

---

## 5. Null Rate on Critical Columns — Top 20 Marts

Sorted by severity, worst first. "Critical column" = a join key or the mart's primary metric, chosen per-mart by reading the dbt model SQL.

| Mart | Column | Role | Null/Unusable % | Why it matters |
|---|---|---|---:|---|
| HEALTH__FED_CMS_NPPES | EIN | join key | **~100%** (raw COUNT() falsely shows 0%) | 🔴 **worst finding in this section.** `COUNT()` says fully populated; `COUNT(DISTINCT)` reveals only 2 values exist — empty string (79.8%) and the literal sentinel text `<UNAVAIL>` (20.2%). Effectively zero real EINs. Any join/spine logic bridging NPPES→EIN silently matches nothing. |
| CORPORATE_REGISTRY__INTL_UK_COMPANIES_HOUSE | dissolution_date | core metric | 100.0% | field never populates across all 5,734,780 rows — any "dissolved but still operating" story is currently unbuildable on this column |
| ECONOMICS__INTL_GLEIF_RR | period_start_date | primary date | 100.0% | `try_to_date(...,'YYYY-MM-DD')` parse is broken or source is empty for all 391,664 rows — easy green-lane fix, check the raw format |
| ENVIRONMENT__FED_EPA_ECHO | penalty_count | primary metric | 99.3% | `total_penalties` is 100% populated but the count behind it is nearly all null — looks like a zero-fill artifact; any "who's fined most" ranking must filter on count, not just non-null dollars |
| MARITIME__FED_NOAA_AIS | imo_number | join key | **~56.2%** (raw COUNT() falsely shows 0%) | blank-string (30.8%) + zero/placeholder (25.5%) masked by raw COUNT(). `mmsi` is the reliable vessel key here, not imo_number |
| ECONOMICS__FED_IRS_REVOCATION | reinstatement_date | core metric | **unmeasured** (raw COUNT() shows 0%, but the model's own SQL treats it as empty-string, not NULL) | flagging the measurement gap rather than a false clean number — real fill rate needs `TRIM(...) != ''`, not attempted this pass |
| ECONOMICS__FED_IRS_BMF | revenue_amt | primary metric | 29.1% | expected — many smaller exempt orgs don't file full financials |
| ECONOMICS__FED_IRS_BMF | asset_amt / income_amt | primary metric | 22.7% each | same as above |
| FINANCE__FED_SEC_INSIDER_NONDERIV_TRANS | transaction_value / price_per_share | primary metric | 6.7% (in lockstep) | real gap, not a load error — likely gifts/non-cash transfers with no reported price; exclude from dollar-volume aggregates |
| LABOR__FED_MSHA_VIOLATIONS | proposed_penalty | primary metric | 2.2% | plausibly legitimate (some violation types carry no fine) — spot-check against `section_of_act` |
| LABOR__FED_MSHA_ACCIDENTS | operator_id | join key | 0.3% | small, won't block joins |
| HEALTH__FED_DEA_ARCOS | total_mme | primary metric | 0.2% | clean |
| CONSUMER_SAFETY__FED_CPSC_NEISS / FINANCE__FED_FEC_INDIV_CONTRIBUTIONS / FINANCE__FED_SEC_INSIDER_SUBMISSION / FINANCE__FED_SEC_INSIDER_REPORTINGOWNER / POLITICS__VOTEVIEW_VOTES / POLITICS__BILL_COSPONSORS / ENVIRONMENT__FED_EPA_FRS_FACILITIES | all checked join keys and metrics | 0.0% | clean across the board |

**Separate schema/lineage finding (not a null-rate number):** `CORPORATE_REGISTRY__INTL_IE_CRO`'s live table (in schema `DBT_CROGERS`) has a **completely different column set** than its own dbt model file defines (`COMPANY_NUM`/`COMPANY_STATUS_CODE`/... vs. the model's `company_id`/`company_status`/...). This looks like a personal-dev-target build sitting in place of whatever the model is supposed to produce. Worth confirming which one is the intended production mart before trusting either.

---

## Summary for Chris

- **Biggest structural gap:** 98.2% of `CONNECT_EDGES` (the connection graph) reference at least one table `ENTITY_INDEX` has never indexed — the edge-discovery step and the entity-indexing step are scanning different table universes. Only 0.1% are actually dead/renamed tables, so this is a coverage gap, not decay.
- **Fake bridge key confirmed live:** NPPES's `EIN` column reads as 100% populated by a naive null-check but is ~100% blank/`<UNAVAIL>` sentinel underneath — matches the "Bridge Fuel Reality" pattern already in memory, now measured. Same masking pattern hit `FED_NOAA_AIS.imo_number` (~56% fake).
- **Mission-relevant:** `FED_HHS_OIG_LEIE` (the federal exclusions list) is 89.6% unusable by NPI — most of the "banned" list can't be joined to a provider profile at all, which directly undercuts the "banned but still operating" lens.
- **13 marts confirmed off-parity** against their true dbt-lineage-verified raw source (not name-guessing — that approach produced 2 false positives, corrected here). Worst: `CONSUMER_PROTECTION__FED_CFPB_COMPLAINTS` at 500 rows vs. 17.2M real.
- **Two easy green-lane fixes surfaced:** `ECONOMICS__INTL_GLEIF_RR.period_start_date` is 100% null (broken date-parse format), and `CORPORATE_REGISTRY__INTL_IE_CRO`'s live table doesn't match its own dbt model at all.
- No fixes applied, no schema changes, no writes — every number above came from a live read-only query or a verified static lineage trace.
