-- EOIR eyeball: 6 random old-band cases (IDNCASE 10,441,284-13,639,609, opened ~2022-2024) logged detained Jan-May 2026 with a lawyer notice dated before detention. Parsed fields side by side.
with p as (
  select try_to_number(split_part(CASE_TYPE, '\t', 1)) idn, split_part(CASE_TYPE, '\t', 2) city, split_part(CASE_TYPE, '\t', 3) st, split_part(CASE_TYPE, '\t', 4) zip,
    split_part(CASE_TYPE, '\t', 7) nat, split_part(CASE_TYPE, '\t', 8) lang, split_part(CASE_TYPE, '\t', 9) cust,
    left(split_part(CASE_TYPE, '\t', 11), 10) e28, split_part(CASE_TYPE, '\t', 13) ctype, split_part(CASE_TYPE, '\t', 14) site,
    left(split_part(CASE_TYPE, '\t', 15), 10) hear, split_part(CASE_TYPE, '\t', 17) cal, left(split_part(CASE_TYPE, '\t', 24), 10) entry,
    split_part(CASE_TYPE, '\t', 26) birth, left(split_part(CASE_TYPE, '\t', 29), 10) addr_changed, split_part(CASE_TYPE, '\t', 31) sex,
    left(split_part(CASE_TYPE, '\t', 32), 10) det, left(split_part(CASE_TYPE, '\t', 33), 10) rel, split_part(CASE_TYPE, '\t', 39) prio
  from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_EOIR_CASE_DATA
  where regexp_count(CASE_TYPE, '\t') = 38 and CASE_TYPE like '%\t2026-0%')
select * from p where idn >= 10441284 and idn < 13639610 and det between '2026-01-01' and '2026-05-31' and e28 < det
order by hash(idn) limit 6
