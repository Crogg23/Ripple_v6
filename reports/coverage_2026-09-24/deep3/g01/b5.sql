-- @echo_sterilizers
select frs_id, facility_name, city, state, county, fips_code, pct_minority, population_density,
  compliance_status, significant_noncompliance_flag, quarters_with_noncompliance, three_yr_compliance_history,
  total_inspection_count, date_last_inspection, informal_action_count, formal_action_count,
  date_last_formal_action, total_penalties, penalty_count, last_penalty_amt, date_last_penalty,
  tri_on_site_releases, is_major_facility
from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ECHO
where frs_id in ('110000332015','110000334745','110000349720','110000352706','110000357827','110000403242','110000466488','110000469065','110000472541','110000478162','110000479740','110000498168','110000499425','110000882466','110001260803','110001638032','110001742419','110002131014','110002338738','110006625474','110009356464','110010307373','110014421438','110015320543','110018354010','110019608735','110024942678','110031315903','110035029313','110037143203','110055923336','110062088636','110066023145','110070557911','110070848179','110071091875','110071440424','110071673291','110071778836','110071786584','110071854207','110071854691','110071947898')
-- @eto_tri_gap_check
select registry_id, pgm_sys_acrnm, reporting_year::int yr, count(*) n_rows,
  count_if(pollutant_name = 'Ethylene oxide') eto_rows
from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_AIR_EMISSIONS_POLL_RPT_COMBINED_EMISSIONS
where registry_id in ('110031315903','110000499425','110000349720','110015320543','110000472541','110002338738')
group by 1,2,3 order by 1,2,3
-- @faers_drugnames
select upper(trim(drugname)) dn, count(*) n, count_if(role_cod = 'PS') ps,
  count(distinct src_quarter) quarters, count(*) over () distinct_names
from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_DRUG
group by 1
qualify row_number() over (order by count(*) desc) <= 40
-- @faers_demo_occp
select left(src_quarter,4) yr, occp_cod, count(*) n,
  count_if(gndr_cod in ('M','F')) sex_mf, count_if(gndr_cod in ('Y','N')) sex_yn,
  count_if(i_f_cod in ('I','F') or i_f_code in ('I','F')) if_ok
from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_DEMO
group by 1,2 order by 1,3 desc
