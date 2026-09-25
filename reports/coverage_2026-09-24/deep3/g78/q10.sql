-- FRA casualties: is UP's jump a reporting change? For trespasser deaths, 2015-2017 vs 2023-2025, UP vs BNSF/CSX/NS:
-- narratives that say found / body / discovered (unwitnessed), that say suicide, blank narratives, unknown event, median age, top event
with f as (select RAILROAD_CODE rr, iff(INCIDENT_YEAR<=2017,'A_2015_17','B_2023_25') p, upper(coalesce(NARRATIVE,'')) nar, EVENT, PHYSICAL_ACT_CIRCUMSTANCES pac, AGE_OF_PERSON age, GENERAL_LOCATION_OF_PERSON loc
           from LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_FRA_CASUALTIES
           where FATALITY='Yes' and TYPE_OF_PERSON ilike 'Trespass%' and RAILROAD_CODE in ('UP','BNSF','CSX','NS')
             and (INCIDENT_YEAR between 2015 and 2017 or INCIDENT_YEAR between 2023 and 2025))
select rr, p, count(*) n,
  count_if(nar like any ('%FOUND%','%DISCOVERED%','%BODY%','%REMAINS%','%DECEASED%')) found_like,
  count_if(nar like any ('%SUICID%','%INTENTIONAL%')) suicide_word,
  count_if(trim(nar)='') blank_nar,
  count_if(EVENT ilike '%unknown%' or EVENT is null) event_unknown,
  median(age) med_age, count_if(age is null or age=0) age_missing,
  mode(EVENT) top_event, mode(pac) top_act, mode(loc) top_loc
from f group by 1,2 order by 1,2;
