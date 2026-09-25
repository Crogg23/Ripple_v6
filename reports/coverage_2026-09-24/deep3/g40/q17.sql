-- Time by jurisdiction: informal actions (distinct activities) per year 2019-2025 and Jan-May 2024/2025/2026, top 25 issuers; Tesla Fremont share inside Bay Area AQMD
with f as (select PGM_SYS_ID, STATE, LOCAL_CONTROL_REGION_NAME lcr from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES),
i as (select a.ACTIVITY_ID, a.ACHIEVED_DATE d, year(a.ACHIEVED_DATE) y, month(a.ACHIEVED_DATE) m, a.PGM_SYS_ID,
        case when a.STATE_EPA_FLAG='E' then 'EPA' when a.STATE_EPA_FLAG='L' then coalesce(f.lcr, 'local ' || f.STATE) else 'state ' || f.STATE end jur
      from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_INFORMAL_ACTIONS a left join f using (PGM_SYS_ID)
      where a.ACHIEVED_DATE between '2019-01-01' and '2026-07-31')
select * from (select left(jur,45) jur,
  count(distinct iff(y=2019,ACTIVITY_ID,null)) y19, count(distinct iff(y=2020,ACTIVITY_ID,null)) y20, count(distinct iff(y=2021,ACTIVITY_ID,null)) y21,
  count(distinct iff(y=2022,ACTIVITY_ID,null)) y22, count(distinct iff(y=2023,ACTIVITY_ID,null)) y23, count(distinct iff(y=2024,ACTIVITY_ID,null)) y24,
  count(distinct iff(y=2025,ACTIVITY_ID,null)) y25,
  count(distinct iff(y=2024 and m<=5,ACTIVITY_ID,null)) jm24, count(distinct iff(y=2025 and m<=5,ACTIVITY_ID,null)) jm25, count(distinct iff(y=2026 and m<=5,ACTIVITY_ID,null)) jm26,
  count(distinct iff(y=2026 and m in (6,7),ACTIVITY_ID,null)) jj26, count(distinct iff(y=2025 and m in (6,7),ACTIVITY_ID,null)) jj25,
  count(distinct iff(PGM_SYS_ID='CABAA00006001A1438',ACTIVITY_ID,null)) tesla_all, count(distinct ACTIVITY_ID) all_n
from i group by 1 order by all_n desc limit 25)
union all
select 'ALL', count(distinct iff(y=2019,ACTIVITY_ID,null)), count(distinct iff(y=2020,ACTIVITY_ID,null)), count(distinct iff(y=2021,ACTIVITY_ID,null)),
  count(distinct iff(y=2022,ACTIVITY_ID,null)), count(distinct iff(y=2023,ACTIVITY_ID,null)), count(distinct iff(y=2024,ACTIVITY_ID,null)), count(distinct iff(y=2025,ACTIVITY_ID,null)),
  count(distinct iff(y=2024 and m<=5,ACTIVITY_ID,null)), count(distinct iff(y=2025 and m<=5,ACTIVITY_ID,null)), count(distinct iff(y=2026 and m<=5,ACTIVITY_ID,null)),
  count(distinct iff(y=2026 and m in (6,7),ACTIVITY_ID,null)), count(distinct iff(y=2025 and m in (6,7),ACTIVITY_ID,null)),
  count(distinct iff(PGM_SYS_ID='CABAA00006001A1438',ACTIVITY_ID,null)), count(distinct ACTIVITY_ID) from i
