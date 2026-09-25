-- Profile all nine quarters: keys, dupes, EIN filler, forms, filer size, dates outside the quarter
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
), x as (select q, ADSH, count(*) over (partition by q, ADSH) dup_in_q, count(distinct q) over (partition by ADSH) nq from u)
select u.q, count(*) n, count(distinct u.ADSH) adsh, count(distinct CIK) cik,
  count_if(EIN='000000000') ein_zero, count_if(EIN is null or trim(EIN)='') ein_blank,
  count_if(PREVRPT='1') prevrpt1, count_if(DETAIL='1') detail1,
  count_if(FORM='10-K') k, count_if(FORM='10-Q') q10, count_if(FORM='10-K/A') ka, count_if(FORM='10-Q/A') qa,
  count_if(FORM in ('20-F','40-F','20-F/A','40-F/A')) foreign_annual, count_if(FORM not in ('10-K','10-Q','10-K/A','10-Q/A','20-F','40-F','20-F/A','40-F/A')) other_form,
  listagg(distinct AFS, '|') afs_vals,
  min(try_to_date(FILED,'YYYYMMDD')) filed_min, max(try_to_date(FILED,'YYYYMMDD')) filed_max,
  count_if(try_to_date(FILED,'YYYYMMDD') is null) filed_bad, count_if(try_to_date(PERIOD,'YYYYMMDD') is null) period_bad,
  max(x.dup_in_q) max_adsh_dup_in_q, count_if(x.nq>1) rows_adsh_in_2plus_q,
  count_if(try_to_number(NCIKS)>1) multi_cik
from u join (select distinct q, ADSH, dup_in_q, nq from x) x on x.q=u.q and x.ADSH=u.ADSH
group by 1 order by 1
