-- FJC appeals: appeals docketed per month, Oct 2022 - Mar 2026, by stream. One appeal = circuit+docket+reopen, counted once.
with a as (select distinct CIRCUIT, DOCKET, REOPEN,
             date_trunc('month', try_to_date(DOCKET_DATE::string)) m, NATURE_OF_SUIT::string nos, AGENCY::string ag,
             APPEAL_TYPE::string t, US_APPELLANT::string usa, US_APPELLEE::string use
           from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE
           where try_to_date(DOCKET_DATE::string) >= '2022-10-01')
select m, count(*) all_appeals,
  sum(iff(nos='463',1,0)) alien_habeas, sum(iff(nos='463' and usa='1',1,0)) alien_habeas_us_appeals,
  sum(iff(ag='6',1,0)) agency6, sum(iff(t='3' and usa='1',1,0)) us_civil_appeals_by_us,
  sum(iff(t='3',1,0)) us_civil_all, sum(iff(t in ('14','15','16','17','18','19','20','21'),1,0)) criminal
from a group by 1 order by 1
