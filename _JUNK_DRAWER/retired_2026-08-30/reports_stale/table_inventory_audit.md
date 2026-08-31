# Table Inventory Audit — 2026-07-28

Static read of the pasted `INFORMATION_SCHEMA.TABLES` dump (3,512 tables). No warehouse queries run, no fixes applied — report only, per instructions. INFORMATION_SCHEMA system views (APPLICABLE_ROLES, COLUMNS, etc., repeated 5x per DB) excluded as noise.

---

## 1. Duplicate / near-duplicate tables

**FED_MSHA_* vs FED_DOL_MSHA_*** (accidents, mines, violations)
- Two parallel loaders for the same MSHA data, three days apart: `FED_MSHA_*` (created 07-23) and `FED_DOL_MSHA_*` (created 07-26, later — looks like a re-run under a new naming convention).
- `LABOR__FED_MSHA_ACCIDENTS`/`MINES`/`VIOLATIONS` marts match the **non-DOL-prefixed** row counts exactly (273,623 / 91,906 / 3,087,215), not the DOL-prefixed ones.
- `FED_DOL_MSHA_VIOLATIONS` is capped at exactly **500,000** rows vs. `FED_MSHA_VIOLATIONS`'s real 3,087,266 — the newer loader is badly undercounting.
- **Canonical:** `FED_MSHA_*` (has working marts). **Abandoned:** `FED_DOL_MSHA_*` (broken/capped re-load, never wired to anything, plus 5 more DOL_MSHA_* siblings — ADDRESSES, ASSESSED_VIOLATIONS, CONTROLLER_HISTORY, EMPLOYMENT_YEARLY, INSPECTIONS — with no counterpart or mart at all).

**FED_EPA_FRS_FRS_FACILITIES vs FED_EPA_FRS_FULL**
- `FRS_FRS_FACILITIES` (note the doubled "FRS_FRS" — naming bug from a nested-source flatten) capped at exactly 500,000 rows, created 07-26.
- `FRS_FULL` has the real 5,300,149 rows, created 07-27 (one day later).
- `ENVIRONMENT__FED_EPA_FRS_FACILITIES` mart matches `FRS_FULL` exactly. **Canonical:** FRS_FULL. **Abandoned:** FRS_FRS_FACILITIES, plus its siblings FRS_NAICS_CODES / FRS_PROGRAM_LINKS / FRS_SIC_CODES (all also capped at 500,000, all orphaned, no marts).

**FED_EPA_ECHO vs FED_EPA_ECHO_EXPORTER_ECHO_EXPORTER**
- Same pattern: the "EXPORTER_ECHO_EXPORTER" table (doubled name again) is capped at 500,000 rows, loaded 07-26.
- `ENVIRONMENT__FED_EPA_ECHO` mart matches base `FED_EPA_ECHO` (3.16M rows), not the capped exporter copy. **Abandoned:** the EXPORTER table.

**FED_FEC_BULK_* vs FED_FEC_* (non-bulk)**
- Old "BULK" ingest (candidates/committees/summary, loaded ~06-29) sits alongside a newer non-bulk ingest of the same subjects (loaded 07-23) with materially different row counts (e.g. candidates 17,900 → 33,506).
- `POLITICS__FEC_CANDIDATE` mart still matches the **old BULK** count (17,900) — the July 23 reload was never wired into the mart layer. Same story for committees. Looks like a half-finished pipeline swap: someone re-pulled FEC data under new names and never repointed the marts.

**FED_IRS_EO_BMF vs FED_IRS_BMF**
- `FED_IRS_EO_BMF` sits in an explicit `RETIRED` schema (3,949,660 rows, last touched 07-12) — self-flagged as superseded by `FED_IRS_BMF` (1,974,830 rows, mart-backed). No action needed, just noting it's still taking up ~200MB.

**FED_CMS_OPEN_PAYMENTS family (4-way duplication)**
- `FED_CMS_OPEN_PAYMENTS` (15.4M rows, base), `_2022` (13.25M), `_2023` (14.7M), and `FED_CMS_OPEN_PAYMENTS_GNRL` (15.4M, sitting in `RETIRED` schema, loaded most recently on 07-23/24).
- No mart anywhere consolidates these (see §4) — this is a duplicate cluster **and** an orphan at the same time. Given CLAUDE.md's own example findings reference opioid-prescriber-paid-after-exclusion patterns, this looks like a live gap, not dead code.

**FED_CMS_HOSPITAL_COMPARE vs FED_CMS_HOSPITAL_GENERAL**
- Identical row count (5,432) — near-certainly the same CMS dataset pulled under two different portal names. Neither has a mart. Low priority but easy dup to collapse.

**FED_CMS_NURSING_HOME vs FED_NURSINGHOME411**
- 14,700 vs 14,713 rows — same underlying CMS nursing-home data from two source portals. `HEALTH__FED_CMS_NURSING_HOME` mart exists (matches the CMS-prefixed one). `FED_NURSINGHOME411` is the orphaned twin.

**FED_DEA_ARCOS vs FED_DEA_ARCOS_FULL**
- `FED_DEA_ARCOS` is a 409-row stub from 07-01 (same day created/altered — never touched again). `FED_DEA_ARCOS_FULL` is the real 178.6M-row load from 07-27, correctly mart-backed (`HEALTH__FED_DEA_ARCOS`). The stub should just be dropped — it's dead weight, not a live alternate.

**FED_SEC_13F_SUBMISSION (singular) vs FED_SEC_13F_SUBMISSIONS (plural)**
- 3,822,885 rows vs 336,124 rows — different grain or different loader run under near-identical names, both landed 07-26/07-27. No mart on either yet (whole 13F cluster looks mid-build, consistent with the recent "wire SEC 13F into connection engine" commit — flagging for reconciliation, not necessarily abandoned).

---

## 2. Row counts that look way too low

**`ECONOMICS__FED_IRS_990` — 200 rows** (your own example, confirmed)
- Raw `FED_IRS_990` is also only 200 rows. But the real IRS 990 universe is sitting right there in the warehouse: `FED_IRS_990_EFILE_INDEX` (5.5M rows) and `FED_IRS_990_EFILER_INDEX_2022`/`_2023` (500K each, capped). The mart was **rebuilt as recently as 07-27** but still points at the 200-row stub, not the real index tables. This isn't stale neglect — it's actively wired to the wrong source.

**`CONSUMER_PROTECTION__FED_CFPB_COMPLAINTS` — 500 rows**
- Raw `FED_CFPB_COMPLAINTS` has 17,179,788 rows (loaded 07-23). The mart was built 06-20 and last touched 07-12 — a month before the real 17M-row load landed — and never rebuilt since. Biggest count gap in the whole inventory (500 vs 17.2M).

**`FED_SAM_EXCLUSIONS` (9,000) → `PROCUREMENT__FED_SAM_EXCLUSIONS` (8,500)**
- Both suspiciously round numbers. SAM.gov's exclusions list typically runs tens of thousands of active records — this smells like a paginated API pull that stopped at a page-count limit rather than exhausting the source.

**Round-number caps recur across a whole batch of 07-26 EPA/CMS loads** (pattern already known per memory — loader hits 500K/1M/9K/20M and stops):
- EPA: `FED_EPA_FRS_FRS_FACILITIES`, `_NAICS_CODES`, `_PROGRAM_LINKS`, `_SIC_CODES`; `FED_EPA_NPDES_ICIS_FACILITIES`, `_INFORMAL_ENFORCEMENT_ACTIONS`, `_INSPECTIONS`, `_QNCR_HISTORY`, `_SICS`; `FED_EPA_SDWA_SDWA_FACILITIES`, `_GEOGRAPHIC_AREAS`, `_LCR_SAMPLES`, `_SITE_VISITS`, `_VIOLATIONS_ENFORCEMENT`; `FED_EPA_ICIS_AIR_*_FCES_PCES`, `_POLLUTANTS`, `_STACK_TESTS`, `_TITLEV_CERTS`.
- CMS: `FED_CMS_MEDICARE_DIALYSIS_FACILITIES`, `_FEE_FOR_SERVICE_PUBLIC_PROVIDER_ENROLLMENT`, `_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER` (and `_AND_SERVICE`), `_QUALITY_PAYMENT_PROGRAM_EXPERIENCE`, `_ORDER_AND_REFERRING`, `_FACILITY_LEVEL_MINIMUM_DATA_SET_FREQUENCY`, `_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_...`.
- USASpending: `FED_USASPENDING_CONTRACTS_FULL` is exactly **20,000,000** rows — "FULL" is a misnomer, it hit a cap. `FED_USASPENDING_ASSISTANCE_FULL` (19,902,879) is suspiciously close to the same ceiling.
- None of these have marts (see §4), so nobody's hit the undercounting yet downstream — worth checking before anyone builds on top.

**`CONSUMER_SAFETY__FED_NHTSA_INVESTIGATIONS` — 30,748 rows vs raw 154,209**
- ~80% of rows disappeared between raw and mart. Worth checking the mart's filter/join logic — this doesn't look like a dedup, it looks like a bad join dropping rows.

**Cluster of 1-row "stub" tables that never got real data**, mostly created 07-01/07-02, all last touched 07-12 (a bulk metadata touch, not a real refresh): `FED_FINCEN_BOI`, `FED_ED_FSA_DATACENTER`, `FED_FRA_SAFETY`, `FED_DOJ_CRT_CASES`, `FED_FBI_CDE`, `FED_CMS_HPT_MRF`, `FED_FDA_DRUG_ENFORCEMENT` (1 row but 6.3MB — likely one unflattened JSON blob), `FED_CDC_WONDER` (1 row, 88KB — same pattern). `FED_FINCEN_BOI` (Beneficial Ownership registry) being empty is the one I'd worry about most given the corporate-transparency angle of the mission.

---

## 3. Stale tables sitting next to active ones from the same source

- **`GOLD_PAIRS`** (CONNECT, 6.5M rows) — last touched 06-25, never since. Sits next to **`MATCH_PAIRS`** (16.2M rows, CONNECT) which was refreshed 07-27. Same entity-matching subject area, one frozen for a month, the other running daily.
- **`ENTITY_LINKS`** (CONNECT, 2,324 rows) — last touched 06-25. Sits next to `ENTITY_MAP`/`ENTITY_INDEX`/`ENTITY_GOLDEN`, all refreshed 07-27. Looks like a predecessor table the pipeline moved past without dropping.
- **`VAULT_RECEIPTS`** (INGEST_LOGS, 8 rows) — last touched 06-13. Sits next to `INGEST_RUNS` (2,421 rows), refreshed 07-27 — six weeks of drift in the same schema.
- **`FED_CMS_OPEN_PAYMENTS_GNRL`** and **`FED_IRS_EO_BMF`** — both explicitly parked in a `RETIRED` schema, both untouched since 07-24 and 07-12 respectively. Self-flagged already, just still consuming ~1GB and ~200MB.
- **`KEYSET_SCRATCH`** (54.4M rows, CONNECT) and **`CROSSWALK_SCRATCH`** (4.9M rows, CONNECT) — named as scratch/working tables but sitting fully populated at production scale, 2 days stale next to `KEYSET_LIVE` (refreshed today). Looks like leftover intermediate output from the entity-resolution run that isn't being cleaned up between runs.
- **`_SOURCE_REGISTRY_BAK_*`** — five separate backup snapshots of `SOURCE_REGISTRY` (20260701, JOINKEYS_20260712, SPINEBACKFILL_20260705, SPINECOLS_20260705, SPINE_ENTITY_20260706), several weeks old, sitting in LIBRARY_META.REGISTRY. Pre-migration snapshots that were probably meant to be temporary.
- **`LIBRARY_MARTS._RESTORE_20260701`** schema — a whole batch of 12 tables (CIVIL_RIGHTS__FED_NARA_WRA_AAD, CORPORATE_REGISTRY__INTL_IE_CRO, ECONOMICS__FED_HHS_TAGGS, ECONOMICS__INTL_CH_ZEFIX, ECONOMICS__INTL_GR_GEMI, GOVERNMENT_RECORDS__FED_NARA_AAD, HISTORICAL_RECORDS__FED_SLAVEVOYAGES_INTRAAMERICAN, JUSTICE__FED_DOJ_CRT_CASES, JUSTICE__FED_FJC_IDB, LEGAL_ENFORCEMENT__FED_NAAG_MULTISTATE_SETTLEMENTS, MART_EPSTEIN_COMPLIANCE_LEDGER, REGULATION__FED_FDIC_ENFORCEMENT), all created/altered the same moment on 07-01, all 1-3 rows. Reads as a disaster-recovery/pre-refactor snapshot that's been sitting untouched for almost a month. Whole-schema cleanup candidate.

---

## 4. Orphaned raw/staging tables — no dbt mart built on top

**The big one: PORTAL_ARC_* / PORTAL_CKA_* / PORTAL_SOC_* sprawl.** Hundreds of hash-suffixed tables (`PORTAL_ARC_ATLANTA_DATAATLA_03DC194F2A`, `PORTAL_CKA_WPRDC_ALLEGHENY_*`, `PORTAL_SOC_UTAH_OPEN_DATA_P_*`, etc.) landed in one big batch 06-23 through 07-02 — reads like an automated crawl trying to auto-ingest every city/county/state open-data portal it could find (Atlanta, Houston, Harris County, LA County, Tucson, Boston, Cambridge, California, Indiana, Ireland, Israel, Oklahoma, San Jose, Tampa, Virginia, Western PA/WPRDC, Austin, Chicago, Colorado, Connecticut, DataLA, Maryland, NY State, Oregon, PA, Santa Clara, Seattle, SF, Texas, Utah, Washington, Wisconsin...). Most are tiny (dozens to a few thousand rows), each has a matching `STG_PORTAL_*` staging model (also empty row counts = views), and **none have a mart**. This is by far the largest orphaned layer in the warehouse. Reads as a "can we ingest every open-data portal automatically" experiment that got parked mid-flight rather than a bug — worth a taste-lane decision (Chris) on whether to finish, prune, or archive.

**SEC 13F cluster** — `FED_SEC_13F_FILERS`, `_HOLDINGS` (101.3M rows!), `_POSITIONS`, `_SUBMISSION`, `_SUBMISSIONS` — all landed 07-26/07-27, no marts yet. Matches the recent "wire SEC 13F into connection engine" commit, so likely just in-progress rather than abandoned.

**FED_SEC_INSIDER_DERIV_TRANS** (1,049,121 rows) — its three siblings (NONDERIV_TRANS, REPORTINGOWNER, SUBMISSION) all got `FINANCE__` marts built 07-27. DERIV_TRANS is the one that got skipped — looks like a straightforward miss, not a design choice.

**INTL_GLEIF** (3.38M rows, base LEI registry) and **INTL_GLEIF_REPEX** (6.26M rows) — only the smaller `_RELATIONSHIPS`/`RR` facet (via `INT_GLEIF_RR`) got a mart (`ECONOMICS__INTL_GLEIF_RR`). The core entity registry itself was never matted.

**FED_COURTLISTENER_DOCKETS** — 71.7M rows, loaded 07-26, no mart at all. Largest un-matted single table in the inventory by row count outside of DEA_ARCOS_FULL.

**Whole EPA NPDES/ICIS-Air/SDWA batch from 07-26** — roughly 25 raw tables (facilities, violations, inspections, enforcement actions, permits, program subparts, etc. across three EPA sub-programs) landed the same day, capped at round numbers (see §2), and none have marts. This looks like a big single-day ingest push that outran the mart-build step — a natural next-build candidate, but currently 100% orphaned.

**FED_USASPENDING_CONTRACTS_FULL / _ASSISTANCE_FULL** (20M / 19.9M rows, 07-23) — only the older, smaller `FED_USASPENDING_CONTRACTS` (6.3M) feeds the `SPENDING_BUDGET__*` aggregate marts. The "FULL" reloads are sitting unused, in addition to being capped (§2).

**FED_USASPENDING_BULK** (50,000 rows, round/capped, 07-02) and **FED_USASPENDING_SUBAWARDS** (5,000 rows, round/capped, 06-10) — old stubs with no mart and, unlike CONTRACTS/ASSISTANCE, never got a "_FULL" successor either. These look like genuinely abandoned pulls, not just pre-mart.

---

## Summary for Chris

- **Clearest "pick one and delete the other" calls:** FED_MSHA_* vs FED_DOL_MSHA_* (keep MSHA_*), FRS_FRS_FACILITIES vs FRS_FULL (keep FULL), ECHO vs ECHO_EXPORTER_ECHO_EXPORTER (keep base), FED_DEA_ARCOS 409-row stub (just drop it).
- **Broken marts that need a rebuild, not a judgment call:** `ECONOMICS__FED_IRS_990` (200 rows, wrong source wired in) and `CONSUMER_PROTECTION__FED_CFPB_COMPLAINTS` (500 rows, month-stale) are both truth questions — green-lane fixes once someone points them at the right raw table.
- **Biggest open taste question:** what to do with the PORTAL_* portal-crawl sprawl (hundreds of tables, zero marts) and the big 07-26 EPA regulatory batch (also zero marts) — finish building marts on them, or was the crawl an experiment that's done?
