-- Borgers clients vs peers: after the May 2024 bar, who kept filing 10-K/10-Q in the SEC index; SPACs (6770) out
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
, t as (
  select b.cik, b.name, b.afs, lp.FIRM_NAME, lp.FIRM_ID, fs.firm_clients,
    case when lp.FIRM_NAME ilike '%borgers%' then '1 Borgers'
         when lp.FIRM_ID is null then '4 no pre-bar Form AP'
         when b.afs='4-NON' and fs.firm_clients between 20 and 300 then '2 other small shops (20-300 clients), NON filers'
         when b.afs='4-NON' then '3 other NON filers' else '5 accelerated' end grp,
    coalesce(a.still_filing,0) still_filing, coalesce(a.any_after_q2,0) any_after, coalesce(a.k_2025on,0) k_2025on, coalesce(a.per_n,0) per_n, coalesce(a.per_late,0) per_late
  from base b left join lastpre lp on lp.cik=b.cik left join fsize fs on fs.FIRM_ID=lp.FIRM_ID left join after a on a.cik=b.cik
  where coalesce(b.sic,'') <> '6770'
)
select 'group' kind, grp, null firm, count(*) ciks, sum(any_after) any_after_q2, sum(still_filing) still_filing_2025q3on,
  round(100*(1-avg(still_filing)),1) gone_pct, sum(k_2025on) k_2025on, sum(per_late) late_filings, sum(per_n) filings,
  round(100*sum(per_late)/nullif(sum(per_n),0),1) late_pct
from t group by 1,2,3
union all
select 'firm', null, FIRM_NAME, count(*), sum(any_after), sum(still_filing), round(100*(1-avg(still_filing)),1), sum(k_2025on), sum(per_late), sum(per_n),
  round(100*sum(per_late)/nullif(sum(per_n),0),1)
from t where afs='4-NON' and FIRM_ID is not null group by 1,2,3 having count(*) >= 12
order by 1 desc, 2, 7 desc
