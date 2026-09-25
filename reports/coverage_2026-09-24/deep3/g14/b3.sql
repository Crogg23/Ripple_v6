-- Q11: 118th Congress bills flagged "advanced past committee": what the latest action actually was, House vs Senate bills
SELECT BILL_TYPE,
       CASE WHEN LATEST_ACTION_TEXT ILIKE 'Referred to the Subcommittee%' THEN '1 sent to a subcommittee, nothing after'
            WHEN LATEST_ACTION_TEXT ILIKE 'Subcommittee Hearings Held%' THEN '2 subcommittee hearing'
            WHEN LATEST_STAGE = 'committee_action' THEN '3 other committee action'
            WHEN LATEST_STAGE = 'reached_floor' THEN '4 reached floor'
            ELSE '5 ' || LATEST_STAGE END AS WHAT,
       COUNT(*) AS N, SUM(IFF(SPONSOR_BIOGUIDE = 'B001302', 1, 0)) AS BIGGS
FROM LIBRARY_MARTS.POLITICS.POLITICS__BILLS
WHERE CONGRESS = 118 AND BILL_TYPE IN ('HR','S') AND ADVANCED_PAST_COMMITTEE = TRUE
GROUP BY 1, 2 ORDER BY 1, 2

-- Q12: Andy Biggs's 118th-Congress bills (B001302): first five words of the title, count, first and last introduced date
SELECT REGEXP_SUBSTR(TITLE, '^(\S+\s+){0,4}\S+') AS FIRST_WORDS, COUNT(*) AS N,
       MIN(INTRODUCED_DATE) AS FIRST_DT, MAX(INTRODUCED_DATE) AS LAST_DT, MAX(N_COSPONSORS) AS MAX_COSP,
       ANY_VALUE(LEFT(TITLE, 140)) AS EXAMPLE
FROM LIBRARY_MARTS.POLITICS.POLITICS__BILLS
WHERE CONGRESS = 118 AND SPONSOR_BIOGUIDE = 'B001302'
GROUP BY 1 ORDER BY 2 DESC LIMIT 20

-- Q13: CA lobbying firms (2001 session table) vs their own filings in the cover table: did the firms with $0 in Q1-Q2 2002 file for those quarters?
WITH f AS (
  SELECT FIRM_ID, IFF(QTR_5 = 0 AND QTR_6 = 0 AND QTR_7 > 0, 'Q1-Q2 2002 zero', 'other') AS GRP
  FROM LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_FIRM
), c AS (
  SELECT TRY_TO_NUMBER(TO_VARCHAR(FILER_ID)) AS FID, FORM_TYPE, FILING_ID,
         COALESCE(TRY_TO_DATE(LEFT(TO_VARCHAR(FROM_DATE), 10)),
                  TRY_TO_DATE(SPLIT_PART(TO_VARCHAR(FROM_DATE), ' ', 1), 'MM/DD/YYYY')) AS FD
  FROM LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_COVER
)
SELECT f.GRP, c.FORM_TYPE, YEAR(c.FD) || '-Q' || QUARTER(c.FD) AS QTR,
       COUNT(DISTINCT f.FIRM_ID) AS FIRMS, COUNT(DISTINCT c.FILING_ID) AS FILINGS,
       (SELECT COUNT(*) FROM f f2 WHERE f2.GRP = f.GRP) AS GRP_SIZE
FROM f JOIN c ON c.FID = f.FIRM_ID
WHERE YEAR(c.FD) BETWEEN 2001 AND 2002
GROUP BY 1, 2, 3 ORDER BY 1, 2, 3
