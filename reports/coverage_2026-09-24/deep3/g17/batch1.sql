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
