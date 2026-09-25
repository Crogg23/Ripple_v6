-- Oral arguments, test inside the group: in each court, are cases with "Trump" in the name the long ones, or did everything get longer?
with oa as (select DOCKET_ID::string did, DURATION, CASE_NAME from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_ORAL_ARGUMENTS),
d as (select ID::string id, COURT_ID, try_to_date(DATE_ARGUED::string) da from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS
      where ID::string in (select did from oa))
select case when d.COURT_ID in ('cadc','scotus') then d.COURT_ID else 'other_fed_circuits' end grp,
  case when year(d.da) between 2021 and 2024 then '2021-24' when year(d.da) >= 2025 then '2025-26' end period,
  iff(oa.CASE_NAME ilike '%trump%', 'trump_named', 'other') kind,
  count(*) n, median(DURATION) med, percentile_cont(0.75) within group (order by DURATION) p75,
  sum(iff(DURATION > 3600,1,0)) over_60m
from oa join d on d.id = oa.did
where d.COURT_ID like 'ca%' or d.COURT_ID = 'scotus'
group by 1,2,3 having period is not null order by 1,2,3
