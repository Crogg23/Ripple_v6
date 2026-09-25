-- EOIR (A_TblCase layout, 39 tab fields; fields named from the sample profile q06): cases by month of DATE_DETAINED (field 32), 2018-01 to 2026-05.
-- Per month: cases, still detained now, entry-to-detention gap buckets (DATE_OF_ENTRY field 24), LPR flag, priority codes, age at detention (birth M/YYYY field 26), sex, attorney notice (E_28 field 11)
with p as (
  select split_part(CASE_TYPE, '\t', 1) idn, split_part(CASE_TYPE, '\t', 7) nat, split_part(CASE_TYPE, '\t', 9) cust,
    trim(split_part(CASE_TYPE, '\t', 11)) e28, split_part(CASE_TYPE, '\t', 14) site,
    try_to_date(left(split_part(CASE_TYPE, '\t', 24), 10), 'YYYY-MM-DD') entry,
    trim(split_part(CASE_TYPE, '\t', 26)) birth, split_part(CASE_TYPE, '\t', 31) sex,
    try_to_date(left(split_part(CASE_TYPE, '\t', 32), 10), 'YYYY-MM-DD') det,
    split_part(CASE_TYPE, '\t', 34) lpr, trim(split_part(CASE_TYPE, '\t', 39)) prio
  from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_EOIR_CASE_DATA
  where regexp_count(CASE_TYPE, '\t') = 38),
q as (select *, case when birth like '%/%' then datediff(month, date_from_parts(try_to_number(split_part(birth,'/',2)), try_to_number(split_part(birth,'/',1)), 1), det)/12.0 end age,
             datediff(day, entry, det) gap from p where det >= '2018-01-01' and det < '2026-06-01')
select date_trunc(month, det)::date mo, count(*) n, count_if(cust='D') still_d, count_if(cust='R') rel, count_if(cust='N') never,
  count_if(entry is not null) entry_known, count_if(gap between 0 and 30) g_0_30d, count_if(gap between 31 and 730) g_1m_2y,
  count_if(gap between 731 and 3652) g_2_10y, count_if(gap > 3652) g_10y_plus, count_if(gap < 0) g_neg,
  count_if(lpr='1') lpr1, count_if(prio='AWC/D') awc_d, count_if(prio='RBC/D') rbc_d, count_if(prio='UC') uc, count_if(prio='AWC/ATD') awc_atd,
  count_if(age is not null) age_known, count_if(age < 18) minor, count_if(age < 6) under6, count_if(sex='F') female,
  count_if(e28 <> '') has_e28, count_if(nat='MX') mx, count_if(nat in ('GT','HO','ES')) nt, count_if(nat='VE') ve
from q group by 1 order by 1
