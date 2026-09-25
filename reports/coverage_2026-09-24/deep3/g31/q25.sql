-- Harm join: insider open-market trades (Form 4, code S/P) at the 15 filed-before-audit companies, inside [10-K filed, audit report date] vs the 365 days before filing
with u as (
  select '2024Q1' q, * from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_DERA_SUB_2024Q1 union all
  select '2024Q2', * from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_DERA_SUB_2024Q2 union all
  select '2024Q3', * from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_DERA_SUB_2024Q3 union all
  select '2024Q4', * from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_DERA_SUB_2024Q4 union all
  select '2025Q1', * from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_DERA_SUB_2025Q1 union all
  select '2025Q2', * from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_DERA_SUB_2025Q2 union all
  select '2025Q3', * from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_DERA_SUB_2025Q3 union all
  select '2025Q4', * from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_DERA_SUB_2025Q4 union all
  select '2026Q1', * from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_DERA_SUB_2026Q1
), f as (
  select q, ADSH, try_to_number(CIK) cik, NAME, SIC, COUNTRYBA, STPRBA, CITYBA, STPRINC, COUNTRYINC, AFS, FORM, EIN,
    upper(regexp_replace(BAS1,'[^A-Za-z0-9]','')) a1, left(ZIPBA,5) zip, regexp_replace(BAPH,'[^0-9]','') ph,
    try_to_date(FILED,'YYYYMMDD') fd, try_to_date(PERIOD,'YYYYMMDD') pd,
    datediff(day, try_to_date(PERIOD,'YYYYMMDD'), try_to_date(FILED,'YYYYMMDD')) days,
    case when FORM='10-K' then case AFS when '1-LAF' then 60 when '2-ACC' then 75 else 90 end + 18
         when FORM='10-Q' then case AFS when '4-NON' then 45 else 40 end + 8 end hard_deadline
  from u
)
, apv as (select try_to_number(ISSUER_CIK) cik, FISCAL_PERIOD_END_DATE fpe, AUDIT_REPORT_DATE from LIBRARY_MARTS.FINANCE.FINANCE__FED_PCAOB_FORM_AP_FILINGS where try_to_number(ISSUER_CIK) is not null),
k as (select * from f where FORM='10-K' and q between '2024Q2' and '2025Q2'),
w as (
  select k.cik, k.NAME, k.fd, min(apv.AUDIT_REPORT_DATE) rpt
  from k join apv on apv.cik=k.cik and abs(datediff(day, apv.fpe, k.pd))<=7 group by 1,2,3
  having min(apv.AUDIT_REPORT_DATE) > dateadd(day, 3, k.fd)
),
subm as (
  select s.ACCESSION_NUMBER, try_to_number(s.ISSUER_CIK) cik from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_SUBMISSION s
  where try_to_number(s.ISSUER_CIK) in (select cik from w) and s.FILING_DATE between '2023-01-01' and '2026-09-30'
),
tr as (
  select subm.cik, t.TRANSACTION_DATE td, t.TRANSACTION_CODE code, t.SHARES, t.TRANSACTION_VALUE val
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_NONDERIV_TRANS t join subm on subm.ACCESSION_NUMBER=t.ACCESSION_NUMBER
  where t.TRANSACTION_CODE in ('S','P') and t.TRANSACTION_DATE between '2023-01-01' and '2026-09-30'
)
select w.NAME, w.fd k_filed, w.rpt audit_report, datediff(day, w.fd, w.rpt) window_days,
  count_if(tr.code='S' and tr.td between w.fd and w.rpt) sales_in_window, round(sum(iff(tr.code='S' and tr.td between w.fd and w.rpt, tr.val, 0))) sale_value_in_window,
  count_if(tr.code='P' and tr.td between w.fd and w.rpt) buys_in_window,
  count_if(tr.code='S' and tr.td between dateadd(day,-365,w.fd) and dateadd(day,-1,w.fd)) sales_prior_365, round(sum(iff(tr.code='S' and tr.td between dateadd(day,-365,w.fd) and dateadd(day,-1,w.fd), tr.val, 0))) sale_value_prior_365,
  count(tr.td) all_sp_trades_2023_26
from w left join tr on tr.cik=w.cik group by 1,2,3,4 order by sale_value_in_window desc
