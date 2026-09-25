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
