-- Hostile check on the San Joaquin stop and the South Coast blank: violations (federally reportable, by determination date) and HPVs (by day zero)
-- logged per year for the three biggest California districts, 2019-2026
with f as (select PGM_SYS_ID, LOCAL_CONTROL_REGION_NAME lcr from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES
           where STATE='CA' and (LOCAL_CONTROL_REGION_NAME like 'San Joaquin%' or LOCAL_CONTROL_REGION_NAME like 'South Coast%' or LOCAL_CONTROL_REGION_NAME like 'Bay Area%')),
v as (select left(f.lcr,12) d, year(coalesce(v.EARLIEST_FRV_DETERM_DATE, v.HPV_DAYZERO_DATE)) y, count(*) rows_all, count(v.HPV_DAYZERO_DATE) hpv,
        count(distinct v.PGM_SYS_ID) facs
      from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_VIOLATION_HISTORY v join f using (PGM_SYS_ID)
      where coalesce(v.EARLIEST_FRV_DETERM_DATE, v.HPV_DAYZERO_DATE) between '2019-01-01' and '2026-09-24' group by 1,2)
select * from v order by 1,2
