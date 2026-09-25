-- State peers: efficiency + demand-response program dollars per electricity customer, every reporter in the state (third-party administrators
-- like Efficiency Maine or Energy Trust count under their state). Two units slips corrected /1000: Delaware SEU (58854) and West River (20401).
-- Denominator: all customers in the sales table except energy-only retailers (part B) so no customer is counted twice.
with c as (select STATE, sum(TOTAL_CUSTOMERS) cust, sum(RESIDENTIAL_CUSTOMERS) homes from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_SALES_ULT_CUST where PART<>'B' group by 1),
e as (select STATE, count(*) ee_rows,
        sum((coalesce(TOTAL_INCREMENTAL_CUSTOMER_INCENTIVES_THOUSAND_DOLLARS,0)+coalesce(TOTAL_INCREMENTAL_ALL_OTHER_COSTS_THOUSAND_DOLLARS,0)) / iff(UTILITY_NUMBER in (58854,20401),1000,1)) ee_k,
        sum(TOTAL_INCREMENTAL_ENERGY_SAVINGS_MWH) sav
      from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_ENERGY_EFFICIENCY group by 1),
d as (select STATE, sum(coalesce(TOTAL_CUSTOMER_INCENTIVES_THOUSAND_DOLLARS,0)+coalesce(TOTAL_ALL_OTHER_COSTS_THOUSAND_DOLLARS,0)) dr_k
      from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_DEMAND_RESPONSE group by 1),
s as (select STATE, sum(TOTAL_SALES_MWH) mwh from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_SALES_ULT_CUST group by 1),
j as (select c.STATE, c.cust, c.homes, e.ee_rows, e.ee_k, d.dr_k, e.sav, s.mwh,
        coalesce(e.ee_k,0)*1000/c.cust ee_cust, (coalesce(e.ee_k,0)+coalesce(d.dr_k,0))*1000/c.cust both_cust, 100*e.sav/nullif(s.mwh,0) sav_pct
      from c left join e on e.STATE=c.STATE left join d on d.STATE=c.STATE left join s on s.STATE=c.STATE where c.cust>0)
select STATE, round(cust) cust, ee_rows, round(ee_k) ee_k, round(dr_k) dr_k, round(ee_cust,2) ee_per_cust, round(both_cust,2) ee_dr_per_cust, round(sav_pct,3) sav_pct_sales,
  rank() over (order by both_cust desc) rnk, round(median(both_cust) over (),2) nat_median, count(*) over () states
from j order by both_cust desc
