-- EE with denominators: join each utility-state row to its own 2024 retail sales (SALES_ULT_CUST, same utility number + state).
-- Cost per first-year MWh saved, savings as % of own sales, residential incentive $ per residential customer, each vs the state median.
-- Also the Delaware SEU row against the whole state's 2024 electricity revenue.
with e as (select * from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_ENERGY_EFFICIENCY),
s as (select UTILITY_NUMBER, STATE, sum(RESIDENTIAL_CUSTOMERS) rc, sum(TOTAL_SALES_MWH) tmwh, sum(TOTAL_REVENUES_THOUSAND_DOLLARS) trev
      from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_SALES_ULT_CUST group by 1,2),
st as (select STATE, sum(TOTAL_REVENUES_THOUSAND_DOLLARS) st_rev_k, sum(RESIDENTIAL_REVENUES_THOUSAND_DOLLARS) st_res_rev_k, sum(RESIDENTIAL_CUSTOMERS) st_rc
       from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_SALES_ULT_CUST group by 1),
j as (select e.UTILITY_NAME, e.UTILITY_NUMBER, e.STATE,
   coalesce(e.TOTAL_INCREMENTAL_CUSTOMER_INCENTIVES_THOUSAND_DOLLARS,0)+coalesce(e.TOTAL_INCREMENTAL_ALL_OTHER_COSTS_THOUSAND_DOLLARS,0) cost_k,
   e.TOTAL_INCREMENTAL_ENERGY_SAVINGS_MWH sav, e.RESIDENTIAL_INCREMENTAL_CUSTOMER_INCENTIVES_THOUSAND_DOLLARS rinc, s.rc, s.tmwh, s.trev, st.st_rev_k, st.st_res_rev_k, st.st_rc,
   iff(e.TOTAL_INCREMENTAL_ENERGY_SAVINGS_MWH>0 and cost_k>0, cost_k*1000/e.TOTAL_INCREMENTAL_ENERGY_SAVINGS_MWH, null) usd_per_mwh,
   iff(s.tmwh>0, 100*e.TOTAL_INCREMENTAL_ENERGY_SAVINGS_MWH/s.tmwh, null) sav_pct_sales,
   iff(s.rc>0, e.RESIDENTIAL_INCREMENTAL_CUSTOMER_INCENTIVES_THOUSAND_DOLLARS*1000/s.rc, null) rinc_per_cust
  from e left join s on s.UTILITY_NUMBER=e.UTILITY_NUMBER and s.STATE=e.STATE left join st on st.STATE=e.STATE),
k as (select j.*, median(usd_per_mwh) over (partition by STATE) st_med_usd_mwh, count(usd_per_mwh) over (partition by STATE) st_n,
        median(usd_per_mwh) over () nat_med_usd_mwh, median(sav_pct_sales) over () nat_med_pct, median(rinc_per_cust) over () nat_med_rinc from j)
select 'summary' k, count(*)::text a, count(rc)::text b, count(usd_per_mwh)::text c, round(max(nat_med_usd_mwh),1)::text d, round(max(nat_med_pct),3)::text e,
  round(max(nat_med_rinc),2)::text f, count_if(sav_pct_sales>5)::text g, count_if(usd_per_mwh>5*st_med_usd_mwh and st_n>=3)::text h, count_if(usd_per_mwh<st_med_usd_mwh/5 and st_n>=3)::text i,
  null l, null m, null n2, null o from k
union all
select * from (select 'row' k, UTILITY_NAME a, STATE b, round(cost_k)::text c, round(sav)::text d, round(usd_per_mwh,1)::text e, round(st_med_usd_mwh,1)::text f, st_n::text g,
  round(sav_pct_sales,3)::text h, round(rinc_per_cust,2)::text i, rc::text l, round(tmwh)::text m, round(st_rev_k)::text n2, round(st_res_rev_k)::text o
 from k where STATE='DE' or sav_pct_sales>4 or (st_n>=3 and (usd_per_mwh>4*st_med_usd_mwh or usd_per_mwh<st_med_usd_mwh/4)) or rinc_per_cust>150
 order by usd_per_mwh desc nulls last limit 60)
