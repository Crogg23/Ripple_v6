-- s04 (= s03 fixed): state practice for HPVs that began 2015-2024: denominators, minor-source share, resolution with/without a formal action after day zero,
-- informal action within 30 days of day zero, formal/informal flow 2015-2026
with f as (select PGM_SYS_ID, any_value(STATE) st, any_value(AIR_POLLUTANT_CLASS_CODE) cls from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES group by 1),
p as (select PGM_SYS_ID, max(iff(PROGRAM_CODE = 'CAATVP' and AIR_OPERATING_STATUS_CODE = 'OPR', 1, 0)) tv_opr, max(iff(AIR_OPERATING_STATUS_CODE = 'OPR', 1, 0)) any_opr
      from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_PROGRAMS group by 1),
v as (select PGM_SYS_ID, ACTIVITY_ID, HPV_DAYZERO_DATE dz, HPV_RESOLVED_DATE rd from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_VIOLATION_HISTORY
      where ENF_RESPONSE_POLICY_CODE = 'HPV' and HPV_DAYZERO_DATE between '2015-01-01' and '2024-12-31'),
fa as (select PGM_SYS_ID, SETTLEMENT_ENTERED_DATE d from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS),
ia as (select PGM_SYS_ID, ACHIEVED_DATE d from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_INFORMAL_ACTIONS),
vfa as (select v.PGM_SYS_ID, v.ACTIVITY_ID, v.dz, count(fa.d) n from v left join fa on fa.PGM_SYS_ID = v.PGM_SYS_ID and fa.d >= v.dz group by 1, 2, 3),
via as (select v.PGM_SYS_ID, v.ACTIVITY_ID, v.dz, count(ia.d) n from v left join ia on ia.PGM_SYS_ID = v.PGM_SYS_ID and ia.d between dateadd('day', -30, v.dz) and dateadd('day', 30, v.dz) group by 1, 2, 3),
vx as (select v.*, vfa.n fa_after, via.n ia_near from v join vfa on v.PGM_SYS_ID = vfa.PGM_SYS_ID and v.ACTIVITY_ID = vfa.ACTIVITY_ID and v.dz = vfa.dz
         join via on v.PGM_SYS_ID = via.PGM_SYS_ID and v.ACTIVITY_ID = via.ACTIVITY_ID and v.dz = via.dz),
vs as (select f.st, count(*) hpv_rows, count(distinct vx.PGM_SYS_ID) hpv_fac, count(distinct iff(f.cls = 'MIN', vx.PGM_SYS_ID, null)) hpv_fac_min,
         count_if(rd is not null) resolved, count_if(rd is not null and fa_after = 0) resolved_no_fa, count_if(rd is null) open_rows,
         count_if(fa_after > 0) with_fa_after, count_if(ia_near > 0) ia_near_dz
       from vx left join f on vx.PGM_SYS_ID = f.PGM_SYS_ID group by 1),
den as (select f.st, count_if(p.any_opr = 1) opr_any, count_if(p.any_opr = 1 and f.cls = 'MAJ') opr_maj, count_if(p.tv_opr = 1) opr_tv
        from p left join f on p.PGM_SYS_ID = f.PGM_SYS_ID group by 1),
flow as (select f.st, count_if(year(fa.d) between 2015 and 2026) fa_15_26 from fa left join f on fa.PGM_SYS_ID = f.PGM_SYS_ID group by 1),
iflow as (select f.st, count_if(year(ia.d) between 2015 and 2026) ia_15_26 from ia left join f on ia.PGM_SYS_ID = f.PGM_SYS_ID group by 1),
j as (select den.st, den.opr_any, den.opr_maj, den.opr_tv, vs.hpv_fac, vs.hpv_fac_min, vs.hpv_rows, vs.resolved, vs.resolved_no_fa, vs.open_rows, vs.with_fa_after, vs.ia_near_dz,
        flow.fa_15_26, iflow.ia_15_26
      from den left join vs on den.st = vs.st left join flow on den.st = flow.st left join iflow on den.st = iflow.st)
select coalesce(st, 'ALL') st_, sum(opr_any) opr_any_, sum(opr_maj) opr_maj_, sum(opr_tv) opr_tv_, sum(hpv_fac) hpv_fac_, sum(hpv_fac_min) hpv_fac_min_, sum(hpv_rows) hpv_rows_,
  sum(resolved) resolved_, sum(resolved_no_fa) resolved_no_fa_, sum(open_rows) open_rows_, sum(with_fa_after) with_fa_after_, sum(ia_near_dz) ia_near_dz_,
  sum(fa_15_26) fa_15_26_, sum(ia_15_26) ia_15_26_
from j group by rollup(st) order by 7 desc nulls last;
