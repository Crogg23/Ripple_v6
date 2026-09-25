-- EOIR: monthly check of the old-case rise, 2023-01 to 2026-05. Adds the courthouse signature: latest hearing date (field 15) = detention date (field 32).
-- Artifact checks: busiest single day per month, weekend share (a batch data fix would pile on few days)
with p as (
  select try_to_number(split_part(CASE_TYPE, '\t', 1)) idn,
    try_to_date(left(split_part(CASE_TYPE, '\t', 15), 10), 'YYYY-MM-DD') hear,
    split_part(CASE_TYPE, '\t', 17) caltype,
    try_to_date(left(split_part(CASE_TYPE, '\t', 24), 10), 'YYYY-MM-DD') entry,
    try_to_date(left(split_part(CASE_TYPE, '\t', 32), 10), 'YYYY-MM-DD') det
  from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_EOIR_CASE_DATA
  where regexp_count(CASE_TYPE, '\t') = 38),
d as (select *, date_trunc(quarter, det)::date qtr, datediff(day, entry, det) gap from p where det >= '2012-01-01' and det < '2026-06-01'),
cal as (select qtr, median(idn) med_idn from d where gap between 0 and 30 group by 1),
m as (select d.*, (d.idn < c8.med_idn) old from d join cal c8 on c8.qtr = dateadd(quarter, -8, d.qtr) where d.det >= '2023-01-01'),
dd as (select det, count(*) n_day, count_if(old) old_day from m group by 1)
select date_trunc(month, m.det)::date mo, count(*) detained, count_if(old) old_case, count_if(hear = det) hear_eq_det,
  count_if(old and hear = det) old_hear_eq_det, count_if(old and hear = det and caltype = 'M') old_eq_master, count_if(old and hear = det and caltype = 'I') old_eq_indiv,
  count_if(dayofweekiso(det) >= 6) weekend, count_if(old and dayofweekiso(det) >= 6) old_weekend,
  (select max(old_day) from dd where date_trunc(month, dd.det) = date_trunc(month, m.det)) max_old_one_day,
  (select count(*) from dd where date_trunc(month, dd.det) = date_trunc(month, m.det) and old_day > 0) days_with_old
from m group by 1 order by 1
