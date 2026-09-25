-- EOIR: where are the Jan-May 2026 old-band detainees (IDNCASE 10,441,284-13,639,609, cases opened ~Q1 2022-Q1 2024)?
-- Top address places (city/state/ZIP on file, usually the jail for custody D) and top courts (UPDATE_SITE, field 14)
with p as (
  select try_to_number(split_part(CASE_TYPE, '\t', 1)) idn, upper(trim(split_part(CASE_TYPE, '\t', 2))) city, split_part(CASE_TYPE, '\t', 3) st,
    left(split_part(CASE_TYPE, '\t', 4), 5) zip, split_part(CASE_TYPE, '\t', 9) cust, split_part(CASE_TYPE, '\t', 14) site,
    try_to_date(left(split_part(CASE_TYPE, '\t', 32), 10), 'YYYY-MM-DD') det
  from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_EOIR_CASE_DATA
  where regexp_count(CASE_TYPE, '\t') = 38),
o as (select * from p where idn >= 10441284 and idn < 13639610 and det between '2026-01-01' and '2026-05-31'),
a as (select 'place' k, city || ', ' || st || ' ' || zip v, count(*) n, count_if(cust='D') d from o group by 2),
b as (select 'court' k, site v, count(*) n, count_if(cust='D') d from o group by 2),
t as (select 'total' k, 'all' v, count(*) n, count_if(cust='D') d from o)
select * from t
union all select * from (select * from a order by n desc limit 15)
union all select * from (select * from b order by n desc limit 12)
