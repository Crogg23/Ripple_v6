# Wiring gap re-derived without the name join — 2026-08-31

Handoff said: 628 STEEL+STRONG joinable, 132 wired, 496 to go — but built on
`UPPER(SOURCE_ID) = SOURCE_TABLE`, a known trap.

## Method

Mapped each of the 266 distinct `SOURCE_TABLE` values in
`LIBRARY_META."CONNECT".ENTITY_INDEX` to a registry `SOURCE_ID` by, in order:

1. `LIBRARY_META.REGISTRY.SOURCE_FRESHNESS.LANDING_FQN` (102 rows carry a real FQN)
2. case-insensitive exact name match
3. hand-checked alias map (12 tables, listed below)
4. longest registry SOURCE_ID prefix (catches child tables like `FED_COURTLISTENER_COURTS`)

Result: 258 of 266 mapped → 246 distinct registry sources wired.
8 index tables have **no registry row at all**:

```
FED_CMS_PECOS_PROVIDER_ENROLLMENT   FED_EPA_GHGRP_FACILITY
FED_HRSA_UDS_SERVICE_DELIVERY_SITES FED_IRS_527_ORGS
FED_PCAOB_FORM_AP_FILINGS           FED_SBIR_STTR_AWARDS
FED_SEC_INVESTMENT_COMPANY_SERIES_CLASS  INTL_ISO_MIC_REGISTRY
```

## Alias map used (index table → registry SOURCE_ID)

| Index table | Registry row |
|---|---|
| FED_CFPB_HMDA_ARID2017_LEI_XREF, FED_CFPB_HMDA_LAR | FED_CFPB_HMDA |
| FED_CMS_OPEN_PAYMENTS_PROFILE_SUPPLEMENT | FED_CMS_OPEN_PAYMENTS |
| FED_DOL_EBSA_FORM5500_SCHEDULE_SB | fed_dol_form5500 |
| FED_EPA_FRS_FRS_FACILITIES | FED_EPA_FRS_FULL |
| FED_NCUA_CALL_REPORTS_FOICU / _FS220 / CHARTER_MERGER_EVENTS / FEDERALLY_INSURED_CU_LIST | fed_ncua_call_reports |
| FED_PBGC_TRUSTEED_PENSION_PLANS | fed_pbgc_trusteed_plans |
| FED_SAM_EXCLUSIONS_FULL_R2 | FED_SAM_EXCLUSIONS |
| FED_ICE_DETENTION_FACILITY_CODES | fed_ice_detention_facility_list |
| UK_COMPANIES_HOUSE_PSC | corporate_registry_uk_companies_house_psc |

## Numbers

| Basis | STEEL+STRONG total | Wired | Gap |
|---|---|---|---|
| INCLUDE='Y' only (handoff's basis) | 628 | 132 | 496 |
| Whole registry | 799 | 218 | 581 |

The handoff's tier table was already filtered to INCLUDE='Y'; its 496 holds.

## New facts the handoff didn't have

- Registry SOURCE_ID is mixed-case; case-blind matching is mandatory.
- 90 wired sources sit in the registry without INCLUDE='Y' (handoff guessed 87).
- Registry carries near-duplicate rows for the same real source
  (companies house ×3, pbgc ×2, form5500 ×2) — denominators are slightly inflated.
- SOURCE_FRESHNESS.LANDING_FQN is the only real source→landing mapping table,
  and it only covers 102 sources. Extending it as wiring proceeds would kill
  this trap permanently.

Query: joined SOURCE_REGISTRY (2,786 rows) to distinct ENTITY_INDEX.SOURCE_TABLE
via the four-step mapping above; script inline in session, ~5 s runtime, trivial cost.

---

# Batch A execution receipts — same day

## What ran

1. `python -m connect apply-config` — exit 0. Wired FED_DOL_FORM5500
   (29,069 sponsor EINs) and swept a CMS backlog: PECOS 2,456,135 ids,
   hospitals 5,280, home health 10,223, hospice 5,372, SNF 12,218,
   FQHC 1,559, RHC 2,500.
2. Six staged tables were tracked but never resliced. Root causes, both proven:
   - connect-one silent no-op: watermark content-key already stored by an old
     discover-path run, so the spine reslice never fired. Early returns at
     connect/incremental.py:1097-1103 skip the print — invisible.
   - KEY_TYPE truncation: ENTITY_INDEX (12), ENTITY_GOLDEN (12),
     SOURCE_OVERLAP_MATRIX (8) were too narrow for 'EIA_UTILITY_ID' (14).
     The 2026-08-29 batch run crashed there, leaving EIA860_1 in keyset but
     not index. All three widened to VARCHAR(32); widths came from old CTAS
     inference, no coded DDL to patch.
3. Direct `reslice_spine` per table after the widenings:

| Table | Keys merged |
|---|---|
| FED_FDIC_BANK_DATA | 54,406 |
| FED_FDIC_SOD_BRANCH_DEPOSITS | 31,042 |
| FED_FHFA_FHLB_MEMBERSHIP | 3,984 |
| FED_EIA860_2_PLANT | 16,128 |
| FED_EPA_EGRID_PLANT_2022 | 11,971 |
| FED_EIA860_1_UTILITY | attr-refresh, ids already present, index backfilled |

## End state

ENTITY_INDEX: 96,181,019 rows, 273 sources (was 93,534,490 / 266).
Keyset == index for all seven touched tables, verified row-for-row.
Agreement guard: 2 passed, 60s.
New live axes: FDIC_CERT, RSSD, EIA_UTILITY_ID, EIA_PLANT_ID.

## Final end state, after skeptic fixes — verified live

- FED_DOL_FORM5500 retracted: 0 index rows, 1,513 solo entities deleted,
  27,556 shared entities re-derived.
- Two more bugs found while closing:
  - stale config pins: apply-config's pin write is its last step, and every
    run today crashed before reaching it, so each run redid all drift work.
  - the crasher: reslice_discover's pair query on FED_USASPENDING_CONTRACTS
    (the superseded 6.3M early pull) exceeds Snowflake's 128MB LOB cap
    (239MB actual). Fixed by removing that dead table's two graph-key
    entries from keys.py — FULL_R2 carries both keys already.
- Config pinned: 368 units, drift re-reads ZERO.
- Index: 96,399,174 rows, 272 sources, 28 key types.
- Agreement guard: 2 passed post-everything.
- Offline suite additions: KEY_TYPE width regression test (44 pass in file).
- Session warehouse burn to ~18:00: 4.58+ credits ≈ $9-11 at the $2 default.
