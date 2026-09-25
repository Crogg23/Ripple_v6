select year(DATE_FILED) y, count(*) n, count_if(upper(CASE_NAME) like '%KAPADIA%') kapadia, count_if(upper(CASE_NAME) like '%UNITED STATES%' and upper(CASE_NAME) like '%HEALTH%') us_health,
  count_if(upper(CASE_NAME) like '%JENG%') jeng, count_if(upper(CASE_NAME) like '%DENNY%' and STATE_HINT) denny_az
from (select DATE_FILED, CASE_NAME, COURT_ID in ('azd','azb') STATE_HINT from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS)
where DATE_FILED >= '2015-01-01' group by 1 order by 1
