-- deep-14.sql  |  coverage round 2, group 14  |  2026-09-24
-- Door: Python (connect/db.py). Read-only. 28 SELECT/WITH statements + 6 session statements = 34.
-- Each connection (3 total) opened with:
--   ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300;
--   ALTER SESSION SET QUERY_TAG = 'coverage-r2-2026-09-24';
-- [12] failed to compile (ACTION_DATE is text). [22] is the fixed rerun; it hit the 300 s timeout.


-- ===== connection 1 =====

-- [1] PBGC trusteed plans: size, keys, dates
SELECT COUNT(*) n, COUNT(DISTINCT CASE_NUMBER) cases, COUNT(DISTINCT EIN) eins, COUNT(DISTINCT SPONSOR_NAME) sponsors, MIN(DATE_OF_PLAN_TERMINATION) term_min, MAX(DATE_OF_PLAN_TERMINATION) term_max, MIN(DATE_OF_PBGC_TRUSTEESHIP) tr_min, MAX(DATE_OF_PBGC_TRUSTEESHIP) tr_max, SUM(TRY_TO_DOUBLE(NUMBER_OF_PARICIPANTS_AT_DATE_OF_PLAN_TERMINATION::varchar)) participants, COUNT_IF(LENGTH(REGEXP_REPLACE(EIN::varchar,'[^0-9]',''))=9) ein9, COUNT_IF(LENGTH(REGEXP_REPLACE(EIN::varchar,'[^0-9]',''))=8) ein8, COUNT_IF(EIN IS NULL OR TRIM(EIN::varchar)='') ein_blank, COUNT_IF(TRY_TO_NUMBER(REGEXP_REPLACE(EIN::varchar,'[^0-9]',''))=0) ein_zero, COUNT(DISTINCT _SOURCE_RUN_ID) runs FROM LIBRARY_MARTS.LABOR.LABOR__FED_PBGC_TRUSTEED_PLANS;

-- [2] PBGC sample 5 random rows
SELECT * FROM LIBRARY_MARTS.LABOR.LABOR__FED_PBGC_TRUSTEED_PLANS SAMPLE (5 ROWS);

-- [3] FEC committee: size by cycle, treasurers, PAC types
SELECT CYCLE, COUNT(*) n, COUNT(DISTINCT CMTE_ID) cmtes, COUNT(DISTINCT TRES_NM) treasurers, COUNT_IF(TRES_NM IS NULL OR TRIM(TRES_NM)='') tres_blank, COUNT_IF(CMTE_TP IN ('N','Q','O','V','W')) pac_rows, COUNT_IF(CMTE_TP IN ('H','S','P')) cand_rows, COUNT_IF(CMTE_DSGN='D') leadership, COUNT_IF(CMTE_FILING_FREQ IN ('T','A')) terminated FROM LIBRARY_MARTS.POLITICS.POLITICS__FEC_COMMITTEE GROUP BY CYCLE ORDER BY CYCLE;

-- [4] FEC committee sample 5 random rows
SELECT * FROM LIBRARY_MARTS.POLITICS.POLITICS__FEC_COMMITTEE SAMPLE (5 ROWS);

-- [5] EAVS: size, mail ballots returned/counted/rejected, sentinels, year hints
SELECT COUNT(*) n, COUNT(DISTINCT FIPSCODE) fips, COUNT(DISTINCT STATE_ABBR) states, SUM(IFF(TRY_TO_DOUBLE(C1A::varchar)>=0,TRY_TO_DOUBLE(C1A::varchar),0)) c1a_sent, SUM(IFF(TRY_TO_DOUBLE(C1B::varchar)>=0,TRY_TO_DOUBLE(C1B::varchar),0)) c1b_returned, SUM(IFF(TRY_TO_DOUBLE(C8A::varchar)>=0,TRY_TO_DOUBLE(C8A::varchar),0)) c8a_counted, SUM(IFF(TRY_TO_DOUBLE(C9A::varchar)>=0,TRY_TO_DOUBLE(C9A::varchar),0)) c9a_rejected, SUM(IFF(TRY_TO_DOUBLE(F1A::varchar)>=0,TRY_TO_DOUBLE(F1A::varchar),0)) f1a_voted, SUM(IFF(TRY_TO_DOUBLE(E1A::varchar)>=0,TRY_TO_DOUBLE(E1A::varchar),0)) e1a_prov, COUNT_IF(TRY_TO_DOUBLE(C9A::varchar)<0) c9a_neg, COUNT_IF(TRY_TO_DOUBLE(C1B::varchar)<0) c1b_neg, COUNT_IF(C9A IS NULL) c9a_null, COUNT_IF(TRY_TO_DOUBLE(C8A::varchar)+TRY_TO_DOUBLE(C9A::varchar)=TRY_TO_DOUBLE(C1B::varchar)) c8_plus_c9_eq_c1b, COUNT_IF(CONCAT_WS(' ',C1COMMENTS,C9COMMENTS,F1COMMENTS) ILIKE '%2024%') m2024, COUNT_IF(CONCAT_WS(' ',C1COMMENTS,C9COMMENTS,F1COMMENTS) ILIKE '%2022%') m2022, COUNT_IF(CONCAT_WS(' ',C1COMMENTS,C9COMMENTS,F1COMMENTS) ILIKE '%2020%') m2020 FROM LIBRARY_MARTS.POLITICS.POLITICS__FED_EAC_EAVS;

-- [6] EAVS sample 5 random rows (key cols)
SELECT * FROM LIBRARY_MARTS.POLITICS.POLITICS__FED_EAC_EAVS SAMPLE (5 ROWS);

-- [7] Canada contributions: rows and $ by recipient kind, donor kind, return kind
SELECT POLITICAL_ENTITY, CONTRIBUTOR_TYPE, CASE WHEN ELECTORAL_EVENT ILIKE '%quarter%' THEN 'Q' WHEN ELECTORAL_EVENT ILIKE '%annual%' THEN 'A' ELSE 'E' END ev, COUNT(*) n, ROUND(SUM(MONETARY_AMOUNT)) amt, MIN(FISCAL_ELECTION_DATE) d0, MAX(FISCAL_ELECTION_DATE) d1 FROM LIBRARY_MARTS.POLITICS.POLITICS__INTL_ELECTIONS_CANADA_CONTRIBUTIONS GROUP BY 1,2,3 ORDER BY amt DESC NULLS LAST;

-- [8] Canada sample: 5 biggest lines + 5 random lines
SELECT * FROM (SELECT * FROM LIBRARY_MARTS.POLITICS.POLITICS__INTL_ELECTIONS_CANADA_CONTRIBUTIONS ORDER BY MONETARY_AMOUNT DESC NULLS LAST LIMIT 5) UNION ALL SELECT * FROM (SELECT * FROM LIBRARY_MARTS.POLITICS.POLITICS__INTL_ELECTIONS_CANADA_CONTRIBUTIONS SAMPLE (5 ROWS));

-- [9] IRS 8872: size, amendments, duplicate periods, $
SELECT COUNT(*) n, COUNT(DISTINCT EIN) eins, COUNT(DISTINCT FORM_ID_NUMBER) forms, COUNT(DISTINCT EIN||'|'||PERIOD_BEGIN_DATE::varchar||'|'||PERIOD_END_DATE::varchar) ein_periods, COUNT_IF(AMENDED_REPORT_IND::varchar='1') amended, ROUND(SUM(TRY_TO_DOUBLE(TOTAL_SCHED_A::varchar))) a_sum, ROUND(SUM(TRY_TO_DOUBLE(TOTAL_SCHED_B::varchar))) b_sum, ROUND(SUM(IFF(AMENDED_REPORT_IND::varchar='1',TRY_TO_DOUBLE(TOTAL_SCHED_A::varchar),0))) a_amended, MIN(PERIOD_BEGIN_DATE) p0, MAX(PERIOD_END_DATE) p1, MIN(INSERT_DATETIME) i0, MAX(INSERT_DATETIME) i1, COUNT(DISTINCT FORM_TYPE) ftypes, COUNT_IF(TRY_TO_DOUBLE(TOTAL_SCHED_A::varchar)<0) a_neg FROM LIBRARY_MARTS.POLITICS.POLITICS__IRS527_8872_REPORTS;

-- [10] IRS 8872 sample 5 random rows
SELECT * FROM LIBRARY_MARTS.POLITICS.POLITICS__IRS527_8872_REPORTS SAMPLE (5 ROWS);

-- ===== connection 2 =====

-- [11] PBGC repeat dumpers: one EIN, plans terminated in years 3+ apart
WITH p AS (SELECT LPAD(REGEXP_REPLACE(EIN::varchar,'[^0-9]',''),9,'0') ein, SPONSOR_NAME, YEAR(DATE_OF_PLAN_TERMINATION) ty, TRY_TO_DOUBLE(NUMBER_OF_PARICIPANTS_AT_DATE_OF_PLAN_TERMINATION::varchar) parts FROM LIBRARY_MARTS.LABOR.LABOR__FED_PBGC_TRUSTEED_PLANS)
, e AS (SELECT ein, COUNT(*) plans, COUNT(DISTINCT ty) term_years, MIN(ty) first_y, MAX(ty) last_y, SUM(parts) parts, COUNT(DISTINCT SPONSOR_NAME) names, MIN(SPONSOR_NAME) name1, MAX(SPONSOR_NAME) name2 FROM p GROUP BY ein)
SELECT ein, plans, term_years, first_y, last_y, last_y-first_y span, parts, names, name1, name2,
 COUNT_IF(plans>=2) OVER () eins_2plus, COUNT_IF(last_y-first_y>=3) OVER () eins_span3, SUM(IFF(last_y-first_y>=3,parts,0)) OVER () parts_span3, COUNT_IF(last_y-first_y>=10) OVER () eins_span10
FROM e WHERE last_y-first_y>=3 ORDER BY term_years DESC, parts DESC LIMIT 30;

-- [12] PBGC sponsor name -> USAspending contract recipient name (R2), $ after trusteeship, state check
-- RESULT: compile error, DATE_TRUNC on a VARCHAR ACTION_DATE. Fixed in [22].
WITH p AS (SELECT TRIM(REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(' ' || REGEXP_REPLACE(UPPER(SPONSOR_NAME), '[^A-Z0-9]+', ' ') || ' ', ' (INC|INCORPORATED|CORP|CORPORATION|CO|COMPANY|LLC|LTD|LIMITED|LP|THE|OF) ', ' '), ' (INC|INCORPORATED|CORP|CORPORATION|CO|COMPANY|LLC|LTD|LIMITED|LP|THE|OF) ', ' '), ' +', ' ')) nm, MIN(DATE_OF_PBGC_TRUSTEESHIP) tr, MAX(STATE) st, COUNT(*) plans, SUM(TRY_TO_DOUBLE(NUMBER_OF_PARICIPANTS_AT_DATE_OF_PLAN_TERMINATION::varchar)) parts, MIN(SPONSOR_NAME) sponsor FROM LIBRARY_MARTS.LABOR.LABOR__FED_PBGC_TRUSTEED_PLANS WHERE DATE_OF_PBGC_TRUSTEESHIP >= '2008-01-01' GROUP BY 1 HAVING REGEXP_COUNT(nm, ' ') >= 1)
, n0 AS (SELECT RECIPIENT_NAME, TRIM(REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(' ' || REGEXP_REPLACE(UPPER(RECIPIENT_NAME), '[^A-Z0-9]+', ' ') || ' ', ' (INC|INCORPORATED|CORP|CORPORATION|CO|COMPANY|LLC|LTD|LIMITED|LP|THE|OF) ', ' '), ' (INC|INCORPORATED|CORP|CORPORATION|CO|COMPANY|LLC|LTD|LIMITED|LP|THE|OF) ', ' '), ' +', ' ')) nm FROM (SELECT DISTINCT RECIPIENT_NAME FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS_FULL_R2))
, n1 AS (SELECT n0.RECIPIENT_NAME, n0.nm FROM n0 JOIN (SELECT DISTINCT nm FROM p) pp ON pp.nm = n0.nm)
, r0 AS (SELECT RECIPIENT_NAME, RECIPIENT_STATE_CODE, DATE_TRUNC('month', ACTION_DATE) m, SUM(FEDERAL_ACTION_OBLIGATION) amt, COUNT(*) tx FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS_FULL_R2 WHERE RECIPIENT_NAME IN (SELECT RECIPIENT_NAME FROM n1) GROUP BY 1,2,3)
, r AS (SELECT n1.nm, r0.RECIPIENT_STATE_CODE rst, r0.m, r0.amt, r0.tx FROM r0 JOIN n1 USING (RECIPIENT_NAME))
, j AS (SELECT p.nm, p.sponsor, p.tr, p.st, p.plans, p.parts, SUM(IFF(r.m > p.tr, r.amt, 0)) amt_after, SUM(IFF(r.m <= p.tr, r.amt, 0)) amt_before, SUM(IFF(r.m > p.tr, r.tx, 0)) tx_after, MAX(IFF(r.m > p.tr, r.m, NULL)) last_m, MAX(IFF(r.rst = p.st, 1, 0)) state_agree, LISTAGG(DISTINCT r.rst, ',') WITHIN GROUP (ORDER BY r.rst) rsts FROM p JOIN r ON r.nm = p.nm GROUP BY 1,2,3,4,5,6)
SELECT j.*, (SELECT COUNT(*) FROM p) pbgc_names, COUNT(*) OVER () names_hit, COUNT_IF(amt_after > 0) OVER () names_after, COUNT_IF(state_agree = 1) OVER () names_state_ok, SUM(IFF(state_agree = 1, amt_after, 0)) OVER () amt_after_state_ok, (SELECT MIN(ACTION_DATE) FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS_FULL_R2) r2_first, (SELECT MAX(ACTION_DATE) FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS_FULL_R2) r2_last
FROM j ORDER BY amt_after DESC NULLS LAST LIMIT 40;

-- [13] FEC 2024 PACs by treasurer: $ raised, share of spending that reached candidates/committees/IEs, vs all other PACs
WITH c AS (SELECT CMTE_ID, UPPER(TRIM(TRES_NM)) tres, CMTE_NM, CMTE_TP, CMTE_DSGN FROM LIBRARY_MARTS.POLITICS.POLITICS__FEC_COMMITTEE WHERE CYCLE = 2024 AND CMTE_TP IN ('N','Q','O','V','W'))
, s AS (SELECT CMTE_ID, TRY_TO_DOUBLE(TOTAL_RECEIPTS::varchar) r, TRY_TO_DOUBLE(TOTAL_DISBURSEMENTS::varchar) d, TRY_TO_DOUBLE(INDIVIDUAL_CONTRIBUTIONS::varchar) ind, COALESCE(TRY_TO_DOUBLE(CONTRIBUTIONS_TO_OTHER_COMMITTEES::varchar),0) + COALESCE(TRY_TO_DOUBLE(INDEPENDENT_EXPENDITURES::varchar),0) pol, COVERAGE_END_DATE ce FROM LIBRARY_MARTS.POLITICS.POLITICS__FED_FEC_PAC_SUMMARY WHERE COVERAGE_END_DATE BETWEEN '2023-01-01' AND '2025-01-31' QUALIFY ROW_NUMBER() OVER (PARTITION BY CMTE_ID ORDER BY COVERAGE_END_DATE DESC) = 1)
, j AS (SELECT c.*, s.r, s.d, s.ind, s.pol, s.ce, IFF(s.d > 0, s.pol / s.d, NULL) pshare FROM c LEFT JOIN s USING (CMTE_ID))
, t AS (SELECT tres, COUNT(*) pacs, COUNT(r) matched, SUM(r) rec, SUM(ind) ind, SUM(d) disb, SUM(pol) pol, COUNT_IF(ind >= 100000 AND pshare < 0.10) low_pacs, SUM(IFF(ind >= 100000 AND pshare < 0.10, ind, 0)) low_ind, COUNT_IF(CMTE_DSGN = 'D') leadership FROM j GROUP BY tres)
, k AS (SELECT t.*, ROW_NUMBER() OVER (ORDER BY pacs DESC) rk FROM t)
SELECT IFF(rk <= 20, tres, 'ALL OTHER') tres_g, SUM(pacs) pacs, SUM(matched) matched, ROUND(SUM(rec)) rec, ROUND(SUM(ind)) ind, ROUND(SUM(disb)) disb, ROUND(SUM(pol)) pol, ROUND(SUM(pol) / NULLIF(SUM(disb),0), 3) pol_share, SUM(low_pacs) low_pacs, ROUND(SUM(low_ind)) low_ind, SUM(leadership) leadership, MIN(rk) rk
FROM k GROUP BY 1 ORDER BY rk;

-- [14] FEC 2024 PACs raising $1M+ from individuals with <10% of spending reaching candidates/committees/IEs
WITH c AS (SELECT CMTE_ID, UPPER(TRIM(TRES_NM)) tres, CMTE_NM, CMTE_TP, CMTE_DSGN FROM LIBRARY_MARTS.POLITICS.POLITICS__FEC_COMMITTEE WHERE CYCLE = 2024 AND CMTE_TP IN ('N','Q','O','V','W'))
, s AS (SELECT CMTE_ID, TRY_TO_DOUBLE(TOTAL_RECEIPTS::varchar) r, TRY_TO_DOUBLE(TOTAL_DISBURSEMENTS::varchar) d, TRY_TO_DOUBLE(INDIVIDUAL_CONTRIBUTIONS::varchar) ind, COALESCE(TRY_TO_DOUBLE(CONTRIBUTIONS_TO_OTHER_COMMITTEES::varchar),0) + COALESCE(TRY_TO_DOUBLE(INDEPENDENT_EXPENDITURES::varchar),0) pol, COVERAGE_END_DATE ce FROM LIBRARY_MARTS.POLITICS.POLITICS__FED_FEC_PAC_SUMMARY WHERE COVERAGE_END_DATE BETWEEN '2023-01-01' AND '2025-01-31' QUALIFY ROW_NUMBER() OVER (PARTITION BY CMTE_ID ORDER BY COVERAGE_END_DATE DESC) = 1)
, j AS (SELECT c.*, s.r, s.d, s.ind, s.pol, s.ce, IFF(s.d > 0, s.pol / s.d, NULL) pshare FROM c LEFT JOIN s USING (CMTE_ID))
, tc AS (SELECT tres, COUNT(*) OVER (PARTITION BY tres) tres_pacs FROM c QUALIFY ROW_NUMBER() OVER (PARTITION BY tres ORDER BY CMTE_ID) = 1)
SELECT j.CMTE_ID, j.CMTE_NM, j.tres, tc.tres_pacs, j.CMTE_TP, j.CMTE_DSGN, j.ce, ROUND(j.ind) ind, ROUND(j.d) disb, ROUND(j.pol) pol, ROUND(j.pshare, 3) pshare,
 COUNT(*) OVER () n_low, SUM(j.ind) OVER () ind_low, COUNT_IF(tc.tres_pacs >= 100) OVER () n_low_pro_tres
FROM j JOIN tc USING (tres) WHERE j.ind >= 1000000 AND j.pshare < 0.10 ORDER BY j.ind DESC LIMIT 40;

-- [15] EAVS 2022 mail ballots: jurisdictions (1,000+ returned) rejecting far above their own state's rate
WITH v AS (SELECT STATE_ABBR st, JURISDICTION_NAME jur, FIPSCODE, TRY_TO_DOUBLE(C1B::varchar) ret, TRY_TO_DOUBLE(C9A::varchar) rej, IFF(TRY_TO_DOUBLE(C9B::varchar)>=0,TRY_TO_DOUBLE(C9B::varchar),NULL) C9B, IFF(TRY_TO_DOUBLE(C9C::varchar)>=0,TRY_TO_DOUBLE(C9C::varchar),NULL) C9C, IFF(TRY_TO_DOUBLE(C9D::varchar)>=0,TRY_TO_DOUBLE(C9D::varchar),NULL) C9D, IFF(TRY_TO_DOUBLE(C9E::varchar)>=0,TRY_TO_DOUBLE(C9E::varchar),NULL) C9E, IFF(TRY_TO_DOUBLE(C9F::varchar)>=0,TRY_TO_DOUBLE(C9F::varchar),NULL) C9F, IFF(TRY_TO_DOUBLE(C9G::varchar)>=0,TRY_TO_DOUBLE(C9G::varchar),NULL) C9G, IFF(TRY_TO_DOUBLE(C9H::varchar)>=0,TRY_TO_DOUBLE(C9H::varchar),NULL) C9H, IFF(TRY_TO_DOUBLE(C9I::varchar)>=0,TRY_TO_DOUBLE(C9I::varchar),NULL) C9I, IFF(TRY_TO_DOUBLE(C9J::varchar)>=0,TRY_TO_DOUBLE(C9J::varchar),NULL) C9J, IFF(TRY_TO_DOUBLE(C9K::varchar)>=0,TRY_TO_DOUBLE(C9K::varchar),NULL) C9K, IFF(TRY_TO_DOUBLE(C9L::varchar)>=0,TRY_TO_DOUBLE(C9L::varchar),NULL) C9L, IFF(TRY_TO_DOUBLE(C9M::varchar)>=0,TRY_TO_DOUBLE(C9M::varchar),NULL) C9M, IFF(TRY_TO_DOUBLE(C9N::varchar)>=0,TRY_TO_DOUBLE(C9N::varchar),NULL) C9N, IFF(TRY_TO_DOUBLE(C9O::varchar)>=0,TRY_TO_DOUBLE(C9O::varchar),NULL) C9O, IFF(TRY_TO_DOUBLE(C9P::varchar)>=0,TRY_TO_DOUBLE(C9P::varchar),NULL) C9P, IFF(TRY_TO_DOUBLE(C9Q::varchar)>=0,TRY_TO_DOUBLE(C9Q::varchar),NULL) C9Q, IFF(TRY_TO_DOUBLE(C9R::varchar)>=0,TRY_TO_DOUBLE(C9R::varchar),NULL) C9R, IFF(TRY_TO_DOUBLE(C9S::varchar)>=0,TRY_TO_DOUBLE(C9S::varchar),NULL) C9S, IFF(TRY_TO_DOUBLE(C9T::varchar)>=0,TRY_TO_DOUBLE(C9T::varchar),NULL) C9T FROM LIBRARY_MARTS.POLITICS.POLITICS__FED_EAC_EAVS WHERE TRY_TO_DOUBLE(C1B::varchar) >= 0 AND TRY_TO_DOUBLE(C9A::varchar) >= 0)
, s AS (SELECT st, SUM(rej) / NULLIF(SUM(ret),0) srate, SUM(ret) sret, SUM(rej) srej FROM v GROUP BY st)
, x AS (SELECT v.*, s.srate, s.srej, rej / ret rate, (rej / ret) / NULLIF(s.srate,0) ratio, rej - s.srate * ret excess FROM v JOIN s USING (st) WHERE ret >= 1000)
SELECT st, jur, ret, rej, ROUND(rate,4) rate, ROUND(srate,4) srate, ROUND(ratio,1) ratio, ROUND(excess) excess, srej, C9B, C9C, C9D, C9E, C9F, C9G, C9H, C9I, C9J, C9K, C9L, C9M, C9N, C9O, C9P, C9Q, C9R, C9S, C9T,
 COUNT(*) OVER () n_elig, COUNT_IF(ratio >= 3 AND rej >= 50) OVER () n_3x, SUM(IFF(excess > 0, excess, 0)) OVER () excess_all, (SELECT SUM(rej) FROM v) rej_valid, (SELECT SUM(ret) FROM v) ret_valid
FROM x ORDER BY excess DESC LIMIT 30;

-- [16] EAVS 2022 provisional ballots: jurisdictions (500+ cast) rejecting far above their own state's rate
WITH v AS (SELECT STATE_ABBR st, JURISDICTION_NAME jur, TRY_TO_DOUBLE(E1A::varchar) cast_, TRY_TO_DOUBLE(E1B::varchar) full_, TRY_TO_DOUBLE(E1C::varchar) part_, TRY_TO_DOUBLE(E1D::varchar) rej FROM LIBRARY_MARTS.POLITICS.POLITICS__FED_EAC_EAVS WHERE TRY_TO_DOUBLE(E1A::varchar) >= 0 AND TRY_TO_DOUBLE(E1D::varchar) >= 0)
, s AS (SELECT st, SUM(rej) / NULLIF(SUM(cast_),0) srate, SUM(cast_) scast FROM v GROUP BY st)
, x AS (SELECT v.*, s.srate, s.scast, rej / cast_ rate, (rej / cast_) / NULLIF(s.srate,0) ratio, rej - s.srate * cast_ excess FROM v JOIN s USING (st) WHERE cast_ >= 500)
SELECT st, jur, cast_, full_, part_, rej, ROUND(rate,3) rate, ROUND(srate,3) srate, ROUND(ratio,1) ratio, ROUND(excess) excess, scast,
 COUNT(*) OVER () n_elig, COUNT_IF(ratio >= 3 AND rej >= 50) OVER () n_3x, (SELECT SUM(rej) FROM v) rej_valid, (SELECT SUM(cast_) FROM v) cast_valid
FROM x ORDER BY excess DESC LIMIT 25;

-- [17] Canada: do quarterly party returns repeat the annual return lines? by year
WITH b AS (SELECT RECIPIENT, UPPER(TRIM(CONTRIBUTOR_NAME)) nm, CONTRIBUTOR_POSTAL_CODE pc, CONTRIBUTION_RECEIVED_DATE rd, MONETARY_AMOUNT amt, YEAR(FISCAL_ELECTION_DATE) yr, IFF(ELECTORAL_EVENT ILIKE '%quarter%', 'Q', 'A') ev, PART_NUMBER_OF_RETURN part FROM LIBRARY_MARTS.POLITICS.POLITICS__INTL_ELECTIONS_CANADA_CONTRIBUTIONS WHERE POLITICAL_ENTITY = 'Registered parties' AND CONTRIBUTOR_TYPE = 'Individuals')
, a AS (SELECT DISTINCT RECIPIENT, nm, pc, rd, amt FROM b WHERE ev = 'A')
, q AS (SELECT b.*, IFF(a.nm IS NOT NULL, 1, 0) in_a FROM b LEFT JOIN a ON a.RECIPIENT = b.RECIPIENT AND a.nm = b.nm AND EQUAL_NULL(a.pc, b.pc) AND EQUAL_NULL(a.rd, b.rd) AND a.amt = b.amt WHERE b.ev = 'Q')
SELECT yr, SUM(n_a) n_a, ROUND(SUM(amt_a)) amt_a, SUM(n_q) n_q, ROUND(SUM(amt_q)) amt_q, SUM(q_in_a) q_in_a, ROUND(SUM(amt_q_in_a)) amt_q_in_a, SUM(n_part_other) n_part_not_2a FROM (
 SELECT yr, COUNT(*) n_a, SUM(amt) amt_a, 0 n_q, 0 amt_q, 0 q_in_a, 0 amt_q_in_a, COUNT_IF(part <> '2a') n_part_other FROM b WHERE ev = 'A' GROUP BY yr
 UNION ALL SELECT yr, 0, 0, COUNT(*), SUM(amt), SUM(in_a), SUM(IFF(in_a = 1, amt, 0)), COUNT_IF(part <> '2a') FROM q GROUP BY yr) GROUP BY yr ORDER BY yr;

-- [18] Canada: individuals over the yearly per-party cap (annual party returns only, lump lines dropped)
WITH b AS (SELECT RECIPIENT, UPPER(TRIM(CONTRIBUTOR_NAME)) nm, CONTRIBUTOR_POSTAL_CODE pc, YEAR(FISCAL_ELECTION_DATE) yr, MONETARY_AMOUNT amt, PART_NUMBER_OF_RETURN part FROM LIBRARY_MARTS.POLITICS.POLITICS__INTL_ELECTIONS_CANADA_CONTRIBUTIONS WHERE POLITICAL_ENTITY = 'Registered parties' AND CONTRIBUTOR_TYPE = 'Individuals' AND ELECTORAL_EVENT NOT ILIKE '%quarter%' AND CONTRIBUTOR_NAME NOT ILIKE 'Contributions of%' AND CONTRIBUTOR_NAME IS NOT NULL)
, g AS (SELECT RECIPIENT, nm, pc, yr, SUM(amt) tot, COUNT(*) lines, LISTAGG(DISTINCT part, ',') parts FROM b GROUP BY 1,2,3,4)
, x AS (SELECT g.*, CASE WHEN yr <= 2006 THEN 5400 WHEN yr <= 2011 THEN 1100 WHEN yr <= 2014 THEN 1200 WHEN yr = 2015 THEN 1500 ELSE 1500 + 25 * (yr - 2015) END cap FROM g)
SELECT RECIPIENT, nm, pc, yr, tot, cap, lines, parts, COUNT(*) OVER () n_over, SUM(tot - cap) OVER () excess_all, (SELECT COUNT(*) FROM g) n_keys, (SELECT COUNT(*) FROM g WHERE pc IS NULL) n_keys_nopc
FROM x WHERE tot > cap * 1.10 ORDER BY tot - cap DESC LIMIT 30;

-- [19] Canada: donors (name+postal code) giving $200+ to two or more parties in the same year
WITH b AS (SELECT RECIPIENT, UPPER(TRIM(CONTRIBUTOR_NAME)) nm, CONTRIBUTOR_POSTAL_CODE pc, YEAR(FISCAL_ELECTION_DATE) yr, MONETARY_AMOUNT amt FROM LIBRARY_MARTS.POLITICS.POLITICS__INTL_ELECTIONS_CANADA_CONTRIBUTIONS WHERE POLITICAL_ENTITY = 'Registered parties' AND CONTRIBUTOR_TYPE = 'Individuals' AND ELECTORAL_EVENT NOT ILIKE '%quarter%' AND CONTRIBUTOR_NAME NOT ILIKE 'Contributions of%' AND CONTRIBUTOR_NAME IS NOT NULL AND CONTRIBUTOR_POSTAL_CODE IS NOT NULL)
, g AS (SELECT nm, pc, yr, RECIPIENT, SUM(amt) tot FROM b GROUP BY 1,2,3,4 HAVING SUM(amt) >= 200)
, d AS (SELECT nm, pc, yr, COUNT(*) parties, SUM(tot) tot, MAX(IFF(RECIPIENT ILIKE 'Conservative%', 1, 0)) + MAX(IFF(RECIPIENT ILIKE 'Liberal%', 1, 0)) cl, LISTAGG(RECIPIENT || ':' || ROUND(tot), ' | ') WITHIN GROUP (ORDER BY tot DESC) mix FROM g GROUP BY 1,2,3)
SELECT nm, pc, yr, parties, tot, mix, (SELECT COUNT(*) FROM d) donor_years, COUNT_IF(parties >= 2) OVER () multi, COUNT_IF(cl = 2) OVER () con_and_lib
FROM d WHERE parties >= 2 QUALIFY ROW_NUMBER() OVER (ORDER BY cl DESC, tot DESC) <= 25 ORDER BY cl DESC, tot DESC;

-- [20] IRS 8872: raw vs deduped (latest per EIN+period) totals, overlapping periods left after dedupe, by cycle
WITH r AS (SELECT LPAD(REGEXP_REPLACE(EIN::varchar,'[^0-9]',''),9,'0') ein, ORGANIZATION_NAME org, PERIOD_BEGIN_DATE pb, PERIOD_END_DATE pe, INSERT_DATETIME ins, FORM_ID_NUMBER fid, AMENDED_REPORT_IND::varchar am, TRY_TO_DOUBLE(TOTAL_SCHED_A::varchar) a, TRY_TO_DOUBLE(TOTAL_SCHED_B::varchar) b FROM LIBRARY_MARTS.POLITICS.POLITICS__IRS527_8872_REPORTS)
, d AS (SELECT * FROM r QUALIFY ROW_NUMBER() OVER (PARTITION BY ein, pb, pe ORDER BY ins DESC, fid DESC) = 1)
, ov AS (SELECT d1.ein, d1.pb, d1.pe, d1.a, d1.b FROM d d1 JOIN d d2 ON d1.ein = d2.ein AND (d1.pb <> d2.pb OR d1.pe <> d2.pe) AND d1.pb <= d2.pe AND d2.pb <= d1.pe AND d2.ins > d1.ins QUALIFY ROW_NUMBER() OVER (PARTITION BY d1.ein, d1.pb, d1.pe ORDER BY d2.ins) = 1)
SELECT CEIL(YEAR(pe) / 2) * 2 cycle, SUM(n_raw) n_raw, ROUND(SUM(a_raw)) a_raw, ROUND(SUM(b_raw)) b_raw, SUM(n_dd) n_dd, ROUND(SUM(a_dd)) a_dd, ROUND(SUM(b_dd)) b_dd, SUM(n_ov) n_ov, ROUND(SUM(a_ov)) a_ov, ROUND(SUM(b_ov)) b_ov FROM (
 SELECT pe, 1 n_raw, a a_raw, b b_raw, 0 n_dd, 0 a_dd, 0 b_dd, 0 n_ov, 0 a_ov, 0 b_ov FROM r
 UNION ALL SELECT pe, 0, 0, 0, 1, a, b, 0, 0, 0 FROM d
 UNION ALL SELECT pe, 0, 0, 0, 0, 0, 0, 1, a, b FROM ov) GROUP BY 1 ORDER BY 1;

-- [21] IRS 8872 deduped: per-EIN-per-cycle raised minus spent, biggest both ways
WITH r AS (SELECT LPAD(REGEXP_REPLACE(EIN::varchar,'[^0-9]',''),9,'0') ein, ORGANIZATION_NAME org, PERIOD_BEGIN_DATE pb, PERIOD_END_DATE pe, INSERT_DATETIME ins, FORM_ID_NUMBER fid, AMENDED_REPORT_IND::varchar am, TRY_TO_DOUBLE(TOTAL_SCHED_A::varchar) a, TRY_TO_DOUBLE(TOTAL_SCHED_B::varchar) b FROM LIBRARY_MARTS.POLITICS.POLITICS__IRS527_8872_REPORTS)
, d AS (SELECT * FROM r QUALIFY ROW_NUMBER() OVER (PARTITION BY ein, pb, pe ORDER BY ins DESC, fid DESC) = 1)
, c AS (SELECT ein, CEIL(YEAR(pe) / 2) * 2 cycle, MAX(org) org, COUNT(*) reports, SUM(a) a, SUM(b) b, SUM(a) - SUM(b) gap FROM d GROUP BY 1,2)
, l AS (SELECT ein, SUM(a) la, SUM(b) lb, MIN(cycle) c0, MAX(cycle) c1 FROM c GROUP BY 1)
SELECT c.*, l.la - l.lb life_gap, l.c0, l.c1, COUNT_IF(ABS(gap) >= 1000000) OVER () n_swing1m, COUNT_IF(gap >= 1000000) OVER () n_up1m, COUNT_IF(gap <= -1000000) OVER () n_down1m, COUNT_IF(l.la - l.lb >= 5000000) OVER () n_life_up5m
FROM c JOIN l USING (ein) QUALIFY ROW_NUMBER() OVER (ORDER BY gap DESC) <= 20 OR ROW_NUMBER() OVER (ORDER BY gap ASC) <= 10 ORDER BY gap DESC;

-- ===== connection 3 =====

-- [22] PBGC sponsor name -> USAspending contract recipient name (R2), $ after trusteeship, state check (date fixed)
-- RESULT: canceled at the 300 s statement timeout. The distinct-name scan + regex over 93M R2 rows is too slow. Unresolved.
WITH p AS (SELECT TRIM(REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(' ' || REGEXP_REPLACE(UPPER(SPONSOR_NAME), '[^A-Z0-9]+', ' ') || ' ', ' (INC|INCORPORATED|CORP|CORPORATION|CO|COMPANY|LLC|LTD|LIMITED|LP|THE|OF) ', ' '), ' (INC|INCORPORATED|CORP|CORPORATION|CO|COMPANY|LLC|LTD|LIMITED|LP|THE|OF) ', ' '), ' +', ' ')) nm, MIN(DATE_OF_PBGC_TRUSTEESHIP) tr, MAX(STATE) st, COUNT(*) plans, SUM(TRY_TO_DOUBLE(NUMBER_OF_PARICIPANTS_AT_DATE_OF_PLAN_TERMINATION::varchar)) parts, MIN(SPONSOR_NAME) sponsor FROM LIBRARY_MARTS.LABOR.LABOR__FED_PBGC_TRUSTEED_PLANS WHERE DATE_OF_PBGC_TRUSTEESHIP >= '2008-01-01' GROUP BY 1 HAVING REGEXP_COUNT(nm, ' ') >= 1)
, n0 AS (SELECT RECIPIENT_NAME, TRIM(REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(' ' || REGEXP_REPLACE(UPPER(RECIPIENT_NAME), '[^A-Z0-9]+', ' ') || ' ', ' (INC|INCORPORATED|CORP|CORPORATION|CO|COMPANY|LLC|LTD|LIMITED|LP|THE|OF) ', ' '), ' (INC|INCORPORATED|CORP|CORPORATION|CO|COMPANY|LLC|LTD|LIMITED|LP|THE|OF) ', ' '), ' +', ' ')) nm FROM (SELECT DISTINCT RECIPIENT_NAME FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS_FULL_R2))
, n1 AS (SELECT n0.RECIPIENT_NAME, n0.nm FROM n0 JOIN (SELECT DISTINCT nm FROM p) pp ON pp.nm = n0.nm)
, r0 AS (SELECT RECIPIENT_NAME, RECIPIENT_STATE_CODE, DATE_TRUNC('month', TRY_TO_DATE(LEFT(ACTION_DATE, 10))) m, SUM(TRY_TO_DOUBLE(FEDERAL_ACTION_OBLIGATION::varchar)) amt, COUNT(*) tx FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS_FULL_R2 WHERE RECIPIENT_NAME IN (SELECT RECIPIENT_NAME FROM n1) GROUP BY 1,2,3)
, r AS (SELECT n1.nm, r0.RECIPIENT_STATE_CODE rst, r0.m, r0.amt, r0.tx FROM r0 JOIN n1 USING (RECIPIENT_NAME))
, j AS (SELECT p.nm, p.sponsor, p.tr, p.st, p.plans, p.parts, SUM(IFF(r.m > p.tr, r.amt, 0)) amt_after, SUM(IFF(r.m <= p.tr, r.amt, 0)) amt_before, SUM(IFF(r.m > p.tr, r.tx, 0)) tx_after, MAX(IFF(r.m > p.tr, r.m, NULL)) last_m, MAX(IFF(r.rst = p.st, 1, 0)) state_agree, LISTAGG(DISTINCT r.rst, ',') WITHIN GROUP (ORDER BY r.rst) rsts FROM p JOIN r ON r.nm = p.nm GROUP BY 1,2,3,4,5,6)
SELECT j.*, (SELECT COUNT(*) FROM p) pbgc_names, COUNT(*) OVER () names_hit, COUNT_IF(amt_after > 0) OVER () names_after, COUNT_IF(state_agree = 1) OVER () names_state_ok, SUM(IFF(state_agree = 1, amt_after, 0)) OVER () amt_after_state_ok, (SELECT MIN(ACTION_DATE) FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS_FULL_R2) r2_first, (SELECT MAX(ACTION_DATE) FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS_FULL_R2) r2_last
FROM j ORDER BY amt_after DESC NULLS LAST LIMIT 40;

-- [23] PBGC EIN -> Form 5500 (plan year ~2025): sponsors that handed a plan to PBGC and still file for other plans
WITH p AS (SELECT LPAD(REGEXP_REPLACE(EIN::varchar,'[^0-9]',''),9,'0') ein, MIN(SPONSOR_NAME) sponsor, MAX(STATE) st, MIN(DATE_OF_PBGC_TRUSTEESHIP) tr, COUNT(*) plans, SUM(TRY_TO_DOUBLE(NUMBER_OF_PARICIPANTS_AT_DATE_OF_PLAN_TERMINATION::varchar)) parts FROM LIBRARY_MARTS.LABOR.LABOR__FED_PBGC_TRUSTEED_PLANS WHERE LPAD(REGEXP_REPLACE(EIN::varchar,'[^0-9]',''),9,'0') <> '000000000' GROUP BY 1)
, f AS (SELECT LPAD(REGEXP_REPLACE(SPONS_DFE_EIN::varchar, '[^0-9]', ''), 9, '0') ein, COUNT(*) filings, MAX(SPONSOR_DFE_NAME) f_name, MAX(SPONS_DFE_MAIL_US_STATE) f_st, SUM(TRY_TO_DOUBLE(TOT_ACTIVE_PARTCP_CNT::varchar)) active, MIN(FORM_PLAN_YEAR_BEGIN_DATE) py0, MAX(FORM_TAX_PRD) py1 FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_DOL_FORM5500 GROUP BY 1)
, j AS (SELECT p.*, f.filings, f.f_name, f.f_st, f.active, f.py0, f.py1, IFF(SPLIT_PART(TRIM(REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(' ' || REGEXP_REPLACE(UPPER(p.sponsor), '[^A-Z0-9]+', ' ') || ' ', ' (INC|INCORPORATED|CORP|CORPORATION|CO|COMPANY|LLC|LTD|LIMITED|LP|THE|OF) ', ' '), ' (INC|INCORPORATED|CORP|CORPORATION|CO|COMPANY|LLC|LTD|LIMITED|LP|THE|OF) ', ' '), ' +', ' ')), ' ', 1) = SPLIT_PART(TRIM(REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(' ' || REGEXP_REPLACE(UPPER(f.f_name), '[^A-Z0-9]+', ' ') || ' ', ' (INC|INCORPORATED|CORP|CORPORATION|CO|COMPANY|LLC|LTD|LIMITED|LP|THE|OF) ', ' '), ' (INC|INCORPORATED|CORP|CORPORATION|CO|COMPANY|LLC|LTD|LIMITED|LP|THE|OF) ', ' '), ' +', ' ')), ' ', 1), 1, 0) word1_ok, IFF(p.st = f.f_st, 1, 0) st_ok FROM p JOIN f USING (ein))
SELECT j.*, (SELECT COUNT(*) FROM p) pbgc_eins, (SELECT COUNT(*) FROM f) f5500_eins, COUNT(*) OVER () hit, COUNT_IF(word1_ok = 1) OVER () hit_name_ok, COUNT_IF(word1_ok = 1 AND tr >= '2008-01-01') OVER () hit_name_ok_2008, SUM(IFF(word1_ok = 1, active, 0)) OVER () active_name_ok
FROM j ORDER BY word1_ok DESC, parts DESC LIMIT 30;

-- [24] FEC 2024 non-JFC PACs with $250K+ from individuals: low-share rate by treasurer (pol = contribs + IEs + transfers)
WITH c AS (SELECT CMTE_ID, UPPER(TRIM(TRES_NM)) tres, CMTE_NM, CMTE_TP, CMTE_DSGN FROM LIBRARY_MARTS.POLITICS.POLITICS__FEC_COMMITTEE WHERE CYCLE = 2024 AND CMTE_TP IN ('N','Q','O','V','W') AND COALESCE(CMTE_DSGN, '') <> 'J')
, s AS (SELECT CMTE_ID, TRY_TO_DOUBLE(TOTAL_RECEIPTS::varchar) r, TRY_TO_DOUBLE(TOTAL_DISBURSEMENTS::varchar) d, TRY_TO_DOUBLE(INDIVIDUAL_CONTRIBUTIONS::varchar) ind, COALESCE(TRY_TO_DOUBLE(CONTRIBUTIONS_TO_OTHER_COMMITTEES::varchar),0) + COALESCE(TRY_TO_DOUBLE(INDEPENDENT_EXPENDITURES::varchar),0) + COALESCE(TRY_TO_DOUBLE(TRANSFERS_TO_AFFILIATES::varchar),0) pol, COVERAGE_END_DATE ce FROM LIBRARY_MARTS.POLITICS.POLITICS__FED_FEC_PAC_SUMMARY WHERE COVERAGE_END_DATE BETWEEN '2023-01-01' AND '2025-01-31' QUALIFY ROW_NUMBER() OVER (PARTITION BY CMTE_ID ORDER BY COVERAGE_END_DATE DESC) = 1)
, j AS (SELECT c.*, s.r, s.d, s.ind, s.pol, s.ce, IFF(s.d > 0, s.pol / s.d, NULL) pshare FROM c LEFT JOIN s USING (CMTE_ID))
, t AS (SELECT tres, COUNT(*) pacs, COUNT_IF(ind >= 250000) elig, COUNT_IF(ind >= 250000 AND pshare < 0.10) low, SUM(IFF(ind >= 250000, ind, 0)) elig_ind, SUM(IFF(ind >= 250000 AND pshare < 0.10, ind, 0)) low_ind, SUM(IFF(ind >= 250000, pol, 0)) elig_pol, SUM(IFF(ind >= 250000, d, 0)) elig_d FROM j GROUP BY tres)
, k AS (SELECT t.*, ROW_NUMBER() OVER (ORDER BY pacs DESC) rk FROM t)
SELECT IFF(rk <= 12, tres, 'ALL OTHER') tres_g, SUM(pacs) pacs, SUM(elig) elig, SUM(low) low, ROUND(SUM(low) / NULLIF(SUM(elig), 0), 3) low_rate, ROUND(SUM(elig_ind)) elig_ind, ROUND(SUM(low_ind)) low_ind, ROUND(SUM(elig_pol) / NULLIF(SUM(elig_d), 0), 3) pooled_share, MIN(rk) rk
FROM k GROUP BY 1 ORDER BY rk;

-- [25] FEC 2024 non-JFC PACs, $1M+ from individuals, <10% to candidates/committees/IEs/transfers; IE check from Schedule E table
WITH c AS (SELECT CMTE_ID, UPPER(TRIM(TRES_NM)) tres, CMTE_NM, CMTE_TP, CMTE_DSGN FROM LIBRARY_MARTS.POLITICS.POLITICS__FEC_COMMITTEE WHERE CYCLE = 2024 AND CMTE_TP IN ('N','Q','O','V','W') AND COALESCE(CMTE_DSGN, '') <> 'J')
, s AS (SELECT CMTE_ID, TRY_TO_DOUBLE(TOTAL_RECEIPTS::varchar) r, TRY_TO_DOUBLE(TOTAL_DISBURSEMENTS::varchar) d, TRY_TO_DOUBLE(INDIVIDUAL_CONTRIBUTIONS::varchar) ind, COALESCE(TRY_TO_DOUBLE(CONTRIBUTIONS_TO_OTHER_COMMITTEES::varchar),0) + COALESCE(TRY_TO_DOUBLE(INDEPENDENT_EXPENDITURES::varchar),0) + COALESCE(TRY_TO_DOUBLE(TRANSFERS_TO_AFFILIATES::varchar),0) pol, COVERAGE_END_DATE ce FROM LIBRARY_MARTS.POLITICS.POLITICS__FED_FEC_PAC_SUMMARY WHERE COVERAGE_END_DATE BETWEEN '2023-01-01' AND '2025-01-31' QUALIFY ROW_NUMBER() OVER (PARTITION BY CMTE_ID ORDER BY COVERAGE_END_DATE DESC) = 1)
, j AS (SELECT c.*, s.r, s.d, s.ind, s.pol, s.ce, IFF(s.d > 0, s.pol / s.d, NULL) pshare FROM c LEFT JOIN s USING (CMTE_ID))
, tc AS (SELECT tres, COUNT(*) tres_pacs FROM c GROUP BY tres)
, e AS (SELECT SPE_ID, SUM(TRY_TO_DOUBLE(EXP_AMO::varchar)) ie_all, SUM(IFF(UPPER(COALESCE(IS_SUPERSEDED::varchar, 'F')) IN ('TRUE','T','1','Y','YES'), 0, TRY_TO_DOUBLE(EXP_AMO::varchar))) ie_live FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDEPENDENT_EXPENDITURES WHERE CYCLE_FILE::varchar = '2024' GROUP BY 1)
SELECT j.CMTE_ID, j.CMTE_NM, j.tres, tc.tres_pacs, j.CMTE_TP, j.CMTE_DSGN, ROUND(j.ind) ind, ROUND(j.d) disb, ROUND(j.pol) pol, ROUND(j.pshare, 3) pshare, ROUND(e.ie_live) ie_sched_e,
 COUNT(*) OVER () n_low, ROUND(SUM(j.ind) OVER ()) ind_low, COUNT_IF(e.ie_live > 0.10 * j.d) OVER () n_ie_contradicts
FROM j JOIN tc USING (tres) LEFT JOIN e ON e.SPE_ID = j.CMTE_ID WHERE j.ind >= 1000000 AND j.pshare < 0.10 ORDER BY j.ind DESC LIMIT 30;

-- [26] EAVS 2022: what the 'other' rejection columns and comments say for the top outliers
SELECT STATE_ABBR, JURISDICTION_NAME, C9R_OTHER, C9R, C9S_OTHER, C9S, C9T_OTHER, C9T, LEFT(C9COMMENTS, 400) c9comments
FROM LIBRARY_MARTS.POLITICS.POLITICS__FED_EAC_EAVS WHERE (STATE_ABBR, JURISDICTION_NAME) IN (('CA','ORANGE COUNTY'),('CA','LOS ANGELES COUNTY'),('CA','KINGS COUNTY'),('PA','PHILADELPHIA COUNTY'),('TX','BEXAR COUNTY'),('FL','HERNANDO COUNTY'),('NY','KINGS COUNTY'),('OR','WASHINGTON COUNTY'),('TX','HARRIS COUNTY'),('MI','MACOMB COUNTY'),('WA','KING COUNTY'));

-- [27] Canada: individuals over the yearly per-party cap, Part 2a lines only (annual party returns, lumps dropped)
WITH b AS (SELECT RECIPIENT, UPPER(TRIM(CONTRIBUTOR_NAME)) nm, CONTRIBUTOR_POSTAL_CODE pc, YEAR(FISCAL_ELECTION_DATE) yr, MONETARY_AMOUNT amt, CONTRIBUTION_RECEIVED_DATE rd FROM LIBRARY_MARTS.POLITICS.POLITICS__INTL_ELECTIONS_CANADA_CONTRIBUTIONS WHERE POLITICAL_ENTITY = 'Registered parties' AND CONTRIBUTOR_TYPE = 'Individuals' AND ELECTORAL_EVENT NOT ILIKE '%quarter%' AND PART_NUMBER_OF_RETURN = '2a' AND CONTRIBUTOR_NAME NOT ILIKE 'Contributions of%' AND CONTRIBUTOR_NAME IS NOT NULL)
, g AS (SELECT RECIPIENT, nm, pc, yr, SUM(amt) tot, COUNT(*) lines, COUNT(DISTINCT rd || '|' || amt) uniq_lines FROM b GROUP BY 1,2,3,4)
, x AS (SELECT g.*, CASE WHEN yr <= 2006 THEN 5400 WHEN yr <= 2011 THEN 1100 WHEN yr <= 2014 THEN 1200 WHEN yr = 2015 THEN 1500 ELSE 1500 + 25 * (yr - 2015) END cap, IFF(nm ILIKE '%ESTATE%' OR nm ILIKE '%SUCCESSION%', 1, 0) estate FROM g)
SELECT RECIPIENT, nm, pc, yr, tot, cap, lines, uniq_lines, estate, COUNT(*) OVER () n_over, COUNT_IF(estate = 1) OVER () n_over_estate, COUNT_IF(tot > 2 * cap) OVER () n_over_2x, COUNT_IF(lines > uniq_lines) OVER () n_over_with_dup_lines, ROUND(SUM(tot - cap) OVER ()) excess_all, ROUND(SUM(IFF(estate = 1, tot - cap, 0)) OVER ()) excess_estate, (SELECT COUNT(*) FROM g) n_keys
FROM x WHERE tot > cap * 1.10 QUALIFY ROW_NUMBER() OVER (ORDER BY estate, tot - cap DESC) <= 25 ORDER BY estate, tot - cap DESC;

-- [28] IRS 527: 8872 totals (raw, deduped) vs Schedule A and B line tables for the top-gap EINs, plus biggest B line
WITH r AS (SELECT LPAD(REGEXP_REPLACE(EIN::varchar,'[^0-9]',''),9,'0') ein, MAX(ORGANIZATION_NAME) org, SUM(TRY_TO_DOUBLE(TOTAL_SCHED_A::varchar)) a_raw, SUM(TRY_TO_DOUBLE(TOTAL_SCHED_B::varchar)) b_raw FROM LIBRARY_MARTS.POLITICS.POLITICS__IRS527_8872_REPORTS WHERE LPAD(REGEXP_REPLACE(EIN::varchar,'[^0-9]',''),9,'0') IN ('823855986','113655877','202517748','394485462','522257109','270160261') GROUP BY 1)
, d AS (SELECT ein, SUM(a) a_dd, SUM(b) b_dd FROM (SELECT LPAD(REGEXP_REPLACE(EIN::varchar,'[^0-9]',''),9,'0') ein, TRY_TO_DOUBLE(TOTAL_SCHED_A::varchar) a, TRY_TO_DOUBLE(TOTAL_SCHED_B::varchar) b FROM LIBRARY_MARTS.POLITICS.POLITICS__IRS527_8872_REPORTS WHERE LPAD(REGEXP_REPLACE(EIN::varchar,'[^0-9]',''),9,'0') IN ('823855986','113655877','202517748','394485462','522257109','270160261') QUALIFY ROW_NUMBER() OVER (PARTITION BY LPAD(REGEXP_REPLACE(EIN::varchar,'[^0-9]',''),9,'0'), PERIOD_BEGIN_DATE, PERIOD_END_DATE ORDER BY INSERT_DATETIME DESC, FORM_ID_NUMBER DESC) = 1) GROUP BY 1)
, sa AS (SELECT LPAD(REGEXP_REPLACE(EIN::varchar,'[^0-9]',''),9,'0') ein, COUNT(*) a_lines, SUM(TRY_TO_DOUBLE(CONTRIBUTION_AMOUNT::varchar)) a_lines_sum FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_IRS527_SCHEDULE_A_CONTRIBUTIONS WHERE LPAD(REGEXP_REPLACE(EIN::varchar,'[^0-9]',''),9,'0') IN ('823855986','113655877','202517748','394485462','522257109','270160261') GROUP BY 1)
, sb AS (SELECT LPAD(REGEXP_REPLACE(EIN::varchar,'[^0-9]',''),9,'0') ein, COUNT(*) b_lines, SUM(TRY_TO_DOUBLE(EXPENDITURE_AMOUNT::varchar)) b_lines_sum, MAX(TRY_TO_DOUBLE(EXPENDITURE_AMOUNT::varchar)) b_max, MAX_BY(RECIPIENT_NAME, TRY_TO_DOUBLE(EXPENDITURE_AMOUNT::varchar)) b_max_to, MAX_BY(EXPENDITURE_PURPOSE, TRY_TO_DOUBLE(EXPENDITURE_AMOUNT::varchar)) b_max_purpose, MAX_BY(EXPENDITURE_DATE, TRY_TO_DOUBLE(EXPENDITURE_AMOUNT::varchar)) b_max_date FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_IRS527_SCHEDULE_B_EXPENDITURES WHERE LPAD(REGEXP_REPLACE(EIN::varchar,'[^0-9]',''),9,'0') IN ('823855986','113655877','202517748','394485462','522257109','270160261') GROUP BY 1)
SELECT r.ein, r.org, ROUND(r.a_raw) a_raw, ROUND(r.b_raw) b_raw, ROUND(d.a_dd) a_dd, ROUND(d.b_dd) b_dd, sa.a_lines, ROUND(sa.a_lines_sum) a_lines_sum, sb.b_lines, ROUND(sb.b_lines_sum) b_lines_sum, sb.b_max, sb.b_max_to, sb.b_max_purpose, sb.b_max_date
FROM r LEFT JOIN d USING (ein) LEFT JOIN sa USING (ein) LEFT JOIN sb USING (ein) ORDER BY r.ein;
