-- S07 sales to ultimate customers: whole table, the customer-count and price denominator for every join
SELECT * FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_SALES_ULT_CUST;

-- S08 reliability: whole table, outage minutes (SAIDI) and counts (SAIFI) per utility-state, the harm side
SELECT * FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_RELIABILITY;

-- S09 advanced meters: whole table, smart-meter counts per utility-state, the precondition for time-varying rates
SELECT * FROM LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_ADVANCED_METERS;
