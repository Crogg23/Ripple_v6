-- DIM_TRACT key vintage vs the biggest tract-level money table: HMDA historic 2015-2017 (2010 tracts). Aggregate first, then join.
-- Tract = 2-digit state + 3-digit county + 6-digit tract (dot removed). Also shows how STATE_CODE / COUNTY_CODE are written.
with h as (
  select AS_OF_YEAR yr, STATE_CODE, COUNTY_CODE, CENSUS_TRACT_NUMBER, count(*) n
  from LIBRARY_MARTS.HOUSING.HOUSING__FED_CFPB_HMDA_HISTORIC group by 1,2,3,4),
k as (select yr, n, STATE_CODE, COUNTY_CODE, CENSUS_TRACT_NUMBER,
        iff(try_to_number(STATE_CODE::text) is not null and try_to_number(COUNTY_CODE::text) is not null and nullif(trim(CENSUS_TRACT_NUMBER::text),'') is not null,
            lpad(try_to_number(STATE_CODE::text)::text,2,'0') || lpad(try_to_number(COUNTY_CODE::text)::text,3,'0')
            || lpad(replace(trim(CENSUS_TRACT_NUMBER::text),'.',''),6,'0'), null) geoid
      from h)
select yr::text yr, iff(left(geoid,2)='09','CT','rest') grp, sum(n) rows_, sum(iff(geoid is null, n, 0)) rows_no_tract,
  sum(iff(d.TRACT_GEOID is not null, n, 0)) rows_landed, round(100*sum(iff(d.TRACT_GEOID is not null, n, 0))/nullif(sum(iff(geoid is not null, n, 0)),0),1) pct_landed_of_coded,
  count(distinct geoid) tracts, count(distinct iff(d.TRACT_GEOID is not null, geoid, null)) tracts_landed,
  any_value(STATE_CODE)::text st_eg, any_value(COUNTY_CODE)::text cty_eg, any_value(CENSUS_TRACT_NUMBER)::text tr_eg
from k left join LIBRARY_MARTS.CORE.DIM_TRACT d on d.TRACT_GEOID = k.geoid
group by 1,2 order by 1,2;
