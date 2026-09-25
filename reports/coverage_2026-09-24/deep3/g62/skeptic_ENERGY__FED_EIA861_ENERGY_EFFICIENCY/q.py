EE = "LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_ENERGY_EFFICIENCY"
SA = "LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_SALES_ULT_CUST"
DR = "LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_DEMAND_RESPONSE"
LAND = "LIBRARY_RAW.LANDING.FED_EIA861_ENERGY_EFFICIENCY"
YR = "'^[0-9]{4}$'"
Q = {}
Q['s1'] = f"""
select 'landing' k, count(*)::text a, count_if(regexp_like(trim(UNNAMED_0),{YR}))::text b,
  listagg(distinct iff(regexp_like(trim(UNNAMED_0),{YR}), null, left(coalesce(UNNAMED_0,'<null>'),40)), ' | ') c,
  count(distinct _SOURCE_RUN_ID)::text d, listagg(distinct _SRC_FILE,'|') e, count_if(trim(UNNAMED_3)='OH')::text f
from {LAND}
union all
select 'sales', count(*)::text, count(distinct DATA_YEAR)::text, listagg(distinct DATA_YEAR,'|'), count(distinct _SOURCE_RUN_ID)::text, listagg(distinct PART,'|'), listagg(distinct DATA_TYPE,'|') from {SA}
union all
select 'dr', count(*)::text, count(distinct DATA_YEAR)::text, listagg(distinct DATA_YEAR,'|'), count(distinct UTILITY_NUMBER||'|'||STATE)::text, count(distinct _SOURCE_RUN_ID)::text, null from {DR}
"""
Q['s2'] = f"""
with e as (select *, count(*) over (partition by UTILITY_NUMBER, STATE) dup from {EE})
select UTILITY_NUMBER, UTILITY_NAME, STATE, dup,
  TOTAL_INCREMENTAL_CUSTOMER_INCENTIVES_THOUSAND_DOLLARS inc_k, TOTAL_INCREMENTAL_ALL_OTHER_COSTS_THOUSAND_DOLLARS oth_k,
  TOTAL_LIFE_CYCLE_CUSTOMER_INCENTIVES_THOUSAND_DOLLARS lc_inc_k, TOTAL_LIFE_CYCLE_ALL_OTHER_COSTS_THOUSAND_DOLLARS lc_oth_k,
  TOTAL_INCREMENTAL_ENERGY_SAVINGS_MWH sav, left(WEBSITE,60) web
from e
where STATE in ('OH','MI') or dup>1
   or UTILITY_NAME ilike any ('%duke%','%dayton%','%aes %','%aes-%','%ohio%','%municipal power%','%efficiency%','%firstenergy%','%buckeye%','%dp&l%','%dpl%')
order by STATE, UTILITY_NAME
"""
Q['s3'] = f"""
with ids as (select distinct UTILITY_NUMBER from {SA}
             where STATE='OH' and (UTILITY_NAME ilike '%duke%' or UTILITY_NAME ilike '%dayton%' or UTILITY_NAME ilike '%aes%' or UTILITY_NAME ilike '%ohio power%'))
select 'sales' src, s.UTILITY_NUMBER::text un, s.UTILITY_NAME nm, s.STATE st, s.PART p, s.DATA_TYPE dt, s.TOTAL_CUSTOMERS::text v, s.OWNERSHIP o
 from {SA} s where s.UTILITY_NUMBER in (select UTILITY_NUMBER from ids)
union all
select 'ee', UTILITY_NUMBER::text, UTILITY_NAME, STATE, null, null, (coalesce(TOTAL_INCREMENTAL_CUSTOMER_INCENTIVES_THOUSAND_DOLLARS,0)+coalesce(TOTAL_INCREMENTAL_ALL_OTHER_COSTS_THOUSAND_DOLLARS,0))::text, null
 from {EE} where UTILITY_NUMBER in (select UTILITY_NUMBER from ids)
union all
select 'dr', UTILITY_NUMBER::text, UTILITY_NAME, STATE, null, null,
  (coalesce(TOTAL_CUSTOMER_INCENTIVES_THOUSAND_DOLLARS,0)+coalesce(TOTAL_ALL_OTHER_COSTS_THOUSAND_DOLLARS,0))::text||' k$; enrolled '||coalesce(TOTAL_CUSTOMERS_ENROLLED::text,'-'), null
 from {DR} where STATE='OH' or UTILITY_NUMBER in (select UTILITY_NUMBER from ids) or UTILITY_NAME ilike any ('%dayton%','%aes%','%duke%ohio%')
order by 1,4,3
"""
Q['s4'] = f"""
select STATE, PART, listagg(distinct SERVICE_TYPE,'|') svc, count(*) n, sum(TOTAL_CUSTOMERS) cust, sum(TOTAL_SALES_MWH) mwh,
  round(sum(TOTAL_REVENUES_THOUSAND_DOLLARS)) rev_k, count_if(UTILITY_NUMBER=99999) adj_rows, sum(iff(UTILITY_NUMBER=99999,TOTAL_CUSTOMERS,0)) adj_cust,
  count_if(DATA_TYPE='I') imputed_rows
from {SA} where STATE in ('OH','MI','PA','IL','IN','KY') group by 1,2 order by 1,2
"""
COST = "(coalesce(TOTAL_INCREMENTAL_CUSTOMER_INCENTIVES_THOUSAND_DOLLARS,0)+coalesce(TOTAL_INCREMENTAL_ALL_OTHER_COSTS_THOUSAND_DOLLARS,0))"
LCOST = "(coalesce(TOTAL_LIFE_CYCLE_CUSTOMER_INCENTIVES_THOUSAND_DOLLARS,0)+coalesce(TOTAL_LIFE_CYCLE_ALL_OTHER_COSTS_THOUSAND_DOLLARS,0))"
FIX = "iff(UTILITY_NUMBER in (58854,20401),1000,1)"
DCOST = "(coalesce(TOTAL_CUSTOMER_INCENTIVES_THOUSAND_DOLLARS,0)+coalesce(TOTAL_ALL_OTHER_COSTS_THOUSAND_DOLLARS,0))"
Q['s5'] = f"""
with c as (select STATE, sum(iff(PART<>'B',TOTAL_CUSTOMERS,0)) cust, sum(iff(PART<>'B' and UTILITY_NUMBER<>99999,TOTAL_CUSTOMERS,0)) cust_noadj,
             sum(TOTAL_REVENUES_THOUSAND_DOLLARS) rev_k, sum(TOTAL_SALES_MWH) mwh_all, sum(iff(PART<>'B',TOTAL_SALES_MWH,0)) mwh_nob
           from {SA} group by 1),
e as (select STATE, sum({COST}/{FIX}) ee_k, sum(greatest({COST},{LCOST})/{FIX}) ee_max_k, sum(TOTAL_INCREMENTAL_ENERGY_SAVINGS_MWH) sav
      from {EE} group by 1),
d as (select STATE, sum({DCOST}) dr_k from {DR} group by 1),
j as (select c.STATE, c.cust, coalesce(e.ee_k,0) ee_k, coalesce(d.dr_k,0) dr_k,
        coalesce(e.ee_k,0)*1000/c.cust ee_cust,
        (coalesce(e.ee_k,0)+coalesce(d.dr_k,0))*1000/c.cust both_cust,
        coalesce(e.ee_k,0)*1000/nullif(c.cust_noadj,0) ee_cust_noadj,
        coalesce(e.ee_max_k,0)*1000/c.cust ee_max_cust,
        100*coalesce(e.ee_k,0)/nullif(c.rev_k,0) ee_pct_rev,
        100*coalesce(e.sav,0)/nullif(c.mwh_all,0) sav_pct_all,
        100*coalesce(e.sav,0)/nullif(c.mwh_nob,0) sav_pct_nob
      from c left join e on e.STATE=c.STATE left join d on d.STATE=c.STATE where c.cust>0),
r as (select j.*, rank() over (order by ee_cust desc) r_ee, rank() over (order by both_cust desc) r_both, rank() over (order by ee_cust_noadj desc) r_noadj,
        rank() over (order by ee_max_cust desc) r_max, rank() over (order by ee_pct_rev desc) r_rev, rank() over (order by sav_pct_nob desc) r_sav,
        median(ee_cust) over () med_ee, median(both_cust) over () med_both, median(ee_pct_rev) over () med_rev, median(sav_pct_nob) over () med_sav, count(*) over () n from j)
select STATE, round(cust) cust, round(ee_k) ee_k, round(ee_cust,2) ee_cust, r_ee, round(both_cust,2) both_cust, r_both, round(ee_cust_noadj,2) ee_noadj, r_noadj,
  round(ee_max_cust,2) ee_max, r_max, round(ee_pct_rev,3) ee_pct_rev, r_rev, round(sav_pct_all,3) sav_all, round(sav_pct_nob,3) sav_nob, r_sav,
  round(med_ee,2) med_ee, round(med_both,2) med_both, round(med_rev,3) med_rev, round(med_sav,3) med_sav, n
from r where STATE in ('OH','MI','IL','PA','IN','KY','WV','FL','AL','KS','GA','TX') or r_both>=45 order by r_both
"""
Q['s6'] = f"""
with s as (select UTILITY_NUMBER, STATE, max(UTILITY_NAME) uname, sum(TOTAL_CUSTOMERS) tc
           from {SA} where PART<>'B' and OWNERSHIP='Investor Owned' group by 1,2 having sum(TOTAL_CUSTOMERS)>=20000),
e as (select UTILITY_NUMBER, STATE, sum({COST}) ee_k from {EE} group by 1,2),
d as (select UTILITY_NUMBER, STATE, sum({DCOST}) dr_k from {DR} group by 1,2),
j as (select s.*, coalesce(e.ee_k,0)*1000/s.tc ee_cust, (coalesce(e.ee_k,0)+coalesce(d.dr_k,0))*1000/s.tc both_cust, iff(e.ee_k is null,1,0) no_ee
      from s left join e on e.UTILITY_NUMBER=s.UTILITY_NUMBER and e.STATE=s.STATE left join d on d.UTILITY_NUMBER=s.UTILITY_NUMBER and d.STATE=s.STATE),
g as (select STATE, count(*) n_iou, sum(no_ee) n_no_ee, round(sum(tc)) iou_cust, round(median(ee_cust),2) med_ee, round(median(both_cust),2) med_both,
        round(max(ee_cust),2) max_ee from j group by 1 having count(*)>=2)
select g.*, rank() over (order by med_ee desc) r_med_ee, rank() over (order by med_both desc) r_med_both, count(*) over () n_states from g order by med_ee asc
"""
