-- One join: FEMA IA registrations (block group -> first 11 digits = tract) to DIM_TRACT. Aggregate FEMA first. Land rate by census vintage, declaration era, CT vs rest
with f as (
  select coalesce(nullif(trim(CENSUS_YEAR),''),'blank') cy,
         year(try_to_timestamp(DECLARATION_DATE::text)) dy,
         iff(DAMAGED_STATE_ABBREVIATION='CT','CT', iff(DAMAGED_STATE_ABBREVIATION='PR','PR','rest')) grp,
         left(CENSUS_GEOID,11) tr, count(*) n
  from LIBRARY_MARTS.HOUSING.HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS
  where regexp_like(CENSUS_GEOID, '[0-9]{11,12}(\.0)?')
  group by 1,2,3,4),
g as (
  select cy, case when dy is null then 'nodate' when dy<2012 then 'a<2012' when dy<2022 then 'b2012-21' else 'c2022+' end era, grp,
    sum(n) rows_, count(distinct tr) tracts, sum(iff(d.TRACT_GEOID is not null, n, 0)) rows_landed,
    count(distinct iff(d.TRACT_GEOID is not null, tr, null)) tracts_landed
  from f left join LIBRARY_MARTS.CORE.DIM_TRACT d on d.TRACT_GEOID = f.tr
  group by 1,2,3)
select *, round(100*rows_landed/nullif(rows_,0),1) pct_rows_landed from g
union all
select 'no_geoid', null, null, count(*), null, null, null, null
from LIBRARY_MARTS.HOUSING.HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS
where not regexp_like(coalesce(CENSUS_GEOID,''), '[0-9]{11,12}(\.0)?')
order by 1,2,3;
