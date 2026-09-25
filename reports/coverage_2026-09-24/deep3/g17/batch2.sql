-- S11 TX clients: non-media spend on single-client reports, spend year 2019-2026 (period start), with the median client
WITH i AS (SELECT REPORT_ID::string rid, MAX(UPPER(TRIM(ONBEHALFNAME))) client, COUNT(DISTINCT UPPER(TRIM(ONBEHALFNAME))) ncl
           FROM LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_INDIVIDUAL_REPORTING GROUP BY 1),
cv AS (SELECT REPORT_INFO_IDENT::string rid, FILER_IDENT, YEAR(PERIOD_START_DT) y,
         COALESCE(TRY_TO_DECIMAL(TOTAL_EXPEND_FOOD, 18, 2), 0) food, COALESCE(TRY_TO_DECIMAL(TOTAL_EXPEND_ENTERTAINMENT, 18, 2), 0) ent,
         COALESCE(TRY_TO_DECIMAL(TOTAL_EXPEND_GIFT, 18, 2), 0) gift, COALESCE(TRY_TO_DECIMAL(TOTAL_EXPEND_TRANSPORTATION, 18, 2), 0) transp,
         COALESCE(TRY_TO_DECIMAL(TOTAL_EXPEND_EVENT, 18, 2), 0) event, COALESCE(TRY_TO_DECIMAL(TOTAL_EXPEND_AWARD, 18, 2), 0) award
       FROM LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_COVER),
j AS (SELECT i.client, cv.*, food + ent + gift + transp + event + award nonmedia FROM i JOIN cv ON cv.rid = i.rid
      WHERE i.ncl = 1 AND cv.y BETWEEN 2019 AND 2026),
agg AS (SELECT client, SUM(nonmedia) tot, SUM(food) food, SUM(ent) ent, SUM(gift) gift, SUM(transp) transp, SUM(event) event, SUM(award) award,
               COUNT(*) reports, COUNT(DISTINCT FILER_IDENT) lobbyists, MAX(nonmedia) max_report,
               SUM(IFF(y IN (2019, 2020), nonmedia, 0)) y19_20, SUM(IFF(y IN (2021, 2022), nonmedia, 0)) y21_22,
               SUM(IFF(y IN (2023, 2024), nonmedia, 0)) y23_24, SUM(IFF(y IN (2025, 2026), nonmedia, 0)) y25_26
        FROM j GROUP BY 1)
SELECT client, tot, food, ent, gift, transp, event, award, reports, lobbyists, max_report, y19_20, y21_22, y23_24, y25_26,
       MEDIAN(tot) OVER () med_client, COUNT(*) OVER () n_clients, SUM(tot) OVER () all_clients_tot
FROM agg ORDER BY tot DESC LIMIT 20;

-- S12 CA: biggest one-year drop clusters: a firm dropped by many employers (F603), a client dropped by many firms (F601)
WITH d AS (SELECT 'firm_dropped' k, UPPER(TRIM(D_LF_NAME)) nm, YEAR(EXEC_DATE) xy, FILING_ID, DEL_LF_EFF eff
           FROM LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_AMENDMENTS WHERE DEL_LF_CB = 'X'
           UNION ALL
           SELECT 'client_dropped', UPPER(TRIM(D_LE_NAML)), YEAR(EXEC_DATE), FILING_ID, DEL_LE_EFF
           FROM LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_AMENDMENTS WHERE DEL_LE_CB = 'X'),
g AS (SELECT k, nm, xy, COUNT(*) n, COUNT(DISTINCT FILING_ID) filings, MIN(eff) eff0, MAX(eff) eff1 FROM d GROUP BY 1, 2, 3)
SELECT k, nm, xy, n, filings, eff0, eff1, MEDIAN(n) OVER (PARTITION BY k) med_n, SUM(n) OVER (PARTITION BY k, xy) yr_total
FROM g QUALIFY ROW_NUMBER() OVER (PARTITION BY k ORDER BY filings DESC, n DESC) <= 12 ORDER BY k, filings DESC, n DESC;

-- S13 CA: can FILING_ID reach a filer name anywhere (COVER2, FIRM_EMPLOYER)? plus repeated drop lines across versions
WITH a AS (SELECT FILING_ID, FORM_TYPE FROM LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_AMENDMENTS),
c2 AS (SELECT FILING_ID, MAX(FORM_TYPE) f, MAX(ENTY_NAML) nm FROM LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_COVER2 GROUP BY 1),
fe AS (SELECT DISTINCT FILING_ID FROM LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_FIRM_EMPLOYER)
SELECT a.FORM_TYPE, COUNT(*) n, COUNT(c2.FILING_ID) landed_cover2, LISTAGG(DISTINCT c2.f, ',') cover2_forms, ANY_VALUE(c2.nm) sample_name,
       COUNT(fe.FILING_ID) landed_firm_employer,
       (SELECT COUNT(*) FROM (SELECT FILING_ID, UPPER(TRIM(D_LE_NAML)) x, DEL_LE_EFF FROM LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_AMENDMENTS
                              WHERE DEL_LE_CB = 'X' GROUP BY 1, 2, 3 HAVING COUNT(*) > 1)) repeated_client_drop_groups,
       (SELECT COUNT(*) FROM LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_AMENDMENTS WHERE DEL_LE_CB = 'X') client_drop_rows
FROM a LEFT JOIN c2 ON c2.FILING_ID = a.FILING_ID LEFT JOIN fe ON fe.FILING_ID = a.FILING_ID GROUP BY 1;

-- S14 FCC ham licenses: grants by year since 2005, status mix, cancel dates on non-cancelled rows, active past expiry
SELECT YEAR(GRANT_DATE) y, COUNT(*) n, COUNT_IF(RADIO_SERVICE_CODE = 'HV') vanity, COUNT_IF(LICENSE_STATUS = 'A') active,
       COUNT_IF(LICENSE_STATUS = 'E') expired, COUNT_IF(LICENSE_STATUS = 'C') cancelled, COUNT_IF(LICENSE_STATUS = 'T') terminated,
       COUNT_IF(CANCELLATION_DATE IS NOT NULL AND LICENSE_STATUS <> 'C') cancel_date_not_c, COUNT_IF(LICENSE_STATUS = 'A' AND EXPIRED_DATE < '2026-06-27') active_past_expiry,
       COUNT_IF(APPLICANT_TYPE_CODE <> 'I') non_individual, COUNT(DISTINCT FRN) frns
FROM LIBRARY_MARTS.POLITICS.POLITICS__FED_FCC_LICENSING WHERE GRANT_DATE >= '2005-01-01' GROUP BY 1 ORDER BY 1;

-- S15 FEC trap rows: no FEC_CANDIDATE match, or negative cash / receipts
WITH c AS (SELECT CAND_ID, CYCLE, MAX(CAND_ELECTION_YR) ey FROM LIBRARY_MARTS.POLITICS.POLITICS__FEC_CANDIDATE GROUP BY 1, 2)
SELECT s.CYCLE, s.CAND_ID, s.CAND_NAME, s.PARTY, s.INCUMBENT_CHALLENGER ic, s.TTL_RECEIPTS, s.TTL_DISB, s.CASH_ON_HAND_CLOSE, s.DEBTS_OWED_BY,
       s.TRANS_FROM_AUTH, s.TRANS_TO_AUTH, s.NET_RECEIPTS, s.COVERAGE_END_DATE, c.ey
FROM LIBRARY_MARTS.POLITICS.POLITICS__FEC_CANDIDATE_SUMMARY s LEFT JOIN c ON c.CAND_ID = s.CAND_ID AND c.CYCLE = s.CYCLE
WHERE c.CAND_ID IS NULL OR s.CASH_ON_HAND_CLOSE < 0 OR s.TTL_RECEIPTS < 0 OR s.TTL_DISB < 0
ORDER BY ABS(s.CASH_ON_HAND_CLOSE) DESC LIMIT 25;

-- S16 FEC zombies: House/Senate committees spending in a cycle when the candidate's last declared race was 2+ cycles back
WITH c AS (SELECT CAND_ID, CYCLE, MAX(CAND_ELECTION_YR) ey, MAX(CAND_STATUS) st, MAX(OFFICE_STATE) ost, MAX(PRINCIPAL_CMTE_ID) pcc
           FROM LIBRARY_MARTS.POLITICS.POLITICS__FEC_CANDIDATE GROUP BY 1, 2),
m AS (SELECT FEC_ID, MAX(FULL_NAME) member, MAX(LAST_TERM_TYPE) ltt FROM LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_FEC_ID GROUP BY 1),
z AS (SELECT s.*, c.ey, c.st, c.ost, c.pcc, m.member, m.ltt
      FROM LIBRARY_MARTS.POLITICS.POLITICS__FEC_CANDIDATE_SUMMARY s JOIN c ON c.CAND_ID = s.CAND_ID AND c.CYCLE = s.CYCLE
      LEFT JOIN m ON m.FEC_ID = s.CAND_ID
      WHERE c.ey < s.CYCLE::int - 2 AND LEFT(s.CAND_ID, 1) IN ('H', 'S'))
SELECT CYCLE, CAND_ID, CAND_NAME, PARTY, INCUMBENT_CHALLENGER ic, ey, st, ost, pcc, member, ltt, TTL_RECEIPTS, TTL_INDIV_CONTRIB, TTL_DISB,
       TRANS_TO_AUTH, CASH_ON_HAND_CLOSE, DEBTS_OWED_BY, COVERAGE_END_DATE,
       COUNT(*) OVER (PARTITION BY CYCLE) n_cycle, MEDIAN(TTL_DISB) OVER (PARTITION BY CYCLE) med_disb, SUM(TTL_DISB) OVER (PARTITION BY CYCLE) sum_disb,
       SUM(IFF(INCUMBENT_CHALLENGER = 'I', 1, 0)) OVER (PARTITION BY CYCLE) n_flag_incumbent,
       SUM(IFF(INCUMBENT_CHALLENGER = 'I', TTL_DISB, 0)) OVER (PARTITION BY CYCLE) disb_flag_incumbent,
       SUM(IFF(TTL_DISB >= 100000, 1, 0)) OVER (PARTITION BY CYCLE) n_over_100k
FROM z QUALIFY ROW_NUMBER() OVER (PARTITION BY CYCLE ORDER BY TTL_DISB DESC) <= 15 ORDER BY CYCLE, TTL_DISB DESC;

-- S17 FJC lag check: senior status, commissions and other exits by quarter, district + appeals, 2015 on
WITH e AS (SELECT DATE_TRUNC('quarter', SENIOR_STATUS_DATE) q, 'senior' k FROM LIBRARY_MARTS.POLITICS.POLITICS__FED_FJC_SERVICE
           WHERE SENIOR_STATUS_DATE >= '2015-01-01' AND COURT_TYPE IN ('U.S. District Court', 'U.S. Court of Appeals')
           UNION ALL
           SELECT DATE_TRUNC('quarter', COMMISSION_DATE), 'commission' FROM LIBRARY_MARTS.POLITICS.POLITICS__FED_FJC_SERVICE
           WHERE COMMISSION_DATE >= '2015-01-01' AND COURT_TYPE IN ('U.S. District Court', 'U.S. Court of Appeals')
           UNION ALL
           SELECT DATE_TRUNC('quarter', TERMINATION_DATE), 'exit_' || COALESCE(TERMINATION, '?') FROM LIBRARY_MARTS.POLITICS.POLITICS__FED_FJC_SERVICE
           WHERE TERMINATION_DATE >= '2015-01-01' AND TERMINATION_DATE < '2100-01-01' AND SENIOR_STATUS_DATE IS NULL
             AND COURT_TYPE IN ('U.S. District Court', 'U.S. Court of Appeals'))
SELECT q, COUNT_IF(k = 'senior') senior, COUNT_IF(k = 'commission') commissions, COUNT_IF(k LIKE 'exit_%') active_exits,
       LISTAGG(DISTINCT IFF(k LIKE 'exit_%', SUBSTR(k, 6), NULL), '; ') exit_kinds
FROM e GROUP BY q ORDER BY q;

-- S18 FJC selection test: same window, split by how long the judge had already been eligible, and by court type
WITH p AS (SELECT column1 pres, column2 pparty, column3::date d0 FROM VALUES
             ('1 Reagan', 'R', '1981-01-20'), ('2 Bush41', 'R', '1989-01-20'), ('3 Clinton', 'D', '1993-01-20'), ('4 Bush43', 'R', '2001-01-20'),
             ('5 Obama', 'D', '2009-01-20'), ('6 Trump1', 'R', '2017-01-20'), ('7 Biden', 'D', '2021-01-20'), ('8 Trump2', 'R', '2025-01-20')),
s AS (SELECT s.NID, LEFT(s.PARTY_OF_APPOINTING_PRESIDENT, 1) ap, s.COURT_TYPE court, s.COMMISSION_DATE cd, s.SENIOR_STATUS_DATE ssd,
             IFF(s.TERMINATION_DATE >= '2100-01-01', NULL, s.TERMINATION_DATE) td, j.BIRTH_YEAR by_,
             GREATEST(j.BIRTH_YEAR + 65, CEIL((80 + j.BIRTH_YEAR + YEAR(s.COMMISSION_DATE)) / 2)) elig_yr
      FROM LIBRARY_MARTS.POLITICS.POLITICS__FED_FJC_SERVICE s JOIN LIBRARY_MARTS.POLITICS.POLITICS__FJC_JUDGE j ON j.NID = s.NID
      WHERE s.COURT_TYPE IN ('U.S. District Court', 'U.S. Court of Appeals') AND LEFT(s.PARTY_OF_APPOINTING_PRESIDENT, 1) IN ('R', 'D')),
pool AS (SELECT p.pres, s.ap, s.court, IFF(YEAR(p.d0) - s.elig_yr <= 3, 'eligible_0_3y', 'eligible_4y_plus') b,
                IFF(s.ssd >= p.d0 AND s.ssd < DATEADD(day, 517, p.d0), 1, 0) took
         FROM p CROSS JOIN s
         WHERE s.cd < p.d0 AND (s.ssd IS NULL OR s.ssd >= p.d0) AND (s.td IS NULL OR s.td >= p.d0) AND YEAR(p.d0) >= s.elig_yr)
SELECT IFF(GROUPING(b) = 0, 'by_eligible_age', 'by_court') cut, pres, ap, b, court, COUNT(*) eligible, SUM(took) took,
       ROUND(100 * SUM(took) / COUNT(*), 1) pct
FROM pool GROUP BY GROUPING SETS ((pres, ap, b), (pres, ap, court)) ORDER BY cut, pres, ap, b, court;
