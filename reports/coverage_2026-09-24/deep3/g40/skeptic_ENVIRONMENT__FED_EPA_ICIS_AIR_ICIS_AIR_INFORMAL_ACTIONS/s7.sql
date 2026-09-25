-- Unit check since 2019: NOV rows vs facility-days by regulator, and for the 46 tagged auto plants (Tesla vs the rest)
with f as (select PGM_SYS_ID, NAICS_CODES, AIR_OPERATING_STATUS_CODE op, case when STATE='CA' then coalesce(LOCAL_CONTROL_REGION_NAME,'CA other') else STATE end jur from {F}),
i as (select PGM_SYS_ID, ACHIEVED_DATE, count(distinct ACTIVITY_ID) n from {I} where ACHIEVED_DATE between '2019-01-01' and '2026-07-31' group by 1,2),
sub as (select distinct PGM_SYS_ID from {S} where AIR_PROGRAM_SUBPART_CODE like 'CAAMACTIIII%'),
j as (select i.*, f.jur, (f.PGM_SYS_ID in (select PGM_SYS_ID from sub) and f.op='OPR' and (f.NAICS_CODES like '%33611%' or f.NAICS_CODES like '%336120%')) auto from i join f on f.PGM_SYS_ID=i.PGM_SYS_ID)
select * from (select 'jur' k, left(jur,20) a, sum(n) nov, count(*) fac_days, round(sum(n)/count(*),2) per_day, round(100*count_if(n>1)/count(*),1) pct_multi, max(n) max_day from j group by 2 order by sum(n) desc limit 14)
union all select 'auto', iff(PGM_SYS_ID='CABAA00006001A1438','Tesla','other 45'), sum(n), count(*), round(sum(n)/count(*),2), round(100*count_if(n>1)/count(*),1), max(n) from j where auto group by 2
