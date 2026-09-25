-- s06: did Nebraska's violations rise in 2019, or only its HPV designations? By year 2012-2026: HPVs by day-zero year, NOVs, warning letters,
-- formal actions, full compliance evaluations, failed stack tests. Nebraska vs its EPA Region 7 neighbours (IA, KS, MO).
with f as (select PGM_SYS_ID, any_value(STATE) st from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES group by 1),
g as (select PGM_SYS_ID, iff(st = 'NE', 'NE', 'R7_IA_KS_MO') grp from f where st in ('NE', 'IA', 'KS', 'MO')),
e as (
  select g.grp, year(v.HPV_DAYZERO_DATE) y, 'hpv' ev, v.PGM_SYS_ID id from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_VIOLATION_HISTORY v join g on v.PGM_SYS_ID = g.PGM_SYS_ID where v.ENF_RESPONSE_POLICY_CODE = 'HPV'
  union all select g.grp, year(v.EARLIEST_FRV_DETERM_DATE), 'frv', v.PGM_SYS_ID from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_VIOLATION_HISTORY v join g on v.PGM_SYS_ID = g.PGM_SYS_ID where v.ENF_RESPONSE_POLICY_CODE = 'FRV'
  union all select g.grp, year(i.ACHIEVED_DATE), iff(i.ENF_TYPE_DESC ilike '%notice of violation%', 'nov', iff(i.ENF_TYPE_DESC ilike '%warning%', 'wl', 'ia_other')), i.PGM_SYS_ID from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_INFORMAL_ACTIONS i join g on i.PGM_SYS_ID = g.PGM_SYS_ID
  union all select g.grp, year(a.SETTLEMENT_ENTERED_DATE), 'fa', a.PGM_SYS_ID from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS a join g on a.PGM_SYS_ID = g.PGM_SYS_ID
  union all select g.grp, year(c.ACTUAL_END_DATE), 'fce', c.PGM_SYS_ID from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FCES_PCES c join g on c.PGM_SYS_ID = g.PGM_SYS_ID where c.COMP_MONITOR_TYPE_DESC ilike '%full%' or c.COMP_MONITOR_TYPE_CODE = 'FOO'
  union all select g.grp, year(s.ACTUAL_END_DATE), iff(s.AIR_STACK_TEST_STATUS_DESC ilike '%fail%', 'stk_fail', 'stk_other'), s.PGM_SYS_ID from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_STACK_TESTS s join g on s.PGM_SYS_ID = g.PGM_SYS_ID)
select grp, y, count_if(ev = 'hpv') hpv, count(distinct iff(ev = 'hpv', id, null)) hpv_fac, count_if(ev = 'frv') frv, count_if(ev = 'nov') nov, count_if(ev = 'wl') wl, count_if(ev = 'ia_other') ia_other,
  count_if(ev = 'fa') fa, count_if(ev = 'fce') fce, count_if(ev = 'stk_fail') stk_fail, count_if(ev = 'stk_other') stk_other
from e where y between 2012 and 2026 group by 1, 2 order by 1, 2;
