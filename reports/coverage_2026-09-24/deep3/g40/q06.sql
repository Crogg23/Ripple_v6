-- Peer group: every Bay Area AQMD facility with 20+ informal actions since 2010; formal actions and penalties (one penalty per action) since 2010; HPV rows
with fac as (select PGM_SYS_ID, FACILITY_NAME, CITY, AIR_POLLUTANT_CLASS_CODE cls, NAICS_CODES
             from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES where LOCAL_CONTROL_REGION_NAME like 'Bay Area%'),
inf as (select PGM_SYS_ID, count(distinct ACTIVITY_ID) n_inf, count(distinct ACHIEVED_DATE) d_inf,
          count(distinct iff(ACHIEVED_DATE>='2019-01-01', ACTIVITY_ID, null)) n_inf19
        from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_INFORMAL_ACTIONS
        where ACHIEVED_DATE between '2010-01-01' and '2026-07-31' and PGM_SYS_ID in (select PGM_SYS_ID from fac) group by 1),
fa1 as (select PGM_SYS_ID, ACTIVITY_ID, max(SETTLEMENT_ENTERED_DATE) d, max(PENALTY_AMOUNT) pen, any_value(STATE_EPA_FLAG) ag
        from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS
        where SETTLEMENT_ENTERED_DATE between '2010-01-01' and '2026-09-24' and PGM_SYS_ID in (select PGM_SYS_ID from fac) group by 1,2),
frm as (select PGM_SYS_ID, count(*) n_frm, count_if(d>='2019-01-01') n_frm19, round(sum(pen)) pen, max(d) last_frm, listagg(distinct ag,'') ags from fa1 group by 1),
vh as (select PGM_SYS_ID, count(HPV_DAYZERO_DATE) hpv, count_if(HPV_DAYZERO_DATE is not null and HPV_RESOLVED_DATE is null) hpv_open
       from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_VIOLATION_HISTORY where PGM_SYS_ID in (select PGM_SYS_ID from fac) group by 1)
select fac.FACILITY_NAME, fac.CITY, fac.cls, fac.NAICS_CODES, inf.n_inf, inf.d_inf, inf.n_inf19, coalesce(frm.n_frm,0) n_frm, coalesce(frm.n_frm19,0) n_frm19,
  frm.pen, frm.last_frm, frm.ags, round(100*coalesce(frm.n_frm,0)/inf.n_inf,1) frm_per_100_inf, vh.hpv, vh.hpv_open
from inf join fac using (PGM_SYS_ID) left join frm using (PGM_SYS_ID) left join vh using (PGM_SYS_ID)
where inf.n_inf >= 20 order by inf.n_inf desc
