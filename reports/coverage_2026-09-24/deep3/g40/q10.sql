-- Industry peers from the subparts table: every facility tagged with the auto/light-truck surface coating rule (MACT IIII),
-- NOVs and formal actions since 2019 (formal counted across all air IDs sharing the FRS registry ID); plus Tesla's own tags
with sub as (select distinct PGM_SYS_ID from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_PROGRAM_SUBPARTS
             where AIR_PROGRAM_SUBPART_CODE like 'CAAMACTIIII%'),
fac as (select PGM_SYS_ID, REGISTRY_ID, FACILITY_NAME, CITY, STATE, AIR_POLLUTANT_CLASS_CODE cls, AIR_OPERATING_STATUS_CODE op
        from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES),
grp as (select f.* from fac f where f.PGM_SYS_ID in (select PGM_SYS_ID from sub) or f.REGISTRY_ID='110000482898'),
inf as (select PGM_SYS_ID, count(distinct ACTIVITY_ID) n_inf19 from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_INFORMAL_ACTIONS
        where ACHIEVED_DATE between '2019-01-01' and '2026-07-31' and PGM_SYS_ID in (select PGM_SYS_ID from grp) group by 1),
frm_reg as (select f.REGISTRY_ID, count(distinct a.ACTIVITY_ID) n_frm19, sum(a.PENALTY_AMOUNT) pen19
            from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS a join fac f using (PGM_SYS_ID)
            where a.SETTLEMENT_ENTERED_DATE >= '2019-01-01' and f.REGISTRY_ID in (select REGISTRY_ID from grp) group by 1)
select 'peer' k, g.FACILITY_NAME, g.CITY, g.STATE, g.cls, g.op, coalesce(inf.n_inf19,0) n_inf19, coalesce(fr.n_frm19,0) n_frm19_registry, round(fr.pen19) pen19_registry,
  iff(g.PGM_SYS_ID in (select PGM_SYS_ID from sub),'IIII','not tagged') tag
from grp g left join inf using (PGM_SYS_ID) left join frm_reg fr on fr.REGISTRY_ID=g.REGISTRY_ID
order by n_inf19 desc
