-- ICE hold rooms and staging sites (type from FACILITY_CODES): stint length, same Oct 1 - Feb 28 window in FY23-FY26; drop rows ICE's own file flags as duplicates; midnight book-outs counted to catch date-only stamps
with f as (select DETENTION_FACILITY_CODE code, TYPE_DETAILED td from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_FACILITY_CODES where TYPE_GROUPED = 'Hold/Staging'),
s as (select DETENTION_FACILITY_CODE code, BOOK_IN_AT, BOOK_OUT_AT, datediff(minute, BOOK_IN_AT, BOOK_OUT_AT) / 60.0 hrs,
        case when BOOK_IN_AT >= '2022-10-01' and BOOK_IN_AT < '2023-03-01' then 'FY23'
             when BOOK_IN_AT >= '2023-10-01' and BOOK_IN_AT < '2024-03-01' then 'FY24'
             when BOOK_IN_AT >= '2024-10-01' and BOOK_IN_AT < '2025-03-01' then 'FY25'
             when BOOK_IN_AT >= '2025-10-01' and BOOK_IN_AT < '2026-03-01' then 'FY26' end fy
      from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_STINTS
      where coalesce(DUPLICATE_DROP_ROW, 'False') <> 'True')
select coalesce(f.td, '(blank)') td, s.fy, count(*) stints, count(distinct s.code) sites, count_if(BOOK_OUT_AT is null) still_open,
  round(median(hrs), 1) med_hrs, round(percentile_cont(0.9) within group (order by hrs), 1) p90_hrs,
  count_if(hrs > 12) gt12h, round(100 * count_if(hrs > 12) / count_if(hrs is not null), 1) pct_gt12h,
  count_if(hrs > 24) gt24h, round(100 * count_if(hrs > 24) / count_if(hrs is not null), 1) pct_gt24h,
  count_if(hrs > 72) gt72h, count_if(hrs > 168) gt7d, round(max(hrs), 0) max_hrs,
  count_if(hrs < 0) neg, count_if(to_time(BOOK_OUT_AT) = '00:00:00') midnight_out
from s join f on f.code = s.code where s.fy is not null group by 1, 2 order by 1, 2
