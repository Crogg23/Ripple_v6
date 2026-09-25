-- Dull-explanation test for the top late firms: remove ex-Borgers clients; add partner count and client growth by audit-report year
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
  select try_to_number(ISSUER_CIK) cik, FISCAL_PERIOD_END_DATE fpe, FIRM_ID, FIRM_NAME, ENGAGEMENT_PARTNER_ID, AUDIT_REPORT_DATE
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_PCAOB_FORM_AP_FILINGS
  where LATEST_FORM_AP_FILING='1' and try_to_number(ISSUER_CIK) is not null
    and AUDIT_REPORT_TYPE='Issuer, other than Employee Benefit Plan or Investment Company'
), pre as (select * from ap where AUDIT_REPORT_DATE between '2023-01-01' and '2024-05-02'),
lastpre as (select cik, FIRM_ID, FIRM_NAME from pre qualify row_number() over (partition by cik order by AUDIT_REPORT_DATE desc, fpe desc)=1),
fsize as (select FIRM_ID, count(distinct cik) firm_clients from pre group by 1),
base as (
  select cik, max(AFS) afs, max(SIC) sic, max(COUNTRYBA) ctry, max(NAME) name from f
  where q in ('2024Q1','2024Q2') and FORM in ('10-K','10-Q') and fd < '2024-05-03' group by 1
),
after as (
  select cik,
    max(iff(q between '2025Q3' and '2026Q1' and FORM in ('10-K','10-Q'),1,0)) still_filing,
    max(iff(q between '2024Q3' and '2026Q1' and FORM in ('10-K','10-Q'),1,0)) any_after_q2,
    max(iff(q between '2025Q1' and '2026Q1' and FORM='10-K',1,0)) k_2025on,
    count_if(q between '2024Q3' and '2025Q2' and FORM in ('10-K','10-Q')) per_n,
    count_if(q between '2024Q3' and '2025Q2' and FORM in ('10-K','10-Q') and days > hard_deadline) per_late
  from f group by 1
)
, borg as (select distinct cik from ap where FIRM_NAME ilike '%borgers%' and AUDIT_REPORT_DATE >= '2022-01-01'),
p as (select * from f where FORM in ('10-K','10-Q') and AFS='4-NON' and q between '2024Q2' and '2025Q2'),
pa as (
  select p.ADSH, p.cik, p.days, p.hard_deadline, ap.FIRM_ID, ap.FIRM_NAME, iff(b.cik is not null,1,0) exborg
  from p join ap on ap.cik=p.cik and ap.AUDIT_REPORT_DATE <= p.fd left join borg b on b.cik=p.cik
  qualify row_number() over (partition by p.ADSH order by ap.AUDIT_REPORT_DATE desc, ap.fpe desc)=1
),
sel as (select FIRM_ID from pa group by 1 having count(*)>=40 and count_if(days>hard_deadline)/count(*) >= 0.2),
lat as (
  select FIRM_ID, any_value(FIRM_NAME) firm, count(*) n, count_if(days>hard_deadline) late,
    count(distinct iff(exborg=1, cik, null)) exborg_clients, count(distinct cik) clients,
    count_if(exborg=0) n_nonborg, count_if(exborg=0 and days>hard_deadline) late_nonborg
  from pa where FIRM_ID in (select FIRM_ID from sel) group by 1
),
grow as (
  select FIRM_ID, any_value(FIRM_COUNTRY) country, any_value(FIRM_ISSUING_CITY) city,
    count(distinct iff(year(AUDIT_REPORT_DATE)=2022, ISSUER_CIK, null)) c2022, count(distinct iff(year(AUDIT_REPORT_DATE)=2023, ISSUER_CIK, null)) c2023,
    count(distinct iff(year(AUDIT_REPORT_DATE)=2024, ISSUER_CIK, null)) c2024, count(distinct iff(year(AUDIT_REPORT_DATE)=2025, ISSUER_CIK, null)) c2025,
    count(distinct iff(AUDIT_REPORT_DATE >= '2024-01-01', ENGAGEMENT_PARTNER_ID, null)) partners_2024on,
    min(AUDIT_REPORT_DATE) first_report
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_PCAOB_FORM_AP_FILINGS
  where LATEST_FORM_AP_FILING='1' and AUDIT_REPORT_TYPE='Issuer, other than Employee Benefit Plan or Investment Company' and FIRM_ID in (select FIRM_ID from sel)
  group by 1
)
select l.firm, g.country, g.city, l.clients, l.exborg_clients, l.n, l.late, round(100*l.late/l.n,1) late_pct,
  l.n_nonborg, l.late_nonborg, round(100*l.late_nonborg/nullif(l.n_nonborg,0),1) late_pct_nonborg,
  g.c2022, g.c2023, g.c2024, g.c2025, g.partners_2024on, g.first_report
from lat l join grow g on g.FIRM_ID=l.FIRM_ID order by late_pct_nonborg desc
