-- CFTC lead hunt: which markets have their 4 biggest traders holding more of one side now than ever?
-- Now = the 13 report dates 2026-05-05 .. 2026-08-04. History = 2016-2025 same market (trimmed code).
-- Only markets with 300+ history weeks and 50+ traders now (thin markets are concentrated by arithmetic).
with f as (select trim(CFTC_CONTRACT_MARKET_CODE) code, MARKET_AND_EXCHANGE_NAMES nm, AS_OF_DATE_IN_FORM_YYYY_MM_DD d,
             try_to_number(trim(OPEN_INTEREST_ALL)) oi, try_to_number(trim(TRADERS_TOTAL_ALL)) tr,
             CONCENTRATION_GROSS_LT_4_TDR_SHORT_ALL g4s, CONCENTRATION_GROSS_LT_4_TDR_LONG_ALL g4l
           from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_CFTC_COT_FUTURES
           where AS_OF_DATE_IN_FORM_YYYY_MM_DD >= '2016-01-01' and greatest(g4s, g4l) <= 100),
h as (select code, count(*) wks, median(g4s) med_s, max(g4s) max_s, median(g4l) med_l, max(g4l) max_l, median(oi) med_oi, median(tr) med_tr
      from f where d < '2026-01-01' group by 1),
n as (select code, max_by(nm, d) nm, count(*) wks_now, avg(g4s) now_s, max(g4s) now_max_s, avg(g4l) now_l, max(g4l) now_max_l, avg(oi) now_oi, avg(tr) now_tr
      from f where d between '2026-05-05' and '2026-08-04' group by 1),
j as (select n.*, h.wks, h.med_s, h.max_s, h.med_l, h.max_l, h.med_oi, h.med_tr,
        n.now_s - h.med_s d_s, n.now_l - h.med_l d_l
      from n join h on h.code = n.code where h.wks >= 300 and n.now_tr >= 50 and n.wks_now >= 10)
select code, left(nm,55) nm, round(now_s,1) now_s, round(med_s,1) med_s, round(max_s,1) hist_max_s, round(now_max_s,1) now_max_s,
  round(now_l,1) now_l, round(med_l,1) med_l, round(max_l,1) hist_max_l, round(now_max_l,1) now_max_l,
  round(now_oi,0) now_oi, med_oi, round(now_tr,0) now_tr, med_tr, wks,
  round(median(d_s) over (),1) peer_med_d_s, round(median(d_l) over (),1) peer_med_d_l, count(*) over () n_mkts,
  count_if(now_max_s > max_s) over () n_record_s, count_if(now_max_l > max_l) over () n_record_l
from j
qualify row_number() over (order by greatest(d_s, d_l) desc) <= 30
order by greatest(d_s, d_l) desc
