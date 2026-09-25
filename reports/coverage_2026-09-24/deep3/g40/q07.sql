-- Tesla Fremont check: NOVs by year, every formal action on file, any second air ID for the plant, EPA civil cases on its FRS registry ID
with ids as (select PGM_SYS_ID, REGISTRY_ID, FACILITY_NAME, STREET_ADDRESS, AIR_POLLUTANT_CLASS_CODE cls
             from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES
             where (FACILITY_NAME ilike '%TESLA%' and STATE='CA') or REGISTRY_ID='110000482898'),
inf as (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_INFORMAL_ACTIONS where PGM_SYS_ID in (select PGM_SYS_ID from ids)),
frm as (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS where PGM_SYS_ID in (select PGM_SYS_ID from ids)),
vh as (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_VIOLATION_HISTORY where PGM_SYS_ID='CABAA00006001A1438')
select 'id' k, PGM_SYS_ID a, REGISTRY_ID b, FACILITY_NAME c, STREET_ADDRESS d, cls e,
  (select count(*) from inf where inf.PGM_SYS_ID=ids.PGM_SYS_ID)::text f, (select count(*) from frm where frm.PGM_SYS_ID=ids.PGM_SYS_ID)::text g from ids
union all select 'inf_year', PGM_SYS_ID, year(ACHIEVED_DATE)::text, count(distinct ACTIVITY_ID)::text, count(distinct ACHIEVED_DATE)::text, listagg(distinct ENF_TYPE_CODE,'|'), listagg(distinct STATE_EPA_FLAG,''), null from inf group by 2,3
union all select 'formal', PGM_SYS_ID, SETTLEMENT_ENTERED_DATE::text, ENF_TYPE_DESC, PENALTY_AMOUNT::text, STATE_EPA_FLAG, ENF_IDENTIFIER, ACTIVITY_ID from frm
union all select 'hpv_year', 'CABAA00006001A1438', year(HPV_DAYZERO_DATE)::text, count(*)::text, count_if(HPV_RESOLVED_DATE is null)::text, listagg(distinct ENF_RESPONSE_POLICY_CODE,'|'), left(listagg(distinct POLLUTANT_DESCS,'|'),120), left(listagg(distinct PROGRAM_CODES,'|'),120) from vh group by 3
union all select 'fec_case', CASE_NUMBER, ACTIVITY_ID, FACILITY_NAME, LOCATION_ADDRESS, CITY, REGISTRY_ID, null
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_CASE_FACILITIES where REGISTRY_ID='110000482898' or (FACILITY_NAME ilike '%TESLA%' and STATE_CODE='CA')
