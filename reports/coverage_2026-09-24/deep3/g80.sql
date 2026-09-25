-- deep3/g80: deep pass 3, 2026-09-24. Python door (connect/db.py), read-only SELECT/WITH only, QUERY_TAG 'deep3-2026-09-24'.
-- Every connection first ran: ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300; ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24'. Four connections; those pairs are not counted.
-- Tables: INVESTIGATIONS__XC_WAYBACK_REPLAY_DOJ_DEEP_PAGES, INVESTIGATIONS__INTL_LEIDEN_RUSSIAN_OPS_EUROPE, PROCUREMENT__INTL_EC_SERCOP,
--         PROCUREMENT__FED_USASPENDING_SUBAWARDS, SCIENCE_RESEARCH__XC_BIORXIV_MEDRXIV.
-- Joined: INVESTIGATIONS__XC_WAYBACK_REPLAY_DOJ_LISTING, OPEN_DATA__XC_WAYBACK_DOJ_EPSTEIN, JUSTICE__INTL_OPENSANCTIONS_DEFAULT, SCIENCE_RESEARCH__FED_RETRACTION_WATCH.
-- 11 statements (S01-S11), all below, in run order. Outputs: g80/out_Sxx.txt and g80/out_Sxx.csv. Local pandas work on the pulled rows ran no SQL.
-- Note: S06 returned 0 rows because the CDX table holds no PDF URLs (found by S09). It still counts.

-- S01 Leiden Russian ops: every row (150), to read and tally locally
SELECT * FROM LIBRARY_MARTS.INVESTIGATIONS.INVESTIGATIONS__INTL_LEIDEN_RUSSIAN_OPS_EUROPE
;

-- S02 Wayback DOJ deep pages: every row (2,542), to diff link sets across captures locally
SELECT * FROM LIBRARY_MARTS.INVESTIGATIONS.INVESTIGATIONS__XC_WAYBACK_REPLAY_DOJ_DEEP_PAGES
;

-- S03 bioRxiv/medRxiv: every row (432)
SELECT * FROM LIBRARY_MARTS.SCIENCE_RESEARCH.SCIENCE_RESEARCH__XC_BIORXIV_MEDRXIV
;

-- S04 USAspending subawards sample: every row (5,000) with RECORD_JSON, to unpack prime award and UEIs locally
SELECT * FROM LIBRARY_MARTS.PROCUREMENT.PROCUREMENT__FED_USASPENDING_SUBAWARDS
;

-- S05 Ecuador SERCOP: every row (132,995), working columns only (constants and party lists left out)
SELECT OCID, RECORD_ID, RECORD_DATE, BUYER_ID, BUYER_NAME, TENDER_ID, TENDER_TITLE, TENDER_STATUS,
       TENDER_PROCUREMENT_METHOD, TENDER_VALUE_AMOUNT, AWARD_ID, AWARD_DATE, AWARD_STATUS, AWARD_VALUE_AMOUNT,
       SUPPLIER_ID, SUPPLIER_NAME, CONTRACT_ID, CONTRACT_DATE_SIGNED, CONTRACT_VALUE_AMOUNT, PLANNING_BUDGET_AMOUNT,
       LANGUAGE, TENDER_DATE_PUBLISHED, PARTIES_ROLES, ARRAY_SIZE(SPLIT(PARTIES_ID, '|')) N_PARTIES,
       _SOURCE_RUN_ID, _INGESTED_AT
FROM LIBRARY_MARTS.PROCUREMENT.PROCUREMENT__INTL_EC_SERCOP
;

-- S06 Join: Wayback CDX captures of Data Set 10 PDFs, split at EFTA01889529 (last file the shrunken listing showed), by week and HTTP status
WITH f AS (
  SELECT TRY_TO_NUMBER(REGEXP_SUBSTR(ORIGINAL_URL, 'data[ _]?set(%20|%2520|[+])?10/efta0*([0-9]+)', 1, 1, 'ie', 2)) efta,
         CAPTURED_AT, STATUS_CODE::string status
  FROM LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__XC_WAYBACK_DOJ_EPSTEIN
  WHERE ORIGINAL_URL ILIKE '%10/EFTA%'
)
SELECT IFF(efta <= 1889529, 'A_upto_1889529', 'B_above_1889529') bucket,
       DATE_TRUNC('week', CAPTURED_AT)::date wk, status,
       COUNT(*) captures, COUNT(DISTINCT efta) files, MIN(efta) efta_min, MAX(efta) efta_max
FROM f WHERE efta IS NOT NULL
GROUP BY 1, 2, 3 ORDER BY 1, 2, 3
;

-- S07 OpenSanctions (default collection): every entity tagged with Ecuador, to match SERCOP suppliers and buyers locally on RUC/cedula digits and names
SELECT ID, ENTITY_TYPE, NAME, LEFT(ALIASES::string, 400) ALIASES, BIRTH_DATE::string BIRTH_DATE, COUNTRIES::string COUNTRIES,
       LEFT(IDENTIFIERS::string, 400) IDENTIFIERS, LEFT(SANCTIONS::string, 300) SANCTIONS, PROGRAM_IDS::string PROGRAM_IDS,
       LEFT(DATASETS::string, 300) DATASETS, FIRST_SEEN::string FIRST_SEEN, LAST_SEEN::string LAST_SEEN
FROM LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_OPENSANCTIONS_DEFAULT
WHERE COUNTRIES::string ILIKE '%ec%'
  AND REGEXP_LIKE(LOWER(COUNTRIES::string), '.*(^|[^a-z])ec([^a-z]|$).*', 's')
;

-- S08 Join: bioRxiv/medRxiv DOIs (preprint and journal) against Retraction Watch original-paper DOIs, plus how fresh Retraction Watch is
WITH b AS (
  SELECT DISTINCT LOWER(TRIM(x)) doi FROM (
    SELECT NULLIF(TRIM(PUBLISHED_DOI), '') x FROM LIBRARY_MARTS.SCIENCE_RESEARCH.SCIENCE_RESEARCH__XC_BIORXIV_MEDRXIV
    UNION ALL
    SELECT NULLIF(TRIM(DOI), '') FROM LIBRARY_MARTS.SCIENCE_RESEARCH.SCIENCE_RESEARCH__XC_BIORXIV_MEDRXIV) WHERE x IS NOT NULL
), r AS (
  SELECT LOWER(TRIM(ORIGINAL_PAPER_DOI::string)) doi, RETRACTION_DATE::string rdate, RETRACTION_NATURE::string nature, TITLE::string title
  FROM LIBRARY_MARTS.SCIENCE_RESEARCH.SCIENCE_RESEARCH__FED_RETRACTION_WATCH
)
SELECT (SELECT COUNT(*) FROM b) biorxiv_dois,
       (SELECT COUNT(*) FROM r) rw_rows,
       (SELECT MAX(TRY_TO_DATE(LEFT(rdate, 10))) FROM r) rw_max_date_iso,
       (SELECT MAX(rdate) FROM r) rw_max_text,
       (SELECT COUNT_IF(rdate ILIKE '%2026%') FROM r) rw_rows_2026,
       COUNT(r.doi) hits, ARRAY_AGG(OBJECT_CONSTRUCT('doi', b.doi, 'date', r.rdate, 'nature', r.nature, 'title', r.title)) hit_list
FROM b JOIN r ON r.doi = b.doi
;

-- S09 Wayback CDX table: what URL shapes it holds (digits collapsed to #), since S06 matched nothing
SELECT REGEXP_REPLACE(LOWER(ORIGINAL_URL), '[0-9]+', '#') shape, COUNT(*) n, COUNT(DISTINCT ORIGINAL_URL) urls,
       ANY_VALUE(ORIGINAL_URL) ex, ANY_VALUE(URLKEY) ex_key, MIN(CAPTURED_AT) t0, MAX(CAPTURED_AT) t1
FROM LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__XC_WAYBACK_DOJ_EPSTEIN
GROUP BY 1 ORDER BY 2 DESC LIMIT 60
;

-- S10 Wayback listing replay: for every captured listing page, the pager's Last page, the highest page linked, and the PDF range shown
SELECT PAGE_URL, CAPTURE_TIMESTAMP_RAW, CAPTURED_AT,
       MAX(IFF(LINK_TEXT = 'Last', TRY_TO_NUMBER(REGEXP_SUBSTR(HREF, 'page=([0-9]+)', 1, 1, 'e', 1)), NULL)) last_pg,
       MAX(TRY_TO_NUMBER(REGEXP_SUBSTR(HREF, '^[?]page=([0-9]+)$', 1, 1, 'e', 1))) max_pg_link,
       COUNT_IF(RESOLVED_URL ILIKE '%.pdf%') pdfs, COUNT(*) links,
       MIN(TRY_TO_NUMBER(REGEXP_SUBSTR(RESOLVED_URL, 'EFTA0*([0-9]+)', 1, 1, 'e', 1))) efta_min,
       MAX(TRY_TO_NUMBER(REGEXP_SUBSTR(RESOLVED_URL, 'EFTA0*([0-9]+)', 1, 1, 'e', 1))) efta_max
FROM LIBRARY_MARTS.INVESTIGATIONS.INVESTIGATIONS__XC_WAYBACK_REPLAY_DOJ_LISTING
GROUP BY 1, 2, 3 ORDER BY 1, 2
;

-- S11 Wayback CDX, data-set listing pages only: per data set and week, captures, distinct pages, highest page number captured, status mix
WITH p AS (
  SELECT TRY_TO_NUMBER(REGEXP_SUBSTR(ORIGINAL_URL, 'data-set-([0-9]+)-files', 1, 1, 'e', 1)) ds,
         TRY_TO_NUMBER(REGEXP_SUBSTR(ORIGINAL_URL, '[?&]page=([0-9]+)', 1, 1, 'e', 1)) pg,
         DATE_TRUNC('week', CAPTURED_AT)::date wk, STATUS_CODE::string st
  FROM LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__XC_WAYBACK_DOJ_EPSTEIN
  WHERE ORIGINAL_URL ILIKE '%/data-set-%-files%'
)
SELECT ds, wk, COUNT(*) captures, COUNT(DISTINCT pg) pages, MAX(pg) max_pg,
       MAX(IFF(st = '200', pg, NULL)) max_pg_200, COUNT_IF(st = '200') s200, COUNT_IF(st LIKE '3%') s3xx,
       COUNT_IF(st LIKE '4%') s4xx, COUNT_IF(st LIKE '5%') s5xx, COUNT_IF(st IS NULL OR st NOT RLIKE '[0-9]{3}') s_other
FROM p WHERE ds IS NOT NULL
GROUP BY 1, 2 ORDER BY 1, 2
;
