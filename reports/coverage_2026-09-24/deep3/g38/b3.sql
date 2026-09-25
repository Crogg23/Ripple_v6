-- S11 AQS: extract every site (20,994 rows) for local time and distance math
SELECT AQS_SITE_ID, STATE_CODE, COUNTY_CODE, SITE_NUMBER, LATITUDE, LONGITUDE, LAND_USE, LOCATION_SETTING,
       SITE_ESTABLISHED_DATE, SITE_CLOSED_DATE, OWNING_AGENCY, LOCAL_SITE_NAME, ADDRESS, CITY_NAME, COUNTY_NAME, STATE_NAME, CBSA_NAME, TRIBE_NAME
FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_AQS_SITES;

-- S12 TRI 2023 per facility: air and carcinogen-air pounds, coordinates, TRI's own parent name, left-joined to the corporate crosswalk
WITH t AS (
  SELECT c_3_frs_id::varchar frs, MAX(c_2_trifd) trifd, MAX(c_4_facility_name) name, MAX(c_6_city) city, MAX(c_7_county) county, MAX(c_8_st) st,
         MAX(TRY_TO_DOUBLE(c_12_latitude::string)) lat, MAX(TRY_TO_DOUBLE(c_13_longitude::string)) lon,
         MAX(c_15_parent_co_name) parent_raw, MAX(c_17_standard_parent_co_name) parent_std, MAX(c_23_industry_sector) sector,
         SUM(IFF(c_50_unit_of_measure ILIKE 'Pounds', COALESCE(TRY_TO_DOUBLE(c_51_5_1_fugitive_air::string),0)+COALESCE(TRY_TO_DOUBLE(c_52_5_2_stack_air::string),0), 0)) air_lbs,
         SUM(IFF(c_50_unit_of_measure ILIKE 'Pounds' AND c_46_carcinogen ILIKE 'Y%', COALESCE(TRY_TO_DOUBLE(c_51_5_1_fugitive_air::string),0)+COALESCE(TRY_TO_DOUBLE(c_52_5_2_stack_air::string),0), 0)) carc_air_lbs,
         COUNT(DISTINCT IFF(c_46_carcinogen ILIKE 'Y%', c_37_chemical, NULL)) carc_chems,
         MAX_BY(IFF(c_46_carcinogen ILIKE 'Y%', c_37_chemical, NULL),
                IFF(c_46_carcinogen ILIKE 'Y%' AND c_50_unit_of_measure ILIKE 'Pounds', COALESCE(TRY_TO_DOUBLE(c_51_5_1_fugitive_air::string),0)+COALESCE(TRY_TO_DOUBLE(c_52_5_2_stack_air::string),0), -1)) top_carc,
         COUNT(*) forms
  FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_BASIC_2023 GROUP BY 1)
SELECT t.*, x.FACILITY_NAME xw_fac, x.MATCHED_LEGAL_NAME, x.PARENT_LEGAL_NAME, x.MATCH_METHOD, x.PARENT_CIK, (x.EPA_REGISTRY_ID IS NOT NULL) in_xw
FROM t LEFT JOIN LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__XC_EPA_CORPORATE_CROSSWALK x ON x.EPA_REGISTRY_ID = t.frs;

-- S13 census tracts: 2020 population and population-center point, for people-near-plant counts
SELECT TRACT_GEOID, COUNTY_FIPS, POPULATION_2020, POP_CENTER_LAT, POP_CENTER_LON FROM LIBRARY_MARTS.CORE.DIM_TRACT;

-- S14 FracFocus water rows joined to their disclosure: operator, place, total base water gallons
SELECT w.WATER_SOURCE_ID, w.DISCLOSURE_ID, d.API_NUMBER, d.STATE_NAME, d.COUNTY_NAME, d.OPERATOR_NAME, w.OPERATOR_NAME w_operator, d.WELL_NAME,
       w.DESCRIPTION, w.PERCENT, d.TOTAL_BASE_WATER_VOLUME, d.TOTAL_BASE_NON_WATER_VOLUME, d.TVD, d.FF_VERSION, d.FEDERAL_WELL, d.INDIAN_WELL, d.LATITUDE, d.LONGITUDE
FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_FRACFOCUS_WATER_SOURCE w
JOIN LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_FRACFOCUS_DISCLOSURE_LIST d ON d.DISCLOSURE_ID = w.DISCLOSURE_ID;

-- S15 FracFocus: every version-4 disclosure with a has-water flag, for coverage by state and operator
SELECT d.DISCLOSURE_ID, d.API_NUMBER, d.STATE_NAME, d.COUNTY_NAME, d.OPERATOR_NAME, d.TOTAL_BASE_WATER_VOLUME, d.FF_VERSION,
       (w.DISCLOSURE_ID IS NOT NULL) has_water
FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_FRACFOCUS_DISCLOSURE_LIST d
LEFT JOIN (SELECT DISTINCT DISCLOSURE_ID FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_FRACFOCUS_WATER_SOURCE) w ON w.DISCLOSURE_ID = d.DISCLOSURE_ID
WHERE d.FF_VERSION IN ('3','4');

-- S16 FRS code tables: what the registry IDs that do not start with 110 look like
SELECT tbl, PGM_SYS_ACNRM, LEN(REGISTRY_ID) len, COUNT(*) n, MIN(REGISTRY_ID) lo, MAX(REGISTRY_ID) hi, ANY_VALUE(PGM_SYS_ID) pgm_id_eg FROM (
  SELECT 'NAICS' tbl, PGM_SYS_ACNRM, REGISTRY_ID, PGM_SYS_ID FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FRS_NAICS_CODES WHERE LEFT(REGISTRY_ID,3) <> '110'
  UNION ALL
  SELECT 'SIC', PGM_SYS_ACNRM, REGISTRY_ID, PGM_SYS_ID FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FRS_SIC_CODES WHERE LEFT(REGISTRY_ID,3) <> '110'
) GROUP BY 1,2,3 ORDER BY n DESC
