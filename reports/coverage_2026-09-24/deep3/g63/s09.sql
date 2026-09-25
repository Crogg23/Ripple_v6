-- S09 SERVICE_TERRITORY lookup check: key uniqueness, county name forms, filler utilities, short-form flag, the lost first row
SELECT COUNT(*) n, COUNT(DISTINCT UTILITY_NUMBER, STATE, COUNTY) keys, COUNT(DISTINCT UTILITY_NUMBER) utils, COUNT(DISTINCT STATE) states,
       COUNT(DISTINCT STATE, COUNTY) state_counties, COUNT_IF(COUNTY ILIKE '%county%' OR COUNTY ILIKE '%parish%') county_word,
       COUNT_IF(UTILITY_NUMBER = 99999 OR UTILITY_NAME ILIKE 'adjust%') filler, COUNT_IF(SHORT_FORM_FLAG = 'Y') short_y,
       COUNT_IF(NULLIF(TRIM(SHORT_FORM_FLAG),'') IS NULL) short_blank, COUNT(DISTINCT DATA_YEAR) years, MIN(DATA_YEAR) y0,
       COUNT_IF(NULLIF(TRIM(COUNTY),'') IS NULL) county_blank, COUNT(DISTINCT _SOURCE_RUN_ID) runs,
       MIN(UTILITY_NUMBER) min_util, MAX_BY(UTILITY_NAME || ' / ' || STATE || ' / ' || COUNTY, -UTILITY_NUMBER) first_util_row,
       COUNT_IF(UTILITY_NUMBER = 34 AND STATE = 'AR') city_of_abbeville_probe
FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_SERVICE_TERRITORY
