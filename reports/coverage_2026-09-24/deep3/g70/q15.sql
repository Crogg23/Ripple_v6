-- ICE hold-room stints over 24 hours, Oct 2025 - Feb 2026: is the person booked somewhere else at the same time (a paper booking, not a body in the room)? overlap with any other stint of the same person at another code; by site for the top six
with f as (select DETENTION_FACILITY_CODE code, TYPE_DETAILED td from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_FACILITY_CODES),
all_s as (select STINT_ID, PERSON_HASH, DETENTION_FACILITY_CODE code, BOOK_IN_AT, coalesce(BOOK_OUT_AT, '2026-03-12'::timestamp) BOOK_OUT_AT
      from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_STINTS
      where coalesce(DUPLICATE_DROP_ROW, 'False') <> 'True' and BOOK_IN_AT >= '2025-06-01'),
h as (select a.* from all_s a join f on f.code = a.code
      where f.td = 'Hold' and a.BOOK_IN_AT >= '2025-10-01' and a.BOOK_IN_AT < '2026-03-01' and datediff(minute, a.BOOK_IN_AT, a.BOOK_OUT_AT) > 24 * 60),
ov as (select h.STINT_ID, max(datediff(minute, greatest(h.BOOK_IN_AT, o.BOOK_IN_AT), least(h.BOOK_OUT_AT, o.BOOK_OUT_AT))) / 60.0 ov_hrs
       from h join all_s o on o.PERSON_HASH = h.PERSON_HASH and o.STINT_ID <> h.STINT_ID and o.code <> h.code
         and o.BOOK_IN_AT < h.BOOK_OUT_AT and o.BOOK_OUT_AT > h.BOOK_IN_AT group by 1)
select iff(h.code in ('BALHOLD', 'IWAHOLD', 'DALHOLD', 'ATLHOLD', 'PHOHOLD', 'LOSHOLD'), h.code, 'all other hold sites') site,
  count(*) stints_over_24h, count(ov.STINT_ID) with_any_overlap, count_if(ov.ov_hrs > 1) overlap_over_1h, count_if(ov.ov_hrs > 12) overlap_over_12h,
  round(median(datediff(minute, h.BOOK_IN_AT, h.BOOK_OUT_AT)) / 60.0, 1) med_hrs
from h left join ov on ov.STINT_ID = h.STINT_ID group by 1 order by 2 desc
