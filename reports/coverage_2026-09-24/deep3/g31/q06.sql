-- (rewrite of q05 without correlated subquery) 10-Ks in my five quarters with NO Form AP within 7 days of period end, plus last auditor
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
  select try_to_number(ISSUER_CIK) cik, FISCAL_PERIOD_END_DATE fpe, FIRM_NAME, ENGAGEMENT_PARTNER_ID, AUDIT_REPORT_DATE, AUDIT_REPORT_TYPE
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_PCAOB_FORM_AP_FILINGS where LATEST_FORM_AP_FILING='1' and try_to_number(ISSUER_CIK) is not null
), k as (select * from f where FORM='10-K' and q between '2024Q2' and '2025Q2'),
km as (select k.ADSH, max(iff(abs(datediff(day, ap.fpe, k.pd))<=7,1,0)) hit from k left join ap on ap.cik=k.cik group by 1),
nomatch as (select k.* from k join km on km.ADSH=k.ADSH where km.hit=0),
lastap as (
  select cik, FIRM_NAME, fpe, AUDIT_REPORT_DATE, AUDIT_REPORT_TYPE, row_number() over (partition by cik order by fpe desc, AUDIT_REPORT_DATE desc) rn,
    count(*) over (partition by cik) n_ap from ap
)
select n.q, n.cik, n.NAME, n.AFS, n.SIC, n.COUNTRYBA, n.STPRBA, n.pd, n.fd, n.days, n.days > n.hard_deadline late,
  l.FIRM_NAME last_firm, l.fpe last_fpe, l.AUDIT_REPORT_DATE last_report, l.n_ap, l.AUDIT_REPORT_TYPE
from nomatch n left join lastap l on l.cik=n.cik and l.rn=1
order by l.FIRM_NAME nulls first, n.q
