# Wonder to table map, 2026-09-09

125 wonders from `reports/wonder_list_2026-09-09.md`, each mapped to the tables and columns it needs.
Metadata only: THE_CATALOG.csv, mart_table_catalog, topo map, traps.md. Nothing was queried.
Five agents, one arc each. Their blocks are below, verbatim.

## Scorecard

| arc | join found | no join | of 25 |
|---|---|---|---|
| Place | 17 | 8 | 25 |
| Body | 18 | 7 | 25 |
| Money | 20 | 5 | 25 |
| Power | 21 | 4 | 25 |
| Work and things | 18 | 7 | 25 |
| **all** | **94** | **31** | **125** |

Of the 94 joins, roughly 25 are name-only or state-grain. Real-id joins: about 69.

## Gap ledger, ranked by wonders unlocked

One fix, many wonders. Same gap hit by several arcs independently.

| rank | gap | fix | wonders unlocked | kind |
|---|---|---|---|---|
| 1 | ~~no ZIP-to-county crosswalk anywhere~~ WRONG, verified 2026-09-09: LIBRARY_MARTS.CORE.XWALK_ZCTA_COUNTY exists, 46,960 rows, ZCTA5 to COUNTY_FIPS, vintage 2020. The five agents searched THE_CATALOG.csv, which does not list CORE. | none; use it | 1,6,8,10,21,27,34,47,60,67,75,103 | already there |
| 2 | full contracts table (R2) dropped county FIPS, agency code, entity type | reload R2 with the columns; 93M rows, 9.7 GB, so this is a phase-2 size job, not a column add | 55,70,80,90,92,93,103 | reload a table |
| 3 | Part B, Part D, inpatient, outpatient are one data year | land prior-year CMS PUFs DY2013-2023 | 23,38,40,44,47,48 | land a table |
| 4 | HMDA full is 2015-2017 only; 2018+ are samples | land HMDA LAR 2018-2024 state by year | 1,4,5,56,59,71 | land a table |
| 5 | ~~FEMA IA mart is a 12% load~~ WRONG, verified 2026-09-09: mart holds 26,250,920 rows, same as raw. The 12% note was stale. Disaster declarations table is still missing. | land DisasterDeclarationsSummaries only | 4,55,67,122 | land a table |
| 6 | plant list is one vintage; retired units absent | land EIA-860 prior years, eGRID 2019-2023 | 13,23,25,85,124 | land a table |
| 7 | SDWA county is a name, no FIPS | add FIPS via REF__DIM_GEOGRAPHY | 2,11,14,16,25 | add a column |
| 8 | NPPES is a snapshot; no doctor history | land NPPES monthly deactivation files | 6,8,29,34,37 | land a table |
| 9 | no nursing home ownership file at owner grain | land CMS SNF ownership file | 28,97,113 | land a table |
| 10 | ARCOS county is a name; mart unprofiled | add FIPS column to ARCOS mart | 26,41,42 | add a column |
| 11 | EOIR has no judge or decision column | land tblDecision, tblJudge | 76,91 | land a table |
| 12 | no wage-enforcement table | land DOL WHD enforcement | 102,105 | land a table |
| 13 | no CUSIP-to-CIK, no CIK-to-UEI bridge | land SEC CUSIP list; land SAM entity registration | 51,62 | land a table |
| 14 | LDA missing 2011-2019 and 2022+ | land the missing LDA years | 82,87 | land a table |
| 15 | EAVS has no year column | add YEAR; land multi-year with codebook | 22,83 | add a column |
| 16 | no CCN-to-EIN bridge | land 990 Schedule H CCN or Hospital Compare EIN | 36,123 | land a table |
| 17 | no EIN on assistance awards | add RECIPIENT_EIN to assistance loader | 68,73 | add a column |

Fixes 1, 2, 7, 10, 15, 17 are column adds or one small file each. Together they unlock about 30 wonders.

## Dead in public data, say so in the wonder

| # | why |
|---|---|
| 43 | FAERS has no state or prescriber |
| 57, 64 | lender-to-facility financing edge is not published at facility grain |
| 69 | 501(c)(3) cannot donate; reframe to hospital PAC and employee employer |
| 108 | NOAA AIS is US waters only; foreign port calls unobservable |
| 120, 121 | no gap; join through program links, check masked ZIP first |

## Traps that bite

See each block's `trap:` line. Repeat offenders: HMDA historic is originations only; FEC itoth memo double-count; Part B suppressed subset; portal 10k cap; INGESTED_AT epoch micros.

---


# Arc 1

# Arc 1 — PLACE — wonders #1–#25 mapped to catalog tables (metadata only, 2026-09-09)

Sources: reports/THE_CATALOG.csv, reports/mart_table_catalog_2026-09-08.csv, reports/warehouse_topo_map_2026-09-05.md, .claude/traps.md. No warehouse queries.
Shorthand: M. = LIBRARY_MARTS. L. = LIBRARY_RAW.LANDING.

### #1 — Flood-aid zips denied mortgages more the next year
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | M.HOUSING.HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS | DISASTER_NUMBER, FLOOD_DAMAGE, IHP_AMOUNT, HA_AMOUNT | DECLARATION_DATE | DAMAGED_ZIP_CODE, FIPS |
| B | M.HOUSING.HOUSING__FED_CFPB_HMDA_HISTORIC | ACTION_TAKEN, LOAN_PURPOSE, DENIAL_REASON_1 | AS_OF_YEAR | STATE_CODE + COUNTY_CODE (no ZIP) |
join: county — FEMA FIPS ↔ HMDA STATE_CODE||COUNTY_CODE. ZIP: none found (HMDA has tract, not ZIP).
gap: hub drops from ZIP to county; FEMA mart is a 12% truncated sample (3.08M of 25.9M); HMDA post-2017 marts are DC-only / 17K samples, so HISTORIC (to 2017) is the only usable side B.
trap: FEMA IA FIPS unpadded for states 01-09; HMDA_HISTORIC STATE_CODE/COUNTY_CODE unpadded, year only, no date; HMDA_HISTORIC has two file families — group by ACTION_TAKEN first.

### #2 — 1930s redline maps predict today's water violations
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | M.HOUSING.HOUSING__FED_MAPPING_INEQUALITY | HOLC_GRADE, HOLC_GRADE_RANK, GEOMETRY, LAT, LON | YEAR_MAPPED | FIPS, CITY, STATE |
| B | M.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT | PWSID, VIOLATION_CODE, IS_HEALTH_BASED_IND | NON_COMPL_PER_BEGIN_DATE | PWSID |
| B2 | M.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_GEOGRAPHIC_AREAS | PWSID, AREA_TYPE_CODE | LAST_REPORTED_DATE | COUNTY_SERVED, ZIP_CODE_SERVED, STATE_SERVED |
join: PWSID (B↔B2); then county — A.FIPS ↔ B2.COUNTY_SERVED (name) via M.REFERENCE.REF__DIM_GEOGRAPHY COUNTY_NAME+STATE_ABBR → FIPS_CODE.
gap: SDWA gives county NAME/ZIP, not FIPS; tract-level match needs L.FED_MAPPING_INEQUALITY GeoJSON, not the mart.
trap: MAPPING_INEQUALITY mart is one polygon per (city, grade), 1,155 of 10,154 rows — 11% of the map; county names without " COUNTY" suffix leak past filters.

### #3 — PE landlords and CFPB complaints rise together
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | NOT FOUND in catalog | — | — | — |
| B | M.CONSUMER_PROTECTION.CONSUMER_PROTECTION__FED_CFPB_COMPLAINTS | PRODUCT, SUB_PRODUCT, ISSUE, COMPANY | RECEIVED_YEAR | ZIP_CODE, STATE |
join: none found
gap: no landlord/property-owner table; searched LANDLORD, EVICT, PARCEL, PROPERTY, ASSESSOR, HUD_MF (MF_FIRM_COMMITMENTS names the LENDER, not the owner), HUD_ASSISTED_HOUSING (program units, no owner). CFPB side is fine.
trap: none

### #4 — Counties aided three times and rebuilt again
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | M.HOUSING.HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS | DISASTER_NUMBER (count distinct per FIPS), IHP_AMOUNT, REPAIR_AMOUNT, DESTROYED | DECLARATION_DATE | FIPS |
| B | M.HOUSING.HOUSING__FED_CFPB_HMDA_HISTORIC | LOAN_PURPOSE (home improvement), ACTION_TAKEN, LOAN_AMOUNT_000S | AS_OF_YEAR | STATE_CODE + COUNTY_CODE |
join: FIPS ↔ STATE_CODE||COUNTY_CODE (pad both)
gap: no disaster-declarations table (searched DISASTER, DECLARATION — only IA registrations); FEMA mart is a 12% truncated sample, so "three times" is a floor.
trap: FEMA IA FIPS unpadded ('1097' and '01097' both exist, 69,662 null); HMDA_HISTORIC codes unpadded.

### #5 — Lenders pull out of a county after the first big storm
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | M.ENVIRONMENT.ENVIRONMENT__FED_NOAA_STORM_EVENTS | EVENT_TYPE, DAMAGE_PROPERTY, DEATHS_DIRECT, CZ_TYPE | YEAR | STATE_FIPS + CZ_FIPS (CZ_TYPE='C') |
| B | M.HOUSING.HOUSING__FED_CFPB_HMDA_HISTORIC | RESPONDENT_ID, AGENCY_CODE, ACTION_TAKEN | AS_OF_YEAR | STATE_CODE + COUNTY_CODE |
join: STATE_FIPS||CZ_FIPS ↔ STATE_CODE||COUNTY_CODE (county rows only)
gap: DAMAGE_PROPERTY is TEXT with K/M suffix — parse; CZ_TYPE='Z' rows are forecast zones, not counties, and drop out.
trap: HMDA_HISTORIC unpadded codes, year only; CZ_NAME bare county names leak past suffix filters.

### #6 — Counties that lost doctors, banks, factories same decade
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | M.HEALTH.HEALTH__FED_CMS_NPPES | NPI, ENTITY_TYPE_CODE, HEALTHCARE_PROVIDER_TAXONOMY_CODE_1 | PROVIDER_ENUMERATION_DATE, NPI_DEACTIVATION_DATE | PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_POSTAL_CODE (ZIP, no county) |
| B | M.FINANCE.FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS | FDIC_CERT, BRANCH_NAME | SURVEY_YEAR | BRANCH_STATE_COUNTY_FIPS |
| C | M.ECONOMICS.ECONOMICS__FED_BLS_QCEW | INDUSTRY_CODE (31-33), ANNUAL_AVG_ESTABLISHMENTS, ANNUAL_AVG_EMPLOYMENT | YEAR | AREA_FIPS |
join: county FIPS (B↔C); A needs ZIP→county — none found
gap: NPPES has no county and no ZIP→county crosswalk in catalog (CENSUS_CB_ZCTA has GEOID20 only); NPPES is a snapshot, doctor count by year must be rebuilt from enumeration/deactivation dates.
trap: NPPES mart blanks every deactivated NPI (346,179 rows: ENTITY_TYPE_CODE '', dates NULL) — the lost doctors are the rows with no attributes.

### #7 — Single P.O. box hosts clinics, PACs, contractors
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | M.HEALTH.HEALTH__FED_CMS_NPPES | PROVIDER_FIRST_LINE_BUSINESS_MAILING_ADDRESS, PROVIDER_BUSINESS_MAILING_ADDRESS_CITY_NAME, PROVIDER_BUSINESS_MAILING_ADDRESS_STATE_NAME, PROVIDER_ORGANIZATION_NAME_LEGAL_BUSINESS_NAME | PROVIDER_ENUMERATION_DATE | PROVIDER_BUSINESS_MAILING_ADDRESS_POSTAL_CODE |
| B | M.FINANCE.FINANCE__FED_FEC_COMMITTEES | CMTE_ID, CMTE_NM, CMTE_ST1, CMTE_CITY, CMTE_ST, CMTE_TP | none (cycle only in FINANCE__FED_FEC_BULK_COMMITTEES.CYCLE) | CMTE_ZIP |
| C | M.ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS_FULL | RECIPIENT_NAME, RECIPIENT_UEI, RECIPIENT_ADDRESS_LINE_1, RECIPIENT_CITY_NAME | ACTION_DATE_FISCAL_YEAR | RECIPIENT_ZIP_4_CODE |
join: normalized address line + ZIP5 (string match, no shared key)
gap: no normalized-address key exists in any mart; NET picture, so year is optional, but FEC_COMMITTEES has none.
trap: FEC committee IDs repeat across cycles (count entities, never pairs); CONTRACTS_FULL is a 20M-row cap — use L.FED_USASPENDING_CONTRACTS_FULL_R2 (93M, uppercase columns).

### #8 — Counties with one doctor per thousand and shrinking
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | M.HEALTH.HEALTH__FED_CMS_NPPES | NPI, ENTITY_TYPE_CODE='1', HEALTHCARE_PROVIDER_TAXONOMY_CODE_1 | PROVIDER_ENUMERATION_DATE, NPI_DEACTIVATION_DATE | PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_POSTAL_CODE |
| B | M.HEALTH.HEALTH__FED_CDC_DRUG_POISONING_COUNTY | POPULATION | YEAR | FIPS |
| alt A | M.HEALTH.HEALTH__FED_HRSA_HPSA_PRIMARY_CARE | PROVIDER_RATIO_GOAL, DESIGNATION_TYPE, HPSA_STATUS_CODE | DESIGNATION_DATE, WITHDRAWN_DATE | COMMON_STATE_COUNTY_FIPS_CODE |
join: FIPS (alt A↔B); NPPES ZIP→county none found
gap: NPPES has no county; only county-year population in catalog is the CDC drug-poisoning table's POPULATION column.
trap: NPPES deactivated rows blanked; HPSA ratio text columns were zeroed by a name-keyed numeric cast (2026-09-07) — check PROVIDER_RATIO_GOAL values before trusting.

### #9 — Rural clinics close where the only bank branch closed
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | M.HEALTH.HEALTH__FED_CMS_POS_OTHER | CCN, PRVDR_CTGRY_CD, FAC_NAME, CBSA_URBN_RRL_IND | TRMNTN_EXPRTN_DT | FIPS_STATE_CD + FIPS_CNTY_CD |
| B | M.FINANCE.FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS | FDIC_CERT, BRANCH_NAME (count per county-year; closure = row disappears next SURVEY_YEAR) | SURVEY_YEAR | BRANCH_STATE_COUNTY_FIPS |
join: FIPS_STATE_CD||lpad(FIPS_CNTY_CD,3) ↔ BRANCH_STATE_COUNTY_FIPS
gap: FIPS_CNTY_CD is NUMBER (unpadded); RURAL_HEALTH_CLINIC_ENROLLMENTS has no county and no dates, so POS is the only clinic side.
trap: POS_OTHER keeps only the latest snapshot per CCN; CHOW_SW '' on all rows.

### #10 — Rural counties send most to DC, get least back
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | M.FINANCE.FINANCE__FED_IRS_SOI | TOTAL_TAX, AGI, N_RETURNS, AGI_STUB | TAX_YEAR | ZIP_CODE, STATE_FIPS |
| B | M.ECONOMICS.ECONOMICS__FED_USASPENDING_ASSISTANCE_FULL | TOTAL_OBLIGATED_AMOUNT, CFDA_NUMBER | ACTION_DATE_FISCAL_YEAR | PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE |
| B2 | M.ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS_FULL | TOTAL_DOLLARS_OBLIGATED | ACTION_DATE_FISCAL_YEAR | PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE |
join: none found — SOI is ZIP, spending is county FIPS; no ZIP→county crosswalk in catalog
gap: need a ZIP↔county crosswalk table; rural flag has to come from POS_OTHER.CBSA_URBN_RRL_IND or Part B RNDRNG_PRVDR_RUCA, neither county-native. TOTAL_TAX is FLOAT but AGI and N_RETURNS are TEXT in SOI.
trap: ASSISTANCE_FULL capped 1M rows/year (every FY total is a floor); CONTRACTS_FULL 20M cap — use R2; CURRENT_TOTAL_VALUE_OF_AWARD is not spend, sum obligations.

### #11 — Rural water systems violate more per capita than urban
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | M.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT | VIOLATION_ID, IS_HEALTH_BASED_IND, VIOLATION_CATEGORY_CODE | NON_COMPL_PER_BEGIN_DATE | PWSID |
| B | M.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS | POPULATION_SERVED_COUNT, PWS_TYPE_CODE, OWNER_TYPE_CODE, PWS_ACTIVITY_CODE | SUBMISSIONYEARQUARTER | PWSID, STATE_CODE, ZIP_CODE |
| B2 | M.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_GEOGRAPHIC_AREAS | AREA_TYPE_CODE | LAST_REPORTED_DATE | PWSID → COUNTY_SERVED, STATE_SERVED |
join: PWSID; county name → FIPS via M.REFERENCE.REF__DIM_GEOGRAPHY (COUNTY_NAME, STATE_ABBR → FIPS_CODE)
gap: no rural/urban flag on any SDWA table; borrow from POS_OTHER.CBSA_URBN_RRL_IND by county, or use POPULATION_SERVED_COUNT bands as the proxy.
trap: county names without " COUNTY" suffix leak past filters.

### #12 — Mine closed, overdoses rose within three years
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | M.LABOR.LABOR__FED_MSHA_MINES | MINE_ID, CURRENT_MINE_STATUS, COAL_METAL_IND, NO_EMPLOYEES | CURRENT_STATUS_DT | STATE + FIPS_CNTY_CD |
| B | M.HEALTH.HEALTH__FED_CDC_DRUG_POISONING_COUNTY | ESTIMATED_AGE_ADJUSTED_DEATH_RATE_11_CATEGORIES_IN_RANGES, POPULATION | YEAR | FIPS |
| alt B | M.HEALTH.HEALTH__FED_CDC_INJURY_VIOLENCE_COUNTY | INTENT (overdose), RATE, RATE_M, COUNT_SUP | PERIOD / TTM_DATE_RANGE (2019-2024) | GEOID |
join: M.REFERENCE.REF__DIM_STATE STATE_ABBR→STATE_FIPS, then STATE_FIPS||lpad(FIPS_CNTY_CD,3) ↔ FIPS / GEOID
gap: MSHA holds only CURRENT status and its date — one closure per mine, no history; CDC drug-poisoning rate is a binned range, not a number.
trap: CDC injury county RATE_M is a text flag, RATE -999 is a sentinel; overdose there is 2019-2024 only.

### #13 — Counties host most plants, get least federal money
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | M.ENVIRONMENT.ENVIRONMENT__FED_EPA_EGRID_PLANT_2022 | DOE_EIA_ORIS_PLANT_OR_FACILITY_CODE, PLANT_NAMEPLATE_CAPACITY_MW, PLANT_PRIMARY_FUEL_CATEGORY, PLANT_ANNUAL_NOX_EMISSIONS_TONS | DATA_YEAR (2022 only) | PLANT_FIPS_STATE_CODE + PLANT_FIPS_COUNTY_CODE |
| B | M.ECONOMICS.ECONOMICS__FED_USASPENDING_ASSISTANCE_FULL | TOTAL_OBLIGATED_AMOUNT | ACTION_DATE_FISCAL_YEAR | PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE |
join: county FIPS (concat state+county on A)
gap: EGRID is one year; ENERGY__FED_EIA860_2_PLANT has COUNTY as a name and no year. Per-capita needs POPULATION from HEALTH__FED_CDC_DRUG_POISONING_COUNTY.
trap: ASSISTANCE_FULL 1M/year cap — totals are floors; PLANT_NAMEPLATE_CAPACITY_MW is TEXT in the mart.

### #14 — Water violations rise where a hospital just closed
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | M.HEALTH.HEALTH__FED_CMS_POS_OTHER | CCN, PRVDR_CTGRY_CD (hospital), FAC_NAME, BED_CNT | TRMNTN_EXPRTN_DT | FIPS_STATE_CD + FIPS_CNTY_CD |
| B | M.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT + ENVIRONMENT__FED_EPA_SDWA_SDWA_GEOGRAPHIC_AREAS | VIOLATION_ID, IS_HEALTH_BASED_IND; COUNTY_SERVED, STATE_SERVED | NON_COMPL_PER_BEGIN_DATE | PWSID → COUNTY_SERVED |
join: county — POS FIPS ↔ REF__DIM_GEOGRAPHY(COUNTY_NAME, STATE_ABBR) ↔ COUNTY_SERVED
gap: SDWA county is a name; POS keeps latest snapshot only, so closures are those with a termination date still on file.
trap: POS_OTHER latest-snapshot-only; FIPS_CNTY_CD NUMBER unpadded.

### #15 — Unsafe dams upstream of nursing homes or schools
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | M.ENVIRONMENT.ENVIRONMENT__FED_NID_DAMS | NID_ID, HAZARD_POTENTIAL, CONDITION_ASSESSMENT, OWNER_TYPES | CONDITION_ASSESSMENT_DATE, LAST_INSPECTION_DATE | LATITUDE, LONGITUDE, STATE, COUNTY |
| B | M.HEALTH.HEALTH__FED_CMS_NURSING_HOME | CMS_CERTIFICATION_NUMBER_CCN, NUMBER_OF_CERTIFIED_BEDS | none (snapshot) | LATITUDE, LONGITUDE, COUNTY_FIPS |
| B2 (schools) | NOT FOUND in catalog | — | — | — |
join: coordinate distance (no shared key)
gap: no K-12 school table (searched SCHOOL, NCES, K-12 — only CIP codes and CourtListener judge schools); "upstream" needs flow direction — USGS_WBD_HUC8 mart has no geometry; nursing home side has no year; DHS_HIFLD is a 500-row sample.
trap: none

### #16 — Fracking counties see water violations climb after boom
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | M.ENVIRONMENT.ENVIRONMENT__FED_FRACFOCUS_DISCLOSURE_LIST | DISCLOSURE_ID, API_NUMBER, OPERATOR_NAME, TOTAL_BASE_WATER_VOLUME | JOB_START_DATE | STATE_NAME + COUNTY_NAME, LATITUDE, LONGITUDE |
| B | M.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT + ENVIRONMENT__FED_EPA_SDWA_SDWA_GEOGRAPHIC_AREAS | VIOLATION_ID, CONTAMINANT_CODE, IS_HEALTH_BASED_IND; COUNTY_SERVED, STATE_SERVED | NON_COMPL_PER_BEGIN_DATE | PWSID → COUNTY_SERVED |
join: county name + state, both sides (normalize through REF__DIM_GEOGRAPHY to FIPS)
gap: neither side carries FIPS; STATE_NAME (full) vs STATE_SERVED (abbr) — REF__DIM_STATE bridges.
trap: county names without " COUNTY" suffix leak past filters.

### #17 — Discharge permits upstream of poorest water systems
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | M.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_ICIS_FACILITIES | NPDES_ID, FACILITY_NAME, FACILITY_TYPE_CODE | none (permit snapshot) | GEOCODE_LATITUDE, GEOCODE_LONGITUDE, COUNTY_CODE, STATE_CODE |
| B | M.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS | PWSID, PRIMARY_SOURCE_CODE (surface water), POPULATION_SERVED_COUNT | SUBMISSIONYEARQUARTER | ZIP_CODE, STATE_CODE (no coords) |
| C (poorest) | M.FINANCE.FINANCE__FED_IRS_SOI | AGI, N_RETURNS, AGI_STUB | TAX_YEAR | ZIP_CODE |
join: B.ZIP_CODE ↔ C.ZIP_CODE; A↔B by NPDES coords vs PWS ZIP — no shared key
gap: PWS side has no coordinates (SDWA_FACILITIES lists intakes but no lat/lon); "upstream" needs a flow network — WQP_MONITORING_STATIONS has HUC_EIGHT_DIGIT_CODE but NPDES/SDWA marts carry no HUC; NPDES facilities has no year.
trap: none

### #18 — Water systems violate yearly, never enforced
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | M.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT | VIOLATION_ID, IS_HEALTH_BASED_IND, VIOLATION_STATUS, ENFORCEMENT_ID (null = never), ENFORCEMENT_ACTION_TYPE_CODE, ENF_ACTION_CATEGORY | NON_COMPL_PER_BEGIN_DATE, ENFORCEMENT_DATE | PWSID |
| B | M.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS | PWS_NAME, POPULATION_SERVED_COUNT, OWNER_TYPE_CODE, PRIMACY_AGENCY_CODE | SUBMISSIONYEARQUARTER | PWSID, STATE_CODE |
join: PWSID
gap: none
trap: none

### #19 — Highway deaths rise where trauma centers closed
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | NOT FOUND in catalog (FARS) | — | — | — |
| B | NOT FOUND in catalog (trauma center list) | — | — | — |
join: none found
gap: searched FARS, FATAL, CRASH, HIGHWAY, TRAUMA — CONSUMER_SAFETY__FED_NHTSA_COMPLAINTS has DEATHS per complaint but state only, no county/year series; POS_OTHER has HEAD_TRMA_BED_CNT (beds) but no trauma-level designation; DHS_HIFLD is a 500-row sample of one layer. Land FARS accident file (ST_CASE, COUNTY, YEAR) and a trauma-center list.
trap: NHTSA landing is headerless (five-tables trap).

### #20 — For-profit colleges cluster near bases and vets
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | M.EDUCATION.EDUCATION__FED_ED_COLLEGE_SCORECARD_INSTITUTION | UNITID, INSTITUTION_NAME, CONTROL_CODE (for-profit), CURRENTLY_OPERATING, PREDOMINANT_DEGREE_CODE | none (single vintage) | ZIP, STATE_FIPS, LATITUDE, LONGITUDE |
| B | NOT FOUND in catalog (military installations) | — | — | — |
| B2 (vets) | M.HEALTH.HEALTH__FED_VA_SUICIDE_STATE | veteran counts if present | YEAR | state only |
join: none found
gap: searched MILITARY, BASE, INSTALLATION, DOD — nothing but the 500-row HIFLD sample; no veteran population by ZIP or county; scorecard mart has no year column (full 3,311-col file stays in landing).
trap: none

### #21 — Counties lost only hospital and community college
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | M.HEALTH.HEALTH__FED_CMS_POS_OTHER | CCN, PRVDR_CTGRY_CD (hospital), count per county | TRMNTN_EXPRTN_DT | FIPS_STATE_CD + FIPS_CNTY_CD |
| B | M.EDUCATION.EDUCATION__FED_ED_COLLEGE_SCORECARD_INSTITUTION | UNITID, CONTROL_CODE, PREDOMINANT_DEGREE_CODE (2 = associate), CURRENTLY_OPERATING | none | ZIP, STATE_FIPS, LATITUDE, LONGITUDE (no county) |
join: none found — scorecard has ZIP/coords, POS has county FIPS; no ZIP→county crosswalk
gap: scorecard mart has no closure date or year; no county column; needs the LANDING wide file or IPEDS closure history (not landed).
trap: POS_OTHER latest snapshot only.

### #22 — Counties run elections on smallest budget per voter
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | M.POLITICS.POLITICS__FED_EAC_EAVS | A1A (registered voters), JURISDICTION_NAME | none found in mart | FIPSCODE, STATE_ABBR |
| B | NOT FOUND in catalog (election budget / spend per jurisdiction) | — | — | — |
join: none found
gap: EAVS carries no budget question and the mart has no YEAR column (searched YEAR, ELECTION, DATE); no local-government finance table (searched BUDGET, EXPEND, FINANCE). Would need Census of Governments finance or state election-cost files.
trap: EAVS has no codebook landed; -99/-88 sentinels; Wisconsin reports by municipality (1,851 rows) and drops out of a county join.

### #23 — Where coal plants closed, respiratory claims fell
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | M.ENERGY.ENERGY__FED_EIA860_3_1_GENERATOR | PLANT_CODE, GENERATOR_ID, ENERGY_SOURCE_1 (coal), STATUS, NAMEPLATE_CAPACITY_MW | OPERATING_YEAR, PLANNED_RETIREMENT_YEAR | STATE + COUNTY (name) |
| A2 | M.ENVIRONMENT.ENVIRONMENT__FED_EPA_EGRID_PLANT_2022 | DOE_EIA_ORIS_PLANT_OR_FACILITY_CODE, PLANT_ANNUAL_COAL_NET_GENERATION_MWH | DATA_YEAR | PLANT_FIPS_STATE_CODE + PLANT_FIPS_COUNTY_CODE |
| B | M.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER | BENE_CC_PH_COPD_V2_PCT, BENE_CC_PH_ASTHMA_V2_PCT, TOT_BENES | none (DY2024 only) | RNDRNG_PRVDR_ZIP5, RNDRNG_PRVDR_STATE_FIPS |
join: A.PLANT_CODE ↔ A2.DOE_EIA_ORIS_PLANT_OR_FACILITY_CODE (gives FIPS); A2 county FIPS ↔ B ZIP: none found
gap: no respiratory claims series by county-year — Part B mart is one data year; CDC_WONDER has ICD_CHAPTER x YEAR but no place; EIA-860 mart is the 2024 file so coal units retired before then are absent (retired-generator schedule not landed).
trap: Part B service table is a suppressed subset (under-11 rows deleted); carbon-date per-NPI CMS files by newest enumeration.

### #24 — Plants run dirtiest on hottest days
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | L.FED_EPA_CAMPD_EMISSIONS_DAILY (topo map names it; 16.5M rows; columns not in THE_CATALOG) | daily SO2/NOx/CO2, heat input (unverified) | daily date (unverified) | ORIS/facility id (unverified) |
| B | NOT FOUND in catalog (daily temperature by station/county) | — | — | — |
join: none found
gap: no daily weather table — ENVIRONMENT__FED_NOAA_WEATHER_API is alerts/stations with a TEMPERATURE snapshot, STORM_EVENTS is events only; CAMPD is landing-only with no mart and no catalog columns. Land NOAA GHCN-Daily and mart CAMPD.
trap: CAMPD _INGESTED_AT is epoch microseconds stamped as seconds — year() throws.

### #25 — Plant-county water systems violate more after hot summer
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | M.ENVIRONMENT.ENVIRONMENT__FED_EPA_EGRID_PLANT_2022 | DOE_EIA_ORIS_PLANT_OR_FACILITY_CODE, PLANT_PRIMARY_FUEL_CATEGORY | DATA_YEAR (2022 only) | PLANT_FIPS_STATE_CODE + PLANT_FIPS_COUNTY_CODE |
| B | M.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT + ENVIRONMENT__FED_EPA_SDWA_SDWA_GEOGRAPHIC_AREAS | VIOLATION_ID, IS_HEALTH_BASED_IND; COUNTY_SERVED, STATE_SERVED | NON_COMPL_PER_BEGIN_DATE | PWSID → COUNTY_SERVED |
| C (hot summer proxy) | M.ENVIRONMENT.ENVIRONMENT__FED_NOAA_STORM_EVENTS | EVENT_TYPE in ('Heat','Excessive Heat'), count per county-summer | YEAR, BEGIN_YEARMONTH | STATE_FIPS + CZ_FIPS |
join: county FIPS (A↔C); B county name via REF__DIM_GEOGRAPHY
gap: no temperature series — heat EVENTS are a proxy and mostly CZ_TYPE='Z' zones, not counties; plant list is a single year.
trap: county names without " COUNTY" suffix leak; SDWA county is a name not FIPS.

## Gaps summary
| # | gap | fix (land a table / add a column / parse a field) |
|---|---|---|
| 1,4,5 | HMDA usable only through 2017 (HISTORIC); post-2017 marts are DC-only/17K samples; FEMA IA mart is a 12% truncated load | land full HMDA state x year loop; finish FEMA IA full reload |
| 1,6,8,10,21 | no ZIP↔county crosswalk; NPPES, IRS SOI, College Scorecard are ZIP-only, spending/POS/CDC are county | land HUD USPS ZIP-county crosswalk (add FIPS column to CENSUS_CB_ZCTA) |
| 2,11,14,16,25 | SDWA geography is COUNTY_SERVED as a name, no FIPS | add a FIPS column to SDWA_GEOGRAPHIC_AREAS via REF__DIM_GEOGRAPHY |
| 3 | no landlord / property-owner table | land county assessor or HUD multifamily owner file |
| 4 | no disaster-declarations table | land OpenFEMA DisasterDeclarationsSummaries (FIPS, declaration date) |
| 5 | STORM_EVENTS DAMAGE_PROPERTY is text with K/M suffix | parse a numeric column |
| 6,8 | NPPES is a snapshot, doctor counts by year must be rebuilt from enumeration/deactivation dates; deactivated rows blanked | land NPPES monthly deactivation file; keep landing attributes |
| 7 | no normalized address key across NPPES / FEC / USAspending | add a normalized address+ZIP5 column to each |
| 9,14,21 | POS_OTHER keeps latest snapshot only — closure history lost | land historic POS quarterly files |
| 12 | MSHA_MINES holds current status only; CDC county overdose rate is a binned range | land MSHA mine status history; land CDC WONDER county overdose counts |
| 13,23,25 | plant list is one year (EGRID 2022 / EIA-860 2024); retired coal units absent | land EIA-860 retired-generator schedule and multi-year EGRID |
| 15 | no K-12 school table; no watershed flow direction | land NCES CCD school file; land NHDPlus flowlines or HUC12 geometry |
| 17 | PWS intakes have no coordinates; NPDES has no HUC | land SDWIS source-water locations; add HUC8 to NPDES facilities |
| 19 | no FARS, no trauma-center list | land FARS accident file; land ACS trauma center registry |
| 20 | no military installation list; no veteran population by ZIP/county | land DoD installations; land VA vet population (VetPop) by county |
| 22 | no election budget data; EAVS mart has no year column | land Census of Governments finance; add YEAR to EAVS |
| 23 | no county-year respiratory claims series (Part B is DY2024 only) | land Part B by-provider prior years (DY2013-2023) |
| 24,25 | no daily temperature series; CAMPD daily is landing-only, uncataloged | land NOAA GHCN-Daily; mart FED_EPA_CAMPD_EMISSIONS_DAILY |

# Arc 2

# Arc 2 (BODY) — wonders #26–#50 mapped to catalog tables. Metadata only, nothing queried. 2026-09-09.

Conventions: M = LIBRARY_MARTS, R = LIBRARY_RAW.LANDING. County-name→FIPS bridge = M.REFERENCE.REF__DIM_GEOGRAPHY (COUNTY_NAME, STATE_ABBR, FIPS_CODE). No ZIP→county crosswalk exists in either catalog (only REFERENCE__CENSUS_CB_ZCTA GEOMETRY, spatial).

### #26 — 2010 pill counties become 2024 overdose counties, or not
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_RAW.LANDING.FED_DEA_ARCOS_FULL | BUYER_COUNTY, BUYER_STATE, DOSAGE_UNIT, MME_CONVERSION_FACTOR, TRANSACTION_DATE | TRANSACTION_DATE (MMDDYYYY text) | BUYER_COUNTY + BUYER_STATE (names) |
| B | LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_INJURY_VIOLENCE_COUNTY | GEOID, INTENT, PERIOD, RATE, TTM_DATE_RANGE | PERIOD / TTM_DATE_RANGE | GEOID (county FIPS) |
join: county name+state → FIPS via REF__DIM_GEOGRAPHY, then FIPS = GEOID
gap: ARCOS carries no FIPS; mart UNCATEGORIZED__FED_DEA_ARCOS_FULL has 0 profiled columns, so raw only; name join to FIPS is lossy on parish/borough spellings
trap: ARCOS TRANSACTION_DATE is MMDDYYYY text with two float rows (topo map); CDC RATE has -999 sentinel and RATE_M text flag (memory trap)

### #27 — Power plant bad-air day shows in local Part B claims
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_RAW.LANDING.FED_EPA_CAMPD_EMISSIONS_DAILY | columns NOT IN CATALOG (landing not profiled); fallback M.ENVIRONMENT.ENVIRONMENT__FED_EPA_EGRID_PLANT_2022: PLANT_FIPS_COUNTY_CODE, PLANT_ANNUAL_NOX_EMISSIONS_TONS, PLANT_ANNUAL_SO2_EMISSIONS_TONS, DATA_YEAR | DATA_YEAR (annual only) | PLANT_FIPS_STATE_CODE + PLANT_FIPS_COUNTY_CODE |
| B | LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER_AND_SERVI | RNDRNG_NPI, RNDRNG_PRVDR_ZIP5, RNDRNG_PRVDR_STATE_FIPS, HCPCS_CD, TOT_SRVCS, TOT_BENES | none (one DY, 2024) | RNDRNG_PRVDR_ZIP5 |
join: none found — plant side is county FIPS, Part B side is ZIP5, no ZIP→county table
gap: Part B is annual per-provider, no claim date, so "day" cannot be tested; CAMPD daily columns unprofiled; ZIP↔county crosswalk missing
trap: Part B service table is a suppressed subset, under-11-bene rows deleted (memory trap); Part B/D are one year, no before/after (traps.md 2026-09-05)

### #28 — Nursing homes chart sicker right after a chain buys them
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS | CCN, ENROLLMENT_ID (date encoded), AFFILIATION_ENTITY_ID, AFFILIATION_ENTITY_NAME, PROPRIETARY_NONPROFIT | ENROLLMENT_ID parse (O+YYYYMMDD) | CCN; STATE, ZIP_CODE |
| B | LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FACILITY_LEVEL_MINIMUM_DATA_SET_FREQUENCY | CCN, REPORT_DATE, MDS_ITEM_QUESTION_DESCRIPTION, MDS_ITEM_RESPONSE, OVERALL_PERCENT, TOTAL_RESIDENTS | REPORT_DATE | CCN; FIPS_COUNTY_CODE |
join: CCN
gap: no ownership-change history table; purchase date only via ENROLLMENT_ID parse or HEALTH__FED_NURSINGHOME411.PROVIDER_CHANGED_OWNERSHIP_IN_LAST_12_MONTHS (55 'Y'); chain = NURSINGHOME411.CHAIN_ID, one snapshot 2025-12-01
trap: ENROLLMENT_ID is record-creation date, INCORPORATION_DATE is not a recency clock; CHOW flag all 'N' on FED_CMS_NURSING_HOME (traps.md 2026-09-05)

### #29 — Dialysis chains arrive, local kidney doctor count falls
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_DIALYSIS | CCN, CHAIN_OWNED, CHAIN_ORGANIZATION, CERTIFICATION_DATE, OF_DIALYSIS_STATIONS | CERTIFICATION_DATE | COUNTY_PARISH + STATE (names); ZIP_CODE |
| B | LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES | NPI, ENTITY_TYPE_CODE, HEALTHCARE_PROVIDER_TAXONOMY_CODE_1, PROVIDER_ENUMERATION_DATE, NPI_DEACTIVATION_DATE | PROVIDER_ENUMERATION_DATE (floor, not presence) | PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_POSTAL_CODE (ZIP) |
join: ZIP_CODE = first 5 of POSTAL_CODE; county via COUNTY_PARISH name → REF__DIM_GEOGRAPHY
gap: NPPES is a current snapshot, no doctor-count-by-year; only arrival (enumeration) and death (deactivation) dates; dialysis county is a name
trap: NPPES deactivated rows blanked to '' (traps.md 2026-09-05); FED_CMS_DIALYSIS.FIVE_STAR_DATE is one range string on every row (traps.md 2026-09-06)

### #30 — Water violations cluster where hospitals closed
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT + ENVIRONMENT__FED_EPA_SDWA_SDWA_GEOGRAPHIC_AREAS | PWSID, IS_HEALTH_BASED_IND, NON_COMPL_PER_BEGIN_DATE, VIOLATION_CATEGORY_CODE; PWSID, COUNTY_SERVED, STATE_SERVED, ZIP_CODE_SERVED | NON_COMPL_PER_BEGIN_DATE | COUNTY_SERVED + STATE_SERVED (names) via PWSID |
| B | LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER | CCN, PRVDR_CTGRY_CD, PGM_TRMNTN_CD, TRMNTN_EXPRTN_DT | TRMNTN_EXPRTN_DT | FIPS_STATE_CD + FIPS_CNTY_CD |
join: county — COUNTY_SERVED name → REF__DIM_GEOGRAPHY.FIPS_CODE = FIPS_STATE_CD||FIPS_CNTY_CD
gap: POS is one snapshot keeping only the latest status per CCN, so closures before the file's window are invisible; FIPS_CNTY_CD is NUMBER (unpadded)
trap: POS_OTHER CHOW_DT is effective date, keeps latest only; id column is CCN (traps.md 2026-09-05)

### #31 — Hospices in chains discharge alive more or less
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPICE + IMMIGRATION__FED_CMS_HOSPICE_ENROLLMENTS | CCN, OWNERSHIP_TYPE, CERTIFICATION_DATE; CCN, ASSOCIATE_ID, ORGANIZATION_NAME | CERTIFICATION_DATE | CCN; STATE, ZIP_CODE, COUNTY_PARISH |
| B | NOT FOUND in catalog | live-discharge rate | — | — |
join: none found (B missing)
gap: searched DISCHARG, ALIVE, LIVE_DISCH, HOSPICE across both catalogs — no hospice quality / PEPPER / claims file landed; no hospice chain id, only ASSOCIATE_ID (org)
trap: hospice enrollments sit under domain "immigration", a registry mislabel (traps.md 2026-09-01)

### #32 — Nursing census drops, hospice enrollments rise same year
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FACILITY_LEVEL_MINIMUM_DATA_SET_FREQUENCY | CCN, REPORT_DATE, TOTAL_RESIDENTS | REPORT_DATE | FIPS_COUNTY_CODE |
| B | LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPICE | CCN, CERTIFICATION_DATE, OWNERSHIP_TYPE | CERTIFICATION_DATE (agency openings, not patient enrollments) | COUNTY_PARISH + STATE (names) |
join: county — COUNTY_PARISH name → REF__DIM_GEOGRAPHY.FIPS_CODE = FIPS_COUNTY_CODE
gap: patient-level hospice enrollment is not landed anywhere; only agency certification dates stand in; TOTAL_RESIDENTS is TEXT; MDS date span unknown from catalog
trap: none

### #33 — Sickest-charted homes also carry most fire violations
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME | CMS_CERTIFICATION_NUMBER_CCN, NURSING_CASE_MIX_INDEX, NUMBER_OF_CERTIFIED_BEDS | PROCESSING_DATE (null on mart) | COUNTY_FIPS; ZIP_CODE |
| B | LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_FIRE_DEFICIENCIES | CMS_CERTIFICATION_NUMBER_CCN, SURVEY_DATE, DEFICIENCY_TAG_NUMBER, SCOPE_SEVERITY_CODE, DEFICIENCY_CORRECTED | SURVEY_DATE | STATE, ZIP_CODE |
join: CMS_CERTIFICATION_NUMBER_CCN
gap: A is one snapshot; year on A comes from LANDING (2026-05-01), mart PROCESSING_DATE is null
trap: K0351 is the only no-sprinkler tag; DEFICIENCY_CORRECTED is a status not a boolean; mart PROCESSING_DATE null on all rows (traps.md 2026-09-05)

### #34 — Counties with more nursing beds than doctors to staff
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME | COUNTY_FIPS, NUMBER_OF_CERTIFIED_BEDS | none (snapshot) | COUNTY_FIPS |
| B | LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PART_D_PRESCRIBERS | NPI, PRSCRBR_TYPE, PRSCRBR_STATE_FIPS, PRSCRBR_ZIP5 | none (DY2024) | PRSCRBR_ZIP5 |
join: none found — beds are by county FIPS, doctors by ZIP5; no ZIP→county table
gap: ZIP→county crosswalk missing; alt doctor count HEALTH__FED_HRSA_HPSA_PRIMARY_CARE.HPSA_FTE by COUNTY_FIPS_CODE covers designated shortage areas only
trap: NPPES/Part D snapshot, one year (traps.md 2026-09-05)

### #35 — Dementia charting jumps after reimbursement rule change
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FACILITY_LEVEL_MINIMUM_DATA_SET_FREQUENCY | CCN, REPORT_DATE, MDS_ITEM_QUESTION_DESCRIPTION, MDS_ITEM_RESPONSE, OVERALL_PERCENT, LONG_STAY_PERCENT | REPORT_DATE | CCN; STATE, FIPS_COUNTY_CODE |
| B | rule-change date is a constant (PDPM 2019-10-01), not a table | — | — | — |
join: not needed (time split on REPORT_DATE)
gap: which MDS item is the dementia item is unknown until MDS_ITEM_QUESTION_DESCRIPTION values are read; REPORT_DATE span unknown from catalog (31.4M rows landed)
trap: none

### #36 — Nonprofit hospitals pay least charity per surplus dollar
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HCRIS | PROVIDER_CCN, TYPE_OF_CONTROL, COST_OF_CHARITY_CARE, NET_INCOME, FISCAL_YEAR_LENGTH_DAYS | FISCAL_YEAR_END_DATE / SOURCE_FILE_YEAR | STATE_CODE, COUNTY, ZIP_CODE |
| B | LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_990 | EIN, ORGANIZATION_NAME, TOTAL_REVENUE_AMT, TOTAL_EXPENSES_AMT, TAX_YEAR | TAX_YEAR | STATE, ZIP_CODE |
join: none found — no CCN→EIN bridge; name+ZIP match only
gap: CCN↔EIN bridge missing (NPPES EIN is '<UNAVAIL>'); HCRIS alone answers it (charity / NET_INCOME by TYPE_OF_CONTROL), B optional
trap: HCRIS 'nan' typed as FLOAT NaN; for-profit charity mostly blank; filter FISCAL_YEAR_LENGTH_DAYS >= 300 (traps.md 2026-09-05); grain is RPT_REC_NUM, 2011-2023 (2026-09-06)

### #37 — Hospitals closed, where doctors showed up next year
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER | CCN, PRVDR_CTGRY_CD, PGM_TRMNTN_CD, TRMNTN_EXPRTN_DT | TRMNTN_EXPRTN_DT | FIPS_STATE_CD + FIPS_CNTY_CD, ZIP_CD |
| B | LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FACILITY_AFFILIATION → HEALTH__FED_CMS_NPPES | NPI, CCN, FACILITY_TYPE; NPI, PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_POSTAL_CODE, LAST_UPDATE_DATE | LAST_UPDATE_DATE (NPPES, weak) | POSTAL_CODE (ZIP) |
join: CCN (POS ↔ affiliation), then NPI (affiliation ↔ NPPES)
gap: affiliation is a current snapshot — doctors at a closed hospital are already gone from it; no NPPES address history, so "next year" has no before-state
trap: facility affiliation under-reports badly (memory trap); CAH_OR_HOSPITAL_CCN splits on '|' (traps.md 2026-09-05)

### #38 — Hospital mergers precede local Part B price rises
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER | CCN, CHOW_DT, CHOW_PRIOR_DT, CHOW_CNT | CHOW_DT | FIPS_STATE_CD + FIPS_CNTY_CD |
| B | LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_OUTPATIENT_HOSPITALS_BY_PROVIDER_AND_SERVICE | RNDRNG_PRVDR_CCN, APC_CD, AVG_TOT_SBMTD_CHRGS, AVG_MDCR_PYMT_AMT | none (one DY) | RNDRNG_PRVDR_CCN; RNDRNG_PRVDR_STATE_FIPS, RNDRNG_PRVDR_ZIP5 |
join: CCN = RNDRNG_PRVDR_CCN
gap: B has no year — one data year, so "rise" has no series; A keeps only the latest CHOW per CCN
trap: POS keeps latest CHOW only, CHOW_SW blank on all rows (traps.md 2026-09-05); one-year CMS files have no before/after (2026-09-05)

### #39 — Hospitals own the home health agency they refer to most
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH_OWNERS + HEALTH__FED_CMS_HOSPITAL_ENROLLMENTS | CCN, NPI, ASSOCIATE_ID_OWNER, ORGANIZATION_NAME_OWNER, ASSOCIATION_DATE_OWNER, PERCENTAGE_OWNERSHIP; CCN, ASSOCIATE_ID, ORGANIZATION_NAME | ASSOCIATION_DATE_OWNER | AGENCY_STATE; ENROLLMENT_STATE |
| B | NOT FOUND in catalog (hospital→HHA referral volume) | — | — | — |
join: ASSOCIATE_ID_OWNER = ASSOCIATE_ID (ownership leg only)
gap: searched REFER, HHA, HOME_HEALTH — only HEALTH__FED_CMS_ORDER_AND_REFERRING.HHA (eligibility Y/N, no volume) and DME-by-referrer; no referral-flow file landed
trap: 95 HHA CCNs are 7-char with letter suffix, a 6-char join drops them (traps.md 2026-09-05); ASSOCIATE_ID is org↔org only (memory trap)

### #40 — Hospitals near pollution bill more respiratory per patient
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_BASIC_2023 | C_2_TRIFD, C_51_5_1_FUGITIVE_AIR, C_52_5_2_STACK_AIR, C_42_CLEAN_AIR_ACT_CHEMICAL, C_12_LATITUDE, C_13_LONGITUDE | C_1_YEAR | C_9_ZIP; C_7_COUNTY |
| B | LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_INPATIENT_HOSPITALS_BY_PROVIDER_AND_SERVICE | RNDRNG_PRVDR_CCN, DRG_CD, DRG_DESC, TOT_DSCHRGS, AVG_MDCR_PYMT_AMT | none (one DY) | RNDRNG_PRVDR_ZIP5 |
join: C_9_ZIP = RNDRNG_PRVDR_ZIP5
gap: B is one year; "per patient" = respiratory DRG discharges / TOT_DSCHRGS all DRGs; no hospital lat/lon in HEALTH__FED_CMS_HOSPITAL_GENERAL, so distance needs ZIP centroid via REFERENCE__CENSUS_CB_ZCTA.GEOMETRY
trap: TRI_FACILITY lat/lon are packed DDMMSS; TRI_BASIC_2023 has clean decimals (traps.md 2026-09-05)

### #41 — Pharmacies took most pills per resident 2012, by county
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_RAW.LANDING.FED_DEA_ARCOS_FULL | BUYER_DEA_NO, BUYER_BUS_ACT, BUYER_NAME, DOSAGE_UNIT, TRANSACTION_DATE | TRANSACTION_DATE | BUYER_COUNTY + BUYER_STATE (names); BUYER_ZIP |
| B | LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_DRUG_POISONING_COUNTY | FIPS, YEAR, POPULATION | YEAR | FIPS |
join: county name+state → REF__DIM_GEOGRAPHY.FIPS_CODE = FIPS
gap: no DEA_NO→FIPS table; the hub named in the wonder does not exist, county comes off BUYER_COUNTY text; DRUG_POISONING YEAR span unknown from catalog
trap: ARCOS TRANSACTION_DATE is MMDDYYYY text (topo map)

### #42 — Top 2012 distributor counties saw steepest death rise
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_RAW.LANDING.FED_DEA_ARCOS_FULL | REPORTER_DEA_NO, REPORTER_NAME, REPORTER_FAMILY, BUYER_COUNTY, BUYER_STATE, DOSAGE_UNIT, TRANSACTION_DATE | TRANSACTION_DATE | BUYER_COUNTY + BUYER_STATE (names) |
| B | LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_DRUG_POISONING_COUNTY | FIPS, YEAR, ESTIMATED_AGE_ADJUSTED_DEATH_RATE_11_CATEGORIES_IN_RANGES, POPULATION | YEAR | FIPS |
join: county name+state → REF__DIM_GEOGRAPHY.FIPS_CODE = FIPS
gap: death rate is an 11-bin range, not a number — "steepest rise" is bin jumps; HEALTH__FED_CDC_INJURY_VIOLENCE_COUNTY.RATE is numeric but 2019-2024 only
trap: CDC injury RATE -999 sentinel, RATE_M text flag (memory trap)

### #43 — Adverse events through 2014 cluster by prescriber state
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_DEMO + HEALTH__FED_FDA_FAERS_DRUG | PRIMARYID, CASEID, EVENT_DT, OCCP_COD, REPORTER_COUNTRY, OCCR_COUNTRY; PRIMARYID, DRUGNAME, ROLE_COD | EVENT_DT | none — country only, no state, no NPI |
| B | LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PART_D_PRESCRIBERS | NPI, PRSCRBR_STATE_ABRVTN, BRND_TOT_CLMS | none (DY2024) | PRSCRBR_STATE_ABRVTN |
join: none found — FAERS carries no state and no prescriber id (searched STATE across all FAERS_* tables)
gap: place missing on A entirely; 2014 FAERS vs 2024 Part D never overlap in time
trap: FDA_DT is receipt date, reconcile by run id (traps.md 2026-08-31); FAERS ends 2014q2 (topo map)

### #44 — Drugs leading Part D cost growth, who prescribes most
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PARTD_PRESCRIBERS | NPI, BRAND_NAME, GENERIC_NAME, TOTAL_DRUG_COST, TOTAL_CLAIMS, PRESCRIBER_TYPE | none (DY22, one load) | PRESCRIBER_STATE, PRESCRIBER_STATE_FIPS |
| B | LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PART_D_PRESCRIBERS | NPI, TOT_DRUG_CST, PRSCRBR_TYPE | none (DY2024) | PRSCRBR_STATE_FIPS, PRSCRBR_ZIP5 |
join: NPI
gap: "growth" needs two years of the by-drug file; only DY22 exists, and the DY2024 by-provider file has no drug column — growth by drug is untestable
trap: Part D prescriber-drug has NO year column, one load = DY22 (traps.md 2026-08-31); by-provider is DY2024 (2026-09-05)

### #45 — Antipsychotic scripts per nursing bed track chain ownership
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PART_D_PRESCRIBERS | NPI, ANTPSYCT_GE65_TOT_CLMS, ANTPSYCT_GE65_SPRSN_FLAG, ANTPSYCT_GE65_TOT_BENES | none (DY2024) | NPI; PRSCRBR_ZIP5 |
| B | LIBRARY_MARTS.HEALTH.HEALTH__FED_NURSINGHOME411 | CMS_CERTIFICATION_NUMBER_CCN, CHAIN_ID, CHAIN_NAME, NUMBER_OF_CERTIFIED_BEDS, OWNERSHIP_TYPE | PROCESSING_DATE (snapshot) | CMS_CERTIFICATION_NUMBER_CCN; COUNTY_PARISH, STATE |
join: NPI → CCN via HEALTH__FED_CMS_FACILITY_AFFILIATION (NPI, CCN, FACILITY_TYPE)
gap: affiliation lists one doctor for 35.5% of nursing homes (memory trap), so beds-per-prescriber is mostly a lone name; ANTPSYCT_GE65_TOT_CLMS is TEXT
trap: NH411 CHAIN_ID '' on 4,551 homes, pin on CHAIN_ID not name; ANTPSYCT blank is suppressed 1-10 not zero (traps.md 2026-09-05)

### #46 — After poverty explains overdoses, which counties stand out
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_INJURY_VIOLENCE_COUNTY | GEOID, INTENT, PERIOD, RATE, COUNT_SUP | PERIOD / TTM_DATE_RANGE | GEOID |
| B | LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_HPSA_PRIMARY_CARE | PCT_POPULATION_BELOW_POVERTY, DESIGNATION_POPULATION, HPSA_STATUS | DESIGNATION_DATE | STATE_COUNTY_FIPS_CODE / COUNTY_FIPS_CODE |
join: GEOID = STATE_COUNTY_FIPS_CODE
gap: no all-county poverty table (searched POVERTY, SAIPE, ACS, CENSUS, INCOME) — HPSA covers designated shortage areas only; FINANCE__FED_IRS_SOI is ZIP-level AGI (STATE_FIPS, ZIP_CODE, AGI_STUB, TAX_YEAR), no county
trap: HPSA ratio columns were text-cast to null by name-keyed casts (traps.md 2026-09-07)

### #47 — After age explains Part D, which counties prescribe more
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PART_D_PRESCRIBERS | NPI, TOT_CLMS, TOT_BENES, BENE_AVG_AGE, BENE_AGE_65_74_CNT, BENE_AGE_75_84_CNT, BENE_AGE_GT_84_CNT | none (DY2024) | PRSCRBR_STATE_FIPS, PRSCRBR_ZIP5 |
| B | LIBRARY_MARTS.REFERENCE.REF__DIM_GEOGRAPHY | FIPS_CODE, COUNTY_NAME, STATE_ABBR | none | FIPS_CODE |
join: none found — A is ZIP5, B is county FIPS, no ZIP→county table
gap: ZIP→county crosswalk missing; no county age-structure table, so age control is prescriber-level (BENE_AVG_AGE) not county-level; no year
trap: Part D by-provider is one year (traps.md 2026-09-05)

### #48 — Open Payments dinners precede prescribing shifts by a quarter
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS (+ _2022, _2023) | NPI, DATE_OF_PAYMENT, NATURE_OF_PAYMENT_OR_TRANSFER_OF_VALUE, TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS, APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_NAME | PROGRAM_YEAR, DATE_OF_PAYMENT (TEXT) | NPI; RECIPIENT_STATE, RECIPIENT_ZIP_CODE |
| B | LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PARTD_PRESCRIBERS | NPI, BRAND_NAME, TOTAL_CLAIMS, TOTAL_DRUG_COST | none (DY22, annual) | NPI; PRESCRIBER_STATE |
join: NPI
gap: prescribing is annual and one year — no quarter grain anywhere, so "by a quarter" is untestable; payments 2022-2024 vs scripts DY22
trap: bare OPEN_PAYMENTS is PY2024 only, blank NPI is '' on 48,059 rows, 73 year-0002 dates (traps.md 2026-09-05); Part D one year (2026-09-05)

### #49 — Doctors excluded, reinstated, and paid again by pharma
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE | NPI, EXCLUSION_TYPE, EXCLUSION_DATE, REINSTATEMENT_DATE, WAS_REINSTATED | EXCLUSION_DATE | NPI; STATE, ZIP |
| B | LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS (+ _2022, _2023) | NPI, DATE_OF_PAYMENT, TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS, NATURE_OF_PAYMENT_OR_TRANSFER_OF_VALUE | PROGRAM_YEAR | NPI; RECIPIENT_STATE |
join: NPI
gap: "reinstated" cannot be seen — the LEIE file is active exclusions only, so the wonder collapses to "excluded and still paid"; a reinstatement file would need landing
trap: WAS_REINSTATED false and REINSTATEMENT_DATE blank on 100% of rows; only 10.6% of LEIE rows carry a real NPI (traps.md 2026-09-05)

### #50 — Device recalls follow surgeon royalty payments by product
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_RAW.LANDING.FED_CMS_OPEN_PAYMENTS | NPI, NATURE_OF_PAYMENT_OR_TRANSFER_OF_VALUE, NAME_OF_DRUG_OR_BIOLOGICAL_OR_DEVICE_OR_MEDICAL_SUPPLY_1, ASSOCIATED_DEVICE_OR_MEDICAL_SUPPLY_PDI_1, DATE_OF_PAYMENT, TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS | PROGRAM_YEAR | product: PDI_1 / product name; NPI |
| B | LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_DEVICE_ENFORCEMENT (+ HEALTH__FED_FDA_GUDID) | RECALL_NUMBER, PRODUCT_CODE, PRODUCT_DESCRIPTION, RECALLING_FIRM, CLASSIFICATION; PRIMARY_DI, BRAND_NAME, PRIMARY_PRODUCT_CODE, COMPANY_NAME | RECALL_INITIATION_DATE | PRODUCT_CODE; STATE (firm) |
join: ASSOCIATED_DEVICE_OR_MEDICAL_SUPPLY_PDI_1 = GUDID.PRIMARY_DI → PRIMARY_PRODUCT_CODE = DEVICE_ENFORCEMENT.PRODUCT_CODE; fallback product-name text match
gap: mart drops product columns, raw only; PDI fill rate unknown; GUDID mart may be a partial load (a __staging twin exists); place is the recalling firm, not the surgeon
trap: royalty rows carry blank NPI on 43% of royalty dollars; product columns live only in LANDING (traps.md 2026-09-05)

## Gaps summary
| # | gap | fix |
|---|---|---|
| 26, 41, 42 | ARCOS has county names, no FIPS; mart profile empty | add a column: BUYER_COUNTY+STATE → FIPS via REF__DIM_GEOGRAPHY, materialize in the ARCOS mart |
| 27, 34, 47 | no ZIP→county crosswalk; CMS per-provider files are ZIP5, everything else is FIPS | land a table: HUD ZIP-county crosswalk |
| 27 | CAMPD daily emissions landing unprofiled; Part B has no claim dates | parse a field: profile FED_EPA_CAMPD_EMISSIONS_DAILY; "day" needs claims, not summaries |
| 28 | no nursing-home ownership-change history | land a table: CMS SNF ownership/CHOW file |
| 29, 34, 37 | NPPES is a snapshot, no doctor location history | land a table: NPPES monthly deactivation/history files |
| 31 | no hospice quality or live-discharge measure | land a table: CMS Hospice Compare / PEPPER |
| 32 | no patient-level hospice enrollment | land a table: CMS hospice utilization by provider |
| 35 | dementia MDS item unknown | parse a field: read distinct MDS_ITEM_QUESTION_DESCRIPTION |
| 36 | no CCN→EIN bridge | land a table: CMS Hospital Compare EIN / IRS 990 Schedule H CCN |
| 38, 40, 44, 47, 48 | CMS Part B/Part D/inpatient/outpatient are one data year | land a table: prior-year CMS PUFs (DY2019-2023) |
| 39 | no hospital→HHA referral volume | land a table: CMS post-acute referral / shared-patient file |
| 43 | FAERS has no state or prescriber | none possible from FAERS; needs MedWatch state field (not in public file) |
| 46 | no all-county poverty | land a table: Census SAIPE county poverty |
| 49 | LEIE is active-only, no reinstatements | land a table: LEIE monthly reinstatement supplement |
| 50 | Open Payments product columns dropped from mart | add a column: carry PDI_1 and product name into the mart |

# Arc 3

# Arc 3 — MONEY — wonders #51–#75 mapped to catalog tables (metadata only, 2026-09-09)

Table naming: `LIBRARY_MARTS.<REALM>.<TABLE>` where REALM is column 1 of THE_CATALOG.csv. Nothing below was queried.

### #51 — 13F ownership shifts the quarter before a contract lands
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_SUBMISSIONS + LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_HOLDINGS | CIK, ACCESSION_NUMBER, PERIODOFREPORT, FILING_DATE; CUSIP, NAMEOFISSUER, VALUE_USD, SSHPRNAMT | PERIODOFREPORT | CIK (filer), CUSIP (issuer) |
| B | LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS_FULL_R2 | RECIPIENT_UEI, RECIPIENT_NAME, ACTION_DATE, FEDERAL_ACTION_OBLIGATION, RECIPIENT_STATE_CODE | ACTION_DATE | RECIPIENT_UEI |
join: none found directly. Only CIK→UEI bridge in catalog is LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__XC_EPA_CORPORATE_CROSSWALK (PARENT_CIK, PARENT_UEI) — covers EPA-facility parents only. Issuer side of 13F is CUSIP, and no CUSIP→CIK table exists (COMPANY_TICKERS has CIK+TICKER, no CUSIP).
gap: two missing links — CUSIP→CIK (issuer identity) and CIK→UEI (contractor identity). Searched: CUSIP in every table (only 13F holdings/submission), UEI (17 tables, none with CIK except EPA crosswalk).
trap: 13F missed 7 of 53 zips while checkpoint-sum matched; CURRENT_TOTAL_VALUE_OF_AWARD is not spend — use FEDERAL_ACTION_OBLIGATION > 0.

### #52 — Congressional trades cluster around committee hearings
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.POLITICS.POLITICS__SENATE_TRADES | TRANSACTION_DATE, TICKER, TRANSACTION_TYPE, AMOUNT_BAND, BIOGUIDE | TRANSACTION_DATE | BIOGUIDE, TICKER |
| A2 | LIBRARY_MARTS.FINANCE.FINANCE__FED_SENATE_EFD_PTR | TRANSACTION_DATE, FILED_DATE, TICKER, FILER_LAST_CLEAN, FILING_YEAR | FILING_YEAR | FILER_LAST_CLEAN (name only) |
| B | NOT FOUND in catalog (committee hearings). Nearest: LIBRARY_MARTS.POLITICS.POLITICS__FED_CONGRESS_COMMITTEE_MEMBERSHIP | CONGRESS, COMMITTEE_CODE, COMMITTEE_NAME, BIOGUIDE | CONGRESS | BIOGUIDE |
join: BIOGUIDE (trades → membership). No hearing-date side.
gap: no hearing schedule table anywhere (searched HEARING in table names and columns). No place column on either side; state only via POLITICS__MEMBER_CROSSWALK.LAST_STATE. Ticker→company needs FINANCE__FED_SEC_EDGAR_COMPANY_TICKERS_EXCHANGE (TICKER→CIK).
trap: SENATE_TRADES runs 2012-06 to 2020-12 with 2,111 blank tickers; bills/votes start 2023, zero overlap. EFD PTR SENATOR column holds the literal 'Senator' on 98 rows; key on FILER_LAST_CLEAN. Committee membership is one row per congress per seat — dedupe before joining money.

### #53 — Zips give most to politics, get least back
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS | ZIP_CODE, TRANSACTION_DATE, TRANSACTION_AMT, TRANSACTION_TYPE, STATE | TRANSACTION_DATE | ZIP_CODE |
| B | LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS_FULL_R2 (+ ECONOMICS__FED_USASPENDING_ASSISTANCE_FULL) | RECIPIENT_ZIP_4_CODE, ACTION_DATE, FEDERAL_ACTION_OBLIGATION (assistance: RECIPIENT_ZIP_CODE, ACTION_DATE_FISCAL_YEAR) | ACTION_DATE | RECIPIENT_ZIP_4_CODE (left 5) |
| norm | LIBRARY_MARTS.FINANCE.FINANCE__FED_IRS_SOI | ZIP_CODE, TAX_YEAR, N_RETURNS, AGI | TAX_YEAR | ZIP_CODE |
join: ZIP5 on all three (FEC ZIP_CODE may be 9 digits; contracts is ZIP+4 — truncate both).
gap: FEC side is 2023-2026 only, so the "give" window is four years; contracts run 2006-2026. Assistance side capped at 1M rows/year.
trap: FEC indiv is a four-year file, earmarks are TRANSACTION_TYPE 15E (no MEMO_CD); USAspending assistance is capped 1M rows per year — every total is a floor; ZIP is a geography key, it identifies nothing.

### #54 — CFPB complaint spikes lead enforcement by a year
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.CONSUMER_PROTECTION.CONSUMER_PROTECTION__FED_CFPB_COMPLAINTS | COMPANY, DATE_RECEIVED, RECEIVED_YEAR, PRODUCT, STATE, ZIP_CODE | RECEIVED_YEAR | COMPANY (name), STATE |
| B | NOT FOUND in catalog (CFPB enforcement actions). Nearest: LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FDIC_ENFORCEMENT_ORDERS | INSTITUTION_NAME, ORDER_DATE, ORDER_YEAR, ORDER_TYPE, CMP_AMOUNT_TOTAL, BANK_STATE, CERT_NUMBER | ORDER_YEAR | INSTITUTION_NAME, CERT_NUMBER |
| B2 | LIBRARY_MARTS.LEGAL_ENFORCEMENT.LEGAL_ENFORCEMENT__FED_NAAG_MULTISTATE_SETTLEMENTS | DEFENDANTS, YEAR, DATERESOLVED, TOTALSETTLEMENTAMOUNT, CORPORATEHEADQUARTERS | YEAR | DEFENDANTS (name) |
join: company name only (COMPANY ↔ INSTITUTION_NAME / DEFENDANTS). No shared id.
gap: no CFPB enforcement table (searched CFPB, ENFORC in table names — only FDIC, EPA, FDA, NHTSA). FDIC orders cover banks only; complaints are mostly credit bureaus, servicers, debt collectors. Name join needed.
trap: single-word name matches are 8% real; "National Association" bank names are one entity — use FDIC SOD RSSDID/NAMEHCR to confirm.

### #55 — Disaster contractors win same counties every storm
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS_FULL_R2 | RECIPIENT_UEI, RECIPIENT_NAME, ACTION_DATE, FEDERAL_ACTION_OBLIGATION, AWARDING_SUB_AGENCY_NAME (FEMA), PRIMARY_PLACE_OF_PERFORMANCE_STATE_CODE, PRIMARY_PLACE_OF_PERFORMANCE_CITY_NAME | ACTION_DATE | RECIPIENT_UEI; place = state+city only |
| A2 | LIBRARY_MARTS.PROCUREMENT.PROCUREMENT__FED_USASPENDING_BULK | RECIPIENT_UEI, ACTION_DATE, PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE | ACTION_DATE | county FIPS |
| B | LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_NOAA_STORM_EVENTS | YEAR, BEGIN_DATE_TIME, EVENT_TYPE, STATE_FIPS, CZ_FIPS, CZ_TYPE, DAMAGE_PROPERTY | YEAR | STATE_FIPS+CZ_FIPS (county when CZ_TYPE='C') |
| B2 | LIBRARY_MARTS.HOUSING.HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS | DISASTER_NUMBER, DECLARATION_DATE, FIPS, DAMAGED_STATE_ABBREVIATION | DECLARATION_DATE | FIPS |
join: county FIPS — exists on storms and FEMA IA, but NOT on the full contracts table (R2 has state+city only). BULK has county FIPS but is a 50,000-row sample.
gap: full contracts table lacks a county column; only the sample carries it. FEMA IA mart is 3.08M of 25.9M (truncated). No disaster-declarations table — declaration date rides on each IA registration.
trap: FEMA IA FIPS is unpadded TEXT for states 01-09 — lpad before joining; USASPENDING_BULK is a sample, never for totals.

### #56 — Banks under orders keep lending in same zips
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FDIC_ENFORCEMENT_ORDERS | CERT_NUMBER, ORDER_DATE, ORDER_YEAR, ORDER_TYPE, TERMINATION_DATE, BANK_STATE, BANK_RSSD_ID | ORDER_YEAR | CERT_NUMBER |
| B | LIBRARY_MARTS.HOUSING.HOUSING__FED_CFPB_HMDA_HISTORIC | AS_OF_YEAR, RESPONDENT_ID, AGENCY_CODE, ACTION_TAKEN, STATE_CODE, COUNTY_CODE, CENSUS_TRACT_NUMBER, LOAN_AMOUNT_000S | AS_OF_YEAR | STATE_CODE+COUNTY_CODE+CENSUS_TRACT_NUMBER (no ZIP) |
| B2 | LIBRARY_MARTS.FINANCE.FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS | FDIC_CERT, SURVEY_YEAR, BRANCH_ZIP, BRANCH_STATE_COUNTY_FIPS, BRANCH_DEPOSITS_THOUSANDS | SURVEY_YEAR | FDIC_CERT, BRANCH_ZIP |
join: FDIC_CERT (orders CERT_NUMBER ↔ SOD FDIC_CERT) is clean. Orders ↔ HMDA needs RESPONDENT_ID = cert for AGENCY_CODE=FDIC lenders — plausible, unverified.
gap: HMDA has no ZIP (tract/county only), full HMDA is 2015-2017 only, HOUSING__FED_CFPB_HMDA and _LAR are samples (DC 2023 / 17k rows). SOD gives deposits by ZIP, not lending. Lender bridge RESPONDENT_ID↔CERT unverified.
trap: HMDA_HISTORIC STATE_CODE/COUNTY_CODE unpadded, no date column (year only), 19,331 denials have null county; FDIC_BANK_DATA is a 10,000-row sample.

### #57 — Banks finance most polluting sites per asset dollar
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.FINANCE.FINANCE__FED_FDIC_BANK_DATA (SAMPLE, 10k rows) / FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS | CERT, LEI, ASSET, REPDTE, STALP / FDIC_CERT, INSTITUTION_ASSETS_THOUSANDS, SURVEY_YEAR, INSTITUTION_STATE | REPDTE / SURVEY_YEAR | CERT, LEI (bank data only) |
| B | LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__XC_EPA_CORPORATE_CROSSWALK + LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__EPA_PENALTY_GAP | EPA_REGISTRY_ID, MATCHED_LEI, ULTIMATE_PARENT_LEI; FRS_ID, FIPS_CODE, STATE, TOTAL_PENALTIES, TRI_ON_SITE_RELEASES, DATE_LAST_FORMAL_ACTION | DATE_LAST_FORMAL_ACTION (crosswalk: none) | FRS_ID, LEI |
join: none found for "finances". LEI links a facility to its OWNER, not its lender. No loan/credit-relationship table exists in the catalog.
gap: the financing edge does not exist anywhere (searched LOAN, CREDIT, SYNDICAT, LENDER across columns — only SBA/PPP/HMDA lender names, none tied to EPA facilities). Bank LEI lives only in the 10k sample.
trap: FRS_ID↔LEI in ENTITY_XREF is a star forest — no middleman possible by construction; FDIC_BANK_DATA is a sample.

### #58 — Small-business loans dry up where local bank absorbed
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_SBA_LOANS | APPROVAL_DATE, APPROVAL_FISCAL_YEAR, LENDER_NAME, LENDER_STATE, PROJECT_COUNTY, PROJECT_STATE, GROSS_APPROVAL_AMOUNT | APPROVAL_FISCAL_YEAR | PROJECT_COUNTY (name) + PROJECT_STATE |
| B | LIBRARY_MARTS.FINANCE.FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS | FDIC_CERT, SURVEY_YEAR, SIMS_ACQUIRED_DATE, BRANCH_STATE_COUNTY_FIPS, INSTITUTION_NAME, HOLDING_COMPANY_NAME | SURVEY_YEAR | BRANCH_STATE_COUNTY_FIPS |
| B2 | LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_FDIC_FAILED_BANKS | FAIL_DATE, FIPS, ACQUIRING_INSTITUTION, FDIC_CERT | FAIL_DATE | FIPS |
| xwalk | LIBRARY_MARTS.REFERENCE.REF__DIM_GEOGRAPHY | COUNTY_NAME, STATE_ABBR, FIPS_CODE | — | FIPS_CODE |
join: county — SBA PROJECT_COUNTY+PROJECT_STATE → REF__DIM_GEOGRAPHY → FIPS ↔ SOD BRANCH_STATE_COUNTY_FIPS / failed-bank FIPS. Lender-to-bank is name only (LENDER_NAME ↔ INSTITUTION_NAME).
gap: SBA county is a name, not FIPS; mergers (not failures) only visible through SOD SIMS_ACQUIRED_DATE or the sampled FDIC_BANK_DATA.SUCCESSOR_CERT. No merger-events table for banks (NCUA has one for credit unions).
trap: "National Association" bank names are one entity — confirm via SOD RSSD_ID/HOLDING_COMPANY_NAME before treating branches as separate lenders.

### #59 — Denial rates diverge most between neighboring counties
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.HOUSING.HOUSING__FED_CFPB_HMDA_HISTORIC | AS_OF_YEAR, STATE_CODE, COUNTY_CODE, ACTION_TAKEN, APPLICANT_INCOME_000S, LOAN_PURPOSE | AS_OF_YEAR | STATE_CODE+COUNTY_CODE |
| B | LIBRARY_MARTS.REFERENCE.REFERENCE__CENSUS_CB_COUNTY | GEOID, STATEFP, COUNTYFP, NAME, GEOMETRY, VINTAGE | VINTAGE | GEOID |
join: lpad(STATE_CODE,2)||lpad(COUNTY_CODE,3) ↔ GEOID. Neighbors come from GEOMETRY (ST_TOUCHES) — no adjacency table exists.
gap: HMDA full coverage is 2015-2017 only; no county-adjacency table (must compute from GEOMETRY).
trap: HMDA_HISTORIC state/county unpadded; county-null rows (19,331 denials) fall into any control group unless COUNTY_CODE is not null is on.

### #60 — Failed banks cluster where complaints rose beforehand
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_FDIC_FAILED_BANKS | FAIL_DATE, FIPS, STATE_ABBR, BANK_NAME, FDIC_CERT, TOTAL_ASSETS_THOUSANDS | FAIL_DATE | FIPS |
| B | LIBRARY_MARTS.CONSUMER_PROTECTION.CONSUMER_PROTECTION__FED_CFPB_COMPLAINTS | DATE_RECEIVED, RECEIVED_YEAR, ZIP_CODE, STATE, COMPANY, PRODUCT | RECEIVED_YEAR | ZIP_CODE, STATE |
join: place mismatch — FIPS vs ZIP. No ZIP→county crosswalk table; only spatial route: REFERENCE__CENSUS_CB_ZCTA.GEOMETRY ∩ REFERENCE__CENSUS_CB_COUNTY.GEOMETRY. Company route: BANK_NAME ↔ COMPANY (name).
gap: no ZIP→FIPS crosswalk (searched ZCTA, CROSSWALK, ZIP_COUNTY — only geometry tables). Complaints start 2011; most bank failures cluster 2008-2012, so early failures have no "before".
trap: single-word name match 8% real; ZIP is a geography key.

### #61 — Firms with going-concern doubt win new contracts
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_FAC_SINGLE_AUDIT | AUDITEE_UEI, AUDITEE_EIN, AUDIT_YEAR, IS_GOING_CONCERN_INCLUDED, AUDITEE_STATE, TOTAL_AMOUNT_EXPENDED | AUDIT_YEAR | AUDITEE_UEI |
| B | LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS_FULL_R2 | RECIPIENT_UEI, ACTION_DATE, FEDERAL_ACTION_OBLIGATION, RECIPIENT_STATE_CODE, AWARD_TYPE | ACTION_DATE | RECIPIENT_UEI |
join: UEI (AUDITEE_UEI ↔ RECIPIENT_UEI). The CIK route in the wonder text is not needed — FAC carries UEI directly.
gap: FAC covers single-audit filers (nonprofits, governments, universities), not SEC registrants; an SEC going-concern flag (XBRL) is not in any catalog table. Assistance (grants) side needs ECONOMICS__FED_USASPENDING_ASSISTANCE_FULL, capped 1M/yr.
trap: FEDERAL_ACTION_OBLIGATION is signed — 90% of some cohorts are ≤ 0; filter > 0.

### #62 — 13F holders exit before the first big fine
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_SUBMISSIONS + FINANCE__FED_SEC_13F_HOLDINGS | CIK, PERIODOFREPORT; CUSIP, NAMEOFISSUER, VALUE_USD, SSHPRNAMT | PERIODOFREPORT | CIK (holder), CUSIP (issuer) |
| B | LIBRARY_MARTS.JUSTICE.JUSTICE__FED_DOJ_FCA_SETTLEMENTS | COMPANY_ID, CASE_TITLE, SETTLEMENT_DATE, FISCAL_YEAR, SETTLEMENT_AMOUNT, DISTRICT | FISCAL_YEAR | COMPANY_ID (no CIK), DISTRICT |
| B2 | LIBRARY_MARTS.LEGAL_ENFORCEMENT.LEGAL_ENFORCEMENT__FED_NAAG_MULTISTATE_SETTLEMENTS | DEFENDANTS, YEAR, TOTALSETTLEMENTAMOUNT, CORPORATEHEADQUARTERS | YEAR | DEFENDANTS (name) |
join: none found. Fines carry names; 13F carries CUSIP. No CUSIP→CIK, no SEC enforcement/penalty table with CIK.
gap: no SEC enforcement table (searched SEC_ENF, LITIG, PENALT); no CUSIP→CIK bridge. Name join NAMEOFISSUER ↔ CASE_TITLE/DEFENDANTS only.
trap: 13F missed 7 of 53 zips; multi-word name match clears 92%, single-word 8%.

### #63 — Pension plans collapsed after a buyout
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.LABOR.LABOR__FED_PBGC_TRUSTEED_PLANS | EIN, SPONSOR_NAME, DATE_OF_PLAN_TERMINATION, DATE_OF_PBGC_TRUSTEESHIP, STATE, NUMBER_OF_PARICIPANTS_AT_DATE_OF_PLAN_TERMINATION | DATE_OF_PLAN_TERMINATION | EIN, STATE |
| B | NOT FOUND in catalog (buyout / M&A). Proxy: LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_DOL_FORM5500 | EIN, FORM_YEAR, SPONSOR_DFE_NAME, LAST_RPT_SPONS_NAME, LAST_RPT_SPONS_EIN, SPONS_DFE_MAIL_US_STATE | FORM_YEAR | EIN |
| B2 | LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_SEC_EDGAR | CIK, EIN, FORM, FILEDAT (SC 13D / 8-K as takeover signal) | FILEDAT | EIN |
join: EIN (PBGC ↔ Form 5500 ↔ EDGAR EIN). Sponsor change on 5500 (LAST_RPT_SPONS_EIN ≠ EIN) is the buyout proxy.
gap: no buyout/PE-transaction table (searched BUYOUT, ACQUI, MERGER, PRIVATE_EQ — only EIA861 and NCUA mergers). Private buyers never file with EDGAR.
trap: FED_DOL_FORM5500_FULL landing is 4.3M rows, the mart 33k — the mart is a slice; EIN chains at 19% for OSHA↔5500, not "freely".

### #64 — Failed banks financed most polluting sites by state
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_FDIC_FAILED_BANKS | FDIC_CERT, BANK_NAME, FAIL_DATE, STATE_ABBR, TOTAL_ASSETS_THOUSANDS | FAIL_DATE | FDIC_CERT, STATE_ABBR |
| B | LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__EPA_PENALTY_GAP (+ ENVIRONMENT__XC_EPA_CORPORATE_CROSSWALK) | FRS_ID, STATE, TOTAL_PENALTIES, TRI_ON_SITE_RELEASES, DATE_LAST_FORMAL_ACTION; MATCHED_LEI | DATE_LAST_FORMAL_ACTION | STATE, FRS_ID |
join: none found. Same hole as #57 — no lender→facility edge. FDIC_CERT→LEI exists only in the 10k FDIC_BANK_DATA sample, and LEI reaches the facility's owner, not its banker. State is the only shared column.
gap: financing relationship absent from the catalog; a state-level overlay is all that is possible.
trap: FRS_ID↔LEI star forest; FDIC_BANK_DATA is a sample.

### #65 — Parents hide behind most subsidiaries per contract
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS_FULL_R2 | RECIPIENT_PARENT_UEI, RECIPIENT_PARENT_NAME, RECIPIENT_UEI, RECIPIENT_NAME, ACTION_DATE, FEDERAL_ACTION_OBLIGATION, RECIPIENT_STATE_CODE | ACTION_DATE | RECIPIENT_PARENT_UEI |
| B | same table, self-join (count distinct RECIPIENT_UEI per RECIPIENT_PARENT_UEI) | — | ACTION_DATE | RECIPIENT_UEI |
join: RECIPIENT_PARENT_UEI. Optional depth: ECONOMICS__INTL_GLEIF_RELATIONSHIPS (RELATIONSHIP_STARTNODE_NODEID, RELATIONSHIP_ENDNODE_NODEID, RELATIONSHIP_PERIOD_1_STARTDATE) but that is LEI, and no UEI↔LEI bridge exists.
gap: one-table wonder; parent UEI fill rate unverified (count distinct before trusting). GLEIF tree unreachable without UEI↔LEI.
trap: FEDERAL_ACTION_OBLIGATION signed, filter > 0; R2 columns are UPPERCASE — the lowercase-USAspending trap does not apply.

### #66 — Charities pay top officer most per program dollar
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_990 | EIN, ORGANIZATION_NAME, TAX_YEAR, OFFICER_COMPENSATION_AMT, TOTAL_EXPENSES_AMT, TOTAL_REVENUE_AMT, STATE, ZIP_CODE | TAX_YEAR | EIN, STATE/ZIP_CODE |
| B | LIBRARY_MARTS.HEALTH.HEALTH__HOSPITAL_OFFICER_PAY (hospitals only) | EIN, TAX_YEAR, PERSON_NAME, TITLE, TOTAL_COMPENSATION, IS_SCHEDULE_J_POINTER, HOSPITAL_STATE | TAX_YEAR | EIN |
| ntee | LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_BMF | EIN, NTEE_CODE, STATE, ZIP | — | EIN |
join: EIN.
gap: no program-service-expense column (only TOTAL_EXPENSES_AMT); "top officer" per person exists only for hospitals — every other charity has one aggregate OFFICER_COMPENSATION_AMT.
trap: 990 Part VII repeats an exec on every affiliate's return — group by person+tax year, take max; "SEE SCH J" pointer lines restate dollars; tax years before 2017 absent from officer pay.

### #67 — Nonprofit revenues spike after disaster declaration
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_990 | EIN, TAX_YEAR, TAX_PERIOD_END_DATE, TOTAL_REVENUE_AMT, STATE, ZIP_CODE | TAX_YEAR | ZIP_CODE, STATE (no county) |
| B | LIBRARY_MARTS.HOUSING.HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS | DISASTER_NUMBER, DECLARATION_DATE, INCIDENT_TYPE_CODE, FIPS, DAMAGED_STATE_ABBREVIATION, DAMAGED_ZIP_CODE | DECLARATION_DATE | FIPS, DAMAGED_ZIP_CODE |
join: ZIP (990 ZIP_CODE ↔ DAMAGED_ZIP_CODE) or STATE. County needs a ZIP→FIPS crosswalk that does not exist.
gap: no disaster-declarations table — declaration date must be distinct-ed out of 26M IA registrations (mart holds 12%). No ZIP→county crosswalk.
trap: FEMA IA FIPS unpadded TEXT for states 01-09; FEMA mart is a truncated 3.08M-row load, not a random sample.

### #68 — Nonprofits win grants and register lobbyists
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_ASSISTANCE_FULL | RECIPIENT_UEI, RECIPIENT_NAME, ACTION_DATE, ACTION_DATE_FISCAL_YEAR, FEDERAL_ACTION_OBLIGATION, BUSINESS_TYPES_DESCRIPTION, RECIPIENT_STATE_CODE, RECIPIENT_ZIP_CODE | ACTION_DATE_FISCAL_YEAR | RECIPIENT_UEI; RECIPIENT_STATE_CODE |
| B | LIBRARY_MARTS.EDUCATION.EDUCATION__FED_SENATE_LDA_FILINGS | CLIENT_ID, CLIENT_NAME, CLIENT_STATE, FILING_YEAR, REGISTRANT_NAME, INCOME, EXPENSES | FILING_YEAR | CLIENT_ID; CLIENT_STATE |
join: name + state (RECIPIENT_NAME ↔ CLIENT_NAME). No EIN on either side; LDA has no UEI.
gap: EIN absent from both (ECONOMICS__FED_US_USASPENDING_API has RECIPIENT_EIN but is an API slice). LDA covers 1999-2010 and 2020-2021 only.
trap: LDA 2011-2019 missing, INCOME/EXPENSES are TEXT and mutually exclusive by filer type; assistance capped 1M rows/yr; multi-word name match 92%, single 8%.

### #69 — Hospital foundations donate to members who fund hospitals
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS → FINANCE__FED_FEC_COMMITTEES_DIM → POLITICS__MEMBER_FEC_ID | EMPLOYER, DONOR_NAME, CMTE_ID, TRANSACTION_DATE, TRANSACTION_AMT, STATE, ZIP_CODE; CMTE_ID, CAND_ID; FEC_ID, BIOGUIDE | TRANSACTION_DATE | CMTE_ID→CAND_ID→BIOGUIDE; EMPLOYER (name) |
| A2 | LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_BMF | EIN, ORGANIZATION_NAME, NTEE_CODE (E-codes), STATE, ZIP | — | EIN; name |
| B | LIBRARY_MARTS.POLITICS.POLITICS__FED_CONGRESS_COMMITTEE_MEMBERSHIP | BIOGUIDE, CONGRESS, COMMITTEE_NAME (health/appropriations) | CONGRESS | BIOGUIDE |
join: BIOGUIDE (money → member → committee). Foundation ↔ donor is EMPLOYER text ↔ BMF ORGANIZATION_NAME (name only; FEC has no EIN).
gap: premise is off — a 501(c)(3) foundation cannot give to a candidate; the signal is employees' EMPLOYER field or a hospital PAC (CMTE_ID with CONNECTED_ORG_NM). "Fund hospitals" has no table: no appropriations-to-hospital column; nearest is committee seat.
trap: FEC indiv is 2023-2026 only; COMMITTEES_DIM CYCLE null on 55%, IS_AMBIGUOUS on 14% of money rows; committee membership one row per congress — dedupe.

### #70 — After population explains contracts, which counties get more
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_US_USASPENDING_API | PLACE_OF_PERFORMANCE_FIPS, RECIPIENT_LOCATION_FIPS, FISCAL_YEAR, TOTAL_OBLIGATION, AWARD_TYPE | FISCAL_YEAR | PLACE_OF_PERFORMANCE_FIPS |
| A2 | LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS_FULL_R2 (full, no county) | ACTION_DATE, FEDERAL_ACTION_OBLIGATION, PRIMARY_PLACE_OF_PERFORMANCE_STATE_CODE, PRIMARY_PLACE_OF_PERFORMANCE_CITY_NAME | ACTION_DATE | state+city only |
| B | LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_DRUG_POISONING_COUNTY | FIPS, YEAR, POPULATION | YEAR | FIPS |
join: FIPS (county) — only if the API table is a real corpus; the full R2 table has no county column.
gap: full contracts table lacks county FIPS; the API mart's size is undocumented (mart catalog says "inferred"). No standalone county-population table — POPULATION borrowed from a CDC file.
trap: FEDERAL_ACTION_OBLIGATION signed; CURRENT_TOTAL_VALUE is a ceiling, not spend.

### #71 — After income explains denials, which lenders deny more
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.HOUSING.HOUSING__FED_CFPB_HMDA_HISTORIC | AS_OF_YEAR, RESPONDENT_ID, AGENCY_CODE, ACTION_TAKEN, APPLICANT_INCOME_000S, LOAN_AMOUNT_000S, STATE_CODE, COUNTY_CODE | AS_OF_YEAR | RESPONDENT_ID+AGENCY_CODE (lender); STATE_CODE+COUNTY_CODE |
| B | LIBRARY_MARTS.HOUSING.HOUSING__FED_CFPB_HMDA_ARID2017_LEI_XREF | ARID_2017, RESPONDENT_NAME, LEI_2018 | — (2017 only) | ARID_2017 |
join: RESPONDENT_ID ↔ ARID_2017 (format match unverified — ARID may be agency-prefixed).
gap: lender names for 2015-2016 respondent ids not in catalog; xref is 2017 vintage. Full HMDA is 2015-2017 only.
trap: HMDA_HISTORIC unpadded codes, no date column; county-null denials fall into any control group.

### #72 — Contractors suspended and win again under a new name
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.PROCUREMENT.PROCUREMENT__FED_SAM_EXCLUSIONS | UEI, CAGE_CODE, ENTITY_NAME, ACTIVATION_DATE, TERMINATION_DATE, EXCLUSION_TYPE, CITY, STATE, ZIP | ACTIVATION_DATE | UEI, CAGE_CODE; CITY+ZIP |
| B | LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS_FULL_R2 | RECIPIENT_UEI, CAGE_CODE, RECIPIENT_NAME, RECIPIENT_DOING_BUSINESS_AS_NAME, ACTION_DATE, RECIPIENT_CITY_NAME, RECIPIENT_ZIP_4_CODE, HIGHLY_COMPENSATED_OFFICER_1_NAME | ACTION_DATE | RECIPIENT_UEI, CAGE_CODE; CITY+ZIP5 |
join: UEI / CAGE_CODE for the suspended entity; the "new name" leg is CITY+ZIP5 (and officer name) — neither table carries a street address.
gap: no street address on either mart (SAM mart has CITY/STATE/ZIP only; R2 has no address line), so the address bridge is ZIP-grain — coarse.
trap: SAM exclusions fan out (1,798 UEIs with 3+ overlapping windows) — use EXISTS, never a join, before summing; ACTIVATION_DATE carries 1908/2084/2099 sentinels and 11,016 nulls.

### #73 — Pandemic loans went to firms already excluded
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_SBA_PPP_LOANS_150K_PLUS | BORROWERNAME, BORROWERADDRESS, BORROWERCITY, BORROWERSTATE, BORROWERZIP, DATEAPPROVED, INITIALAPPROVALAMOUNT, PROCESSINGMETHOD, FORGIVENESSAMOUNT | DATEAPPROVED | BORROWERNAME+BORROWERZIP |
| B | LIBRARY_MARTS.PROCUREMENT.PROCUREMENT__FED_SAM_EXCLUSIONS + LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE | ENTITY_NAME, ACTIVATION_DATE, TERMINATION_DATE, CITY, STATE, ZIP; BUSINESS_NAME, EXCLUSION_DATE, ZIP, STATE | ACTIVATION_DATE / EXCLUSION_DATE | name+ZIP |
join: name + ZIP5. No EIN on PPP, SAM, or LEIE.
gap: no EIN anywhere on either side; PPP under-$150k file (ECONOMICS__FED_SBA_PPP) has no address line.
trap: the 150K_PLUS file holds 4,092 loans under $150k (label, not filter); split PROCESSINGMETHOD (PPS second-draw capped at $2M); LEIE mart blanks the '0000000000' NPI sentinel to ''.

### #74 — Universities hold NIH grants and pharma-paid faculty
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.SCIENCE_RESEARCH.SCIENCE_RESEARCH__FED_NIH_REPORTER | ORG_NAME, ORG_UEI, FISCAL_YEAR, AWARD_AMOUNT, PI_NAMES, PI_PROFILE_IDS, ORG_STATE, ORG_ZIP, ORG_FIPS | FISCAL_YEAR | ORG_UEI; ORG_FIPS/ORG_ZIP |
| B | LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS | NPI, COVERED_RECIPIENT_LAST_NAME, COVERED_RECIPIENT_FIRST_NAME, PROGRAM_YEAR, TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS, TEACHING_HOSPITAL_NAME, CCN, RECIPIENT_STATE, RECIPIENT_ZIP_CODE | PROGRAM_YEAR | NPI; RECIPIENT_ZIP_CODE |
| bridge | LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES | NPI, PROVIDER_LAST_NAME_LEGAL_NAME, PROVIDER_FIRST_NAME, PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_POSTAL_CODE | — | NPI |
join: name only — PI_NAMES ↔ NPPES/Open Payments first+last (+ZIP to disambiguate); org leg ORG_NAME ↔ TEACHING_HOSPITAL_NAME (name). NIH carries no NPI and no EIN; ORG_UEI reaches no health table.
gap: no NPI or EIN on the NIH side (PI_PROFILE_IDS is NIH-internal); university EIN not in NIH REPORTER. Person match is name+place.
trap: NPPES EIN column is '<UNAVAIL>' on every row — never build an EIN edge from it; single-word name match 8% real; unsuffixed OPEN_PAYMENTS is program year 2024.

### #75 — NIH grants land where pharma dinners land
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.SCIENCE_RESEARCH.SCIENCE_RESEARCH__FED_NIH_REPORTER | FISCAL_YEAR, AWARD_AMOUNT, ORG_ZIP, ORG_FIPS, ORG_STATE | FISCAL_YEAR | ORG_ZIP / ORG_FIPS |
| B | LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS | PROGRAM_YEAR, DATE_OF_PAYMENT, NATURE_OF_PAYMENT_OR_TRANSFER_OF_VALUE ('Food and Beverage'), TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS, RECIPIENT_ZIP_CODE, RECIPIENT_STATE, NPI | PROGRAM_YEAR | RECIPIENT_ZIP_CODE |
join: ZIP5 (ORG_ZIP ↔ RECIPIENT_ZIP_CODE, left 5). NPI-grain join impossible (NIH has no NPI) — this is a place-grain scatter.
gap: wonder key says NPI; only ZIP is shared. County needs ORG_FIPS on NIH but a ZIP→FIPS crosswalk on the Open Payments side, which does not exist.
trap: meal-cap fingerprint — $124.99 clustering per maker (HEALTH__PHARMA_MEAL_CAP_FINGERPRINT); ZIP identifies nothing; unsuffixed OPEN_PAYMENTS is 2024 only.

## Gaps summary
| # | gap | fix (land a table / add a column / parse a field) |
|---|---|---|
| 51, 62 | no CUSIP→CIK bridge; no CIK→UEI bridge beyond EPA parents | land SEC company CUSIP list (or 13F issuer→CIK via EDGAR full-index); land SAM entity registration (UEI + parent + EIN) |
| 52 | no committee hearings table | land congress.gov / govinfo hearings (date, committee code) |
| 54 | no CFPB enforcement actions table | land CFPB enforcement actions (company, date, penalty) |
| 55, 70 | full contracts table (R2) has no county FIPS | add PLACE_OF_PERFORMANCE_COUNTY_FIPS to the R2 loader (source file carries it; BULK sample proves it) |
| 55, 67 | FEMA IA mart is 12% truncated; no disaster-declarations table | finish FEMA IA reload; land OpenFEMA DisasterDeclarationsSummaries (disaster_number, declaration_date, FIPS) |
| 56, 59, 71 | HMDA full = 2015-2017 only; 2018+ marts are samples; no lender-name table for RESPONDENT_ID | land HMDA LAR 2018-2024 state×year; land HMDA panel/transmittal (respondent id → name, cert) |
| 57, 64 | no lender→facility financing edge anywhere | none in public data at facility grain; state-level overlay only — say so in the wonder |
| 60, 67, 75 | no ZIP→county FIPS crosswalk table | land HUD USPS ZIP-county crosswalk (or precompute ZCTA∩county from GEOMETRY) |
| 63 | no buyout / M&A table | land SEC SC 13D + 8-K item 1.01 parse, or a PE-deal list; else sponsor-change proxy on Form 5500 |
| 57, 58 | FDIC_BANK_DATA is a 10k sample (LEI, SUCCESSOR_CERT live there) | land full FDIC institutions file with paginated loader |
| 66 | 990 mart has no program-service-expense column | parse PART IX line 25B from 990 XML into ECONOMICS__FED_IRS_990 |
| 68, 73 | no EIN on assistance awards, LDA, PPP, SAM, LEIE | add RECIPIENT_EIN to assistance loader (API has it); PPP/SAM/LEIE never publish EIN — name+ZIP only |
| 74, 75 | NIH REPORTER carries no NPI/EIN | land NIH PI profile → ORCID and an ORCID→NPI list if one exists; else name+ZIP |
| 69 | premise: 501(c)(3) cannot donate; no "funds hospitals" table | reframe to hospital PAC (CONNECTED_ORG_NM) and employees' EMPLOYER; land appropriations earmarks if wanted |

# Arc 4

# Arc 4 — POWER, who decides, who watches (#76–#100)
Metadata only. Tables/columns verbatim from THE_CATALOG.csv unless marked NOT FOUND.

### #76 — Immigration judge grant rate drifts with administration
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_EOIR_CASES | CASE_ID, COURT_CODE, CASE_TYPE, CUSTODY, NATIONALITY, LATEST_HEARING_AT | LATEST_HEARING_AT | COURT_CODE |
| B | NOT FOUND in catalog (judge + decision/outcome table) | — | — | — |
join: none found
gap: no judge column and no decision/grant column anywhere in EOIR_CASES; searched EOIR, JUDGE, DECISION, GRANT in THE_CATALOG — only CASES (38 cols, no outcome) and CASE_DATA (1 col). Need EOIR tblDecision/tblJudge (or a parsed CASE_DATA).
trap: IMMIGRATION__FED_EOIR_CASE_DATA is one unparsed column against 12.6M rows — a broken parallel load, use FED_EOIR_CASES.

### #77 — Judges hold stock in companies on their own docket
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_INVESTMENTS + JUSTICE__FED_COURTLISTENER_FINANCIAL_DISCLOSURES | INVESTMENTS.DESCRIPTION, GROSS_VALUE_CODE, FINANCIAL_DISCLOSURE_ID; FINANCIAL_DISCLOSURES.ID, PERSON_ID, YEAR_COL | FINANCIAL_DISCLOSURES.YEAR_COL | PERSON_ID |
| B | LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS | ID, CASE_NAME, ASSIGNED_TO_ID, COURT_ID, DATE_FILED, NATURE_OF_SUIT | DATE_FILED | ASSIGNED_TO_ID, COURT_ID |
join: FINANCIAL_DISCLOSURES.PERSON_ID = DOCKETS.ASSIGNED_TO_ID; company match is INVESTMENTS.DESCRIPTION text vs DOCKETS.CASE_NAME text (normalize via FINANCE__FED_SEC_EDGAR_COMPANY_TICKERS_EXCHANGE.COMPANY_NAME/CIK)
gap: no CIK on either side; company match is name-on-name. Place is court, not state (COURT_ID → JUSTICE__FED_COURTLISTENER_COURTS for name only).
trap: INVESTMENTS "X Bank Accounts" rows are cash, not equity (93% of the wide number); FINANCIAL_DISCLOSURES.YEAR is column-shifted text on 38,530 of 70,776 rows; use DOCKETS.ASSIGNED_TO_ID not FED_FJC_SERVICE.

### #78 — Court filings against a chain rise before Medicare fines
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_CIVIL | DEFENDANT, NATURE_OF_SUIT, FILE_DATE, DISTRICT, COUNTY | FILE_DATE | DISTRICT / COUNTY |
| B | LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_PENALTIES + HEALTH__FED_CMS_NURSING_HOME | PENALTIES.CMS_CERTIFICATION_NUMBER_CCN, PENALTY_DATE, FINE_AMOUNT, STATE; NURSING_HOME.CMS_CERTIFICATION_NUMBER_CCN, CHAIN_ID, CHAIN_NAME, COUNTY_FIPS | PENALTY_DATE | CCN → CHAIN_ID; COUNTY_FIPS |
join: IDB_CIVIL.DEFENDANT (free text) ~ NURSING_HOME.CHAIN_NAME / LEGAL_BUSINESS_NAME — name only, no CCN on the court side
gap: IDB DEFENDANT is first-named party only, not a chain key; a chain-name alias list is needed to bind the two.
trap: single-word name matches are 8% real — use multi-word chain names; JUDGMENT filled on 21% of civil cases.

### #79 — Mine fines unpaid longer under certain operators
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_VIOLATIONS | VIOLATION_NO, MINE_ID, CONTROLLER_ID, CONTROLLER_NAME, VIOLATOR_ID, VIOLATION_ISSUE_DATE, CAL_YR, PROPOSED_PENALTY, AMOUNT_DUE, AMOUNT_PAID | CAL_YR / VIOLATION_ISSUE_DATE | MINE_ID, CONTROLLER_ID |
| B | LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_MINES | MINE_ID, CURRENT_OPERATOR_ID, CURRENT_OPERATOR_NAME, STATE, FIPS_CNTY_CD | CURRENT_STATUS_DT | MINE_ID; STATE, FIPS_CNTY_CD |
join: MINE_ID (measured 13,338+ shared values)
gap: "how long unpaid" needs a payment date; only AMOUNT_DUE / AMOUNT_PAID exist — unpaid balance, not days. MINES operator is CURRENT_ only, no history.
trap: FED_MSHA_VIOLATIONS every value carries literal double quotes; 500,990 copy-paste rows flood the sweep.

### #80 — Detention contractors donate where they house detainees
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS_FULL_R2 + IMMIGRATION__FED_ICE_DETENTION_FACILITY_CODES | R2.RECIPIENT_NAME, RECIPIENT_UEI, RECIPIENT_PARENT_NAME, AWARDING_SUB_AGENCY_NAME, ACTION_DATE, FEDERAL_ACTION_OBLIGATION, PRIMARY_PLACE_OF_PERFORMANCE_STATE_CODE; CODES.DETENTION_FACILITY_NAME, STATE, COUNTY, TYPE_DETAILED | ACTION_DATE | PRIMARY_PLACE_OF_PERFORMANCE_STATE_CODE; CODES.STATE |
| B | LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS + FINANCE__FED_FEC_CANDIDATES via FINANCE__FED_FEC_CAND_CMTE_LINKAGE | INDIV.EMPLOYER, DONOR_NAME, CMTE_ID, TRANSACTION_DATE, TRANSACTION_AMT; LINKAGE.CMTE_ID, CAND_ID; CANDIDATES.CAND_OFFICE_ST, CAND_OFFICE | TRANSACTION_DATE | CAND_OFFICE_ST |
join: R2.RECIPIENT_NAME ~ INDIV.EMPLOYER (name); place = performance state = CAND_OFFICE_ST
gap: no contractor→facility key; R2 has no county FIPS (FULL has it but is capped). Operator of a facility is not a column in CODES (TYPE_DETAILED only).
trap: FEC EMPLOYER first-8-letters = firm is the join that works; INDIV_CONTRIBUTIONS is 99.99% 2023-2026, a four-year file not a series.

### #81 — Votes drift toward donors after donation, by member
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_VOTES + POLITICS__VOTEVIEW_ROLLCALLS | VOTES.ICPSR, CONGRESS, CHAMBER, ROLLNUMBER, CAST_CODE; ROLLCALLS.VOTE_DATE, BILL_NUMBER, VOTE_DESC | ROLLCALLS.VOTE_DATE | ICPSR |
| B | LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS via FINANCE__FED_FEC_CAND_CMTE_LINKAGE → POLITICS__MEMBER_FEC_ID → POLITICS__MEMBER_SPINE | INDIV.CMTE_ID, EMPLOYER, TRANSACTION_DATE, TRANSACTION_AMT; LINKAGE.CMTE_ID, CAND_ID; MEMBER_FEC_ID.FEC_ID, BIOGUIDE; MEMBER_SPINE.BIOGUIDE, ICPSR, STATE | TRANSACTION_DATE | ICPSR / BIOGUIDE; STATE |
join: INDIV.CMTE_ID → LINKAGE.CAND_ID = MEMBER_FEC_ID.FEC_ID → BIOGUIDE → MEMBER_SPINE.ICPSR = VOTES.ICPSR
gap: "toward donors" needs a donor-interest ↔ bill-subject code; none landed (no industry code on EMPLOYER, no subject on BILL_NUMBER).
trap: INDIV_CONTRIBUTIONS is 2023-2026 only; FEC_COMMITTEES repeats ids across cycles with no cycle column — join FINANCE__FED_FEC_COMMITTEES_DIM.

### #82 — Bills lobbied hardest before markup, and by whom
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.EDUCATION.EDUCATION__FED_SENATE_LDA_FILINGS | FILING_UUID, FILING_YEAR, FILING_PERIOD, CLIENT_NAME, REGISTRANT_NAME, SPECIFIC_ISSUES, INCOME, EXPENSES | FILING_YEAR | CLIENT_STATE |
| B | LIBRARY_MARTS.POLITICS.POLITICS__BILLS | CONGRESS, BILL_TYPE, BILL_NUMBER, TITLE, INTRODUCED_DATE, ADVANCED_PAST_COMMITTEE, LATEST_ACTION_DATE, SPONSOR_BIOGUIDE | INTRODUCED_DATE | none (sponsor state via SPONSOR_BIOGUIDE → POLITICS__MEMBER_SPINE.STATE) |
join: bill number parsed out of LDA.SPECIFIC_ISSUES text = BILLS.BILL_TYPE+BILL_NUMBER+CONGRESS
gap: no markup date column (only ADVANCED_PAST_COMMITTEE flag and LATEST_ACTION_DATE); bill refs sit inside free text; BILLS has no place column.
trap: LDA_FILINGS covers 1999-2010 and 2020-2021 only, 2011-2019 missing; INCOME and EXPENSES are TEXT and mutually exclusive by filer type.

### #83 — 527 groups spend most per registered voter
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.FINANCE.FINANCE__FED_IRS527_SCHEDULE_B_EXPENDITURES | FORM_ID_NUMBER, ORG_NAME, EIN, EXPENDITURE_AMOUNT, EXPENDITURE_DATE, RECIPIENT_STATE | EXPENDITURE_DATE | RECIPIENT_STATE |
| B | LIBRARY_MARTS.POLITICS.POLITICS__FED_EAC_EAVS | STATE_ABBR, FIPSCODE, JURISDICTION_NAME, A1A | none | STATE_ABBR / FIPSCODE |
join: RECIPIENT_STATE = STATE_ABBR (state roll-up)
gap: EAVS has no year column — one vintage, cannot align to expenditure year; A1A assumed = total registered (no codebook landed). Expenditure state is the recipient's, not where the ad ran.
trap: EAVS has no codebook; -99 and -88 are sentinels; Wisconsin reports by municipality. 527 Schedule A and B diverge at field 15.

### #84 — Foreign agents register before trade or arms votes
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.FOREIGN_INFLUENCE.FOREIGN_INFLUENCE__FED_FARA_BULK | REGISTRATION_NUMBER, REGISTRANT_NAME, FOREIGN_PRINCIPAL_NAME, FOREIGN_PRINCIPAL_COUNTRY, FOREIGN_PRINCIPAL_REGISTRATION_DATE, DATE_STAMPED | FOREIGN_PRINCIPAL_REGISTRATION_DATE | FOREIGN_PRINCIPAL_COUNTRY |
| B | LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_ROLLCALLS | CONGRESS, CHAMBER, ROLLNUMBER, VOTE_DATE, BILL_NUMBER, VOTE_DESC, VOTE_QUESTION | VOTE_DATE | none (country only inside VOTE_DESC text) |
join: date only (registration date vs VOTE_DATE); country requires text match on VOTE_DESC
gap: no vote subject code; "trade or arms" must be keyword-filtered from VOTE_DESC; rollcalls carry no country column.
trap: FARA Short-Form rows keep the person only in SHORT_FORM_NAME and the date only in DATE_STAMPED; one registration number carries 1,281 rows.

### #85 — Plant owners donate to regulators' overseers by state
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_4_OWNER + ENERGY__FED_EIA860_2_PLANT | OWNER.PLANT_CODE, OWNER_NAME, OWNER_STATE, PERCENT_OWNED; PLANT.PLANT_CODE, STATE, COUNTY | none (2024 vintage) | PLANT_CODE; PLANT.STATE |
| B | LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS → FINANCE__FED_FEC_CAND_CMTE_LINKAGE → POLITICS__MEMBER_FEC_ID → POLITICS__FED_CONGRESS_COMMITTEE_MEMBERSHIP | INDIV.EMPLOYER, CMTE_ID, TRANSACTION_DATE, TRANSACTION_AMT; LINKAGE.CAND_ID; MEMBER_FEC_ID.FEC_ID, BIOGUIDE, STATE; MEMBERSHIP.BIOGUIDE, COMMITTEE_NAME, CONGRESS | TRANSACTION_DATE / CONGRESS | BIOGUIDE; MEMBER_FEC_ID.STATE |
join: OWNER_NAME ~ INDIV.EMPLOYER (name); PLANT.STATE = MEMBER_FEC_ID.STATE; overseers = MEMBERSHIP.COMMITTEE_NAME filtered to energy committees
gap: EIA-860 owner file is one year (2024), no time axis on the plant side; state regulators (PUC commissioners) are not landed, only Congress committees.
trap: committee roster misses 14-35 members per congress (~4%); FEC EMPLOYER first-8-letters join.

### #86 — Lag from complaint spike to enforcement, by bank
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.CONSUMER_PROTECTION.CONSUMER_PROTECTION__FED_CFPB_COMPLAINTS | COMPLAINT_ID, COMPANY, DATE_RECEIVED, RECEIVED_MONTH, PRODUCT, ISSUE, STATE | DATE_RECEIVED | STATE; COMPANY |
| B | LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FDIC_ENFORCEMENT_ORDERS | ORDER_ID, ORDER_DATE, ORDER_YEAR, INSTITUTION_NAME, BANK_NAME, BANK_RSSD_ID, ORDER_TYPE, CMP_AMOUNT_TOTAL, BANK_STATE | ORDER_DATE | BANK_STATE; BANK_RSSD_ID |
join: CFPB.COMPANY ~ FDIC.BANK_NAME / INSTITUTION_NAME (name only)
gap: CFPB has no RSSD/charter id; FDIC covers state non-member banks only — OCC/Fed/CFPB enforcement actions not landed.
trap: "National Association" bank names are always one entity — do not split them.

### #87 — Lobbying spikes before agency rules, by how many weeks
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.EDUCATION.EDUCATION__FED_SENATE_LDA_FILINGS | FILING_YEAR, FILING_PERIOD, CLIENT_NAME, GOVERNMENT_ENTITIES, LOBBYING_ISSUES, SPECIFIC_ISSUES | FILING_YEAR (quarter via FILING_PERIOD) | GOVERNMENT_ENTITIES (agency text) |
| B | LIBRARY_MARTS.REGULATORY.REGULATORY__FED_FEDERAL_REGISTER_DOCUMENTS | DOCUMENT_NUMBER, AGENCY, AGENCIES, TYPE, PUBLICATION_DATE, IS_SIGNIFICANT, REGULATION_ID_NUMBERS | PUBLICATION_DATE | AGENCY |
join: LDA.GOVERNMENT_ENTITIES text = FR.AGENCY text
gap: LDA is quarterly, not weekly; and the two tables share no years.
trap: LDA_FILINGS 1999-2010 + 2020-2021; FEDERAL_REGISTER 2023-01 to 2026-06 — lobby-vs-rule has zero overlap.

### #88 — Judges' former firms appear most on their dockets
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_POSITIONS | PERSON_ID, POSITION_TYPE, SECTOR, ORGANIZATION_NAME, DATE_START, DATE_TERMINATION, LOCATION_STATE | DATE_START | PERSON_ID; LOCATION_STATE |
| B | LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS + JUSTICE__FED_COURTLISTENER_OPINION_CLUSTERS | DOCKETS.ID, ASSIGNED_TO_ID, DATE_FILED, COURT_ID; CLUSTERS.DOCKET_ID, ATTORNEYS, DATE_FILED | DOCKETS.DATE_FILED | ASSIGNED_TO_ID; COURT_ID |
join: POSITIONS.PERSON_ID = DOCKETS.ASSIGNED_TO_ID; firm = POSITIONS.ORGANIZATION_NAME text vs CLUSTERS.ATTORNEYS text
gap: no docket-level attorney/firm table; ATTORNEYS lives only on opinion clusters (decided cases with opinions), a small slice of dockets.
trap: common-surname case-name templates are noise; use DOCKETS.ASSIGNED_TO_ID (3,350 judges), not FED_FJC_SERVICE.

### #89 — Lobbyists who were regulators and vice versa
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.POLITICS.POLITICS__FED_SENATE_LDA_LOBBYIST_POSITIONS | LOBBYIST_ID, LOBBYIST_FIRST_NAME, LOBBYIST_LAST_NAME, COVERED_POSITION, HAS_COVERED_POSITION, REGISTRANT_NAME, CLIENT_NAME, FILING_YEAR | FILING_YEAR | COVERED_POSITION (agency text) |
| B | LIBRARY_MARTS.GOVERNANCE.GOVERNANCE__FED_REVOLVINGDOOR_PROJECT | POSITION_KEY, AGENCY, POSITION_NAME, POSITION_TYPE, INDUSTRY_SECTOR, IS_SENATE_CONFIRMED | none | AGENCY |
join: COVERED_POSITION text ~ AGENCY + POSITION_NAME text (job, not person)
gap: REVOLVINGDOOR_PROJECT lists positions, not people — no name, no year; the "vice versa" (regulator who was a lobbyist) has no named-official table. Neither side has a place column.
trap: REVOLVINGDOOR_PROJECT is_political_appointee and is_revolving_door were false on every row; POSITION_TYPE only holds 'Senate-confirmed', 'Appointive', 'nan'.

### #90 — Detention contracts grow where ICE detainers grow
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETAINERS + IMMIGRATION__FED_ICE_DETENTION_FACILITY_CODES | DETAINERS.DETAINER_PREPARE_DATE, DETENTION_FACILITY_CODE, FACILITY_STATE, FACILITY_AOR; CODES.DETENTION_FACILITY_CODE, COUNTY, STATE | DETAINER_PREPARE_DATE | DETENTION_FACILITY_CODE → CODES.COUNTY, STATE |
| B | LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS_FULL_R2 | AWARDING_SUB_AGENCY_NAME, RECIPIENT_NAME, ACTION_DATE, FEDERAL_ACTION_OBLIGATION, PRIMARY_PLACE_OF_PERFORMANCE_STATE_CODE, PRIMARY_PLACE_OF_PERFORMANCE_CITY_NAME | ACTION_DATE | PRIMARY_PLACE_OF_PERFORMANCE_STATE_CODE |
join: state (CODES.STATE = PRIMARY_PLACE_OF_PERFORMANCE_STATE_CODE); county needs CODES.COUNTY name → REFERENCE.REF__DIM_GEOGRAPHY.COUNTY_NAME/FIPS_CODE and R2 has no county at all
gap: FIPS is on neither side. R2 dropped county FIPS; FULL has PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE but is capped at 20M rows.
trap: FED_USASPENDING_CONTRACTS_FULL is exactly 20,000,000 rows — a cap, superseded by _R2 (93M).

### #91 — Immigration judges who reverse most, and who appointed
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | NOT FOUND in catalog (EOIR judge / decision / appeal table) | — | — | — |
| B | NOT FOUND in catalog (immigration-judge appointment roster) | — | — | — |
join: none found
gap: IMMIGRATION__FED_EOIR_CASES has no judge id, no decision, no BIA appeal outcome; searched JUDGE, APPEAL, BIA, EOIR, DECISION in THE_CATALOG. Immigration judges are DOJ hires, not in FJC/CourtListener judge tables.
trap: EOIR_CASE_DATA is one unparsed column — not a second dataset.

### #92 — Foreign-owned contractors win more in certain agencies
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS_FULL_R2 | RECIPIENT_UEI, RECIPIENT_NAME, RECIPIENT_PARENT_NAME, RECIPIENT_COUNTRY_NAME, FOREIGN_OWNED, AWARDING_AGENCY_NAME, AWARDING_SUB_AGENCY_NAME, FEDERAL_ACTION_OBLIGATION, ACTION_DATE, AWARD_TYPE | ACTION_DATE | RECIPIENT_UEI; RECIPIENT_STATE_CODE / PRIMARY_PLACE_OF_PERFORMANCE_STATE_CODE |
| B | LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_TOPTIER_AGENCIES | TOPTIER_CODE, AGENCY_NAME, ACTIVE_FY, OBLIGATED_AMOUNT | ACTIVE_FY | AGENCY_NAME |
join: AWARDING_AGENCY_NAME = AGENCY_NAME (name; R2 has no agency code)
gap: R2 has FOREIGN_OWNED only; DOMESTIC_OR_FOREIGN_ENTITY and AWARDING_AGENCY_CODE exist only on capped FULL. "Win" needs offers — NUMBER_OF_OFFERS_RECEIVED is on FULL, not R2.
trap: CURRENT_TOTAL_VALUE_OF_AWARD varies per transaction — money moved is FEDERAL_ACTION_OBLIGATION; R2 columns are UPPERCASE, bare names work.

### #93 — Foreign-owned contractors, defense versus health
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS_FULL_R2 (AWARDING_AGENCY_NAME = Department of Defense) | RECIPIENT_UEI, RECIPIENT_NAME, FOREIGN_OWNED, RECIPIENT_COUNTRY_NAME, FEDERAL_ACTION_OBLIGATION, ACTION_DATE, NAICS_CODE | ACTION_DATE | RECIPIENT_UEI; RECIPIENT_STATE_CODE |
| B | same table (AWARDING_AGENCY_NAME = Department of Health and Human Services) | same | ACTION_DATE | RECIPIENT_UEI; RECIPIENT_STATE_CODE |
join: one table, split on AWARDING_AGENCY_NAME; RECIPIENT_UEI shared across both halves
gap: none beyond #92 (FOREIGN_OWNED flag is the only ownership signal on R2).
trap: FULL capped at 20M, use R2; sum FEDERAL_ACTION_OBLIGATION not CURRENT_TOTAL_VALUE.

### #94 — Foreign agent filings track arms sales by country
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.FOREIGN_INFLUENCE.FOREIGN_INFLUENCE__FED_FARA_BULK | FOREIGN_PRINCIPAL_NAME, FOREIGN_PRINCIPAL_COUNTRY, COUNTRY_LOCATION_REPRESENTED, FOREIGN_PRINCIPAL_REGISTRATION_DATE, DATE_STAMPED | FOREIGN_PRINCIPAL_REGISTRATION_DATE | FOREIGN_PRINCIPAL_COUNTRY |
| B | NOT FOUND in catalog (arms sales by country — DSCA FMS notifications / State DDTC exports) | — | — | — |
join: none found
gap: searched ARMS, DSCA, FMS, WEAPON, EXPORT, DDTC in THE_CATALOG and mart catalog — nothing. Nearest: ECONOMICS__FED_FOREIGNASSISTANCE (aid, not arms) and POLITICS__INTL_OWID_MILSPEND (spend, not US sales).
trap: FARA Short-Form date only in DATE_STAMPED.

### #95 — Political nonprofits share addresses with PACs
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.POLITICS.POLITICS__IRS527_8871_ORGS | FORM_ID_NUMBER, EIN, ORGANIZATION_NAME, MAILING_ADDR1, MAILING_CITY, MAILING_STATE, MAILING_ZIP, ESTABLISHED_DATE | ESTABLISHED_DATE | MAILING_ZIP + MAILING_ADDR1 |
| B | LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_COMMITTEES | CMTE_ID, CMTE_NM, CMTE_ST1, CMTE_CITY, CMTE_ST, CMTE_ZIP, CMTE_TP, TRES_NM | none | CMTE_ZIP + CMTE_ST1 |
join: MAILING_ADDR1 + MAILING_ZIP = CMTE_ST1 + CMTE_ZIP (normalized street + ZIP)
gap: FEC_COMMITTEES has no year/cycle column; 501(c)(4) "political nonprofits" are not in 8871 (527s only) — need CORPORATE_REGISTRY__FED_IRS_EO_BMF filtered to c4 for the wider set.
trap: FED_FEC_COMMITTEES repeats 16,943 ids across cycles with no cycle column — join FINANCE__FED_FEC_COMMITTEES_DIM.

### #96 — Years from redline map to shortage-area designation
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.HOUSING.HOUSING__FED_MAPPING_INEQUALITY | HOLC_ID, FIPS, CITY, STATE, HOLC_GRADE, YEAR_MAPPED, GEOMETRY | YEAR_MAPPED | FIPS |
| B | LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_HPSA_PRIMARY_CARE | HPSA_ID, HPSA_NAME, DESIGNATION_TYPE, HPSA_SCORE, DESIGNATION_DATE, WITHDRAWN_DATE, COUNTY_FIPS_CODE, STATE_COUNTY_FIPS_CODE, HPSA_GEOGRAPHY_ID | DESIGNATION_DATE | STATE_COUNTY_FIPS_CODE |
join: MAPPING_INEQUALITY.FIPS = HPSA.STATE_COUNTY_FIPS_CODE (county), or GEOMETRY point-in-polygon on the landing GeoJSON for tract-level
gap: FIPS level on MAPPING_INEQUALITY is unstated ("FIPS geo code") — county vs place must be checked before joining; HPSA components are tracts/places, county roll-up loses the neighborhood.
trap: MAPPING_INEQUALITY mart is one polygon per (city, grade), 1,155 rows vs 10,154 in LANDING — spatial counts off the mart cover 11% of the map.

### #97 — Doctors also donors, contractors, nursing owners
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES | NPI, PROVIDER_LAST_NAME_LEGAL_NAME, PROVIDER_FIRST_NAME, PROVIDER_CREDENTIAL_TEXT, PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_STATE_NAME, PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_POSTAL_CODE, PROVIDER_ENUMERATION_DATE | PROVIDER_ENUMERATION_DATE | NPI; practice ZIP + STATE |
| B | LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS + ECONOMICS__FED_USASPENDING_CONTRACTS_FULL_R2 + HEALTH__FED_CMS_HOME_HEALTH_OWNERS | INDIV.DONOR_NAME, OCCUPATION, ZIP_CODE, STATE, TRANSACTION_DATE; R2.RECIPIENT_NAME, RECIPIENT_ZIP_4_CODE, ACTION_DATE; OWNERS.OWNER_NAME, FIRST_NAME_OWNER, LAST_NAME_OWNER, ZIP_CODE_OWNER, ASSOCIATION_DATE_OWNER, ROLE_TEXT_OWNER | TRANSACTION_DATE / ACTION_DATE / ASSOCIATION_DATE_OWNER | name + ZIP on every side |
join: name + ZIP (NPPES last/first + postal code vs DONOR_NAME + ZIP_CODE vs OWNER name + ZIP_CODE_OWNER vs RECIPIENT_NAME + RECIPIENT_ZIP_4_CODE)
gap: no nursing-home owner table — HOME_HEALTH_OWNERS is home health agencies; SKILLED_NURSING_FACILITY_ENROLLMENTS carries only ASSOCIATE_ID, no owner names. No EIN bridge from NPI to a contractor UEI.
trap: NPPES EIN column is '<UNAVAIL>' on every populated row — the NPI-to-EIN bridge does not exist; no org-to-person enrollment bridge; single-word name matches are 8% real.

### #98 — Offshore-leak names in US federal contracts
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_ENTITIES + CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_OFFICERS | ENTITIES.NODE_ID, NAME, JURISDICTION, INCORPORATION_DATE, COUNTRY_CODES, SOURCE_LEAK; OFFICERS.NODE_ID, NAME, COUNTRY_CODES | INCORPORATION_DATE (entities only) | COUNTRY_CODES (country, no state) |
| B | LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS_FULL_R2 | RECIPIENT_NAME, RECIPIENT_PARENT_NAME, HIGHLY_COMPENSATED_OFFICER_1_NAME, RECIPIENT_UEI, RECIPIENT_STATE_CODE, RECIPIENT_COUNTRY_NAME, ACTION_DATE, FEDERAL_ACTION_OBLIGATION | ACTION_DATE | RECIPIENT_UEI; RECIPIENT_STATE_CODE |
join: ENTITIES.NAME / OFFICERS.NAME ~ R2.RECIPIENT_NAME / HIGHLY_COMPENSATED_OFFICER_n_NAME (name only)
gap: OFFICERS has no year and no US place; ICIJ ADDRESSES table exists (CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_ADDRESSES) but is not linked here without RELATIONSHIPS. No shared id on either side.
trap: the 8 ICIJ "different vintage" copies were the same snapshot with different blank spellings; single-word name matches are 8% real.

### #99 — Hospital execs on boards of their own suppliers
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.HEALTH.HEALTH__HOSPITAL_OFFICER_PAY | EIN, HOSPITAL_NAME, PERSON_NAME, TITLE, IS_OFFICER, IS_TRUSTEE_OR_DIRECTOR, TAX_YEAR, HOSPITAL_STATE, TOTAL_COMPENSATION | TAX_YEAR | EIN; HOSPITAL_STATE |
| B | LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_REPORTINGOWNER + FINANCE__FED_SEC_INSIDER_SUBMISSION | REPORTINGOWNER.OWNER_NAME, OWNER_CIK, RELATIONSHIP, TITLE, STATE, ACCESSION_NUMBER; SUBMISSION.ACCESSION_NUMBER, ISSUER_CIK, ISSUER_NAME, FILING_DATE | FILING_DATE | OWNER_CIK / ISSUER_CIK; REPORTINGOWNER.STATE |
join: PERSON_NAME ~ OWNER_NAME (name only); ACCESSION_NUMBER links owner to issuer
gap: "their own suppliers" — no hospital purchasing/vendor table landed (no AP ledgers, no 990 Schedule L/Part VII-B vendor lines). Only public-company directors are visible; private suppliers invisible.
trap: 990 Part VII repeats an executive on every affiliate's return; pointer lines "SEE SCH J" restate dollars — dedupe on PERSON_NAME + EIN + TAX_YEAR.

### #100 — Universities patent on federal money, license to donor
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.SCIENCE_RESEARCH.SCIENCE_RESEARCH__FED_NIH_REPORTER + SCIENCE.SCIENCE__FED_NSF_AWARDS | NIH.CORE_PROJECT_NUM, ORG_NAME, ORG_UEI, FISCAL_YEAR, AWARD_AMOUNT, ORG_STATE, ORG_FIPS; NSF.AWARD_ID, INSTITUTION, EIN, AWARD_DATE, STATE | FISCAL_YEAR / AWARD_DATE | ORG_UEI / EIN; ORG_STATE |
| B | NOT FOUND in catalog (patents with government-interest statement; licensing deals; university donors) | — | — | — |
join: none found
gap: searched PATENT, USPTO, LICENS, IEDISON, DONOR in THE_CATALOG — only HEALTH__FED_FDA_PURPLE_BOOK.PATENT_LIST_PROVIDED (a flag). No USPTO grant table, no iEdison, no licensing, no university donor list (ECONOMICS__FED_IRS_990 gives totals, not donors).
trap: none

## Gaps summary
| # | gap | fix |
|---|---|---|
| 76 | EOIR has no judge or decision column | land EOIR tblDecision + tblJudge (or parse CASE_DATA) |
| 77 | no CIK on judge investments or dockets; name-on-name only | add a column: CIK via ticker-name match on INVESTMENTS.DESCRIPTION |
| 78 | court DEFENDANT is free text, no CCN/chain key | parse a field: chain alias list → IDB DEFENDANT |
| 79 | no payment date on MSHA violations | land a table: MSHA assessed-penalty payment history |
| 80 | R2 dropped county FIPS; no contractor→facility key | add a column: county FIPS to R2; land ICE facility-operator list |
| 81 | no donor-industry ↔ bill-subject code | land a table: industry codes for EMPLOYER (OpenSecrets style) + bill subjects |
| 82 | bill refs buried in SPECIFIC_ISSUES text; no markup date; LDA 2011-2019 missing | parse a field: bill numbers out of SPECIFIC_ISSUES; land LDA 2011-2019; land bill actions |
| 83 | EAVS has no year column; no codebook | land a table: EAVS multi-year with codebook |
| 84 | rollcalls carry no subject/country code | parse a field: VOTE_DESC keywords; land bill subjects |
| 85 | EIA-860 owner file is one vintage; no state PUC roster | land a table: EIA-860 prior years; state utility commissioners |
| 86 | CFPB COMPANY has no RSSD; only FDIC enforcement landed | land a table: OCC/Fed/CFPB enforcement; add RSSD crosswalk |
| 87 | LDA and Federal Register share no years | land a table: LDA 2022-2026 or Federal Register pre-2023 |
| 88 | no docket-level attorney/firm table | land a table: CourtListener parties/attorneys |
| 89 | RevolvingDoor lists positions not people; no named ex-officials | land a table: named appointee roster (Plum Book with names / OPM) |
| 90 | county FIPS on neither ICE nor R2 side | add a column: county FIPS to R2; map CODES.COUNTY → REF__DIM_GEOGRAPHY |
| 92 | R2 lacks agency code, entity type, offers received | add columns to R2 from FULL spec |
| 93 | same as 92 | same |
| 94 | no arms-sales table | land a table: DSCA FMS notifications by country |
| 95 | FEC_COMMITTEES has no cycle; c4 nonprofits not in 8871 | use COMMITTEES_DIM; add IRS EO BMF c4 slice |
| 96 | MAPPING_INEQUALITY FIPS level unstated; mart is 11% of polygons | parse a field: tract FIPS from landing GeoJSON; rebuild mart at neighborhood grain |
| 97 | no nursing-home owner table; NPI→EIN bridge dead | land a table: CMS SNF ownership file |
| 98 | ICIJ officers have no year or US place | join RELATIONSHIPS + ADDRESSES for country/address; add year from linked entity |
| 99 | no hospital vendor/supplier data | land a table: 990 Schedule L / hospital AP disclosures |
| 100 | no patents, licensing, or donor tables | land a table: USPTO grants with gov-interest + iEdison |

# Arc 5

# Arc 5 — WORK and THINGS — wonders #101–#125 mapped to catalog tables (metadata only, 2026-09-09)

### #101 — Injury rates jump the year after a chain buys the plant
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2023 / _2024 / _2025 | ESTABLISHMENT_ID, EIN, ESTABLISHMENT_NAME, TOTAL_INJURIES, TOTAL_HOURS_WORKED, ANNUAL_AVERAGE_EMPLOYEES | YEAR_FILING_FOR | ESTABLISHMENT_ID / EIN / ZIP_CODE |
| B | NOT FOUND in catalog (plant acquisition events) | — | — | — |
join: ESTABLISHMENT_ID across the three 300A year tables (measured, catalog joins_to); EIN change on same ESTABLISHMENT_ID = proxy for "bought"
gap: no acquisition table; searched ACQUI, MERGER, CHOW — only ENERGY__FED_EIA861_MERGERS (utilities) and FDIC failed banks. Only 3 years of 300A.
trap: 2026-09-08 — 300A COMPANY_NAME is not the company ('Facility 982'); TOTAL_HOURS_WORKED not per-establishment for multi-site filers.

### #102 — Visa sponsors carry unpaid wage judgments
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_DOL_OFLC | EMPLOYER_NAME, EMPLOYER_STATE, EMPLOYER_POSTAL_CODE, VISA_CLASS, TOTAL_WORKER_POSITIONS, WILLFUL_VIOLATOR | DECISION_DATE | EMPLOYER_NAME + EMPLOYER_POSTAL_CODE (no EIN) |
| B | NOT FOUND in catalog (WHD back-wage / enforcement) | — | — | — |
join: none found
gap: no DOL WHD table; searched WHD, BACK_WAGE, WAGE in catalog and topo map. OFLC has no EIN, so the join would be NAME@ZIP even after landing WHD.
trap: 2026-09-03 — single-word NAME@ZIP matches clear at 8%; multi-word 92%.

### #103 — Union locals shrink where county contracts grow
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.LABOR.LABOR__FED_DOL_OLMS | MEMBERS, UNION_NAME, DESIGNATION_NUMBER, FILE_NUMBER, STATE, ZIP | YEAR_COVERED | ZIP (no county FIPS) |
| B | LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS_FULL | FEDERAL_ACTION_OBLIGATION, PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE | ACTION_DATE_FISCAL_YEAR | PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE |
join: county FIPS, after OLMS ZIP → county via REFERENCE__CENSUS_CB_ZCTA GEOMETRY (spatial), no flat ZIP→county crosswalk exists
gap: OLMS has ZIP only; R2 mart (93M, wired) has no county column, FULL (has county) is capped at 20M rows.
trap: 2026-09-01 — FED_USASPENDING_CONTRACTS_FULL is exactly 20,000,000 rows, a cap; R2 supersedes it but the R2 mart carries no county FIPS.

### #104 — Mines delinquent on fines, injuries climb next year
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_VIOLATIONS | MINE_ID, PROPOSED_PENALTY, AMOUNT_DUE, AMOUNT_PAID, CONTROLLER_ID | CAL_YR | MINE_ID |
| B | LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_ACCIDENTS | MINE_ID, NO_INJURIES, DAYS_LOST, IS_FATALITY | CAL_YR | MINE_ID |
join: MINE_ID (measured 13,338 shared); LABOR__FED_MSHA_MINES gives FIPS_CNTY_CD, NO_EMPLOYEES for the rate
gap: none
trap: topo map §5 — FED_MSHA_VIOLATIONS every value carries literal double quotes; strip before casting AMOUNT_DUE.

### #105 — Visa sponsors cluster in wage-violation zips
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_DOL_OFLC | EMPLOYER_POSTAL_CODE, TOTAL_WORKER_POSITIONS, VISA_CLASS | DECISION_DATE | EMPLOYER_POSTAL_CODE |
| B | NOT FOUND in catalog (WHD wage violations by zip) | — | — | — |
join: none found (would be ZIP)
gap: same hole as #102 — no WHD table; searched WHD, BACK_WAGE, WAGE.
trap: topo map — ZIP is a geography key, groups rows, identifies nothing.

### #106 — Drug price spike after generic count drops to one
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NADAC | NDC, DRUG_DESCRIPTION, NADAC_PER_UNIT, GENERIC_NADAC_PER_UNIT, RATE_CLASSIFICATION, BRAND_TO_GENERIC_RATIO | EFFECTIVE_DATE / AS_OF_DATE | NDC (no place) |
| B | NOT FOUND in catalog (FDA NDC directory: labelers per ingredient) | — | — | — |
join: NDC (only NADAC carries NDC); HEALTH__FED_DEA_ARCOS has DRUG_NAME + LABELER_NAME but no NDC and only controlled substances
gap: no NDC directory, so "generic count" cannot be built; searched NDC, LABELER, NONPROPRIETARY. NADAC is national — no place column on either side.
trap: none

### #107 — Fast-track devices recall more than standard
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_DEVICE_510K | K_NUMBER, EXPEDITED_REVIEW_FLAG, THIRD_PARTY_FLAG, CLEARANCE_TYPE, PRODUCT_CODE, APPLICANT | DECISION_DATE | K_NUMBER; STATE |
| B | LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_DEVICE_ENFORCEMENT | K_NUMBER_LIST, PRODUCT_CODE, CLASSIFICATION, RECALLING_FIRM | RECALL_INITIATION_DATE | K_NUMBER_LIST (parse); STATE |
join: K_NUMBER = element of K_NUMBER_LIST (split the list); fallback PRODUCT_CODE both sides. HEALTH__FED_FDA_DEVICE_PMA (PMA_NUMBER, EXPEDITED_REVIEW_FLAG) for the PMA route.
gap: K_NUMBER_LIST is a packed list, needs parsing; enforcement has no PMA-number list column.
trap: 2026-09-05 — bare LANDING FED_FDA_DEVICE_510K is 88 rows, mart is 175,686; use the mart.

### #108 — Ships visit sanctioned ports then US ports
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.MARITIME.MARITIME__FED_NOAA_AIS | MMSI, IMO_NUMBER, VESSEL_NAME, LATITUDE, LONGITUDE, POSITION_GEOGRAPHY, NAV_STATUS | DATE / BASE_DATETIME | IMO_NUMBER; LATITUDE/LONGITUDE |
| B | LIBRARY_MARTS.JUSTICE.JUSTICE__FED_OFAC_SDN | IMO_NUMBER, SDN_NAME, VESSEL_FLAG, VESSEL_OWNER, PROGRAM, IS_VESSEL | none (no date) | IMO_NUMBER |
join: IMO_NUMBER (catalog: AIS IMO_NUMBER measured shared with UK sanctions list; OFAC SDN carries IMO_NUMBER)
gap: no port polygon table anywhere — searched PORT; AIS is US-waters-only (NOAA), so a foreign sanctioned-port call is never in the track. SDN has no designation date.
trap: 2026-09-05 — OFAC SDN_TYPE is the string '-0- ' for entities, not blank.

### #109 — Rail crossing crashes cluster where rail owner fined
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_FRA_CROSSING_INCIDENTS | GRADE_CROSSING_ID, RAILROAD_CODE, REPORTING_RAILROAD_HOLDING_COMPANY, TOTAL_KILLED_FORM_57, TOTAL_INJURED_FORM_57 | INCIDENT_YEAR | GRADE_CROSSING_ID; STATE_CODE + COUNTY_CODE |
| B | NOT FOUND in catalog (FRA civil penalties by railroad) | — | — | — |
join: none found (would be RAILROAD_CODE)
gap: no FRA enforcement/penalty table; searched FRA_, ENFORCEMENT, PENALTY — only EPA/MSHA/CMS penalties. ECHO fines by railroad would need a FACILITY_NAME match.
trap: none

### #110 — Shell-owned aircraft fly contractor routes
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_FAA_AIRCRAFT_REGISTRY | N_NUMBER, REGISTRANT_NAME, TYPE_REGISTRANT, STREET, CITY, STATE, ZIP_CODE | CERT_ISSUE_DATE / LAST_ACTION_DATE | N_NUMBER; ZIP_CODE |
| B | LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS_FULL_R2 | RECIPIENT_NAME, RECIPIENT_UEI, RECIPIENT_ZIP_4_CODE, PRIMARY_PLACE_OF_PERFORMANCE_STATE_CODE | ACTION_DATE | RECIPIENT_NAME + RECIPIENT_ZIP_4_CODE |
join: REGISTRANT_NAME ↔ RECIPIENT_NAME at ZIP (NAME@ZIP, fuzzy); no shared ID
gap: no flight-track table (routes) — searched AIRCRAFT, FAA; only registry and NTSB accidents. "Shell" needs a registrant-is-trust flag; TYPE_REGISTRANT is the nearest.
trap: 2026-09-03 — single-word NAME@ZIP matches clear at 8%.

### #111 — Vehicle recalls hit models sold heaviest in poorer states
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.CONSUMER_SAFETY.CONSUMER_SAFETY__FED_NHTSA_RECALLS | MAKE, MODEL, MODEL_YEAR, POTENTIALLY_AFFECTED_UNITS, CAMPNO | NOTIFICATION_DATE | MAKE+MODEL+MODEL_YEAR (no place) |
| B | LIBRARY_MARTS.CONSUMER_SAFETY.CONSUMER_SAFETY__FED_NHTSA_COMPLAINTS | MAKE, MODEL, MODEL_YEAR, STATE | DATE_RECEIVED | STATE (proxy for where the model lives) |
join: MAKE + MODEL + MODEL_YEAR; state income from LIBRARY_MARTS.FINANCE.FINANCE__FED_IRS_SOI (STATE, AGI, N_RETURNS, TAX_YEAR) on STATE
gap: no vehicle sales or registrations by state — searched VEHICLE_REG, REGISTRATION, SALES; complaint counts by state stand in for sales.
trap: topo map draft-1 table — FED_NHTSA_COMPLAINTS is 2,227,941 rows, not 2.6M.

### #112 — Ships loiter off ports before a spill report
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.MARITIME.MARITIME__FED_NOAA_AIS | MMSI, IMO_NUMBER, SPEED_OVER_GROUND, SPEED_CATEGORY, NAV_STATUS, LATITUDE, LONGITUDE, POSITION_GEOGRAPHY | BASE_DATETIME | LATITUDE/LONGITUDE |
| B | LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_USCG_NRC_INCIDENT_REPORTS | SEQNOS, CALL_TYPE, RESPONSIBLE_COMPANY, RESPONSIBLE_STATE, SOURCE | DATE_TIME_RECEIVED | RESPONSIBLE_STATE only (no incident lat/lon) |
join: none found — time window + place, but NRC extract has no incident location or vessel id
gap: NRC mart is the "secondary extract": responsible-party address, five EXTRA_COL_n, no incident lat/lon, no vessel name/IMO. Needs the full NRC file landed.
trap: none

### #113 — UK shell controls a US nursing home
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__UK_COMPANIES_HOUSE_PSC | COMPANY_NUMBER, NAME, KIND, ADDRESS_COUNTRY, COUNTRY_REGISTERED, NATURES_OF_CONTROL | NOTIFIED_ON | COMPANY_NUMBER; NAME |
| B | LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS | CCN, ORGANIZATION_NAME, AFFILIATION_ENTITY_NAME, AFFILIATION_ENTITY_ID, INCORPORATION_STATE, STATE | INCORPORATION_DATE | CCN; STATE |
join: PSC.NAME ↔ ORGANIZATION_NAME / AFFILIATION_ENTITY_NAME (name only); HEALTH__FED_CMS_NURSING_HOME adds COUNTY_FIPS, CHAIN_ID on CCN
gap: no US-side owner file names foreign parents; CMS nursing-home ownership file (owner-level) is not in the catalog — only OWNERSHIP_TYPE. Name-only bridge.
trap: 2026-09-07 — PSC stopped mid-load, ~7M of 10M+; every count is a floor. 2026-09-05 — SNF INCORPORATION_DATE maxes 2024-09, 62% filled.

### #114 — UK controllers of US firms share address with sanctions
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__UK_COMPANIES_HOUSE_PSC | NAME, ADDRESS_PREMISES, ADDRESS_LINE_1, ADDRESS_LOCALITY, ADDRESS_POSTAL_CODE, ADDRESS_COUNTRY, COUNTRY_OF_RESIDENCE | NOTIFIED_ON | ADDRESS (built from the ADDRESS_* parts) |
| B | LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_OPENSANCTIONS_DEFAULT | ID, NAME, ADDRESSES, COUNTRIES, SANCTIONS | FIRST_SEEN / LAST_SEEN | ADDRESSES (packed text) |
join: normalized address string; JUSTICE__FED_CONSOLIDATED_SCREENING_LIST.ADDRESSES as second sanctions source
gap: "of US firms" needs PSC → US company link, which is the #115 name bridge; ADDRESSES on both sanctions tables are packed multi-value text to parse.
trap: 2026-09-05 — sanctions lists carry DOB but no US address; sanctioned-name matches into US files were 100% noise on eye check.

### #115 — UK controllers also control US contractors
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__UK_COMPANIES_HOUSE_PSC | NAME, COMPANY_NUMBER, KIND, COUNTRY_OF_RESIDENCE, NATURES_OF_CONTROL | NOTIFIED_ON | COMPANY_NUMBER; NAME |
| B | LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS_FULL_R2 | RECIPIENT_UEI, RECIPIENT_NAME, RECIPIENT_PARENT_NAME, FOREIGN_OWNED, HIGHLY_COMPENSATED_OFFICER_1_NAME, RECIPIENT_STATE_CODE | ACTION_DATE | RECIPIENT_UEI; RECIPIENT_STATE_CODE |
join: PSC.NAME ↔ RECIPIENT_PARENT_NAME / HIGHLY_COMPENSATED_OFFICER_n_NAME (name only); no COMPANY_NUMBER↔UEI bridge exists
gap: no registry-number-to-UEI crosswalk (GLEIF in ECONOMICS__INTL_GLEIF could bridge via LEI but PSC carries no LEI).
trap: 2026-09-07 — PSC ~7M of 10M+, floors only. 2026-09-05 — R2 columns are UPPERCASE; the lowercase-USAspending trap does not apply.

### #116 — Offshore-leak names hold US property or nonprofits
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_OFFICERS | NODE_ID, NAME, COUNTRIES, COUNTRY_CODES, SOURCE_LEAK | none (no date) | NAME; COUNTRY_CODES |
| B | LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_IRS_EO_BMF | EIN, ORG_NAME, IN_CARE_OF, STATE, ZIP, RULING_YYYYMM | RULING_YYYYMM | EIN; STATE/ZIP |
join: OFFICERS.NAME ↔ BMF.IN_CARE_OF / ORG_NAME (name only); CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_ADDRESSES.ADDRESS via RELATIONSHIPS (NODE_ID_START/END) gives a US address to match
gap: no US property/deed table — searched DEED, PARCEL, ASSESS, PROPERTY_OWNER; nonprofit half works, property half is NOT FOUND. Officers table has no year.
trap: 2026-08-31 — the 8 ICIJ "different vintage" copies are the same snapshot with different blank spellings.

### #117 — US doctors control UK companies, what sector
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES | NPI, PROVIDER_LAST_NAME_LEGAL_NAME, PROVIDER_FIRST_NAME, PROVIDER_CREDENTIAL_TEXT, PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_STATE_NAME, HEALTHCARE_PROVIDER_TAXONOMY_CODE_1 | PROVIDER_ENUMERATION_DATE | NPI; practice STATE |
| B | LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__UK_COMPANIES_HOUSE_PSC | NAME_FORENAME, NAME_SURNAME, DOB_YEAR, COUNTRY_OF_RESIDENCE, NATIONALITY, COMPANY_NUMBER | NOTIFIED_ON | COMPANY_NUMBER; COUNTRY_OF_RESIDENCE |
join: surname + forename with COUNTRY_OF_RESIDENCE = United States (name only); COMPANY_NUMBER → CORPORATE_REGISTRY__INTL_UK_COMPANIES_HOUSE for COMPANY_CATEGORY
gap: "what sector" has no column — the UK company mart carries no SIC code (searched SIC on INTL_UK_COMPANIES_HOUSE: none). Land the SIC columns.
trap: 2026-09-05 — NPPES mart blanks deactivated NPIs (346,179 rows). 2026-09-07 — PSC ~7M of 10M+.

### #118 — Student-loan complaints rise where servicer changed
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.CONSUMER_PROTECTION.CONSUMER_PROTECTION__FED_CFPB_COMPLAINTS | COMPLAINT_ID, COMPANY, PRODUCT, SUB_PRODUCT, ISSUE, STATE, ZIP_CODE | RECEIVED_YEAR / RECEIVED_MONTH | STATE / ZIP_CODE; COMPANY |
| B | same table, prior year — COMPANY share by STATE shifts = servicer change | COMPANY, STATE | RECEIVED_YEAR | STATE |
join: STATE + RECEIVED_YEAR, self-join across years on COMPANY
gap: no servicer-assignment roster (which servicer holds which loans, by state, by year); the change is inferred from the complaint stream itself, so it is circular. Filter PRODUCT to student loan.
trap: topo map — FED_CFPB_COMPLAINTS 17.2M rows; FINANCE__FED_CFPB_COMPLAINTS is a second mart of the same source, say which one.

### #119 — Research patents track federal or donor money more
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | NOT FOUND in catalog (patents / PatentsView) | — | — | — |
| B | LIBRARY_MARTS.SCIENCE_RESEARCH.SCIENCE_RESEARCH__FED_NIH_REPORTER | ORG_NAME, ORG_UEI, ORG_STATE, ORG_FIPS, AWARD_AMOUNT | FISCAL_YEAR | ORG_UEI; ORG_FIPS |
join: none found (would be ORG_NAME/UEI on the patent assignee); donor side = LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_990 (EIN, TOTAL_REVENUE_AMT, TAX_YEAR, STATE)
gap: no patent table — searched PATENT (only Purple Book PATENT_LIST_PROVIDED flag). Also no EIN↔UEI bridge between 990 and NIH.
trap: 2026-09-07 — IRS hosts 990 XML for 2019+ only; older returns are missing.

### #120 — Operators fined, paid, fined again for same thing
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_VIOLATIONS | MINE_ID, CONTROLLER_ID, VIOLATOR_ID, SECTION_OF_ACT, PROPOSED_PENALTY, AMOUNT_PAID, VIOLATION_ISSUE_DATE | CAL_YR | MINE_ID / CONTROLLER_ID |
| B | LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_RCRA_ENFORCEMENTS | ID_NUMBER, ENFORCEMENT_TYPE, ENFORCEMENT_ACTION_DATE, FMP_AMOUNT, FSC_AMOUNT | ENFORCEMENT_ACTION_DATE | ID_NUMBER (RCRA handler) → FRS_ID via ENVIRONMENT__FED_EPA_FRS_FRS_PROGRAM_LINKS (PGM_SYS_ID, REGISTRY_ID, FIPS_CODE) |
join: within-table repeat on MINE_ID + SECTION_OF_ACT (MSHA) and ID_NUMBER + ENFORCEMENT_TYPE (RCRA); air side ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS (PGM_SYS_ID, ENF_TYPE_CODE, SETTLEMENT_ENTERED_DATE, PENALTY_AMOUNT); ENVIRONMENT__FED_EPA_ECHO holds only the LAST penalty per FRS_ID, not the series
gap: RCRA/ICIS action tables carry no place column of their own — place comes through FRS_PROGRAM_LINKS. "Same thing" = ENFORCEMENT_TYPE / SECTION_OF_ACT, not the underlying violation text.
trap: topo map §5 — MSHA VIOLATIONS values carry literal double quotes. 2026-09-08 — FRS_FACILITIES vs FRS_FRS_FACILITIES are two different files, neither contains the other.

### #121 — Zips file same complaint against same firm yearly
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.CONSUMER_PROTECTION.CONSUMER_PROTECTION__FED_CFPB_COMPLAINTS | ZIP_CODE, COMPANY, PRODUCT, ISSUE, SUB_ISSUE, COMPLAINT_ID | RECEIVED_YEAR | ZIP_CODE; COMPANY |
| B | same table, other years | ZIP_CODE, COMPANY, ISSUE | RECEIVED_YEAR | ZIP_CODE |
join: self-join on ZIP_CODE + COMPANY + ISSUE across RECEIVED_YEAR
gap: ZIP_CODE is partly masked in the public CFPB file (XXXXX / 3-digit) — check distinct count before trusting it as a place.
trap: topo map — ZIP is a geography key, not an identity.

### #122 — Counties flood, rebuild, flood again on federal money
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.HOUSING.HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS | DISASTER_NUMBER, FIPS, FLOOD_DAMAGE, FLOOD_DAMAGE_AMOUNT, IHP_AMOUNT, REPAIR_AMOUNT, REPLACEMENT_AMOUNT, FLOOD_INSURANCE | DECLARATION_DATE / APPLIED_DATE | FIPS (county) |
| B | LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_ASSISTANCE_FULL | CFDA_NUMBER, CFDA_TITLE, FEDERAL_ACTION_OBLIGATION, PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE, AWARDING_AGENCY_NAME | ACTION_DATE_FISCAL_YEAR | PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE |
join: county FIPS; repeat = same FIPS with 2+ distinct DISASTER_NUMBER
gap: no NFIP claims table (only HOUSING__FED_FEMA_NFIP_COMMUNITY_STATUS_BOOK, a participation roster); FEMA IA mart is flagged SAMPLE ONLY in the mart catalog while LANDING holds 26.3M rows — say which one.
trap: 2026-09-05 — FEMA IA FIPS is unpadded TEXT for states 01-09, 69,662 null; lpad before grouping. USAspending assistance is capped at 1M rows per year — every FY total is a floor.

### #123 — 990 hospital charity rises where wages fall
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HCRIS | PROVIDER_CCN, COST_OF_CHARITY_CARE, COST_OF_UNCOMPENSATED_CARE, TOTAL_BAD_DEBT_EXPENSE, STATE_CODE, COUNTY, ZIP_CODE | FISCAL_YEAR_END_DATE | PROVIDER_CCN; COUNTY (name text, not FIPS) |
| B | LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_BLS_QCEW | AREA_FIPS, ANNUAL_AVG_WEEKLY_WAGE, AVG_ANNUAL_PAY, YOY_WAGES_PCT_CHANGE, OWNERSHIP_CODE, INDUSTRY_CODE | YEAR | AREA_FIPS |
join: county — HCRIS COUNTY is a name, QCEW AREA_FIPS is a code; bridge via HCRIS ZIP_CODE → REFERENCE__CENSUS_CB_ZCTA GEOMETRY or STATE_CODE + county name lookup
gap: ECONOMICS__FED_IRS_990 has no charity-care column (only totals), so the "990" side is really HCRIS Worksheet S-10. No county FIPS on HCRIS.
trap: 2026-09-06 — HCRIS grain is RPT_REC_NUM; PROVIDER_CCN + year is not unique (1,186 hospital-years with 2+ reports). 2026-09-05 — HCRIS 'nan' typed as FLOAT NaN, not NULL.

### #124 — After plant count explains emissions, which operators dirtier
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_EGRID_PLANT_2022 | DOE_EIA_ORIS_PLANT_OR_FACILITY_CODE, PLANT_ANNUAL_CO2_EMISSIONS_TONS, PLANT_ANNUAL_NOX_EMISSIONS_TONS, PLANT_ANNUAL_SO2_EMISSIONS_TONS, PLANT_ANNUAL_NET_GENERATION_MWH, PLANT_PRIMARY_FUEL | DATA_YEAR | DOE_EIA_ORIS_PLANT_OR_FACILITY_CODE; PLANT_FIPS_STATE_CODE + PLANT_FIPS_COUNTY_CODE |
| B | LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_4_OWNER | PLANT_CODE, OWNER_NAME, OWNERSHIP_ID, PERCENT_OWNED, UTILITY_ID, UTILITY_NAME | none (2024 vintage, one year) | PLANT_CODE; OWNER_STATE |
join: EIA plant id — DOE_EIA_ORIS_PLANT_OR_FACILITY_CODE = PLANT_CODE (EIA_PLANT_ID, 10 tables in topo map)
gap: eGRID is 2022 only, EIA-860 owner is 2024 only — one-year cross-section, no series. Multi-year emissions: ENVIRONMENT__FED_EPA_GHGRP_EMISSION (FACILITY_ID, REPORTING_YEAR, CO2E_EMISSION) + GHGRP_FACILITY (PARENT_COMPANY, COUNTY_FIPS), but GHGRP FACILITY_ID is not the EIA plant id.
trap: none

### #125 — Workplaces with rising injury rates, by owner
| side | table | columns needed | year col | place/key col |
|---|---|---|---|---|
| A | LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2023 / _2024 / _2025 | ESTABLISHMENT_ID, EIN, ESTABLISHMENT_NAME, TOTAL_INJURIES, TOTAL_DAFW_CASES, TOTAL_HOURS_WORKED, NAICS_CODE | YEAR_FILING_FOR | ESTABLISHMENT_ID; EIN; STATE / ZIP_CODE |
| B | LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_IRS_EO_BMF | EIN, ORG_NAME, STATE | TAX_PERIOD_YYYYMM | EIN |
join: EIN (catalog: 300A EIN measured 6,414 shared with EO_BMF); BMF only names nonprofits — for-profit owner name comes from LIBRARY_RAW.LANDING.FED_DOL_FORM5500_FULL (topo/trap: 19% of OSHA EINs match)
gap: no for-profit EIN-to-owner table in marts; ECONOMICS__FED_IRS_990 covers nonprofits only. Three years is a short series for "rising".
trap: 2026-09-08 — OSHA EIN → Form 5500 matches 19.0%, not the shelf's 86-100%. 300A TOTAL_HOURS_WORKED is not per-establishment for multi-site filers.

## Gaps summary
| # | gap | fix (land a table / add a column / parse a field) |
|---|---|---|
| 101 | no plant acquisition / ownership-change table | land a table (M&A or SEC 8-K acquisitions); or derive EIN change per ESTABLISHMENT_ID across 300A years |
| 102, 105 | no DOL WHD wage-violation table | land a table (WHD enforcement data, has EIN-less employer name + zip) |
| 103 | OLMS has ZIP only; R2 mart has no county FIPS | add a column (county FIPS to R2 mart); spatial ZIP→county via CENSUS_CB_ZCTA |
| 106 | no NDC directory for generic/labeler count; NADAC has no place | land a table (FDA NDC directory) |
| 107 | K_NUMBER_LIST is a packed list | parse a field (split K_NUMBER_LIST) |
| 108 | no port polygons; AIS is US waters only; SDN has no date | land a table (world port index) — foreign port calls still not observable in NOAA AIS |
| 109 | no FRA civil-penalty table | land a table (FRA enforcement reports) |
| 110 | no flight-track / route table | land a table (flight tracks); registrant-name join is fuzzy |
| 111 | no vehicle sales or registrations by state | land a table (state registrations); complaints-by-state is the proxy |
| 112 | NRC extract lacks incident lat/lon and vessel id | land a table (full NRC incident file) |
| 113 | no owner-level nursing-home ownership file; UK↔US bridge is name only | land a table (CMS nursing home ownership) |
| 114 | ADDRESSES on sanctions tables are packed text | parse a field (ADDRESSES) |
| 115 | no COMPANY_NUMBER↔UEI bridge | add a column (LEI on PSC via GLEIF) or accept name join |
| 116 | no US property/deed table; officers have no year | land a table (county deeds / assessor) |
| 117 | UK company mart has no SIC code | add a column (SIC_CODE_1..4 from Companies House basic file) |
| 118 | no servicer-assignment roster | land a table (FSA servicer portfolio by year) |
| 119 | no patent table; no EIN↔UEI bridge | land a table (PatentsView assignee) |
| 120 | RCRA/ICIS actions carry place only via FRS_PROGRAM_LINKS; ECHO is last-penalty only | none needed — join through program links |
| 121 | CFPB ZIP_CODE partly masked | none — check distinct before use |
| 122 | no NFIP claims; FEMA IA mart flagged sample vs 26M in LANDING | land a table (NFIP claims); confirm which FEMA IA mart is full |
| 123 | HCRIS county is a name, not FIPS; 990 has no charity column | add a column (county FIPS on HCRIS) |
| 124 | eGRID 2022 and EIA-860 2024 are single years; GHGRP id ≠ EIA plant id | land a table (eGRID 2019-2023 series) |
| 125 | no for-profit EIN→owner table in marts | land a table (Form 5500 sponsor mart from LANDING.FED_DOL_FORM5500_FULL) |
