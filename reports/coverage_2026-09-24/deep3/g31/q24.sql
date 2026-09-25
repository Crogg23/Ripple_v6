-- PREVRPT trap: originals that the index itself shows were later amended (same CIK + period, a /A filed later), and how many carry PREVRPT=1; plus EIN width check
with u as (
  select '2024Q1' q, * from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_DERA_SUB_2024Q1 union all
  select '2024Q2', * from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_DERA_SUB_2024Q2 union all
  select '2024Q3', * from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_DERA_SUB_2024Q3 union all
  select '2024Q4', * from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_DERA_SUB_2024Q4 union all
  select '2025Q1', * from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_DERA_SUB_2025Q1 union all
  select '2025Q2', * from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_DERA_SUB_2025Q2 union all
  select '2025Q3', * from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_DERA_SUB_2025Q3 union all
  select '2025Q4', * from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_DERA_SUB_2025Q4 union all
  select '2026Q1', * from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_DERA_SUB_2026Q1
),
o as (select q, ADSH, CIK, PERIOD, FORM, PREVRPT, FILED, EIN from u where FORM in ('10-K','10-Q')),
a as (select CIK, PERIOD, replace(FORM,'/A','') base, min(FILED) first_amend from u where FORM in ('10-K/A','10-Q/A') group by 1,2,3)
select o.q, count(*) originals, count_if(o.PREVRPT='1') prevrpt1,
  count_if(a.CIK is not null and a.first_amend >= o.FILED) amended_later_in_index,
  count_if(a.CIK is not null and a.first_amend >= o.FILED and o.PREVRPT='1') amended_and_flagged,
  count_if(length(o.EIN) <> 9) ein_not_9, count_if(o.EIN = '000000000') ein_zero
from o left join a on a.CIK=o.CIK and a.PERIOD=o.PERIOD and a.base=o.FORM
group by 1 order by 1
