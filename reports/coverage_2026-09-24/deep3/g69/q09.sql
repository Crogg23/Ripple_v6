-- EOIR: "old case" detentions (case number 2+ years old at detention, per the q08 calendar) in Jan-May 2019, 2024, 2026.
-- Totals per window plus by nationality (field 7). Checks: hearing on/after detention (field 15), future hearing, lawyer before detention, 10y+ in US, custody now, case type
with p as (
  select try_to_number(split_part(CASE_TYPE, '\t', 1)) idn, split_part(CASE_TYPE, '\t', 7) nat, split_part(CASE_TYPE, '\t', 9) cust,
    split_part(CASE_TYPE, '\t', 13) ctype, split_part(CASE_TYPE, '\t', 14) site,
    try_to_date(left(split_part(CASE_TYPE, '\t', 11), 10), 'YYYY-MM-DD') e28d,
    try_to_date(left(split_part(CASE_TYPE, '\t', 15), 10), 'YYYY-MM-DD') hear,
    try_to_date(left(split_part(CASE_TYPE, '\t', 24), 10), 'YYYY-MM-DD') entry,
    try_to_date(left(split_part(CASE_TYPE, '\t', 32), 10), 'YYYY-MM-DD') det
  from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_EOIR_CASE_DATA
  where regexp_count(CASE_TYPE, '\t') = 38),
d as (select *, date_trunc(quarter, det)::date qtr, datediff(day, entry, det) gap from p where det >= '2012-01-01' and det < '2026-06-01'),
cal as (select qtr, median(idn) med_idn from d where gap between 0 and 30 group by 1),
o as (select d.*, year(d.det) yr from d join cal c8 on c8.qtr = dateadd(quarter, -8, d.qtr)
      where d.idn < c8.med_idn and month(d.det) <= 5 and year(d.det) in (2019, 2024, 2026)),
g as (select yr, grouping(nat) is_total, iff(grouping(nat)=1, 'ALL', nat) nat, count(*) n,
        count_if(hear >= det) hear_on_after_det, count_if(hear > '2026-05-31') hear_future, count_if(e28d < det) lawyer_before,
        count_if(gap > 3652) in_us_10y, count_if(cust='D') cust_d, count_if(cust='R') cust_r, count_if(ctype='RMV') rmv,
        median(idn) med_idn, min(det) first_det
      from o group by grouping sets ((yr), (yr, nat)))
select * from g qualify is_total = 1 or row_number() over (partition by yr, is_total order by n desc) <= 12
order by yr, is_total desc, n desc
