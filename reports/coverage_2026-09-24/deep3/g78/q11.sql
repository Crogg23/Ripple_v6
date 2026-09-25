-- FRA casualties: UP trespasser deaths in California by county, 2015-2017 vs 2023-2025 (yearly avg), and BNSF in the same counties
with f as (select RAILROAD_CODE rr, COUNTY_NAME cty, INCIDENT_YEAR y from LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_FRA_CASUALTIES
           where FATALITY='Yes' and TYPE_OF_PERSON ilike 'Trespass%' and STATE_NAME='CALIFORNIA' and RAILROAD_CODE in ('UP','BNSF','ATK','SCAX','PCJX','PCMZ')
             and (INCIDENT_YEAR between 2015 and 2017 or INCIDENT_YEAR between 2023 and 2025))
select cty, round(count_if(rr='UP' and y<=2017)/3,1) up_a, round(count_if(rr='UP' and y>=2023)/3,1) up_b,
  round(count_if(rr='BNSF' and y<=2017)/3,1) bnsf_a, round(count_if(rr='BNSF' and y>=2023)/3,1) bnsf_b,
  round(count_if(rr not in ('UP','BNSF') and y<=2017)/3,1) pass_a, round(count_if(rr not in ('UP','BNSF') and y>=2023)/3,1) pass_b
from f group by 1 order by up_b - up_a desc limit 12;
