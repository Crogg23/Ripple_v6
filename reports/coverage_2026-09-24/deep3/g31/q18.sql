-- Size the blank-CIK trap in Form AP: operating-company audits (report 2023+) with no usable CIK, name-matched to SEC index filers where fiscal year-end MMDD also agrees; then re-score Borgers clients
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
, nrm as (
  select distinct try_to_number(CIK) cik, FYE,
    regexp_replace(replace(replace(replace(replace(upper(NAME),'INCORPORATED','INC'),'CORPORATION','CORP'),'COMPANY','CO'),'LIMITED','LTD'),'[^A-Z0-9]','') nm
  from u
),
apall as (
  select try_to_number(ISSUER_CIK) cik, ISSUER_CIK_NONE, FIRM_NAME, FISCAL_PERIOD_END_DATE fpe, AUDIT_REPORT_DATE,
    regexp_replace(replace(replace(replace(replace(upper(ISSUER_NAME),'INCORPORATED','INC'),'CORPORATION','CORP'),'COMPANY','CO'),'LIMITED','LTD'),'[^A-Z0-9]','') nm
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_PCAOB_FORM_AP_FILINGS
  where LATEST_FORM_AP_FILING='1' and AUDIT_REPORT_TYPE='Issuer, other than Employee Benefit Plan or Investment Company' and AUDIT_REPORT_DATE >= '2023-01-01'
),
nocik as (select * from apall where cik is null),
hit as (select nc.*, n.cik matched_cik from nocik nc join nrm n on n.nm = nc.nm and n.FYE = to_char(nc.fpe,'MMDD')),
borg as (select cik from apall where FIRM_NAME ilike '%borgers%' and cik is not null group by 1),
newap as (
  select cik from apall where FIRM_NAME not ilike '%borgers%' and AUDIT_REPORT_DATE >= '2024-05-03' and cik is not null
  union select matched_cik from hit where FIRM_NAME not ilike '%borgers%' and AUDIT_REPORT_DATE >= '2024-05-03'
),
newap_cikonly as (select cik from apall where FIRM_NAME not ilike '%borgers%' and AUDIT_REPORT_DATE >= '2024-05-03' and cik is not null group by 1)
select 'total' k, null firm, (select count(*) from apall) rows_2023on, count(*) nocik_rows, count(distinct nm) nocik_names,
  (select count(*) from hit) matched_rows, (select count(distinct matched_cik) from hit) matched_ciks,
  (select count(*) from borg) borg_clients,
  (select count(*) from borg b where b.cik not in (select cik from newap_cikonly)) borg_no_new_by_cik,
  (select count(*) from borg b where b.cik not in (select cik from newap)) borg_no_new_by_cik_or_name
from nocik
union all
select 'firm', FIRM_NAME, null, count(*), count(distinct nm), count(distinct iff(matched_cik is not null, nm, null)), null, null, null, null
from (select nc.FIRM_NAME, nc.nm, h.matched_cik from nocik nc left join (select distinct nm, FIRM_NAME, matched_cik from hit) h on h.nm=nc.nm and h.FIRM_NAME=nc.FIRM_NAME)
group by 2 having count(distinct iff(matched_cik is not null, nm, null)) >= 2
order by 1 desc, 6 desc nulls last
