-- READ FIRST. This is a RECORD of the 5 views as they stood before the 2026-09-20 repair, not a runnable undo.
-- All 5 errored on open before the repair: their column lists no longer match the landing tables, and
-- LIBRARY_RAW.LANDING.FED_NCUA_CALL_REPORTS no longer exists. Running this DDL fails, and it has no COPY GRANTS.
-- The only meaningful undo is the two renames:
--   alter view THE_LIBRARY.CRIME_SECURITY.FBI_CRIME_STATE_MONTHLY rename to THE_LIBRARY.CRIME_SECURITY.FBI_CRIME_INCIDENTS;
--   alter view THE_LIBRARY.HEALTH.CDC_MORTALITY_BY_CAUSE_AND_SEX rename to THE_LIBRARY.HEALTH.CDC_MORTALITY_QUERIES;
-- FRIENDLY_LAYER before-rows are JSON in the comments below; restoring them is a hand UPDATE.

-- THE_LIBRARY."CRIME_SECURITY"."FBI_CRIME_INCIDENTS"
-- renamed to THE_LIBRARY."CRIME_SECURITY"."FBI_CRIME_STATE_MONTHLY": run `alter view THE_LIBRARY."CRIME_SECURITY"."FBI_CRIME_STATE_MONTHLY" rename to THE_LIBRARY."CRIME_SECURITY"."FBI_CRIME_INCIDENTS";` first
-- FRIENDLY_LAYER before: [{"OBJECT_FQN": "LIBRARY_RAW.LANDING.FED_FBI_CDE", "LANDING_FQN": "LIBRARY_RAW.LANDING.FED_FBI_CDE", "SOURCE_ID": "fed_fbi_cde", "LAYER": "landing", "FRIENDLY_SCHEMA": "CRIME_SECURITY", "FRIENDLY_NAME": "FBI_CRIME_INCIDENTS", "FRIENDLY_DOMAIN": "crime_security", "ONE_LINER": "FBI Crime Data Explorer incident schema (1-row stub -- needs a real pour before it's usable).", "COMMENT": "Meant to hold NIBRS/UCR incident-level crime data from the FBI's Crime Data Explorer: agency, offense, date, and clearance. Exactly one row landed -- this is a schema probe, not data. Don't chart it; re-pour it.", "IS_SAMPLE": "False", "ROW_COUNT": "1", "THE_LIBRARY_FQN": "THE_LIBRARY.CRIME_SECURITY.FBI_CRIME_INCIDENTS", "GENERATED_AT": "2026-07-12 12:08:40.560000"}]
create or replace view THE_LIBRARY.CRIME_SECURITY.FBI_CRIME_INCIDENTS(
	INCIDENT_ID,
	ORI,
	AGENCY_NAME,
	STATE_ABBR,
	FIPS_STATE_CODE,
	FIPS_COUNTY_CODE,
	DATA_YEAR,
	INCIDENT_DATE,
	OFFENSE_CODE,
	OFFENSE_NAME,
	OFFENSE_CATEGORY,
	CLEARED,
	VICTIM_COUNT,
	OFFENDER_COUNT,
	ARRESTEE_COUNT,
	LOCATION_TYPE,
	WEAPON_TYPE,
	BIAS_MOTIVATION,
	REPORT_TYPE,
	POPULATION_GROUP,
	NOTE,
	_INGESTED_AT,
	_SOURCE_RUN_ID,
	_SRC_SHA256
) COMMENT='Meant to hold NIBRS/UCR incident-level crime data from the FBI''s Crime Data Explorer: agency, offense, date, and clearance. Exactly one row landed -- this is a schema probe, not data. Don''t chart it; re-pour it.'
 as SELECT * FROM LIBRARY_RAW.LANDING.FED_FBI_CDE;

-- THE_LIBRARY."HEALTH"."CDC_MORTALITY_QUERIES"
-- renamed to THE_LIBRARY."HEALTH"."CDC_MORTALITY_BY_CAUSE_AND_SEX": run `alter view THE_LIBRARY."HEALTH"."CDC_MORTALITY_BY_CAUSE_AND_SEX" rename to THE_LIBRARY."HEALTH"."CDC_MORTALITY_QUERIES";` first
-- FRIENDLY_LAYER before: [{"OBJECT_FQN": "LIBRARY_RAW.LANDING.FED_CDC_WONDER", "LANDING_FQN": "LIBRARY_RAW.LANDING.FED_CDC_WONDER", "SOURCE_ID": "fed_cdc_wonder", "LAYER": "landing", "FRIENDLY_SCHEMA": "HEALTH", "FRIENDLY_NAME": "CDC_MORTALITY_QUERIES", "FRIENDLY_DOMAIN": "health_medicine", "ONE_LINER": "CDC WONDER mortality/health query results (1-row stub -- needs a real pour).", "COMMENT": "Meant to hold CDC WONDER query results -- deaths, population, crude and age-adjusted rates by group. One row landed; it's a probe of the XML API shape, not data. Re-pour with real queries before using.", "IS_SAMPLE": "False", "ROW_COUNT": "1", "THE_LIBRARY_FQN": "THE_LIBRARY.HEALTH.CDC_MORTALITY_QUERIES", "GENERATED_AT": "2026-07-12 12:08:40.560000"}]
create or replace view THE_LIBRARY.HEALTH.CDC_MORTALITY_QUERIES(
	DATABASE_ID,
	GROUP_BY_1,
	GROUP_BY_1_CODE,
	GROUP_BY_2,
	GROUP_BY_2_CODE,
	DEATHS,
	POPULATION,
	CRUDE_RATE,
	AGE_ADJUSTED_RATE,
	AGE_ADJUSTED_RATE_SE,
	AGE_ADJUSTED_RATE_CI_LOWER,
	AGE_ADJUSTED_RATE_CI_UPPER,
	ROW_TYPE,
	CAUSE_OF_DEATH_FILTER,
	QUERY_TIMESTAMP,
	RAW_XML_RESPONSE,
	_INGESTED_AT,
	_SOURCE_RUN_ID,
	_SRC_SHA256
) COMMENT='Meant to hold CDC WONDER query results -- deaths, population, crude and age-adjusted rates by group. One row landed; it''s a probe of the XML API shape, not data. Re-pour with real queries before using.'
 as SELECT * FROM LIBRARY_RAW.LANDING.FED_CDC_WONDER;

-- THE_LIBRARY."HEALTH"."VETERAN_MORTALITY_APPENDIX"
-- FRIENDLY_LAYER before: [{"OBJECT_FQN": "LIBRARY_RAW.LANDING.FED_VA_ALLCAUSE_MORTALITY", "LANDING_FQN": "LIBRARY_RAW.LANDING.FED_VA_ALLCAUSE_MORTALITY", "SOURCE_ID": "fed_va_allcause_mortality", "LAYER": "landing", "FRIENDLY_SCHEMA": "HEALTH", "FRIENDLY_NAME": "VETERAN_MORTALITY_APPENDIX", "FRIENDLY_DOMAIN": "health_medicine", "ONE_LINER": "VA all-cause death figures for veterans, 2018-2023, as extracted from a report appendix.", "COMMENT": "The all-cause mortality data appendix from a VA mental-health report, covering veteran deaths 2018-2023. Heads up: this is a raw dump of report tables -- generic column names (FIGURES_AND_TABLES, COL_1, COL_2) and only 244 rows, so it needs careful reshaping before it's usable, and it's more a supporting appendix than a clean dataset. Raw as loaded (all text); no join key. From the US Dept of Veterans Affairs.", "IS_SAMPLE": "False", "ROW_COUNT": "244", "THE_LIBRARY_FQN": "THE_LIBRARY.HEALTH.VETERAN_MORTALITY_APPENDIX", "GENERATED_AT": "2026-07-12 12:08:40.560000"}]
create or replace view THE_LIBRARY.HEALTH.VETERAN_MORTALITY_APPENDIX(
	FIGURES_AND_TABLES,
	COL_1,
	COL_2,
	INGESTED_AT,
	SOURCE_RUN_ID,
	SRC_SHA256
) COMMENT='The all-cause mortality data appendix from a VA mental-health report, covering veteran deaths 2018-2023. Heads up: this is a raw dump of report tables -- generic column names (FIGURES_AND_TABLES, COL_1, COL_2) and only 244 rows, so it needs careful reshaping before it''s usable, and it''s more a supporting appendix than a clean dataset. Raw as loaded (all text); no join key. From the US Dept of Veterans Affairs.'
 as SELECT * FROM LIBRARY_RAW.LANDING.FED_VA_ALLCAUSE_MORTALITY;

-- THE_LIBRARY."GEOGRAPHY"."TRIBAL_LANDS_GEO"
-- FRIENDLY_LAYER before: [{"OBJECT_FQN": "LIBRARY_RAW.LANDING.FED_BIA_TRIBAL_GEO", "LANDING_FQN": "LIBRARY_RAW.LANDING.FED_BIA_TRIBAL_GEO", "SOURCE_ID": "fed_bia_tribal_geo", "LAYER": "landing", "FRIENDLY_SCHEMA": "GEOGRAPHY", "FRIENDLY_NAME": "TRIBAL_LANDS_GEO", "FRIENDLY_DOMAIN": "geo_demographics", "ONE_LINER": "Bureau of Indian Affairs geospatial records of tribal lands and boundaries (100-row probe).", "COMMENT": "Tribal land and boundary records from the BIA's ArcGIS portal: layer, name, state, area, and geometry. A 100-row probe. FIPS and geometry columns make it joinable to county tables once fully poured.", "IS_SAMPLE": "False", "ROW_COUNT": "100", "THE_LIBRARY_FQN": "THE_LIBRARY.GEOGRAPHY.TRIBAL_LANDS_GEO", "GENERATED_AT": "2026-07-12 12:08:40.560000"}]
create or replace view THE_LIBRARY.GEOGRAPHY.TRIBAL_LANDS_GEO(
	OBJECTID,
	LAYER_NAME,
	NAME,
	FIPS,
	STATE,
	AREA_SQMI,
	GEOMETRY,
	DATA_SOURCE,
	LAST_UPDATED,
	_INGESTED_AT,
	_SOURCE_RUN_ID,
	_SRC_SHA256
) COMMENT='Tribal land and boundary records from the BIA''s ArcGIS portal: layer, name, state, area, and geometry. A 100-row probe. FIPS and geometry columns make it joinable to county tables once fully poured.'
 as SELECT * FROM LIBRARY_RAW.LANDING.FED_BIA_TRIBAL_GEO;

-- THE_LIBRARY."MONEY"."CREDIT_UNION_CALL_REPORTS"
-- FRIENDLY_LAYER before: [{"OBJECT_FQN": "LIBRARY_RAW.LANDING.FED_NCUA_CALL_REPORTS", "LANDING_FQN": "LIBRARY_RAW.LANDING.FED_NCUA_CALL_REPORTS", "SOURCE_ID": "fed_ncua_call_reports", "LAYER": "landing", "FRIENDLY_SCHEMA": "MONEY", "FRIENDLY_NAME": "CREDIT_UNION_CALL_REPORTS", "FRIENDLY_DOMAIN": "money_finance", "ONE_LINER": "122K quarterly call-report records for federally insured credit unions -- the financial vitals, 1994 to present.", "COMMENT": "The credit-union equivalent of bank call reports: quarterly account-level financial data for every federally insured credit union, in long format (one row per institution-quarter-account code). EIN and state columns make it joinable; the account-code layout means you filter to the metric you want, then pivot.", "IS_SAMPLE": "False", "ROW_COUNT": "121713", "THE_LIBRARY_FQN": "THE_LIBRARY.MONEY.CREDIT_UNION_CALL_REPORTS", "GENERATED_AT": "2026-07-12 12:08:40.560000"}]
create or replace view THE_LIBRARY.MONEY.CREDIT_UNION_CALL_REPORTS(
	CU_NUMBER,
	CYCLE_DATE,
	ACCT_CODE,
	ACCT_VALUE,
	CU_NAME,
	STATE,
	CITY,
	ZIP_CODE,
	EIN,
	CHARTER_TYPE,
	TABLE_NAME,
	ACCT_DESC,
	ACCT_STATUS,
	_INGESTED_AT,
	_SOURCE_RUN_ID,
	_SRC_SHA256
) COMMENT='The credit-union equivalent of bank call reports: quarterly account-level financial data for every federally insured credit union, in long format (one row per institution-quarter-account code). EIN and state columns make it joinable; the account-code layout means you filter to the metric you want, then pivot.'
 as
SELECT
    "CU_NUMBER",
    CASE WHEN TRIM("CYCLE_DATE") LIKE '%-%' OR TRIM("CYCLE_DATE") LIKE '%/%' THEN TRY_TO_DATE(TRIM("CYCLE_DATE")) END AS "CYCLE_DATE",
    "ACCT_CODE",
    TRY_TO_NUMBER(NULLIF(NULLIF(NULLIF(NULLIF(TRIM("ACCT_VALUE"),'nan'),'NaN'),'NAN'),'')) AS "ACCT_VALUE",
    "CU_NAME",
    "STATE",
    "CITY",
    "ZIP_CODE",
    "EIN",
    "CHARTER_TYPE",
    "TABLE_NAME",
    "ACCT_DESC",
    "ACCT_STATUS",
    "_INGESTED_AT",
    "_SOURCE_RUN_ID",
    "_SRC_SHA256"
FROM LIBRARY_RAW.LANDING.FED_NCUA_CALL_REPORTS;