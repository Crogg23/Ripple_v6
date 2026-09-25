-- geography for the Mississippi loss cluster: every county each Mississippi utility serves (EIA-861 service territory)
SELECT UTILITY_NUMBER, UTILITY_NAME, LISTAGG(DISTINCT COUNTY, ', ') WITHIN GROUP (ORDER BY COUNTY) counties, COUNT(DISTINCT COUNTY) n_counties
FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_SERVICE_TERRITORY WHERE STATE='MS' GROUP BY 1,2
