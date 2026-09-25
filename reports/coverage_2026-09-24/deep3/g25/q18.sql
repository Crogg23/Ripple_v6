-- SEC insider: eyeball the late open-market sale filings (11-365 days) at six high-ranked issuers: who, when sold, when filed, how much
with t as (select ACCESSION_NUMBER, min(TRANSACTION_DATE) s_min, max(TRANSACTION_DATE) s_max, count(*) n_s, sum(SHARES) sh,
             sum(iff(PRICE_PER_SHARE between 0.01 and 5000, SHARES*PRICE_PER_SHARE, null)) val, min(PRICE_PER_SHARE) pmin, max(PRICE_PER_SHARE) pmax
           from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_NONDERIV_TRANS where TRANSACTION_CODE = 'S' group by 1),
o as (select ACCESSION_NUMBER, listagg(distinct OWNER_NAME, ' + ') nm, listagg(distinct coalesce(nullif(TITLE,''), RELATIONSHIP), ' + ') ttl
      from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_REPORTINGOWNER group by 1)
select sub.ISSUER_NAME, o.nm, left(o.ttl, 60) ttl, t.s_min, t.s_max, sub.FILING_DATE, datediff('day', t.s_min, sub.FILING_DATE) lag,
  t.n_s, round(t.sh) shares, round(t.val) usd, t.pmin, t.pmax, sub.ACCESSION_NUMBER, left(sub.REMARKS, 80) remarks
from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_SUBMISSION sub join t on t.ACCESSION_NUMBER = sub.ACCESSION_NUMBER
left join o on o.ACCESSION_NUMBER = sub.ACCESSION_NUMBER
where sub.DOCUMENT_TYPE = '4' and datediff('day', t.s_min, sub.FILING_DATE) between 11 and 365
  and sub.ISSUER_CIK in ('0001341766','0001476840','0001624512','0001436208','0000834365','0001562088')
order by sub.ISSUER_NAME, t.val desc nulls last
