with b as (select RNDRNG_NPI n, RNDRNG_PRVDR_LAST_ORG_NAME ln, RNDRNG_PRVDR_FIRST_NAME fn, RNDRNG_PRVDR_TYPE typ, RNDRNG_PRVDR_ST1 a1, RNDRNG_PRVDR_CITY city, RNDRNG_PRVDR_STATE_ABRVTN st, HCPCS_CD h, left(HCPCS_DESC,30) hd,
   try_to_double(AVG_MDCR_ALOWD_AMT::varchar)*try_to_double(TOT_SRVCS::varchar) a, try_to_double(TOT_BENES::varchar) bn
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER_AND_SERVI where HCPCS_CD between 'Q4100' and 'Q4399'),
p as (select n, ln, fn, typ, a1, city, st, round(sum(a)) ss, max(bn) mb, listagg(h||' '||hd||' $'||round(a/1e6,1)||'M', '; ') within group (order by a desc) codes from b group by 1,2,3,4,5,6,7)
select 'state' k, st, count(*)::varchar n, round(sum(ss))::varchar ss, null c1, null c2, null c3, null c4, null c5 from p group by st qualify row_number() over (order by sum(ss) desc) <= 8
union all
select * from (select 'az', n, ln||' '||fn, typ, a1, city, ss::varchar, mb::varchar, codes from p where st='AZ' order by ss desc limit 12)
