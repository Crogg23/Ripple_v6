-- Bay Area backlog test: every district facility with 10+ NOVs 2019-2026-07, split old (2019-22) vs new (2023-26), formal actions since 2019 across sibling IDs on the registry
with f as (select PGM_SYS_ID, REGISTRY_ID, left(FACILITY_NAME,40) nm, CITY, AIR_POLLUTANT_CLASS_CODE cls from {F} where LOCAL_CONTROL_REGION_NAME like 'Bay Area%'),
inf as (select PGM_SYS_ID, count(distinct iff(ACHIEVED_DATE<'2023-01-01',ACTIVITY_ID,null)) n1922, count(distinct iff(ACHIEVED_DATE>='2023-01-01',ACTIVITY_ID,null)) n2326
   from {I} where ACHIEVED_DATE between '2019-01-01' and '2026-07-31' and PGM_SYS_ID in (select PGM_SYS_ID from f) group by 1),
frm as (select ff.REGISTRY_ID, count(distinct a.ACTIVITY_ID) n_frm19, count(distinct iff(a.STATE_EPA_FLAG='L',a.ACTIVITY_ID,null)) n_frm19_l, max(a.SETTLEMENT_ENTERED_DATE) last_frm
   from {A} a join {F} ff on a.PGM_SYS_ID=ff.PGM_SYS_ID
   where a.SETTLEMENT_ENTERED_DATE>='2019-01-01' and ff.REGISTRY_ID in (select REGISTRY_ID from f where REGISTRY_ID is not null) group by 1)
select f.PGM_SYS_ID, f.nm, f.CITY, f.cls, inf.n1922, inf.n2326, coalesce(frm.n_frm19,0) n_frm19, coalesce(frm.n_frm19_l,0) n_frm19_l, frm.last_frm
from inf join f on f.PGM_SYS_ID=inf.PGM_SYS_ID left join frm on frm.REGISTRY_ID=f.REGISTRY_ID
where inf.n1922+inf.n2326>=10 order by inf.n1922+inf.n2326 desc
