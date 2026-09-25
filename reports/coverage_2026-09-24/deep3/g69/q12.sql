-- EOIR: denominator test by nationality. Band = cases opened 2-4 years before the window, by IDNCASE, using q08 calendar medians:
--   2026 window (Jan-May 2026): IDNCASE in [10,441,284 (Q1 2022), 13,639,610 (Q1 2024))
--   2024 window (Jan-May 2024): IDNCASE in [9,441,378 (Q1 2020), 10,441,284 (Q1 2022))
--   2019 window (Jan-May 2019): IDNCASE in [7,636,140 (Q1 2015), 8,145,229 (Q1 2017))
-- Rate = band cases logged detained in the window per 1,000 band cases. Top 14 nationalities by 2026 detained + ALL.
with p as (
  select try_to_number(split_part(CASE_TYPE, '\t', 1)) idn, split_part(CASE_TYPE, '\t', 7) nat,
    try_to_date(left(split_part(CASE_TYPE, '\t', 11), 10), 'YYYY-MM-DD') e28d,
    try_to_date(left(split_part(CASE_TYPE, '\t', 32), 10), 'YYYY-MM-DD') det
  from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_EOIR_CASE_DATA
  where regexp_count(CASE_TYPE, '\t') = 38),
b as (select *, case when idn >= 10441284 and idn < 13639610 then 2026 when idn >= 9441378 and idn < 10441284 then 2024
                     when idn >= 7636140 and idn < 8145229 then 2019 end w from p),
g as (select iff(grouping(nat)=1, 'ALL', nat) nat,
  count_if(w=2019) band19, count_if(w=2019 and det between '2019-01-01' and '2019-05-31') det19,
  count_if(w=2024) band24, count_if(w=2024 and det between '2024-01-01' and '2024-05-31') det24,
  count_if(w=2026) band26, count_if(w=2026 and det between '2026-01-01' and '2026-05-31') det26,
  count_if(w=2026 and det between '2026-01-01' and '2026-05-31' and e28d < det) det26_lawyer_before
  from b where w is not null group by grouping sets ((), (nat)))
select nat, band19, det19, round(1000*det19/nullif(band19,0),2) r19, band24, det24, round(1000*det24/nullif(band24,0),2) r24,
  band26, det26, round(1000*det26/nullif(band26,0),2) r26, det26_lawyer_before
from g qualify nat = 'ALL' or row_number() over (order by det26 desc) <= 16
order by det26 desc
