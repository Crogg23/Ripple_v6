-- ICE facility list: confirm lookup; types; duplicate name+city; name+state match to the facility-code table; load stamps
with l as (select * from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_FACILITY_LIST),
f as (select upper(trim(DETENTION_FACILITY_NAME)) nm, upper(trim(STATE)) st, min(DETENTION_FACILITY_CODE) code, min(TYPE_DETAILED) td from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_FACILITY_CODES group by 1, 2)
select 'profile' k, count(*)::text a, count(distinct FACILITY_NAME)::text b, count(distinct FACILITY_NAME||'|'||CITY)::text c, count(distinct STATE)::text d from l
union all select 'type', FACILITY_TYPE_DETAILED, count(*)::text, null, null from l group by 2
union all select 'name_state_match', count(*)::text, count_if(f.code is not null)::text, null, null from l left join f on f.nm = upper(trim(l.FACILITY_NAME)) and f.st = upper(trim(l.STATE))
union all select 'dupe', FACILITY_NAME, CITY, count(*)::text, null from l group by 2, 3 having count(*) > 1
union all select 'load', _INGESTED_AT::text, _SOURCE_RUN_ID, count(*)::text, null from l group by 2, 3
