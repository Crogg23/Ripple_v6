-- deep-0: coverage deep pass, 2026-09-24. Python door, QUERY_TAG 'coverage-b-2026-09-24'.
-- Tables: CPSC_NEISS, NHTSA_COMPLAINTS, NHTSA_RECALLS, DOL_OSHA_INSPECTIONS, FAC_SINGLE_AUDIT.
-- Note: one extra statement ran before this log started: the first batch was sent as a single
-- string by a shared-scratchpad runner and failed at compile (syntax error, no data read).

-- S01 NEISS count + profile
SELECT COUNT(*) n, COUNT(DISTINCT case_number) cases, MIN(data_year) y0, MAX(data_year) y1,
       MIN(treatment_date) d0, MAX(treatment_date) d1, SUM(statistical_weight) wsum,
       COUNT_IF(statistical_weight IS NULL) w_null, COUNT(DISTINCT product_code_1) prods,
       COUNT_IF(YEAR(treatment_date) <> data_year) yr_mismatch
FROM LIBRARY_MARTS.CONSUMER_SAFETY.CONSUMER_SAFETY__FED_CPSC_NEISS;

-- S02 NEISS sample 5
SELECT case_number, treatment_date, data_year, age, sex_code, product_code_1, product_code_2, diagnosis_code, disposition_code, stratum, statistical_weight, LEFT(narrative,120) narr
FROM LIBRARY_MARTS.CONSUMER_SAFETY.CONSUMER_SAFETY__FED_CPSC_NEISS LIMIT 5;

-- S03 NHTSA complaints count + profile
SELECT COUNT(*) n, COUNT(DISTINCT cmplid) cmplids, COUNT(DISTINCT odino) odinos,
       MIN(date_received) r0, MAX(date_received) r1, MAX(deaths) dmax, MAX(injured) imax,
       COUNT_IF(deaths = 99) d99, COUNT_IF(injured = 99) i99, COUNT_IF(deaths > 0) d_rows,
       COUNT(DISTINCT IFF(deaths > 0, odino, NULL)) d_odinos, SYSTEM$TYPEOF(MAX(deaths)) dtype,
       COUNT_IF(model_year = 9999) my9999
FROM LIBRARY_MARTS.CONSUMER_SAFETY.CONSUMER_SAFETY__FED_NHTSA_COMPLAINTS;

-- S04 NHTSA complaints sample 5
SELECT cmplid, odino, mfr_name, make, model, model_year, component, crash, fire, injured, deaths, fail_date, date_received, LEFT(complaint_description,100) d
FROM LIBRARY_MARTS.CONSUMER_SAFETY.CONSUMER_SAFETY__FED_NHTSA_COMPLAINTS LIMIT 5;

-- S05 NHTSA recalls count + profile
SELECT COUNT(*) n, COUNT(DISTINCT record_id) recs, COUNT(DISTINCT campno) camps,
       MIN(notification_date) n0, MAX(notification_date) n1, MAX(potentially_affected_units) umax,
       SYSTEM$TYPEOF(MAX(potentially_affected_units)) utype, SYSTEM$TYPEOF(MAX(notification_date)) ntype,
       COUNT_IF(notification_date IS NULL) n_null, COUNT_IF(potentially_affected_units IS NULL) u_null
FROM LIBRARY_MARTS.CONSUMER_SAFETY.CONSUMER_SAFETY__FED_NHTSA_RECALLS;

-- S06 NHTSA recalls sample 5
SELECT record_id, campno, make, model, model_year, component, mfg_name, potentially_affected_units, notification_date, influenced_by, rcl_type_cd, begin_manufacture_date
FROM LIBRARY_MARTS.CONSUMER_SAFETY.CONSUMER_SAFETY__FED_NHTSA_RECALLS LIMIT 5;

-- S07 OSHA inspections count + profile
SELECT COUNT(*) n, COUNT(DISTINCT activity_nr) acts, MIN(open_date) o0, MAX(open_date) o1,
       COUNT_IF(close_case_date IS NULL) open_cases, SYSTEM$TYPEOF(MAX(open_date)) otype,
       COUNT(DISTINCT insp_type) insp_types, COUNT_IF(open_date >= '2015-01-01') since2015
FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_DOL_OSHA_INSPECTIONS;

-- S08 OSHA inspections sample 5
SELECT activity_nr, reporting_id, estab_name, site_city, site_state, naics_code, sic_code, owner_type, insp_type, insp_scope, safety_hlth, nr_in_estab, open_date, close_conf_date, close_case_date, why_no_insp
FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_DOL_OSHA_INSPECTIONS LIMIT 5;

-- S09 FAC single audit count + profile
SELECT COUNT(*) n, COUNT(DISTINCT report_id) reps, COUNT(DISTINCT auditee_ein) eins, MIN(audit_year) a0, MAX(audit_year) a1,
       SYSTEM$TYPEOF(MAX(total_amount_expended)) ttype,
       COUNT_IF(is_going_concern_included ILIKE 'y%') gc_yes, COUNT(DISTINCT is_going_concern_included) gc_vals,
       COUNT_IF(is_internal_control_material_weakness_disclosed ILIKE 'y%') mw_yes,
       COUNT_IF(is_material_noncompliance_disclosed ILIKE 'y%') mnc_yes,
       COUNT(DISTINCT data_source) srcs
FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_FAC_SINGLE_AUDIT;

-- S10 FAC sample 5
SELECT report_id, audit_year, auditee_ein, auditee_name, auditee_state, entity_type, is_going_concern_included gc, is_internal_control_material_weakness_disclosed mw, is_material_noncompliance_disclosed mnc, total_amount_expended, fy_start_date, data_source
FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_FAC_SINGLE_AUDIT LIMIT 5;

-- N01 NEISS weighted national estimate by product (any of 3 slots) and year, labels from code book; top risers 2019->2024/25
WITH t AS (SELECT data_year y, statistical_weight w, product_code_1 p1, product_code_2 p2, product_code_3 p3
           FROM LIBRARY_MARTS.CONSUMER_SAFETY.CONSUMER_SAFETY__FED_CPSC_NEISS WHERE data_year BETWEEN 2015 AND 2025),
p AS (SELECT y, w, p1 pc FROM t UNION ALL SELECT y, w, p2 FROM t WHERE p2 NOT IN ('0','') UNION ALL SELECT y, w, p3 FROM t WHERE p3 NOT IN ('0','')),
agg AS (SELECT TRY_TO_NUMBER(pc) pc, y, SUM(w) est, COUNT(*) n FROM p GROUP BY 1,2),
piv AS (SELECT pc, MIN(y) first_y,
   ROUND(SUM(IFF(y=2015,est,0))) e15, ROUND(SUM(IFF(y=2019,est,0))) e19, ROUND(SUM(IFF(y=2021,est,0))) e21,
   ROUND(SUM(IFF(y=2023,est,0))) e23, ROUND(SUM(IFF(y=2024,est,0))) e24, ROUND(SUM(IFF(y=2025,est,0))) e25,
   SUM(IFF(y=2019,n,0)) n19, SUM(IFF(y=2025,n,0)) n25 FROM agg GROUP BY pc),
codes AS (SELECT TRY_TO_NUMBER(TRIM(starting_value_for_format)) code, ANY_VALUE(format_value_label) label
          FROM LIBRARY_MARTS.EDUCATION.EDUCATION__FED_CPSC_NEISS_CODES WHERE format_name ILIKE '%PROD%' GROUP BY 1),
tot AS (SELECT -1 pc, MIN(y) first_y, ROUND(SUM(IFF(y=2015,w,0))) e15, ROUND(SUM(IFF(y=2019,w,0))) e19, ROUND(SUM(IFF(y=2021,w,0))) e21,
   ROUND(SUM(IFF(y=2023,w,0))) e23, ROUND(SUM(IFF(y=2024,w,0))) e24, ROUND(SUM(IFF(y=2025,w,0))) e25, COUNT_IF(y=2019) n19, COUNT_IF(y=2025) n25 FROM t)
SELECT * FROM (
 SELECT piv.*, c.label, ROUND(GREATEST(e24,e25)/NULLIF(e19,0),2) ratio, GREATEST(e24,e25)-e19 gain
 FROM piv LEFT JOIN codes c ON c.code = piv.pc
 WHERE GREATEST(e24,e25) >= 5000
 QUALIFY ROW_NUMBER() OVER (ORDER BY ratio DESC NULLS FIRST) <= 30 OR ROW_NUMBER() OVER (ORDER BY gain DESC) <= 15
 UNION ALL SELECT tot.*, 'ALL CASES (primary rows)', ROUND(GREATEST(e24,e25)/e19,2), GREATEST(e24,e25)-e19 FROM tot)
ORDER BY ratio DESC NULLS FIRST;

-- C01 NHTSA complaints: harm per complaint (ODINO), sentinel 99, complaint type, by received year band
WITH o AS (SELECT odino, MAX(deaths) d, MAX(injured) i, MIN(date_received) r, ANY_VALUE(cmpl_type) ct, COUNT(*) rows_
           FROM LIBRARY_MARTS.CONSUMER_SAFETY.CONSUMER_SAFETY__FED_NHTSA_COMPLAINTS GROUP BY odino)
SELECT ct, COUNT(*) complaints, COUNT_IF(d>0) fatal_cmpl, COUNT_IF(d>0 AND d<99) fatal_ok, SUM(IFF(d<99,d,0)) deaths_dedup,
       COUNT_IF(i>0) injury_cmpl, SUM(IFF(i<99,i,0)) injured_dedup, COUNT_IF(d=99 OR i=99) sentinel99,
       COUNT_IF(d>0 AND r<'2010-01-01') fatal_pre2010, COUNT_IF(d>0 AND r>='2015-01-01') fatal_2015on, AVG(rows_) avg_rows
FROM o GROUP BY ct ORDER BY complaints DESC;

-- R01 NHTSA recalls: once per campaign; rows per campaign; makers per campaign; raw vs dedup units by maker
WITH c AS (SELECT campno, mfg_name, MAX(potentially_affected_units) u, COUNT(*) rows_, MIN(notification_date) nd,
                  COUNT(DISTINCT potentially_affected_units) uvals
           FROM LIBRARY_MARTS.CONSUMER_SAFETY.CONSUMER_SAFETY__FED_NHTSA_RECALLS GROUP BY campno, mfg_name)
SELECT mfg_name, COUNT(*) campaigns, SUM(rows_) rows_, SUM(u*rows_) raw_units_sum, SUM(u) units_dedup,
       COUNT_IF(uvals>1) camps_units_vary, COUNT_IF(TRY_TO_NUMBER(LEFT(campno,2)) BETWEEN 15 AND 25) camps_2015_25,
       SUM(IFF(TRY_TO_NUMBER(LEFT(campno,2)) BETWEEN 15 AND 25, u, 0)) units_2015_25,
       (SELECT COUNT(*) FROM (SELECT campno FROM c GROUP BY campno HAVING COUNT(*)>1)) camps_multi_maker
FROM c GROUP BY mfg_name ORDER BY units_dedup DESC LIMIT 20;

-- O01 OSHA inspection type mix since 2015, open cases, days to close
SELECT insp_type, COUNT(*) n, COUNT_IF(open_date >= '2015-01-01') n2015,
       COUNT_IF(close_case_date IS NULL) open_all, COUNT_IF(close_case_date IS NULL AND open_date < '2020-01-01') open_pre2020,
       MEDIAN(IFF(open_date >= '2015-01-01', DATEDIFF('day', open_date, close_case_date), NULL)) med_days_close_2015,
       COUNT_IF(close_case_date < open_date) close_before_open, MIN(open_date) first_open, MAX(open_date) last_open
FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_DOL_OSHA_INSPECTIONS GROUP BY insp_type ORDER BY n DESC;

-- F01 FAC: flag values, duplicate EIN-years, entity-type rates (denominator = audit reports)
SELECT entity_type, COUNT(*) reports, COUNT(DISTINCT auditee_ein) eins,
       COUNT_IF(is_going_concern_included='Yes') gc, COUNT_IF(is_internal_control_material_weakness_disclosed='Yes') mw,
       COUNT_IF(is_material_noncompliance_disclosed='Yes') mnc, COUNT_IF(is_going_concern_included NOT IN ('Yes','No')) gc_other,
       ROUND(100*COUNT_IF(is_internal_control_material_weakness_disclosed='Yes')/COUNT(*),1) mw_pct,
       ROUND(100*COUNT_IF(is_going_concern_included='Yes')/COUNT(*),2) gc_pct,
       ROUND(SUM(total_amount_expended)/1e9,1) exp_bn, MEDIAN(total_amount_expended) med_exp,
       COUNT(*) - COUNT(DISTINCT auditee_ein||'|'||audit_year) dup_ein_year,
       COUNT_IF(total_amount_expended <= 0) nonpos
FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_FAC_SINGLE_AUDIT GROUP BY ROLLUP(entity_type) ORDER BY reports DESC;

-- N02 NEISS narrative keyword families, weighted national estimate by year; narrative fill rate
SELECT data_year, COUNT(*) cases, COUNT_IF(narrative IS NOT NULL AND TRIM(narrative)<>'') narr_filled,
 ROUND(SUM(IFF(narrative ILIKE ANY ('%E-BIKE%','%EBIKE%','%ELECTRIC BIKE%','%ELECTRIC BICYCLE%','%E BIKE%'), statistical_weight,0))) ebike,
 ROUND(SUM(IFF(narrative ILIKE ANY ('%E-SCOOTER%','%ESCOOTER%','%ELECTRIC SCOOTER%','%MOTORIZED SCOOTER%','%POWERED SCOOTER%','%ELEC SCOOTER%'), statistical_weight,0))) escooter,
 ROUND(SUM(IFF(narrative ILIKE '%MAGNET%', statistical_weight,0))) magnet, COUNT_IF(narrative ILIKE '%MAGNET%') magnet_n,
 ROUND(SUM(IFF(narrative ILIKE ANY ('%WATER BEAD%','%WATERBEAD%','%ORBEEZ%','%GEL BEAD%','%WATER BALL%'), statistical_weight,0))) waterbead,
 COUNT_IF(narrative ILIKE ANY ('%WATER BEAD%','%WATERBEAD%','%ORBEEZ%','%GEL BEAD%','%WATER BALL%')) waterbead_n,
 ROUND(SUM(IFF(narrative ILIKE '%GUMM%', statistical_weight,0))) gummy, COUNT_IF(narrative ILIKE '%GUMM%') gummy_n,
 ROUND(SUM(IFF(narrative ILIKE ANY ('%EDIBLE%','% THC%','%MARIJUANA%','%CANNABIS%'), statistical_weight,0))) cannabis,
 COUNT_IF(narrative ILIKE ANY ('%EDIBLE%','% THC%','%MARIJUANA%','%CANNABIS%')) cannabis_n,
 ROUND(SUM(IFF(narrative ILIKE ANY ('%UTV%','%SIDE BY SIDE%','%SIDE-BY-SIDE%'), statistical_weight,0))) utv,
 ROUND(SUM(IFF(narrative ILIKE ANY ('%BUTTON BATTER%','%COIN BATTER%','%DISC BATTER%','%BUTTON CELL%'), statistical_weight,0))) button_batt,
 ROUND(SUM(IFF(narrative ILIKE '%LITHIUM%', statistical_weight,0))) lithium
FROM LIBRARY_MARTS.CONSUMER_SAFETY.CONSUMER_SAFETY__FED_CPSC_NEISS WHERE data_year BETWEEN 2015 AND 2025 GROUP BY 1 ORDER BY 1;

-- N03 NEISS who gets hurt on the code-stable risers, 2019 vs 2025, with two sample narratives
SELECT product_code_1 pc, data_year y, ROUND(SUM(statistical_weight)) est, COUNT(*) n,
  ROUND(100*SUM(IFF(age < 18 OR age >= 200, statistical_weight, 0))/SUM(statistical_weight),1) pct_child,
  ROUND(100*SUM(IFF(sex_code='1', statistical_weight, 0))/SUM(statistical_weight),1) pct_male,
  ROUND(100*SUM(IFF(disposition_code IN ('4','5'), statistical_weight, 0))/SUM(statistical_weight),1) pct_admit_obs,
  SUM(IFF(disposition_code='8',1,0)) deaths_n, MEDIAN(IFF(age BETWEEN 1 AND 120, age, NULL)) med_age,
  LEFT(MIN(IFF(TRIM(narrative)<>'', narrative, NULL)),110) narr_a, LEFT(MAX(IFF(TRIM(narrative)<>'', narrative, NULL)),110) narr_b
FROM LIBRARY_MARTS.CONSUMER_SAFETY.CONSUMER_SAFETY__FED_CPSC_NEISS
WHERE product_code_1 IN ('5022','5045','5046','5044','1107','1062','884','1381','1807') AND data_year IN (2019,2021,2025)
GROUP BY 1,2 ORDER BY 1,2;

-- C02 NHTSA harm complaints filed before a recall on the same make/model/year/component head, per campaign
WITH cm AS (
  SELECT odino, UPPER(TRIM(make)) mk, UPPER(TRIM(model)) md, model_year my,
         TRIM(SPLIT_PART(SPLIT_PART(component, ':', 1), ',', 1)) comp,
         MAX(IFF(deaths < 99, deaths, 0)) d, MAX(IFF(injured < 99, injured, 0)) i, MIN(date_received) r
  FROM LIBRARY_MARTS.CONSUMER_SAFETY.CONSUMER_SAFETY__FED_NHTSA_COMPLAINTS
  WHERE (deaths > 0 OR injured > 0) AND model_year BETWEEN 1980 AND 2027
  GROUP BY 1,2,3,4,5),
rc AS (
  SELECT campno, ANY_VALUE(mfg_name) mfg, UPPER(TRIM(make)) mk, UPPER(TRIM(model)) md, model_year my,
         TRIM(SPLIT_PART(SPLIT_PART(component, ':', 1), ',', 1)) comp,
         MIN(notification_date) nd, MAX(potentially_affected_units) u, MAX(influenced_by) inf
  FROM LIBRARY_MARTS.CONSUMER_SAFETY.CONSUMER_SAFETY__FED_NHTSA_RECALLS
  WHERE notification_date >= '1966-01-01' AND rcl_type_cd = 'V'
  GROUP BY campno, 3, 4, 5, 6),
j AS (SELECT DISTINCT rc.campno, rc.mfg, rc.comp, rc.nd, rc.u, rc.inf, rc.mk, rc.md, rc.my, cm.odino, cm.d, cm.i, cm.r
      FROM rc JOIN cm ON cm.mk = rc.mk AND cm.md = rc.md AND cm.my = rc.my AND cm.comp = rc.comp AND cm.r < rc.nd),
jo AS (SELECT campno, odino, MAX(d) d, MAX(i) i, MIN(r) r FROM j GROUP BY 1,2),
per AS (SELECT campno, COUNT(*) harm_before, COUNT_IF(d > 0) fatal_before, SUM(d) deaths_before, SUM(i) injured_before,
               MIN(IFF(d > 0, r, NULL)) first_fatal, MIN(r) first_harm FROM jo GROUP BY 1),
meta AS (SELECT campno, ANY_VALUE(mfg) mfg, ANY_VALUE(comp) comp, MIN(mk) mk, LEFT(LISTAGG(DISTINCT md, ','),40) models,
                MIN(my) my0, MAX(my) my1, MIN(nd) nd, MAX(u) u, MAX(inf) inf FROM rc GROUP BY 1)
SELECT m.campno, m.mfg, m.mk, m.models, m.my0, m.my1, m.comp, m.nd recall_notice, m.u units, m.inf,
       p.harm_before, p.fatal_before, p.deaths_before, p.injured_before, p.first_fatal, p.first_harm,
       ROUND(DATEDIFF('day', p.first_fatal, m.nd)/365.25,1) yrs_fatal_lead
FROM per p JOIN meta m USING (campno)
ORDER BY p.fatal_before DESC, p.deaths_before DESC LIMIT 30;

-- R02 NHTSA recalls by maker key (first word), once per campaign; biggest row-repeater; same model-year-component recalled 3+ times
WITH r AS (SELECT campno, REGEXP_SUBSTR(UPPER(mfg_name), '^[A-Z]+') mkey, UPPER(TRIM(make)) mk, UPPER(TRIM(model)) md, model_year my,
                  TRIM(SPLIT_PART(SPLIT_PART(component, ':', 1), ',', 1)) comp, potentially_affected_units u, notification_date nd
           FROM LIBRARY_MARTS.CONSUMER_SAFETY.CONSUMER_SAFETY__FED_NHTSA_RECALLS WHERE rcl_type_cd = 'V'),
c AS (SELECT mkey, campno, MAX(u) u, COUNT(*) rows_ FROM r GROUP BY 1,2),
cmb AS (SELECT mkey, mk, md, my, comp, COUNT(DISTINCT campno) ncamp FROM r WHERE my BETWEEN 1980 AND 2027 GROUP BY 1,2,3,4,5),
ck AS (SELECT mkey, COUNT(*) combos, COUNT_IF(ncamp >= 3) combos_3plus, MAX(ncamp) max_camp_one_combo FROM cmb GROUP BY 1)
SELECT c.mkey, COUNT(*) campaigns, SUM(u) units_once, SUM(u*rows_) units_rowsum, MAX(rows_) max_rows_one_camp,
       MAX_BY(campno, rows_) camp_most_rows, MAX_BY(u, rows_) units_that_camp,
       ck.combos, ck.combos_3plus, ROUND(100*ck.combos_3plus/ck.combos,1) pct_3plus, ck.max_camp_one_combo
FROM c JOIN ck USING (mkey) GROUP BY c.mkey, ck.combos, ck.combos_3plus, ck.max_camp_one_combo
ORDER BY units_rowsum DESC LIMIT 25;

-- O02 OSHA employers with the most fatality/catastrophe inspections (types A, M) since 2015, normalized names
WITH o AS (SELECT activity_nr, insp_type, open_date, close_case_date, site_state, site_city, site_zip, naics_code,
   TRIM(REGEXP_REPLACE(REGEXP_REPLACE(UPPER(estab_name), '[^A-Z0-9 ]', ''), '( INC| LLC| CORP| CORPORATION| CO| COMPANY| LP| LTD)+ *$', '')) k
   FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_DOL_OSHA_INSPECTIONS WHERE open_date >= '2015-01-01')
SELECT k, COUNT_IF(insp_type IN ('A','M')) fat_insp, COUNT(*) all_insp,
       COUNT(DISTINCT IFF(insp_type IN ('A','M'), site_city||site_state, NULL)) fat_sites, COUNT(DISTINCT site_state) states,
       COUNT_IF(insp_type IN ('A','M') AND close_case_date IS NULL) fat_open,
       COUNT_IF(insp_type IN ('A','M') AND close_case_date IS NULL AND open_date < '2022-01-01') fat_open_pre2022,
       MEDIAN(IFF(insp_type IN ('A','M'), DATEDIFF('day', open_date, close_case_date), NULL)) med_days_fat,
       ROUND(100*COUNT_IF(insp_type IN ('A','M'))/COUNT(*),1) pct_fat, MODE(naics_code) naics_mode
FROM o GROUP BY k ORDER BY fat_insp DESC LIMIT 30;

-- F02 FAC: auditees (not state) with going-concern doubt in 3+ audit years, ranked by federal $ spent in those years
WITH ey AS (SELECT auditee_ein ein, audit_year y, MAX(auditee_name) nm, MAX(entity_type) et, MAX(auditee_state) st,
   MAX(IFF(is_going_concern_included='Yes',1,0)) gc, MAX(IFF(is_internal_control_material_weakness_disclosed='Yes',1,0)) mw,
   MAX(IFF(is_material_noncompliance_disclosed='Yes',1,0)) mnc, MAX(total_amount_expended) ex, COUNT(DISTINCT UPPER(auditee_name)) names
   FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_FAC_SINGLE_AUDIT WHERE entity_type <> 'state' GROUP BY 1,2),
e AS (SELECT ein, MAX(nm) nm, MAX(et) et, MAX(st) st, COUNT(*) yrs, MIN(y) y0, MAX(y) y1, SUM(gc) gc_yrs, SUM(mw) mw_yrs, SUM(mnc) mnc_yrs,
   ROUND(SUM(IFF(gc=1, ex, 0))/1e6,1) exp_gc_yrs_m, ROUND(SUM(ex)/1e6,1) exp_all_m, ROUND(MAX_BY(ex, y)/1e6,1) exp_last_m,
   MAX(names) max_names, MIN(IFF(gc=1,y,NULL)) first_gc
   FROM ey GROUP BY ein)
SELECT *, (SELECT COUNT(*) FROM e WHERE gc_yrs >= 3) n_gc3, (SELECT COUNT(*) FROM e WHERE yrs >= 3) n_yrs3
FROM e WHERE gc_yrs >= 3 ORDER BY exp_gc_yrs_m DESC LIMIT 25;

-- N04 NEISS predecessor codes: products (any slot) that lost 40%+ between 2019->2021 or 2023->2024, est 5,000+, plus micromobility families
WITH t AS (SELECT data_year y, statistical_weight w, product_code_1 p1, product_code_2 p2, product_code_3 p3
           FROM LIBRARY_MARTS.CONSUMER_SAFETY.CONSUMER_SAFETY__FED_CPSC_NEISS WHERE data_year BETWEEN 2017 AND 2025),
p AS (SELECT y, w, p1 pc FROM t UNION ALL SELECT y, w, p2 FROM t WHERE p2 NOT IN ('0','') UNION ALL SELECT y, w, p3 FROM t WHERE p3 NOT IN ('0','')),
piv AS (SELECT TRY_TO_NUMBER(pc) pc, ROUND(SUM(IFF(y=2017,w,0))) e17, ROUND(SUM(IFF(y=2019,w,0))) e19, ROUND(SUM(IFF(y=2020,w,0))) e20, ROUND(SUM(IFF(y=2021,w,0))) e21,
   ROUND(SUM(IFF(y=2023,w,0))) e23, ROUND(SUM(IFF(y=2024,w,0))) e24, ROUND(SUM(IFF(y=2025,w,0))) e25, MAX(y) last_y FROM p GROUP BY 1),
codes AS (SELECT TRY_TO_NUMBER(TRIM(starting_value_for_format)) code, ANY_VALUE(format_value_label) label
          FROM LIBRARY_MARTS.EDUCATION.EDUCATION__FED_CPSC_NEISS_CODES WHERE format_name ILIKE '%PROD%' GROUP BY 1)
SELECT piv.*, c.label FROM piv LEFT JOIN codes c ON c.code = piv.pc
WHERE (e19 >= 5000 AND e21 < 0.6*e19) OR (e23 >= 5000 AND e24 < 0.6*e23)
   OR c.label ILIKE ANY ('%SCOOTER%','%BICYCLE%','%MOPED%','%HOVERBOARD%','%SKATEBOARD%','%CYCLE%','%ALL-TERRAIN%','%UTILITY VEH%','%GOLF CART%')
ORDER BY pc;

-- C03 NHTSA fatal complaints by make/model/component head, split by whether that model year ever got a recall on that component; join sanity
WITH cm AS (
  SELECT odino, UPPER(TRIM(make)) mk, UPPER(TRIM(model)) md, model_year my,
         TRIM(SPLIT_PART(SPLIT_PART(component, ':', 1), ',', 1)) comp, MAX(deaths) d, MIN(date_received) r
  FROM LIBRARY_MARTS.CONSUMER_SAFETY.CONSUMER_SAFETY__FED_NHTSA_COMPLAINTS
  WHERE deaths > 0 AND deaths < 99 AND model_year BETWEEN 1980 AND 2027 GROUP BY 1,2,3,4,5),
rc AS (SELECT UPPER(TRIM(make)) mk, UPPER(TRIM(model)) md, model_year my, TRIM(SPLIT_PART(SPLIT_PART(component, ':', 1), ',', 1)) comp,
              MIN(notification_date) first_recall
       FROM LIBRARY_MARTS.CONSUMER_SAFETY.CONSUMER_SAFETY__FED_NHTSA_RECALLS WHERE rcl_type_cd = 'V' AND notification_date >= '1966-01-01' GROUP BY 1,2,3,4),
rv AS (SELECT DISTINCT mk, md, my FROM rc),
x AS (SELECT cm.*, rc.first_recall, (rv.mk IS NOT NULL) veh_any_recall
      FROM cm LEFT JOIN rc ON rc.mk=cm.mk AND rc.md=cm.md AND rc.my=cm.my AND rc.comp=cm.comp
              LEFT JOIN rv ON rv.mk=cm.mk AND rv.md=cm.md AND rv.my=cm.my),
g AS (SELECT mk, md, comp, COUNT(DISTINCT odino) fatal_cmpl, COUNT(DISTINCT IFF(first_recall IS NULL, odino, NULL)) fatal_no_comp_recall,
             SUM(IFF(first_recall IS NULL, d, 0)) deaths_no_recall, MIN(my) my0, MAX(my) my1,
             MIN(IFF(first_recall IS NULL, r, NULL)) first_r, MAX(IFF(first_recall IS NULL, r, NULL)) last_r,
             COUNT(DISTINCT IFF(first_recall IS NULL, my, NULL)) yrs_no_recall
      FROM x GROUP BY 1,2,3)
SELECT * FROM (
  SELECT g.*, NULL sanity FROM g WHERE comp NOT IN ('UNKNOWN OR OTHER')
  QUALIFY ROW_NUMBER() OVER (ORDER BY fatal_no_comp_recall DESC, deaths_no_recall DESC) <= 25
  UNION ALL
  SELECT 'ALL', 'ALL', 'ALL', COUNT(DISTINCT odino), COUNT(DISTINCT IFF(first_recall IS NULL, odino, NULL)), NULL, NULL, NULL, NULL, NULL, NULL,
         ROUND(100*COUNT(DISTINCT IFF(veh_any_recall, odino, NULL))/COUNT(DISTINCT odino),1) FROM x)
ORDER BY fatal_no_comp_recall DESC;

-- O03 OSHA top fatality/catastrophe employers split by period and California; plus A/M inspections by state
WITH o AS (SELECT insp_type, open_date, close_case_date, site_state,
   TRIM(REGEXP_REPLACE(REGEXP_REPLACE(UPPER(estab_name), '[^A-Z0-9 ]', ''), '( INC| LLC| CORP| CORPORATION| CO| COMPANY| LP| LTD)+ *$', '')) k
   FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_DOL_OSHA_INSPECTIONS WHERE open_date >= '2015-01-01' AND insp_type IN ('A','M'))
SELECT * FROM (
 SELECT k, COUNT(*) fat, COUNT_IF(YEAR(open_date) BETWEEN 2015 AND 2019) f15_19, COUNT_IF(YEAR(open_date) IN (2020,2021)) f20_21,
        COUNT_IF(YEAR(open_date) >= 2022) f22_26, COUNT_IF(site_state='CA') f_ca, COUNT_IF(insp_type='A') a_type, COUNT_IF(insp_type='M') m_type,
        COUNT_IF(close_case_date IS NULL) still_open
 FROM o WHERE k IN ('UNITED PARCEL SERVICE','UPS','SIERRA PACIFIC INDUSTRIES','WALMART','WALMART STORES','SAFEWAY','FOSTER POULTRY FARMS','COSTCO WHOLESALE',
   'TARGET','TESLA','PACIFIC GAS AND ELECTRIC','FEDERAL EXPRESS','KAISER FOUNDATION HOSPITALS','SOUTHERN CALIFORNIA EDISON','TIMBERWORKS CONSTRUCTION',
   'US POSTAL SERVICE','AEROTEK','INTERNATIONAL PAPER','UNITED PRODUCTION FRAMING','AMAZONCOM SERVICES','HOME DEPOT USA','ESPARZA ENTERPRISES')
 GROUP BY k
 UNION ALL
 SELECT 'STATE ' || site_state, COUNT(*), COUNT_IF(YEAR(open_date) BETWEEN 2015 AND 2019), COUNT_IF(YEAR(open_date) IN (2020,2021)),
        COUNT_IF(YEAR(open_date) >= 2022), NULL, COUNT_IF(insp_type='A'), COUNT_IF(insp_type='M'), COUNT_IF(close_case_date IS NULL)
 FROM o GROUP BY site_state QUALIFY ROW_NUMBER() OVER (ORDER BY COUNT(*) DESC) <= 12)
ORDER BY fat DESC;

-- F03 FAC: material-weakness streaks of 5+ straight audit years (not state), ranked by average federal $/yr; peer rate by entity type
WITH ey AS (SELECT auditee_ein ein, audit_year y, MAX(auditee_name) nm, MAX(entity_type) et, MAX(auditee_state) st,
   MAX(IFF(is_going_concern_included='Yes',1,0)) gc, MAX(IFF(is_internal_control_material_weakness_disclosed='Yes',1,0)) mw,
   MAX(IFF(is_material_noncompliance_disclosed='Yes',1,0)) mnc, MAX(total_amount_expended) ex, COUNT(DISTINCT UPPER(auditee_name)) names
   FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_FAC_SINGLE_AUDIT WHERE entity_type <> 'state' GROUP BY 1,2),
isl AS (SELECT ein, y - ROW_NUMBER() OVER (PARTITION BY ein ORDER BY y) g FROM ey WHERE mw = 1),
sk AS (SELECT ein, MAX(c) streak FROM (SELECT ein, g, COUNT(*) c FROM isl GROUP BY 1,2) GROUP BY 1),
e AS (SELECT ey.ein, MAX(nm) nm, MAX(et) et, MAX(st) st, COUNT(*) yrs, MIN(y) y0, MAX(y) y1, SUM(mw) mw_yrs, SUM(mnc) mnc_yrs, SUM(gc) gc_yrs,
        COALESCE(MAX(sk.streak),0) streak, ROUND(AVG(ex)/1e6,1) avg_exp_m, ROUND(SUM(ex)/1e6,1) sum_exp_m, ROUND(MAX_BY(ex,y)/1e6,1) last_exp_m, MAX(names) max_names
      FROM ey LEFT JOIN sk ON sk.ein = ey.ein GROUP BY ey.ein),
w AS (SELECT e.*, COUNT_IF(yrs >= 5) OVER (PARTITION BY et) et_eins_5yrs, COUNT_IF(streak >= 5) OVER (PARTITION BY et) et_streak5,
             COUNT_IF(streak >= 5) OVER () all_streak5, COUNT_IF(yrs >= 5) OVER () all_eins_5yrs FROM e)
SELECT * FROM w WHERE streak >= 5 ORDER BY avg_exp_m DESC LIMIT 30;

-- F04 FAC flag sanity by audit year and source system (rates per audit report)
SELECT audit_year, data_source, COUNT(*) reports, ROUND(100*COUNT_IF(is_going_concern_included='Yes')/COUNT(*),2) gc_pct,
       ROUND(100*COUNT_IF(is_internal_control_material_weakness_disclosed='Yes')/COUNT(*),2) mw_pct,
       ROUND(100*COUNT_IF(is_material_noncompliance_disclosed='Yes')/COUNT(*),2) mnc_pct,
       COUNT_IF(is_going_concern_included NOT IN ('Yes','No') OR is_going_concern_included IS NULL) gc_other,
       ROUND(SUM(total_amount_expended)/1e9,1) exp_bn
FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_FAC_SINGLE_AUDIT GROUP BY 1,2 ORDER BY 1,2;

-- N05 NEISS sample-design check: cases, weighted estimate, average weight by hospital stratum and year
SELECT data_year, stratum, COUNT(*) cases, ROUND(SUM(statistical_weight)) est, ROUND(AVG(statistical_weight),2) avg_w,
       ROUND(SUM(IFF(product_code_1 = '1807' OR product_code_2 = '1807' OR product_code_3 = '1807', statistical_weight, 0))) floors_est
FROM LIBRARY_MARTS.CONSUMER_SAFETY.CONSUMER_SAFETY__FED_CPSC_NEISS WHERE data_year IN (2019, 2022, 2023, 2024, 2025)
GROUP BY 1,2 ORDER BY 2,1;

-- C04 NHTSA spot-check: fatal complaints behind three leads (Lincoln MKS engine, Tesla Model S suspension, Freightliner Cascadia brakes before recall)
SELECT UPPER(make) mk, UPPER(model) md, model_year, component, odino, deaths, injured, crash, fire, date_received, cmpl_type, LEFT(complaint_description, 230) txt
FROM LIBRARY_MARTS.CONSUMER_SAFETY.CONSUMER_SAFETY__FED_NHTSA_COMPLAINTS
WHERE deaths > 0 AND deaths < 99 AND (
      (UPPER(make) = 'LINCOLN' AND UPPER(model) = 'MKS' AND component ILIKE 'ENGINE%')
   OR (UPPER(make) = 'TESLA' AND UPPER(model) = 'MODEL S' AND component ILIKE 'SUSPENSION%')
   OR (UPPER(make) = 'FREIGHTLINER' AND UPPER(model) = 'CASCADIA' AND component ILIKE 'SERVICE BRAKES%' AND date_received < '2023-10-16'))
QUALIFY ROW_NUMBER() OVER (PARTITION BY odino ORDER BY cmplid) = 1
ORDER BY mk, date_received;

-- R03 NHTSA recalls: the model-year-component combos recalled in the most separate campaigns
WITH r AS (SELECT campno, mfg_name, UPPER(TRIM(make)) mk, UPPER(TRIM(model)) md, model_year my,
                  TRIM(SPLIT_PART(SPLIT_PART(component, ':', 1), ',', 1)) comp, notification_date nd
           FROM LIBRARY_MARTS.CONSUMER_SAFETY.CONSUMER_SAFETY__FED_NHTSA_RECALLS WHERE rcl_type_cd = 'V' AND model_year BETWEEN 1980 AND 2027)
SELECT mk, md, my, comp, COUNT(DISTINCT campno) camps, ANY_VALUE(mfg_name) mfg, MIN(nd) first_nd, MAX(nd) last_nd,
       LEFT(LISTAGG(DISTINCT campno, ' ') WITHIN GROUP (ORDER BY campno), 120) camp_list
FROM r GROUP BY 1,2,3,4 ORDER BY camps DESC, my DESC LIMIT 20;

-- O04 OSHA inspections opened 2015-2020 that still have no close date, by employer (any inspection type)
WITH o AS (SELECT insp_type, open_date, close_case_date, site_state, case_mod_date,
   TRIM(REGEXP_REPLACE(REGEXP_REPLACE(UPPER(estab_name), '[^A-Z0-9 ]', ''), '( INC| LLC| CORP| CORPORATION| CO| COMPANY| LP| LTD)+ *$', '')) k
   FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_DOL_OSHA_INSPECTIONS WHERE open_date BETWEEN '2015-01-01' AND '2020-12-31')
SELECT k, COUNT_IF(close_case_date IS NULL) open_5yr_plus, COUNT(*) insp_2015_20, ROUND(100*COUNT_IF(close_case_date IS NULL)/COUNT(*),1) pct_open,
       COUNT_IF(close_case_date IS NULL AND insp_type IN ('A','M')) open_fat, LISTAGG(DISTINCT IFF(close_case_date IS NULL, site_state, NULL), ',') open_states,
       MAX(IFF(close_case_date IS NULL, case_mod_date, NULL)) last_mod_open,
       SUM(COUNT_IF(close_case_date IS NULL)) OVER () all_open_5yr, SUM(COUNT(*)) OVER () all_insp_2015_20
FROM o GROUP BY k ORDER BY open_5yr_plus DESC LIMIT 20;

-- F05 FAC tribes: going-concern and noncompliance years per tribe vs tribal peers; plus 'local' rows that are states
WITH ey AS (SELECT auditee_ein ein, audit_year y, MAX(auditee_name) nm, MAX(auditee_state) st,
   MAX(IFF(is_going_concern_included='Yes',1,0)) gc, MAX(IFF(is_internal_control_material_weakness_disclosed='Yes',1,0)) mw,
   MAX(IFF(is_material_noncompliance_disclosed='Yes',1,0)) mnc, MAX(total_amount_expended) ex
   FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_FAC_SINGLE_AUDIT WHERE entity_type = 'tribal' GROUP BY 1,2),
e AS (SELECT ein, MAX(nm) nm, MAX(st) st, COUNT(*) yrs, MIN(y) y0, MAX(y) y1, SUM(gc) gc_yrs, SUM(mw) mw_yrs, SUM(mnc) mnc_yrs,
             ROUND(SUM(ex)/1e6,1) sum_exp_m, ROUND(MAX_BY(ex, y)/1e6,1) last_exp_m FROM ey GROUP BY ein)
SELECT e.*, COUNT_IF(yrs >= 3) OVER () tribes_3yrs, COUNT_IF(gc_yrs >= 3) OVER () tribes_gc3, COUNT_IF(yrs >= 5 AND gc_yrs + mnc_yrs >= 10) OVER () tribes_gc_mnc_10,
       (SELECT COUNT(*) FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_FAC_SINGLE_AUDIT WHERE entity_type = 'local' AND auditee_name ILIKE 'STATE OF %') local_named_state
FROM e QUALIFY ROW_NUMBER() OVER (ORDER BY gc_yrs + mnc_yrs DESC, sum_exp_m DESC) <= 15
ORDER BY gc_yrs + mnc_yrs DESC, sum_exp_m DESC;

-- F06 FAC sample check on the two lead auditees: every row, year by year (flags, dollars, auditor, source)
SELECT auditee_ein, auditee_name, audit_year, fy_end_date, total_amount_expended, is_going_concern_included gc,
       is_internal_control_material_weakness_disclosed mw, is_material_noncompliance_disclosed mnc, gaap_results,
       auditor_firm_name, data_source, report_id
FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_FAC_SINGLE_AUDIT
WHERE auditee_ein IN ('460222351', '272053273')
ORDER BY auditee_ein, audit_year;

-- Statement count: 32 logged above + 1 failed compile before this log = 33 of 35.
-- The failed compile was sent through another agent's runner (shared scratchpad run.py),
-- so its text also landed in deep-4.sql as a block starting "-- Q:S01 NEISS count + profile" with no data read.
