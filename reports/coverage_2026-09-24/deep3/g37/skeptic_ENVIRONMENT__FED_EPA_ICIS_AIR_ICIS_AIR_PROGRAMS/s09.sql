-- s09: sensitivity of "NE 24 of 66". Day-zero cutoffs 2021-07-01 / 2022-07-01 / 2023-07-01 / 2024-07-01; "no formal action ever" vs "none since day zero";
-- all operating facilities vs operating Title V only; NE share at each; also distinct registry IDs (one site, two program IDs).
with v as (select PGM_SYS_ID, HPV_DAYZERO_DATE dz from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_VIOLATION_HISTORY
           where ENF_RESPONSE_POLICY_CODE = 'HPV' and HPV_RESOLVED_DATE is null),
c as (select column1::date cut from values ('2021-07-01'), ('2022-07-01'), ('2023-07-01'), ('2024-07-01')),
vc as (select c.cut, v.PGM_SYS_ID, min(v.dz) dz from v join c on v.dz < c.cut group by 1, 2),
p as (select PGM_SYS_ID, max(iff(PROGRAM_CODE = 'CAATVP' and AIR_OPERATING_STATUS_CODE = 'OPR', 1, 0)) tv_opr, max(iff(AIR_OPERATING_STATUS_CODE = 'OPR', 1, 0)) any_opr
      from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_PROGRAMS group by 1),
f as (select PGM_SYS_ID, any_value(STATE) st, any_value(REGISTRY_ID) reg from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES group by 1),
fa as (select vc.cut, vc.PGM_SYS_ID, count(a.ACTIVITY_ID) n_all, count_if(a.SETTLEMENT_ENTERED_DATE >= vc.dz) n_since
       from vc left join LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS a on a.PGM_SYS_ID = vc.PGM_SYS_ID group by 1, 2),
j as (select vc.cut, vc.PGM_SYS_ID, f.st, f.reg, p.tv_opr, fa.n_all, fa.n_since from vc join p on vc.PGM_SYS_ID = p.PGM_SYS_ID and p.any_opr = 1
        left join f on vc.PGM_SYS_ID = f.PGM_SYS_ID join fa on vc.cut = fa.cut and vc.PGM_SYS_ID = fa.PGM_SYS_ID)
select cut,
  count_if(st = 'NE' and n_all = 0) || ' of ' || count_if(n_all = 0) ever_all,
  count_if(st = 'NE' and n_all = 0 and tv_opr = 1) || ' of ' || count_if(n_all = 0 and tv_opr = 1) ever_tv,
  count_if(st = 'NE' and n_since = 0) || ' of ' || count_if(n_since = 0) since_all,
  count_if(st = 'NE' and n_since = 0 and tv_opr = 1) || ' of ' || count_if(n_since = 0 and tv_opr = 1) since_tv,
  count(distinct iff(st = 'NE' and n_all = 0, reg, null)) || ' of ' || count(distinct iff(n_all = 0, reg, null)) ever_all_regids,
  count_if(st = 'NE') || ' of ' || count(*) open_opr_any_action
from j group by 1 order by 1;
