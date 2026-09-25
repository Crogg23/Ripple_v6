-- s08: is ECHO a second witness or the same one? ECHO rows (by registry ID) for (a) operating facilities with an open HPV begun before mid-2024,
-- (b) the NE 24, (c) operating air facilities with CURRENT_HPV 'No Violation Identified'. If (a) is ~all 12-of-12 "Significant Violation", ECHO is echoing the HPV flag.
with v as (select PGM_SYS_ID, min(HPV_DAYZERO_DATE) dz from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_VIOLATION_HISTORY
           where ENF_RESPONSE_POLICY_CODE = 'HPV' and HPV_RESOLVED_DATE is null and HPV_DAYZERO_DATE < '2024-07-01' group by 1),
p as (select PGM_SYS_ID, max(iff(AIR_OPERATING_STATUS_CODE = 'OPR', 1, 0)) any_opr from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_PROGRAMS group by 1),
fa as (select distinct PGM_SYS_ID from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS),
f as (select PGM_SYS_ID, any_value(STATE) st, any_value(REGISTRY_ID) reg, any_value(CURRENT_HPV) chpv from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES group by 1),
grp as (
  select 'a_open_old_hpv' g, f.reg from v join p on v.PGM_SYS_ID = p.PGM_SYS_ID join f on v.PGM_SYS_ID = f.PGM_SYS_ID where p.any_opr = 1
  union all select 'b_ne_24', f.reg from v join p on v.PGM_SYS_ID = p.PGM_SYS_ID join f on v.PGM_SYS_ID = f.PGM_SYS_ID left join fa on v.PGM_SYS_ID = fa.PGM_SYS_ID
    where p.any_opr = 1 and f.st = 'NE' and fa.PGM_SYS_ID is null
  union all select 'c_no_violation', f.reg from f join p on f.PGM_SYS_ID = p.PGM_SYS_ID where p.any_opr = 1 and f.chpv = 'No Violation Identified'),
e as (select FRS_ID, max(QUARTERS_WITH_NONCOMPLIANCE) qnc, max(FORMAL_ACTION_COUNT) fac, max(iff(COMPLIANCE_STATUS ilike 'Significant%', 1, 0)) sv, count(*) erows
      from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ECHO group by 1)
select grp.g, count(*) fac_n, count(e.FRS_ID) in_echo, count_if(e.qnc = 12) qnc12, count_if(e.sv = 1) sig_viol, count_if(e.qnc = 12 and e.sv = 1) both_,
  count_if(e.fac = 0) echo_fa0, round(avg(e.qnc), 2) avg_qnc, max(e.erows) max_echo_rows
from grp left join e on grp.reg = e.FRS_ID group by 1 order by 1;
