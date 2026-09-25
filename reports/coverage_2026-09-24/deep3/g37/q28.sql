-- Robustness for the NPDES lead against a second table: six-year chronic individual permits with no NPDES formal action,
-- joined to ECHO by FRS ID. How many does ECHO say had any formal action (any program), and do those sites also carry drinking-water or air programs?
with q as (
  select NPDES_ID, substr(NPDES_ID, 1, 2) st,
    count_if(YEARQTR between '20233' and '20262' and try_to_number(NUME90_Q) > 0) qa,
    count_if(YEARQTR between '20203' and '20232' and try_to_number(NUME90_Q) > 0) qb
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_QNCR_HISTORY
  where YEARQTR between '20203' and '20262' and substr(NPDES_ID, 3, 1) = '0' group by 1, 2 having qa >= 8 and qb >= 8),
fa as (select distinct NPDES_ID from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_FORMAL_ENFORCEMENT_ACTIONS),
f as (select NPDES_ID, FACILITY_UIN from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_ICIS_FACILITIES),
j as (select iff(q.st in ('MO', 'OH'), q.st, 'REST') grp, q.NPDES_ID, e.FRS_ID, e.FORMAL_ACTION_COUNT fac, e.DATE_LAST_FORMAL_ACTION dlfa,
        e.HAS_DRINKING_WATER_PROGRAM dw, e.HAS_AIR_PROGRAM air, e.HAS_HAZWASTE_PROGRAM rcra, e.QUARTERS_WITH_NONCOMPLIANCE qnc
      from q left join fa on q.NPDES_ID = fa.NPDES_ID left join f on q.NPDES_ID = f.NPDES_ID left join LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ECHO e on f.FACILITY_UIN = e.FRS_ID
      where fa.NPDES_ID is null)
select grp, count(*) no_npdes_formal, count(FRS_ID) in_echo, count_if(fac > 0) echo_formal_any, count_if(fac > 0 and dlfa >= '2021-07-01') echo_formal_recent,
  count_if(fac > 0 and (dw or air or rcra)) echo_formal_multi_program, count_if(fac > 0 and not (coalesce(dw, false) or coalesce(air, false) or coalesce(rcra, false))) echo_formal_water_only,
  count_if(qnc >= 8) echo_qnc8
from j group by rollup(grp) order by grp;
