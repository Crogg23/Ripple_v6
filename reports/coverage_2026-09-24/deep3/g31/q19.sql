-- 10-Ks (my five quarters) whose matching audit reports (same CIK, fiscal period end within 7 days) are ALL dated after the 10-K was filed
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
, ap as (
  select try_to_number(ISSUER_CIK) cik, FISCAL_PERIOD_END_DATE fpe, FIRM_NAME, AUDIT_REPORT_DATE, DUAL_DATED, AUDIT_DUAL_DATE, IS_MULTIPLE_AUDIT_PERIOD
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_PCAOB_FORM_AP_FILINGS
  where LATEST_FORM_AP_FILING='1' and try_to_number(ISSUER_CIK) is not null
), k as (select * from f where FORM='10-K' and q between '2024Q2' and '2025Q2'),
m as (
  select k.q, k.cik, k.NAME, k.AFS, k.STPRBA, k.pd, k.fd, k.days,
    count(*) n_ap, min(ap.AUDIT_REPORT_DATE) first_report, max(ap.AUDIT_REPORT_DATE) last_report,
    listagg(distinct ap.FIRM_NAME, ' / ') firms, max(ap.DUAL_DATED) dual
  from k join ap on ap.cik=k.cik and abs(datediff(day, ap.fpe, k.pd))<=7
  group by 1,2,3,4,5,6,7,8
),
kk as (select cik, pd, count(*) n_k, listagg(fd::text, ',') within group (order by fd) k_filed_dates from f where FORM in ('10-K','10-K/A') group by 1,2)
select 'summary' k, null q, count(*)::text n_10k_matched, count_if(first_report > fd)::text report_after_filing,
  count_if(first_report > dateadd(day, 3, fd))::text report_4plus_days_after, count_if(first_report > dateadd(day, 30, fd))::text report_31plus_days_after,
  null a, null b, null c, null d, null e
from m
union all
select 'row', m.q, m.NAME, m.AFS, m.fd::text, m.first_report::text, datediff(day, m.fd, m.first_report)::text, m.firms, m.pd::text, kk.k_filed_dates, m.dual
from m left join kk on kk.cik=m.cik and kk.pd=m.pd
where m.first_report > dateadd(day, 3, m.fd)
order by 1 desc, 7 desc
