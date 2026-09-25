-- Dull-explanation test for the low EE spenders: maybe they spend through demand response (load control) instead.
-- Same 62 big utility-state rows; EE $ per customer, demand-response $ per customer (EIA-861 DR file, same utility number + state), combined, peer medians.
with s as (select UTILITY_NUMBER, STATE, max(UTILITY_NAME) uname, sum(RESIDENTIAL_CUSTOMERS) rc, sum(TOTAL_CUSTOMERS) tc
           from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_SALES_ULT_CUST where PART<>'B' group by 1,2 having sum(RESIDENTIAL_CUSTOMERS)>=500000),
e as (select UTILITY_NUMBER, STATE, sum(coalesce(TOTAL_INCREMENTAL_CUSTOMER_INCENTIVES_THOUSAND_DOLLARS,0)+coalesce(TOTAL_INCREMENTAL_ALL_OTHER_COSTS_THOUSAND_DOLLARS,0)) ee_k
      from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_ENERGY_EFFICIENCY group by 1,2),
d as (select UTILITY_NUMBER, STATE, sum(coalesce(TOTAL_CUSTOMER_INCENTIVES_THOUSAND_DOLLARS,0)+coalesce(TOTAL_ALL_OTHER_COSTS_THOUSAND_DOLLARS,0)) dr_k,
        sum(RESIDENTIAL_CUSTOMERS_ENROLLED) dr_res_enrolled, sum(TOTAL_ACTUAL_PEAK_DEMAND_SAVINGS_MW) dr_actual_mw, sum(TOTAL_POTENTIAL_PEAK_DEMAND_SAVINGS_MW) dr_pot_mw
      from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_DEMAND_RESPONSE group by 1,2),
j as (select s.*, e.ee_k, d.dr_k, d.dr_res_enrolled, d.dr_actual_mw, d.dr_pot_mw, e.ee_k*1000/s.tc ee_cust, d.dr_k*1000/s.tc dr_cust,
        (coalesce(e.ee_k,0)+coalesce(d.dr_k,0))*1000/s.tc both_cust
      from s left join e on e.UTILITY_NUMBER=s.UTILITY_NUMBER and e.STATE=s.STATE left join d on d.UTILITY_NUMBER=s.UTILITY_NUMBER and d.STATE=s.STATE)
select 'peer' k, null uname, null st, count(*)::text n, count(dr_k)::text with_dr, round(median(ee_cust),2)::text, round(median(dr_cust),2)::text, round(median(both_cust),2)::text, null, null, null from j
union all
select * from (select 'row', uname, STATE, round(rc)::text, round(ee_k)::text, round(ee_cust,2)::text, round(dr_cust,2)::text, round(both_cust,2)::text,
   round(dr_res_enrolled)::text, round(dr_actual_mw)::text, (rank() over (order by both_cust desc))::text
 from j order by both_cust asc limit 20)
