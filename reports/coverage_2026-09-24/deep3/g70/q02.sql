-- SDWA service areas: primary service type x water-system type, active systems only, with people served and groundwater share
with sa as (select PWSID, min(SERVICE_AREA_TYPE_CODE) code, count(*) nprim from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_EPA_SDWA_SDWA_SERVICE_AREAS where IS_PRIMARY_SERVICE_AREA_CODE = 'Y' group by 1),
p as (select PWSID, PWS_TYPE_CODE, POPULATION_SERVED_COUNT pop, GW_SW_CODE, IS_SCHOOL_OR_DAYCARE_IND from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS where PWS_ACTIVITY_CODE = 'A')
select sa.code, p.PWS_TYPE_CODE, count(*) systems, sum(p.pop) people, median(p.pop) med_pop, count_if(p.GW_SW_CODE = 'GW') gw, count_if(p.IS_SCHOOL_OR_DAYCARE_IND = 'Y') school_flag, count_if(sa.nprim > 1) multi_primary
from sa join p on p.PWSID = sa.PWSID group by 1, 2 having count(*) >= 200 order by systems desc
