-- S09 USGS minerals: by development status, fill of the columns said to be empty, ID uniqueness, coordinates, newest years (S06 rerun without the missing run-id column)
SELECT DEV_STAT, COUNT(*) n, COUNT(DISTINCT DEP_ID) dep_ids, COUNT(DISTINCT MRDS_ID) mrds_ids, COUNT_IF(MRDS_ID IS NOT NULL) mrds_filled,
       COUNT_IF(NULLIF(TRIM(DATA_SOURCE_NOTES::STRING),'') IS NOT NULL) notes_filled, COUNT_IF(COMMODITY IS NOT NULL) commodity_filled,
       COUNT_IF(PRODUCTION_QUANTITY IS NOT NULL) prod_filled, COUNT_IF(NULLIF(TRIM(STATE::STRING),'') IS NOT NULL) state_filled,
       COUNT_IF(NULLIF(TRIM(FIPS::STRING),'') IS NOT NULL) fips_filled, COUNT_IF(NULLIF(TRIM(YEAR::STRING),'') IS NOT NULL) year_filled,
       COUNT_IF(LATITUDE IS NULL OR LATITUDE::STRING IN ('0','0.0','None')) lat_bad,
       MAX(TRY_TO_NUMBER(YR_LST_PRD::STRING)) max_last_prod, MAX(TRY_TO_NUMBER(DISC_YR::STRING)) max_disc,
       MAX(TRY_TO_NUMBER(YR_FST_PRD::STRING)) max_first_prod,
       COUNT_IF(TRY_TO_NUMBER(YR_LST_PRD::STRING) >= 2000) last_prod_2000plus,
       COUNT_IF(COUNTRY = 'United States') us_rows, ANY_VALUE(COM_TYPE) com_type_ex
FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_USGS_MINERALS
GROUP BY 1 ORDER BY n DESC

-- S10 GHGRP emission x facility type, 2022: which sector and gas ids belong to suppliers vs direct emitters
WITH f AS (
  SELECT FACILITY_ID, REPORTING_YEAR, FACILITY_TYPES
  FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_GHGRP_FACILITY
  WHERE NULLIF(TRIM(REPORTING_STATUS),'') IS NULL
)
SELECT e.SECTOR_ID, e.GAS_ID,
       CASE WHEN f.FACILITY_ID IS NULL THEN 'no_facility_row'
            WHEN f.FACILITY_TYPES = 'Supplier' THEN 'supplier_only'
            WHEN f.FACILITY_TYPES ILIKE '%Supplier%' THEN 'supplier_mixed'
            ELSE 'no_supplier' END cls,
       COUNT(*) n, COUNT(DISTINCT e.FACILITY_ID) fac, COUNT(DISTINCT e.SUBSECTOR_ID) subsectors,
       ROUND(SUM(e.CO2E_EMISSION)) co2e, ANY_VALUE(f.FACILITY_TYPES) type_ex
FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_GHGRP_EMISSION e
LEFT JOIN f ON f.FACILITY_ID = e.FACILITY_ID AND f.REPORTING_YEAR = e.REPORTING_YEAR
WHERE e.REPORTING_YEAR = 2022
GROUP BY 1,2,3 ORDER BY 1,2,3
