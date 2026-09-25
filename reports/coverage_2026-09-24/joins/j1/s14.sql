-- [rerun, numeric columns] OSHA 300A injury summaries 2023-2025, MO nursing homes (NAICS 623110): match to Reliant homes on name prefix + city (or company name RELIANT); injury rate per 100 FTE vs other MO nursing homes; hours sanity 500-4500 per worker
with n as (select distinct PROVIDER_NAME, upper(CITY) city, regexp_replace(upper(PROVIDER_NAME),'[^A-Z0-9]','') k from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME where CHAIN_ID='446' and STATE='MO'),
a as (select 2023 yr, ESTABLISHMENT_NAME, COMPANY_NAME, EIN, upper(CITY) city, STREET_ADDRESS, ANNUAL_AVERAGE_EMPLOYEES emp, TOTAL_HOURS_WORKED hrs, TOTAL_DAFW_CASES dafw, TOTAL_DJTR_CASES djtr, TOTAL_OTHER_CASES oth, TOTAL_DEATHS deaths from LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2023 where STATE='MO' and NAICS_CODE::varchar='623110'
  union all select 2024, ESTABLISHMENT_NAME, COMPANY_NAME, EIN, upper(CITY), STREET_ADDRESS, ANNUAL_AVERAGE_EMPLOYEES, TOTAL_HOURS_WORKED, TOTAL_DAFW_CASES, TOTAL_DJTR_CASES, TOTAL_OTHER_CASES, TOTAL_DEATHS from LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2024 where STATE='MO' and NAICS_CODE::varchar='623110'
  union all select 2025, ESTABLISHMENT_NAME, COMPANY_NAME, EIN, upper(CITY), STREET_ADDRESS, ANNUAL_AVERAGE_EMPLOYEES, TOTAL_HOURS_WORKED, TOTAL_DAFW_CASES, TOTAL_DJTR_CASES, TOTAL_OTHER_CASES, TOTAL_DEATHS from LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2025 where STATE='MO' and NAICS_CODE::varchar='623110'),
m as (select a.*, n.PROVIDER_NAME matched_home from a left join n on regexp_replace(upper(a.ESTABLISHMENT_NAME),'[^A-Z0-9]','') like n.k||'%' and a.city=n.city),
f as (select *, iff(matched_home is not null or COMPANY_NAME ilike '%RELIANT CARE%', 'reliant', 'other_mo_623110') grp from m
  where coalesce(emp::float,0)>0 and coalesce(hrs::float,0)/coalesce(emp::float,0) between 500 and 4500)
select grp, yr, count(*) filings, count(distinct matched_home) homes, sum(coalesce(emp::float,0)) emp, sum(coalesce(hrs::float,0)) hrs,
  sum(coalesce(dafw::float,0)+coalesce(djtr::float,0)+coalesce(oth::float,0)) cases, sum(coalesce(dafw::float,0)) dafw,
  round(200000*sum(coalesce(dafw::float,0)+coalesce(djtr::float,0)+coalesce(oth::float,0))/sum(coalesce(hrs::float,0)),2) trir, round(200000*sum(coalesce(dafw::float,0))/sum(coalesce(hrs::float,0)),2) dafw_rate,
  listagg(distinct iff(grp='reliant', ESTABLISHMENT_NAME||'|'||COMPANY_NAME||'|'||EIN, null), '; ') reliant_names
from f group by 1,2 order by 1,2
