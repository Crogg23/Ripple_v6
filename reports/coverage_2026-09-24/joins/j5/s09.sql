-- CourtListener dockets: any case name with an official surname from the four clusters or a CFHC entity, plus every Texas federal case with HOSPICE in the name since 2015
select COURT_ID, DATE_FILED, DATE_TERMINATED, DOCKET_NUMBER, left(CASE_NAME,160) case_name, NATURE_OF_SUIT, CAUSE,
  case when CASE_NAME ilike '%OSHINUGA%' then 'oshinuga' when CASE_NAME ilike '%BENJAMIN ARISE%' or CASE_NAME ilike 'ARISE%' then 'arise'
       when CASE_NAME ilike '%CFHC%' or CASE_NAME ilike '%COMMUNITY FIRST HOSPICE%' then 'cfhc' when CASE_NAME ilike '%GLEASON%' and CASE_NAME ilike '%HOSPICE%' then 'gleason'
       when CASE_NAME ilike '%JP2D%' then 'jp2d' else 'tx hospice' end hit
from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS
where CASE_NAME ilike '%OSHINUGA%' or CASE_NAME ilike '%BENJAMIN ARISE%' or CASE_NAME ilike 'ARISE,%' or CASE_NAME ilike '%CFHC%' or CASE_NAME ilike '%COMMUNITY FIRST HOSPICE%' or CASE_NAME ilike '%JP2D%'
   or (CASE_NAME ilike '%HOSPICE%' and COURT_ID in ('txsd','txwd','txnd','txed','txsb','txwb','txnb','txeb','ca5') and DATE_FILED >= '2015-01-01')
order by hit, DATE_FILED
