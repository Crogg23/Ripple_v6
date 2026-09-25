-- SEC insider hostile check: were the same sales also reported ON TIME by another filer? Every Form 4/4-A with a sale in the three windows, all filers
with t as (select ACCESSION_NUMBER, min(TRANSACTION_DATE) s_min, max(TRANSACTION_DATE) s_max, count(*) n_s, round(sum(SHARES)) sh
           from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_NONDERIV_TRANS where TRANSACTION_CODE = 'S' group by 1),
o as (select ACCESSION_NUMBER, left(listagg(distinct OWNER_NAME, ' + '), 90) nm from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_REPORTINGOWNER group by 1)
select sub.ISSUER_NAME, sub.DOCUMENT_TYPE, o.nm, t.s_min, t.s_max, sub.FILING_DATE, datediff('day', t.s_min, sub.FILING_DATE) lag, t.n_s, t.sh, sub.ACCESSION_NUMBER
from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_SUBMISSION sub join t on t.ACCESSION_NUMBER = sub.ACCESSION_NUMBER
left join o on o.ACCESSION_NUMBER = sub.ACCESSION_NUMBER
where (sub.ISSUER_CIK = '0001341766' and t.s_max >= '2024-04-25' and t.s_min <= '2024-05-10')
   or (sub.ISSUER_CIK = '0001562088' and t.s_max >= '2021-11-10' and t.s_min <= '2021-12-05')
   or (sub.ISSUER_CIK = '0000834365' and t.s_max >= '2019-10-01' and t.s_min <= '2020-06-05' and o.nm ilike any ('%WAVI%', '%VILLIGER%', '%GIRSCHWEILER%', '%TAURUS%'))
order by 1, 4, 6
