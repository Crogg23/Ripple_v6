-- EOIR: how old was the court case when the person was detained? IDNCASE (field 1) is a sequence number.
-- Calendar: median IDNCASE of "fresh" cases (entry-to-detention gap 0-30 days) per detention quarter = the number being handed out then.
-- A detained case is "old" if its IDNCASE is below the calendar marker 8 quarters (2 years) before its detention quarter.
with p as (
  select try_to_number(split_part(CASE_TYPE, '\t', 1)) idn, trim(split_part(CASE_TYPE, '\t', 11)) e28,
    try_to_date(left(split_part(CASE_TYPE, '\t', 11), 10), 'YYYY-MM-DD') e28d,
    try_to_date(left(split_part(CASE_TYPE, '\t', 24), 10), 'YYYY-MM-DD') entry,
    try_to_date(left(split_part(CASE_TYPE, '\t', 32), 10), 'YYYY-MM-DD') det
  from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_EOIR_CASE_DATA
  where regexp_count(CASE_TYPE, '\t') = 38),
d as (select *, date_trunc(quarter, det)::date qtr, datediff(day, entry, det) gap from p where det >= '2012-01-01' and det < '2026-06-01'),
cal as (select qtr, count(*) fresh_n, median(idn) med_idn, min(idn) min_idn, max(idn) max_idn from d where gap between 0 and 30 group by 1)
select d.qtr, c.fresh_n, c.med_idn, c.min_idn, c.max_idn, c8.med_idn marker_2y_before, count(*) detained,
  count_if(d.idn < c8.med_idn) old_case_2y, count_if(d.idn < c8.med_idn and d.gap > 730) old_case_2y_entry_2y,
  count_if(d.idn < c8.med_idn and d.e28d < d.det) old_case_lawyer_before_det,
  count_if(d.e28 <> '') has_e28, count_if(d.e28d < d.det) e28_before_det
from d join cal c on c.qtr = d.qtr
left join cal c8 on c8.qtr = dateadd(quarter, -8, d.qtr)
group by 1,2,3,4,5,6 order by 1
