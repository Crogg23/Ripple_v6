-- FRA casualties: same months across years. Trespasser deaths January-May, 2019-2026, for UP, BNSF, CSX, NS and everyone
select INCIDENT_YEAR yr, count_if(RAILROAD_CODE='UP') up, count_if(RAILROAD_CODE='BNSF') bnsf, count_if(RAILROAD_CODE='CSX') csx, count_if(RAILROAD_CODE='NS') ns,
  count_if(RAILROAD_CODE='ATK') atk, count(*) all_rr
from LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_FRA_CASUALTIES
where FATALITY='Yes' and TYPE_OF_PERSON ilike 'Trespass%' and INCIDENT_YEAR between 2019 and 2026 and month(DATE) between 1 and 5
group by 1 order by 1;
