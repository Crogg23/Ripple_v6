-- FJC appeals, immigration-detention habeas (NATURE_OF_SUIT 463): by circuit, three periods, with the circuit's all-appeals denominator
with a as (select distinct CIRCUIT, DOCKET, REOPEN, try_to_date(DOCKET_DATE::string) dd, NATURE_OF_SUIT::string nos,
             US_APPELLANT::string usa, PRO_SE_FILED::string ps, DISTRICT_COURT::string dc
           from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_APPELLATE
           where try_to_date(DOCKET_DATE::string) >= '2023-10-01')
select CIRCUIT,
  sum(iff(nos='463' and dd < '2024-10-01',1,0)) hab_fy24,
  sum(iff(nos='463' and dd >= '2024-10-01' and dd < '2025-10-01',1,0)) hab_fy25,
  sum(iff(nos='463' and dd >= '2025-10-01',1,0)) hab_oct25_mar26,
  sum(iff(nos='463' and dd >= '2025-10-01' and usa='1',1,0)) hab_oct25_mar26_us_appeals,
  sum(iff(nos='463' and dd >= '2025-10-01' and ps not in ('0','-8'),1,0)) hab_oct25_mar26_pro_se,
  count(distinct iff(nos='463' and dd >= '2025-10-01', dc, null)) hab_n_districts,
  sum(iff(dd >= '2025-10-01',1,0)) all_oct25_mar26,
  sum(iff(dd >= '2024-10-01' and dd < '2025-04-01',1,0)) all_oct24_mar25
from a group by 1 order by hab_oct25_mar26 desc
