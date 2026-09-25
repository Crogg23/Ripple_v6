-- Re-audit rate by firm: share of a firm's company audits (fiscal periods 2022-2024) that ANOTHER firm later re-audited (same CIK, period end within 7 days, report 30+ days later). Renames merged; filers ever coded SIC 6770 excluded; issuers limited to filers active in my five quarters
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
, act as (select cik from f where q between '2024Q2' and '2025Q2' group by 1 having max(iff(SIC='6770',1,0))=0),
spacever as (select cik from f where SIC='6770' group by 1),
apx as (
  select try_to_number(ISSUER_CIK) cik, FISCAL_PERIOD_END_DATE fpe, AUDIT_REPORT_DATE rpt, FIRM_NAME,
    case when FIRM_NAME ilike any ('%marcum%','%cbiz%','%friedman llp%') then 'MARCUM'
         when FIRM_NAME ilike any ('%mazars%','%forvis%') then 'FORVIS'
         when FIRM_NAME ilike 'BDO %' then 'BDO'
         else regexp_substr(upper(FIRM_NAME),'[A-Z0-9&]+') end fk
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_PCAOB_FORM_AP_FILINGS
  where LATEST_FORM_AP_FILING='1' and try_to_number(ISSUER_CIK) is not null
    and AUDIT_REPORT_TYPE='Issuer, other than Employee Benefit Plan or Investment Company' and FISCAL_PERIOD_END_DATE >= '2022-01-01'
),
a as (select apx.* from apx join act using (cik) where cik not in (select cik from spacever)),
base as (select * from a where year(fpe) between 2022 and 2024
         qualify row_number() over (partition by cik, fk, fpe order by rpt)=1),
ra as (
  select b.fk, b.FIRM_NAME, b.cik, b.fpe, b.rpt, max(iff(a2.cik is not null,1,0)) redone
  from base b left join a a2 on a2.cik=b.cik and a2.fk<>b.fk and abs(datediff(day,a2.fpe,b.fpe))<=7 and a2.rpt > dateadd(day,30,b.rpt)
  group by 1,2,3,4,5
),
fr as (select fk, any_value(FIRM_NAME) firm, count(*) audits, count(distinct cik) clients, sum(redone) redone, round(100*avg(redone),1) pct from ra group by 1 having count(*) >= 20)
select 'firm' k, firm, audits, clients, redone, pct from fr where pct >= 5 or firm ilike '%borgers%'
union all
select 'median_firm', count(*)::text, median(audits), median(clients), median(redone), median(pct) from fr
union all
select 'all', null, count(*), count(distinct cik), sum(redone), round(100*avg(redone),1) from ra
order by 1 desc, 6 desc
