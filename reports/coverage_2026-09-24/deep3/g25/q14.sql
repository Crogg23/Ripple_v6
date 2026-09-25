-- EPA informal: Region 6 SDWA notices via ICIS (the Osage-county injection wells), by year: rows vs distinct actions vs wells;
-- EPA inspections of the same wells by year (ICIS-FE&C inspections), and all EPA Region 6 SDWA inspections as control
with w as (select distinct REGISTRY_ID from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_EPA_INFORMAL_ENFORCEMENT_ACTIONS
           where left(ENF_IDENTIFIER,2) = '06' and STATUTE = 'SDWA' and PGM_SYS_ACRNM = 'ICIS'),
inf as (select year(ACHIEVED_DATE) yr, count(*) rows_, count(distinct ENF_IDENTIFIER) actions, count(distinct REGISTRY_ID) wells
        from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_EPA_INFORMAL_ENFORCEMENT_ACTIONS
        where left(ENF_IDENTIFIER,2) = '06' and STATUTE = 'SDWA' and PGM_SYS_ACRNM = 'ICIS' group by 1),
ins as (select year(i.ACTUAL_BEGIN_DATE) yr, count(distinct iff(w.REGISTRY_ID is not null, i.ACTIVITY_ID, null)) insp_wells,
          count(distinct iff(w.REGISTRY_ID is not null, i.REGISTRY_ID, null)) wells_inspected,
          count(distinct iff(i.EPA_REGION_CODE = '06' and i.STATUTE_CODE ilike '%SDWA%', i.ACTIVITY_ID, null)) r6_sdwa_insp,
          count(distinct i.ACTIVITY_ID) all_insp
        from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_ICIS_FEC_EPA_INSPECTIONS i left join w on w.REGISTRY_ID = i.REGISTRY_ID group by 1)
select coalesce(inf.yr, ins.yr) yr, inf.rows_, inf.actions, inf.wells, ins.insp_wells, ins.wells_inspected, ins.r6_sdwa_insp, ins.all_insp,
  (select count(*) from w) wells_total
from inf full outer join ins on ins.yr = inf.yr where coalesce(inf.yr, ins.yr) >= 2000 order by 1
