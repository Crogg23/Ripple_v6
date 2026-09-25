-- Peer comparison by state: per facility informal vs formal counts since 2010; how often 5+ informal actions end with zero formal actions
with inf as (select PGM_SYS_ID, count(distinct ACTIVITY_ID) n_inf, count(distinct ACHIEVED_DATE) d_inf, min(ACHIEVED_DATE) f1, max(ACHIEVED_DATE) f2
             from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_INFORMAL_ACTIONS
             where ACHIEVED_DATE between '2010-01-01' and '2026-07-31' group by 1),
frm as (select PGM_SYS_ID, count(distinct ACTIVITY_ID) n_frm
        from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS
        where SETTLEMENT_ENTERED_DATE between '2010-01-01' and '2026-09-24' group by 1),
fac as (select PGM_SYS_ID, STATE, AIR_POLLUTANT_CLASS_CODE cls from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES),
j as (select coalesce(fac.STATE,'??') st, inf.*, coalesce(frm.n_frm,0) n_frm, fac.cls, fac.PGM_SYS_ID is not null landed
      from inf left join frm using (PGM_SYS_ID) left join fac using (PGM_SYS_ID))
select st, count(*) fac_inf, count_if(landed) landed, sum(n_inf) inf_acts, sum(n_frm) frm_acts_of_those,
  count_if(n_frm=0) fac_zero_formal, round(100*count_if(n_frm=0)/count(*),1) pct_zero,
  count_if(n_inf>=5) fac_5plus, count_if(n_inf>=5 and n_frm=0) fac_5plus_zero,
  round(100*count_if(n_inf>=5 and n_frm=0)/nullif(count_if(n_inf>=5),0),1) pct_5plus_zero,
  max(n_inf) max_inf, median(n_inf) med_inf,
  count_if(cls='MAJ') maj, count_if(cls='MAJ' and n_inf>=5 and n_frm=0) maj_5plus_zero
from j group by 1 order by fac_5plus desc
