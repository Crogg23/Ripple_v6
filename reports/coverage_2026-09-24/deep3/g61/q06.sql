-- OWNER peer test: coal units with several owners vs one owner vs operator-only. Share with a planned retirement date, by vintage.
WITH own AS (SELECT PLANT_CODE, GENERATOR_ID, COUNT(*) n_own FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_4_OWNER GROUP BY 1,2),
g AS (SELECT g.PLANT_CODE, g.GENERATOR_ID, g.NAMEPLATE_CAPACITY_MW mw, g.OPERATING_YEAR oy, g.PLANNED_RETIREMENT_YEAR ry, g.STATUS, g.SECTOR_NAME,
             CASE WHEN own.n_own>1 THEN 'joint' WHEN own.n_own=1 THEN 'one_nonop_owner' ELSE 'operator_only' END ownership
      FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_3_1_GENERATOR g
      LEFT JOIN own ON own.PLANT_CODE=g.PLANT_CODE AND own.GENERATOR_ID=g.GENERATOR_ID
      WHERE g.ENERGY_SOURCE_1 IN ('BIT','SUB','LIG','ANT','RC','WC','SGC') AND g.STATUS='OP' AND g.NAMEPLATE_CAPACITY_MW>=100)
SELECT CASE WHEN oy<1970 THEN 'a <1970' WHEN oy<1980 THEN 'b 1970s' WHEN oy<1990 THEN 'c 1980s' ELSE 'd 1990+' END vintage, ownership,
       COUNT(*) units, ROUND(SUM(mw)) mw, SUM(IFF(ry IS NOT NULL,1,0)) units_with_date, ROUND(SUM(IFF(ry IS NOT NULL,mw,0))) mw_with_date,
       ROUND(100*SUM(IFF(ry IS NOT NULL,mw,0))/SUM(mw),1) pct_mw_dated, ROUND(MEDIAN(mw)) med_mw, MIN(ry) min_ry, MAX(ry) max_ry,
       SUM(IFF(ry<=2030,1,0)) units_by_2030
FROM g GROUP BY ROLLUP(1,2) ORDER BY 1,2
