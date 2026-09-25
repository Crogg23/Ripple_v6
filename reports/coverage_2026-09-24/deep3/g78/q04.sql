-- FRA deaths by railroad: grain check, years, person types with death totals
with t as (select * from LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_FRA_RAIL_DEATHS_BY_RAILROAD)
select 'profile' k, count(*)::varchar a, count(distinct RAILROAD_CODE||'|'||INCIDENT_YEAR||'|'||TYPE_OF_PERSON)::varchar b,
  count(distinct RAILROAD_CODE)::varchar c, min(INCIDENT_YEAR)||'-'||max(INCIDENT_YEAR) d, sum(DEATHS)::varchar e,
  count(distinct _INGESTED_AT)::varchar f, count_if(DEATHS<=0)::varchar g from t
union all select 'type', TYPE_OF_PERSON, count(*)::varchar, sum(DEATHS)::varchar, min(INCIDENT_YEAR)||'-'||max(INCIDENT_YEAR), null, null, null from t group by 2
union all select 'year', INCIDENT_YEAR::varchar, count(*)::varchar, sum(DEATHS)::varchar, sum(iff(TYPE_OF_PERSON ilike 'trespass%',DEATHS,0))::varchar, count(distinct RAILROAD_CODE)::varchar, null, null from t group by 2
order by 1,2;
