-- Facilities: most informal actions since 2010 with zero formal actions since 2010, plus the top 8 overall; with class, status, HPV, violation rows
with inf as (select PGM_SYS_ID, count(distinct ACTIVITY_ID) n_inf, count(distinct ACHIEVED_DATE) d_inf, min(ACHIEVED_DATE) f1, max(ACHIEVED_DATE) f2,
               listagg(distinct STATE_EPA_FLAG,'') ag, count_if(ENF_TYPE_CODE='NOV') nov
             from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_INFORMAL_ACTIONS
             where ACHIEVED_DATE between '2010-01-01' and '2026-07-31' group by 1),
frm as (select PGM_SYS_ID, count(distinct ACTIVITY_ID) n_frm, count(distinct iff(SETTLEMENT_ENTERED_DATE>='2010-01-01', ACTIVITY_ID, null)) n_frm10,
          max(SETTLEMENT_ENTERED_DATE) last_frm
        from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS group by 1),
vh as (select PGM_SYS_ID, count(*) viol_rows, count(HPV_DAYZERO_DATE) hpv_rows, count_if(HPV_DAYZERO_DATE is not null and HPV_RESOLVED_DATE is null) hpv_open,
         max(EARLIEST_FRV_DETERM_DATE) last_frv
       from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_VIOLATION_HISTORY group by 1),
fac as (select PGM_SYS_ID, REGISTRY_ID, FACILITY_NAME, CITY, STATE, AIR_POLLUTANT_CLASS_CODE cls, AIR_OPERATING_STATUS_CODE op, CURRENT_HPV, NAICS_CODES, LOCAL_CONTROL_REGION_NAME lcr
        from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES),
j as (select inf.*, coalesce(frm.n_frm10,0) n_frm10, coalesce(frm.n_frm,0) n_frm_all, frm.last_frm, vh.viol_rows, vh.hpv_rows, vh.hpv_open, vh.last_frv, fac.*
      from inf left join frm using (PGM_SYS_ID) left join vh using (PGM_SYS_ID) left join fac using (PGM_SYS_ID))
select * from (select 'zero_formal' k, * from j where n_frm_all=0 order by n_inf desc limit 30)
union all select * from (select 'top_all' k, * from j order by n_inf desc limit 8)
