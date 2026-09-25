-- FRA deaths: who carries the rise in trespasser deaths? Per railroad, yearly average 2015-2017 vs 2023-2025, sorted by change.
-- Plus: how many railroads went up / down, and code-name drift (codes with 2+ names, names with 2+ codes).
with t as (select * from LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_FRA_RAIL_DEATHS_BY_RAILROAD where TYPE_OF_PERSON = 'Trespassers'),
r as (select RAILROAD_CODE code, max(RAILROAD_NAME) nm, max(PARENT_RAILROAD_CODE) parent,
        sum(iff(INCIDENT_YEAR between 2015 and 2017, DEATHS, 0))/3 a, sum(iff(INCIDENT_YEAR between 2023 and 2025, DEATHS, 0))/3 b,
        sum(iff(INCIDENT_YEAR = 2025, DEATHS, 0)) y25, min(INCIDENT_YEAR) first_yr
      from t group by 1),
tot as (select sum(a) ta, sum(b) tb, count_if(b>a) up, count_if(b<a) down, count_if(a>0 and b=0) gone, count_if(a=0 and b>0) new_ from r)
select 'total' k, null code, null nm, round(ta,1) a, round(tb,1) b, round(tb-ta,1) d, up||' up / '||down||' down / '||gone||' gone / '||new_||' new' note from tot
union all select * from (select 'rr', code, nm, round(a,1), round(b,1), round(b-a,1), 'parent '||parent||'; 2025 '||y25||'; first yr '||first_yr from r order by b-a desc limit 15)
union all select * from (select 'rr_down', code, nm, round(a,1), round(b,1), round(b-a,1), 'parent '||parent from r order by b-a asc limit 6)
union all select 'drift_code', RAILROAD_CODE, listagg(distinct RAILROAD_NAME, ' | '), count(distinct RAILROAD_NAME), null, null, null
  from LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_FRA_RAIL_DEATHS_BY_RAILROAD group by RAILROAD_CODE having count(distinct RAILROAD_NAME) > 1
union all select 'drift_name', listagg(distinct RAILROAD_CODE, ' | '), RAILROAD_NAME, count(distinct RAILROAD_CODE), null, null, null
  from LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_FRA_RAIL_DEATHS_BY_RAILROAD group by RAILROAD_NAME having count(distinct RAILROAD_CODE) > 1;
