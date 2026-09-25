-- FJC appeals, 463 appeals docketed Oct 2025 - Mar 2026: which trial courts they came from, by month. Do 3-4 courts carry it?
with a as (select distinct CIRCUIT, DOCKET, REOPEN, try_to_date(DOCKET_DATE::string) dd, US_APPELLANT::string usa,
             DISTRICT_COURT::string dc, APPELLANT, APPELLEE, PRO_SE_FILED::string ps
           from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE
           where NATURE_OF_SUIT::string='463' and try_to_date(DOCKET_DATE::string) >= '2025-10-01')
select CIRCUIT, dc, count(*) n,
  sum(iff(month(dd)=10,1,0)) oct, sum(iff(month(dd)=11,1,0)) nov, sum(iff(month(dd)=12,1,0)) dec_,
  sum(iff(month(dd)=1,1,0)) jan, sum(iff(month(dd)=2,1,0)) feb, sum(iff(month(dd)=3,1,0)) mar,
  sum(iff(usa='1',1,0)) us_appellant, sum(iff(ps not in ('0','-8'),1,0)) pro_se,
  count(distinct APPELLANT) n_appellant_names, mode(APPELLANT) top_appellant, mode(APPELLEE) top_appellee
from a group by 1,2 order by n desc limit 25
