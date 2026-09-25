-- SDWA service-area codes checked against system names: share of active systems per primary code whose name says mobile home / school / daycare / restaurant / camp / motel
with sa as (select PWSID, min(SERVICE_AREA_TYPE_CODE) code from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_EPA_SDWA_SDWA_SERVICE_AREAS where IS_PRIMARY_SERVICE_AREA_CODE = 'Y' group by 1 having count(*) = 1),
p as (select PWSID, upper(PWS_NAME) nm, OWNER_TYPE_CODE from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS where PWS_ACTIVITY_CODE = 'A')
select sa.code, count(*) systems,
  round(100 * count_if(nm like any ('%MOBILE%', '%MHP%', '%TRAILER%', '%MANUFACTURED%', '%M.H.P%', '%MH PARK%', '%HOME PARK%', '%RV PARK%')) / count(*), 1) pct_mobile,
  round(100 * count_if(nm like any ('%SCHOOL%', '%ELEM%', '%ACADEMY%', '% HIGH%', '% MIDDLE%', '% HS', '% ES')) / count(*), 1) pct_school,
  round(100 * count_if(nm like any ('%DAY CARE%', '%DAYCARE%', '%CHILD%', '%PRESCHOOL%', '%LEARNING%', '%KIDS%', '%MONTESSORI%', '%NURSERY%')) / count(*), 1) pct_daycare,
  round(100 * count_if(nm like any ('%RESTAURANT%', '%CAFE%', '%DINER%', '%GRILL%', '%TAVERN%', '% BAR%', '%PIZZA%', '% INN%')) / count(*), 1) pct_food,
  round(100 * count_if(nm like any ('%CAMP%')) / count(*), 1) pct_camp,
  round(100 * count_if(nm like any ('%MOTEL%', '%HOTEL%', '%LODGE%', '%RESORT%')) / count(*), 1) pct_lodging,
  round(100 * count_if(nm like any ('%SUBDIVISION%', '%ESTATES%', '%HOA%', '%HOMEOWNERS%', '%WATER ASSOC%', '%WATER CO%', '%WATER SUPPLY%', '%WSC%', '%UTILIT%', '%CITY OF%', '%TOWN OF%', '%VILLAGE OF%')) / count(*), 1) pct_residential_word,
  round(100 * count_if(OWNER_TYPE_CODE = 'P') / count(*), 1) pct_private, any_value(nm) example
from sa join p on p.PWSID = sa.PWSID group by 1 having count(*) >= 300 order by systems desc
