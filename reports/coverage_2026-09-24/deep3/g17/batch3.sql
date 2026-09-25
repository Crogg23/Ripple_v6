-- S19 FEC mirror trap: one principal committee's totals listed under two or more candidate IDs in the same cycle
WITH c AS (SELECT CAND_ID, CYCLE, MAX(PRINCIPAL_CMTE_ID) pcc, MAX(CAND_ELECTION_YR) ey
           FROM LIBRARY_MARTS.POLITICS.POLITICS__FEC_CANDIDATE GROUP BY 1, 2),
s AS (SELECT s.CYCLE, s.CAND_ID, s.CAND_NAME, s.TTL_DISB, s.TTL_RECEIPTS, s.TTL_INDIV_CONTRIB, c.pcc, c.ey
      FROM LIBRARY_MARTS.POLITICS.POLITICS__FEC_CANDIDATE_SUMMARY s JOIN c ON c.CAND_ID = s.CAND_ID AND c.CYCLE = s.CYCLE
      WHERE c.pcc IS NOT NULL),
g AS (SELECT CYCLE, pcc, COUNT(*) n, COUNT(DISTINCT TTL_DISB) nd, SUM(TTL_DISB) sd, MAX(TTL_DISB) mx,
             LISTAGG(CAND_ID || ' ' || LEFT(CAND_NAME, 22), ' | ') WITHIN GROUP (ORDER BY CAND_ID) ids FROM s GROUP BY 1, 2),
st AS (SELECT CYCLE, COUNT_IF(LEFT(CAND_ID, 1) = 'H' AND TTL_INDIV_CONTRIB > 50000 AND ey < CYCLE::int - 2) house_raising_but_stale_year,
              COUNT_IF(LEFT(CAND_ID, 1) = 'H' AND TTL_INDIV_CONTRIB > 50000) house_raising
       FROM s GROUP BY 1)
SELECT g.CYCLE, pcc, n, nd, sd, mx, ids,
       SUM(IFF(n > 1, 1, 0)) OVER (PARTITION BY g.CYCLE) shared_pccs, SUM(IFF(n > 1, n, 0)) OVER (PARTITION BY g.CYCLE) rows_in_shared,
       SUM(IFF(n > 1 AND nd = 1, 1, 0)) OVER (PARTITION BY g.CYCLE) shared_identical_money,
       SUM(IFF(n > 1, sd - mx, 0)) OVER (PARTITION BY g.CYCLE) dup_disb_dollars, SUM(sd) OVER (PARTITION BY g.CYCLE) cycle_disb,
       st.house_raising_but_stale_year, st.house_raising
FROM g JOIN st ON st.CYCLE = g.CYCLE
QUALIFY n > 1 AND ROW_NUMBER() OVER (PARTITION BY g.CYCLE ORDER BY IFF(n > 1, sd, 0) DESC) <= 8
ORDER BY g.CYCLE, sd DESC;

-- S20 FEC dormant committees: House/Senate principal committees, $0 from individuals all cycle, not declared for this cycle, one row per committee, plus gifts to candidates
WITH c AS (SELECT CAND_ID, CYCLE, MAX(PRINCIPAL_CMTE_ID) pcc, MAX(CAND_ELECTION_YR) ey, MAX(CAND_STATUS) st
           FROM LIBRARY_MARTS.POLITICS.POLITICS__FEC_CANDIDATE GROUP BY 1, 2),
s AS (SELECT s.CYCLE, s.CAND_ID, s.CAND_NAME, s.PARTY, s.INCUMBENT_CHALLENGER ic, s.TTL_RECEIPTS, s.TTL_INDIV_CONTRIB, s.TTL_DISB,
             s.TRANS_TO_AUTH, s.CASH_ON_HAND_CLOSE, s.DEBTS_OWED_BY, s.COVERAGE_END_DATE, c.pcc, c.ey, c.st
      FROM LIBRARY_MARTS.POLITICS.POLITICS__FEC_CANDIDATE_SUMMARY s JOIN c ON c.CAND_ID = s.CAND_ID AND c.CYCLE = s.CYCLE
      WHERE LEFT(s.CAND_ID, 1) IN ('H', 'S') AND c.pcc IS NOT NULL),
p AS (SELECT CYCLE, pcc, MAX(TTL_INDIV_CONTRIB) max_indiv, MAX(ey) max_ey, COUNT(*) n_ids FROM s GROUP BY 1, 2),
d AS (SELECT s.*, p.n_ids FROM s JOIN p ON p.CYCLE = s.CYCLE AND p.pcc = s.pcc
      WHERE p.max_indiv <= 0 AND p.max_ey < s.CYCLE::int AND s.TTL_DISB > 0
      QUALIFY ROW_NUMBER() OVER (PARTITION BY s.CYCLE, s.pcc ORDER BY s.TTL_DISB DESC, s.CAND_ID) = 1),
gifts AS (SELECT CMTE_ID, CYCLE, SUM(TRANSACTION_AMT) gave, COUNT(DISTINCT CAND_ID) recips, COUNT(*) gifts_n
          FROM (SELECT DISTINCT CMTE_ID, CYCLE, TRAN_ID, CAND_ID, TRANSACTION_AMT, TRANSACTION_DT
                FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_COMMITTEE_TO_CANDIDATE
                WHERE COALESCE(MEMO_CD, '') <> 'X' AND CMTE_ID IN (SELECT pcc FROM d)) GROUP BY 1, 2)
SELECT d.CYCLE, d.CAND_ID, d.CAND_NAME, d.PARTY, d.ic, d.ey, d.st, d.pcc, d.n_ids, d.TTL_RECEIPTS, d.TTL_DISB, d.TRANS_TO_AUTH,
       d.CASH_ON_HAND_CLOSE, d.DEBTS_OWED_BY, d.COVERAGE_END_DATE, g.gave, g.recips, g.gifts_n,
       COUNT(*) OVER (PARTITION BY d.CYCLE) n_dormant, MEDIAN(d.TTL_DISB) OVER (PARTITION BY d.CYCLE) med_disb,
       SUM(d.TTL_DISB) OVER (PARTITION BY d.CYCLE) tot_disb, SUM(IFF(d.TTL_DISB >= 100000, 1, 0)) OVER (PARTITION BY d.CYCLE) n_100k
FROM d LEFT JOIN gifts g ON g.CMTE_ID = d.pcc AND g.CYCLE = d.CYCLE
QUALIFY ROW_NUMBER() OVER (PARTITION BY d.CYCLE ORDER BY d.TTL_DISB DESC) <= 15
ORDER BY d.CYCLE, d.TTL_DISB DESC;

-- S21 FJC robustness: a 365-day window instead of 517, same rule-of-80 pool at day one
WITH p AS (SELECT column1 pres, column2 pparty, column3::date d0 FROM VALUES
             ('1 Reagan', 'R', '1981-01-20'), ('2 Bush41', 'R', '1989-01-20'), ('3 Clinton', 'D', '1993-01-20'), ('4 Bush43', 'R', '2001-01-20'),
             ('5 Obama', 'D', '2009-01-20'), ('6 Trump1', 'R', '2017-01-20'), ('7 Biden', 'D', '2021-01-20'), ('8 Trump2', 'R', '2025-01-20')),
s AS (SELECT LEFT(s.PARTY_OF_APPOINTING_PRESIDENT, 1) ap, s.COMMISSION_DATE cd, s.SENIOR_STATUS_DATE ssd,
             IFF(s.TERMINATION_DATE >= '2100-01-01', NULL, s.TERMINATION_DATE) td,
             GREATEST(j.BIRTH_YEAR + 65, CEIL((80 + j.BIRTH_YEAR + YEAR(s.COMMISSION_DATE)) / 2)) elig_yr
      FROM LIBRARY_MARTS.POLITICS.POLITICS__FED_FJC_SERVICE s JOIN LIBRARY_MARTS.POLITICS.POLITICS__FJC_JUDGE j ON j.NID = s.NID
      WHERE s.COURT_TYPE IN ('U.S. District Court', 'U.S. Court of Appeals') AND LEFT(s.PARTY_OF_APPOINTING_PRESIDENT, 1) IN ('R', 'D'))
SELECT p.pres, IFF(s.ap = p.pparty, 'same_party', 'other_party') who, COUNT(*) eligible,
       SUM(IFF(s.ssd >= p.d0 AND s.ssd < DATEADD(day, 365, p.d0), 1, 0)) took_365,
       ROUND(100 * SUM(IFF(s.ssd >= p.d0 AND s.ssd < DATEADD(day, 365, p.d0), 1, 0)) / COUNT(*), 1) pct_365,
       SUM(IFF(s.td >= p.d0 AND s.td < DATEADD(day, 365, p.d0) AND (s.ssd IS NULL OR s.ssd >= DATEADD(day, 365, p.d0)), 1, 0)) left_active_365
FROM p CROSS JOIN s
WHERE s.cd < p.d0 AND (s.ssd IS NULL OR s.ssd >= p.d0) AND (s.td IS NULL OR s.td >= p.d0) AND YEAR(p.d0) >= s.elig_yr
GROUP BY 1, 2 ORDER BY 1, 2 DESC;

-- S22 FJC names: Republican-appointed appeals judges eligible (rule of 80) and active on 2025-01-20, and whether they went senior by the data edge
SELECT s.JUDGE_NAME, s.COURT_NAME, s.APPOINTING_PRESIDENT, j.BIRTH_YEAR, YEAR(s.COMMISSION_DATE) commissioned, s.SENIOR_STATUS_DATE,
       IFF(s.TERMINATION_DATE >= '2100-01-01', NULL, s.TERMINATION_DATE) term_date, s.TERMINATION
FROM LIBRARY_MARTS.POLITICS.POLITICS__FED_FJC_SERVICE s JOIN LIBRARY_MARTS.POLITICS.POLITICS__FJC_JUDGE j ON j.NID = s.NID
WHERE s.COURT_TYPE = 'U.S. Court of Appeals' AND LEFT(s.PARTY_OF_APPOINTING_PRESIDENT, 1) = 'R'
  AND s.COMMISSION_DATE < '2025-01-20' AND (s.SENIOR_STATUS_DATE IS NULL OR s.SENIOR_STATUS_DATE >= '2025-01-20')
  AND (s.TERMINATION_DATE IS NULL OR s.TERMINATION_DATE >= '2025-01-20')
  AND 2025 >= GREATEST(j.BIRTH_YEAR + 65, CEIL((80 + j.BIRTH_YEAR + YEAR(s.COMMISSION_DATE)) / 2))
ORDER BY s.SENIOR_STATUS_DATE NULLS LAST, j.BIRTH_YEAR;

-- S23 TX trap check: how often the "on behalf of" name is itself a lobby shop, 2019-2026 client lines
SELECT COUNT(*) lines, COUNT(DISTINCT UPPER(TRIM(ONBEHALFNAME))) names,
       COUNT_IF(REGEXP_LIKE(UPPER(ONBEHALFNAME), '.*(GOVERNMENTAL AFFAIRS|GOVERNMENT AFFAIRS|PUBLIC AFFAIRS|STRATEGIES|CONSULTING|COMMUNICATIONS|LLP|, P\\.?C\\.?|LAW FIRM|& ASSOCIATES).*')) lobbyshop_like,
       COUNT_IF(UPPER(TRIM(ONBEHALFNAME)) = UPPER(TRIM(FILERNAME))) same_as_filer,
       COUNT_IF(ONBEHALFMAILINGADDR1 IS NULL OR TRIM(ONBEHALFMAILINGADDR1) = '') no_address,
       COUNT_IF(UPPER(ONBEHALFNAME) LIKE '%CENTERPOINT%') centerpoint_lines, COUNT_IF(UPPER(ONBEHALFNAME) LIKE '%ONCOR%') oncor_lines,
       COUNT_IF(UPPER(ONBEHALFNAME) LIKE '%AEP%' OR UPPER(ONBEHALFNAME) LIKE '%AMERICAN ELECTRIC POWER%') aep_lines,
       COUNT_IF(UPPER(ONBEHALFNAME) LIKE '%ENTERGY%') entergy_lines
FROM LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_INDIVIDUAL_REPORTING WHERE APPLICABLEYEAR >= '2019';
