-- Subparts trap + clean industry peer group: who carries the auto-coating tag (MACT IIII) by industry code;
-- operating auto/truck assembly plants (NAICS 33611x/336120) with the tag: NOVs since 2019, median and max without Tesla
with sub as (select distinct PGM_SYS_ID from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_PROGRAM_SUBPARTS where AIR_PROGRAM_SUBPART_CODE like 'CAAMACTIIII%'),
fac as (select PGM_SYS_ID, FACILITY_NAME, STATE, NAICS_CODES, AIR_OPERATING_STATUS_CODE op from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES where PGM_SYS_ID in (select PGM_SYS_ID from sub)),
inf as (select PGM_SYS_ID, count(distinct ACTIVITY_ID) n from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_INFORMAL_ACTIONS
        where ACHIEVED_DATE between '2019-01-01' and '2026-07-31' and PGM_SYS_ID in (select PGM_SYS_ID from sub) group by 1),
j as (select fac.*, coalesce(inf.n,0) n, (NAICS_CODES like '%33611%' or NAICS_CODES like '%336120%') auto from fac left join inf using (PGM_SYS_ID))
select 'tag_by_industry' k, case when auto then 'auto assembly 33611x/336120' when NAICS_CODES like '%3363%' or NAICS_CODES like '%3362%' then 'auto parts/bodies 3362-3363'
  when NAICS_CODES like '%211%' or NAICS_CODES like '%486%' or NAICS_CODES like '%2212%' then 'oil and gas wells, pipelines, gas utilities'
  when NAICS_CODES like '%2211%' then 'power plants' else 'other' end a, count(*)::text b, null c, null d
from j group by 2
union all select 'auto_peers_operating', count(*)::text, median(iff(PGM_SYS_ID<>'CABAA00006001A1438', n, null))::text,
  max(iff(PGM_SYS_ID<>'CABAA00006001A1438', n, null))::text, sum(iff(PGM_SYS_ID<>'CABAA00006001A1438', n, 0))::text
from j where auto and op='OPR'
union all select * from (select 'auto_top', FACILITY_NAME, STATE, n::text, NAICS_CODES from j where auto and op='OPR' order by n desc limit 5)
