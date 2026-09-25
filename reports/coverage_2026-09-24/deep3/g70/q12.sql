-- ICE hold rooms by book-in month, Oct 2022 - Feb 2026: all Hold sites, the top four sites, and Staging sites as the control; stints and stints over 24 / 72 hours
with f as (select DETENTION_FACILITY_CODE code, TYPE_DETAILED td from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_FACILITY_CODES where TYPE_GROUPED = 'Hold/Staging'),
s as (select DETENTION_FACILITY_CODE code, to_char(BOOK_IN_AT, 'YYYY-MM') ym, datediff(minute, BOOK_IN_AT, BOOK_OUT_AT) / 60.0 hrs
      from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_STINTS
      where coalesce(DUPLICATE_DROP_ROW, 'False') <> 'True' and BOOK_IN_AT >= '2022-10-01' and BOOK_IN_AT < '2026-03-01')
select ym,
  count_if(f.td = 'Hold') hold_n, count_if(f.td = 'Hold' and hrs > 24) hold_24, count_if(f.td = 'Hold' and hrs > 72) hold_72,
  count_if(f.td = 'Hold' and hrs > 24 and s.code not in ('BALHOLD', 'IWAHOLD', 'DALHOLD', 'ATLHOLD')) hold_24_ex_top4,
  count_if(s.code = 'BALHOLD') bal_n, count_if(s.code = 'BALHOLD' and hrs > 24) bal_24,
  count_if(s.code = 'IWAHOLD') mesa_n, count_if(s.code = 'IWAHOLD' and hrs > 24) mesa_24,
  count_if(s.code = 'DALHOLD') dal_n, count_if(s.code = 'DALHOLD' and hrs > 24) dal_24,
  count_if(s.code = 'ATLHOLD') atl_n, count_if(s.code = 'ATLHOLD' and hrs > 24) atl_24,
  count_if(f.td = 'Staging') stg_n, round(100 * count_if(f.td = 'Staging' and hrs > 24) / nullif(count_if(f.td = 'Staging' and hrs is not null), 0), 1) stg_pct24,
  count(distinct iff(f.td = 'Hold' and hrs > 24, s.code, null)) hold_sites_with_24
from s join f on f.code = s.code group by 1 order by 1
