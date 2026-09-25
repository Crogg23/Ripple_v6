-- ICIS-Air programs: program x status, date text parse, the default date, mixed statuses per facility, duplicate rows
with t as (select *, try_to_date(BEGIN_DATE,'MM/DD/YYYY') bd, try_to_date(UPDATED_DATE,'MM/DD/YYYY') ud from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_PROGRAMS),
f as (select PGM_SYS_ID, count(distinct AIR_OPERATING_STATUS_CODE) nst, count(*) n, count(distinct PROGRAM_CODE) np from t group by 1)
select 'profile' k, count(*)::text a, count(distinct PGM_SYS_ID)::text b, count_if(bd is null and BEGIN_DATE is not null)::text c, count_if(BEGIN_DATE is null)::text d,
  count_if(BEGIN_DATE='10/19/2014')::text e, count_if(ud is null)::text f, (select count_if(nst>1)||' mixed; '||count_if(n>np)||' dup-program' from f) g from t
union all select 'pgm_status', PROGRAM_CODE, AIR_OPERATING_STATUS_CODE, count(*)::text, count(distinct PGM_SYS_ID)::text, count_if(BEGIN_DATE='10/19/2014')::text, null, null from t group by 2,3
union all select 'begin_yr', year(bd)::text, count(*)::text, count_if(PROGRAM_CODE='CAATVP')::text, count_if(AIR_OPERATING_STATUS_CODE='CLS')::text, null, null, null from t group by 2
union all select 'upd_yr', year(ud)::text, count(*)::text, count_if(AIR_OPERATING_STATUS_CODE='CLS')::text, count_if(AIR_OPERATING_STATUS_CODE='OPR')::text, null, null, null from t group by 2
union all select * from (select 'topbegin', BEGIN_DATE, count(*)::text, null, null, null, null, null from t group by 2 order by count(*) desc limit 8);
