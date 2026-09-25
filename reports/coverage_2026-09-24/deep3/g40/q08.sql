-- Hostile check on "many NOVs, zero formal": for facilities with 10+ informal actions since 2010 and no formal action on their own air ID,
-- look for formal air actions on a sibling air ID with the same FRS registry ID, and EPA civil cases on that registry ID
with fac as (select PGM_SYS_ID, REGISTRY_ID, FACILITY_NAME, CITY, STATE, AIR_POLLUTANT_CLASS_CODE cls
             from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES),
inf as (select PGM_SYS_ID, count(distinct ACTIVITY_ID) n_inf
        from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_INFORMAL_ACTIONS
        where ACHIEVED_DATE between '2010-01-01' and '2026-07-31' group by 1 having count(distinct ACTIVITY_ID)>=10),
frm_id as (select PGM_SYS_ID, count(distinct ACTIVITY_ID) n, max(SETTLEMENT_ENTERED_DATE) last_d, sum(PENALTY_AMOUNT) pen
           from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS group by 1),
zero as (select inf.PGM_SYS_ID, inf.n_inf, fac.REGISTRY_ID, fac.FACILITY_NAME, fac.CITY, fac.STATE, fac.cls
         from inf join fac using (PGM_SYS_ID) left join frm_id using (PGM_SYS_ID) where frm_id.PGM_SYS_ID is null),
sib as (select z.PGM_SYS_ID, count(distinct f2.PGM_SYS_ID) sib_ids, sum(fr.n) sib_formal, max(fr.last_d) sib_last, sum(fr.pen) sib_pen
        from zero z join fac f2 on f2.REGISTRY_ID=z.REGISTRY_ID and f2.PGM_SYS_ID<>z.PGM_SYS_ID
        left join frm_id fr on fr.PGM_SYS_ID=f2.PGM_SYS_ID group by 1),
fec as (select z.PGM_SYS_ID, count(distinct c.CASE_NUMBER) cases, listagg(distinct c.CASE_NUMBER, ' ') case_list
        from zero z join LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_CASE_FACILITIES c on c.REGISTRY_ID=z.REGISTRY_ID group by 1)
select 'summary' k, count(*)::text a, count_if(sib.sib_formal>0)::text b, count_if(fec.cases>0)::text c,
  count_if(coalesce(sib.sib_formal,0)=0 and coalesce(fec.cases,0)=0)::text d, count_if(z.REGISTRY_ID is null)::text e, null f, null g, null h
from zero z left join sib using (PGM_SYS_ID) left join fec using (PGM_SYS_ID)
union all
select * from (select 'row', z.FACILITY_NAME, z.STATE, z.n_inf::text, z.cls, coalesce(sib.sib_formal,0)::text, sib.sib_last::text, coalesce(fec.cases,0)::text, left(fec.case_list,80)
from zero z left join sib using (PGM_SYS_ID) left join fec using (PGM_SYS_ID) order by z.n_inf desc limit 30)
