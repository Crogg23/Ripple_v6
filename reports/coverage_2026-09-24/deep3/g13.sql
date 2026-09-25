-- g13: deep pass 3, 2026-09-24. Python door (connect/db.py), QUERY_TAG 'deep3-2026-09-24'. Read-only.
-- Tables: POLITICS__WHO_WON, POLITICS__CA_LOBBY_CONTRIBUTIONS, POLITICS__CA_LOBBY_EMPLOYER,
--         POLITICS__FED_SENATE_LDA_LOBBYIST_POSITIONS, POLITICS__MEMBER_FEC_ID.
-- Budget: 35 statements total = 29 SELECT/WITH + 6 ALTER SESSION (3 connections, 2 each). No statement failed.
-- Results: g13/batch1_results.json, batch2_results.json, batch3_results.json. Runner: g13/run.py.

-- ===== connection 1 (batch1.sql)
ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300;
ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24';

-- S01 WHO_WON shape by office: years, race keys, fillers, unopposed, missing member IDs, winner=runner-up
SELECT office, MIN(year) y0, MAX(year) y1, COUNT(DISTINCT year) n_years, COUNT(*) n,
       COUNT(DISTINCT year||'|'||state||'|'||district||'|'||is_special) n_race_keys,
       COUNT_IF(winner_votes = 1) votes_eq_1, COUNT_IF(vote_share >= 0.9999) share_1,
       COUNT_IF(runner_up IS NULL) no_runner_up, COUNT_IF(bioguide IS NULL) no_bioguide,
       COUNT_IF(LOWER(TRIM(winner)) = LOWER(TRIM(runner_up))) winner_eq_runner, COUNT_IF(is_special) specials
FROM LIBRARY_MARTS.POLITICS.POLITICS__WHO_WON GROUP BY office ORDER BY office;

-- S02 WHO_WON same race content (office, state, district, winner, votes) repeated across rows
WITH g AS (
  SELECT office, state, district, winner, winner_votes, total_votes, COUNT(*) n, COUNT(DISTINCT year) ny,
         LISTAGG(DISTINCT year::string, ',') WITHIN GROUP (ORDER BY year::string) yrs
  FROM LIBRARY_MARTS.POLITICS.POLITICS__WHO_WON WHERE winner_votes > 1
  GROUP BY 1,2,3,4,5,6 HAVING COUNT(*) > 1)
SELECT office, state, district, winner, winner_votes, total_votes, n, ny, LEFT(yrs, 200) yrs,
       COUNT(*) OVER () n_groups, SUM(n) OVER () rows_in_groups, SUM(n - 1) OVER () excess_rows,
       SUM(n - 1) OVER (PARTITION BY office) excess_in_office
FROM g ORDER BY n DESC, office LIMIT 15;

-- S03 WHO_WON president: states won per candidate per year
SELECT year, winner, COUNT(*) states, SUM(winner_votes) votes
FROM LIBRARY_MARTS.POLITICS.POLITICS__WHO_WON WHERE office = 'PRESIDENT'
GROUP BY 1,2 ORDER BY 1, 3 DESC;

-- S04 WHO_WON drill: every row naming Doggett as winner
SELECT year, state, district, is_special, winner, winner_party, winner_votes, total_votes, vote_share,
       runner_up, bioguide, spine_name, match_method
FROM LIBRARY_MARTS.POLITICS.POLITICS__WHO_WON WHERE winner ILIKE '%Doggett%' ORDER BY year, district;

-- S05 WHO_WON House by year: seats, repeat winners in one year, fillers, unopposed-like, missing IDs
SELECT year, COUNT(*) house_rows, COUNT(DISTINCT state||'|'||district) seats, COUNT(DISTINCT winner) winners,
       COUNT(*) - COUNT(DISTINCT winner) repeat_winner_rows, COUNT_IF(winner_votes = 1) filler_1,
       COUNT_IF(vote_share >= 0.9999 OR runner_up IS NULL) unopposed_like, COUNT_IF(bioguide IS NULL) no_bio
FROM LIBRARY_MARTS.POLITICS.POLITICS__WHO_WON WHERE office = 'HOUSE' AND NOT is_special
GROUP BY year ORDER BY year;

-- S06 MEMBER_FEC_ID shape: keys vs bioguide, FEC id shape, FEC ids shared across members
SELECT COUNT(*) n, COUNT(DISTINCT member_key) keys_, COUNT(DISTINCT bioguide) bios, COUNT(DISTINCT fec_id) fec_ids,
       COUNT_IF(member_key <> bioguide) key_ne_bio, COUNT_IF(bioguide IS NULL) bio_null,
       COUNT_IF(member_key LIKE 'gt:%') gt_keys, COUNT(DISTINCT IFF(member_key <> bioguide, member_key, NULL)) keys_ne_bio,
       (SELECT COUNT(*) FROM (SELECT fec_id FROM LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_FEC_ID
                              GROUP BY 1 HAVING COUNT(DISTINCT member_key) > 1)) fec_multi_member,
       COUNT_IF(NOT REGEXP_LIKE(fec_id, '^[HSP][0-9A-Z]{8}$')) bad_fec_shape
FROM LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_FEC_ID;

-- S07 MEMBER_FEC_ID drill: the three BIOGUIDE values with 14-15 rows
SELECT bioguide, member_key, full_name, state, party, last_term_type, fec_id
FROM LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_FEC_ID
WHERE bioguide IN ('W000800', 'Y000066', 'Y000064') ORDER BY bioguide, member_key, fec_id;

-- S08 LDA mart by year and filing type: filings, lobbyists, posting window, covered flag vs filler text
SELECT filing_year, filing_type, COUNT(*) n, COUNT(DISTINCT filing_uuid) filings, COUNT(DISTINCT lobbyist_id) lobbyist_ids,
       MIN(LEFT(dt_posted, 10)) posted_first, MAX(LEFT(dt_posted, 10)) posted_last,
       COUNT_IF(has_covered_position = 'True') hcp_true,
       COUNT_IF(UPPER(TRIM(covered_position)) IN ('N/A','NA','NONE','N.A.','NOT APPLICABLE','SEE PRIOR FILING')) filler_text
FROM LIBRARY_MARTS.POLITICS.POLITICS__FED_SENATE_LDA_LOBBYIST_POSITIONS
GROUP BY 1,2 ORDER BY 1, 3 DESC;

-- S09 LDA landing table by year (does the mart hold everything landed?)
SELECT filing_year, COUNT(*) n, COUNT(DISTINCT filing_uuid) filings
FROM LIBRARY_RAW.LANDING.FED_SENATE_LDA_LOBBYIST_POSITIONS GROUP BY 1 ORDER BY 1;

-- S10 LDA covered position: top values and the flag they carry
SELECT has_covered_position, LEFT(covered_position, 90) cp, COUNT(*) n, COUNT(DISTINCT lobbyist_id) lobbyist_ids
FROM LIBRARY_MARTS.POLITICS.POLITICS__FED_SENATE_LDA_LOBBYIST_POSITIONS
GROUP BY 1,2 ORDER BY n DESC LIMIT 30;

-- S11 LDA peer: registrants with 20+ lobbyists, share whose covered position is real text
WITH l AS (
  SELECT registrant_id, ANY_VALUE(registrant_name) rn, lobbyist_id,
         MAX(IFF(NULLIF(TRIM(covered_position), '') IS NULL
                 OR UPPER(TRIM(covered_position)) IN ('N/A','NA','NONE','N.A.','NOT APPLICABLE','SEE PRIOR FILING','SEE PRIOR FILINGS','NO','-'), 0, 1)) cov,
         MAX(IFF(UPPER(covered_position) LIKE 'SEE PRIOR%', 1, 0)) see_prior
  FROM LIBRARY_MARTS.POLITICS.POLITICS__FED_SENATE_LDA_LOBBYIST_POSITIONS GROUP BY 1, 3),
r AS (SELECT registrant_id, ANY_VALUE(rn) rn, COUNT(*) lobbyists, SUM(cov) cov, SUM(see_prior) see_prior FROM l GROUP BY 1)
SELECT rn, lobbyists, cov, ROUND(cov / lobbyists, 3) share, see_prior,
       MEDIAN(cov / lobbyists) OVER () med_share_20plus, COUNT(*) OVER () n_regs_20plus,
       (SELECT SUM(cov) FROM r) all_cov, (SELECT SUM(lobbyists) FROM r) all_lobbyist_ids
FROM r WHERE lobbyists >= 20 ORDER BY share DESC LIMIT 20;

-- S12 LDA former members of Congress: covered position that starts with a member title
WITH m AS (
  SELECT TRIM(lobbyist_first_name)||' '||TRIM(lobbyist_last_name) nm, registrant_name, covered_position, client_name, general_issue
  FROM LIBRARY_MARTS.POLITICS.POLITICS__FED_SENATE_LDA_LOBBYIST_POSITIONS
  WHERE covered_position ILIKE ANY ('member of congress%', 'member, u.s. house%', 'u.s. representative%', 'united states representative%',
        'u.s. senator%', 'united states senator%', 'member of the u.s. house%', 'member, house of rep%', 'congressman%',
        'congresswoman%', 'senator%', 'member, u.s. senate%', 'member of the house%', 'representative%', 'former member%'))
SELECT nm, ANY_VALUE(registrant_name) registrant, LEFT(ANY_VALUE(covered_position), 90) cp,
       COUNT(DISTINCT client_name) clients, COUNT(DISTINCT general_issue) issues, COUNT(*) rows_,
       COUNT(*) OVER () n_people
FROM m GROUP BY nm ORDER BY clients DESC LIMIT 25;

-- S13 CA contributions by filing period: rows, filers, money, blanks, duplicate-looking rows
SELECT filing_period_start_dt, filing_period_end_dt, COUNT(*) n, COUNT(DISTINCT filer_id) filers,
       COUNT(DISTINCT recipient_id) recip_ids, SUM(amount) amt, MEDIAN(amount) med, COUNT_IF(amount <= 0) nonpos,
       COUNT_IF(recipient_id IS NULL OR recipient_id = '0') no_recip_id, COUNT_IF(contribution_dt IS NOT NULL) has_cdt,
       COUNT(*) - COUNT(DISTINCT filer_id||'|'||recipient_name||'|'||amount) dup_like
FROM LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_CONTRIBUTIONS GROUP BY 1,2 ORDER BY 1,2;

-- S14 CA contributions top recipient IDs, with how many name spellings each carries
SELECT recipient_id, COUNT(*) n, SUM(amount) amt, COUNT(DISTINCT recipient_name) n_names,
       LEFT(LISTAGG(DISTINCT recipient_name, ' | '), 300) names, ROUND(RATIO_TO_REPORT(SUM(amount)) OVER (), 4) share,
       COUNT(DISTINCT filer_id) filers
FROM LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_CONTRIBUTIONS GROUP BY 1 ORDER BY amt DESC LIMIT 15;

-- S15 CA contributions join: who the filers are (employer, firm, lobbyist, none) by period, and Gray Davis money
WITH f AS (
  SELECT filer_id, filing_period_start_dt p, COUNT(*) n, SUM(amount) amt,
         SUM(IFF(recipient_name ILIKE '%DAVIS%' AND (recipient_name ILIKE '%GRAY%' OR recipient_name ILIKE '%GOVERNOR%'), amount, 0)) davis
  FROM LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_CONTRIBUTIONS GROUP BY 1,2),
emp AS (SELECT DISTINCT employer_id id FROM LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_EMPLOYER),
fm AS (SELECT DISTINCT firm_id id FROM LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_FIRM),
lb AS (SELECT lobbyist_id id FROM LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_EMP_LOBBYIST
       UNION SELECT lobbyist_id FROM LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_FIRM_LOBBYIST)
SELECT f.p, CASE WHEN emp.id IS NOT NULL THEN 'employer' WHEN fm.id IS NOT NULL THEN 'firm'
                 WHEN lb.id IS NOT NULL THEN 'lobbyist' ELSE 'unmatched' END kind,
       COUNT(DISTINCT f.filer_id) filers, SUM(f.n) rows_, SUM(f.amt) amt, SUM(f.davis) davis
FROM f LEFT JOIN emp ON emp.id = f.filer_id LEFT JOIN fm ON fm.id = f.filer_id LEFT JOIN lb ON lb.id = f.filer_id
GROUP BY 1,2 ORDER BY 1,2;

-- S16 CA employer shape: sessions, does SESSION_TOTAL add up to years or quarters, constant columns
SELECT session_id, session_yr_1, session_yr_2, COUNT(*) n, COUNT(DISTINCT employer_id) ids,
       SUM(session_total_amt) tot, SUM(yr_1_ytd_amt) y1, SUM(yr_2_ytd_amt) y2,
       SUM(COALESCE(qtr_1,0)+COALESCE(qtr_2,0)+COALESCE(qtr_3,0)+COALESCE(qtr_4,0)) q1_4,
       SUM(COALESCE(qtr_5,0)+COALESCE(qtr_6,0)+COALESCE(qtr_7,0)+COALESCE(qtr_8,0)) q5_8, SUM(current_qtr_amt) cur_q,
       COUNT_IF(yr_1_ytd_amt <> 0) y1_nonzero,
       COUNT_IF(COALESCE(qtr_1,0) <> 0 OR COALESCE(qtr_2,0) <> 0 OR COALESCE(qtr_3,0) <> 0 OR COALESCE(qtr_4,0) <> 0) q1_4_nonzero,
       COUNT_IF(ABS(session_total_amt - (COALESCE(yr_1_ytd_amt,0) + COALESCE(yr_2_ytd_amt,0))) > 1) tot_ne_years,
       COUNT_IF(ABS(session_total_amt - (COALESCE(qtr_1,0)+COALESCE(qtr_2,0)+COALESCE(qtr_3,0)+COALESCE(qtr_4,0)
                +COALESCE(qtr_5,0)+COALESCE(qtr_6,0)+COALESCE(qtr_7,0)+COALESCE(qtr_8,0))) > 1) tot_ne_quarters,
       COUNT_IF(contributor_id = '0' OR contributor_id IS NULL) contrib_0, COUNT(DISTINCT interest_name) interests,
       COUNT_IF(interest_name IS NULL) no_interest, COUNT_IF(session_total_amt = 0) zero_total
FROM LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_EMPLOYER GROUP BY 1,2,3 ORDER BY 1;

-- S17 CA employer peer: each industry's total, median employer, and its biggest spender's share
WITH r AS (
  SELECT interest_name, employer_name, session_total_amt amt,
         SUM(session_total_amt) OVER (PARTITION BY interest_name) itot, COUNT(*) OVER (PARTITION BY interest_name) n,
         MEDIAN(session_total_amt) OVER (PARTITION BY interest_name) med,
         ROW_NUMBER() OVER (PARTITION BY interest_name ORDER BY session_total_amt DESC) rk
  FROM LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_EMPLOYER)
SELECT interest_name, n, itot, med, employer_name top_employer, amt top_amt,
       ROUND(amt / NULLIF(itot, 0), 3) top_share, ROUND(amt / NULLIF(med, 0), 1) x_median,
       ROUND(RATIO_TO_REPORT(itot) OVER (), 3) interest_share
FROM r WHERE rk = 1 ORDER BY itot DESC;

-- ===== connection 2 (batch2.sql)
ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300;
ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24';

-- S18 WHO_WON: is BIOGUIDE right? one member matched to 2+ seats in a year, or winner surname differs from the matched member
WITH w AS (
  SELECT year, office, state, district, winner, spine_name, bioguide, match_method,
         COUNT(*) OVER (PARTITION BY year, office, bioguide) nb,
         SPLIT_PART(REGEXP_REPLACE(REGEXP_REPLACE(UPPER(TRIM(winner)), '[,.]', ''), ' (JR|SR|II|III|IV)$', ''), ' ', -1) s_w,
         SPLIT_PART(REGEXP_REPLACE(REGEXP_REPLACE(UPPER(TRIM(spine_name)), '[,.]', ''), ' (JR|SR|II|III|IV)$', ''), ' ', -1) s_s
  FROM LIBRARY_MARTS.POLITICS.POLITICS__WHO_WON WHERE bioguide IS NOT NULL AND office <> 'PRESIDENT')
SELECT year, office, state, district, winner, spine_name, bioguide, nb, s_w, s_s,
       COUNT_IF(nb > 1) OVER () n_double_rows, COUNT_IF(s_w <> s_s) OVER () n_surname_diff, COUNT(*) OVER () n_matched
FROM w QUALIFY nb > 1 OR s_w <> s_s ORDER BY nb DESC, year LIMIT 40;

-- S19 WHO_WON: which states lost House seats in 1996 and 2006 versus the election before
SELECT state, COUNT_IF(year = 1994) y1994, COUNT_IF(year = 1996) y1996, COUNT_IF(year = 2004) y2004, COUNT_IF(year = 2006) y2006
FROM LIBRARY_MARTS.POLITICS.POLITICS__WHO_WON
WHERE office = 'HOUSE' AND NOT is_special AND year IN (1994, 1996, 2004, 2006)
GROUP BY state HAVING COUNT_IF(year = 1994) <> COUNT_IF(year = 1996) OR COUNT_IF(year = 2004) <> COUNT_IF(year = 2006)
ORDER BY state;

-- S20 WHO_WON peer + time: share of House seat-elections with no runner-up, by state, 2010-2018 vs 1976-1984
WITH s AS (
  SELECT state,
         COUNT_IF(year BETWEEN 2010 AND 2018) n_late,
         COUNT_IF(year BETWEEN 2010 AND 2018 AND (runner_up IS NULL OR vote_share >= 0.9999)) u_late,
         COUNT_IF(year BETWEEN 1976 AND 1984) n_early,
         COUNT_IF(year BETWEEN 1976 AND 1984 AND (runner_up IS NULL OR vote_share >= 0.9999)) u_early,
         COUNT_IF(winner_votes = 1) filler_1
  FROM LIBRARY_MARTS.POLITICS.POLITICS__WHO_WON WHERE office = 'HOUSE' AND NOT is_special GROUP BY state)
SELECT state, n_late, u_late, ROUND(u_late / NULLIF(n_late, 0), 3) sh_late, n_early, u_early,
       ROUND(u_early / NULLIF(n_early, 0), 3) sh_early, filler_1,
       MEDIAN(u_late / NULLIF(n_late, 0)) OVER () med_state_late, SUM(u_late) OVER () tot_u_late, SUM(n_late) OVER () tot_n_late,
       SUM(u_early) OVER () tot_u_early, SUM(n_early) OVER () tot_n_early
FROM s ORDER BY sh_late DESC, u_late DESC LIMIT 15;

-- S21 MEMBER_FEC_ID land rate: sitting members with and without an FEC row
SELECT x.last_term_type, COUNT(*) current_members, COUNT(f.member_key) with_fec_row,
       LEFT(LISTAGG(IFF(f.member_key IS NULL, x.full_name, NULL), '; '), 600) missing_names
FROM LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_CROSSWALK x
LEFT JOIN (SELECT DISTINCT member_key FROM LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_FEC_ID) f ON f.member_key = x.member_key
WHERE x.legislator_set = 'current' GROUP BY 1 ORDER BY 1;

-- S22 LDA landing (full source) by year: people, people with a real covered position, former members, flag vs filler
WITH l AS (
  SELECT filing_year, UPPER(TRIM(lobbyist_first_name))||' '||UPPER(TRIM(lobbyist_last_name)) nm,
         UPPER(TRIM(covered_position)) cp, has_covered_position::string hcp
  FROM LIBRARY_RAW.LANDING.FED_SENATE_LDA_LOBBYIST_POSITIONS),
k AS (
  SELECT filing_year, nm, cp, hcp,
         IFF(NULLIF(cp, '') IS NULL OR cp IN ('N/A','NA','NONE','N.A.','NOT APPLICABLE','SEE PRIOR FILING','SEE PRIOR FILINGS','NO','-',
             'PRESIDENT','VICE PRESIDENT','PRINCIPAL','PARTNER','LOBBYIST','CEO','OWNER','DIRECTOR','CONSULTANT','LEGISLATIVE CONSULTANT',
             'SENIOR VICE PRESIDENT','COUNSEL','ATTORNEY','EXECUTIVE DIRECTOR','MANAGING DIRECTOR','SHAREHOLDER','OF COUNSEL','ASSOCIATE','MEMBER'), 0, 1) real_cp,
         IFF(cp ILIKE ANY ('MEMBER OF CONGRESS%', 'FORMER MEMBER%', 'U.S. REPRESENTATIVE%', 'UNITED STATES REPRESENTATIVE%', 'U.S. SENATOR%',
             'UNITED STATES SENATOR%', 'MEMBER, U.S. HOUSE%', 'MEMBER, HOUSE OF REP%', 'MEMBER OF THE U.S. HOUSE%', 'MEMBER, U.S. SENATE%',
             'FMR CONG%', 'FORMER CONGRESSMAN%', 'FORMER SENATOR%', 'FORMER U.S. SENATOR%', 'FORMER U.S. REP%'), 1, 0) ex_member
  FROM l)
SELECT filing_year, COUNT(*) n, COUNT(DISTINCT nm) people, COUNT(DISTINCT IFF(real_cp = 1, nm, NULL)) people_real_cp,
       ROUND(COUNT(DISTINCT IFF(real_cp = 1, nm, NULL)) / NULLIF(COUNT(DISTINCT nm), 0), 3) share_real_cp,
       COUNT(DISTINCT IFF(ex_member = 1, nm, NULL)) ex_members,
       COUNT_IF(LOWER(hcp) = 'true') flag_true_rows, COUNT_IF(LOWER(hcp) = 'true' AND real_cp = 0) flag_true_but_filler
FROM k GROUP BY 1 ORDER BY 1;

-- S23 CA contributions join to CA_LOBBY_COVER: what kind of filer made each contribution, by year, and Gray Davis money
WITH cv AS (
  SELECT filer_id, LISTAGG(DISTINCT entity_cd, '/') WITHIN GROUP (ORDER BY entity_cd) ent,
         LISTAGG(DISTINCT form_type, '/') WITHIN GROUP (ORDER BY form_type) forms
  FROM LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_COVER GROUP BY 1),
c AS (
  SELECT filer_id, YEAR(filing_period_start_dt) yr, COUNT(*) n, SUM(amount) amt,
         SUM(IFF(recipient_name ILIKE '%DAVIS%' AND (recipient_name ILIKE '%GRAY%' OR recipient_name ILIKE '%GOVERNOR%'), amount, 0)) davis
  FROM LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_CONTRIBUTIONS GROUP BY 1, 2)
SELECT yr, COALESCE(cv.ent, 'NOT IN COVER') ent, COALESCE(cv.forms, '-') forms, COUNT(*) filers, SUM(n) rows_, SUM(amt) amt, SUM(davis) davis
FROM c LEFT JOIN cv ON cv.filer_id = c.filer_id GROUP BY 1, 2, 3 ORDER BY 1, amt DESC;

-- S24 CA contributions drill: rows from individual-lobbyist filers (entity LBY) in 2001, or to Gray Davis in any period
WITH cv AS (
  SELECT filer_id, LISTAGG(DISTINCT entity_cd, '/') WITHIN GROUP (ORDER BY entity_cd) ent,
         ANY_VALUE(TRIM(filer_naml||', '||COALESCE(filer_namf, ''))) nm
  FROM LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_COVER GROUP BY 1)
SELECT c.filing_period_start_dt, c.filing_period_end_dt, c.filer_id, cv.nm, cv.ent, c.recipient_name, c.recipient_id, c.amount
FROM LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_CONTRIBUTIONS c LEFT JOIN cv ON cv.filer_id = c.filer_id
WHERE cv.ent ILIKE '%LBY%'
  AND (YEAR(c.filing_period_start_dt) = 2001
       OR (c.recipient_name ILIKE '%DAVIS%' AND (c.recipient_name ILIKE '%GRAY%' OR c.recipient_name ILIKE '%GOVERNOR%')))
ORDER BY c.amount DESC LIMIT 60;

-- S25 CA employer join: lobbying spend vs campaign money the same employer reported giving in 2000
WITH c AS (
  SELECT filer_id, SUM(amount) given, COUNT(*) n_gifts
  FROM LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_CONTRIBUTIONS WHERE YEAR(filing_period_start_dt) = 2000 GROUP BY 1),
e AS (
  SELECT employer_id, ANY_VALUE(employer_name) nm, ANY_VALUE(interest_name) intr, MAX(session_total_amt) lob
  FROM LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_EMPLOYER GROUP BY 1)
SELECT nm, intr, lob, given, n_gifts, ROUND(given / NULLIF(lob, 0), 2) given_per_lobby_dollar,
       COUNT(*) OVER () n_employers, COUNT(given) OVER () n_giving, SUM(given) OVER () total_given, SUM(lob) OVER () total_lob,
       MEDIAN(given / NULLIF(lob, 0)) OVER () med_ratio_givers
FROM e LEFT JOIN c ON c.filer_id = e.employer_id
ORDER BY given DESC NULLS LAST LIMIT 20;

-- ===== connection 3 (batch3.sql)
ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300;
ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24';

-- S26 WHO_WON: size the BIOGUIDE surname-match problem: doubled IDs in one year (floor) and first-initial disagreement (ceiling)
WITH w AS (
  SELECT year, office, state, district, winner, spine_name, bioguide,
         COUNT(*) OVER (PARTITION BY year, office, bioguide) nb,
         LEFT(REGEXP_REPLACE(UPPER(TRIM(winner)), '[^A-Z ]', ''), 1) fi_w,
         LEFT(UPPER(TRIM(spine_name)), 1) fi_s
  FROM LIBRARY_MARTS.POLITICS.POLITICS__WHO_WON WHERE bioguide IS NOT NULL AND office <> 'PRESIDENT')
SELECT COUNT(*) matched, COUNT_IF(nb > 1) doubled_rows, COUNT(DISTINCT IFF(nb > 1, bioguide, NULL)) doubled_bioguides,
       COUNT_IF(fi_w <> fi_s) first_initial_diff, COUNT_IF(fi_w <> fi_s AND nb > 1) fi_diff_and_doubled,
       COUNT(DISTINCT IFF(fi_w <> fi_s, bioguide, NULL)) fi_diff_bioguides,
       LEFT(LISTAGG(DISTINCT IFF(fi_w <> fi_s AND nb = 1, winner||' -> '||spine_name, NULL), '; '), 1800) sample_fi_diff_not_doubled
FROM w;

-- S27 WHO_WON drill: Georgia and Alabama House winners with no runner-up, 2010-2018 (real unopposed or missing data?)
SELECT state, year, district, winner, winner_party, winner_votes, total_votes, vote_share, runner_up
FROM LIBRARY_MARTS.POLITICS.POLITICS__WHO_WON
WHERE office = 'HOUSE' AND NOT is_special AND year BETWEEN 2010 AND 2018 AND state IN ('GA', 'AL')
  AND (runner_up IS NULL OR vote_share >= 0.9999)
ORDER BY state, district, year;

-- S28 LDA landing: people listing a past executive-branch job vs a past Hill job, by year (admin-change test)
WITH k AS (
  SELECT filing_year, UPPER(TRIM(lobbyist_first_name))||' '||UPPER(TRIM(lobbyist_last_name)) nm, UPPER(TRIM(covered_position)) cp
  FROM LIBRARY_RAW.LANDING.FED_SENATE_LDA_LOBBYIST_POSITIONS
  WHERE NULLIF(TRIM(covered_position), '') IS NOT NULL
    AND UPPER(TRIM(covered_position)) NOT IN ('N/A','NA','NONE','N.A.','NOT APPLICABLE','SEE PRIOR FILING','SEE PRIOR FILINGS','NO','-')),
f AS (
  SELECT filing_year, nm,
         MAX(IFF(cp ILIKE ANY ('%WHITE HOUSE%','%DEPARTMENT%','%DEPT%','%ADMINISTRAT%','%AGENCY%','%OMB%','%OFFICE OF MANAGEMENT%',
             '%TREASURY%','%USDA%','%DOD%','%PENTAGON%','%EPA%','%COMMISSION%','%BUREAU%','%NATIONAL SECURITY COUNCIL%',
             '%EXECUTIVE OFFICE%','%USTR%','%TRADE REPRESENTATIVE%','%ASSISTANT SECRETARY%','%DEPUTY SECRETARY%','%UNDER SECRETARY%'), 1, 0)) ex_exec,
         MAX(IFF(cp ILIKE ANY ('%SENATOR%','%SEN.%','%REP.%','%CONGRESS%','%COMMITTEE%','%CMTE%','%SENATE%','%U.S. HOUSE%','%HOUSE OF REP%'), 1, 0)) ex_hill
  FROM k GROUP BY 1, 2)
SELECT filing_year, COUNT(*) people_any_text, SUM(ex_exec) exec_people, SUM(ex_hill) hill_people,
       COUNT_IF(ex_exec = 1 AND ex_hill = 0) exec_only, COUNT_IF(ex_hill = 1 AND ex_exec = 0) hill_only
FROM f WHERE filing_year::string >= '2011' GROUP BY 1 ORDER BY 1;

-- S29 CA contributions drill: filers whose ID matches only the CA lobbyist lists, giving to Gray Davis or giving in 2001
WITH lb AS (
  SELECT id, ANY_VALUE(nm) nm, ANY_VALUE(org) org FROM (
    SELECT lobbyist_id id, lobbyist_last_name||', '||lobbyist_first_name nm, employer_name org FROM LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_EMP_LOBBYIST
    UNION ALL
    SELECT lobbyist_id, lobbyist_last_name||', '||lobbyist_first_name, firm_name FROM LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_FIRM_LOBBYIST) GROUP BY 1)
SELECT c.filing_period_start_dt, c.filer_id, lb.nm, lb.org, c.recipient_name, c.amount
FROM LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_CONTRIBUTIONS c JOIN lb ON lb.id = c.filer_id
WHERE c.filer_id NOT IN (SELECT employer_id FROM LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_EMPLOYER WHERE employer_id IS NOT NULL)
  AND c.filer_id NOT IN (SELECT firm_id FROM LIBRARY_MARTS.POLITICS.POLITICS__CA_LOBBY_FIRM WHERE firm_id IS NOT NULL)
  AND ((c.recipient_name ILIKE '%DAVIS%' AND (c.recipient_name ILIKE '%GRAY%' OR c.recipient_name ILIKE '%GOVERNOR%'))
       OR YEAR(c.filing_period_start_dt) = 2001)
ORDER BY c.amount DESC LIMIT 40;

