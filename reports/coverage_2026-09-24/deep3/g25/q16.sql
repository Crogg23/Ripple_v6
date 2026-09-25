-- SEC insider: open-market SALES (code S) reported on Form 4 more than 10 days after the sale, by issuer. Peer = all issuers with 30+ sale filings.
-- Plus: late small buys (<= $10K, the Rule 16a-6 deferral) and a summary by exchange
with t as (select ACCESSION_NUMBER, min(case when TRANSACTION_CODE='S' then TRANSACTION_DATE end) s_min,
             min(case when TRANSACTION_CODE='P' then TRANSACTION_DATE end) p_min,
             sum(case when TRANSACTION_CODE='P' and PRICE_PER_SHARE between 0.01 and 5000 then SHARES*PRICE_PER_SHARE end) p_val,
             sum(case when TRANSACTION_CODE='S' and PRICE_PER_SHARE between 0.01 and 5000 then SHARES*PRICE_PER_SHARE end) s_val
           from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_NONDERIV_TRANS where TRANSACTION_CODE in ('P','S') group by 1),
o as (select ACCESSION_NUMBER, min(OWNER_CIK) owner from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_REPORTINGOWNER group by 1),
s as (select sub.ISSUER_CIK, sub.ISSUER_NAME, sub.FILING_DATE, t.*, o.owner,
        datediff('day', t.s_min, sub.FILING_DATE) slag, datediff('day', t.p_min, sub.FILING_DATE) plag
      from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_SUBMISSION sub join t on t.ACCESSION_NUMBER = sub.ACCESSION_NUMBER
      left join o on o.ACCESSION_NUMBER = sub.ACCESSION_NUMBER where sub.DOCUMENT_TYPE = '4'),
iss as (select ISSUER_CIK, max(ISSUER_NAME) nm, count_if(s_min is not null) sale_f, count_if(slag between 11 and 365) late_s,
          count(distinct iff(slag between 11 and 365, owner, null)) late_owners, count(distinct iff(s_min is not null, owner, null)) sale_owners,
          median(iff(slag between 11 and 365, slag, null)) med_late_days, round(sum(iff(slag between 11 and 365, s_val, 0))/1e6, 1) late_s_musd,
          count_if(slag between 11 and 365 and FILING_DATE >= '2023-10-01') late_s_post_sweep, count_if(s_min is not null and FILING_DATE >= '2023-10-01') sale_f_post,
          min(iff(slag between 11 and 365, FILING_DATE, null)) first_late, max(iff(slag between 11 and 365, FILING_DATE, null)) last_late
        from s group by 1),
pe as (select *, round(100*late_s/sale_f, 1) pct from iss where sale_f >= 30),
x as (select try_to_number(CIK) c, max(EXCHANGE) ex from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_EDGAR_COMPANY_TICKERS_EXCHANGE group by 1)
select 'top' k, ISSUER_CIK a, nm b, sale_f n1, late_s n2, pct n3, late_owners n4, sale_owners n5, med_late_days n6, late_s_musd n7, late_s_post_sweep n8, sale_f_post n9, first_late::text c, last_late::text d
from pe qualify row_number() over (order by late_s desc) <= 25
union all
select 'toppct', ISSUER_CIK, nm, sale_f, late_s, pct, late_owners, sale_owners, med_late_days, late_s_musd, late_s_post_sweep, sale_f_post, first_late::text, last_late::text
from pe where sale_f >= 60 qualify row_number() over (order by pct desc) <= 15
union all
select 'peer', 'issuers 30+ sale filings', null, count(*), sum(late_s), round(100*sum(late_s)/sum(sale_f),2), median(pct), percentile_cont(0.9) within group (order by pct),
  count_if(pct = 0), count_if(pct >= 10), null, null, null, null from pe
union all
select 'exch', coalesce(x.ex, 'no ticker match'), null, sum(sale_f), sum(late_s), round(100*sum(late_s)/nullif(sum(sale_f),0),2), count(*), null, null, null, null, null, null, null
from iss left join x on x.c = try_to_number(iss.ISSUER_CIK) group by 2
union all
select 'buys', 'late buys 11-365d', null, count_if(p_min is not null), count_if(plag between 11 and 365), count_if(plag between 11 and 365 and p_val <= 10000),
  count_if(p_min is not null and p_val <= 10000), median(iff(plag between 11 and 365, p_val, null)), median(iff(p_min is not null, p_val, null)), null, null, null, null, null from s
order by 1, 5 desc
