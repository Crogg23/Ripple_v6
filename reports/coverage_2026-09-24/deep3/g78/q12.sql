-- FRA casualties: trespasser deaths by what the person was doing (lying, walking, sitting/standing), by railroad and year, 2010-2025
-- To see whether UP's rise is people lying on the track, and when it started
select RAILROAD_CODE rr, INCIDENT_YEAR yr, count(*) n,
  count_if(PHYSICAL_ACT_CIRCUMSTANCES ilike 'Lay%' or PHYSICAL_ACT_CIRCUMSTANCES ilike 'Ly%') laying,
  count_if(PHYSICAL_ACT_CIRCUMSTANCES ilike 'Walk%') walking,
  count_if(PHYSICAL_ACT_CIRCUMSTANCES ilike 'Sit%' or PHYSICAL_ACT_CIRCUMSTANCES ilike 'Stand%') sit_stand,
  count_if(PHYSICAL_ACT_CIRCUMSTANCES is null or PHYSICAL_ACT_CIRCUMSTANCES ilike '%other%' or PHYSICAL_ACT_CIRCUMSTANCES ilike '%unknown%') other_unk,
  listagg(distinct iff(PHYSICAL_ACT_CIRCUMSTANCES ilike 'Lay%' or PHYSICAL_ACT_CIRCUMSTANCES ilike 'Ly%', PHYSICAL_ACT_CIRCUMSTANCES, null), ',') lay_label
from LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_FRA_CASUALTIES
where FATALITY='Yes' and TYPE_OF_PERSON ilike 'Trespass%' and RAILROAD_CODE in ('UP','BNSF','CSX','NS') and INCIDENT_YEAR between 2010 and 2025
group by 1,2 order by 1,2;
