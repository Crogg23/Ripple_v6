-- (rerun of q26 with the topmirror pct fixed) SEC insider dedupe: drop late sale filings that mirror an ON-TIME filing (same issuer, same first sale date, same total shares, filed within 5 days).
-- Re-rank issuers (30+ sale filings) on the late filings that remain; peer median and 90th percentile after the dedupe
with t as (select ACCESSION_NUMBER, min(TRANSACTION_DATE) s_min, round(sum(SHARES)) sh,
             sum(iff(PRICE_PER_SHARE between 0.01 and 5000, SHARES*PRICE_PER_SHARE, null)) val
           from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_NONDERIV_TRANS where TRANSACTION_CODE = 'S' group by 1),
f as (select sub.ISSUER_CIK, sub.ISSUER_NAME, sub.ACCESSION_NUMBER, sub.FILING_DATE, t.s_min, t.sh, t.val, datediff('day', t.s_min, sub.FILING_DATE) lag
      from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_SUBMISSION sub join t on t.ACCESSION_NUMBER = sub.ACCESSION_NUMBER where sub.DOCUMENT_TYPE = '4'),
late as (select f.*, exists (select 1 from f f2 where f2.ISSUER_CIK = f.ISSUER_CIK and f2.s_min = f.s_min and f2.sh = f.sh
                                and f2.lag between 0 and 5 and f2.ACCESSION_NUMBER <> f.ACCESSION_NUMBER) mirrored
         from f where lag between 11 and 365),
iss as (select f.ISSUER_CIK, max(f.ISSUER_NAME) nm, count(*) sale_f,
          count(l.ACCESSION_NUMBER) late_all, count_if(l.mirrored) late_mirrored, count_if(not l.mirrored) late_real,
          round(sum(iff(not l.mirrored, l.val, 0))/1e6, 1) late_real_musd, count_if(not l.mirrored and l.FILING_DATE >= '2023-10-01') late_real_post
        from f left join late l on l.ACCESSION_NUMBER = f.ACCESSION_NUMBER group by 1),
pe as (select *, round(100*late_real/sale_f, 1) pct from iss where sale_f >= 30)
select 'all' k, null a, null b, (select count(*) from f) n1, (select count(*) from late) n2, (select count_if(mirrored) from late) n3,
  (select count_if(not mirrored) from late) n4, null n5, null n6, null n7
union all
select 'peer', null, null, count(*), sum(late_real), median(pct), percentile_cont(0.9) within group (order by pct), count_if(pct >= 10), count_if(pct = 0), null from pe
union all
select 'top', ISSUER_CIK, nm, sale_f, late_all, late_mirrored, late_real, pct, late_real_musd, late_real_post
from pe qualify row_number() over (order by late_real desc) <= 20
union all
select 'topmirror', ISSUER_CIK, nm, sale_f, late_all, late_mirrored, late_real, round(100*late_real/sale_f, 1), late_real_musd, late_real_post
from iss qualify row_number() over (order by late_mirrored desc) <= 8
order by 1, 7 desc
