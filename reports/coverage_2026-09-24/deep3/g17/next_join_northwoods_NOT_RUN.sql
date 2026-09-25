-- NOT RUN: the 35-statement budget ran out (a fresh connection needs 2 ALTER SESSION lines). Ready for the next pass.
-- S26 FEC follow the Duffy check: who is NORTHWOODS FUTURE PAC (committee master), who else funds it, and whom it spends for or against (IEs)
WITH nid AS (SELECT DISTINCT OTHER_ID id FROM LIBRARY_RAW.LANDING.FED_FEC_COMMITTEE_TO_COMMITTEE
             WHERE CMTE_ID = 'C00464339' AND UPPER(NAME) LIKE 'NORTHWOODS%' AND COALESCE(MEMO_CD, '') <> 'X'),
m AS (SELECT 'master' part, c.CMTE_ID k1, c.CMTE_NM || ' | tp ' || COALESCE(c.CMTE_TP, '') || ' dsgn ' || COALESCE(c.CMTE_DSGN, '') || ' | '
             || COALESCE(c.CMTE_CITY, '') || ' ' || COALESCE(c.CMTE_ST, '') || ' | treas ' || COALESCE(c.TRES_NM, '') || ' | cand ' || COALESCE(c.CAND_ID, '')
             || ' | cycle ' || c.CYCLE k2, 1 n, NULL::number amt, NULL::date d0, NULL::date d1
      FROM LIBRARY_MARTS.POLITICS.POLITICS__FEC_COMMITTEE c WHERE c.CMTE_ID IN (SELECT id FROM nid)),
r AS (SELECT 'itoth ' || IFF(t.CMTE_ID IN (SELECT id FROM nid), 'filed_by_northwoods', 'names_northwoods') || ' ' || t.TRANSACTION_TP part,
             IFF(t.CMTE_ID IN (SELECT id FROM nid), t.OTHER_ID, t.CMTE_ID) k1, LEFT(UPPER(t.NAME), 50) k2, COUNT(*) n,
             SUM(TRY_TO_DECIMAL(t.TRANSACTION_AMT, 18, 2)) amt, MIN(TRY_TO_DATE(t.TRANSACTION_DT, 'MMDDYYYY')) d0, MAX(TRY_TO_DATE(t.TRANSACTION_DT, 'MMDDYYYY')) d1
      FROM LIBRARY_RAW.LANDING.FED_FEC_COMMITTEE_TO_COMMITTEE t
      WHERE COALESCE(t.MEMO_CD, '') <> 'X' AND (t.CMTE_ID IN (SELECT id FROM nid) OR t.OTHER_ID IN (SELECT id FROM nid))
      GROUP BY 1, 2, 3),
ie AS (SELECT 'ie ' || COALESCE(SUP_OPP, '?') part, CAND_ID k1, LEFT(CAND_NAME, 40) || ' ' || COALESCE(CAN_OFFICE, '') || COALESCE(CAN_OFFICE_STATE, '') k2,
              COUNT(*) n, SUM(EXP_AMO) amt, MIN(TRY_TO_DATE(EXP_DATE, 'DD-MON-YY')) d0, MAX(TRY_TO_DATE(EXP_DATE, 'DD-MON-YY')) d1
       FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDEPENDENT_EXPENDITURES
       WHERE SPE_ID IN (SELECT id FROM nid) AND COALESCE(IS_SUPERSEDED::string, 'false') NOT IN ('true', 'TRUE') GROUP BY 1, 2, 3)
SELECT * FROM m
UNION ALL (SELECT * FROM r ORDER BY ABS(amt) DESC LIMIT 15)
UNION ALL (SELECT * FROM ie ORDER BY amt DESC LIMIT 10)
ORDER BY part, amt DESC NULLS LAST;
