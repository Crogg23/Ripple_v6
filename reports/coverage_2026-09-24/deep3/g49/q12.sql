-- Oral arguments: length distribution by year for the D.C. Circuit, the Supreme Court, and the other 12 federal appeals courts pooled
with oa as (select DOCKET_ID::string did, DURATION from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_ORAL_ARGUMENTS),
d as (select ID::string id, COURT_ID, try_to_date(DATE_ARGUED::string) da from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS
      where ID::string in (select did from oa))
select case when d.COURT_ID in ('cadc','scotus') then d.COURT_ID when d.COURT_ID like 'ca%' then 'other_fed_circuits' else 'illinois' end grp,
  year(d.da) yr, count(*) n, percentile_cont(0.25) within group (order by DURATION) p25, median(DURATION) med,
  percentile_cont(0.75) within group (order by DURATION) p75, sum(iff(DURATION > 3600,1,0)) over_60m,
  sum(iff(DURATION > 5400,1,0)) over_90m, max(DURATION) mx, sum(iff(DURATION is null or DURATION <= 0,1,0)) bad_dur
from oa join d on d.id = oa.did
where year(d.da) >= 2012
group by 1,2 order by 1,2
