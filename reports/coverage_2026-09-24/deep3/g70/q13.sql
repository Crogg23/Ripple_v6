-- ICE hold-room stints over 24 hours, Oct 2025 - Feb 2026: distinct people, how the stint ended, what kind of place came next in the same stay, and the same for Oct 2024 - Feb 2025
with f as (select DETENTION_FACILITY_CODE code, TYPE_DETAILED td, TYPE_GROUPED tg from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_FACILITY_CODES),
s as (select STAY_ID, PERSON_HASH, DETENTION_FACILITY_CODE code, BOOK_IN_AT, BOOK_OUT_AT, DETENTION_RELEASE_REASON rr, GENDER, BIRTH_YEAR,
        datediff(minute, BOOK_IN_AT, BOOK_OUT_AT) / 60.0 hrs,
        lead(DETENTION_FACILITY_CODE) over (partition by STAY_ID order by BOOK_IN_AT, BOOK_OUT_AT) next_code
      from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_STINTS
      where coalesce(DUPLICATE_DROP_ROW, 'False') <> 'True' and BOOK_IN_AT >= '2024-10-01' and STAY_ID is not null),
h as (select s.*, iff(BOOK_IN_AT >= '2025-10-01', 'FY26', 'FY25') fy from s join f on f.code = s.code
      where f.td = 'Hold' and hrs > 24 and ((BOOK_IN_AT >= '2025-10-01' and BOOK_IN_AT < '2026-03-01') or (BOOK_IN_AT < '2025-03-01')))
select 'people' k, fy, count(*)::text a, count(distinct PERSON_HASH)::text b, count_if(GENDER = 'Female')::text c, count_if(BIRTH_YEAR >= 2008)::text d from h group by 2
union all select * from (select 'release_reason', fy, rr, count(*)::text, null, null from h group by 2, 3 order by 4 desc limit 16)
union all select 'next_place', fy, coalesce(nf.tg, iff(h.next_code is null, '(none: stay ended)', '(code not in lookup)')), count(*)::text, null, null from h left join f nf on nf.code = h.next_code group by 2, 3
