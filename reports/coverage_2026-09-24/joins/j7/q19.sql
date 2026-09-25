-- [S19] National Emissions Inventory (EIS) for GPC Muscatine, which sits on a second registry ID (110072214456), vs GPC Washington IN (110041204265): criteria pollutants by inventory year, pounds
SELECT TO_VARCHAR(REGISTRY_ID) AS REG, REPORTING_YEAR, POLLUTANT_NAME, SUM(ANNUAL_EMISSION) AS LB, COUNT(*) AS N
FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_AIR_EMISSIONS_POLL_RPT_COMBINED_EMISSIONS
WHERE TO_VARCHAR(REGISTRY_ID) IN ('110072214456','110041204265') AND PGM_SYS_ACRNM = 'EIS'
  AND POLLUTANT_NAME IN ('Sulfur dioxide','Nitrogen oxides','Volatile organic compounds','Primary PM2.5 (filterables and condensibles)','Primary PM10 (filterables and condensibles)','Carbon monoxide','Lead','Acetaldehyde','Hydrochloric acid','Mercury')
GROUP BY 1,2,3 ORDER BY 3,1,2
