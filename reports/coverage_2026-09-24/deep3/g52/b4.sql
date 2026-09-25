-- S08 County and state population 2020 for per-capita ATF rates [pull]
SELECT c.COUNTY_FIPS::string county_fips, c.STATE_FIPS::string state_fips, s.STATE_USPS st, c.COUNTY_NAME, c.POPULATION_2020 pop
FROM LIBRARY_MARTS.CORE.DIM_COUNTY c
LEFT JOIN LIBRARY_MARTS.CORE.DIM_STATE s ON TRY_TO_NUMBER(s.STATE_FIPS::string) = TRY_TO_NUMBER(c.STATE_FIPS::string);

-- S09 CDC firearm deaths by county: every period, three firearm intents, count and rate as landed in the mart [pull]
SELECT GEOID::string geoid, ST_NAME, NAME, PERIOD::string period, INTENT, COUNT_SUP, RATE, RATE_M
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_INJURY_VIOLENCE_COUNTY
WHERE INTENT IN ('FA_Deaths','FA_Suicide','FA_Homicide');

-- S10 NICS checks: every row whose month mentions 2024 or 2025, raw, for local parsing [pull]
SELECT MONTH::string month, STATE::string state, HANDGUN, LONG_GUN, MULTIPLE, OTHER, PERMIT, PERMIT_RECHECK, PRIVATE_SALE_HANDGUN, PRIVATE_SALE_LONG_GUN, TOTALS
FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FBI_NICS_CHECKS
WHERE MONTH::string ILIKE '%2024%' OR MONTH::string ILIKE '%2025%';
