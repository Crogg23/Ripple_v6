T = "LIBRARY_MARTS.HEALTH"
TRI = "LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_BASIC_2023"
ECHO = "LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ECHO"
P65 = f"{T}.HEALTH__ST_OEHHA_PROPOSITION_65_LIST"
route = "('%ingested%','%airborne%','%gas)%','%inhal%','%oral%','%respirable%')"
p65clean = f"""p65 AS (SELECT TRIM(cas_no) cas, MIN(chemical) p65_name,
         BOOLOR_AGG(type_of_toxicity ILIKE '%cancer%') p65_cancer,
         BOOLOR_AGG(type_of_toxicity ILIKE '%developmental%' OR type_of_toxicity ILIKE '%male%') p65_repro,
         BOOLOR_AGG(chemical ILIKE ANY {route}) route_limited,
         MIN(date_listed) first_listed
       FROM {P65}
       WHERE cas_no NOT LIKE '--%' AND NULLIF(TRIM(cas_no),'') IS NOT NULL AND date_listed IS NOT NULL
         AND chemical NOT ILIKE '%delisted%'
       GROUP BY 1)"""
air = "COALESCE(TRY_TO_DOUBLE(c_51_5_1_fugitive_air::string),0)+COALESCE(TRY_TO_DOUBLE(c_52_5_2_stack_air::string),0)"
b = f"""-- S19 Prop 65 hygiene: delisted rows, footnote rows, group listings with no CAS, route-limited listings, how lead is listed
SELECT COUNT(*) n, COUNT_IF(chemical ILIKE '%delisted%') delisted_rows, COUNT_IF(date_listed IS NULL) nodate_rows,
       COUNT_IF(cas_no LIKE '--%') dash_cas, COUNT_IF(cas_no LIKE '--%' AND date_listed IS NOT NULL AND chemical NOT ILIKE '%delisted%') dash_cas_live,
       COUNT_IF(chemical ILIKE ANY {route}) route_rows,
       COUNT_IF(cas_no LIKE '%,%' OR TRIM(cas_no) LIKE '% %' OR cas_no LIKE '%/%') multi_cas,
       ARRAY_SLICE(ARRAY_AGG(IFF(chemical ILIKE '%delisted%', LEFT(chemical,70), NULL)),0,6) delisted_sample,
       ARRAY_SLICE(ARRAY_AGG(IFF(cas_no LIKE '--%' AND date_listed IS NOT NULL AND chemical NOT ILIKE '%delisted%', LEFT(chemical,60), NULL)),0,15) dash_names,
       ARRAY_AGG(IFF(chemical ILIKE 'lead%' OR chemical ILIKE 'arsenic%' OR chemical ILIKE 'nickel%', LEFT(chemical,50)||' | '||cas_no||' | '||type_of_toxicity, NULL)) metal_rows
FROM {P65};

-- S20 Prop 65 x TRI 2023, corrected: delisted and footnote rows dropped; total and air pounds by TRI flag and Prop 65 harm
WITH {p65clean},
tri AS (SELECT TRIM(c_40_cas) cas, MAX(c_46_carcinogen) tri_carc, COUNT(DISTINCT c_2_trifd) facs,
               SUM(c_107_total_releases::float) lbs, SUM({air}) air_lbs,
               SUM(IFF(c_8_st='CA', c_107_total_releases::float, 0)) ca_lbs, SUM(IFF(c_8_st='CA', {air}, 0)) ca_air
        FROM {TRI} WHERE c_50_unit_of_measure ILIKE 'Pounds' GROUP BY 1)
SELECT tri_carc, (p65.cas IS NOT NULL) on_p65, p65_cancer, p65_repro, route_limited,
       COUNT(*) chems, ROUND(SUM(lbs)) lbs, ROUND(SUM(air_lbs)) air_lbs, ROUND(SUM(ca_lbs)) ca_lbs, ROUND(SUM(ca_air)) ca_air
FROM tri LEFT JOIN p65 ON p65.cas = tri.cas
GROUP BY GROUPING SETS ((tri_carc, on_p65, p65_cancer, p65_repro, route_limited), (on_p65), ())
ORDER BY 1,2,3,4,5;

-- S21 California TRI sites: air pounds of Prop 65 chemicals per site, ranked against same-sector California peers, plus ECHO record on FRS ID
WITH {p65clean},
tri AS (SELECT c_2_trifd trifd, c_3_frs_id::varchar frs, c_4_facility_name name, c_6_city city, c_23_industry_sector sector,
               c_17_standard_parent_co_name parent, c_37_chemical chem, TRIM(c_40_cas) cas, {air} air
        FROM {TRI} WHERE c_8_st='CA' AND c_50_unit_of_measure ILIKE 'Pounds'),
f AS (SELECT trifd, MAX(frs) frs, MAX(name) name, MAX(city) city, MAX(sector) sector, MAX(parent) parent,
             SUM(IFF(p.cas IS NOT NULL, air, 0)) p65_air, SUM(IFF(p.p65_cancer, air, 0)) cancer_air,
             SUM(IFF(p.cas IS NOT NULL AND NOT COALESCE(p.route_limited,FALSE), air, 0)) p65_air_noroute,
             ARRAY_SLICE(ARRAY_AGG(IFF(p.cas IS NOT NULL AND air>0, chem||' '||ROUND(air), NULL)) WITHIN GROUP (ORDER BY air DESC),0,5) top_chems
      FROM tri LEFT JOIN p65 p ON p.cas = tri.cas GROUP BY 1),
r AS (SELECT f.*, COUNT(*) OVER () ca_facs, SUM(p65_air) OVER () ca_air, p65_air/NULLIF(SUM(p65_air) OVER (),0) share,
             SUM(cancer_air) OVER () ca_cancer_air, cancer_air/NULLIF(SUM(cancer_air) OVER (),0) cancer_share,
             MEDIAN(p65_air) OVER () ca_med, MEDIAN(p65_air) OVER (PARTITION BY sector) sec_med, COUNT(*) OVER (PARTITION BY sector) sec_n
      FROM f WHERE p65_air > 0),
top AS (SELECT * FROM r ORDER BY p65_air DESC LIMIT 12),
e AS (SELECT frs_id::varchar frs_id, MAX(quarters_with_noncompliance) qnc, MAX(formal_action_count) formal, MAX(total_inspection_count) insp,
             MAX(last_penalty_amt_allocated) last_pen_alloc, MAX(date_last_formal_action) last_formal, MAX(compliance_status) status
      FROM {ECHO} WHERE frs_id::varchar IN (SELECT frs FROM top) GROUP BY 1)
SELECT top.name, top.city, top.sector, top.parent, top.frs, ROUND(top.p65_air) p65_air, ROUND(top.p65_air_noroute) p65_air_noroute,
       ROUND(top.cancer_air) cancer_air, ROUND(top.share,3) share, ROUND(top.cancer_share,3) cancer_share,
       ROUND(top.sec_med) sec_med, top.sec_n, ROUND(top.p65_air/NULLIF(top.sec_med,0),1) x_sector, ROUND(top.ca_med) ca_med, top.ca_facs,
       ROUND(top.ca_air) ca_air, ROUND(top.ca_cancer_air) ca_cancer_air, top.top_chems,
       e.qnc, e.formal, e.insp, e.last_pen_alloc, e.last_formal, e.status, (e.frs_id IS NOT NULL) echo_hit
FROM top LEFT JOIN e ON e.frs_id = top.frs ORDER BY top.p65_air DESC;
"""
open("batch4.sql","w",encoding="utf-8").write(b)
