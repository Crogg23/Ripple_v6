-- DIM_TRACT: key integrity, padding, sentinels, territories, zero-pop tracts, coordinate sanity
with t as (select * from LIBRARY_MARTS.CORE.DIM_TRACT)
select count(*) n, count(distinct TRACT_GEOID) geoids, count_if(length(TRACT_GEOID)<>11) geoid_not11,
  count_if(length(STATE_FIPS)<>2) st_not2, count_if(length(COUNTY_FIPS)<>5) cty_not5, count_if(length(TRACT_CE)<>6) ce_not6,
  count_if(left(TRACT_GEOID,5)<>COUNTY_FIPS) geoid_cty_mismatch, count_if(left(COUNTY_FIPS,2)<>STATE_FIPS) cty_st_mismatch,
  count_if(right(TRACT_GEOID,6)<>TRACT_CE) ce_mismatch,
  count(distinct STATE_FIPS) states, count(distinct COUNTY_FIPS) counties, listagg(distinct VINTAGE,'|') vintages,
  count_if(POPULATION_2020 is null) pop_null, count_if(POPULATION_2020=0) pop_zero, sum(POPULATION_2020) pop_sum,
  median(POPULATION_2020) pop_med, max(POPULATION_2020) pop_max,
  count_if(POPULATION_2020>8000) over_8000, count_if(POPULATION_2020 between 1 and 1199) under_1200,
  count_if(POP_CENTER_LAT is null or POP_CENTER_LON is null) latlon_null, count_if(POP_CENTER_LON>0) lon_pos,
  min(POP_CENTER_LAT) lat_min, max(POP_CENTER_LAT) lat_max, min(POP_CENTER_LON) lon_min, max(POP_CENTER_LON) lon_max,
  count_if(STATE_FIPS='72') pr_tracts, sum(iff(STATE_FIPS='72',POPULATION_2020,0)) pr_pop,
  count_if(STATE_FIPS in ('60','66','69','78')) island_tracts,
  count_if(TRACT_CE like '99%') ce_99_water, count_if(TRACT_CE like '99%' and POPULATION_2020=0) ce_99_zero,
  count_if(TRACT_CE like '98%') ce_98_special, count_if(TRACT_CE like '98%' and POPULATION_2020=0) ce_98_zero,
  count_if(POPULATION_2020=0 and POP_CENTER_LAT is not null) zero_with_center,
  listagg(distinct iff(STATE_FIPS='09', COUNTY_FIPS, null), ',') ct_counties
from t;
