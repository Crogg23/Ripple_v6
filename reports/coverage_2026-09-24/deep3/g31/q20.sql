-- Rule out the version filter: recompute filed-before-audit 10-Ks using EVERY Form AP version (latest or not); add ticker/exchange
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
, apv as (
  select try_to_number(ISSUER_CIK) cik, FISCAL_PERIOD_END_DATE fpe, FIRM_NAME, AUDIT_REPORT_DATE, LATEST_FORM_AP_FILING, AMENDMENT_PREVIOUS_FILING
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_PCAOB_FORM_AP_FILINGS where try_to_number(ISSUER_CIK) is not null
), k as (select * from f where FORM='10-K' and q between '2024Q2' and '2025Q2'),
m as (
  select k.q, k.cik, k.NAME, k.AFS, k.pd, k.fd,
    count(*) ap_versions, min(apv.AUDIT_REPORT_DATE) earliest_any_version, max(apv.AUDIT_REPORT_DATE) latest_report,
    listagg(distinct apv.FIRM_NAME, ' / ') firms,
    listagg(apv.LATEST_FORM_AP_FILING || ':' || apv.AUDIT_REPORT_DATE || ':' || coalesce(apv.AMENDMENT_PREVIOUS_FILING,''), ' ; ') versions
  from k join apv on apv.cik=k.cik and abs(datediff(day, apv.fpe, k.pd))<=7 group by 1,2,3,4,5,6
),
ka as (select cik, pd, listagg(FORM || ' ' || fd::text, ', ') within group (order by fd) later_filings from f where FORM in ('10-K','10-K/A') group by 1,2),
tk as (select CIK cik, listagg(distinct TICKER, '/') tickers, listagg(distinct EXCHANGE, '/') exch from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_EDGAR_COMPANY_TICKERS_EXCHANGE group by 1)
select m.cik, m.NAME, m.AFS, m.pd, m.fd k_filed, m.earliest_any_version, datediff(day, m.fd, m.earliest_any_version) gap_days, m.ap_versions, m.firms, m.versions, ka.later_filings, tk.tickers, tk.exch
from m left join ka on ka.cik=m.cik and ka.pd=m.pd left join tk on tk.cik=m.cik
where m.earliest_any_version > dateadd(day, 3, m.fd)
order by gap_days desc
