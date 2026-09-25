-- Independent label check: clusters with an F.3d/F.4th (West published reporter) citation, per circuit x year, vs CourtListener status
with c as (select cl.ID, d.COURT_ID, year(cl.DATE_FILED) yr, cl.PRECEDENTIAL_STATUS st
           from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_OPINION_CLUSTERS cl
           join LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS d on d.ID = cl.DOCKET_ID
           where d.COURT_ID in ('ca1','ca2','ca3','ca4','ca5','ca6','ca7','ca8','ca9','ca10','ca11','cadc','cafc')
             and cl.DATE_FILED >= '2018-01-01' and cl.DATE_FILED < '2026-01-01'),
ct as (select CLUSTER_ID, max(iff(REPORTER in ('F.3d','F.4th'),1,0)) f_rep, max(iff(REPORTER like 'F. App%',1,0)) fappx, count(*) n_cites
       from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_CITATIONS
       where CLUSTER_ID in (select ID from c) group by 1)
select c.COURT_ID, c.yr, count(*) n,
  sum(iff(c.st = 'Published', 1, 0)) n_pub,
  sum(coalesce(ct.f_rep, 0)) n_fcite,
  sum(iff(c.st = 'Published', coalesce(ct.f_rep, 0), 0)) pub_with_fcite,
  sum(iff(c.st = 'Unpublished', coalesce(ct.f_rep, 0), 0)) unpub_with_fcite,
  sum(coalesce(ct.fappx, 0)) n_fappx,
  count(ct.CLUSTER_ID) n_any_cite
from c left join ct on ct.CLUSTER_ID = c.ID
group by 1,2 order by 1,2;
