-- 4th Circuit published 2019-2025: which rows collapse on name+date (the builder's dedupe), with their docket numbers
with c as (select cl.ID, cl.DOCKET_ID, year(cl.DATE_FILED) yr, cl.DATE_FILED, cl.CASE_NAME, cl.SOURCE, d.DOCKET_NUMBER
           from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_OPINION_CLUSTERS cl
           join LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS d on d.ID = cl.DOCKET_ID
           where d.COURT_ID = 'ca4' and cl.PRECEDENTIAL_STATUS = 'Published' and cl.DATE_FILED >= '2019-01-01' and cl.DATE_FILED < '2026-01-01'),
g as (select yr, CASE_NAME, DATE_FILED, count(*) n, count(distinct DOCKET_ID) nd,
        listagg(distinct DOCKET_NUMBER, ' ; ') within group (order by DOCKET_NUMBER) dns, listagg(distinct SOURCE, ',') srcs
      from c group by 1,2,3 having count(*) > 1)
select yr, left(CASE_NAME,90) case_name, DATE_FILED, n, nd, left(dns,160) dns, srcs,
  sum(n) over (partition by yr) rows_in_dup_groups, count(*) over (partition by yr) n_dup_groups,
  sum(n - 1) over (partition by yr) rows_removed
from g qualify row_number() over (partition by yr order by n desc, CASE_NAME) <= 5
order by yr, n desc;
