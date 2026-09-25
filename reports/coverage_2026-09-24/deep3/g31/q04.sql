-- Join test: DERA 10-Ks (my 5 quarters) to PCAOB Form AP by CIK (numeric) and fiscal period end; land rates
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
  select try_to_number(ISSUER_CIK) cik, FISCAL_PERIOD_END_DATE fpe, AUDIT_REPORT_TYPE, FIRM_ID, FIRM_NAME, ENGAGEMENT_PARTNER_ID, AUDIT_REPORT_DATE
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_PCAOB_FORM_AP_FILINGS where LATEST_FORM_AP_FILING='1' and try_to_number(ISSUER_CIK) is not null
), k as (select * from f where FORM='10-K' and q between '2024Q2' and '2025Q2'),
m as (
  select k.q, k.ADSH, k.AFS, k.days, k.hard_deadline,
    max(iff(ap.fpe = k.pd,1,0)) exact, max(iff(abs(datediff(day, ap.fpe, k.pd))<=7,1,0)) near7, max(iff(ap.cik is not null,1,0)) anycik
  from k left join ap on ap.cik = k.cik group by 1,2,3,4,5
)
select 'land' kind, q, AFS, count(*) n, sum(exact) exact, sum(near7) near7, sum(anycik) anycik,
  round(100*sum(near7)/count(*),1) near7_pct, count_if(days>hard_deadline) late, sum(iff(days>hard_deadline, near7, 0)) late_landed
from m group by 1,2,3
union all
select 'aptype', AUDIT_REPORT_TYPE, null, count(*), count(distinct cik), min(year(fpe)), max(year(fpe)), null, null, null from ap group by 1,2,3
order by 1,2,3
