-- OTP providers: profile, effective-date years, biggest NPIs and names
with t as (select * from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPIOID_TREATMENT_PROGRAM_PROVIDERS)
select 'profile' k, count(*)::text a, count(distinct NPI)::text b, count(distinct NPI||'|'||upper(trim(ADDRESS_LINE_1))||'|'||left(ZIP,5))::text c,
  count_if(MEDICARE_ID_EFFECTIVE_DATE='2020-01-01')::text d, count(distinct upper(trim(ADDRESS_LINE_1))||'|'||left(ZIP,5))::text e, count(distinct PROVIDER_NAME)::text f from t
union all select 'effyear', year(MEDICARE_ID_EFFECTIVE_DATE)::text, count(*)::text, count(distinct NPI)::text, null, null, null from t group by 2
union all select * from (select 'topnpi', NPI, any_value(PROVIDER_NAME), count(*)::text, count(distinct STATE)::text,
  count(distinct upper(trim(ADDRESS_LINE_1))||left(ZIP,5))::text, min(MEDICARE_ID_EFFECTIVE_DATE)::text from t group by 2 order by count(*) desc limit 8)
union all select * from (select 'topname', upper(PROVIDER_NAME), null, count(*)::text, count(distinct NPI)::text, count(distinct STATE)::text, null
  from t group by 2 order by count(*) desc limit 12)
