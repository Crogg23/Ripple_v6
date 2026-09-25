-- Oral arguments, dull-explanation test for the D.C. Circuit: is the rise just more en banc (full-court) sittings? Split by panel size.
with oa as (select DOCKET_ID::string did, DURATION, JUDGES from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_ORAL_ARGUMENTS),
d as (select ID::string id, COURT_ID, try_to_date(DATE_ARGUED::string) da from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS
      where ID::string in (select did from oa))
select iff(d.COURT_ID='cadc','cadc','other_fed_circuits') grp, year(d.da) yr,
  sum(iff(regexp_count(oa.JUDGES, ';') + 1 <= 3,1,0)) n_panel, median(iff(regexp_count(oa.JUDGES, ';') + 1 <= 3, DURATION, null)) med_panel,
  sum(iff(regexp_count(oa.JUDGES, ';') + 1 > 3,1,0)) n_big_bench, median(iff(regexp_count(oa.JUDGES, ';') + 1 > 3, DURATION, null)) med_big,
  sum(iff(oa.JUDGES is null or trim(oa.JUDGES)='',1,0)) no_judges
from oa join d on d.id = oa.did
where (d.COURT_ID = 'cadc' or d.COURT_ID in ('ca1','ca2','ca3','ca4','ca5','ca6','ca7','ca8','ca9','ca10','ca11','cafc')) and year(d.da) >= 2019
group by 1,2 order by 1,2
