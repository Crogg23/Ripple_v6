-- S18 Affiliation: (a) the per-type cap - how many clinicians sit at exactly 1..5 facilities of one type; (b) clinicians listed per facility CCN
WITH a AS (SELECT DISTINCT facility_type, npi, ccn FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FACILITY_AFFILIATION),
w AS (SELECT facility_type, npi, COUNT(*) k FROM a GROUP BY 1,2)
SELECT 'cap' part, facility_type, k::string key_, COUNT(*) n FROM w GROUP BY 1,2,3
UNION ALL
SELECT 'ccn', facility_type, ccn, COUNT(*) FROM a GROUP BY 1,2,3
