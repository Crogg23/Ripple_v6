with em as (
  select FACILITY_ID, sum(CO2E_EMISSION) co2e from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_GHGRP_EMISSION where REPORTING_YEAR = 2023 group by 1),
fac as (
  select FACILITY_ID, max(FRS_ID) frs, max(FACILITY_NAME) fname, max(PARENT_COMPANY) parent, max(STATE) st, max(NAICS_CODE) naics from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_GHGRP_FACILITY where REPORTING_YEAR = 2023 group by 1),
j as (
  select fac.*, em.co2e, e.COMPLIANCE_STATUS, e.QUARTERS_WITH_NONCOMPLIANCE, e.FORMAL_ACTION_COUNT, e.INFORMAL_ACTION_COUNT, e.PENALTY_COUNT, e.LAST_PENALTY_AMT_ALLOCATED, e.DATE_LAST_PENALTY, e.TOTAL_INSPECTION_COUNT, e.DATE_LAST_INSPECTION, e.PCT_MINORITY
  from em join fac using (FACILITY_ID) left join LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ECHO e on e.FRS_ID = fac.frs),
dec as (select j.*, ntile(10) over (order by co2e) d from j where frs is not null)
select d decile, count(*) facilities, round(avg(co2e)/1e6,2) avg_mt_co2e, round(100*avg(iff(COMPLIANCE_STATUS in ('Violation Identified','Significant Violation','Violation'),1,0)),1) pct_in_violation_now,
  round(avg(QUARTERS_WITH_NONCOMPLIANCE),1) avg_qtrs_noncompliance, round(100*avg(iff(FORMAL_ACTION_COUNT>0,1,0)),1) pct_formal_action, round(avg(TOTAL_INSPECTION_COUNT),1) avg_inspections, round(avg(PCT_MINORITY),1) pct_minority
from dec group by 1 order by 1;
with em as (
  select FACILITY_ID, sum(CO2E_EMISSION) co2e from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_GHGRP_EMISSION where REPORTING_YEAR = 2023 group by 1),
fac as (
  select FACILITY_ID, max(FRS_ID) frs, max(FACILITY_NAME) fname, max(PARENT_COMPANY) parent, max(STATE) st, max(NAICS_CODE) naics from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_GHGRP_FACILITY where REPORTING_YEAR = 2023 group by 1)
select fac.fname, fac.st, fac.parent, round(em.co2e/1e6,2) mt_co2e, e.COMPLIANCE_STATUS, e.QUARTERS_WITH_NONCOMPLIANCE qtrs_nc, e.FORMAL_ACTION_COUNT formal, e.PENALTY_COUNT pens, e.LAST_PENALTY_AMT_ALLOCATED last_pen, e.DATE_LAST_PENALTY, e.TOTAL_INSPECTION_COUNT insp, e.DATE_LAST_INSPECTION, e.PCT_MINORITY
from em join fac using (FACILITY_ID) left join LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ECHO e on e.FRS_ID = fac.frs
order by em.co2e desc limit 40
