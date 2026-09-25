-- ICIS-Air sensitivity: HPV facilities with day zero before 2024-07-01 (so past EPA's 180-day window by far), still unresolved,
-- with NO formal action on file at any date (null settlement dates included), by state; denominator operating Title V sources
with v as (select PGM_SYS_ID, min(HPV_DAYZERO_DATE) dz from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_VIOLATION_HISTORY
           where ENF_RESPONSE_POLICY_CODE = 'HPV' and HPV_RESOLVED_DATE is null and HPV_DAYZERO_DATE < '2024-07-01' group by 1),
fa as (select PGM_SYS_ID, count(*) n, count_if(SETTLEMENT_ENTERED_DATE is null) n_nulldate from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS group by 1),
p as (select PGM_SYS_ID, max(iff(PROGRAM_CODE = 'CAATVP' and AIR_OPERATING_STATUS_CODE = 'OPR', 1, 0)) tv_opr, max(iff(AIR_OPERATING_STATUS_CODE = 'OPR', 1, 0)) any_opr
      from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_PROGRAMS group by 1),
f as (select PGM_SYS_ID, any_value(STATE) st from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES group by 1),
j as (select coalesce(f.st, '??') st, p.PGM_SYS_ID, coalesce(p.tv_opr, 0) tv_opr, coalesce(p.any_opr, 0) any_opr, v.dz, coalesce(fa.n, 0) fa_n, coalesce(fa.n_nulldate, 0) fa_null
      from p left join f on p.PGM_SYS_ID = f.PGM_SYS_ID left join v on p.PGM_SYS_ID = v.PGM_SYS_ID left join fa on p.PGM_SYS_ID = fa.PGM_SYS_ID)
select st, count_if(tv_opr = 1) tv_opr, count_if(dz is not null and any_opr = 1) open_old_operating, count_if(dz is not null and any_opr = 1 and fa_n = 0) open_old_no_fa_ever,
  count_if(dz is not null and any_opr = 1 and fa_n = 0 and tv_opr = 1) same_on_tv, min(iff(dz is not null and any_opr = 1 and fa_n = 0, dz, null)) oldest_dz,
  count_if(fa_null > 0) fac_with_nulldate_fa
from j group by rollup(st) having count_if(dz is not null and any_opr = 1) > 0 or st is null order by open_old_no_fa_ever desc nulls first;
