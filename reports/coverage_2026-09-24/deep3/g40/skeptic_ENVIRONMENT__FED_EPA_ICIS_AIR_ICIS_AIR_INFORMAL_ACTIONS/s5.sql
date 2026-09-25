-- Bay Area district series 2005-2026: NOVs, facilities with NOVs, Tesla NOVs; district (L) formal actions, facilities, penalties (one per action)
with f as (select PGM_SYS_ID from {F} where LOCAL_CONTROL_REGION_NAME like 'Bay Area%'),
i as (select year(ACHIEVED_DATE) y, count(distinct ACTIVITY_ID) nov, count(distinct PGM_SYS_ID) fac_nov, count(distinct iff(PGM_SYS_ID='CABAA00006001A1438',ACTIVITY_ID,null)) tesla
   from {I} where PGM_SYS_ID in (select PGM_SYS_ID from f) and ACHIEVED_DATE between '2005-01-01' and '2026-07-31' group by 1),
a1 as (select ACTIVITY_ID, any_value(PGM_SYS_ID) p, max(SETTLEMENT_ENTERED_DATE) d, max(PENALTY_AMOUNT) pen from {A}
   where PGM_SYS_ID in (select PGM_SYS_ID from f) and STATE_EPA_FLAG='L' group by 1),
a as (select year(d) y, count(*) frm, count(distinct p) fac_frm, round(sum(pen)) pen from a1 where d between '2005-01-01' and '2026-09-24' group by 1)
select coalesce(i.y,a.y) y, i.nov, i.fac_nov, i.tesla, a.frm, a.fac_frm, a.pen from i full outer join a on i.y=a.y order by 1
