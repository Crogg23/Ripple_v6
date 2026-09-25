-- DIM_TRACT vs DIM_COUNTY: county-code land rate and population agreement, per state (state = left 2 of county code)
with tc as (select COUNTY_FIPS, count(*) tracts, sum(POPULATION_2020) pop from LIBRARY_MARTS.CORE.DIM_TRACT group by 1),
dc as (select COUNTY_FIPS, POPULATION_2020 pop from LIBRARY_MARTS.CORE.DIM_COUNTY),
j as (select coalesce(tc.COUNTY_FIPS, dc.COUNTY_FIPS) cf, tc.COUNTY_FIPS t_cf, dc.COUNTY_FIPS d_cf, tc.pop t_pop, dc.pop d_pop, tc.tracts
      from tc full outer join dc on tc.COUNTY_FIPS = dc.COUNTY_FIPS)
select left(cf,2) st, count(t_cf) tract_counties, count(d_cf) dim_counties,
  count_if(t_cf is not null and d_cf is not null) matched, sum(t_pop) tract_pop, sum(d_pop) county_pop,
  sum(iff(d_cf is null, t_pop, 0)) tract_pop_unmatched, sum(iff(d_cf is null, tracts, 0)) tracts_unmatched,
  count_if(t_cf is not null and d_cf is not null and t_pop<>d_pop) pop_diff_counties,
  listagg(iff(t_cf is null, d_cf, null), ',') dim_only, listagg(iff(d_cf is null, t_cf, null), ',') tract_only
from j group by 1
having count(t_cf)<>count(d_cf) or count_if(t_cf is not null and d_cf is not null)<>count(t_cf)
    or count_if(t_cf is not null and d_cf is not null and t_pop<>d_pop)>0 or left(cf,2) in ('06','09','48')
union all
select 'ALL', count(t_cf), count(d_cf), count_if(t_cf is not null and d_cf is not null), sum(t_pop), sum(d_pop),
  sum(iff(d_cf is null, t_pop, 0)), sum(iff(d_cf is null, tracts, 0)),
  count_if(t_cf is not null and d_cf is not null and t_pop<>d_pop), null, null
from j
order by 1;
