-- TRI facility traps: coordinate formats (the DDMMSS / positive-longitude trap), closed-flag facilities that still filed for 2023, blank parents
with t as (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_FACILITY),
b as (select C_2_TRIFD id, any_value(C_4_FACILITY_NAME) nm, sum(C_65_ON_SITE_RELEASE_TOTAL) onsite from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_BASIC_2023 group by 1)
select 'coords' k, count_if(FAC_LATITUDE > 1000)::text a, count_if(FAC_LATITUDE between 1 and 90)::text b, count_if(FAC_LATITUDE = 0 or FAC_LATITUDE is null)::text c,
  count_if(PREF_LONGITUDE > 0)::text d, count_if(PREF_LONGITUDE < 0)::text e, count_if(PREF_ACCURACY = '99999.00')::text f, count_if(nullif(trim(PARENT_CO_NAME), '') is null)::text g from t
union all
select * from (select 'closed_filed', t.TRI_FACILITY_ID, t.FACILITY_NAME, t.CITY_NAME || ', ' || t.STATE_ABBR, round(b.onsite)::text, t.FAC_CLOSED_IND, t.STANDARDIZED_PARENT_COMPANY, null
  from t join b on t.TRI_FACILITY_ID = b.id where t.FAC_CLOSED_IND = '1' order by b.onsite desc nulls last limit 8);
