-- deep-16: coverage round 2 deep pass, 2026-09-24. Python door, QUERY_TAG 'coverage-r2-2026-09-24'.
-- Tables: SBIR_STTR_AWARDS, XC_RETRACTION_WATCH_DATABASE, NTSB_AVIATION_AIRCRAFT, NTSB_AVIATION_EVENTS.
-- Each connection also ran ALTER SESSION timeout 300 + query tag (not counted).

-- S01 SBIR: count + profile
SELECT COUNT(*) n, COUNT(DISTINCT award_record_id) ids, COUNT(DISTINCT UPPER(TRIM(company))) firms, COUNT(DISTINCT uei) ueis,
  SYSTEM$TYPEOF(MAX(award_amount)) amt_type, ROUND(SUM(award_amount)/1e9,2) usd_b,
  COUNT_IF(uei IS NULL OR uei='') uei_blank, ROUND(SUM(IFF(uei IS NULL OR uei='', award_amount,0))/1e9,2) uei_blank_usd_b,
  MIN(award_year) y_min, MAX(award_year) y_max, COUNT_IF(award_amount <= 1) amt_le1,
  LISTAGG(DISTINCT phase, '|') phases, LISTAGG(DISTINCT program, '|') programs, COUNT(DISTINCT agency) agencies,
  COUNT_IF(award_year BETWEEN 2015 AND 2025) n_1525, ROUND(SUM(IFF(award_year BETWEEN 2015 AND 2025, award_amount,0))/1e9,2) usd_1525_b
FROM LIBRARY_MARTS.SCIENCE_RESEARCH.SCIENCE_RESEARCH__FED_SBIR_STTR_AWARDS;

-- S02 SBIR: sample 5
SELECT company, uei, agency, branch, phase, program, award_year, award_amount, number_employees, city, state, award_title
FROM LIBRARY_MARTS.SCIENCE_RESEARCH.SCIENCE_RESEARCH__FED_SBIR_STTR_AWARDS LIMIT 5;

-- S03 Retraction Watch XC: count + profile, against the FED copy
SELECT COUNT(*) n, COUNT(DISTINCT record_id) recs, MIN(retraction_date) d_min, MAX(retraction_date) d_max,
  LISTAGG(DISTINCT retraction_nature, '|') natures,
  COUNT_IF(countries ILIKE '%United States%') us_rows,
  COUNT_IF(reasons ILIKE '%paper mill%') paper_mill, COUNT_IF(reasons ILIKE '%fabrication%' OR reasons ILIKE '%falsification%') fab_fals,
  COUNT_IF(reasons ILIKE '%Investigation by ORI%') ori,
  (SELECT COUNT(*) FROM LIBRARY_MARTS.SCIENCE_RESEARCH.SCIENCE_RESEARCH__FED_RETRACTION_WATCH) fed_copy_n,
  (SELECT COUNT(DISTINCT record_id) FROM LIBRARY_MARTS.SCIENCE_RESEARCH.SCIENCE_RESEARCH__FED_RETRACTION_WATCH) fed_copy_recs,
  (SELECT MAX(retraction_date) FROM LIBRARY_MARTS.SCIENCE_RESEARCH.SCIENCE_RESEARCH__FED_RETRACTION_WATCH) fed_copy_dmax
FROM LIBRARY_MARTS.SCIENCE_RESEARCH.SCIENCE_RESEARCH__XC_RETRACTION_WATCH_DATABASE;

-- S04 Retraction Watch XC: sample 5
SELECT record_id, retraction_date, retraction_nature, journal, publisher, LEFT(institutions,120) inst, countries, LEFT(authors,80) authors, LEFT(reasons,160) reasons
FROM LIBRARY_MARTS.SCIENCE_RESEARCH.SCIENCE_RESEARCH__XC_RETRACTION_WATCH_DATABASE LIMIT 5;

-- S05 NTSB aircraft: count + profile
SELECT COUNT(*) n, COUNT(DISTINCT ev_id) events, COUNT(DISTINCT ev_id||'-'||aircraft_key) ev_ac,
  COUNT(DISTINCT regis_no) tails, COUNT_IF(regis_no IS NULL OR regis_no IN ('None','','UNREG')) tail_blank,
  COUNT_IF(far_part='121') p121, COUNT_IF(far_part='135') p135, COUNT_IF(far_part='091') p091,
  LISTAGG(DISTINCT far_part, '|') parts,
  COUNT_IF(oper_name IS NULL OR oper_name='None') oper_blank, COUNT_IF(owner_acft IS NULL OR owner_acft='None') owner_blank,
  LISTAGG(DISTINCT air_medical,'|') air_med, LISTAGG(DISTINCT site_seeing,'|') sightsee
FROM LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_NTSB_AVIATION_AIRCRAFT;

-- S06 NTSB aircraft: sample 5 (Part 135)
SELECT ev_id, aircraft_key, regis_no, far_part, acft_make, acft_model, acft_serial_no, damage, oper_name, owner_acft, oper_cert_num, type_fly, air_medical, site_seeing
FROM LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_NTSB_AVIATION_AIRCRAFT WHERE far_part='135' LIMIT 5;

-- S07 NTSB events: count + profile
SELECT COUNT(*) n, COUNT(DISTINCT ev_id) events, MIN(ev_date) d_min, MAX(ev_date) d_max,
  LISTAGG(DISTINCT ev_type,'|') types, LISTAGG(DISTINCT ev_highest_injury,'|') hi_inj,
  SYSTEM$TYPEOF(MAX(inj_tot_f)) f_type,
  COUNT_IF(TRY_TO_NUMBER(TO_VARCHAR(inj_tot_f)) > 0) fatal_events, SUM(TRY_TO_NUMBER(TO_VARCHAR(inj_tot_f))) deaths,
  COUNT_IF(ev_highest_injury='FATL') fatl_flag, COUNT_IF(ev_country='USA') usa,
  COUNT_IF(apt_name IS NULL OR apt_name IN ('None','N/A','Private','PRIVATE')) apt_blank
FROM LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_NTSB_AVIATION_EVENTS;

-- S08 NTSB events: sample 5
SELECT ev_id, ntsb_no, ev_type, ev_date, ev_city, ev_state, ev_country, apt_name, ev_highest_injury, inj_tot_f, inj_tot_s, inj_tot_t
FROM LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_NTSB_AVIATION_EVENTS LIMIT 5;

-- S09 SBIR: top 25 firms by award count 2015-2025, name-normalized (UEI is blank before 2022)
WITH a AS (
  SELECT TRIM(REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(UPPER(company),'[^A-Z0-9 ]',' '),'\b(INC|INCORPORATED|LLC|L L C|CORP|CORPORATION|CO|COMPANY|LTD|LC|PLLC)\b',''),' +',' ')) firm,
    agency, phase, award_amount, number_employees, award_year
  FROM LIBRARY_MARTS.SCIENCE_RESEARCH.SCIENCE_RESEARCH__FED_SBIR_STTR_AWARDS WHERE award_year BETWEEN 2015 AND 2025),
tot AS (SELECT SUM(award_amount) t, COUNT(*) n FROM a),
f AS (SELECT firm, COUNT(*) awards, ROUND(SUM(award_amount)/1e6,1) usd_m, COUNT_IF(phase='Phase I') p1, COUNT_IF(phase='Phase II') p2,
  COUNT(DISTINCT agency) agencies, MODE(agency) top_agency, MAX(number_employees) max_emp, MEDIAN(number_employees) med_emp, COUNT(DISTINCT award_year) yrs
  FROM a GROUP BY 1)
SELECT f.*, ROUND(100*usd_m*1e6/(SELECT t FROM tot),2) pct_usd, ROUND(awards/NULLIF(med_emp,0),2) awards_per_emp
FROM f ORDER BY awards DESC LIMIT 25;

-- S10 SBIR: concentration 2015-2025 - firm count, top-20 / top-1% share, and firms with 100+ awards; phase I->II conversion peers
WITH a AS (
  SELECT TRIM(REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(UPPER(company),'[^A-Z0-9 ]',' '),'\b(INC|INCORPORATED|LLC|L L C|CORP|CORPORATION|CO|COMPANY|LTD|LC|PLLC)\b',''),' +',' ')) firm,
    phase, award_amount
  FROM LIBRARY_MARTS.SCIENCE_RESEARCH.SCIENCE_RESEARCH__FED_SBIR_STTR_AWARDS WHERE award_year BETWEEN 2015 AND 2025),
f AS (SELECT firm, COUNT(*) awards, SUM(award_amount) usd, COUNT_IF(phase='Phase I') p1, COUNT_IF(phase='Phase II') p2 FROM a GROUP BY 1),
r AS (SELECT f.*, ROW_NUMBER() OVER (ORDER BY awards DESC) rk, COUNT(*) OVER () nf, SUM(usd) OVER () tu, SUM(awards) OVER () ta FROM f)
SELECT MAX(nf) firms, ROUND(MAX(tu)/1e9,2) usd_b, MAX(ta) awards,
  ROUND(100*SUM(IFF(rk<=20,usd,0))/MAX(tu),1) top20_pct_usd, ROUND(100*SUM(IFF(rk<=20,awards,0))/MAX(ta),1) top20_pct_awards,
  ROUND(100*SUM(IFF(rk<=MAX(nf)*0.01,usd,0))/MAX(tu),1) top1pct_firms_pct_usd,
  COUNT_IF(awards>=100) firms_100plus, ROUND(100*SUM(IFF(awards>=100,usd,0))/MAX(tu),1) f100_pct_usd,
  COUNT_IF(awards>=50) firms_50plus, ROUND(100*SUM(IFF(awards>=50,usd,0))/MAX(tu),1) f50_pct_usd,
  COUNT_IF(awards=1) one_award_firms,
  ROUND(SUM(IFF(awards>=100,p2,0))/NULLIF(SUM(IFF(awards>=100,p1,0)),0),2) p2_per_p1_100plus,
  ROUND(SUM(IFF(awards BETWEEN 10 AND 99,p2,0))/NULLIF(SUM(IFF(awards BETWEEN 10 AND 99,p1,0)),0),2) p2_per_p1_10to99,
  ROUND(SUM(IFF(awards<10,p2,0))/NULLIF(SUM(IFF(awards<10,p1,0)),0),2) p2_per_p1_under10
FROM r;

-- S11 SBIR: same firm, same title, same phase, funded by 2+ agencies or 2+ times, 2015-2025 (duplicate-funding screen)
WITH a AS (
  SELECT TRIM(REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(UPPER(company),'[^A-Z0-9 ]',' '),'\b(INC|INCORPORATED|LLC|L L C|CORP|CORPORATION|CO|COMPANY|LTD|LC|PLLC)\b',''),' +',' ')) firm,
    REGEXP_REPLACE(UPPER(award_title),'[^A-Z0-9]','') tkey, agency, branch, phase, award_amount, award_year, agency_tracking_number, contract
  FROM LIBRARY_MARTS.SCIENCE_RESEARCH.SCIENCE_RESEARCH__FED_SBIR_STTR_AWARDS
  WHERE award_year BETWEEN 2015 AND 2025 AND award_title IS NOT NULL AND UPPER(award_title) NOT IN ('NOT AVAILABLE','SBIR PHASE I','SBIR PHASE II','STTR PHASE I','STTR PHASE II') AND LENGTH(award_title) >= 25),
g AS (SELECT firm, tkey, phase, COUNT(*) n, COUNT(DISTINCT agency) ag, COUNT(DISTINCT COALESCE(branch,agency)) br,
  COUNT(DISTINCT COALESCE(contract,agency_tracking_number)) contracts, SUM(award_amount) usd, MAX(award_year)-MIN(award_year) span
  FROM a GROUP BY 1,2,3 HAVING COUNT(*) > 1)
SELECT COUNT(*) dup_groups, SUM(n) rows_in_groups, ROUND(SUM(usd)/1e6,1) usd_m,
  COUNT_IF(ag>1) cross_agency_groups, ROUND(SUM(IFF(ag>1,usd,0))/1e6,1) cross_agency_usd_m,
  COUNT_IF(ag=1 AND br>1) cross_branch_groups, ROUND(SUM(IFF(ag=1 AND br>1,usd,0))/1e6,1) cross_branch_usd_m,
  COUNT_IF(br=1 AND contracts=1) same_contract_groups, COUNT_IF(br=1 AND contracts>1) same_branch_diff_contract,
  COUNT_IF(phase='Phase I') p1_groups, COUNT_IF(phase='Phase II') p2_groups,
  (SELECT COUNT(*) FROM a) denom_rows
FROM g;

-- S12 Retraction Watch: reason vocabulary for US rows retracted 2010-2026 (retractions only)
SELECT TRIM(REPLACE(r.value::string,'+','')) reason, COUNT(DISTINCT record_id) recs
FROM LIBRARY_MARTS.SCIENCE_RESEARCH.SCIENCE_RESEARCH__XC_RETRACTION_WATCH_DATABASE, LATERAL SPLIT_TO_TABLE(reasons, ';') r
WHERE countries ILIKE '%United States%' AND retraction_nature='Retraction' AND retraction_date >= '2010-01-01' AND TRIM(r.value::string) <> ''
GROUP BY 1 ORDER BY 2 DESC LIMIT 45;

-- S13 SBIR: concentration 2015-2025 (S10 rerun with the nesting fixed)
WITH a AS (
  SELECT TRIM(REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(UPPER(company),'[^A-Z0-9 ]',' '),'\b(INC|INCORPORATED|LLC|L L C|CORP|CORPORATION|CO|COMPANY|LTD|LC|PLLC)\b',''),' +',' ')) firm,
    phase, award_amount
  FROM LIBRARY_MARTS.SCIENCE_RESEARCH.SCIENCE_RESEARCH__FED_SBIR_STTR_AWARDS WHERE award_year BETWEEN 2015 AND 2025),
f AS (SELECT firm, COUNT(*) awards, SUM(award_amount) usd, COUNT_IF(phase='Phase I') p1, COUNT_IF(phase='Phase II') p2 FROM a GROUP BY 1),
r AS (SELECT f.*, ROW_NUMBER() OVER (ORDER BY awards DESC) rk, COUNT(*) OVER () nf, SUM(usd) OVER () tu, SUM(awards) OVER () ta FROM f)
SELECT MAX(nf) firms, ROUND(MAX(tu)/1e9,2) usd_b, MAX(ta) awards,
  ROUND(100*SUM(IFF(rk<=20,usd,0))/MAX(tu),1) top20_pct_usd, ROUND(100*SUM(IFF(rk<=20,awards,0))/MAX(ta),1) top20_pct_awards,
  ROUND(100*SUM(IFF(rk<=nf*0.01,usd,0))/MAX(tu),1) top1pct_firms_pct_usd, COUNT_IF(rk<=nf*0.01) top1pct_firms,
  COUNT_IF(awards>=100) firms_100plus, ROUND(100*SUM(IFF(awards>=100,usd,0))/MAX(tu),1) f100_pct_usd,
  COUNT_IF(awards>=50) firms_50plus, ROUND(100*SUM(IFF(awards>=50,usd,0))/MAX(tu),1) f50_pct_usd,
  COUNT_IF(awards=1) one_award_firms,
  ROUND(SUM(IFF(awards>=100,p2,0))/NULLIF(SUM(IFF(awards>=100,p1,0)),0),2) p2_per_p1_100plus,
  ROUND(SUM(IFF(awards BETWEEN 10 AND 99,p2,0))/NULLIF(SUM(IFF(awards BETWEEN 10 AND 99,p1,0)),0),2) p2_per_p1_10to99,
  ROUND(SUM(IFF(awards<10,p2,0))/NULLIF(SUM(IFF(awards<10,p1,0)),0),2) p2_per_p1_under10
FROM r;

-- S14 SBIR: drill the cross-agency and cross-branch same-title groups
WITH a AS (
  SELECT TRIM(REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(UPPER(company),'[^A-Z0-9 ]',' '),'\b(INC|INCORPORATED|LLC|L L C|CORP|CORPORATION|CO|COMPANY|LTD|LC|PLLC)\b',''),' +',' ')) firm,
    REGEXP_REPLACE(UPPER(award_title),'[^A-Z0-9]','') tkey, award_title, agency, branch, phase, award_amount, award_year, agency_tracking_number, contract, topic_code
  FROM LIBRARY_MARTS.SCIENCE_RESEARCH.SCIENCE_RESEARCH__FED_SBIR_STTR_AWARDS
  WHERE award_year BETWEEN 2015 AND 2025 AND award_title IS NOT NULL AND UPPER(award_title) NOT IN ('NOT AVAILABLE','SBIR PHASE I','SBIR PHASE II','STTR PHASE I','STTR PHASE II') AND LENGTH(award_title) >= 25),
g AS (SELECT firm, tkey, phase FROM a GROUP BY 1,2,3 HAVING COUNT(DISTINCT COALESCE(branch,agency)) > 1)
SELECT a.firm, a.phase, LEFT(MAX(a.award_title),70) title, COUNT(*) n, LISTAGG(DISTINCT COALESCE(a.branch,a.agency), ' / ') funders,
  LISTAGG(DISTINCT a.award_year, ',') yrs, ROUND(SUM(a.award_amount)/1e6,2) usd_m, LISTAGG(DISTINCT a.topic_code, ',') topics,
  LISTAGG(DISTINCT COALESCE(a.contract,a.agency_tracking_number), ' ; ') ids
FROM a JOIN g USING (firm, tkey, phase) GROUP BY 1,2,a.tkey ORDER BY usd_m DESC LIMIT 30;

-- S15 Retraction Watch: US authors with the most misconduct retractions 2010-2026, with publisher spread
WITH rw AS (
  SELECT record_id, retraction_date, publisher, journal, institutions, TRIM(a.value::string) author
  FROM LIBRARY_MARTS.SCIENCE_RESEARCH.SCIENCE_RESEARCH__XC_RETRACTION_WATCH_DATABASE, LATERAL SPLIT_TO_TABLE(authors, ';') a
  WHERE countries ILIKE '%United States%' AND retraction_nature='Retraction' AND retraction_date >= '2010-01-01'
    AND (reasons ILIKE '%Falsification/Fabrication%' OR reasons ILIKE '%Manipulation of Images%' OR reasons ILIKE '%Paper Mill%'
      OR reasons ILIKE '%Misconduct by Author%' OR reasons ILIKE '%Misconduct - Official%' OR reasons ILIKE '%Investigation by ORI%'
      OR reasons ILIKE '%Plagiarism of%' OR reasons ILIKE '%Fake Peer Review%')
    AND TRIM(a.value::string) <> '')
SELECT author, COUNT(DISTINCT record_id) recs, COUNT(DISTINCT publisher) pubs, COUNT(DISTINCT journal) journals,
  MIN(retraction_date) first_r, MAX(retraction_date) last_r, LEFT(MODE(institutions),90) inst,
  (SELECT COUNT(DISTINCT record_id) FROM rw) total_recs, (SELECT COUNT(DISTINCT author) FROM rw) total_authors
FROM rw GROUP BY 1 ORDER BY recs DESC LIMIT 30;

-- S16 SBIR: duplicate-row trap - same contract number on 2+ rows with the same amount, all years
WITH k AS (
  SELECT UPPER(REGEXP_REPLACE(COALESCE(NULLIF(contract,''),agency_tracking_number),'[^A-Za-z0-9]','')) ckey, award_amount, phase, award_year
  FROM LIBRARY_MARTS.SCIENCE_RESEARCH.SCIENCE_RESEARCH__FED_SBIR_STTR_AWARDS WHERE COALESCE(NULLIF(contract,''),agency_tracking_number) IS NOT NULL),
g AS (SELECT ckey, award_amount, COUNT(*) n FROM k GROUP BY 1,2)
SELECT (SELECT COUNT(*) FROM k) rows_with_id, COUNT_IF(n>1) dup_keys, SUM(IFF(n>1,n-1,0)) extra_rows, ROUND(SUM(IFF(n>1,(n-1)*award_amount,0))/1e6,1) extra_usd_m,
  ROUND(SUM(IFF(n>1,(n-1)*award_amount,0))/SUM(n*award_amount)*100,2) extra_pct_usd, MAX(n) max_n,
  MAX_BY(ckey, n) worst_key
FROM g;

-- S17 Retraction Watch x NIH RePORTER: repeat US misconduct authors (3+ retractions 2010-2025), unique NIH profile, money after the LAST retraction
WITH rw AS (
  SELECT record_id, retraction_date, institutions, TRIM(a.value::string) author
  FROM LIBRARY_MARTS.SCIENCE_RESEARCH.SCIENCE_RESEARCH__XC_RETRACTION_WATCH_DATABASE, LATERAL SPLIT_TO_TABLE(authors, ';') a
  WHERE countries ILIKE '%United States%' AND retraction_nature='Retraction' AND retraction_date BETWEEN '2010-01-01' AND '2025-12-31'
    AND (reasons ILIKE '%Falsification/Fabrication%' OR reasons ILIKE '%Manipulation of Images%' OR reasons ILIKE '%Paper Mill%'
      OR reasons ILIKE '%Misconduct by Author%' OR reasons ILIKE '%Misconduct - Official%' OR reasons ILIKE '%Investigation by ORI%'
      OR reasons ILIKE '%Plagiarism of%' OR reasons ILIKE '%Fake Peer Review%')
    AND TRIM(a.value::string) <> ''),
auth AS (SELECT author, COUNT(DISTINCT record_id) recs, MIN(retraction_date) first_r, MAX(retraction_date) last_r, MODE(institutions) inst
  FROM rw GROUP BY 1 HAVING COUNT(DISTINCT record_id) >= 3),
authn AS (SELECT *, UPPER(REGEXP_SUBSTR(author,'[A-Za-z\-]+$')) last_nm, UPPER(SPLIT_PART(author,' ',1)) first_nm FROM auth
  WHERE ARRAY_SIZE(SPLIT(author,' ')) >= 2 AND LENGTH(SPLIT_PART(author,' ',1)) >= 3),
nih AS (
  SELECT appl_id, fiscal_year, org_name, award_amount, award_notice_date, TRIM(p.value::string) pi, TRIM(SPLIT_PART(pi_profile_ids, ';', p.index)) profile_id
  FROM LIBRARY_MARTS.SCIENCE_RESEARCH.SCIENCE_RESEARCH__FED_NIH_REPORTER, LATERAL SPLIT_TO_TABLE(pi_names, ';') p
  WHERE fiscal_year BETWEEN 2010 AND 2026 AND pi_profile_ids IS NOT NULL),
nihn AS (SELECT *, UPPER(REGEXP_SUBSTR(REGEXP_REPLACE(pi,'\s*\(contact\)',''), '[A-Za-z\-]+$')) last_nm, UPPER(SPLIT_PART(pi,' ',1)) first_nm
  FROM nih WHERE ARRAY_SIZE(SPLIT(pi,' ')) >= 2 AND profile_id <> ''),
nihf AS (SELECT * FROM nihn WHERE last_nm IN (SELECT last_nm FROM authn)),
namekey AS (SELECT last_nm, first_nm, COUNT(DISTINCT profile_id) profiles FROM nihf GROUP BY 1,2),
m AS (
  SELECT a.author, a.recs, a.first_r, a.last_r, LEFT(a.inst,70) rw_inst, MAX(n.pi) nih_name_seen, MAX(n.profile_id) profile,
    COUNT(DISTINCT n.appl_id) nih_awards_all, MIN(n.fiscal_year) fy_min, MAX(n.fiscal_year) fy_max,
    COUNT(DISTINCT IFF(n.award_notice_date > a.last_r, n.appl_id, NULL)) awards_after_last,
    ROUND(SUM(IFF(n.award_notice_date > a.last_r, n.award_amount, 0))/1e6,2) usd_after_last_m,
    ROUND(SUM(IFF(n.award_notice_date > a.first_r, n.award_amount, 0))/1e6,2) usd_after_first_m,
    LEFT(MAX(IFF(n.award_notice_date > a.last_r, n.org_name, NULL)),50) org_after
  FROM authn a JOIN namekey k ON k.last_nm=a.last_nm AND k.first_nm=a.first_nm AND k.profiles=1
  JOIN nihf n ON n.last_nm=a.last_nm AND n.first_nm=a.first_nm GROUP BY 1,2,3,4,5)
SELECT m.*, (SELECT COUNT(*) FROM auth) repeat_authors, (SELECT COUNT(*) FROM authn) nameable, (SELECT COUNT(*) FROM m) matched_unique,
  (SELECT COUNT_IF(usd_after_last_m>0) FROM m) with_money_after_last, (SELECT SUM(usd_after_last_m) FROM m) total_after_last_m
FROM m ORDER BY usd_after_last_m DESC, nih_awards_all DESC LIMIT 40;

-- S18 NTSB aircraft x events: Part 121 and 135 operators by US events 2008-2026 (operator = OPER_NAME, else owner)
WITH a AS (
  SELECT ac.ev_id, ac.far_part,
    TRIM(REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(UPPER(COALESCE(NULLIF(ac.oper_name,'None'),NULLIF(ac.owner_acft,'None'))),'[^A-Z0-9 ]',' '),'\b(INC|LLC|CORP|CORPORATION|CO|COMPANY|LTD|DBA|THE)\b',''),' +',' ')) op,
    UPPER(TRIM(ac.regis_no)) tail, e.ev_type, e.ev_date, TRY_TO_NUMBER(TO_VARCHAR(e.inj_tot_f)) f
  FROM LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_NTSB_AVIATION_AIRCRAFT ac
  JOIN LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_NTSB_AVIATION_EVENTS e ON e.ev_id = ac.ev_id
  WHERE e.ev_country='USA' AND ac.far_part IN ('121','135')),
pe AS (SELECT far_part, op, ev_id, MAX(ev_type) ev_type, MAX(f) f, MAX(ev_date) d, COUNT(DISTINCT tail) tails FROM a GROUP BY 1,2,3),
o AS (SELECT far_part, op, COUNT(*) events, COUNT_IF(ev_type='ACC') accidents, COUNT_IF(f>0) fatal, SUM(f) deaths, SUM(tails) tail_events, MIN(d) first_d, MAX(d) last_d
  FROM pe GROUP BY 1,2)
SELECT o.*, SUM(events) OVER (PARTITION BY far_part) part_events, SUM(fatal) OVER (PARTITION BY far_part) part_fatal,
  COUNT(*) OVER (PARTITION BY far_part) part_ops
FROM o QUALIFY ROW_NUMBER() OVER (PARTITION BY far_part ORDER BY events DESC, fatal DESC) <= 18 ORDER BY far_part, events DESC;

-- S19 NTSB: tails with 2+ US events under Part 121/135, joined to the FAA registry (Aug 2026), serial number as second field
WITH a AS (
  SELECT UPPER(TRIM(ac.regis_no)) tail, UPPER(REGEXP_REPLACE(ac.acft_serial_no,'[^A-Za-z0-9]','')) ser, ac.acft_make, ac.acft_model, ac.far_part, ac.damage,
    COALESCE(NULLIF(ac.oper_name,'None'),NULLIF(ac.owner_acft,'None')) op, e.ev_id, e.ev_date, TRY_TO_NUMBER(TO_VARCHAR(e.inj_tot_f)) f
  FROM LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_NTSB_AVIATION_AIRCRAFT ac
  JOIN LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_NTSB_AVIATION_EVENTS e ON e.ev_id = ac.ev_id
  WHERE e.ev_country='USA' AND ac.far_part IN ('121','135') AND ac.regis_no ILIKE 'N%'),
t AS (SELECT tail, MAX(ser) ser, COUNT(DISTINCT ser) sers, MAX(acft_make||' '||acft_model) ac, COUNT(DISTINCT ev_id) evs, COUNT(DISTINCT IFF(f>0,ev_id,NULL)) fatal,
  LISTAGG(DISTINCT damage,',') dmg, MAX(op) op, MIN(ev_date) first_d, MAX(ev_date) last_d FROM a GROUP BY 1 HAVING COUNT(DISTINCT ev_id) >= 2),
r AS (SELECT 'N'||UPPER(TRIM(n_number)) tail, UPPER(REGEXP_REPLACE(serial_number,'[^A-Za-z0-9]','')) rser, registrant_name, status_code, last_action_date, cert_issue_date, expiration_date, year_mfr
  FROM LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_FAA_AIRCRAFT_REGISTRY)
SELECT t.*, r.rser, LEFT(r.registrant_name,35) registrant, r.status_code, r.last_action_date, r.cert_issue_date, r.expiration_date,
  COUNT(*) OVER () repeat_tails, COUNT_IF(r.tail IS NOT NULL) OVER () in_registry, COUNT_IF(r.rser = t.ser) OVER () serial_agrees,
  (SELECT COUNT(DISTINCT tail) FROM a) all_tails
FROM t LEFT JOIN r ON r.tail = t.tail ORDER BY evs DESC, fatal DESC LIMIT 30;

-- S21 NTSB events: fatal share by operation type, US events 2008-2026 (first aircraft of each event); FATL flag vs death count check
WITH e AS (SELECT ev_id, ev_type, TRY_TO_NUMBER(TO_VARCHAR(inj_tot_f)) f, ev_highest_injury h FROM LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_NTSB_AVIATION_EVENTS WHERE ev_country='USA'),
ac AS (SELECT ev_id, CASE WHEN far_part='121' THEN '121 airline'
    WHEN far_part='135' AND air_medical='Y' THEN '135 air medical' WHEN far_part='135' AND site_seeing='Y' THEN '135 air tour'
    WHEN far_part='135' THEN '135 charter/cargo other' WHEN far_part LIKE '091%' AND air_medical='Y' THEN '91 air medical'
    WHEN far_part LIKE '091%' AND site_seeing='Y' THEN '91 air tour (LOA)' WHEN far_part='091K' THEN '91K fractional'
    WHEN far_part='091' AND type_fly='SKYD' THEN '91 skydiving' WHEN far_part='091' AND type_fly='INST' THEN '91 instruction'
    WHEN far_part='091' AND homebuilt='Y' THEN '91 homebuilt' WHEN far_part='091' THEN '91 other private' WHEN far_part='137' THEN '137 crop dusting'
    WHEN far_part='133' THEN '133 external load' WHEN far_part='PUBU' THEN 'public use' WHEN far_part='107' THEN '107 drone' ELSE 'other/unknown '||far_part END grp
  FROM LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_NTSB_AVIATION_AIRCRAFT WHERE aircraft_key=1)
SELECT grp, COUNT(*) events, COUNT_IF(ev_type='ACC') accidents, COUNT_IF(f>0) fatal_events, ROUND(100*COUNT_IF(f>0)/NULLIF(COUNT_IF(ev_type='ACC'),0),1) fatal_pct_of_acc,
  SUM(f) deaths, COUNT_IF(h='FATL' AND COALESCE(f,0)=0) fatl_flag_no_deaths, COUNT_IF(f>0 AND h<>'FATL') deaths_no_flag,
  SUM(COUNT(*)) OVER () all_events, (SELECT COUNT(*) FROM e) us_events_total
FROM e LEFT JOIN ac USING (ev_id) GROUP BY grp ORDER BY events DESC;

-- S22 NTSB: named operators (not 'Pilot') with 3+ fatal US events 2008-2026, all FAR parts
WITH a AS (
  SELECT ac.ev_id, ac.far_part, ac.type_fly,
    TRIM(REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(UPPER(NULLIF(ac.oper_name,'None')),'[^A-Z0-9 ]',' '),'\b(INC|LLC|CORP|CORPORATION|CO|COMPANY|LTD|DBA|THE)\b',''),' +',' ')) op,
    e.ev_type, e.ev_date, TRY_TO_NUMBER(TO_VARCHAR(e.inj_tot_f)) f, e.ev_state
  FROM LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_NTSB_AVIATION_AIRCRAFT ac
  JOIN LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_NTSB_AVIATION_EVENTS e ON e.ev_id = ac.ev_id
  WHERE e.ev_country='USA'),
pe AS (SELECT op, ev_id, MAX(f) f, MAX(ev_type) t, MAX(ev_date) d, LISTAGG(DISTINCT far_part,',') parts, MAX(ev_state) st FROM a WHERE op IS NOT NULL AND op NOT IN ('PILOT','','N A','NA','UNKNOWN','PRIVATE') GROUP BY 1,2)
SELECT op, COUNT(*) events, COUNT_IF(f>0) fatal, SUM(f) deaths, LISTAGG(DISTINCT parts,',') parts, LISTAGG(DISTINCT st,',') states,
  MIN(IFF(f>0,d,NULL)) first_fatal, MAX(IFF(f>0,d,NULL)) last_fatal, MAX(d) last_event,
  COUNT(*) OVER () ops_with_3plus
FROM pe GROUP BY 1 HAVING COUNT_IF(f>0) >= 3 ORDER BY fatal DESC, deaths DESC LIMIT 30;

-- S23 NTSB events: US airports with the most fatal events 2008-2026, with each airport's accident count
WITH e AS (SELECT UPPER(TRIM(ev_nr_apt_id)) apt, MAX(apt_name) OVER (PARTITION BY UPPER(TRIM(ev_nr_apt_id))) nm, ev_state, ev_type, ev_nr_apt_loc, TRY_TO_NUMBER(TO_VARCHAR(inj_tot_f)) f
  FROM LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_NTSB_AVIATION_EVENTS
  WHERE ev_country='USA' AND ev_nr_apt_id IS NOT NULL AND UPPER(TRIM(ev_nr_apt_id)) NOT IN ('NONE','PVT','N/A','NA',''))
SELECT apt, MAX(nm) name, MAX(ev_state) st, COUNT(*) events, COUNT_IF(ev_type='ACC') accidents, COUNT_IF(f>0) fatal, SUM(f) deaths,
  COUNT_IF(f>0 AND ev_nr_apt_loc='ONAP') fatal_on_airport, ROUND(100*COUNT_IF(f>0)/NULLIF(COUNT_IF(ev_type='ACC'),0),1) fatal_pct,
  COUNT(*) OVER () airports, SUM(COUNT_IF(f>0)) OVER () all_fatal_with_apt
FROM e GROUP BY apt ORDER BY fatal DESC, deaths DESC LIMIT 20;

-- S20 NTSB x FAA registry: US aircraft the NTSB rated DESTROYED, still on the Aug 2026 FAA registry with the same serial number
WITH d AS (
  SELECT DISTINCT ac.ev_id, UPPER(TRIM(ac.regis_no)) tail, UPPER(REGEXP_REPLACE(ac.acft_serial_no,'[^A-Za-z0-9]','')) ser, e.ev_date, ac.far_part,
    TRY_TO_NUMBER(TO_VARCHAR(e.inj_tot_f)) f, ac.acft_make
  FROM LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_NTSB_AVIATION_AIRCRAFT ac
  JOIN LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_NTSB_AVIATION_EVENTS e ON e.ev_id = ac.ev_id
  WHERE ac.damage='DEST' AND e.ev_country='USA' AND ac.regis_no ILIKE 'N%' AND ac.acft_serial_no NOT IN ('None','') ),
r AS (SELECT 'N'||UPPER(TRIM(n_number)) tail, UPPER(REGEXP_REPLACE(serial_number,'[^A-Za-z0-9]','')) rser, status_code,
  TRY_TO_DATE(TO_VARCHAR(last_action_date)) lad, TRY_TO_DATE(TO_VARCHAR(cert_issue_date)) cid, TRY_TO_DATE(TO_VARCHAR(expiration_date)) exd, registrant_name
  FROM LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_FAA_AIRCRAFT_REGISTRY),
j AS (SELECT d.*, r.rser, r.status_code, r.lad, r.cid, r.exd, r.registrant_name, (r.tail IS NOT NULL) in_reg, (r.rser = d.ser) same_ser FROM d LEFT JOIN r ON r.tail = d.tail)
SELECT COUNT(*) destroyed, COUNT_IF(in_reg) tail_on_registry, COUNT_IF(same_ser) same_serial,
  COUNT_IF(same_ser AND cid < ev_date) same_ser_cert_before_crash, COUNT_IF(same_ser AND cid >= ev_date) same_ser_cert_after_crash,
  COUNT_IF(same_ser AND cid < ev_date AND lad > ev_date) cert_before_but_touched_after, COUNT_IF(same_ser AND f>0) same_ser_fatal,
  COUNT_IF(same_ser AND cid < ev_date AND f>0) fatal_cert_before, LISTAGG(DISTINCT IFF(same_ser, status_code, NULL), ',') statuses,
  COUNT_IF(same_ser AND exd > '2026-09-24') same_ser_unexpired, COUNT_IF(same_ser AND cid IS NULL) same_ser_no_cid,
  MIN(IFF(same_ser, ev_date, NULL)) earliest_crash
FROM j;

-- S24 NIH RePORTER trap check: PI_PROFILE_IDS delimiter vs PI_NAMES delimiter on multi-PI grants (F-008 splits both on ';')
SELECT COUNT(*) rows_n, COUNT_IF(pi_names LIKE '%;%') multi_pi_rows, COUNT_IF(pi_names LIKE '%;%' AND pi_profile_ids LIKE '%;%') ids_semicolon,
  COUNT_IF(pi_names LIKE '%;%' AND pi_profile_ids LIKE '%,%') ids_comma, COUNT_IF(pi_names LIKE '%;%' AND pi_profile_ids NOT LIKE '%;%' AND pi_profile_ids NOT LIKE '%,%') ids_single,
  MAX(IFF(pi_names LIKE '%;%', pi_names || ' || ' || pi_profile_ids, NULL)) example,
  COUNT_IF(REGEXP_COUNT(pi_names, ';') <> REGEXP_COUNT(pi_profile_ids, ';')) count_mismatch
FROM LIBRARY_MARTS.SCIENCE_RESEARCH.SCIENCE_RESEARCH__FED_NIH_REPORTER WHERE fiscal_year BETWEEN 2010 AND 2026;

-- S25 SBIR: the cross-AGENCY same-title same-phase groups 2015-2025 (different departments funding one title)
WITH a AS (
  SELECT TRIM(REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(UPPER(company),'[^A-Z0-9 ]',' '),'\b(INC|INCORPORATED|LLC|L L C|CORP|CORPORATION|CO|COMPANY|LTD|LC|PLLC)\b',''),' +',' ')) firm,
    REGEXP_REPLACE(UPPER(award_title),'[^A-Z0-9]','') tkey, award_title, agency, branch, phase, award_amount, award_year, agency_tracking_number, contract, pi_name
  FROM LIBRARY_MARTS.SCIENCE_RESEARCH.SCIENCE_RESEARCH__FED_SBIR_STTR_AWARDS
  WHERE award_year BETWEEN 2015 AND 2025 AND award_title IS NOT NULL AND UPPER(award_title) NOT IN ('NOT AVAILABLE','SBIR PHASE I','SBIR PHASE II','STTR PHASE I','STTR PHASE II') AND LENGTH(award_title) >= 25),
g AS (SELECT firm, tkey, phase FROM a GROUP BY 1,2,3 HAVING COUNT(DISTINCT agency) > 1)
SELECT a.firm, a.phase, LEFT(MAX(a.award_title),60) title, COUNT(*) n, LISTAGG(DISTINCT a.agency||':'||a.award_year||':'||ROUND(a.award_amount/1e3)||'K', ' / ') funding,
  LISTAGG(DISTINCT a.pi_name, ' ; ') pis, ROUND(SUM(a.award_amount)/1e6,2) usd_m
FROM a JOIN g USING (firm, tkey, phase) GROUP BY 1,2,a.tkey ORDER BY usd_m DESC LIMIT 15;

-- S26 NTSB events: is any airport's fatal share out of line with chance? z-score vs the all-airport fatal share, airports with 15+ accidents
WITH e AS (SELECT UPPER(TRIM(ev_nr_apt_id)) apt, ev_type, TRY_TO_NUMBER(TO_VARCHAR(inj_tot_f)) f
  FROM LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_NTSB_AVIATION_EVENTS
  WHERE ev_country='USA' AND ev_type='ACC' AND ev_nr_apt_id IS NOT NULL AND UPPER(TRIM(ev_nr_apt_id)) NOT IN ('NONE','PVT','N/A','NA','')),
p AS (SELECT COUNT_IF(f>0)/COUNT(*) p, COUNT(*) acc FROM e),
a AS (SELECT apt, COUNT(*) n, COUNT_IF(f>0) k FROM e GROUP BY 1 HAVING COUNT(*) >= 15)
SELECT (SELECT ROUND(p*100,1) FROM p) base_fatal_pct, (SELECT acc FROM p) base_acc, COUNT(*) airports_15plus,
  COUNT_IF((k - n*(SELECT p FROM p))/SQRT(n*(SELECT p FROM p)*(1-(SELECT p FROM p))) >= 3) z_ge_3,
  COUNT_IF((k - n*(SELECT p FROM p))/SQRT(n*(SELECT p FROM p)*(1-(SELECT p FROM p))) >= 2.5) z_ge_2_5,
  MAX_BY(apt, (k - n*(SELECT p FROM p))/SQRT(n*(SELECT p FROM p)*(1-(SELECT p FROM p)))) top_apt,
  ROUND(MAX((k - n*(SELECT p FROM p))/SQRT(n*(SELECT p FROM p)*(1-(SELECT p FROM p)))),2) top_z
FROM a;

-- S27 NTSB: air-medical accidents by period (FAA HEMS rule took effect 2014-04-22 / 2015-04) vs other Part 135, US, first aircraft
WITH e AS (SELECT ev_id, ev_type, ev_date, TRY_TO_NUMBER(TO_VARCHAR(inj_tot_f)) f, light_cond FROM LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_NTSB_AVIATION_EVENTS WHERE ev_country='USA' AND ev_type='ACC'),
ac AS (SELECT ev_id, IFF(air_medical='Y','air medical (91+135)', IFF(far_part='135','135 other',NULL)) grp, acft_category
  FROM LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_NTSB_AVIATION_AIRCRAFT WHERE aircraft_key=1 AND (air_medical='Y' OR far_part='135'))
SELECT grp, CASE WHEN ev_date < '2014-01-01' THEN '2008-13' WHEN ev_date < '2020-01-01' THEN '2014-19' ELSE '2020-26' END period,
  COUNT(*) accidents, COUNT_IF(f>0) fatal, ROUND(100*COUNT_IF(f>0)/COUNT(*),1) fatal_pct, SUM(f) deaths,
  COUNT_IF(f>0 AND light_cond LIKE 'NIT%') fatal_night, COUNT_IF(acft_category='HELI') heli
FROM e JOIN ac USING (ev_id) GROUP BY 1,2 ORDER BY 1,2;

-- S28 NTSB x FAA registry: destroyed + same serial, by registry status code and by when the registry last touched the record
WITH d AS (
  SELECT DISTINCT ac.ev_id, UPPER(TRIM(ac.regis_no)) tail, UPPER(REGEXP_REPLACE(ac.acft_serial_no,'[^A-Za-z0-9]','')) ser, e.ev_date,
    TRY_TO_NUMBER(TO_VARCHAR(e.inj_tot_f)) f
  FROM LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_NTSB_AVIATION_AIRCRAFT ac
  JOIN LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_NTSB_AVIATION_EVENTS e ON e.ev_id = ac.ev_id
  WHERE ac.damage='DEST' AND e.ev_country='USA' AND ac.regis_no ILIKE 'N%' AND ac.acft_serial_no NOT IN ('None','')),
r AS (SELECT 'N'||UPPER(TRIM(n_number)) tail, UPPER(REGEXP_REPLACE(serial_number,'[^A-Za-z0-9]','')) rser, status_code,
  TRY_TO_DATE(TO_VARCHAR(last_action_date)) lad, TRY_TO_DATE(TO_VARCHAR(cert_issue_date)) cid, TRY_TO_DATE(TO_VARCHAR(expiration_date)) exd
  FROM LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_FAA_AIRCRAFT_REGISTRY)
SELECT r.status_code, IFF(r.cid < d.ev_date, 'cert before crash', 'cert after crash') cert_timing,
  COUNT(*) n, COUNT_IF(d.f>0) fatal, SUM(d.f) deaths, COUNT_IF(r.lad > d.ev_date) touched_after, MIN(YEAR(r.lad)) lad_min_y, MAX(YEAR(r.lad)) lad_max_y,
  MODE(YEAR(r.lad)) lad_mode_y, COUNT_IF(r.exd > '2026-09-24') unexpired, MIN(d.ev_date) crash_min, MAX(d.ev_date) crash_max
FROM d JOIN r ON r.tail = d.tail AND r.rser = d.ser GROUP BY 1,2 ORDER BY n DESC;

-- S29 NTSB x FAA registry: the worst fatal crashes whose destroyed aircraft still hold a V registration issued before the crash
WITH d AS (
  SELECT ac.ev_id, ac.ntsb_no, UPPER(TRIM(ac.regis_no)) tail, UPPER(REGEXP_REPLACE(ac.acft_serial_no,'[^A-Za-z0-9]','')) ser, e.ev_date, e.ev_city, e.ev_state,
    TRY_TO_NUMBER(TO_VARCHAR(e.inj_tot_f)) f, ac.acft_make, ac.acft_model, ac.far_part, COALESCE(NULLIF(ac.owner_acft,'None'), NULLIF(ac.oper_name,'None')) ntsb_owner
  FROM LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_NTSB_AVIATION_AIRCRAFT ac
  JOIN LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_NTSB_AVIATION_EVENTS e ON e.ev_id = ac.ev_id
  WHERE ac.damage='DEST' AND e.ev_country='USA' AND ac.regis_no ILIKE 'N%' AND ac.acft_serial_no NOT IN ('None','')),
r AS (SELECT 'N'||UPPER(TRIM(n_number)) tail, UPPER(REGEXP_REPLACE(serial_number,'[^A-Za-z0-9]','')) rser, status_code, registrant_name,
  TRY_TO_DATE(TO_VARCHAR(last_action_date)) lad, TRY_TO_DATE(TO_VARCHAR(cert_issue_date)) cid, TRY_TO_DATE(TO_VARCHAR(expiration_date)) exd
  FROM LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_FAA_AIRCRAFT_REGISTRY)
SELECT d.ntsb_no, d.tail, d.ev_date, d.ev_city, d.ev_state, d.f deaths, d.acft_make||' '||d.acft_model ac, d.far_part, LEFT(d.ntsb_owner,30) ntsb_owner,
  LEFT(r.registrant_name,30) faa_registrant, r.status_code, r.cid, r.lad, r.exd
FROM d JOIN r ON r.tail = d.tail AND r.rser = d.ser
WHERE r.status_code='V' AND r.cid < d.ev_date AND d.f > 0 ORDER BY d.f DESC, d.ev_date DESC LIMIT 20;

-- S30 NTSB events: the 10 fatal accidents tied to LNA (Palm Beach County Park, Lantana FL)
SELECT e.ntsb_no, e.ev_date, e.ev_city, e.ev_nr_apt_loc, e.apt_dist, TRY_TO_NUMBER(TO_VARCHAR(e.inj_tot_f)) deaths, e.light_cond, e.wx_cond_basic,
  ac.far_part, ac.type_fly, ac.acft_make||' '||ac.acft_model ac, LEFT(COALESCE(NULLIF(ac.oper_name,'None'),NULLIF(ac.owner_acft,'None')),30) op, ac.regis_no
FROM LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_NTSB_AVIATION_EVENTS e
JOIN LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_NTSB_AVIATION_AIRCRAFT ac ON ac.ev_id = e.ev_id
WHERE UPPER(TRIM(e.ev_nr_apt_id))='LNA' AND e.ev_country='USA' AND TRY_TO_NUMBER(TO_VARCHAR(e.inj_tot_f)) > 0 ORDER BY e.ev_date;

-- S31 NTSB x FAA registry: destroyed aircraft still V with a pre-crash certificate, by crash year (rules out paperwork lag), plus owner-name agreement
WITH d AS (
  SELECT DISTINCT ac.ev_id, UPPER(TRIM(ac.regis_no)) tail, UPPER(REGEXP_REPLACE(ac.acft_serial_no,'[^A-Za-z0-9]','')) ser, e.ev_date,
    TRY_TO_NUMBER(TO_VARCHAR(e.inj_tot_f)) f, UPPER(REGEXP_REPLACE(COALESCE(NULLIF(ac.owner_acft,'None'),''),'[^A-Za-z]','')) own
  FROM LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_NTSB_AVIATION_AIRCRAFT ac
  JOIN LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_NTSB_AVIATION_EVENTS e ON e.ev_id = ac.ev_id
  WHERE ac.damage='DEST' AND e.ev_country='USA' AND ac.regis_no ILIKE 'N%' AND ac.acft_serial_no NOT IN ('None','')),
r AS (SELECT 'N'||UPPER(TRIM(n_number)) tail, UPPER(REGEXP_REPLACE(serial_number,'[^A-Za-z0-9]','')) rser, status_code,
  TRY_TO_DATE(TO_VARCHAR(cert_issue_date)) cid, UPPER(REGEXP_REPLACE(registrant_name,'[^A-Za-z]','')) reg
  FROM LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_FAA_AIRCRAFT_REGISTRY),
j AS (SELECT d.*, (r.status_code='V' AND r.rser=d.ser AND r.cid < d.ev_date) stale, r.reg FROM d LEFT JOIN r ON r.tail=d.tail)
SELECT CASE WHEN YEAR(ev_date) <= 2015 THEN '2008-15' WHEN YEAR(ev_date) <= 2020 THEN '2016-20' WHEN YEAR(ev_date) <= 2023 THEN '2021-23' ELSE '2024-26' END crash_period,
  COUNT(*) destroyed, COUNT_IF(stale) still_valid, ROUND(100*COUNT_IF(stale)/COUNT(*),1) pct_still_valid,
  COUNT_IF(f>0) fatal_destroyed, COUNT_IF(stale AND f>0) fatal_still_valid, SUM(IFF(stale,f,0)) deaths_still_valid,
  COUNT_IF(stale AND own <> '') stale_with_ntsb_owner, COUNT_IF(stale AND own <> '' AND LEFT(own,6)=LEFT(reg,6)) owner_first6_agree
FROM j GROUP BY 1 ORDER BY 1;

-- S32 SBIR trap check: is NUMBER_EMPLOYEES one value stamped on every award of a firm?
WITH a AS (SELECT TRIM(REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(UPPER(company),'[^A-Z0-9 ]',' '),'\b(INC|INCORPORATED|LLC|L L C|CORP|CORPORATION|CO|COMPANY|LTD|LC|PLLC)\b',''),' +',' ')) firm,
  number_employees, award_year FROM LIBRARY_MARTS.SCIENCE_RESEARCH.SCIENCE_RESEARCH__FED_SBIR_STTR_AWARDS),
f AS (SELECT firm, COUNT(*) n, COUNT(DISTINCT number_employees) ne, COUNT(DISTINCT award_year) yrs FROM a GROUP BY 1 HAVING COUNT(*) >= 10)
SELECT COUNT(*) firms_10plus, COUNT_IF(ne=1) one_value, COUNT_IF(ne=0) all_null, COUNT_IF(ne>1) varies, ROUND(100*COUNT_IF(ne<=1)/COUNT(*),1) pct_constant,
  (SELECT COUNT_IF(number_employees IS NULL) FROM a) null_rows, (SELECT COUNT(*) FROM a) all_rows
FROM f;

-- S33 FAA registry: do last-action dates cluster on batch days (a mass extension), and how long are current terms?
WITH r AS (SELECT status_code, TRY_TO_DATE(TO_VARCHAR(last_action_date)) lad, TRY_TO_DATE(TO_VARCHAR(expiration_date)) exd, TRY_TO_DATE(TO_VARCHAR(cert_issue_date)) cid
  FROM LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_FAA_AIRCRAFT_REGISTRY),
t AS (SELECT lad, COUNT(*) n FROM r WHERE status_code='V' GROUP BY 1 QUALIFY ROW_NUMBER() OVER (ORDER BY n DESC) <= 6)
SELECT (SELECT COUNT(*) FROM r) rows_n, (SELECT COUNT_IF(status_code='V') FROM r) valid_n,
  (SELECT COUNT_IF(status_code='V' AND YEAR(lad)=2023) FROM r) valid_lad_2023,
  (SELECT COUNT_IF(status_code='V' AND DATEDIFF('year', GREATEST(cid, lad), exd) >= 6) FROM r) valid_term_6y_plus,
  LISTAGG(lad||':'||n, ' | ') WITHIN GROUP (ORDER BY n DESC) top_lad_days
FROM t;

-- Notes
-- S10 failed at compile (nested aggregate) and is counted; S13 is the fixed rerun.
-- S20 was run after S21-S23; the labels keep the planned numbers. 33 statements in all.
