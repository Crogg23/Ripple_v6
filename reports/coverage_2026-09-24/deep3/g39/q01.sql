-- Envirofacts: is it a sample, is it sorted, does it land in the full TRI facility table?
with e as (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ENVIROFACTS),
t as (select distinct upper(trim(FACILITY_NAME)) nm, left(ZIP_CODE,5) z, STATE_ABBR st from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_FACILITY),
tri as (select count(*) n, count_if(STATE_ABBR='NJ') nj, count(distinct STATE_ABBR) sts from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_FACILITY)
select 'state' k, STATE_CODE::text a, count(*)::text b, null c, null d from e group by 2
union all select 'profile', count(distinct upper(trim(FACILITY_NAME)))::text, count(*)::text, count_if(FRS_ID is not null)::text,
  count_if(LATITUDE is not null)::text || ' lat / runs ' || count(distinct _SOURCE_RUN_ID)::text || ' / tables ' || listagg(distinct TABLE_NAME, '|') from e
union all select 'land_name_zip', null, count(*)::text, count_if(t.nm is not null)::text, null from e left join t on t.nm = upper(trim(e.FACILITY_NAME)) and t.z = left(e.POSTAL_CODE,5)
union all select 'tri_full', null, n::text, nj::text, sts::text from tri
