-- Catch-up filers: 10-K/10-Q filed 365+ days after period end in my five quarters; auditor on file for that period (10-K: fpe within 7 days; any: latest report before filing)
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
, s as (select * from f where FORM in ('10-K','10-Q') and days > 365 and q between '2024Q2' and '2025Q2'),
sa as (
  select s.cik, s.ADSH, s.FORM, s.pd, s.fd, s.days,
    max(iff(s.FORM='10-K' and abs(datediff(day, ap.fpe, s.pd))<=7, ap.FIRM_NAME, null)) k_auditor,
    max(iff(ap.AUDIT_REPORT_DATE <= s.fd, ap.AUDIT_REPORT_DATE, null)) last_report_before
  from s left join ap on ap.cik=s.cik group by 1,2,3,4,5,6
),
lastfirm as (select cik, FIRM_NAME, AUDIT_REPORT_DATE from ap qualify row_number() over (partition by cik order by AUDIT_REPORT_DATE desc)=1),
later as (select cik, max(fd) last_filing_any from f group by 1)
select sa.cik, any_value(f.NAME) name, any_value(f.STPRBA) st, any_value(f.SIC) sic, count(*) stale_filings, count_if(sa.FORM='10-K') stale_10k,
  min(sa.pd) oldest_period, max(sa.days) max_days, min(sa.fd) first_catchup, max(sa.fd) last_catchup,
  count_if(sa.FORM='10-K' and sa.k_auditor is null) k_no_audit_on_file, listagg(distinct sa.k_auditor, ' / ') k_auditors,
  max(sa.last_report_before) last_audit_before, any_value(lf.FIRM_NAME) latest_firm_ever, any_value(l.last_filing_any) last_filing_any
from sa join f on f.ADSH=sa.ADSH left join lastfirm lf on lf.cik=sa.cik left join later l on l.cik=sa.cik
group by 1 order by stale_filings desc, max_days desc
