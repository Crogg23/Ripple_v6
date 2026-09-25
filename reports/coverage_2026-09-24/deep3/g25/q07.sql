-- SEC insider: nonderivative transaction codes, and how many Form 4 accessions land in the transaction table
with t as (select ACCESSION_NUMBER, count(*) n, count_if(TRANSACTION_CODE in ('P','S')) nps from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_NONDERIV_TRANS group by 1)
select 'code' k, TRANSACTION_CODE a, FORM_TYPE b, count(*) n, count(distinct ACCESSION_NUMBER) m,
  count_if(TRANSACTION_DATE is null) x, count_if(year(TRANSACTION_DATE) < 2000 or year(TRANSACTION_DATE) > 2026) y
from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_NONDERIV_TRANS group by 2,3
union all
select 'land', s.DOCUMENT_TYPE, null, count(*), count(t.ACCESSION_NUMBER), count_if(t.nps > 0), count_if(t.nps = t.n)
from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_SUBMISSION s left join t on t.ACCESSION_NUMBER = s.ACCESSION_NUMBER
group by 2
order by 1, 4 desc
