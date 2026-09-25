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
