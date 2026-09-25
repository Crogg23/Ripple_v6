-- S11 OpenSanctions vessels on the US SDN list: first-seen date and IMO, to date every SDN hull against the Jan 2024 AIS week [pull]
SELECT ID, NAME, FIRST_SEEN::string first_seen, REGEXP_SUBSTR(IDENTIFIERS::string, 'IMO([0-9]{7})', 1, 1, 'e', 1) imo, LEFT(DATASETS::string, 200) datasets
FROM LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_OPENSANCTIONS_DEFAULT
WHERE ENTITY_TYPE = 'Vessel' AND DATASETS::string ILIKE '%OFAC Specially Designated Nationals%';

-- S12 NICS month coverage: which years the join source actually holds (S10 found no 2024-25 rows)
SELECT REGEXP_SUBSTR(MONTH::string, '(19|20)[0-9]{2}') yr, COUNT(*) n, COUNT(DISTINCT STATE) states, MIN(MONTH::string) m0, MAX(MONTH::string) m1
FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FBI_NICS_CHECKS
GROUP BY 1 ORDER BY 1 DESC NULLS FIRST LIMIT 12;
