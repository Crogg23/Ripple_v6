-- Auditor churn: distinct audit firms per active filer (my five quarters), audit reports dated 2023-01-01 on; Marcum and CBIZ merged into one; Borgers flagged
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
, act as (select cik, max(AFS) afs, max(NAME) name, max(STPRBA) st, max(COUNTRYBA) ctry, max(SIC) sic from f where q between '2024Q2' and '2025Q2' and FORM in ('10-K','10-Q') group by 1),
apx as (
  select try_to_number(ISSUER_CIK) cik, AUDIT_REPORT_DATE, FISCAL_PERIOD_END_DATE fpe, FIRM_NAME,
    case when FIRM_NAME ilike 'Marcum LLP%' or FIRM_NAME ilike 'CBIZ CPAs%' then 'MARCUM/CBIZ' else FIRM_ID end firm_key
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_PCAOB_FORM_AP_FILINGS
  where LATEST_FORM_AP_FILING='1' and try_to_number(ISSUER_CIK) is not null and AUDIT_REPORT_DATE >= '2023-01-01'
    and AUDIT_REPORT_TYPE='Issuer, other than Employee Benefit Plan or Investment Company'
),
c as (
  select a.cik, a.name, a.afs, a.st, a.ctry, a.sic, count(distinct x.firm_key) firms, max(iff(x.FIRM_NAME ilike '%borgers%',1,0)) had_borgers,
    listagg(distinct x.FIRM_NAME, ' > ') within group (order by x.FIRM_NAME) firm_list,
    count(distinct year(x.fpe)) fiscal_years
  from act a join apx x on x.cik=a.cik group by 1,2,3,4,5,6
)
select 'dist' k, afs, null name, null a, count(*)::text ciks, median(firms)::text median_firms, count_if(firms>=3)::text ge3, count_if(firms>=4)::text ge4, round(100*count_if(firms>=3)/count(*),1)::text pct_ge3, count_if(firms>=4 and had_borgers=0)::text ge4_no_borgers
from c group by 2
union all
select 'churn', afs, name, st || ' ' || ctry || ' sic ' || sic, firms::text, fiscal_years::text, had_borgers::text, firm_list, null, null
from c where firms >= 4
order by 1 desc, 5 desc
