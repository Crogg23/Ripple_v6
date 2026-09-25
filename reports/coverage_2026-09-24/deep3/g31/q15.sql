-- Fair peers: audit shops with <=5 lead partners (2024 on). Late share excluding catch-up filings (365+ days), pick window vs holdout, with per-client median
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
, parts as (select FIRM_ID, count(distinct ENGAGEMENT_PARTNER_ID) partners from ap where AUDIT_REPORT_DATE >= '2024-01-01' group by 1),
p as (select * from f where FORM in ('10-K','10-Q') and AFS='4-NON' and days <= 365),
pa as (
  select p.q, p.ADSH, p.cik, iff(p.days>p.hard_deadline,1,0) late, ap.FIRM_ID, ap.FIRM_NAME,
    iff(p.q between '2024Q2' and '2025Q2','A', iff(p.q between '2025Q3' and '2026Q1','B',null)) w
  from p join ap on ap.cik=p.cik and ap.AUDIT_REPORT_DATE <= p.fd
  qualify row_number() over (partition by p.ADSH order by ap.AUDIT_REPORT_DATE desc, ap.fpe desc)=1
),
cl as (select FIRM_ID, w, cik, avg(late) cr from pa where w is not null group by 1,2,3),
fw as (
  select pa.FIRM_ID, any_value(pa.FIRM_NAME) firm, pa.w, count(*) n, sum(late) late, avg(late) r, count(distinct cik) clients
  from pa where w is not null group by 1,3
),
cm as (select FIRM_ID, w, median(cr) med_client_rate from cl group by 1,2),
wide as (
  select a.FIRM_ID, a.firm, pt.partners, a.n n_a, a.late late_a, a.r r_a, a.clients cl_a, ca.med_client_rate mc_a, b.n n_b, b.late late_b, b.r r_b, b.clients cl_b
  from fw a join parts pt on pt.FIRM_ID=a.FIRM_ID left join fw b on b.FIRM_ID=a.FIRM_ID and b.w='B' left join cm ca on ca.FIRM_ID=a.FIRM_ID and ca.w='A'
  where a.w='A' and a.n >= 40 and pt.partners <= 5
)
select 'shop' k, firm, partners, n_a, late_a, round(100*r_a,1) pct_a, cl_a, round(100*mc_a,1) median_client_pct_a, n_b, late_b, round(100*r_b,1) pct_b
from wide where r_a >= 0.15
union all
select 'median_small_shops', count(*)::text, median(partners), median(n_a), median(late_a), round(100*median(r_a),1), median(cl_a), round(100*median(mc_a),1), median(n_b), median(late_b), round(100*median(r_b),1) from wide
order by 1 desc, 6 desc
