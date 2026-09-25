WITH m AS (SELECT CMTE_ID, MAX(CMTE_TP) tp, MAX(CMTE_DSGN) dsgn FROM LIBRARY_MARTS.POLITICS.POLITICS__FEC_COMMITTEE GROUP BY 1),
t AS (SELECT CMTE_ID, OTHER_ID, UPPER(NAME) nm, TRANSACTION_TP tp, TRY_TO_DECIMAL(TRANSACTION_AMT, 18, 2) amt,
             TRY_TO_DATE(TRANSACTION_DT, 'MMDDYYYY') dt, SUB_ID
      FROM LIBRARY_RAW.LANDING.FED_FEC_COMMITTEE_TO_COMMITTEE WHERE COALESCE(MEMO_CD, '') <> 'X'),
g AS (SELECT t.*, gm.tp giver_tp, gm.dsgn giver_dsgn, rm.tp recip_tp, IFF(rm.CMTE_ID IS NULL, 'N', 'Y') recip_in_master
      FROM t LEFT JOIN m gm ON gm.CMTE_ID = t.CMTE_ID LEFT JOIN m rm ON rm.CMTE_ID = t.OTHER_ID
      WHERE t.tp = '24K' AND t.amt >= 100000 AND t.dt BETWEEN '2025-01-01' AND '2025-12-31'),
r AS (SELECT CMTE_ID, OTHER_ID, amt, dt FROM t
      WHERE CMTE_ID IN (SELECT OTHER_ID FROM g) AND (OTHER_ID IN (SELECT CMTE_ID FROM g) OR amt >= 100000)),
x AS (SELECT g.SUB_ID, MAX(g.CMTE_ID) giver, MAX(g.OTHER_ID) recip, MAX(g.nm) recip_name, MAX(g.amt) amt, MAX(g.dt) dt,
             MAX(g.giver_tp) giver_tp, MAX(g.giver_dsgn) giver_dsgn, MAX(g.recip_tp) recip_tp, MAX(g.recip_in_master) rim,
             MAX(IFF(r.OTHER_ID = g.CMTE_ID, 1, 0)) match_id,
             MAX(IFF(r.amt = g.amt AND ABS(DATEDIFF(day, r.dt, g.dt)) <= 45, 1, 0)) match_amt
      FROM g LEFT JOIN r ON r.CMTE_ID = g.OTHER_ID GROUP BY 1)
SELECT 'summary' part, IFF(giver_tp IN ('H', 'S'), 'giver_house_senate', 'giver_other') a, COALESCE(recip_tp, '?') b, rim c,
       IFF(recip IS NULL OR recip = '', 'no_other_id', 'has_other_id') d,
       COUNT(*) n, SUM(match_id) n_match_id, SUM(match_amt) n_match_amt, SUM(amt) amt, NULL dt
FROM x GROUP BY 1, 2, 3, 4, 5
UNION ALL
(SELECT 'hs_gift_250k', giver || ' ' || COALESCE(giver_dsgn, ''), COALESCE(recip, '') || ' tp=' || COALESCE(recip_tp, '?'), LEFT(recip_name, 50), rim,
        1, match_id, match_amt, amt, dt::string
 FROM x WHERE giver_tp IN ('H', 'S') AND amt >= 250000 ORDER BY amt DESC LIMIT 40)
