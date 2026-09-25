-- Resolve the Borgers absence: all Borgers operating clients (audit report 2023-24) traced through the SEC filing index after the 2024-05-03 bar
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
, borg as (select cik, max(AUDIT_REPORT_DATE) last_borg_report from ap where FIRM_NAME ilike '%borgers%' and AUDIT_REPORT_DATE between '2023-01-01' and '2024-12-31' group by 1),
newap as (select cik, count(*) n_new, min(FIRM_NAME) a_firm from ap where FIRM_NAME not ilike '%borgers%' and AUDIT_REPORT_DATE >= '2024-05-03' group by 1),
k_after as (
  select f.cik, f.ADSH, f.pd, f.fd, f.NAME,
    max(iff(ap.FIRM_NAME not ilike '%borgers%' and abs(datediff(day, ap.fpe, f.pd))<=7,1,0)) audited_new,
    max(iff(ap.FIRM_NAME ilike '%borgers%' and abs(datediff(day, ap.fpe, f.pd))<=7,1,0)) audited_borg
  from f left join ap on ap.cik=f.cik
  where f.FORM in ('10-K','10-K/A') and f.fd >= '2024-05-03' group by 1,2,3,4,5
),
per as (
  select b.cik, b.last_borg_report, n.n_new, n.a_firm,
    max(iff(f.cik is not null,1,0)) in_dera, max(iff(f.fd >= '2024-05-03' and f.FORM in ('10-K','10-Q','10-K/A','10-Q/A'),1,0)) periodic_after,
    max(f.fd) last_filed, max(iff(f.FORM in ('10-K','10-Q') and f.fd >= '2024-05-03' and f.days > f.hard_deadline,1,0)) late_after
  from borg b left join newap n on n.cik=b.cik left join f on f.cik=b.cik group by 1,2,3,4
),
ka as (select cik, count(*) k_n, max(audited_new) any_new, min(audited_new) all_new, max(audited_borg) any_borg_match, max(fd) last_k from k_after group by 1)
select case when p.in_dera=0 then 'a not in SEC index 2024Q1-2026Q1'
            when p.periodic_after=0 then 'b in index, no 10-K/10-Q after bar'
            when ka.cik is null then 'c 10-Q after bar, no 10-K after bar'
            when ka.all_new=1 then 'd every 10-K after bar has new-auditor Form AP'
            when ka.any_new=1 then 'e some 10-Ks after bar lack a Form AP'
            else 'f 10-K after bar, NO new-auditor Form AP' end bucket,
  count(*) clients, count_if(p.n_new is not null) with_new_formap, count_if(p.late_after=1) any_late_after,
  count_if(ka.any_borg_match=1) k_matches_borgers_formap, max(p.last_borg_report) max_borg_report_date,
  listagg(case when ka.all_new=0 or ka.cik is null then p.cik end, ',') within group (order by p.cik) ciks_sample
from per p left join ka on ka.cik=p.cik group by 1 order by 1
