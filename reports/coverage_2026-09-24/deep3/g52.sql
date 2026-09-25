-- deep3/g52: deep pass 3, 2026-09-24. Python door (connect/db.py), read-only SELECT/WITH only, QUERY_TAG 'deep3-2026-09-24'.
-- Every connection first ran: ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300; ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24'. Those two are not counted.
-- Tables: JUSTICE__FED_COURTLISTENER_COURT_APPEALS_TO, JUSTICE__FED_ATF_FFL, JUSTICE__XC_NAGIX_DPRK_MISSILE_TESTS, JUSTICE__INTL_NTI_CNS_DPRK_MISSILE_TESTS, JUSTICE__FED_OFAC_SDN.
-- 12 statements (S01-S12), all below, in run order. S01-S05, S08-S11 are extracts; peer, building, timing and cross-source math ran locally in pandas (g52/ scratch).
-- S06 inlines 1,489 SDN vessel IMOs, 768 MMSIs and 898 call signs parsed from S05; the full text is in g52/b2.sql. Here the lists are shortened to their first entries.
-- Outputs: g52/out_Sxx.txt and g52/out_Sxx.csv.

-- S01 CourtListener appeals-to: the whole lookup [pull]
SELECT * FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_COURT_APPEALS_TO ORDER BY 1;

-- S02 ATF FFL: full extract for local peer, chain and address math [pull]
SELECT * FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_ATF_FFL;

-- S03 NAGIX DPRK missile tests: full extract [pull]
SELECT * FROM LIBRARY_MARTS.JUSTICE.JUSTICE__XC_NAGIX_DPRK_MISSILE_TESTS;

-- S04 NTI/CNS DPRK missile tests: full extract [pull]
SELECT * FROM LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_NTI_CNS_DPRK_MISSILE_TESTS;

-- S05 OFAC SDN: full extract for local profile, IMO and MMSI parsing [pull]
SELECT * FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_OFAC_SDN;

-- S06 AIS x SDN vessels: pings in U.S. waters Jan 1-8 2024 matched on IMO, MMSI or call sign (lists parsed from S05 vessel rows)
SELECT MMSI::string mmsi, IMO_NORMALIZED::string imo, CALL_SIGN::string cs, VESSEL_NAME, VESSEL_TYPE_CODE,
       IFF(IMO_NORMALIZED::string IN ('1006960','1010648','1010703', /* ... 1489 values, full list in g52/b2.sql */),1,0) m_imo,
       IFF(MMSI::string IN ('212256000','215000818','248000368', /* ... 768 values, full list in g52/b2.sql */),1,0) m_mmsi,
       IFF(UPPER(TRIM(CALL_SIGN::string)) IN ('3DBP1','3DCZ1','3E2056', /* ... 898 values, full list in g52/b2.sql */),1,0) m_cs,
       COUNT(*) pings, COUNT(DISTINCT DATE) days, MIN(BASE_DATETIME)::string first_ping, MAX(BASE_DATETIME)::string last_ping,
       ROUND(AVG(LATITUDE),3) lat, ROUND(AVG(LONGITUDE),3) lon, ROUND(MIN(LATITUDE),2) lat0, ROUND(MAX(LATITUDE),2) lat1, ROUND(MIN(LONGITUDE),2) lon0, ROUND(MAX(LONGITUDE),2) lon1,
       ROUND(MAX(SPEED_OVER_GROUND),1) max_sog, LISTAGG(DISTINCT NAV_STATUS, ',') nav, MAX(LENGTH_METERS) len_m, MAX(DRAFT_METERS) draft_m
FROM LIBRARY_MARTS.MARITIME.MARITIME__FED_NOAA_AIS
WHERE IMO_NORMALIZED::string IN ('1006960','1010648','1010703', /* ... 1489 values, full list in g52/b2.sql */) OR MMSI::string IN ('212256000','215000818','248000368', /* ... 768 values, full list in g52/b2.sql */) OR UPPER(TRIM(CALL_SIGN::string)) IN ('3DBP1','3DCZ1','3E2056', /* ... 898 values, full list in g52/b2.sql */)
GROUP BY 1,2,3,4,5,6,7,8 ORDER BY pings DESC;


-- S07 Designation timing for the 4 AIS hits (OpenSanctions first-seen, datasets, sanctions text), plus the AIS tanker denominator for the same week
WITH os AS (
  SELECT NAME, ENTITY_TYPE, FIRST_SEEN::string first_seen, LAST_CHANGE::string last_change, LEFT(DATASETS::string, 300) datasets,
         LEFT(SANCTIONS::string, 300) sanctions, LEFT(IDENTIFIERS::string, 200) ids, LEFT(ALIASES::string, 200) aliases
  FROM LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_OPENSANCTIONS_DEFAULT
  WHERE ENTITY_TYPE = 'Vessel'
    AND (IDENTIFIERS::string ILIKE ANY ('%9379698%','%9259317%','%9275660%','%9299563%') OR NAME::string ILIKE ANY ('%9379698%','%9259317%','%9275660%','%9299563%'))
), den AS (
  SELECT COUNT(DISTINCT IFF(VESSEL_TYPE_CODE BETWEEN 80 AND 89 AND IMO_NORMALIZED::string NOT IN ('0000000','0000001') AND IMO_NORMALIZED IS NOT NULL, IMO_NORMALIZED, NULL)) tanker_imos,
         COUNT(DISTINCT IFF(VESSEL_TYPE_CODE BETWEEN 80 AND 89 AND LENGTH_METERS >= 200 AND IMO_NORMALIZED::string NOT IN ('0000000','0000001') AND IMO_NORMALIZED IS NOT NULL, IMO_NORMALIZED, NULL)) big_tanker_imos,
         COUNT(DISTINCT IFF(IMO_NORMALIZED::string NOT IN ('0000000','0000001') AND IMO_NORMALIZED IS NOT NULL, IMO_NORMALIZED, NULL)) all_imos,
         MIN(DATE)::string d0, MAX(DATE)::string d1
  FROM LIBRARY_MARTS.MARITIME.MARITIME__FED_NOAA_AIS
)
SELECT os.*, den.* FROM den LEFT JOIN os ON TRUE;

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

-- S11 OpenSanctions vessels on the US SDN list: first-seen date and IMO, to date every SDN hull against the Jan 2024 AIS week [pull]
SELECT ID, NAME, FIRST_SEEN::string first_seen, REGEXP_SUBSTR(IDENTIFIERS::string, 'IMO([0-9]{7})', 1, 1, 'e', 1) imo, LEFT(DATASETS::string, 200) datasets
FROM LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_OPENSANCTIONS_DEFAULT
WHERE ENTITY_TYPE = 'Vessel' AND DATASETS::string ILIKE '%OFAC Specially Designated Nationals%';

-- S12 NICS month coverage: which years the join source actually holds (S10 found no 2024-25 rows)
SELECT REGEXP_SUBSTR(MONTH::string, '(19|20)[0-9]{2}') yr, COUNT(*) n, COUNT(DISTINCT STATE) states, MIN(MONTH::string) m0, MAX(MONTH::string) m1
FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FBI_NICS_CHECKS
GROUP BY 1 ORDER BY 1 DESC NULLS FIRST LIMIT 12;
