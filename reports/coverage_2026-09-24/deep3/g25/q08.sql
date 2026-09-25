-- SEC insider: Form 4s holding an open-market buy (P) or sale (S): days from the earliest P/S trade to filing, by filing year
with t as (
  select ACCESSION_NUMBER, min(case when TRANSACTION_CODE in ('P','S') then TRANSACTION_DATE end) ps_min,
    count_if(TRANSACTION_CODE in ('P','S')) nps, count_if(TRANSACTION_CODE = 'S') ns, count_if(TRANSACTION_CODE = 'P') np,
    sum(case when TRANSACTION_CODE in ('P','S') then TRANSACTION_VALUE end) ps_val
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_NONDERIV_TRANS group by 1 having count_if(TRANSACTION_CODE in ('P','S')) > 0),
j as (select year(s.FILING_DATE) yr, datediff('day', t.ps_min, s.FILING_DATE) lag, t.*
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_SUBMISSION s join t on t.ACCESSION_NUMBER = s.ACCESSION_NUMBER
  where s.DOCUMENT_TYPE = '4')
select yr, count(*) ps_filings, count_if(np > 0) with_buy, count_if(ns > 0) with_sale,
  count_if(lag < 0) neg, count_if(lag between 0 and 5) ontime_0_5, count_if(lag between 6 and 10) d6_10,
  count_if(lag between 11 and 30) d11_30, count_if(lag between 31 and 365) d31_365, count_if(lag > 365) gt365,
  round(100 * count_if(lag between 11 and 365) / count(*), 2) pct_late_11_365,
  round(100 * count_if(np > 0 and lag between 11 and 365) / nullif(count_if(np > 0), 0), 2) pct_late_buy,
  round(100 * count_if(ns > 0 and lag between 11 and 365) / nullif(count_if(ns > 0), 0), 2) pct_late_sale,
  round(sum(case when lag between 11 and 365 then ps_val end) / 1e9, 2) late_val_bn, round(sum(ps_val) / 1e9, 1) all_val_bn
from j group by 1 order by 1
