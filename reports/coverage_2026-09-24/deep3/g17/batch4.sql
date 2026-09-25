-- S24 FEC where dormant money went (committee-to-committee landing file, memos dropped): both directions, 2023 on, ten dormant committees
WITH ids AS (SELECT column1 pcc, column2 who FROM VALUES
               ('C00508804', 'Sinema'), ('C00193623', 'Shelby'), ('C00464339', 'Duffy'), ('C00264101', 'Becerra'), ('C00264564', 'Menendez'),
               ('C00370056', 'Nunes'), ('C00831107', 'Porter'), ('C00709899', 'Gideon'), ('C00696153', 'Harrison'), ('C00153684', 'Tallon')),
t AS (SELECT CMTE_ID, OTHER_ID, NAME, TRANSACTION_TP, TRY_TO_DECIMAL(TRANSACTION_AMT, 18, 2) amt, TRY_TO_DATE(TRANSACTION_DT, 'MMDDYYYY') dt, SUB_ID
      FROM LIBRARY_RAW.LANDING.FED_FEC_COMMITTEE_TO_COMMITTEE
      WHERE COALESCE(MEMO_CD, '') <> 'X'
        AND (CMTE_ID IN (SELECT pcc FROM ids) OR OTHER_ID IN (SELECT pcc FROM ids))),
x AS (SELECT DISTINCT i.who, IFF(t.CMTE_ID = i.pcc, 'filed_by_dormant', 'filed_by_other_side') side, t.CMTE_ID, t.OTHER_ID,
             UPPER(t.NAME) nm, t.TRANSACTION_TP, t.amt, t.dt, t.SUB_ID
      FROM t JOIN ids i ON i.pcc = t.CMTE_ID OR i.pcc = t.OTHER_ID WHERE t.dt >= '2023-01-01')
SELECT who, side, TRANSACTION_TP, LEFT(nm, 45) counterparty, COUNT(*) n, SUM(amt) amt, MIN(dt) d0, MAX(dt) d1
FROM x GROUP BY 1, 2, 3, 4
QUALIFY ROW_NUMBER() OVER (PARTITION BY who ORDER BY ABS(SUM(amt)) DESC) <= 6
ORDER BY who, ABS(amt) DESC;

-- S25 FEC eyeball: the summary rows behind the dormant leads, every candidate ID the committee sits under, 2024 and 2026
WITH c AS (SELECT CAND_ID, CYCLE, MAX(PRINCIPAL_CMTE_ID) pcc, MAX(CAND_ELECTION_YR) ey, MAX(CAND_STATUS) st, MAX(OFFICE) office
           FROM LIBRARY_MARTS.POLITICS.POLITICS__FEC_CANDIDATE GROUP BY 1, 2)
SELECT c.pcc, s.CYCLE, s.CAND_ID, s.CAND_NAME, c.office, c.ey, c.st, s.INCUMBENT_CHALLENGER ic, s.TTL_RECEIPTS, s.TTL_INDIV_CONTRIB, s.TTL_DISB,
       s.CASH_ON_HAND_CLOSE, s.DEBTS_OWED_BY, s.COVERAGE_END_DATE
FROM LIBRARY_MARTS.POLITICS.POLITICS__FEC_CANDIDATE_SUMMARY s JOIN c ON c.CAND_ID = s.CAND_ID AND c.CYCLE = s.CYCLE
WHERE c.pcc IN ('C00508804', 'C00193623', 'C00464339', 'C00264101', 'C00264564', 'C00370056')
ORDER BY c.pcc, s.CYCLE, s.CAND_ID;
