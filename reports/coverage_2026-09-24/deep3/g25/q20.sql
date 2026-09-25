-- EPA informal: Osage-county wells (Region 6 SDWA via ICIS) vs every other informal action, by year; formal EPA cases naming those wells by case-number year;
-- and how many of the wells carry the OS (Osage) well-name prefix in ECHO
with w as (select distinct REGISTRY_ID from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_EPA_INFORMAL_ENFORCEMENT_ACTIONS
           where left(ENF_IDENTIFIER,2) = '06' and STATUTE = 'SDWA' and PGM_SYS_ACRNM = 'ICIS'),
inf as (select year(ACHIEVED_DATE) yr, count(distinct iff(w.REGISTRY_ID is null, ENF_IDENTIFIER, null)) other_actions,
          count(distinct iff(w.REGISTRY_ID is null and i.PGM_SYS_ACRNM = 'ICIS', ENF_IDENTIFIER, null)) other_icis_actions,
          count(distinct iff(w.REGISTRY_ID is not null, ENF_IDENTIFIER, null)) osage_actions
        from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_EPA_INFORMAL_ENFORCEMENT_ACTIONS i left join w on w.REGISTRY_ID = i.REGISTRY_ID
        where year(ACHIEVED_DATE) >= 2015 group by 1),
cs as (select try_to_number(split_part(CASE_NUMBER, '-', 2)) yr, count(distinct CASE_NUMBER) osage_cases, count(distinct cf.REGISTRY_ID) osage_case_wells
       from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_CASE_FACILITIES cf join w on w.REGISTRY_ID = cf.REGISTRY_ID group by 1),
nm as (select count(*) wells_in_echo, count_if(FACILITY_NAME like 'OS%') os_prefix, count_if(STATE = 'OK') in_ok, count_if(IS_ON_TRIBAL_LAND) tribal
       from (select FRS_ID, max(FACILITY_NAME) FACILITY_NAME, max(STATE) STATE, max(IS_ON_TRIBAL_LAND::int)::boolean IS_ON_TRIBAL_LAND
             from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ECHO where FRS_ID in (select REGISTRY_ID from w) group by 1))
select coalesce(inf.yr, cs.yr) yr, inf.osage_actions, inf.other_actions, inf.other_icis_actions, cs.osage_cases, cs.osage_case_wells,
  nm.wells_in_echo, nm.os_prefix, nm.in_ok, nm.tribal
from inf full outer join cs on cs.yr = inf.yr cross join nm where coalesce(inf.yr, cs.yr) >= 2015 order by 1
