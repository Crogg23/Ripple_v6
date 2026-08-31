# Verified facts — measured directly this session (2026-08-22)

Everything here came from `INFORMATION_SCHEMA` (live, today) plus deterministic
crunching of the resulting CSVs. Nothing here is an agent's inference.

## 1. The warehouse is overwhelmingly text-typed

162,750 columns across 4,847 objects:

| data type | columns | share |
|---|---:|---:|
| TEXT | 149,003 | 91.6% |
| NUMBER | 7,558 | 4.6% |
| DATE | 2,150 | 1.3% |
| FLOAT | 2,064 | 1.3% |
| TIMESTAMP_NTZ | 1,285 | 0.8% |
| BOOLEAN | 389 | 0.24% |
| TIMESTAMP_LTZ | 120 | 0.07% |
| VARIANT | 110 | 0.07% |
| ARRAY | 65 | 0.04% |
| OBJECT | 4 | — |
| **GEOGRAPHY** | **2** | — |

The two GEOGRAPHY columns are the same one, exposed twice:
`LIBRARY_MARTS.MARITIME.MARITIME__FED_NOAA_AIS.POSITION_GEOGRAPHY` and its
TIMELINE view. There are **zero** GEOMETRY columns and **zero** polygon columns
anywhere in the warehouse.

## 2. Column name ≠ usable type — the gap, measured

| shape | tables whose column NAME matches | tables where at least one is really typed | text-only tables |
|---|---:|---:|---:|
| latitude | 805 | **122** | 683 |
| longitude | 810 | **122** | 688 |
| **both lat and lon, really numeric** | 801 | **122** | 679 |
| money / amount | 948 | **322** | 626 |
| date / time | 3,517 | **1,058** | 2,459 |

Column-level: 844 latitude columns exist, 714 of them TEXT. 4,977 money columns,
3,478 TEXT. 12,562 date-ish columns, 9,385 TEXT.

## 3. The 120 tables that can be plotted on a map today

Tables with **both** latitude and longitude as real numeric columns, excluding
backup/restore/retired schemas. 88 are in `LIBRARY_MARTS`; 20 have ≥100k rows.
Top of the list:

| rows | table |
|---:|---|
| 58,104,610 | LIBRARY_MARTS.MARITIME.MARITIME__FED_NOAA_AIS |
| 7,200,550 | LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_FRACFOCUS_REGISTRY |
| 6,694,816 | LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_USGS_WATER |
| 5,300,149 | LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FACILITIES |
| 3,277,557 | LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FRS_FACILITIES |
| 3,135,554 | LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ECHO |
| 2,823,000 | LIBRARY_MARTS.FINANCE.FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS |
| 1,780,730 | LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_NOAA_STORM_EVENTS |
| 1,613,224 | LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_RCRA_FACILITIES |
| 1,213,737 | LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_ICIS_FACILITIES |
| 1,150,788 | LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_FRA_CASUALTIES |
| 443,274 | LIBRARY_MARTS.SCIENCE.SCIENCE__FED_USGS_EARTHQUAKES |
| 385,918 | LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_UCDP_GED |
| 304,632 | LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_USGS_MINERALS |
| 248,835 | LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_FRACFOCUS_DISCLOSURE_LIST |
| 224,941 | LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_FRA_EQUIPMENT_ACCIDENTS |
| 165,531 | LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_SHORTAGE_AREAS |
| 136,005 | LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_GHGRP_FACILITY |
| 117,672 | LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_USGS_ORPHANED_OIL_GAS_WELLS |
| 93,808 | LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__EPA_PENALTY_GAP |

The pattern is that the **mart layer is where coordinates got cast** — the raw
landing copies of the same sources are usually still TEXT.

## 4. A complete geographic reference spine already exists

| table | rows | what it carries |
|---|---:|---|
| `LIBRARY_MARTS.CORE.DIM_TRACT` | 85,391 | TRACT_GEOID, COUNTY_FIPS, STATE_FIPS, **POPULATION_2020**, **POP_CENTER_LAT/LON** |
| `LIBRARY_MARTS.CORE.DIM_COUNTY` | 3,222 | COUNTY_FIPS, STATE_FIPS, names, **POPULATION_2020**, **POP_CENTER_LAT/LON** |
| `LIBRARY_MARTS.CORE.XWALK_ZCTA_COUNTY` | 46,960 | ZCTA5 → COUNTY_FIPS → STATE_FIPS, XWALK_TYPE |
| `LIBRARY_MARTS.CORE.DIM_STATE` | 56 | STATE_FIPS, USPS, name, territory flag |
| `LIBRARY_MARTS.REFERENCE.REF__DIM_GEOGRAPHY` | 6,988 | FIPS, county/state names, EPA_REGION, **CENTROID_LAT/LON**, FACILITY_COUNT |
| `LIBRARY_MARTS.REFERENCE.REF__DIM_STATE` | 56 | + CENSUS_REGION, CENSUS_DIVISION |
| `LIBRARY_MARTS.CORE.DIM_DATE` | 31,411 | full day spine with fiscal year |
| `LIBRARY_MARTS.REFERENCE.REFERENCE__CALENDAR` | 155,593 | day spine + federal fiscal + **ELECTION_CYCLE, CONGRESS_NUMBER** |

**What is NOT there: any adjacency table** — nothing anywhere says which county
borders which county. Grepped ALL_TABLES.csv for TIGER / SHAPEFILE / BOUNDARY /
ADJACEN / GAZETTEER / ZCTA boundaries: the only polygon-ish source is
`LIBRARY_RAW.LANDING.FED_EPA_SUPERFUND_SITE_BOUNDARIES` (2,114 rows) and
`FED_BIA_TRIBAL_GEO` (100 rows). Neighbour weights would have to be built from
the centroids that DIM_COUNTY and DIM_TRACT already carry.

**Population denominators exist** in DIM_TRACT and DIM_COUNTY (2020 census) — the
"per person served" branch was parked 1,426 times in the census grid and its
denominator has been sitting in CORE the whole time.

## 5. The graph layer — what is actually there

Live counts today (`LIBRARY_META.CONNECT`):

- `MATCH_PAIRS` 181,002,484 — KEY_VALUE × TABLE_A × TABLE_B. An **entity-to-table incidence list**, not an entity-to-entity edge list. Projects into a co-occurrence graph.
- `CONNECT_NODES` / `ENTITY_INDEX` / `SPINE_KEYSET` 84,382,504 each.
- `ENTITY_GOLDEN` / `ENTITY_MAP` 33,312,349 — resolved entities. `ENTITY_MAP.SOURCE_COUNT` is **degree, already computed**, and `MEMBER_TABLES` is an ARRAY of the tables each entity appears in.
- `ENTITY_XREF` 2,672,384 — KEY_A/VALUE_A → KEY_B/VALUE_B with **RELATION** and **FANOUT**: the closest thing to a typed edge list in META.
- `CONNECT_EDGES` **4,512** (was 4,910 pre-08-28 rebuild; corrected 2026-08-30 against live) — this is a **table-to-table** graph (A, B, KEY, TIER, MATCH_RATE, CONFIDENCE), i.e. a schema map, not people or companies.
- `LEADS` 17,598 — LEFT_ENTITY_ID → RIGHT_ENTITY_ID with SCORE and EVIDENCE.
- `BRIDGE_ENTITIES` is **empty (0 rows)**.
- `DOMAIN_OVERLAP_MATRIX` has **7 rows**; `SOURCE_OVERLAP_MATRIX` has **36**. The
  "which domains connect to which" picture is essentially unpopulated.

**No edge in META carries an event time.** Every timestamp on those tables is
`BUILT_AT` / `CREATED_AT` — when Ripple computed the edge, not when anything
happened in the world.

**Documented tier reality** (from `reports/question_ladder_2026-08-12.md`, when the
map held 4,538 edges; it holds 4,512 as of the 2026-08-28 rebuild (was 4,910 before it), so this split is close but not exact):
1,121 edges are hard-ID across 14 key families (EIN, NPI, FRS_ID, CIK, CCN,
PWSID, LEI, FEC_CAND_ID, UEI, BIOGUIDE, FEC_CMTE_ID, DUNS, ICPSR, MINE_ID).
2,606 — the entire "corroborated" tier — are **name-plus-address matches, not IDs**.
That same report records: politics rides zero verified cross-family joins, and
the harm-heaviest sources (opioid shipments, sanctions, offshore leaks, ICE
detention, device injuries, the practitioner data bank, all 71.7M court dockets)
have **zero verified edges to anything**.

## 6. Hard-ID edge lists that exist OUTSIDE the connection layer

These are the strongest graphs in the warehouse and none of them depend on the
fuzzy CONNECT tier:

| table | rows | the edge |
|---|---:|---|
| `LIBRARY_RAW.LANDING.FED_DEA_ARCOS_FULL` / `LIBRARY_MARTS.HEALTH.HEALTH__FED_DEA_ARCOS` | 178,598,026 | **REPORTER_DEA_NO → BUYER_DEA_NO** (distributor → pharmacy) with drug, QUANTITY, TOTAL_MME, TRANSACTION_DATE, and city/state/zip/county on **both** ends. Covers 2006–2012 only. |
| `LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__UK_COMPANIES_HOUSE_PSC` | 7,000,000 | **person/entity → COMPANY_NUMBER**, typed by NATURES_OF_CONTROL, with **NOTIFIED_ON and CEASED_ON** — a directed ownership graph that turns on and off over time |
| `LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FRS_PROGRAM_LINKS` | 4,406,498 | REGISTRY_ID ↔ PGM_SYS_ID/PGM_SYS_ACRNM — one facility to all the regulatory programs it sits in |
| `LIBRARY_RAW.LANDING.FED_CMS_FACILITY_AFFILIATION` | 2,260,193 | **NPI → CCN** (clinician → facility), both hard IDs, plus IND_PAC_ID and FACILITY_TYPE |
| `LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS_FULL` | 20,000,000 (raw base) | AWARDING_AGENCY → RECIPIENT_UEI, plus **RECIPIENT_PARENT_UEI → RECIPIENT_UEI**, PARENT_AWARD_ID_PIID, FEDERAL_ACTION_OBLIGATION, ACTION_DATE, recipient county FIPS **and** place-of-performance county FIPS. 598 columns. |
| `LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_ASSISTANCE_FULL` | 19,902,879 | same shape for grants/assistance |
| `LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_HIERARCHY` | 678,363 | TSN → PARENT_TSN with HIERARCHY_LEVEL and CHILDREN_COUNT — a genuine directed tree, but it is species taxonomy, not harm |

Caution on `FED_USASPENDING_CONTRACTS_FULL`: 20,000,000 is a suspiciously round
row count, and the Aug-10 mart-defect review confirmed 18 tables whose round
counts are load caps. Treat it as capped until checked.

## 7. Co-location substrate (shared address / shared name)

- **1,238** clean tables carry both an address-ish and a name-ish column.
- **262** clean tables carry person-name columns; **116** carry person + address.
- Biggest: ARCOS 178.6M, ENTITY_GOLDEN 33.3M, USAspending contracts 20M,
  USAspending assistance 19.9M, CMS Open Payments 15.4M,
  `HEALTH__FED_CMS_NPPES` 9.6M, UK PSC 7M, UK Companies House 5.7M,
  `ENVIRONMENT__FED_EPA_FRS_FACILITIES` 5.3M.

## 8. The shared time axis is real and already built

`LIBRARY_MARTS.TIMELINE` holds **436 views**. Column counts across them:
`RIPPLE_SOURCE` 435, `RIPPLE_GRAIN` 435, `RIPPLE_CLOCK` 435, `RIPPLE_TS` 403,
`RIPPLE_DAY` 32.

`reports/time_index/TRENDABLE.csv` measures **953 clock columns across 403
tables**: 707 at day grain, 217 year, 15 quarter, 14 month; confidence 517 high /
405 medium / 31 low; meaning 305 happened, 244 reported, 158 span_end, 143
decided, 103 span_start.

`reports/time_index/TREND_FINDINGS.md` headline, which constrains every
time-based technique: **371 series pulled, 307 scored, and most of the
"weirdness" is about how the data was collected, not what happened in the
world.** It also corrects ARCOS: the span is 2006–2012, not 2006–2026 — the old
end date came from Ripple's own download stamp.

## 9. Multi-variable substrate (what dimension reduction has to work with)

261 tables have ≥8 numeric columns, 81 have ≥20, and only **30 have ≥50** — of
which roughly 13 are distinct tables rather than duplicate views/staging copies:

| rows | numeric / total cols | table |
|---:|---|---|
| 503,917 | 62 / 212 | LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_QUALITY_PAYMENT_PROGRAM_EXPERIENCE |
| 381,228 | 52 / 97 | LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT... |
| 44,429 | 204 / 473 | LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER |
| 41,802 | 86 / 127 | LIBRARY_MARTS.LABOR.LABOR__FED_DOL_EBSA_FORM5500_SCHEDULE_SB |
| 14,700 | 61 / 97 | LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME |
| 11,974 | 65 / 141 | LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_EGRID_PLANT_2022 |
| 7,557 | 67 / 142 | LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_DIALYSIS |
| 6,273 | 52 / 66 | LIBRARY_MARTS.EDUCATION.EDUCATION__FED_ED_COLLEGE_SCORECARD_INSTITUTION |
| 6,103 | 107 / 125 | LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HCRIS |
| 4,336 | 244 / 249 | LIBRARY_MARTS.FINANCE.FINANCE__FED_NCUA_CALL_REPORTS_FS220 |
| 1,004 | 112 / 120 | LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_NET_METERING |

Note the inversion: the tables with the most numeric columns are the **smallest**
tables. Nothing in the warehouse is simultaneously wide-numeric and huge.

## 10. Scale

- 252 objects have ≥1M rows; **79 have ≥10M**.
- 726 have ≥50 columns; 108 have ≥150.
- Widest object in the warehouse: `LIBRARY_RAW.LANDING.FED_ED_COLLEGE_SCORECARD_INSTITUTION` at **3,311 columns** over 6,273 rows.
