-- deep-9: coverage round 2, group 9. Hand queries, 2026-09-24. Read-only.
-- Session: STATEMENT_TIMEOUT_IN_SECONDS=300, QUERY_TAG='coverage-r2-2026-09-24'

-- Q1: VA suicide: count + 5-row sample
SELECT t.*, COUNT(*) OVER () AS total_rows FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_VA_SUICIDE_STATE t ORDER BY YEAR_OF_DEATH DESC LIMIT 5;

-- Q2: FHFA suspended: count + 5-row sample
SELECT t.*, COUNT(*) OVER () AS total_rows FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_FHFA_SUSPENDED_COUNTERPARTY t ORDER BY EFFECTIVE_DATE DESC LIMIT 5;

-- Q3: FQHC site people: count + 5-row sample (excluded rows first)
SELECT t.*, COUNT(*) OVER () AS total_rows FROM LIBRARY_MARTS.HEALTH.HEALTH__FQHC_SITE_PEOPLE t ORDER BY IS_EXCLUDED DESC NULLS LAST LIMIT 5;

-- Q4: LEIE: count + 5-row sample (newest)
SELECT t.*, COUNT(*) OVER () AS total_rows FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE t ORDER BY EXCLUSION_DATE DESC LIMIT 5;

-- Q5: HRSA shortage: count + 5-row sample
SELECT t.*, COUNT(*) OVER () AS total_rows FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_SHORTAGE_AREAS t LIMIT 5;

-- Q6: VA suicide: pooled 2011-13 vs 2021-23 crude rate per state (deaths / veteran pop), with region peers and blank counts
WITH v AS (
  SELECT STATE, GEOGRAPHIC_REGION, YEAR_OF_DEATH y,
         TRY_TO_NUMBER(VETERAN_SUICIDES::string) d,
         TRY_TO_NUMBER(VETERAN_POPULATION_ESTIMATE::string) p,
         TRY_TO_DOUBLE(VETERAN_SUICIDE_RATE_PER_100K::string) r
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_VA_SUICIDE_STATE
), s AS (
  SELECT STATE, ANY_VALUE(GEOGRAPHIC_REGION) region,
         MIN(y) y0, MAX(y) y1, COUNT(*) n_years,
         SUM(IFF(d IS NULL,1,0)) blank_deaths, SUM(IFF(r IS NULL,1,0)) blank_rate,
         SUM(IFF(y BETWEEN 2011 AND 2013, d, 0)) d_early,
         SUM(IFF(y BETWEEN 2011 AND 2013 AND d IS NOT NULL, p, 0)) p_early,
         SUM(IFF(y BETWEEN 2021 AND 2023, d, 0)) d_late,
         SUM(IFF(y BETWEEN 2021 AND 2023 AND d IS NOT NULL, p, 0)) p_late,
         MAX(IFF(y = 2023, r, NULL)) r_2023_pub
  FROM v GROUP BY STATE
)
SELECT STATE, region, y0, y1, n_years, blank_deaths, blank_rate,
       d_early, ROUND(p_early/3) avg_pop_early, ROUND(1e5*d_early/NULLIF(p_early,0),1) rate_early,
       d_late,  ROUND(p_late/3)  avg_pop_late,  ROUND(1e5*d_late/NULLIF(p_late,0),1)  rate_late,
       ROUND((d_late/NULLIF(p_late,0))/NULLIF(d_early/NULLIF(p_early,0),0),2) ratio_late_early,
       r_2023_pub
FROM s ORDER BY rate_late DESC NULLS LAST;

-- Q7: HRSA: distinct shortage areas by discipline x designation type x status, score-0 share, designation-date range
SELECT HPSA_DISCIPLINE_CLASS, DESIGNATION_TYPE, HPSA_STATUS,
       COUNT(*) row_ct, COUNT(DISTINCT HPSA_ID) hpsas,
       COUNT(DISTINCT IFF(TRY_TO_NUMBER(HPSA_SCORE::string) = 0, HPSA_ID, NULL)) hpsas_score0,
       MIN(TRY_TO_DATE(HPSA_DESIGNATION_DATE, 'MM/DD/YYYY')) first_desig,
       MAX(TRY_TO_DATE(HPSA_DESIGNATION_DATE, 'MM/DD/YYYY')) last_desig,
       COUNT(DISTINCT IFF(TRY_TO_DATE(HPSA_DESIGNATION_DATE, 'MM/DD/YYYY') < '2000-01-01', HPSA_ID, NULL)) hpsas_pre2000,
       SUM(IFF(TRY_TO_DATE(HPSA_DESIGNATION_DATE, 'MM/DD/YYYY') IS NULL, 1, 0)) bad_dates
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_SHORTAGE_AREAS
GROUP BY 1,2,3 ORDER BY 1,2,3;

-- Q8: FQHC: excluded people at health-center addresses; how many updated NPPES after the ban
SELECT COUNT(*) excl_rows, COUNT(DISTINCT NPI) excl_npis,
       COUNT(DISTINCT IFF(NPPES_LAST_UPDATE_DATE >= EXCLUSION_DATE, NPI, NULL)) npis_nppes_updated_after_ban,
       COUNT(DISTINCT IFF(IS_HIGH_DENSITY_CAMPUS::string ILIKE 'true', NPI, NULL)) npis_on_campus_sites,
       COUNT(DISTINCT BPHC_ASSIGNED_NUMBER) sites, COUNT(DISTINCT HEALTH_CENTER_NAME) centers,
       MIN(EXCLUSION_DATE) min_excl, MAX(EXCLUSION_DATE) max_excl,
       COUNT(DISTINCT IFF(NPI_DEACTIVATION_DATE IS NOT NULL, NPI, NULL)) npis_deactivated,
       (SELECT COUNT(DISTINCT NPI) FROM LIBRARY_MARTS.HEALTH.HEALTH__FQHC_SITE_PEOPLE) all_npis,
       (SELECT COUNT(DISTINCT BPHC_ASSIGNED_NUMBER) FROM LIBRARY_MARTS.HEALTH.HEALTH__FQHC_SITE_PEOPLE) all_sites
FROM LIBRARY_MARTS.HEALTH.HEALTH__FQHC_SITE_PEOPLE
WHERE IS_EXCLUDED::string ILIKE 'true';

-- Q9: LEIE -> current Medicare enrollment (PECOS) on NPI, by ban year, waiver, entity; last name / org name as second field; PECOS carbon date from newest enrollment ID
WITH l AS (
  SELECT NPI, UPPER(TRIM(LAST_NAME)) ln, UPPER(TRIM(BUSINESS_NAME)) bn, EXCLUSION_DATE,
         HAS_WAIVER::string w, IS_ENTITY_NOT_INDIVIDUAL::string ent
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE
  WHERE NPI_IS_REAL::string ILIKE 'true'
), p AS (
  SELECT NPI, MAX(UPPER(TRIM(LAST_NAME))) ln, MAX(UPPER(TRIM(ORG_NAME))) org, COUNT(*) enrl
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PECOS_PROVIDER_ENROLLMENT GROUP BY NPI
)
SELECT CASE WHEN l.EXCLUSION_DATE < '2020-01-01' THEN 'a <2020' WHEN l.EXCLUSION_DATE < '2024-01-01' THEN 'b 2020-23'
            WHEN l.EXCLUSION_DATE < '2025-01-01' THEN 'c 2024' WHEN l.EXCLUSION_DATE < '2026-01-01' THEN 'd 2025' ELSE 'e 2026' END ban_bucket,
       l.w waiver, l.ent entity,
       COUNT(DISTINCT l.NPI) leie_npis,
       COUNT(DISTINCT p.NPI) in_pecos,
       COUNT(DISTINCT IFF(p.NPI IS NOT NULL AND (p.ln = l.ln OR (l.ent ILIKE 'true' AND LEFT(p.org,8) = LEFT(l.bn,8))), p.NPI, NULL)) in_pecos_name_agrees,
       (SELECT MAX(TRY_TO_DATE(SUBSTR(ENRLMT_ID,2,8),'YYYYMMDD')) FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PECOS_PROVIDER_ENROLLMENT) pecos_newest_enrollment
FROM l LEFT JOIN p ON p.NPI = l.NPI
GROUP BY 1,2,3 ORDER BY 1,2,3;

-- Q10: FHFA suspended people -> SAM exclusions (individuals) on first+last name; state and city as second fields
WITH st AS (SELECT DISTINCT PRIMARY_STATE_NAME nm, PRIMARY_STATE_ABBREVIATION ab FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_SHORTAGE_AREAS),
f AS (
  SELECT UPPER(SPLIT_PART(TRIM(FIRST_NAME),' ',1)) fn, UPPER(TRIM(LAST_NAME)) ln, UPPER(TRIM(CITY)) city, st.ab, EFFECTIVE_DATE
  FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_FHFA_SUSPENDED_COUNTERPARTY h LEFT JOIN st ON st.nm = h.STATE
  WHERE COALESCE(TRIM(LAST_NAME),'') <> ''
), s AS (
  SELECT UPPER(TRIM(FIRST_NAME)) fn, UPPER(TRIM(LAST_NAME)) ln, UPPER(TRIM(CITY)) city, UPPER(TRIM(STATE)) st,
         EXCLUDING_AGENCY, EXCLUSION_TYPE, ACTIVATION_DATE, IS_CURRENTLY_EXCLUDED::string cur
  FROM LIBRARY_MARTS.PROCUREMENT.PROCUREMENT__FED_SAM_EXCLUSIONS
)
SELECT (SELECT COUNT(*) FROM f) fhfa_people, (SELECT COUNT(*) FROM f WHERE ab IS NULL) fhfa_state_unmapped,
       COUNT(DISTINCT f.fn||'|'||f.ln||'|'||COALESCE(f.ab,'')) people_name_hit_any_state,
       COUNT(DISTINCT IFF(s.st = f.ab, f.fn||'|'||f.ln, NULL)) people_same_state,
       COUNT(DISTINCT IFF(s.st = f.ab AND s.city = f.city, f.fn||'|'||f.ln, NULL)) people_same_city,
       COUNT(DISTINCT IFF(s.st = f.ab AND s.EXCLUDING_AGENCY = 'HUD', f.fn||'|'||f.ln, NULL)) same_state_by_hud,
       COUNT(DISTINCT IFF(s.st = f.ab AND s.ACTIVATION_DATE < f.EFFECTIVE_DATE, f.fn||'|'||f.ln, NULL)) same_state_sam_first,
       LISTAGG(DISTINCT IFF(s.st = f.ab, s.EXCLUDING_AGENCY, NULL), ',') agencies_same_state
FROM f JOIN s ON s.fn = f.fn AND s.ln = f.ln;

-- Q11: VA vs general population: state veteran suicide rate 2019-20 vs 2022-23 against CDC all-suicide state rows, same years
WITH c AS (
  SELECT ST_NAME st, LISTAGG(DISTINCT PERIOD, ',') WITHIN GROUP (ORDER BY PERIOD) periods,
         SUM(IFF(PERIOD IN ('2019','2020'), COUNT_SUP, 0)) c_early,
         SUM(IFF(PERIOD IN ('2019','2020'), COUNT_SUP / NULLIF(RATE,0) * 1e5, 0)) p_early,
         SUM(IFF(PERIOD IN ('2022','2023'), COUNT_SUP, 0)) c_late,
         SUM(IFF(PERIOD IN ('2022','2023'), COUNT_SUP / NULLIF(RATE,0) * 1e5, 0)) p_late
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_INJURY_VIOLENCE_COUNTY
  WHERE INTENT = 'All_Suicide' AND LENGTH(GEOID) = 2 AND COUNT_SUP IS NOT NULL AND RATE > 0
  GROUP BY 1
), v AS (
  SELECT STATE st, GEOGRAPHIC_REGION region,
         SUM(IFF(YEAR_OF_DEATH IN (2019,2020), TRY_TO_NUMBER(VETERAN_SUICIDES::string), 0)) d_early,
         SUM(IFF(YEAR_OF_DEATH IN (2019,2020), TRY_TO_NUMBER(VETERAN_POPULATION_ESTIMATE::string), 0)) p_early,
         SUM(IFF(YEAR_OF_DEATH IN (2022,2023), TRY_TO_NUMBER(VETERAN_SUICIDES::string), 0)) d_late,
         SUM(IFF(YEAR_OF_DEATH IN (2022,2023), TRY_TO_NUMBER(VETERAN_POPULATION_ESTIMATE::string), 0)) p_late
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_VA_SUICIDE_STATE GROUP BY 1,2
)
SELECT v.st, v.region, v.d_early vet_d_1920, v.d_late vet_d_2223,
       ROUND(1e5*v.d_early/NULLIF(v.p_early,0),1) vet_rate_1920, ROUND(1e5*v.d_late/NULLIF(v.p_late,0),1) vet_rate_2223,
       ROUND((v.d_late/NULLIF(v.p_late,0))/NULLIF(v.d_early/NULLIF(v.p_early,0),0),2) vet_ratio,
       c.c_early gen_d_1920, c.c_late gen_d_2223,
       ROUND(1e5*c.c_early/NULLIF(c.p_early,0),1) gen_rate_1920, ROUND(1e5*c.c_late/NULLIF(c.p_late,0),1) gen_rate_2223,
       ROUND((c.c_late/NULLIF(c.p_late,0))/NULLIF(c.c_early/NULLIF(c.p_early,0),0),2) gen_ratio,
       ROUND(vet_ratio/NULLIF(gen_ratio,0),2) vet_vs_gen, c.periods
FROM v LEFT JOIN c ON UPPER(c.st) = UPPER(v.st)
ORDER BY vet_vs_gen DESC NULLS LAST;

-- Q12: HRSA: currently designated geographic + high-needs areas, one row per HPSA_ID, by discipline x designation era: count, score 18+, median score
WITH h AS (
  SELECT HPSA_ID, HPSA_DISCIPLINE_CLASS disc,
         MIN(TRY_TO_DATE(HPSA_DESIGNATION_DATE,'MM/DD/YYYY')) d,
         MAX(TRY_TO_NUMBER(HPSA_SCORE::string)) sc,
         MAX(TRY_TO_DOUBLE(HPSA_DESIGNATION_POPULATION::string)) pop
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_SHORTAGE_AREAS
  WHERE HPSA_STATUS = 'Designated' AND DESIGNATION_TYPE IN ('Geographic HPSA','High Needs Geographic HPSA')
  GROUP BY 1,2
)
SELECT disc, CASE WHEN d < '1990-01-01' THEN 'a pre-1990' WHEN d < '2000-01-01' THEN 'b 1990s' WHEN d < '2010-01-01' THEN 'c 2000s'
                  WHEN d < '2020-01-01' THEN 'd 2010s' ELSE 'e 2020s' END era,
       COUNT(*) hpsas, SUM(IFF(sc >= 18,1,0)) score18plus, ROUND(100*score18plus/hpsas,1) pct18, MEDIAN(sc) med_score,
       ROUND(SUM(pop)/1e6,2) pop_m
FROM h GROUP BY 1,2 ORDER BY 1,2;

-- Q13: HRSA: list designated geographic/high-needs primary care + mental health areas first designated before 1990, still scoring 18+
WITH h AS (
  SELECT HPSA_ID, HPSA_DISCIPLINE_CLASS disc, ANY_VALUE(HPSA_NAME) nm, ANY_VALUE(PRIMARY_STATE_ABBREVIATION) st,
         LISTAGG(DISTINCT COMMON_COUNTY_NAME, '; ') counties,
         MIN(TRY_TO_DATE(HPSA_DESIGNATION_DATE,'MM/DD/YYYY')) d,
         MAX(TRY_TO_DATE(HPSA_DESIGNATION_LAST_UPDATE_DATE,'MM/DD/YYYY')) upd,
         MAX(TRY_TO_NUMBER(HPSA_SCORE::string)) sc,
         MAX(TRY_TO_DOUBLE(HPSA_DESIGNATION_POPULATION::string)) pop,
         MAX(TRY_TO_DOUBLE(HPSA_FTE::string)) fte, ANY_VALUE(HPSA_FORMAL_RATIO) ratio, ANY_VALUE(RURAL_STATUS) rural,
         ANY_VALUE(DESIGNATION_TYPE) dtype
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_SHORTAGE_AREAS
  WHERE HPSA_STATUS = 'Designated' AND DESIGNATION_TYPE IN ('Geographic HPSA','High Needs Geographic HPSA')
    AND HPSA_DISCIPLINE_CLASS IN ('Primary Care','Mental Health')
  GROUP BY 1,2
)
SELECT disc, HPSA_ID, nm, st, LEFT(counties,60) counties, d, upd, sc, pop, fte, ratio, rural, dtype
FROM h WHERE d < '1990-01-01' AND sc >= 18 ORDER BY disc DESC, sc DESC, d LIMIT 60;

-- Q14: FQHC: sites with 2+ excluded NPIs, or any excluded NPI whose NPPES record was updated after the ban
SELECT BPHC_ASSIGNED_NUMBER, ANY_VALUE(SITE_NAME) site, ANY_VALUE(HEALTH_CENTER_NAME) hc, ANY_VALUE(SITE_STATE) st,
       MAX(PEOPLE_AT_SITE) people_at_site, ANY_VALUE(IS_HIGH_DENSITY_CAMPUS::string) campus,
       COUNT(DISTINCT NPI) excl_npis,
       LISTAGG(DISTINCT FIRST_NAME||' '||LAST_NAME||' '||COALESCE(CREDENTIAL,'')||' excl '||EXCLUSION_DATE::string||' '||EXCLUSION_TYPE||' nppes '||NPPES_LAST_UPDATE_DATE::string, ' | ') who,
       MAX(IFF(NPPES_LAST_UPDATE_DATE >= EXCLUSION_DATE, 1, 0)) updated_after_ban
FROM LIBRARY_MARTS.HEALTH.HEALTH__FQHC_SITE_PEOPLE
WHERE IS_EXCLUDED::string ILIKE 'true'
GROUP BY 1
HAVING excl_npis >= 2 OR updated_after_ban = 1
ORDER BY excl_npis DESC;

-- Q15: LEIE: the 17 NPIs banned in 2026 and still in the June 2026 Medicare enrollment file
WITH p AS (
  SELECT NPI, MAX(UPPER(LAST_NAME)) ln, MAX(ORG_NAME) org, LISTAGG(DISTINCT PROVIDER_TYPE_DESC, '; ') ptype, LISTAGG(DISTINCT STATE_CD, ',') sts,
         MAX(TRY_TO_DATE(SUBSTR(ENRLMT_ID,2,8),'YYYYMMDD')) newest_enrl
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PECOS_PROVIDER_ENROLLMENT GROUP BY NPI
)
SELECT l.NPI, l.FIRST_NAME, l.LAST_NAME, l.BUSINESS_NAME, l.STATE, l.EXCLUSION_DATE, l.EXCLUSION_TYPE, l.SPECIALTY, l.HAS_WAIVER::string waiver,
       p.ln pecos_last, LEFT(p.org,40) pecos_org, LEFT(p.ptype,60) ptype, p.sts, p.newest_enrl,
       DATEDIFF('day', l.EXCLUSION_DATE, '2026-06-29'::date) days_banned_before_file
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE l JOIN p ON p.NPI = l.NPI
WHERE l.NPI_IS_REAL::string ILIKE 'true'
ORDER BY l.EXCLUSION_DATE;

-- Q16: LEIE no-NPI rows -> PECOS by name + state, enrollment ID dated after the ban; middle initial (people) as second field
WITH l AS (
  SELECT EXCLUSION_SK, IFF(IS_ENTITY_NOT_INDIVIDUAL::string ILIKE 'true','entity','person') kind,
         UPPER(TRIM(FIRST_NAME)) fn, UPPER(TRIM(LAST_NAME)) ln, LEFT(UPPER(TRIM(MIDDLE_NAME)),1) mi,
         REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(' '||REGEXP_REPLACE(UPPER(BUSINESS_NAME),'[^A-Z0-9 ]',' ')||' ',
           ' (LLC|INC|CORP|CORPORATION|CO|LTD|PC|PA|PLLC|THE|LLP|INCORPORATED|COMPANY) ',' '),
           ' (LLC|INC|CORP|CORPORATION|CO|LTD|PC|PA|PLLC|THE|LLP|INCORPORATED|COMPANY) ',' '),'[^A-Z0-9]','') bk,
         BUSINESS_NAME, FIRST_NAME, LAST_NAME, MIDDLE_NAME, STATE, CITY, EXCLUSION_DATE, EXCLUSION_TYPE, SPECIALTY, GENERAL_CATEGORY
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE
  WHERE NOT (NPI_IS_REAL::string ILIKE 'true')
), p AS (
  SELECT NPI, STATE_CD, UPPER(TRIM(FIRST_NAME)) fn, UPPER(TRIM(LAST_NAME)) ln, LEFT(UPPER(TRIM(MDL_NAME)),1) mi, ORG_NAME,
         REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(' '||REGEXP_REPLACE(UPPER(ORG_NAME),'[^A-Z0-9 ]',' ')||' ',
           ' (LLC|INC|CORP|CORPORATION|CO|LTD|PC|PA|PLLC|THE|LLP|INCORPORATED|COMPANY) ',' '),
           ' (LLC|INC|CORP|CORPORATION|CO|LTD|PC|PA|PLLC|THE|LLP|INCORPORATED|COMPANY) ',' '),'[^A-Z0-9]','') bk,
         PROVIDER_TYPE_DESC, TRY_TO_DATE(SUBSTR(ENRLMT_ID,2,8),'YYYYMMDD') enrl_date
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PECOS_PROVIDER_ENROLLMENT
), m AS (
  SELECT l.*, p.NPI pnpi, p.ORG_NAME, p.mi pmi, p.PROVIDER_TYPE_DESC, p.enrl_date
  FROM l JOIN p ON p.STATE_CD = l.STATE AND (
       (l.kind = 'entity' AND LENGTH(l.bk) >= 6 AND p.bk = l.bk)
    OR (l.kind = 'person' AND p.fn = l.fn AND p.ln = l.ln AND p.fn <> '' AND p.ln <> ''))
)
SELECT kind,
       (SELECT COUNT(*) FROM l l2 WHERE l2.kind = m.kind) leie_rows,
       COUNT(DISTINCT EXCLUSION_SK) matched_any_date,
       COUNT(DISTINCT IFF(enrl_date > EXCLUSION_DATE, EXCLUSION_SK, NULL)) enrolled_after_ban,
       COUNT(DISTINCT IFF(enrl_date > EXCLUSION_DATE AND mi <> '' AND pmi <> '' AND mi = pmi, EXCLUSION_SK, NULL)) after_ban_mi_agree,
       COUNT(DISTINCT IFF(enrl_date > EXCLUSION_DATE AND mi <> '' AND pmi <> '' AND mi <> pmi, EXCLUSION_SK, NULL)) after_ban_mi_conflict,
       COUNT(DISTINCT IFF(enrl_date > EXCLUSION_DATE, pnpi, NULL)) pecos_npis_after_ban
FROM m GROUP BY kind;

-- Q16 FAILED: 000630 (57014): Statement reached its statement or warehouse timeout of 300 second(s) and was canceled.

-- Q17: FHFA suspended people and companies -> PPP loans by exact name + state; city and date as second fields
WITH st AS (SELECT DISTINCT PRIMARY_STATE_NAME nm, PRIMARY_STATE_ABBREVIATION ab FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_SHORTAGE_AREAS),
f AS (
  SELECT h.FIRST_NAME, h.LAST_NAME, h.COMPANY, UPPER(TRIM(h.CITY)) city, st.ab, h.EFFECTIVE_DATE eff,
         REGEXP_REPLACE(UPPER(SPLIT_PART(TRIM(h.FIRST_NAME),' ',1)),'[^A-Z]','') fn,
         TRIM(REGEXP_REPLACE(REGEXP_REPLACE(UPPER(TRIM(h.FIRST_NAME)),'[^A-Z ]',''),' +',' ')) ffull,
         TRIM(REGEXP_REPLACE(REGEXP_REPLACE(UPPER(TRIM(h.LAST_NAME)),'[^A-Z ]',''),' +',' ')) ln,
         TRIM(REGEXP_REPLACE(REGEXP_REPLACE(UPPER(TRIM(h.COMPANY)),'[^A-Z0-9 ]',''),' +',' ')) co
  FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_FHFA_SUSPENDED_COUNTERPARTY h LEFT JOIN st ON st.nm = h.STATE
), k AS (
  SELECT fn||' '||ln key, 'person' kind, f.* FROM f WHERE ln <> '' AND fn <> ''
  UNION SELECT ffull||' '||ln, 'person', f.* FROM f WHERE ln <> '' AND ffull <> fn
  UNION SELECT co, 'company', f.* FROM f WHERE co <> ''
), p AS (
  SELECT TRIM(REGEXP_REPLACE(REGEXP_REPLACE(UPPER(BORROWER_NAME),'[^A-Z0-9 ]',''),' +',' ')) key, BORROWER_NAME,
         BORROWER_STATE, UPPER(TRIM(BORROWER_CITY)) bcity, DATE_APPROVED, CURRENT_APPROVAL_AMOUNT amt, NAICS_CODE, JOBS_REPORTED, LOAN_NUMBER
  FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_SBA_PPP
  WHERE BORROWER_STATE IN (SELECT ab FROM f)
)
SELECT k.kind, k.FIRST_NAME, k.LAST_NAME, k.COMPANY, k.city, k.ab, k.eff, p.BORROWER_NAME, p.bcity, p.DATE_APPROVED, p.amt, p.NAICS_CODE, p.JOBS_REPORTED,
       IFF(p.bcity = k.city, 'Y', 'N') city_agrees, IFF(p.DATE_APPROVED > k.eff, 'after', 'before') loan_vs_suspension
FROM k JOIN p ON p.key = k.key AND p.BORROWER_STATE = k.ab
ORDER BY city_agrees DESC, loan_vs_suspension, p.amt DESC;

-- Q18: CDC injury file: shape of the all-suicide rows (GEOID length x PERIOD), to line up years with the VA file
SELECT LENGTH(GEOID::string) geoid_len, PERIOD, COUNT(*) row_ct, COUNT(COUNT_SUP) counted, SUM(COUNT_SUP) deaths,
       SUM(IFF(RATE < 0, 1, 0)) rate_sentinel, MIN(GEOID::string) min_geoid, MAX(GEOID::string) max_geoid
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_INJURY_VIOLENCE_COUNTY
WHERE INTENT = 'All_Suicide'
GROUP BY 1,2 ORDER BY 1,2;

-- Q19: LEIE no-NPI rows -> PECOS by name + state (entity: cleaned business name; person: first+last), enrollment ID dated after the ban; totals + detail
WITH l AS (
  SELECT EXCLUSION_SK, IFF(IS_ENTITY_NOT_INDIVIDUAL::string ILIKE 'true','entity','person') kind,
         UPPER(TRIM(FIRST_NAME)) fn, UPPER(TRIM(LAST_NAME)) ln, LEFT(UPPER(TRIM(MIDDLE_NAME)),1) mi,
         REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(' '||REGEXP_REPLACE(UPPER(BUSINESS_NAME),'[^A-Z0-9 ]',' ')||' ',
           ' (LLC|INC|CORP|CORPORATION|CO|LTD|PC|PA|PLLC|THE|LLP|INCORPORATED|COMPANY) ',' '),
           ' (LLC|INC|CORP|CORPORATION|CO|LTD|PC|PA|PLLC|THE|LLP|INCORPORATED|COMPANY) ',' '),'[^A-Z0-9]','') bk,
         BUSINESS_NAME, FIRST_NAME, LAST_NAME, MIDDLE_NAME, STATE, CITY, EXCLUSION_DATE, EXCLUSION_TYPE, SPECIALTY
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE
  WHERE NOT (NPI_IS_REAL::string ILIKE 'true')
), p AS (
  SELECT NPI, STATE_CD, UPPER(TRIM(FIRST_NAME)) fn, UPPER(TRIM(LAST_NAME)) ln, LEFT(UPPER(TRIM(MDL_NAME)),1) mi, ORG_NAME,
         REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(' '||REGEXP_REPLACE(UPPER(ORG_NAME),'[^A-Z0-9 ]',' ')||' ',
           ' (LLC|INC|CORP|CORPORATION|CO|LTD|PC|PA|PLLC|THE|LLP|INCORPORATED|COMPANY) ',' '),
           ' (LLC|INC|CORP|CORPORATION|CO|LTD|PC|PA|PLLC|THE|LLP|INCORPORATED|COMPANY) ',' '),'[^A-Z0-9]','') bk,
         PROVIDER_TYPE_DESC, TRY_TO_DATE(SUBSTR(ENRLMT_ID,2,8),'YYYYMMDD') enrl_date
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PECOS_PROVIDER_ENROLLMENT
), me AS (
  SELECT l.*, p.NPI pnpi, p.ORG_NAME porg, p.fn pfn, p.ln pln, p.mi pmi, p.PROVIDER_TYPE_DESC ptype, p.enrl_date
  FROM l JOIN p ON p.STATE_CD = l.STATE AND p.bk = l.bk
  WHERE l.kind = 'entity' AND LENGTH(l.bk) >= 6 AND p.ORG_NAME IS NOT NULL
), mp AS (
  SELECT l.*, p.NPI pnpi, p.ORG_NAME porg, p.fn pfn, p.ln pln, p.mi pmi, p.PROVIDER_TYPE_DESC ptype, p.enrl_date
  FROM l JOIN p ON p.STATE_CD = l.STATE AND p.fn = l.fn AND p.ln = l.ln
  WHERE l.kind = 'person' AND l.fn <> '' AND l.ln <> ''
), m AS (SELECT * FROM me UNION ALL SELECT * FROM mp),
agg AS (
  SELECT kind, COUNT(DISTINCT EXCLUSION_SK) matched_any,
         COUNT(DISTINCT IFF(enrl_date > EXCLUSION_DATE, EXCLUSION_SK, NULL)) after_ban,
         COUNT(DISTINCT IFF(enrl_date > EXCLUSION_DATE AND mi <> '' AND pmi <> '' AND mi = pmi, EXCLUSION_SK, NULL)) after_ban_mi_agree,
         COUNT(DISTINCT IFF(enrl_date > EXCLUSION_DATE AND mi <> '' AND pmi <> '' AND mi <> pmi, EXCLUSION_SK, NULL)) after_ban_mi_conflict
  FROM m GROUP BY kind
), lr AS (SELECT kind, COUNT(*) leie_rows FROM l GROUP BY kind),
d AS (
  SELECT kind, COALESCE(BUSINESS_NAME, FIRST_NAME||' '||COALESCE(MIDDLE_NAME,'')||' '||LAST_NAME) leie_name, STATE, CITY, EXCLUSION_DATE, EXCLUSION_TYPE, SPECIALTY,
         pnpi, COALESCE(porg, pfn||' '||COALESCE(pmi,'')||' '||pln) pecos_name, ptype, enrl_date
  FROM m WHERE enrl_date > EXCLUSION_DATE AND (kind = 'entity' OR (mi <> '' AND pmi <> '' AND mi = pmi))
)
SELECT lr.kind, lr.leie_rows, agg.matched_any, agg.after_ban, agg.after_ban_mi_agree, agg.after_ban_mi_conflict,
       d.leie_name, d.STATE, d.CITY, d.EXCLUSION_DATE, d.EXCLUSION_TYPE, LEFT(d.SPECIALTY,20) spec, d.pnpi, LEFT(d.pecos_name,40) pecos_name, LEFT(d.ptype,45) ptype, d.enrl_date
FROM lr LEFT JOIN agg ON agg.kind = lr.kind LEFT JOIN d ON d.kind = lr.kind
ORDER BY lr.kind, d.enrl_date DESC NULLS LAST
LIMIT 120;

-- Q20: FHFA suspended people -> PPP loans, looser: borrower name first token = first name, last token = last name, same state; companies by first 12 cleaned chars; plus PPP row count
WITH st AS (SELECT DISTINCT PRIMARY_STATE_NAME nm, PRIMARY_STATE_ABBREVIATION ab FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_SHORTAGE_AREAS),
f AS (
  SELECT h.FIRST_NAME, h.LAST_NAME, h.COMPANY, UPPER(TRIM(h.CITY)) city, st.ab, h.EFFECTIVE_DATE eff,
         REGEXP_REPLACE(UPPER(SPLIT_PART(TRIM(h.FIRST_NAME),' ',1)),'[^A-Z]','') fn,
         REGEXP_SUBSTR(REGEXP_REPLACE(UPPER(TRIM(h.LAST_NAME)),'[^A-Z ]',''),'[A-Z]+$') lt,
         LEFT(REGEXP_REPLACE(UPPER(h.COMPANY),'[^A-Z0-9]',''),12) co12
  FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_FHFA_SUSPENDED_COUNTERPARTY h LEFT JOIN st ON st.nm = h.STATE
), p AS (
  SELECT BORROWER_NAME, BORROWER_STATE, UPPER(TRIM(BORROWER_CITY)) bcity, DATE_APPROVED, CURRENT_APPROVAL_AMOUNT amt, NAICS_CODE,
         SPLIT_PART(TRIM(REGEXP_REPLACE(UPPER(BORROWER_NAME),'[^A-Z ]','')),' ',1) ft,
         REGEXP_SUBSTR(TRIM(REGEXP_REPLACE(UPPER(BORROWER_NAME),'[^A-Z ]','')),'[A-Z]+$') lt,
         LEFT(REGEXP_REPLACE(UPPER(BORROWER_NAME),'[^A-Z0-9]',''),12) co12
  FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_SBA_PPP
  WHERE BORROWER_STATE IN (SELECT ab FROM f)
), hits AS (
  SELECT 'person' kind, f.FIRST_NAME, f.LAST_NAME, f.COMPANY, f.city, f.ab, f.eff, p.BORROWER_NAME, p.bcity, p.DATE_APPROVED, p.amt, p.NAICS_CODE
  FROM f JOIN p ON p.BORROWER_STATE = f.ab AND p.ft = f.fn AND p.lt = f.lt WHERE f.fn <> '' AND f.lt <> ''
  UNION ALL
  SELECT 'company', f.FIRST_NAME, f.LAST_NAME, f.COMPANY, f.city, f.ab, f.eff, p.BORROWER_NAME, p.bcity, p.DATE_APPROVED, p.amt, p.NAICS_CODE
  FROM f JOIN p ON p.BORROWER_STATE = f.ab AND p.co12 = f.co12 WHERE LENGTH(f.co12) >= 8
)
SELECT (SELECT COUNT(*) FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_SBA_PPP) ppp_rows,
       (SELECT COUNT(*) FROM p) ppp_rows_in_fhfa_states,
       COUNT(*) OVER () hit_rows, SUM(IFF(bcity = city, 1, 0)) OVER () city_agree_rows,
       kind, FIRST_NAME, LAST_NAME, COMPANY, city, ab, eff, BORROWER_NAME, bcity, DATE_APPROVED, amt, NAICS_CODE,
       IFF(bcity = city,'Y','N') city_agrees, IFF(DATE_APPROVED > eff,'after','before') loan_vs_susp
FROM hits ORDER BY city_agrees DESC, amt DESC LIMIT 60;

-- Q21: FHFA suspended people -> FDIC enforcement orders where the respondent text holds both first and last name
WITH st AS (SELECT DISTINCT PRIMARY_STATE_NAME nm, PRIMARY_STATE_ABBREVIATION ab FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_SHORTAGE_AREAS),
f AS (
  SELECT h.FIRST_NAME, h.LAST_NAME, st.ab, h.EFFECTIVE_DATE eff,
         REGEXP_REPLACE(UPPER(SPLIT_PART(TRIM(h.FIRST_NAME),' ',1)),'[^A-Z]','') fn,
         TRIM(REGEXP_REPLACE(UPPER(TRIM(h.LAST_NAME)),'[^A-Z ]','')) ln
  FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_FHFA_SUSPENDED_COUNTERPARTY h LEFT JOIN st ON st.nm = h.STATE
  WHERE COALESCE(TRIM(h.LAST_NAME),'') <> ''
), o AS (
  SELECT ORDER_ID, ORDER_DATE, ORDER_TYPE, UPPER(RESPONDENTS) r, STATE, BANK_STATE, BANK_NAME, NMLS_IDS
  FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FDIC_ENFORCEMENT_ORDERS WHERE RESPONDENTS IS NOT NULL
)
SELECT (SELECT COUNT(*) FROM o) fdic_orders_with_respondent, f.FIRST_NAME, f.LAST_NAME, f.ab, f.eff, o.ORDER_DATE, LEFT(o.ORDER_TYPE,40) otype,
       LEFT(o.r,70) respondents, o.STATE, o.BANK_STATE, LEFT(o.BANK_NAME,30) bank, o.NMLS_IDS
FROM f JOIN o ON CONTAINS(' '||REGEXP_REPLACE(o.r,'[^A-Z]',' ')||' ', ' '||f.ln||' ') AND CONTAINS(' '||REGEXP_REPLACE(o.r,'[^A-Z]',' ')||' ', ' '||f.fn||' ')
ORDER BY f.LAST_NAME LIMIT 60;

-- Q22: LEIE name matches enrolled after the ban: second fields. Entities: NPPES practice city vs LEIE city. People: middle initial AND specialty agree, then NPPES city
WITH l AS (
  SELECT EXCLUSION_SK, IFF(IS_ENTITY_NOT_INDIVIDUAL::string ILIKE 'true','entity','person') kind,
         UPPER(TRIM(FIRST_NAME)) fn, UPPER(TRIM(LAST_NAME)) ln, LEFT(UPPER(TRIM(MIDDLE_NAME)),1) mi,
         REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(' '||REGEXP_REPLACE(UPPER(BUSINESS_NAME),'[^A-Z0-9 ]',' ')||' ',
           ' (LLC|INC|CORP|CORPORATION|CO|LTD|PC|PA|PLLC|THE|LLP|INCORPORATED|COMPANY) ',' '),
           ' (LLC|INC|CORP|CORPORATION|CO|LTD|PC|PA|PLLC|THE|LLP|INCORPORATED|COMPANY) ',' '),'[^A-Z0-9]','') bk,
         IFF(SPECIALTY ILIKE '%AIDE%' OR SPECIALTY ILIKE '%TECHNICIAN%', NULL, UPPER(SPLIT_PART(TRIM(SPECIALTY),' ',1))) spec1,
         BUSINESS_NAME, FIRST_NAME, LAST_NAME, MIDDLE_NAME, STATE, UPPER(TRIM(CITY)) city, EXCLUSION_DATE, EXCLUSION_TYPE, SPECIALTY
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE
  WHERE NOT (NPI_IS_REAL::string ILIKE 'true')
), p AS (
  SELECT NPI, STATE_CD, UPPER(TRIM(FIRST_NAME)) fn, UPPER(TRIM(LAST_NAME)) ln, LEFT(UPPER(TRIM(MDL_NAME)),1) mi, ORG_NAME,
         REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(' '||REGEXP_REPLACE(UPPER(ORG_NAME),'[^A-Z0-9 ]',' ')||' ',
           ' (LLC|INC|CORP|CORPORATION|CO|LTD|PC|PA|PLLC|THE|LLP|INCORPORATED|COMPANY) ',' '),
           ' (LLC|INC|CORP|CORPORATION|CO|LTD|PC|PA|PLLC|THE|LLP|INCORPORATED|COMPANY) ',' '),'[^A-Z0-9]','') bk,
         PROVIDER_TYPE_DESC, TRY_TO_DATE(SUBSTR(ENRLMT_ID,2,8),'YYYYMMDD') enrl_date
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PECOS_PROVIDER_ENROLLMENT
), me AS (
  SELECT l.*, p.NPI pnpi, p.ORG_NAME porg, p.fn pfn, p.ln pln, p.mi pmi, p.PROVIDER_TYPE_DESC ptype, p.enrl_date
  FROM l JOIN p ON p.STATE_CD = l.STATE AND p.bk = l.bk
  WHERE l.kind = 'entity' AND LENGTH(l.bk) >= 6 AND p.ORG_NAME IS NOT NULL
), mp AS (
  SELECT l.*, p.NPI pnpi, p.ORG_NAME porg, p.fn pfn, p.ln pln, p.mi pmi, p.PROVIDER_TYPE_DESC ptype, p.enrl_date
  FROM l JOIN p ON p.STATE_CD = l.STATE AND p.fn = l.fn AND p.ln = l.ln
  WHERE l.kind = 'person' AND l.fn <> '' AND l.ln <> ''
), cand AS (
  SELECT * FROM me WHERE enrl_date > EXCLUSION_DATE
  UNION ALL
  SELECT * FROM mp WHERE enrl_date > EXCLUSION_DATE AND mi <> '' AND mi = pmi
     AND LENGTH(spec1) >= 5 AND CONTAINS(UPPER(ptype), spec1)
), n AS (
  SELECT NPI, UPPER(TRIM(PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_CITY_NAME)) ncity,
         PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_STATE_NAME nst, PROVIDER_ENUMERATION_DATE enum_date,
         AUTHORIZED_OFFICIAL_LAST_NAME ao_last
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES WHERE NPI IN (SELECT pnpi FROM cand)
)
SELECT kind, COALESCE(BUSINESS_NAME, FIRST_NAME||' '||COALESCE(MIDDLE_NAME,'')||' '||LAST_NAME) leie_name, STATE, city leie_city,
       EXCLUSION_DATE, EXCLUSION_TYPE, LEFT(SPECIALTY,20) spec, pnpi, LEFT(COALESCE(porg, pfn||' '||pmi||' '||pln),35) pecos_name,
       LEFT(ptype,40) ptype, enrl_date, n.ncity, n.nst, n.enum_date, n.ao_last, IFF(n.ncity = city,'Y','N') city_agrees
FROM cand LEFT JOIN n ON n.NPI = cand.pnpi
ORDER BY kind, city_agrees DESC, enrl_date DESC;

-- Q23: VA vs general population, fixed county panel: CDC all-suicide 2019-20 vs 2022-23 in counties counted all four years, summed to state; national row added
WITH c AS (
  SELECT GEOID::string g, ST_NAME st, PERIOD, COUNT_SUP cnt, COUNT_SUP / NULLIF(RATE,0) * 1e5 pop
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_INJURY_VIOLENCE_COUNTY
  WHERE INTENT = 'All_Suicide' AND PERIOD IN ('2019','2020','2022','2023') AND COUNT_SUP IS NOT NULL AND RATE > 0
), panel AS (SELECT g FROM c GROUP BY g HAVING COUNT(DISTINCT PERIOD) = 4),
gs AS (
  SELECT st, COUNT(DISTINCT c.g) panel_counties,
         SUM(IFF(PERIOD IN ('2019','2020'), cnt, 0)) ce, SUM(IFF(PERIOD IN ('2019','2020'), pop, 0)) pe,
         SUM(IFF(PERIOD IN ('2022','2023'), cnt, 0)) cl, SUM(IFF(PERIOD IN ('2022','2023'), pop, 0)) pl
  FROM c JOIN panel USING (g) GROUP BY st
), gn AS (
  SELECT * FROM gs
  UNION ALL SELECT 'U.S. Total', SUM(panel_counties), SUM(ce), SUM(pe), SUM(cl), SUM(pl) FROM gs
), v AS (
  SELECT STATE st, GEOGRAPHIC_REGION region,
         SUM(IFF(YEAR_OF_DEATH IN (2019,2020), TRY_TO_NUMBER(VETERAN_SUICIDES::string), 0)) de,
         SUM(IFF(YEAR_OF_DEATH IN (2019,2020), TRY_TO_NUMBER(VETERAN_POPULATION_ESTIMATE::string), 0)) pe,
         SUM(IFF(YEAR_OF_DEATH IN (2022,2023), TRY_TO_NUMBER(VETERAN_SUICIDES::string), 0)) dl,
         SUM(IFF(YEAR_OF_DEATH IN (2022,2023), TRY_TO_NUMBER(VETERAN_POPULATION_ESTIMATE::string), 0)) pl
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_VA_SUICIDE_STATE GROUP BY 1,2
)
SELECT v.st, v.region, v.de vet_d_1920, v.dl vet_d_2223,
       ROUND(1e5*v.de/NULLIF(v.pe,0),1) vet_r_1920, ROUND(1e5*v.dl/NULLIF(v.pl,0),1) vet_r_2223,
       ROUND((v.dl/NULLIF(v.pl,0))/NULLIF(v.de/NULLIF(v.pe,0),0),2) vet_ratio,
       gn.panel_counties, gn.ce gen_d_1920, gn.cl gen_d_2223,
       ROUND(1e5*gn.ce/NULLIF(gn.pe,0),1) gen_r_1920, ROUND(1e5*gn.cl/NULLIF(gn.pl,0),1) gen_r_2223,
       ROUND((gn.cl/NULLIF(gn.pl,0))/NULLIF(gn.ce/NULLIF(gn.pe,0),0),2) gen_ratio,
       ROUND(vet_ratio/NULLIF(gen_ratio,0),2) vet_vs_gen
FROM v LEFT JOIN gn ON UPPER(gn.st) = UPPER(v.st)
ORDER BY vet_vs_gen DESC NULLS LAST;

-- Q24: HRSA x overdose: whole counties inside a designated geographic/high-needs HPSA scoring 18+ vs other counties in the same state; CDC overdose 2019-24, counties counted all six years
WITH sev AS (
  SELECT DISTINCT HPSA_DISCIPLINE_CLASS disc, LPAD(COMMON_STATE_COUNTY_FIPS_CODE::string,5,'0') g,
         MIN(TRY_TO_DATE(HPSA_DESIGNATION_DATE,'MM/DD/YYYY')) OVER (PARTITION BY HPSA_DISCIPLINE_CLASS, COMMON_STATE_COUNTY_FIPS_CODE) first_d
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_SHORTAGE_AREAS
  WHERE HPSA_STATUS = 'Designated' AND DESIGNATION_TYPE IN ('Geographic HPSA','High Needs Geographic HPSA')
    AND HPSA_DISCIPLINE_CLASS IN ('Primary Care','Mental Health') AND HPSA_COMPONENT_TYPE_CODE = 'SCTY'
    AND TRY_TO_NUMBER(HPSA_SCORE::string) >= 18
), od AS (
  SELECT GEOID::string g, ST_NAME st, SUM(COUNT_SUP) d, SUM(COUNT_SUP / NULLIF(RATE,0) * 1e5) pop
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_INJURY_VIOLENCE_COUNTY
  WHERE INTENT = 'Drug_OD' AND PERIOD IN ('2019','2020','2021','2022','2023','2024') AND COUNT_SUP IS NOT NULL AND RATE > 0
  GROUP BY 1,2 HAVING COUNT(DISTINCT PERIOD) = 6
), dd AS (SELECT 'Primary Care' disc UNION ALL SELECT 'Mental Health'),
x AS (
  SELECT dd.disc, od.st, IFF(sev.g IS NOT NULL, 'severe', 'other') grp, IFF(sev.first_d < '2000-01-01', 1, 0) old,
         od.d, od.pop
  FROM od CROSS JOIN dd LEFT JOIN sev ON sev.g = od.g AND sev.disc = dd.disc
), s AS (
  SELECT disc, st,
         SUM(IFF(grp='severe', d, 0)) / NULLIF(SUM(IFF(grp='severe', pop, 0)),0) * 1e5 r_sev,
         SUM(IFF(grp='other', d, 0)) / NULLIF(SUM(IFF(grp='other', pop, 0)),0) * 1e5 r_oth,
         COUNT_IF(grp='severe') n_sev, COUNT_IF(grp='other') n_oth, COUNT_IF(grp='severe' AND old = 1) n_sev_pre2000
  FROM x GROUP BY 1,2
)
SELECT disc, COUNT(*) states, COUNT_IF(n_sev > 0 AND n_oth > 0) states_both, SUM(n_sev) sev_counties, SUM(n_sev_pre2000) sev_pre2000, SUM(n_oth) other_counties,
       COUNT_IF(n_sev > 0 AND n_oth > 0 AND r_sev > r_oth) states_sev_higher,
       ROUND(MEDIAN(IFF(n_sev > 0 AND n_oth > 0, r_sev / NULLIF(r_oth,0), NULL)),2) median_ratio_sev_to_other,
       LISTAGG(IFF(n_sev > 0 AND n_oth > 0, st || ' ' || ROUND(r_sev,0) || '/' || ROUND(r_oth,0) || ' (' || n_sev || ')', NULL), '; ') by_state
FROM s GROUP BY disc;

-- Q25: PPP table shape: is it the full loan file or only $150K+ loans?
SELECT COUNT(*) row_ct, MIN(CURRENT_APPROVAL_AMOUNT) min_amt, MIN(INITIAL_APPROVAL_AMOUNT) min_init,
       COUNT_IF(CURRENT_APPROVAL_AMOUNT < 150000) under_150k, COUNT_IF(INITIAL_APPROVAL_AMOUNT < 150000) init_under_150k,
       MIN(DATE_APPROVED) first_approved, MAX(DATE_APPROVED) last_approved, COUNT(DISTINCT BORROWER_STATE) states
FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_SBA_PPP;

-- Q26: FHFA suspensions by year: people vs companies, and how many already carry a same-state SAM exclusion or an FDIC order naming them
WITH st AS (SELECT DISTINCT PRIMARY_STATE_NAME nm, PRIMARY_STATE_ABBREVIATION ab FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_SHORTAGE_AREAS),
f AS (
  SELECT h.FIRST_NAME, h.LAST_NAME, h.COMPANY, h.STATE, st.ab, h.EFFECTIVE_DATE eff, h.SUSPENSION_END_DATE,
         REGEXP_REPLACE(UPPER(SPLIT_PART(TRIM(h.FIRST_NAME),' ',1)),'[^A-Z]','') fn,
         TRIM(REGEXP_REPLACE(UPPER(TRIM(h.LAST_NAME)),'[^A-Z ]','')) ln
  FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_FHFA_SUSPENDED_COUNTERPARTY h LEFT JOIN st ON st.nm = h.STATE
), samk AS (
  SELECT DISTINCT UPPER(TRIM(FIRST_NAME)) fn, UPPER(TRIM(LAST_NAME)) ln, UPPER(TRIM(STATE)) st
  FROM LIBRARY_MARTS.PROCUREMENT.PROCUREMENT__FED_SAM_EXCLUSIONS WHERE LAST_NAME IS NOT NULL
), o AS (
  SELECT ' '||REGEXP_REPLACE(UPPER(RESPONDENTS),'[^A-Z]',' ')||' ' r FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FDIC_ENFORCEMENT_ORDERS WHERE RESPONDENTS IS NOT NULL
), fk AS (
  SELECT DISTINCT f.fn, f.ln FROM f JOIN o ON CONTAINS(o.r, ' '||f.ln||' ') AND CONTAINS(o.r, ' '||f.fn||' ') WHERE f.ln <> '' AND f.fn <> ''
), j AS (
  SELECT f.*, IFF(s.fn IS NOT NULL, 1, 0) sam_hit, IFF(k.fn IS NOT NULL, 1, 0) fdic_hit
  FROM f LEFT JOIN samk s ON s.fn = f.fn AND s.ln = f.ln AND s.st = f.ab
         LEFT JOIN fk k ON k.fn = f.fn AND k.ln = f.ln
)
SELECT YEAR(eff) yr, COUNT(*) rows_all, COUNT_IF(COALESCE(TRIM(LAST_NAME),'') = '') companies,
       COUNT_IF(sam_hit = 1) sam_same_state, COUNT_IF(fdic_hit = 1) fdic_named, COUNT_IF(sam_hit = 1 OR fdic_hit = 1) either,
       COUNT_IF(SUSPENSION_END_DATE IS NOT NULL) has_end_date,
       LISTAGG(DISTINCT ab, ',') WITHIN GROUP (ORDER BY ab) states
FROM j GROUP BY 1 ORDER BY 1;

-- Q27: VA year by year 2013-2023 for Oklahoma, Kansas, Montana, Utah and the nation, plus CDC Oklahoma all-suicide (counted counties) for the general-population line
SELECT 'VA' src, STATE, YEAR_OF_DEATH yr, TRY_TO_NUMBER(VETERAN_SUICIDES::string) deaths, TRY_TO_NUMBER(VETERAN_POPULATION_ESTIMATE::string) pop,
       TRY_TO_DOUBLE(VETERAN_SUICIDE_RATE_PER_100K::string) rate
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_VA_SUICIDE_STATE
WHERE STATE IN ('Oklahoma','Kansas','Montana','Utah','U.S. Total') AND YEAR_OF_DEATH >= 2013
UNION ALL
SELECT 'CDC counted counties', ST_NAME, TRY_TO_NUMBER(PERIOD), SUM(COUNT_SUP), ROUND(SUM(COUNT_SUP / NULLIF(RATE,0) * 1e5)),
       ROUND(1e5 * SUM(COUNT_SUP) / NULLIF(SUM(COUNT_SUP / NULLIF(RATE,0) * 1e5),0),1)
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_INJURY_VIOLENCE_COUNTY
WHERE INTENT = 'All_Suicide' AND ST_NAME IN ('Oklahoma','Kansas') AND PERIOD <> 'TTM' AND COUNT_SUP IS NOT NULL AND RATE > 0
GROUP BY 2,3
ORDER BY 1 DESC, 2, 3;

-- Q28: LEIE name-match candidates: did any bill Medicare Part B (2024 provider file)?
SELECT RNDRNG_NPI, RNDRNG_PRVDR_FIRST_NAME, RNDRNG_PRVDR_LAST_ORG_NAME, RNDRNG_PRVDR_CITY, RNDRNG_PRVDR_STATE_ABRVTN,
       TOT_BENES, TOT_SRVCS, TOT_MDCR_ALOWD_AMT, TOT_MDCR_PYMT_AMT
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER
WHERE RNDRNG_NPI::string IN ('1053350538','1942889399','1821218074','1093142648','1396817995','1205983715','1033179908',
                             '1669216719','1548535925','1437586294','1558763565','1124622618');

-- Q29: LEIE people -> NPPES organizations where a same-name person (first+last+state) is the authorized official; second fields: practice city, middle initial, org NPI created after the ban, org enrolled in Medicare
WITH l AS (
  SELECT EXCLUSION_SK, UPPER(TRIM(FIRST_NAME)) fn, UPPER(TRIM(LAST_NAME)) ln, LEFT(UPPER(TRIM(MIDDLE_NAME)),1) mi,
         STATE, UPPER(TRIM(CITY)) city, EXCLUSION_DATE, EXCLUSION_TYPE, GENERAL_CATEGORY, SPECIALTY,
         FIRST_NAME||' '||COALESCE(MIDDLE_NAME,'')||' '||LAST_NAME nm
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE
  WHERE NOT (IS_ENTITY_NOT_INDIVIDUAL::string ILIKE 'true') AND COALESCE(TRIM(LAST_NAME),'') <> '' AND COALESCE(TRIM(FIRST_NAME),'') <> ''
    AND COALESCE(HAS_WAIVER::string,'false') NOT ILIKE 'true'
), n AS (
  SELECT NPI, UPPER(TRIM(AUTHORIZED_OFFICIAL_FIRST_NAME)) fn, UPPER(TRIM(AUTHORIZED_OFFICIAL_LAST_NAME)) ln,
         LEFT(UPPER(TRIM(AUTHORIZED_OFFICIAL_MIDDLE_NAME)),1) mi, AUTHORIZED_OFFICIAL_TITLE_OR_POSITION title,
         PROVIDER_ORGANIZATION_NAME_LEGAL_BUSINESS_NAME org, UPPER(TRIM(PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_CITY_NAME)) city,
         PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_STATE_NAME st, TRY_TO_DATE(PROVIDER_ENUMERATION_DATE::string) enum_d,
         TRY_TO_DATE(LAST_UPDATE_DATE::string) upd, NPI_DEACTIVATION_DATE deact
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES
  WHERE ENTITY_TYPE_CODE::string = '2' AND AUTHORIZED_OFFICIAL_LAST_NAME IS NOT NULL
), pe AS (
  SELECT NPI, LISTAGG(DISTINCT PROVIDER_TYPE_DESC, '; ') ptype FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PECOS_PROVIDER_ENROLLMENT GROUP BY NPI
), m AS (
  SELECT l.*, n.NPI onpi, n.org, n.title, n.city ncity, n.mi nmi, n.enum_d, n.upd, n.deact, pe.ptype,
         IFF(n.city = l.city, 1, 0) city_ok, IFF(n.mi IS NOT NULL AND n.mi <> '' AND l.mi <> '' AND n.mi <> l.mi, 1, 0) mi_conflict
  FROM l JOIN n ON n.fn = l.fn AND n.ln = l.ln AND n.st = l.STATE
  LEFT JOIN pe ON pe.NPI = n.NPI
), agg AS (
  SELECT (SELECT COUNT(DISTINCT EXCLUSION_SK) FROM l) leie_people,
         COUNT(DISTINCT EXCLUSION_SK) people_matched, COUNT(DISTINCT onpi) orgs_matched,
         COUNT(DISTINCT IFF(city_ok = 1 AND mi_conflict = 0, EXCLUSION_SK, NULL)) people_city_ok,
         COUNT(DISTINCT IFF(city_ok = 1 AND mi_conflict = 0 AND enum_d > EXCLUSION_DATE, EXCLUSION_SK, NULL)) people_city_ok_org_after_ban,
         COUNT(DISTINCT IFF(city_ok = 1 AND mi_conflict = 0 AND enum_d > EXCLUSION_DATE AND ptype IS NOT NULL AND deact IS NULL, EXCLUSION_SK, NULL)) people_city_ok_after_ban_enrolled,
         COUNT(DISTINCT IFF(city_ok = 1 AND mi_conflict = 0 AND enum_d > EXCLUSION_DATE AND ptype IS NOT NULL AND deact IS NULL, onpi, NULL)) orgs_city_ok_after_ban_enrolled
  FROM m
)
SELECT agg.*, m.nm, m.STATE, m.city, m.EXCLUSION_DATE, m.EXCLUSION_TYPE, LEFT(m.GENERAL_CATEGORY,20) cat, LEFT(m.SPECIALTY,20) spec,
       m.onpi, LEFT(m.org,40) org, LEFT(m.title,20) title, m.nmi, m.enum_d, m.upd, LEFT(m.ptype,50) ptype
FROM agg LEFT JOIN m ON m.city_ok = 1 AND m.mi_conflict = 0 AND m.enum_d > m.EXCLUSION_DATE AND m.ptype IS NOT NULL AND m.deact IS NULL
ORDER BY m.enum_d DESC NULLS LAST
LIMIT 100;

-- Q30: Namesake test for the strongest name matches: every NPPES person or authorized official, and every LEIE row, carrying these names (looks for Sr/Jr pairs)
SELECT 'NPPES person' src, NPI::string id, PROVIDER_FIRST_NAME fn, PROVIDER_MIDDLE_NAME mn, PROVIDER_LAST_NAME_LEGAL_NAME ln, PROVIDER_NAME_SUFFIX_TEXT sfx,
       PROVIDER_CREDENTIAL_TEXT cred_or_title, HEALTHCARE_PROVIDER_TAXONOMY_CODE_1 tax_or_org,
       PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_CITY_NAME city, PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_STATE_NAME st,
       PROVIDER_ENUMERATION_DATE::string d1, NPI_DEACTIVATION_DATE::string d2
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES
WHERE ENTITY_TYPE_CODE::string = '1' AND (
      UPPER(PROVIDER_LAST_NAME_LEGAL_NAME) IN ('SZEKELY','BERNAUER')
   OR (UPPER(PROVIDER_LAST_NAME_LEGAL_NAME) = 'SANGHA' AND UPPER(PROVIDER_FIRST_NAME) = 'BHUPINDER')
   OR (UPPER(PROVIDER_LAST_NAME_LEGAL_NAME) = 'MOAYED' AND UPPER(PROVIDER_FIRST_NAME) = 'ALI')
   OR (UPPER(PROVIDER_LAST_NAME_LEGAL_NAME) = 'AWAN' AND UPPER(PROVIDER_FIRST_NAME) = 'ABDUL'))
UNION ALL
SELECT 'NPPES auth official', NPI::string, AUTHORIZED_OFFICIAL_FIRST_NAME, AUTHORIZED_OFFICIAL_MIDDLE_NAME, AUTHORIZED_OFFICIAL_LAST_NAME, AUTHORIZED_OFFICIAL_NAME_SUFFIX_TEXT,
       AUTHORIZED_OFFICIAL_TITLE_OR_POSITION, LEFT(PROVIDER_ORGANIZATION_NAME_LEGAL_BUSINESS_NAME,40),
       PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_CITY_NAME, PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_STATE_NAME,
       PROVIDER_ENUMERATION_DATE::string, NPI_DEACTIVATION_DATE::string
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES
WHERE ENTITY_TYPE_CODE::string = '2' AND (
      UPPER(AUTHORIZED_OFFICIAL_LAST_NAME) IN ('SZEKELY','BERNAUER')
   OR (UPPER(AUTHORIZED_OFFICIAL_LAST_NAME) = 'SANGHA' AND UPPER(AUTHORIZED_OFFICIAL_FIRST_NAME) = 'BHUPINDER')
   OR (UPPER(AUTHORIZED_OFFICIAL_LAST_NAME) = 'MOAYED' AND UPPER(AUTHORIZED_OFFICIAL_FIRST_NAME) = 'ALI')
   OR (UPPER(AUTHORIZED_OFFICIAL_LAST_NAME) = 'AWAN' AND UPPER(AUTHORIZED_OFFICIAL_FIRST_NAME) = 'ABDUL'))
UNION ALL
SELECT 'LEIE', COALESCE(NPI,''), FIRST_NAME, MIDDLE_NAME, LAST_NAME, '', EXCLUSION_TYPE, LEFT(GENERAL_CATEGORY||' / '||SPECIALTY,40), CITY, STATE,
       EXCLUSION_DATE::string, HAS_WAIVER::string
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE
WHERE UPPER(LAST_NAME) IN ('SZEKELY','BERNAUER')
   OR (UPPER(LAST_NAME) = 'SANGHA' AND UPPER(FIRST_NAME) = 'BHUPINDER')
   OR (UPPER(LAST_NAME) = 'MOAYED' AND UPPER(FIRST_NAME) = 'ALI')
   OR (UPPER(LAST_NAME) = 'AWAN' AND UPPER(FIRST_NAME) = 'ABDUL')
ORDER BY 5, 1, 2;

-- Q31: Medicare Part B 2024 money to the orgs whose authorized official matches a banned person (strict set: same first+last+state+city, no middle-initial conflict, org NPI created after the ban, enrolled, active)
WITH l AS (
  SELECT EXCLUSION_SK, UPPER(TRIM(FIRST_NAME)) fn, UPPER(TRIM(LAST_NAME)) ln, LEFT(UPPER(TRIM(MIDDLE_NAME)),1) mi,
         STATE, UPPER(TRIM(CITY)) city, EXCLUSION_DATE, EXCLUSION_TYPE, FIRST_NAME||' '||COALESCE(MIDDLE_NAME,'')||' '||LAST_NAME nm
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE
  WHERE NOT (IS_ENTITY_NOT_INDIVIDUAL::string ILIKE 'true') AND COALESCE(TRIM(LAST_NAME),'') <> '' AND COALESCE(TRIM(FIRST_NAME),'') <> ''
    AND COALESCE(HAS_WAIVER::string,'false') NOT ILIKE 'true'
), n AS (
  SELECT NPI, UPPER(TRIM(AUTHORIZED_OFFICIAL_FIRST_NAME)) fn, UPPER(TRIM(AUTHORIZED_OFFICIAL_LAST_NAME)) ln,
         LEFT(UPPER(TRIM(AUTHORIZED_OFFICIAL_MIDDLE_NAME)),1) mi, PROVIDER_ORGANIZATION_NAME_LEGAL_BUSINESS_NAME org,
         UPPER(TRIM(PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_CITY_NAME)) city, PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_STATE_NAME st,
         TRY_TO_DATE(PROVIDER_ENUMERATION_DATE::string) enum_d, NPI_DEACTIVATION_DATE deact
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES
  WHERE ENTITY_TYPE_CODE::string = '2' AND AUTHORIZED_OFFICIAL_LAST_NAME IS NOT NULL
), pe AS (SELECT DISTINCT NPI FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PECOS_PROVIDER_ENROLLMENT),
m AS (
  SELECT DISTINCT n.NPI onpi, n.org, n.enum_d, l.nm, l.STATE, l.city, l.EXCLUSION_DATE, l.EXCLUSION_TYPE
  FROM l JOIN n ON n.fn = l.fn AND n.ln = l.ln AND n.st = l.STATE AND n.city = l.city
  JOIN pe ON pe.NPI = n.NPI
  WHERE NOT (n.mi IS NOT NULL AND n.mi <> '' AND l.mi <> '' AND n.mi <> l.mi) AND n.enum_d > l.EXCLUSION_DATE AND n.deact IS NULL
), b AS (
  SELECT RNDRNG_NPI::string npi, TOT_BENES, TOT_MDCR_ALOWD_AMT, TOT_MDCR_PYMT_AMT
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER
  WHERE RNDRNG_NPI::string IN (SELECT onpi FROM m)
)
SELECT m.onpi, LEFT(m.org,40) org, m.enum_d, LISTAGG(DISTINCT m.nm || ' (' || m.EXCLUSION_DATE || ' ' || m.EXCLUSION_TYPE || ')', '; ') banned_namesakes,
       ANY_VALUE(m.city) city, ANY_VALUE(m.STATE) st, MAX(b.TOT_BENES) benes_2024, MAX(b.TOT_MDCR_ALOWD_AMT) allowed_2024, MAX(b.TOT_MDCR_PYMT_AMT) paid_2024,
       SUM(MAX(b.TOT_MDCR_PYMT_AMT)) OVER () paid_all, COUNT(*) OVER () orgs
FROM m LEFT JOIN b ON b.npi = m.onpi
GROUP BY m.onpi, m.org, m.enum_d
ORDER BY paid_2024 DESC NULLS LAST;

-- Q32: Surviving AO matches (Moayed, Sangha, ASAP EMS): Medicare enrollment, Part B 2024, Part D, and the ambulance company's authorized-official details
SELECT 'PECOS' src, NPI::string npi, LEFT(COALESCE(ORG_NAME, FIRST_NAME||' '||COALESCE(MDL_NAME,'')||' '||LAST_NAME),40) a, LEFT(PROVIDER_TYPE_DESC,45) b,
       STATE_CD c, TRY_TO_DATE(SUBSTR(ENRLMT_ID,2,8),'YYYYMMDD')::string d
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PECOS_PROVIDER_ENROLLMENT
WHERE NPI::string IN ('1124126503','1295137784','1487288437','1376179309','1629604657','1639038375','1659653483','1003914383','1891885547')
UNION ALL
SELECT 'PartB 2024', RNDRNG_NPI::string, LEFT(COALESCE(RNDRNG_PRVDR_FIRST_NAME||' ','')||RNDRNG_PRVDR_LAST_ORG_NAME,40), 'benes '||TOT_BENES||' allowed '||TOT_MDCR_ALOWD_AMT,
       RNDRNG_PRVDR_CITY, 'paid '||TOT_MDCR_PYMT_AMT
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER
WHERE RNDRNG_NPI::string IN ('1124126503','1295137784','1487288437','1376179309','1629604657','1639038375','1003914383','1891885547')
UNION ALL
SELECT 'PartD', NPI::string, 'claims '||TOT_CLMS, 'drug cost '||TOT_DRUG_CST, 'benes '||TOT_BENES, ''
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PART_D_PRESCRIBERS
WHERE NPI::string IN ('1124126503','1295137784')
UNION ALL
SELECT 'NPPES AO', NPI::string, LEFT(PROVIDER_ORGANIZATION_NAME_LEGAL_BUSINESS_NAME,40),
       AUTHORIZED_OFFICIAL_FIRST_NAME||' '||COALESCE(AUTHORIZED_OFFICIAL_MIDDLE_NAME,'')||' '||AUTHORIZED_OFFICIAL_LAST_NAME||' '||COALESCE(AUTHORIZED_OFFICIAL_NAME_SUFFIX_TEXT,'')||' / '||COALESCE(AUTHORIZED_OFFICIAL_TITLE_OR_POSITION,''),
       PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_CITY_NAME, LAST_UPDATE_DATE::string
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES
WHERE NPI::string IN ('1659653483','1487288437','1639038375')
ORDER BY 1, 2;

-- Q33: Part B 2024 for the 8 strict-set orgs that Q31 dropped (LEIE middle name blank made its NOT(...) filter go NULL)
SELECT RNDRNG_NPI, RNDRNG_PRVDR_LAST_ORG_NAME, RNDRNG_PRVDR_CITY, RNDRNG_PRVDR_STATE_ABRVTN, TOT_BENES, TOT_MDCR_ALOWD_AMT, TOT_MDCR_PYMT_AMT
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER
WHERE RNDRNG_NPI::string IN ('1467330548','1184480311','1922637867','1598175333','1902118805','1619294550','1922288828','1386753580');

-- Q34: Namesake density for the three money leads: how many NPPES people and authorized officials carry each name in that city, and how many LEIE rows
WITH k AS (
  SELECT 'RAUL' fn, 'RODRIGUEZ' ln, 'MIAMI' city, 'FL' st UNION ALL
  SELECT 'KEVIN', 'SMITH', 'LAUREL', 'MS' UNION ALL
  SELECT 'BHUPINDER', 'SANGHA', 'FRESNO', 'CA'
), np AS (
  SELECT k.fn, k.ln, k.city,
         COUNT(DISTINCT IFF(n.ENTITY_TYPE_CODE::string = '1' AND UPPER(n.PROVIDER_FIRST_NAME) = k.fn AND UPPER(n.PROVIDER_LAST_NAME_LEGAL_NAME) = k.ln, n.NPI, NULL)) nppes_people,
         COUNT(DISTINCT IFF(n.ENTITY_TYPE_CODE::string = '2' AND UPPER(n.AUTHORIZED_OFFICIAL_FIRST_NAME) = k.fn AND UPPER(n.AUTHORIZED_OFFICIAL_LAST_NAME) = k.ln, n.NPI, NULL)) ao_orgs,
         LISTAGG(DISTINCT IFF(n.ENTITY_TYPE_CODE::string = '2' AND UPPER(n.AUTHORIZED_OFFICIAL_FIRST_NAME) = k.fn AND UPPER(n.AUTHORIZED_OFFICIAL_LAST_NAME) = k.ln,
                 COALESCE(LEFT(UPPER(n.AUTHORIZED_OFFICIAL_MIDDLE_NAME),1),'-'), NULL), ',') ao_middle_initials
  FROM k JOIN LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES n
    ON UPPER(TRIM(n.PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_CITY_NAME)) = k.city AND n.PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_STATE_NAME = k.st
  GROUP BY 1,2,3
), le AS (
  SELECT k.fn, k.ln, COUNT(*) leie_rows_state, COUNT_IF(UPPER(TRIM(l.CITY)) = k.city) leie_rows_city,
         LISTAGG(DISTINCT COALESCE(l.MIDDLE_NAME,'-')||' '||l.EXCLUSION_DATE||' '||l.EXCLUSION_TYPE||' '||l.CITY, '; ') leie_detail
  FROM k JOIN LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE l ON UPPER(TRIM(l.FIRST_NAME)) = k.fn AND UPPER(TRIM(l.LAST_NAME)) = k.ln AND l.STATE = k.st
  GROUP BY 1,2
)
SELECT np.*, le.leie_rows_state, le.leie_rows_city, LEFT(le.leie_detail,200) leie_detail
FROM np LEFT JOIN le ON le.fn = np.fn AND le.ln = np.ln;

