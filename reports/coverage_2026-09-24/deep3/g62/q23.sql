-- Inside-the-group test for Ohio: every utility with 20K+ customers in OH and its neighbors (MI, IN, PA, KY, WV) plus IL,
-- EE $ and DR $ per own customer, savings % of own sales. Median utility per state, so one or two big rows can't carry the gap.
with s as (select UTILITY_NUMBER, STATE, max(UTILITY_NAME) uname, listagg(distinct OWNERSHIP,'|') own, sum(TOTAL_CUSTOMERS) tc, sum(TOTAL_SALES_MWH) mwh
           from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_SALES_ULT_CUST where PART<>'B' and STATE in ('OH','MI','IN','PA','KY','WV','IL') group by 1,2 having sum(TOTAL_CUSTOMERS)>=20000),
e as (select UTILITY_NUMBER, STATE, sum(coalesce(TOTAL_INCREMENTAL_CUSTOMER_INCENTIVES_THOUSAND_DOLLARS,0)+coalesce(TOTAL_INCREMENTAL_ALL_OTHER_COSTS_THOUSAND_DOLLARS,0)) ee_k,
        sum(TOTAL_INCREMENTAL_ENERGY_SAVINGS_MWH) sav from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_ENERGY_EFFICIENCY group by 1,2),
d as (select UTILITY_NUMBER, STATE, sum(coalesce(TOTAL_CUSTOMER_INCENTIVES_THOUSAND_DOLLARS,0)+coalesce(TOTAL_ALL_OTHER_COSTS_THOUSAND_DOLLARS,0)) dr_k
      from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_DEMAND_RESPONSE group by 1,2),
j as (select s.*, e.ee_k, d.dr_k, e.sav, coalesce(e.ee_k,0)*1000/s.tc ee_cust, coalesce(d.dr_k,0)*1000/s.tc dr_cust, 100*coalesce(e.sav,0)/nullif(s.mwh,0) sav_pct
      from s left join e on e.UTILITY_NUMBER=s.UTILITY_NUMBER and e.STATE=s.STATE left join d on d.UTILITY_NUMBER=s.UTILITY_NUMBER and d.STATE=s.STATE)
select 'state' k, STATE, null uname, count(*)::text utils, count(ee_k)::text with_ee, round(median(ee_cust),2)::text med_ee_cust, round(median(ee_cust+dr_cust),2)::text med_both,
  round(median(sav_pct),3)::text med_sav_pct, round(sum(tc))::text cust, null a from j group by 2
union all
select * from (select 'util', STATE, uname, round(tc)::text, own, round(ee_cust,2)::text, round(ee_cust+dr_cust,2)::text, round(sav_pct,3)::text, round(ee_k)::text, round(dr_k)::text
  from j where STATE in ('OH','MI') order by STATE, tc desc)
