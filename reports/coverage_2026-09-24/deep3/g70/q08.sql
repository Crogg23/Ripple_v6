-- ICE hold rooms (TYPE_DETAILED = Hold) ranked against each other: Oct 1 - Feb 28 window FY24, FY25, FY26; stints over 24 and 72 hours, median hours, name and place from FACILITY_CODES
with f as (select DETENTION_FACILITY_CODE code, DETENTION_FACILITY_NAME nm, CITY, STATE, AOR from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_FACILITY_CODES where TYPE_DETAILED = 'Hold'),
s as (select DETENTION_FACILITY_CODE code, datediff(minute, BOOK_IN_AT, BOOK_OUT_AT) / 60.0 hrs,
        case when BOOK_IN_AT >= '2023-10-01' and BOOK_IN_AT < '2024-03-01' then 'FY24'
             when BOOK_IN_AT >= '2024-10-01' and BOOK_IN_AT < '2025-03-01' then 'FY25'
             when BOOK_IN_AT >= '2025-10-01' and BOOK_IN_AT < '2026-03-01' then 'FY26' end fy
      from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_STINTS
      where coalesce(DUPLICATE_DROP_ROW, 'False') <> 'True' and BOOK_OUT_AT is not null),
g as (select f.code, f.nm, f.CITY, f.STATE, f.AOR,
        count_if(fy = 'FY24') n24, count_if(fy = 'FY24' and hrs > 24) o24_24,
        count_if(fy = 'FY25') n25, count_if(fy = 'FY25' and hrs > 24) o24_25, count_if(fy = 'FY25' and hrs > 72) o72_25,
        count_if(fy = 'FY26') n26, count_if(fy = 'FY26' and hrs > 24) o24_26, count_if(fy = 'FY26' and hrs > 72) o72_26,
        round(median(iff(fy = 'FY26', hrs, null)), 1) med26, round(median(iff(fy = 'FY25', hrs, null)), 1) med25, round(max(iff(fy = 'FY26', hrs, null)), 0) max26
      from s join f on f.code = s.code group by 1, 2, 3, 4, 5)
select * from (select 'site' k, g.*, round(100 * o24_26 / nullif(n26, 0), 1) pct24_26, round(100 * o24_25 / nullif(n25, 0), 1) pct24_25 from g where n26 >= 100 or n25 >= 100 order by o24_26 desc limit 25)
union all select 'all_sites', null, count(*)::text, null, null, null, sum(n24), sum(o24_24), sum(n25), sum(o24_25), sum(o72_25), sum(n26), sum(o24_26), sum(o72_26), null, null, null,
  round(median(iff(n26 >= 100, 100 * o24_26 / n26, null)), 1), round(median(iff(n25 >= 100, 100 * o24_25 / n25, null)), 1) from g
