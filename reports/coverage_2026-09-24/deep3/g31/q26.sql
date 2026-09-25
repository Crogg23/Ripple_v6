-- Filed-before-audit across all nine quarters (all Form AP versions): rate per quarter, and same-firm vs new-firm (prior fiscal year's auditor)
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
, apv as (select try_to_number(ISSUER_CIK) cik, FISCAL_PERIOD_END_DATE fpe, FIRM_ID, FIRM_NAME, AUDIT_REPORT_DATE from LIBRARY_MARTS.FINANCE.FINANCE__FED_PCAOB_FORM_AP_FILINGS where try_to_number(ISSUER_CIK) is not null),
k as (select * from f where FORM='10-K'),
m as (
  select k.q, k.ADSH, k.cik, k.NAME, k.AFS, k.pd, k.fd, min(apv.AUDIT_REPORT_DATE) rpt,
    min_by(apv.FIRM_ID, apv.AUDIT_REPORT_DATE) rpt_firm_id, min_by(apv.FIRM_NAME, apv.AUDIT_REPORT_DATE) rpt_firm
  from k join apv on apv.cik=k.cik and abs(datediff(day, apv.fpe, k.pd))<=7 group by 1,2,3,4,5,6,7
),
prior as (
  select m.ADSH, listagg(distinct apv.FIRM_ID, ',') prior_firm_ids, listagg(distinct apv.FIRM_NAME, ' / ') prior_firms
  from m join apv on apv.cik=m.cik and abs(datediff(day, apv.fpe, dateadd(year,-1,m.pd)))<=30 group by 1
),
x as (select m.*, p.prior_firms, iff(p.prior_firm_ids is null, 'no prior on file', iff(contains(p.prior_firm_ids, m.rpt_firm_id), 'same firm', 'new firm')) firm_change,
        iff(m.rpt > dateadd(day,3,m.fd),1,0) before_audit, datediff(day, m.fd, m.rpt) gap from m left join prior p on p.ADSH=m.ADSH)
select 'qtr' k, q, count(*)::text matched_10k, sum(before_audit)::text filed_before_audit, round(100*avg(before_audit),2)::text pct,
  count_if(before_audit=1 and firm_change='same firm')::text same_firm, count_if(before_audit=1 and firm_change='new firm')::text new_firm, count_if(before_audit=1 and firm_change='no prior on file')::text no_prior, null g
from x group by 2
union all
select 'row', q, NAME, AFS, fd::text, rpt::text, gap::text, rpt_firm || '  <=prior: ' || coalesce(prior_firms,'-'), firm_change
from x where before_audit=1 and q not between '2024Q2' and '2025Q2'
order by 1 desc, 2
