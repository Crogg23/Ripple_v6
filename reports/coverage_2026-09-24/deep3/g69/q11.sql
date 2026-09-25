-- Cross-check against an independent source: ICE detention stays (FED_ICE_DETENTION_STINTS) by month of stay book-in, 2023-01 to 2026-05.
-- Aggregate only (no row join; the tables share no key). Stays, stays whose entry date is 2+ years before book-in, stays whose current ICE case category is [3] (under adjudication by an immigration judge)
with s as (
  select STAY_ID, try_to_date(left(STAY_BOOK_IN_AT::string, 10), 'YYYY-MM-DD') bin,
    try_to_date(left(ENTRY_DATE::string, 10), 'YYYY-MM-DD') entry, CASE_CATEGORY cc, FINAL_PROGRAM fp
  from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_STINTS)
select date_trunc(month, bin)::date mo, count(distinct STAY_ID) stays,
  count(distinct iff(datediff(day, entry, bin) > 730, STAY_ID, null)) stays_entry_2y,
  count(distinct iff(cc like '[3]%', STAY_ID, null)) stays_cat3_ij,
  count(distinct iff(fp ilike '%border patrol%', STAY_ID, null)) stays_bp,
  (select max(try_to_date(left(STAY_BOOK_IN_AT::string, 10), 'YYYY-MM-DD')) from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_STINTS) max_bin
from s where bin >= '2023-01-01' and bin < '2026-06-01'
group by 1 order by 1
