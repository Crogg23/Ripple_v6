-- SEC insider: sale-only late rate by year and by exchange group (time x peer), and insiders with the most late sale filings across all issuers
with t as (select ACCESSION_NUMBER, min(TRANSACTION_DATE) s_min,
             sum(iff(PRICE_PER_SHARE between 0.01 and 5000, SHARES*PRICE_PER_SHARE, null)) val
           from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_NONDERIV_TRANS where TRANSACTION_CODE = 'S' group by 1),
x as (select try_to_number(CIK) c, max(EXCHANGE) ex from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_EDGAR_COMPANY_TICKERS_EXCHANGE group by 1),
s as (select sub.ACCESSION_NUMBER, sub.ISSUER_NAME, year(sub.FILING_DATE) yr, datediff('day', t.s_min, sub.FILING_DATE) lag, t.val,
        case when x.ex in ('NYSE','Nasdaq') then 'NYSE/Nasdaq' when x.ex = 'OTC' then 'OTC' else 'other/none' end grp
      from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_SUBMISSION sub join t on t.ACCESSION_NUMBER = sub.ACCESSION_NUMBER
      left join x on x.c = try_to_number(sub.ISSUER_CIK) where sub.DOCUMENT_TYPE = '4'),
o as (select r.ACCESSION_NUMBER, r.OWNER_CIK, r.OWNER_NAME from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_REPORTINGOWNER r
      where r.ACCESSION_NUMBER in (select ACCESSION_NUMBER from s where lag between 11 and 365))
select 'yr' k, yr::text a, grp b, count(*) n, count_if(lag between 11 and 365) late, round(100*count_if(lag between 11 and 365)/count(*), 2) pct,
  round(sum(iff(lag between 11 and 365, val, 0))/1e6) late_musd, null c
from s group by 2, 3
union all
select 'owner', o.OWNER_CIK, max(o.OWNER_NAME), count(distinct s.ACCESSION_NUMBER), count(distinct s.ISSUER_NAME), median(s.lag),
  round(sum(s.val)/1e6, 1), left(listagg(distinct s.ISSUER_NAME, ' / '), 120)
from o join s on s.ACCESSION_NUMBER = o.ACCESSION_NUMBER group by 2 qualify row_number() over (order by count(distinct s.ACCESSION_NUMBER) desc) <= 15
order by 1, 2, 3
