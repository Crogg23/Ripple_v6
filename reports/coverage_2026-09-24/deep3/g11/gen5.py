T = "LIBRARY_MARTS.HEALTH"
TRI = "LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_BASIC_2023"
num = lambda c: f"TRY_TO_NUMBER(REPLACE({c},',',''))"
fug = "COALESCE(TRY_TO_DOUBLE(c_51_5_1_fugitive_air::string),0)"
stk = "COALESCE(TRY_TO_DOUBLE(c_52_5_2_stack_air::string),0)"
b = f"""-- S22 TRI 2023 trap check: same site + same CAS on more than one row (amendment or double load?)
WITH d AS (SELECT c_2_trifd trifd, TRIM(c_40_cas) cas, COUNT(*) n, COUNT(DISTINCT c_36_doc_ctrl_num) docs, MAX(c_4_facility_name) name, MAX(c_8_st) st,
                  ARRAY_AGG(c_37_chemical||' '||c_49_form_type||' '||ROUND(c_107_total_releases::float)||' air '||ROUND({fug}+{stk})) forms
           FROM {TRI} GROUP BY 1,2 HAVING COUNT(*) > 1)
SELECT (SELECT COUNT(*) FROM {TRI}) all_rows, COUNT(*) dup_pairs, SUM(n) dup_rows, SUM(docs) dup_docs, COUNT_IF(st='CA') ca_dup_pairs,
       ARRAY_SLICE(ARRAY_AGG(name||' ['||st||'] '||cas||' :: '||ARRAY_TO_STRING(forms,' / ')) WITHIN GROUP (ORDER BY st='CA' DESC, n DESC),0,10) sample
FROM d;

-- S23 Styrene air per TRI site: California fiberglass shops ranked against every US styrene reporter and their national sector peers
WITH s AS (SELECT c_2_trifd trifd, MAX(c_4_facility_name) name, MAX(c_6_city) city, MAX(c_8_st) st, MAX(c_23_industry_sector) sector,
                  MAX(c_30_primary_naics) naics, SUM({fug}) fug, SUM({stk}) stk, SUM({fug}+{stk}) air, MAX(c_49_form_type) form,
                  MAX(c_122_8_9_production_ratio) prod_ratio
           FROM {TRI} WHERE TRIM(c_40_cas)='100-42-5' AND c_50_unit_of_measure ILIKE 'Pounds' GROUP BY 1)
SELECT name, city, st, sector, naics, form, ROUND(air) air, ROUND(fug) fug, ROUND(stk) stk, prod_ratio,
       RANK() OVER (ORDER BY air DESC) nat_rank, COUNT(*) OVER () nat_n, ROUND(MEDIAN(air) OVER ()) nat_med,
       ROUND(MEDIAN(air) OVER (PARTITION BY naics)) naics_med, COUNT(*) OVER (PARTITION BY naics) naics_n,
       ROUND(SUM(air) OVER ()) nat_air, ROUND(SUM(IFF(st='CA',air,0)) OVER ()) ca_air, SUM(IFF(st='CA',1,0)) OVER () ca_n,
       ROUND(MEDIAN(IFF(st='CA',air,NULL)) OVER ()) ca_med
FROM s QUALIFY st='CA' ORDER BY air DESC LIMIT 12;

-- S24 UDS: health centers that share a street address or a project director (are they one outfit filed twice?)
WITH i AS (SELECT bhcmisid, grantnumber, healthcentername, healthcentercity, healthcenterstate, fundingchc, fundingmsaw, fundinghp, fundingrph,
                  UPPER(TRIM(healthcenterstreetaddress))||'|'||LEFT(healthcenterzipcode,5) addr,
                  UPPER(REGEXP_REPLACE(TRIM(projectdirector),'[[:space:]]+',' ')) director, LOWER(TRIM(projectdirectoremail)) email
           FROM {T}.HEALTH__FED_HRSA_UDS_HEALTH_CENTER_INFO),
c AS (SELECT bhcmisid, {num('T3A_L39_CA')} + {num('T3A_L39_CB')} tot FROM {T}.HEALTH__FED_HRSA_UDS_TABLE3A_PATIENTS),
k AS (SELECT addr, COUNT(*) OVER (PARTITION BY addr) n_addr, COUNT(*) OVER (PARTITION BY director) n_dir, i.* FROM i)
SELECT k.bhcmisid, k.grantnumber, k.healthcentername, k.healthcentercity, k.healthcenterstate, k.director, k.email, k.n_addr, k.n_dir,
       k.fundingchc, k.fundingmsaw, k.fundinghp, k.fundingrph, c.tot
FROM k JOIN c USING (bhcmisid) WHERE k.n_addr > 1 OR k.n_dir > 1 ORDER BY k.addr, k.director;
"""
open("batch5.sql","w",encoding="utf-8").write(b)
