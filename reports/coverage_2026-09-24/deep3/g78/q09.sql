-- FRA casualties (source): where did UP's and BNSF's trespasser deaths rise? State split, yearly avg 2015-2017 vs 2023-2025
-- Also the last date on file, to size the 2026 partial year
with f as (select RAILROAD_CODE rr, STATE_NAME st, INCIDENT_YEAR y from LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_FRA_CASUALTIES
           where FATALITY='Yes' and TYPE_OF_PERSON ilike 'Trespass%' and RAILROAD_CODE in ('UP','BNSF','CSX','NS') and (INCIDENT_YEAR between 2015 and 2017 or INCIDENT_YEAR between 2023 and 2025)),
s as (select rr, st, count_if(y<=2017)/3 a, count_if(y>=2023)/3 b from f group by 1,2),
tot as (select rr, sum(a) ta, sum(b) tb, count(*) states, count_if(b>a) up_states from s group by 1)
select 'tot' k, rr, null st, round(ta,1) a, round(tb,1) b, round(tb-ta,1) d, states||' states, '||up_states||' up' note from tot
union all select * from (select 'st', rr, st, round(a,1), round(b,1), round(b-a,1), round((b-a)/nullif((select tb-ta from tot where tot.rr=s.rr),0),2)::varchar from s
  qualify row_number() over (partition by rr order by b-a desc) <= 6)
union all select 'maxdate', null, null, null, null, null, (select max(DATE)::varchar from LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_FRA_CASUALTIES)
order by 1, 2, 6 desc;
