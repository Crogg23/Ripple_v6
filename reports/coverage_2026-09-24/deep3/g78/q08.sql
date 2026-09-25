-- FRA deaths table: yearly series 2010-2026 for the big railroads, trespassers and everyone else, to see where UP's jump starts
select INCIDENT_YEAR yr,
  sum(iff(RAILROAD_CODE='UP' and TYPE_OF_PERSON='Trespassers', DEATHS, 0)) up_tr,
  sum(iff(RAILROAD_CODE='UP' and TYPE_OF_PERSON<>'Trespassers', DEATHS, 0)) up_other,
  sum(iff(RAILROAD_CODE='BNSF' and TYPE_OF_PERSON='Trespassers', DEATHS, 0)) bnsf_tr,
  sum(iff(RAILROAD_CODE='CSX' and TYPE_OF_PERSON='Trespassers', DEATHS, 0)) csx_tr,
  sum(iff(RAILROAD_CODE='NS' and TYPE_OF_PERSON='Trespassers', DEATHS, 0)) ns_tr,
  sum(iff(RAILROAD_CODE='ATK' and TYPE_OF_PERSON='Trespassers', DEATHS, 0)) atk_tr,
  sum(iff(RAILROAD_CODE='BLF' and TYPE_OF_PERSON='Trespassers', DEATHS, 0)) blf_tr,
  sum(iff(TYPE_OF_PERSON='Trespassers', DEATHS, 0)) all_tr,
  sum(iff(RAILROAD_CODE='UP' and TYPE_OF_PERSON like 'Worker%', DEATHS, 0)) up_worker,
  sum(iff(TYPE_OF_PERSON like 'Worker%', DEATHS, 0)) all_worker
from LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_FRA_RAIL_DEATHS_BY_RAILROAD
where INCIDENT_YEAR >= 2010 group by 1 order by 1;
