-- NPDES SIC and NAICS crosswalks: primary-flag sanity, duplicates, permit type (3rd character), land rate in the NPDES facility table
with s as (select NPDES_ID, SIC_CODE code, PRIMARY_INDICATOR_FLAG f, SIC_DESC d from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_SICS),
n as (select NPDES_ID, NAICS_CODE code, PRIMARY_INDICATOR_FLAG f, NAICS_DESC d from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_NAICS),
fac as (select distinct NPDES_ID from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_ICIS_FACILITIES),
sp as (select NPDES_ID, count(*) k, count(distinct code) kd, count_if(f='Y') y from s group by 1),
np as (select NPDES_ID, count(*) k, count(distinct code) kd, count_if(f='Y') y from n group by 1),
prof as (
  select 'SIC' t, count(*) permits, count_if(y=0) no_primary, count_if(y=1) one_primary, count_if(y>1) multi_primary, max(k) max_rows, count_if(k>kd) permits_with_dupe_code,
    count_if(substr(NPDES_ID,3,1) = 'R') third_r, count_if(substr(NPDES_ID,3,1) = 'G') third_g, count_if(substr(NPDES_ID,3,1) = '0') third_0,
    count_if(NPDES_ID in (select NPDES_ID from fac)) in_fac, count_if(NPDES_ID in (select NPDES_ID from np)) in_other from sp
  union all
  select 'NAICS', count(*), count_if(y=0), count_if(y=1), count_if(y>1), max(k), count_if(k>kd),
    count_if(substr(NPDES_ID,3,1) = 'R'), count_if(substr(NPDES_ID,3,1) = 'G'), count_if(substr(NPDES_ID,3,1) = '0'),
    count_if(NPDES_ID in (select NPDES_ID from fac)), count_if(NPDES_ID in (select NPDES_ID from sp)) from np),
codes as (
  select 'SIC_codes' t, count(distinct code) permits, count(distinct code||'|'||coalesce(d,'')) no_primary, count_if(code is null or trim(code)='') one_primary,
    count_if(f not in ('Y','N') or f is null) multi_primary, count_if(len(trim(code))<>4) max_rows, count(*) - count(distinct NPDES_ID, code, f) permits_with_dupe_code,
    null third_r, null third_g, null third_0, (select count(*) from fac) in_fac, null in_other from s
  union all
  select 'NAICS_codes', count(distinct code), count(distinct code||'|'||coalesce(d,'')), count_if(code is null or trim(code)=''),
    count_if(f not in ('Y','N') or f is null), count_if(len(trim(code))<>6), count(*) - count(distinct NPDES_ID, code, f), null, null, null, null, null from n),
top as (select 'SIC_top:' || NPDES_ID t, k permits, y no_primary, kd one_primary, null multi_primary, null max_rows, null permits_with_dupe_code, null third_r, null third_g, null third_0, null in_fac, null in_other
  from sp order by k desc limit 3)
select * from prof union all select * from codes union all select * from top
