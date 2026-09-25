-- DIM_TRACT: which states carry which VINTAGE, and CT tract-code sample
select VINTAGE, left(TRACT_GEOID,2) st, count(*) tracts, count(distinct COUNTY_FIPS) counties, sum(POPULATION_2020) pop,
  min(TRACT_GEOID) geoid_min, max(TRACT_GEOID) geoid_max
from LIBRARY_MARTS.CORE.DIM_TRACT
group by 1,2 having VINTAGE <> '2020' or left(TRACT_GEOID,2) in ('09','72')
union all
select VINTAGE, 'ALL', count(*), count(distinct COUNTY_FIPS), sum(POPULATION_2020), null, null
from LIBRARY_MARTS.CORE.DIM_TRACT group by 1
order by 1,2;
