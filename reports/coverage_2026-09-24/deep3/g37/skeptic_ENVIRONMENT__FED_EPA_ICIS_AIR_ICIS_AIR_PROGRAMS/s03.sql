-- s03: state practice, HPVs that began 2015-2024. Denominators (operating any / major / Title V), class mix of HPV facilities,
-- how HPVs get resolved (with or without a formal action after day zero), informal action on/near day zero, and formal/informal flow 2015-2026.
with f as (select PGM_SYS_ID, any_value(STATE) st, any_value(AIR_POLLUTANT_CLASS_CODE) cls from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES group by 1),
p as (select PGM_SYS_ID, max(iff(PROGRAM_CODE = 'CAATVP' and AIR_OPERATING_STATUS_CODE = 'OPR', 1, 0)) tv_opr, max(iff(AIR_OPERATING_STATUS_CODE = 'OPR', 1, 0)) any_opr
      from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_PROGRAMS group by 1),
v as (select PGM_SYS_ID, ACTIVITY_ID, HPV_DAYZERO_DATE dz, HPV_RESOLVED_DATE rd from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_VIOLATION_HISTORY
      where ENF_RESPONSE_POLICY_CODE = 'HPV' and HPV_DAYZERO_DATE between '2015-01-01' and '2024-12-31'),
fa as (select PGM_SYS_ID, SETTLEMENT_ENTERED_DATE d from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS),
ia as (select PGM_SYS_ID, ACHIEVED_DATE d from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_INFORMAL_ACTIONS),
vx as (select v.*, (select count(*) from fa where fa.PGM_SYS_ID = v.PGM_SYS_ID and fa.d >= v.dz) fa_after,
              (select count(*) from ia where ia.PGM_SYS_ID = v.PGM_SYS_ID and ia.d between v.dz - 30 and v.dz + 30) ia_near
       from v),
vs as (select f.st, count(*) hpv_rows, count(distinct vx.PGM_SYS_ID) hpv_fac, count(distinct iff(f.cls = 'MIN', vx.PGM_SYS_ID, null)) hpv_fac_min,
         count_if(rd is not null) resolved, count_if(rd is not null and fa_after = 0) resolved_no_fa, count_if(rd is null) open_rows,
         count_if(fa_after > 0) with_fa_after, count_if(ia_near > 0) ia_near_dz
       from vx left join f on vx.PGM_SYS_ID = f.PGM_SYS_ID group by 1),
den as (select f.st, count_if(p.any_opr = 1) opr_any, count_if(p.any_opr = 1 and f.cls = 'MAJ') opr_maj, count_if(p.tv_opr = 1) opr_tv
        from p left join f on p.PGM_SYS_ID = f.PGM_SYS_ID group by 1),
flow as (select f.st, count_if(year(fa.d) between 2015 and 2026) fa_15_26 from fa left join f on fa.PGM_SYS_ID = f.PGM_SYS_ID group by 1),
iflow as (select f.st, count_if(year(ia.d) between 2015 and 2026) ia_15_26 from ia left join f on ia.PGM_SYS_ID = f.PGM_SYS_ID group by 1)
select coalesce(den.st,'ALL') st, sum(opr_any) opr_any, sum(opr_maj) opr_maj, sum(opr_tv) opr_tv, sum(hpv_fac) hpv_fac, sum(hpv_fac_min) hpv_fac_min, sum(hpv_rows) hpv_rows,
  sum(resolved) resolved, sum(resolved_no_fa) resolved_no_fa, sum(open_rows) open_rows, sum(with_fa_after) with_fa_after, sum(ia_near_dz) ia_near_dz,
  sum(fa_15_26) fa_15_26, sum(ia_15_26) ia_15_26
from den left join vs on den.st = vs.st left join flow on den.st = flow.st left join iflow on den.st = iflow.st
group by rollup(den.st) order by sum(hpv_rows) desc nulls last;
