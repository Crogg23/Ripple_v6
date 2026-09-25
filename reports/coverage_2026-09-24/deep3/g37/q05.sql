-- TRI facility: IDs, closed flag, parents, and land rates into TRI 2023 releases and ECHO
with t as (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_FACILITY),
b as (select distinct C_2_TRIFD id, C_3_FRS_ID frs from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_BASIC_2023),
e as (select distinct FRS_ID from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ECHO)
select 'profile' k, count(*)::text a, count(distinct TRI_FACILITY_ID)::text b, count(distinct EPA_REGISTRY_ID)::text c,
  count_if(EPA_REGISTRY_ID is null or trim(EPA_REGISTRY_ID) = '')::text d, count(FRS_ID)::text e,
  count_if(PREF_LATITUDE is null)::text f, count_if(nullif(trim(STANDARDIZED_PARENT_COMPANY), '') is not null)::text g from t
union all select 'closed', FAC_CLOSED_IND, count(*)::text, count_if(TRI_FACILITY_ID in (select id from b))::text, count_if(EPA_REGISTRY_ID in (select FRS_ID from e))::text, null, null, null from t group by 2
union all select 'land', 'tri2023 ids in facility', (select count(*) from b)::text, (select count(*) from b where id in (select TRI_FACILITY_ID from t))::text,
   (select count(*) from b where frs in (select EPA_REGISTRY_ID from t))::text, null, null, null
union all select * from (select 'parent', STANDARDIZED_PARENT_COMPANY, count(*)::text, count_if(FAC_CLOSED_IND = '0')::text, count_if(TRI_FACILITY_ID in (select id from b))::text, count(distinct STATE_ABBR)::text, null, null from t
   where nullif(trim(STANDARDIZED_PARENT_COMPANY), '') is not null group by 2 order by count(*) desc limit 15)
union all select * from (select 'dupregid', EPA_REGISTRY_ID, count(*)::text, listagg(distinct FACILITY_NAME, ' | '), null, null, null, null from t where EPA_REGISTRY_ID is not null group by 2 having count(*) > 1 order by count(*) desc limit 5);
