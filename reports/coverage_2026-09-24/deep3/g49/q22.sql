-- Oral arguments eyeball: the 15 longest D.C. Circuit arguments argued 2025-26, with case name and panel
with oa as (select DOCKET_ID::string did, DURATION, CASE_NAME, JUDGES from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_ORAL_ARGUMENTS),
d as (select ID::string id, COURT_ID, try_to_date(DATE_ARGUED::string) da, DOCKET_NUMBER from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS
      where ID::string in (select did from oa))
select d.da, d.DOCKET_NUMBER, round(oa.DURATION/60) minutes, left(oa.CASE_NAME,90) case_name, left(oa.JUDGES,80) judges
from oa join d on d.id = oa.did
where d.COURT_ID = 'cadc' and year(d.da) >= 2025
order by oa.DURATION desc limit 15
