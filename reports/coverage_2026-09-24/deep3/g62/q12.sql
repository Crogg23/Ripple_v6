-- EE unit check: each utility's reported program cost against its OWN 2024 retail revenue (same utility number + state).
-- A cost above ~10% of revenue is not an efficiency program, it is a units slip. Lists every row over 5%, plus the national spread.
with e as (select * from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_ENERGY_EFFICIENCY),
s as (select UTILITY_NUMBER, STATE, sum(TOTAL_REVENUES_THOUSAND_DOLLARS) trev_k, sum(RESIDENTIAL_REVENUES_THOUSAND_DOLLARS) rrev_k
      from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA861_SALES_ULT_CUST group by 1,2),
j as (select e.UTILITY_NAME, e.UTILITY_NUMBER, e.STATE,
   coalesce(e.TOTAL_INCREMENTAL_CUSTOMER_INCENTIVES_THOUSAND_DOLLARS,0)+coalesce(e.TOTAL_INCREMENTAL_ALL_OTHER_COSTS_THOUSAND_DOLLARS,0) cost_k,
   e.RESIDENTIAL_INCREMENTAL_CUSTOMER_INCENTIVES_THOUSAND_DOLLARS rinc_k, e.TOTAL_INCREMENTAL_ENERGY_SAVINGS_MWH sav, s.trev_k, s.rrev_k,
   iff(s.trev_k>0, 100*cost_k/s.trev_k, null) cost_pct_rev
  from e left join s on s.UTILITY_NUMBER=e.UTILITY_NUMBER and s.STATE=e.STATE)
select 'spread' k, null a, null b, count(cost_pct_rev)::text c, round(median(cost_pct_rev),3)::text d, round(percentile_cont(0.9) within group (order by cost_pct_rev),3)::text e,
  round(percentile_cont(0.99) within group (order by cost_pct_rev),3)::text f, count_if(cost_pct_rev>5)::text g, count_if(cost_pct_rev>10)::text h,
  round(sum(cost_k))::text i, round(sum(iff(cost_pct_rev>10 or UTILITY_NUMBER=58854,cost_k,0)))::text l from j
union all
select * from (select 'row', UTILITY_NAME, STATE, round(cost_k)::text, round(rinc_k)::text, round(sav)::text, round(trev_k)::text, round(rrev_k)::text,
  round(cost_pct_rev,2)::text, UTILITY_NUMBER::text, null from j where cost_pct_rev>5 or UTILITY_NUMBER=58854 order by cost_pct_rev desc nulls first)
