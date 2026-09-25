-- g17: deep pass 3, 2026-09-24. Python door (connect/db.py), QUERY_TAG 'deep3-2026-09-24'. Read-only: SELECT/WITH only.
-- Tables: POLITICS__TX_LOBBY_INDIVIDUAL_REPORTING, POLITICS__CA_LOBBY_AMENDMENTS, POLITICS__FED_FCC_LICENSING,
--         POLITICS__FEC_CANDIDATE_SUMMARY, POLITICS__FED_FJC_SERVICE.
-- Budget: 33 of 35 statements = 25 SELECT/WITH + 8 ALTER SESSION (4 connections, 2 each). No statement failed.
-- (batch3 was refused once by the runner's own read-only check before any connection opened; nothing reached the warehouse.)
-- Results: g17/batch1_results.json .. batch4_results.json. Runner: g17/run.py.
-- Column types came from outputs/catalog/catalog.json, not from the warehouse.

-- ===== connection 1 (g17/batch1.sql)
ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300;
ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24';

-- S01 TX client lines: per applicable year, report-level lateness, corrections, dup client lines, cover coverage
WITH r AS (
  SELECT REPORT_ID, APPLICABLEYEAR yr, MAX(FORMTYPECD) ft, MAX(FILER_ID) filer, MIN(DUEDT) due, MIN(RECEIVEDDT) rec,
         MIN(PERIODSTARTDT) ps, COUNT(*) lines, COUNT(DISTINCT UPPER(TRIM(ONBEHALFNAME))) clients, COUNT(DISTINCT ON_BEHALF_ID) obids
  FROM LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_INDIVIDUAL_REPORTING GROUP BY 1, 2),
c AS (SELECT APPLICABLE_YEAR yr, COUNT(DISTINCT REPORT_INFO_IDENT) cover_reports, COUNT(DISTINCT FILER_IDENT) cover_filers
      FROM LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_COVER GROUP BY 1)
SELECT r.yr, COUNT(*) reports, SUM(lines) lines, SUM(obids) ob_ids, COUNT(DISTINCT filer) filers, SUM(clients) clients_on_reports,
       COUNT_IF(ft = 'CORLOBBYACT') corr_reports, COUNT_IF(rec > due) late, COUNT_IF(DATEDIFF(day, due, rec) > 30) late30,
       MEDIAN(DATEDIFF(day, due, rec)) med_days_after_due, MIN(ps) ps0, MAX(ps) ps1, MAX(due) due1, MAX(rec) rec1,
       COUNT_IF(lines > clients) reports_dup_client_lines, MAX(c.cover_reports) cover_reports, MAX(c.cover_filers) cover_filers
FROM r LEFT JOIN c ON c.yr = r.yr GROUP BY r.yr ORDER BY r.yr;

-- S02 TX join: client-line reports into TX_LOBBY_COVER on REPORT_ID = REPORT_INFO_IDENT; spend reach; single-client reports
WITH i AS (SELECT REPORT_ID::string rid, COUNT(DISTINCT UPPER(TRIM(ONBEHALFNAME))) ncl
           FROM LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_INDIVIDUAL_REPORTING GROUP BY 1),
cv AS (SELECT REPORT_INFO_IDENT::string rid, COUNT(*) n, MAX(APPLICABLE_YEAR) yr,
         MAX(COALESCE(TRY_TO_DECIMAL(TOTAL_EXPEND_TRANSPORTATION, 18, 2), 0) + COALESCE(TRY_TO_DECIMAL(TOTAL_EXPEND_FOOD, 18, 2), 0)
           + COALESCE(TRY_TO_DECIMAL(TOTAL_EXPEND_ENTERTAINMENT, 18, 2), 0) + COALESCE(TRY_TO_DECIMAL(TOTAL_EXPEND_GIFT, 18, 2), 0)
           + COALESCE(TRY_TO_DECIMAL(TOTAL_EXPEND_AWARD, 18, 2), 0) + COALESCE(TRY_TO_DECIMAL(TOTAL_EXPEND_EVENT, 18, 2), 0)) nonmedia,
         MAX(COALESCE(TRY_TO_DECIMAL(TOTAL_EXPEND_MEDIA, 18, 2), 0)) media
       FROM LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_COVER GROUP BY 1)
SELECT COUNT_IF(i.rid IS NOT NULL) i_reports, COUNT_IF(i.rid IS NOT NULL AND cv.rid IS NOT NULL) i_landed,
       COUNT_IF(cv.rid IS NOT NULL) cv_reports, COUNT_IF(cv.n > 1) cv_dup_ids,
       COUNT_IF(cv.nonmedia > 0) cv_with_nonmedia, COUNT_IF(cv.nonmedia > 0 AND i.rid IS NOT NULL) cv_nonmedia_with_client_lines,
       SUM(cv.nonmedia) nonmedia_all, SUM(IFF(i.rid IS NOT NULL, cv.nonmedia, 0)) nonmedia_on_client_reports,
       SUM(cv.media) media_all, SUM(IFF(i.rid IS NOT NULL, cv.media, 0)) media_on_client_reports,
       COUNT_IF(i.ncl = 1) single_client_reports, SUM(IFF(i.ncl = 1, cv.nonmedia, 0)) single_client_nonmedia,
       MEDIAN(i.ncl) med_clients_per_report, MAX(i.ncl) max_clients_per_report
FROM i FULL OUTER JOIN cv ON i.rid = cv.rid;

-- S03 CA Form 605 amendments: shape by form type and by signed year (GROUPING SETS), bad dates, add/drop counts
SELECT IFF(GROUPING(FORM_TYPE) = 0, 'form', 'year') cut, FORM_TYPE,
       IFF(YEAR(EXEC_DATE) BETWEEN 1995 AND 2026, YEAR(EXEC_DATE), NULL) yr,
       COUNT(*) n, COUNT(DISTINCT FILING_ID) filings, COUNT(DISTINCT FILING_ID || '|' || AMEND_ID) filing_versions,
       COUNT_IF(AMEND_ID <> '0') amended_rows, COUNT_IF(EXEC_DATE IS NULL) null_exec,
       COUNT_IF(YEAR(EXEC_DATE) < 1995 OR YEAR(EXEC_DATE) > 2026) bad_exec,
       COUNT_IF(ADD_L_CB = 'X') add_lobbyist, COUNT_IF(DEL_L_CB = 'X') drop_lobbyist,
       COUNT_IF(ADD_LE_CB = 'X') add_client, COUNT_IF(DEL_LE_CB = 'X') drop_client,
       COUNT_IF(ADD_LF_CB = 'X') add_firm, COUNT_IF(DEL_LF_CB = 'X') drop_firm, COUNT_IF(OTHER_CB = 'X') other_change,
       COUNT_IF(F606_YES = 'X') f606_yes,
       COUNT_IF(D_LE_NAML ILIKE '%ATTACH%' OR A_LE_NAML ILIKE '%ATTACH%' OR D_L_NAML ILIKE '%ATTACH%' OR A_L_NAML ILIKE '%ATTACH%') see_attachment
FROM LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_AMENDMENTS
GROUP BY GROUPING SETS ((FORM_TYPE), (IFF(YEAR(EXEC_DATE) BETWEEN 1995 AND 2026, YEAR(EXEC_DATE), NULL)))
ORDER BY cut, FORM_TYPE, yr;

-- S04 CA join: FILING_ID into CA_LOBBY_COVER; land rate by form type; sample of bad EXEC_DATE values
WITH a AS (SELECT FILING_ID, AMEND_ID, FORM_TYPE, EXEC_DATE FROM LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_AMENDMENTS),
cv AS (SELECT FILING_ID, COUNT(*) n, MAX(FILER_NAML) naml, MAX(FORM_TYPE) cv_form, MAX(ENTITY_CD) ent
       FROM LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_COVER GROUP BY 1)
SELECT a.FORM_TYPE, COUNT(*) n, COUNT(cv.FILING_ID) landed, COUNT(DISTINCT a.FILING_ID) filings,
       LISTAGG(DISTINCT cv.cv_form, ',') cv_forms,
       LISTAGG(DISTINCT IFF(YEAR(a.EXEC_DATE) < 1995 OR YEAR(a.EXEC_DATE) > 2026, a.EXEC_DATE::string, NULL), ',') bad_dates
FROM a LEFT JOIN cv ON cv.FILING_ID = a.FILING_ID GROUP BY 1;

-- S05 FCC: is it one row per license? distinct keys, status, service, EIN and phone constants
SELECT COUNT(*) n, COUNT(DISTINCT UNIQUE_SYSTEM_IDENTIFIER) usi, COUNT(DISTINCT CALL_SIGN) call_signs, COUNT(DISTINCT FRN) frns,
       COUNT(DISTINCT HASH(UNIQUE_SYSTEM_IDENTIFIER, ULS_FILE_NUMBER, CALL_SIGN, LICENSE_STATUS, RADIO_SERVICE_CODE, GRANT_DATE,
             EXPIRED_DATE, CANCELLATION_DATE, LAST_ACTION_DATE, ENTITY_NAME, FRN, ADDRESS_LINE1, CITY, STATE, ZIP_CODE)) distinct_rows,
       COUNT_IF(RADIO_SERVICE_CODE = 'HA') ha, COUNT_IF(RADIO_SERVICE_CODE = 'HV') hv,
       COUNT_IF(LICENSE_STATUS = 'A') st_a, COUNT_IF(LICENSE_STATUS = 'E') st_e, COUNT_IF(LICENSE_STATUS = 'C') st_c, COUNT_IF(LICENSE_STATUS = 'T') st_t,
       COUNT(DISTINCT EIN) ein_vals, MAX(LENGTH(EIN)) ein_maxlen, COUNT(DISTINCT PHONE) phone_vals, MAX(PHONE) phone_max,
       COUNT(DISTINCT APPLICANT_TYPE_CODE) app_types, COUNT_IF(APPLICANT_TYPE_CODE = 'I') app_i,
       MIN(GRANT_DATE) g0, MAX(GRANT_DATE) g1, MAX(LAST_ACTION_DATE) la1, COUNT(DISTINCT STATE) states
FROM LIBRARY_MARTS.POLITICS.POLITICS__FED_FCC_LICENSING;

-- S06 FCC: rows per license id, and what varies inside the most-repeated ids
WITH u AS (SELECT UNIQUE_SYSTEM_IDENTIFIER usi, COUNT(*) n, COUNT(DISTINCT CALL_SIGN) cs, COUNT(DISTINCT ENTITY_NAME) nm,
                  COUNT(DISTINCT ADDRESS_LINE1) addr, COUNT(DISTINCT LICENSE_STATUS) st, COUNT(DISTINCT GRANT_DATE) gd,
                  COUNT(DISTINCT FRN) frn, COUNT(DISTINCT ULS_FILE_NUMBER) uls, MAX(CALL_SIGN) a_call, MAX(ENTITY_NAME) a_name
           FROM LIBRARY_MARTS.POLITICS.POLITICS__FED_FCC_LICENSING GROUP BY 1)
(SELECT 'bucket' k, CASE WHEN n = 1 THEN '1' WHEN n <= 10 THEN '2-10' WHEN n <= 100 THEN '11-100' ELSE '101+' END b,
        COUNT(*) ids, SUM(n) rows_, NULL cs, NULL nm, NULL addr, NULL st, NULL gd, NULL frn, NULL uls, NULL a_call, NULL a_name
 FROM u GROUP BY 2)
UNION ALL
(SELECT 'top', usi, 1, n, cs, nm, addr, st, gd, frn, uls, a_call, a_name FROM u ORDER BY n DESC LIMIT 8);

-- S07 FEC candidate summary: per cycle and office letter; dup keys, text coverage date, debt, empties
SELECT CYCLE, LEFT(CAND_ID, 1) off, COUNT(*) n, COUNT(DISTINCT CAND_ID) cands, SUM(TTL_RECEIPTS) receipts, MEDIAN(TTL_RECEIPTS) med_receipts,
       COUNT_IF(DEBTS_OWED_BY > 0) with_debt, SUM(DEBTS_OWED_BY) debt, SUM(CASH_ON_HAND_CLOSE) coh,
       MIN(TRY_TO_DATE(COVERAGE_END_DATE, 'MM/DD/YYYY')) cov0, MAX(TRY_TO_DATE(COVERAGE_END_DATE, 'MM/DD/YYYY')) cov1,
       COUNT_IF(COVERAGE_END_DATE IS NOT NULL AND TRY_TO_DATE(COVERAGE_END_DATE, 'MM/DD/YYYY') IS NULL) cov_unparsed,
       MAX(COVERAGE_END_DATE) cov_text_max, COUNT_IF(TTL_RECEIPTS = 0 AND TTL_DISB = 0) zero_rows,
       COUNT_IF(TTL_RECEIPTS < 0 OR TTL_DISB < 0) negatives
FROM LIBRARY_MARTS.POLITICS.POLITICS__FEC_CANDIDATE_SUMMARY GROUP BY 1, 2 ORDER BY 1, 2;

-- S08 FEC join to FEC_CANDIDATE on CAND_ID + CYCLE: last declared election year vs the cycle (zombie test prep)
WITH c AS (SELECT CAND_ID, CYCLE, MAX(CAND_ELECTION_YR) ey, MAX(CAND_STATUS) st, COUNT(*) n
           FROM LIBRARY_MARTS.POLITICS.POLITICS__FEC_CANDIDATE GROUP BY 1, 2)
SELECT s.CYCLE, LEFT(s.CAND_ID, 1) off,
       CASE WHEN c.CAND_ID IS NULL THEN 'no_match' WHEN c.ey >= s.CYCLE::int THEN 'running' WHEN c.ey >= s.CYCLE::int - 2 THEN 'last_race_1_cycle_ago'
            ELSE 'last_race_2plus_cycles_ago' END status_vs_cycle,
       COUNT(*) n, SUM(s.TTL_DISB) disb, MEDIAN(s.TTL_DISB) med_disb, SUM(s.CASH_ON_HAND_CLOSE) coh, SUM(s.DEBTS_OWED_BY) debt,
       LISTAGG(DISTINCT c.st, ',') cand_status, MAX(c.n) max_cand_rows
FROM LIBRARY_MARTS.POLITICS.POLITICS__FEC_CANDIDATE_SUMMARY s LEFT JOIN c ON c.CAND_ID = s.CAND_ID AND c.CYCLE = s.CYCLE
GROUP BY 1, 2, 3 ORDER BY 1, 2, 3;

-- S09 FJC service: key uniqueness, data edge, sentinels, overlap with FJC_APPOINTMENT and FJC_JUDGE
SELECT COUNT(*) n, COUNT(DISTINCT NID) nids, COUNT(DISTINCT NID || '|' || SEQUENCE) nid_seq,
       MAX(NOMINATION_DATE) nom1, MAX(CONFIRMATION_DATE) conf1, MAX(COMMISSION_DATE) comm1, MAX(SENIOR_STATUS_DATE) ss1,
       MAX(IFF(TERMINATION_DATE < '2100-01-01', TERMINATION_DATE, NULL)) term1, COUNT_IF(TERMINATION_DATE >= '2100-01-01') term_far_future,
       COUNT_IF(COMMISSION_DATE >= '2025-01-20') comm_since_2025, COUNT_IF(SENIOR_STATUS_DATE >= '2025-01-20') ss_since_2025,
       COUNT_IF(TERMINATION_DATE >= '2025-01-20' AND TERMINATION_DATE < '2100-01-01') term_since_2025,
       COUNT_IF(TERMINATION_DATE IS NULL) open_rows, COUNT_IF(TERMINATION_DATE IS NULL AND SENIOR_STATUS_DATE IS NULL) active_no_senior,
       COUNT_IF(TERMINATION IS NULL AND TERMINATION_DATE IS NOT NULL) term_date_no_reason,
       (SELECT COUNT(*) FROM LIBRARY_MARTS.POLITICS.POLITICS__FJC_APPOINTMENT) appt_rows,
       (SELECT COUNT(*) FROM LIBRARY_MARTS.POLITICS.POLITICS__FJC_APPOINTMENT a JOIN LIBRARY_MARTS.POLITICS.POLITICS__FED_FJC_SERVICE s2
          ON a.NID = s2.NID AND a.SEQUENCE::string = s2.SEQUENCE) appt_key_match,
       (SELECT COUNT(*) FROM LIBRARY_MARTS.POLITICS.POLITICS__FJC_APPOINTMENT a JOIN LIBRARY_MARTS.POLITICS.POLITICS__FED_FJC_SERVICE s2
          ON a.NID = s2.NID AND a.SEQUENCE::string = s2.SEQUENCE
          AND COALESCE(TRY_TO_DATE(a.COMMISSION_DATE), TRY_TO_DATE(a.COMMISSION_DATE, 'MM/DD/YYYY')) = s2.COMMISSION_DATE) appt_same_commission,
       (SELECT MAX(COMMISSION_DATE) FROM LIBRARY_MARTS.POLITICS.POLITICS__FJC_APPOINTMENT) appt_comm_text_max,
       (SELECT COUNT(*) FROM LIBRARY_MARTS.POLITICS.POLITICS__FJC_JUDGE) judge_rows,
       (SELECT COUNT_IF(BIRTH_YEAR IS NULL) FROM LIBRARY_MARTS.POLITICS.POLITICS__FJC_JUDGE) judge_no_birth,
       (SELECT COUNT(DISTINCT s3.NID) FROM LIBRARY_MARTS.POLITICS.POLITICS__FED_FJC_SERVICE s3
          LEFT JOIN LIBRARY_MARTS.POLITICS.POLITICS__FJC_JUDGE j ON j.NID = s3.NID WHERE j.NID IS NULL) service_nids_missing_judge
FROM LIBRARY_MARTS.POLITICS.POLITICS__FED_FJC_SERVICE;

-- S10 FJC senior status inside the same window at the start of each presidency, among judges eligible (rule of 80) at day one
WITH p AS (SELECT column1 pres, column2 pparty, column3::date d0 FROM VALUES
             ('1 Reagan', 'R', '1981-01-20'), ('2 Bush41', 'R', '1989-01-20'), ('3 Clinton', 'D', '1993-01-20'), ('4 Bush43', 'R', '2001-01-20'),
             ('5 Obama', 'D', '2009-01-20'), ('6 Trump1', 'R', '2017-01-20'), ('7 Biden', 'D', '2021-01-20'), ('8 Trump2', 'R', '2025-01-20')),
edge AS (SELECT GREATEST(MAX(SENIOR_STATUS_DATE), MAX(COMMISSION_DATE)) e FROM LIBRARY_MARTS.POLITICS.POLITICS__FED_FJC_SERVICE),
w AS (SELECT DATEDIFF(day, '2025-01-20'::date, e) wdays, e FROM edge),
s AS (SELECT s.NID, LEFT(s.PARTY_OF_APPOINTING_PRESIDENT, 1) ap, s.COMMISSION_DATE cd, s.SENIOR_STATUS_DATE ssd,
             IFF(s.TERMINATION_DATE >= '2100-01-01', NULL, s.TERMINATION_DATE) td, j.BIRTH_YEAR by_
      FROM LIBRARY_MARTS.POLITICS.POLITICS__FED_FJC_SERVICE s JOIN LIBRARY_MARTS.POLITICS.POLITICS__FJC_JUDGE j ON j.NID = s.NID
      WHERE s.COURT_TYPE IN ('U.S. District Court', 'U.S. Court of Appeals')),
pool AS (SELECT p.pres, p.pparty, s.ap, w.wdays, w.e,
                IFF(s.ssd >= p.d0 AND s.ssd < DATEADD(day, w.wdays, p.d0), 1, 0) took,
                IFF(s.td >= p.d0 AND s.td < DATEADD(day, w.wdays, p.d0) AND (s.ssd IS NULL OR s.ssd >= DATEADD(day, w.wdays, p.d0)), 1, 0) left_other
         FROM p CROSS JOIN w CROSS JOIN s
         WHERE s.cd < p.d0 AND (s.ssd IS NULL OR s.ssd >= p.d0) AND (s.td IS NULL OR s.td >= p.d0)
           AND YEAR(p.d0) - s.by_ >= 65 AND (YEAR(p.d0) - s.by_) + (YEAR(p.d0) - YEAR(s.cd)) >= 80)
SELECT pres, pparty, ap appointer_party, MAX(wdays) window_days, MAX(e) data_edge, COUNT(*) eligible_day1, SUM(took) took_senior,
       ROUND(100 * SUM(took) / COUNT(*), 1) pct_took, SUM(left_other) left_other_way
FROM pool GROUP BY 1, 2, 3 ORDER BY 1, 3;

-- ===== connection 2 (g17/batch2.sql)
ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300;
ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24';

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

-- ===== connection 3 (g17/batch3.sql)
ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300;
ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24';

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

-- ===== connection 4 (g17/batch4.sql)
ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300;
ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24';

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
