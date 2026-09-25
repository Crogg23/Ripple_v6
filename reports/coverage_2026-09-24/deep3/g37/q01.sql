-- NPDES facilities: keys, permit-type letter, impaired flag, facility types, placeholders, the FRS IDs that hold thousands of permits
with t as (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_ICIS_FACILITIES)
select 'profile' k, count(*)::text a, count(distinct NPDES_ID)::text b, count(distinct FACILITY_UIN)::text c,
  count(distinct ICIS_FACILITY_INTEREST_ID)::text d, count_if(IMPAIRED_WATERS is not null and trim(IMPAIRED_WATERS)<>'')::text e,
  count_if(GEOCODE_LATITUDE is null or GEOCODE_LATITUDE=0)::text f, count(distinct STATE_CODE)::text g from t
union all select 'impaired_val', IMPAIRED_WATERS, count(*)::text, null, null, null, null, null from t group by 2
union all select 'ptype3', substr(NPDES_ID,3,1), count(*)::text, count_if(IMPAIRED_WATERS is not null and trim(IMPAIRED_WATERS)<>'')::text, count_if(FACILITY_TYPE_CODE='MWD')::text, null, null, null from t group by 2
union all select 'ftype', FACILITY_TYPE_CODE, count(*)::text, count_if(IMPAIRED_WATERS is not null and trim(IMPAIRED_WATERS)<>'')::text, count_if(substr(NPDES_ID,3,1)='0')::text, null, null, null from t group by 2
union all select * from (select 'topuin', FACILITY_UIN, count(*)::text, any_value(FACILITY_NAME), any_value(LOCATION_ADDRESS), listagg(distinct STATE_CODE, ',') within group (order by STATE_CODE), count(distinct FACILITY_NAME)::text, min(NPDES_ID)||'..'||max(NPDES_ID) from t group by 2 order by count(*) desc limit 6)
union all select * from (select 'state', STATE_CODE, count(*)::text, count_if(IMPAIRED_WATERS is not null and trim(IMPAIRED_WATERS)<>'')::text, count_if(substr(NPDES_ID,3,1)='0')::text, count_if(FACILITY_TYPE_CODE='MWD')::text, null, null from t group by 2 order by count(*) desc limit 70);
