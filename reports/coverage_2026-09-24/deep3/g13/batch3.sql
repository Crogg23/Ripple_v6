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
