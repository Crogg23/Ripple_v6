-- PHMSA flagged incidents: NRC report number fill and format, years, and land rate into both NRC copies
with ph as (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_PHMSA_FLAGGED_INCIDENTS),
s as (select distinct SEQNOS from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_USCG_NRC_INCIDENT_REPORTS),
m as (select distinct SEQNOS from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_USCG_NRC_INCIDENTS)
select INCIDENT_YEAR k, REPORT_TYPE a, count(*) n, count(distinct REPORT_NUMBER) reports, count_if(nullif(trim(NRC_REPORT_NUMBER), '') is not null) nrc_filled,
  count_if(trim(NRC_REPORT_NUMBER) in (select SEQNOS from s)) in_secondary, count_if(trim(NRC_REPORT_NUMBER) in (select SEQNOS from m)) in_main,
  min(NRC_REPORT_NUMBER) mn, max(NRC_REPORT_NUMBER) mx, sum(TOTAL_FATALITIES) fat, sum(TOTAL_INJURIES) inj
from ph group by 1, 2 order by 1, 2;
