-- 4th Circuit published 2016-2025: re-posts (same docket earlier, or same case name within 400 days on an earlier date)
with c as (select cl.ID, cl.DATE_FILED, year(cl.DATE_FILED) yr,
             nullif(nullif(upper(trim(cl.CASE_NAME)),''),'NONE') nm, cl.DOCKET_ID
           from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_OPINION_CLUSTERS cl
           join LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS d on d.ID = cl.DOCKET_ID
           where d.COURT_ID = 'ca4' and cl.PRECEDENTIAL_STATUS = 'Published' and cl.DATE_FILED >= '2016-01-01' and cl.DATE_FILED < '2026-01-01'),
x as (select a.ID, a.yr,
        max(iff(b.DOCKET_ID = a.DOCKET_ID and b.DATE_FILED < a.DATE_FILED,1,0)) prior_same_docket,
        max(iff(b.nm = a.nm and b.DATE_FILED < a.DATE_FILED and b.DATE_FILED >= dateadd(day,-400,a.DATE_FILED),1,0)) prior_same_name_400d,
        max(iff(b.nm = a.nm and b.DATE_FILED = a.DATE_FILED,1,0)) same_name_same_day
      from c a left join c b on b.ID <> a.ID and (b.DOCKET_ID = a.DOCKET_ID or b.nm = a.nm)
      group by 1,2)
select yr, count(*) n_pub, sum(prior_same_docket) prior_same_docket, sum(prior_same_name_400d) prior_same_name_400d,
  sum(same_name_same_day) same_name_same_day,
  sum(iff(prior_same_docket=1 or prior_same_name_400d=1,1,0)) any_prior_repeat
from x group by 1 order by 1;
