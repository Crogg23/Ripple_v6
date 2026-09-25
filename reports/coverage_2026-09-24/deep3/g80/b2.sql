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
