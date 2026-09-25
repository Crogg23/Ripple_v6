-- ICIS-Air by state: operating Title V sources (denominator, from the programs table), facilities with an HPV that began 2019-2022,
-- how many still have one open today, how many of those got no formal action since day zero; control: share of 2015-2018 HPV facilities ever resolved
with p as (select PGM_SYS_ID, max(iff(PROGRAM_CODE = 'CAATVP' and AIR_OPERATING_STATUS_CODE = 'OPR', 1, 0)) tv_opr,
             max(iff(AIR_OPERATING_STATUS_CODE = 'OPR', 1, 0)) any_opr
           from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_PROGRAMS group by 1),
f as (select PGM_SYS_ID, any_value(STATE) st from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES group by 1),
v as (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_VIOLATION_HISTORY where ENF_RESPONSE_POLICY_CODE = 'HPV'),
h as (select PGM_SYS_ID, min(HPV_DAYZERO_DATE) dz, count(*) n_hpv, count_if(HPV_RESOLVED_DATE is null) n_open
      from v where HPV_DAYZERO_DATE between '2019-01-01' and '2022-12-31' group by 1),
old as (select PGM_SYS_ID, count(*) n, count_if(HPV_RESOLVED_DATE is not null) n_res from v where HPV_DAYZERO_DATE between '2015-01-01' and '2018-12-31' group by 1),
fa as (select h.PGM_SYS_ID, count(a.ACTIVITY_ID) n_fa, sum(coalesce(a.PENALTY_AMOUNT, 0)) pen
       from h left join LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS a
         on a.PGM_SYS_ID = h.PGM_SYS_ID and a.SETTLEMENT_ENTERED_DATE >= h.dz group by 1),
u as (select PGM_SYS_ID from p union select PGM_SYS_ID from h union select PGM_SYS_ID from old),
j as (select u.PGM_SYS_ID, coalesce(f.st, '??') st, coalesce(p.tv_opr, 0) tv_opr, coalesce(p.any_opr, 0) any_opr,
        h.dz, h.n_hpv, h.n_open, fa.n_fa, fa.pen, old.n old_n, old.n_res old_res
      from u left join p on u.PGM_SYS_ID = p.PGM_SYS_ID left join f on u.PGM_SYS_ID = f.PGM_SYS_ID left join h on u.PGM_SYS_ID = h.PGM_SYS_ID
        left join fa on u.PGM_SYS_ID = fa.PGM_SYS_ID left join old on u.PGM_SYS_ID = old.PGM_SYS_ID)
select st, count_if(tv_opr = 1) tv_opr_fac, count_if(dz is not null) hpv_fac_19_22, count_if(dz is not null and tv_opr = 1) hpv_fac_tv,
  count_if(n_open > 0) open_fac, count_if(n_open > 0 and tv_opr = 1) open_fac_tv, count_if(n_open > 0 and coalesce(n_fa, 0) = 0) open_no_fa,
  count_if(n_open > 0 and any_opr = 0) open_fac_not_operating,
  count_if(dz is not null and coalesce(n_fa, 0) > 0) hpv_with_fa, sum(iff(dz is not null, pen, 0)) pen_since_dz,
  count_if(old_n > 0) old_fac, count_if(old_n > 0 and old_res > 0) old_fac_any_resolved, sum(old_n) old_hpv_rows, sum(old_res) old_res_rows
from j group by rollup(st) order by hpv_fac_19_22 desc nulls first;
