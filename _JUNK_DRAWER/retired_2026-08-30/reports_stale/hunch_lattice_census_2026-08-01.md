# Hunch Engine — Lattice Census (2026-08-01)

One primitive: two columns in two tables that normalize to the same join
key are comparable. Gated = both sides' key column is >= 1.0% populated (measured, not declared).

| Tier | Table-pairs (gated) | (ungated) | Column-pairs (gated) |
|---|---:|---:|---:|
| STEEL | 1,332 | 1,953 | 1,758 |
| STRONG | 10 | 15 | 34 |
| GEO (of which spatial: 181) | 5,018 | 7,668 | 7,644 |
| PROBABILISTIC | 19,471 | 23,430 | 130,298 |
| BRIDGE (2-hop, not directly connected) | 68 | — | — |
| CORROBORATED candidates* | 2,756 | — | — |

**Distinct comparable table-pairs (each counted once, at its strongest tier): 19,326**

Strongest-tier split of the direct pairs: STEEL 1,255, STRONG 10, GEO 4,165, PROBABILISTIC 13,828

Already verified by connect/: 2,371 of 19,326 (12.3%). Previously tested and gated out as flukes: 3,814 (aggregate; per-pair identities not persisted). Never tested: 16,955.

*CORROBORATED candidates = both sides carry a NAME column and share a ZIP/FIPS pin. Whether the names actually co-populate is unmeasurable from metadata — measuring it is a later, costed step.

## Random sample (seed 20260801, weighted by pair count)

| A | B | key | tier | fill A/B | traps | verified |
|---|---|---|---|---|---|---|
| INTL_EG_CAPMAS | INTL_OPENSANCTIONS | NAME | PROBABILISTIC | 100%/77% | — | no |
| FED_SAM_EXCLUSIONS | INTL_EG_CAPMAS | NAME | PROBABILISTIC | 100%/100% | — | no |
| FED_CMS_MEDICARE_DIALYSIS_FACILITIES | INTL_UCDP_GED | NAME | PROBABILISTIC | 100%/100% | — | no |
| FED_CMS_POS_OTHER | FED_EPA_EGRID_PLANT_2022 | NAME | PROBABILISTIC | 100%/100% | — | yes |
| FED_CISA_KEV | FED_SEC_DERA_SUB_2025Q4 | NAME | PROBABILISTIC | 100%/100% | — | no |
| FED_CMS_HOSPICE_ENROLLMENTS | FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER_AND_SERVI | ZIP | GEO | 100%/100% | — | yes |
| FED_IRS_990_EFILE_INDEX | INTL_OPENSANCTIONS | NAME | PROBABILISTIC | 100%/77% | — | no |
| FED_SENATE_LDA_FILINGS | XC_VERA_INCARCERATION_TRENDS | NAME | PROBABILISTIC | 100%/100% | — | no |
| FED_EPA_FRS_FULL | INTL_UCDP_GED | NAME | PROBABILISTIC | 100%/100% | — | no |
| FED_DOL_FORM5500 | FED_FEC_API | NAME | PROBABILISTIC | 100%/100% | — | no |
| FED_CMS_MEDICARE_INPATIENT_HOSPITALS_BY_PROVIDER_AND_SERVICE | FED_CMS_OPT_OUT_AFFIDAVITS | ZIP | GEO | 100%/100% | — | no |
| FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS | FED_ICE_STATISTICS | COUNTRY | GEO | 98%/89% | — | no |
| FED_CMS_OPEN_PAYMENTS_2023 | FED_OSHA_ITA_300A_SUMMARY_2023 | ZIP | GEO | 100%/96% | trap_open_payments_split | no |
| FED_CMS_HCRIS | FED_FDIC_BANK_DATA | ZIP | GEO | 100%/100% | — | no |
| FED_GOOGLE_POLADS_ADVERTISER_DECLARED_STATS | FED_SEC_BUSINESS_DEVELOPMENT_COMPANY_REPORT | NAME | PROBABILISTIC | 92%/100% | — | no |
| FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS | FED_CMS_LTCH | ADDRESS | PROBABILISTIC | 100%/100% | — | no |
| FED_CDC_OVERDOSE | FED_EPA_EGRID_PLANT_2022 | NAME | PROBABILISTIC | 100%/100% | — | no |
| FED_FHFA_NMDB | FED_MSHA_MINES | NAME | PROBABILISTIC | 100%/100% | — | no |
| FED_CMS_MEDICARE_DIABETES_PREVENTION_PROGRAM | FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS | NAME | PROBABILISTIC | 100%/100% | — | yes |
| FED_NOAA_STORM_EVENTS | FED_SENATE_LDA_FILINGS | NAME | PROBABILISTIC | 100%/100% | — | no |

## Blind spots — what this census could NOT compare

- Fingerprinted tables: 1,043. Landing universe: 1,933 → 895 landing tables have no fingerprint and are invisible here.
- Marts: 436 mart tables are not lattice members (no fingerprints, no registry rows) — step-1 scope decision.
- COLUMN_CATALOG: provisioned: 751 column rows over 25 tables
- Deliberately scoped out (mirrors connect/ edge universe): 668 PORTAL_* crawl tables, 7 abandoned duplicates.
- Zero-key tables (fingerprinted, nothing joinable): 102; tables whose only keys are banned classification codes: 2.
- Classification codes banned as join keys (D17): NAICS: 364 tables, 66,066 foregone pairs; NCES: 29 tables, 406 foregone pairs; SIC: 157 tables, 12,246 foregone pairs.
- Trap-flagged lattice members (honesty/traps.py): 9 tables — FED_CMS_NPPES, FED_CMS_OPEN_PAYMENTS, FED_CMS_OPEN_PAYMENTS_2022, FED_CMS_OPEN_PAYMENTS_2023, FED_FCC_LICENSING, FED_HHS_OIG_LEIE, FED_NOAA_AIS, FED_OFAC_SDN, FED_USASPENDING_CONTRACTS.
- Time-only comparisons (two tables with a time axis, no shared key): 82 tables carry a usable time axis → 3,321 possible comparisons. Reported as one aggregate; not lattice rows (no join axis).
- Declared-vs-measured join-key tier disagreements: 169 sources (registry JOIN_KEY_TIER uses a different vocabulary — appendix only).
- fingerprint profiler caps at 80 text columns per table; columns past the cap are invisible to this census
- marts are not lattice members in step 1 (no fingerprints, no registry rows); the mart universe is counted, not paired
