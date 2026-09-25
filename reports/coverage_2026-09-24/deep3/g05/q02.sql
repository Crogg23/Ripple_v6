-- Hospital enrollments: profile, the NPIs that repeat 68 times, provider types
with t as (select * from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPITAL_ENROLLMENTS),
topnpi as (select NPI, count(*) n, count(distinct CCN) ccns, count(distinct ORGANIZATION_NAME) orgs, count(distinct ENROLLMENT_STATE) st,
             any_value(ORGANIZATION_NAME) org, listagg(distinct MULTIPLE_NPI_FLAG,'|') mf
           from t group by 1 order by n desc limit 6)
select 'npi' k, NPI a, n::text b, ccns::text c, orgs::text d, st::text e, org f, mf g from topnpi
union all
select 'profile', count(*)::text, count(distinct CCN)::text, count(distinct NPI)::text, count(distinct ASSOCIATE_ID)::text,
  count_if(MULTIPLE_NPI_FLAG='Y')::text, count_if(REH_CONVERSION_FLAG='Y')::text || ' reh / ' || count_if(REH_CONVERSION_DATE is not null)::text || ' dated',
  count_if(year(INCORPORATION_DATE)<1900)::text || ' pre1900; null ' || count_if(INCORPORATION_DATE is null)::text from t
union all
select 'ptype', PROVIDER_TYPE_CODE, PROVIDER_TYPE_TEXT, count(*)::text, count_if(PROPRIETARY_NONPROFIT='P')::text, count(distinct CCN)::text, null, null from t group by 2,3
