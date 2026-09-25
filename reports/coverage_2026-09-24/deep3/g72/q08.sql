-- DIM_TRACT outliers: 12 biggest tracts, with their state's median tract and the state's share of tracts over 8,000 (Census aims for 1,200-8,000)
with t as (select * from LIBRARY_MARTS.CORE.DIM_TRACT),
st as (select STATE_FIPS, count(*) tracts, median(POPULATION_2020) st_med, count_if(POPULATION_2020>8000) over8k,
         round(100*count_if(POPULATION_2020>8000)/count(*),1) pct_over8k, count_if(POPULATION_2020>15000) over15k from t group by 1),
top as (select t.TRACT_GEOID, t.POPULATION_2020 pop, t.POP_CENTER_LAT, t.POP_CENTER_LON, c.COUNTY_NAME, c.STATE_NAME
        from t left join LIBRARY_MARTS.CORE.DIM_COUNTY c on c.COUNTY_FIPS = t.COUNTY_FIPS
        order by pop desc limit 12)
select 'top' k, top.TRACT_GEOID a, top.pop::text b, top.COUNTY_NAME||', '||top.STATE_NAME c,
  round(top.POP_CENTER_LAT,4)||','||round(top.POP_CENTER_LON,4) d, st.st_med::text e, round(top.pop/st.st_med,1)::text f
from top join st on st.STATE_FIPS = left(top.TRACT_GEOID,2)
union all
select * from (select 'state_over8k', STATE_FIPS, tracts::text, over8k::text, pct_over8k::text, st_med::text, over15k::text from st order by pct_over8k desc limit 10)
union all
select 'nat', 'all', count(*)::text, count_if(POPULATION_2020>8000)::text, round(100*count_if(POPULATION_2020>8000)/count(*),2)::text,
  median(POPULATION_2020)::text, count_if(POPULATION_2020>15000)::text from t;
