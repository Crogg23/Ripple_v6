-- S14 Prop 65 x TRI 2023 on CAS: land rate and pounds, split by TRI's own carcinogen flag (rerun of S12; total_releases is already FLOAT)
WITH p65 AS (SELECT TRIM(cas_no) cas, MIN(chemical) p65_name,
         BOOLOR_AGG(type_of_toxicity ILIKE '%cancer%') p65_cancer,
         BOOLOR_AGG(type_of_toxicity ILIKE '%developmental%' OR type_of_toxicity ILIKE '%male%') p65_repro,
         MIN(date_listed) first_listed
       FROM LIBRARY_MARTS.HEALTH.HEALTH__ST_OEHHA_PROPOSITION_65_LIST WHERE cas_no NOT LIKE '--%' AND NULLIF(TRIM(cas_no),'') IS NOT NULL AND date_listed IS NOT NULL GROUP BY 1),
tri AS (SELECT TRIM(c_40_cas) cas, MAX(c_37_chemical) tri_name, MAX(c_46_carcinogen) tri_carc,
               COUNT(*) forms, COUNT(DISTINCT c_2_trifd) facs, SUM(c_107_total_releases::float) lbs,
               SUM(IFF(c_8_st='CA', c_107_total_releases::float, 0)) ca_lbs
        FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_BASIC_2023 WHERE c_50_unit_of_measure ILIKE 'Pounds' GROUP BY 1)
SELECT tri.tri_carc, (p65.cas IS NOT NULL) on_p65, COALESCE(p65.p65_cancer,FALSE) p65_cancer, COALESCE(p65.p65_repro,FALSE) p65_repro,
       COUNT(*) chems, SUM(forms) forms, ROUND(SUM(lbs)) lbs, ROUND(SUM(ca_lbs)) ca_lbs,
       ARRAY_SLICE(ARRAY_AGG(tri_name) WITHIN GROUP (ORDER BY lbs DESC),0,8) top_chems
FROM tri LEFT JOIN p65 ON p65.cas = tri.cas
GROUP BY ROLLUP(1,2,3,4) ORDER BY 1,2,3,4;

-- S15 Prop 65 x TRI 2023: which Prop 65 chemicals carry the pounds; TRI carcinogen flag next to the Prop 65 listing (rerun of S13)
WITH p65 AS (SELECT TRIM(cas_no) cas, MIN(chemical) p65_name,
         BOOLOR_AGG(type_of_toxicity ILIKE '%cancer%') p65_cancer,
         BOOLOR_AGG(type_of_toxicity ILIKE '%developmental%' OR type_of_toxicity ILIKE '%male%') p65_repro,
         MIN(date_listed) first_listed
       FROM LIBRARY_MARTS.HEALTH.HEALTH__ST_OEHHA_PROPOSITION_65_LIST WHERE cas_no NOT LIKE '--%' AND NULLIF(TRIM(cas_no),'') IS NOT NULL AND date_listed IS NOT NULL GROUP BY 1),
tri AS (SELECT TRIM(c_40_cas) cas, MAX(c_37_chemical) tri_name, MAX(c_46_carcinogen) tri_carc, MAX(c_43_classification) cls,
               COUNT(DISTINCT c_2_trifd) facs, SUM(c_107_total_releases::float) lbs,
               SUM(IFF(c_8_st='CA', c_107_total_releases::float, 0)) ca_lbs,
               COUNT(DISTINCT IFF(c_8_st='CA', c_2_trifd, NULL)) ca_facs
        FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_BASIC_2023 WHERE c_50_unit_of_measure ILIKE 'Pounds' GROUP BY 1)
SELECT tri.cas, tri_name, p65_name, tri_carc, p65_cancer, p65_repro, first_listed, facs, ROUND(lbs) lbs, ca_facs, ROUND(ca_lbs) ca_lbs
FROM tri JOIN p65 ON p65.cas = tri.cas
ORDER BY lbs DESC LIMIT 40;

-- S16 DPD drug: which days carry the bulk last-update stamps
SELECT last_update_date d, COUNT(*) n, COUNT_IF(drug_class='Human') human, MIN(TRY_TO_NUMBER(drug_code)) code_min, MAX(TRY_TO_NUMBER(drug_code)) code_max
FROM LIBRARY_MARTS.HEALTH.HEALTH__INTL_HEALTHCANADA_DPD_DRUG GROUP BY 1 ORDER BY n DESC LIMIT 10;

-- S17 UDS: patients per weekly open site-hour, joined to the site roster on grant number, ranked inside each state
WITH c AS (SELECT bhcmisid, TRY_TO_NUMBER(REPLACE(T3A_L39_CA,',','')) + TRY_TO_NUMBER(REPLACE(T3A_L39_CB,',','')) tot FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_UDS_TABLE3A_PATIENTS),
i AS (SELECT bhcmisid, grantnumber, healthcentername, healthcentercity, healthcenterstate st, urbanruralflag ur FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_UDS_HEALTH_CENTER_INFO),
s AS (SELECT health_center_number g, COUNT(*) sites, SUM(TRY_TO_NUMBER(operating_hours_per_week::string)) hrs,
             COUNT_IF(location_type_description ILIKE '%mobile%') mobile, COUNT_IF(location_setting_description ILIKE '%school%') school,
             COUNT_IF(site_type_description ILIKE '%admin%' AND site_type_description NOT ILIKE '%service%') admin_only,
             ARRAY_AGG(DISTINCT health_center_type) types
      FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_UDS_SERVICE_DELIVERY_SITES GROUP BY 1),
j AS (SELECT i.*, c.tot, s.sites, s.hrs, s.mobile, s.school, s.admin_only, s.types, c.tot/NULLIF(s.hrs,0) per_hr
      FROM i JOIN c USING (bhcmisid) LEFT JOIN s ON s.g = i.grantnumber),
r AS (SELECT j.*, COUNT(*) OVER () n_all, COUNT(sites) OVER () n_landed, MEDIAN(per_hr) OVER () nat_med,
             MEDIAN(per_hr) OVER (PARTITION BY st) st_med, COUNT(per_hr) OVER (PARTITION BY st) st_n,
             per_hr / NULLIF(MEDIAN(per_hr) OVER (PARTITION BY st),0) x_state
      FROM j)
SELECT bhcmisid, healthcentername, healthcentercity, st, ur, tot, sites, hrs, mobile, school, admin_only, ROUND(per_hr,1) per_hr,
       ROUND(st_med,1) st_med, st_n, ROUND(x_state,1) x_state, n_all, n_landed, ROUND(nat_med,1) nat_med, types
FROM r WHERE st_n >= 10 ORDER BY x_state DESC NULLS LAST LIMIT 15;

-- S18 GUDID staging: device records per block, first DI of each block, and whether it is already in the 5.08M GUDID table
WITH s AS (SELECT raw:results[0]:identifiers[0]:id::string di0, raw:results[0]:identifiers[0]:type::string di0_type,
                  ARRAY_SIZE(raw:results) k, raw:results[0]:publish_date::string pd
           FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_GUDID__STAGING),
g AS (SELECT DISTINCT primary_di FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_GUDID WHERE primary_di IN (SELECT di0 FROM s))
SELECT COUNT(*) blocks, SUM(k) records, MIN(k) k_min, MAX(k) k_max, COUNT(DISTINCT di0) distinct_first_di,
       ARRAY_AGG(DISTINCT di0_type) di_types, COUNT_IF(g.primary_di IS NOT NULL) first_di_in_main, MIN(pd) pd_min, MAX(pd) pd_max
FROM s LEFT JOIN g ON g.primary_di = s.di0;
