-- deep3 / g31: proper look at five SEC filing-index tables, 2026-09-24
-- Tables: FINANCE__FED_SEC_DERA_SUB_2024Q2, _2024Q3, _2024Q4, _2025Q1, _2025Q2
--   (the other four quarters, 2024Q1 and 2025Q3-2026Q1, are read only as time context)
-- Door: Python (connect/db.py) via g31/run.py. Every connection first ran:
--   ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300;
--   ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24';
-- Read-only: the runner refuses anything that is not SELECT / WITH. Raw results in g31/<label>.json.
-- Statement numbers below count only SELECT/WITH statements against the 35 budget.

-- [q01] statement 1
-- Profile all nine quarters: keys, dupes, EIN filler, forms, filer size, dates outside the quarter
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
), x as (select q, ADSH, count(*) over (partition by q, ADSH) dup_in_q, count(distinct q) over (partition by ADSH) nq from u)
select u.q, count(*) n, count(distinct u.ADSH) adsh, count(distinct CIK) cik,
  count_if(EIN='000000000') ein_zero, count_if(EIN is null or trim(EIN)='') ein_blank,
  count_if(PREVRPT='1') prevrpt1, count_if(DETAIL='1') detail1,
  count_if(FORM='10-K') k, count_if(FORM='10-Q') q10, count_if(FORM='10-K/A') ka, count_if(FORM='10-Q/A') qa,
  count_if(FORM in ('20-F','40-F','20-F/A','40-F/A')) foreign_annual, count_if(FORM not in ('10-K','10-Q','10-K/A','10-Q/A','20-F','40-F','20-F/A','40-F/A')) other_form,
  listagg(distinct AFS, '|') afs_vals,
  min(try_to_date(FILED,'YYYYMMDD')) filed_min, max(try_to_date(FILED,'YYYYMMDD')) filed_max,
  count_if(try_to_date(FILED,'YYYYMMDD') is null) filed_bad, count_if(try_to_date(PERIOD,'YYYYMMDD') is null) period_bad,
  max(x.dup_in_q) max_adsh_dup_in_q, count_if(x.nq>1) rows_adsh_in_2plus_q,
  count_if(try_to_number(NCIKS)>1) multi_cik
from u join (select distinct q, ADSH, dup_in_q, nq from x) x on x.q=u.q and x.ADSH=u.ADSH
group by 1 order by 1;

-- [q02] statement 2
-- Lateness by quarter and form: days from period end to filing vs SEC deadline + extension + 3 weekend days
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
select q, FORM, count(*) n,
  count_if(AFS='4-NON') non_acc,
  count_if(days > hard_deadline) late,
  round(100*count_if(days > hard_deadline)/count(*),1) late_pct,
  count_if(days > hard_deadline + 90) late_90plus,
  count_if(days > 365) over_1yr,
  count_if(days < 0) negative_days,
  median(days) med_days,
  count_if(fd = '2024-04-01') filed_apr1_2024,
  count_if(fd between '2024-04-02' and '2024-04-16') filed_apr2_16_2024,
  count_if(fd between '2025-04-01' and '2025-04-15') filed_apr1_15_2025
from f where FORM in ('10-K','10-Q') group by 1,2 order by 2,1;

-- [q03] statement 3
-- Peer check: late share among NON-accelerated 10-K/10-Q filers only, my five quarters, by business-address country
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
select coalesce(COUNTRYBA,'(blank)') country, count(*) n, count(distinct cik) ciks,
  count_if(days > hard_deadline) late, round(100*count_if(days > hard_deadline)/count(*),1) late_pct,
  count_if(days > hard_deadline + 90) late_90plus, round(100*count_if(days > hard_deadline+90)/count(*),1) late90_pct,
  count(distinct case when days > hard_deadline then cik end) late_ciks
from f where FORM in ('10-K','10-Q') and AFS='4-NON' and q between '2024Q2' and '2025Q2'
group by 1 having count(*) >= 60 order by n desc;

-- [q04] statement 4
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
order by 1,2,3;

-- [q05] statement 5
-- 10-Ks in my five quarters with NO Form AP (any firm) within 7 days of their fiscal period end: who, and who audited them last
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
  select try_to_number(ISSUER_CIK) cik, FISCAL_PERIOD_END_DATE fpe, FIRM_NAME, ENGAGEMENT_PARTNER_ID, AUDIT_REPORT_DATE, AUDIT_REPORT_TYPE
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_PCAOB_FORM_AP_FILINGS where LATEST_FORM_AP_FILING='1' and try_to_number(ISSUER_CIK) is not null
), k as (select * from f where FORM='10-K' and q between '2024Q2' and '2025Q2'),
nomatch as (
  select k.* from k where not exists (select 1 from ap where ap.cik=k.cik and abs(datediff(day, ap.fpe, k.pd))<=7)
), lastap as (
  select cik, FIRM_NAME, fpe, AUDIT_REPORT_DATE, AUDIT_REPORT_TYPE, row_number() over (partition by cik order by fpe desc, AUDIT_REPORT_DATE desc) rn,
    count(*) over (partition by cik) n_ap from ap
)
select n.q, n.cik, n.NAME, n.AFS, n.SIC, n.COUNTRYBA, n.STPRBA, n.pd, n.fd, n.days, n.days > n.hard_deadline late,
  l.FIRM_NAME last_firm, l.fpe last_fpe, l.AUDIT_REPORT_DATE last_report, l.n_ap, l.AUDIT_REPORT_TYPE
from nomatch n left join lastap l on l.cik=n.cik and l.rn=1
order by l.FIRM_NAME nulls first, n.q;

-- [q06] statement 6
-- (rewrite of q05 without correlated subquery) 10-Ks in my five quarters with NO Form AP within 7 days of period end, plus last auditor
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
  select try_to_number(ISSUER_CIK) cik, FISCAL_PERIOD_END_DATE fpe, FIRM_NAME, ENGAGEMENT_PARTNER_ID, AUDIT_REPORT_DATE, AUDIT_REPORT_TYPE
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_PCAOB_FORM_AP_FILINGS where LATEST_FORM_AP_FILING='1' and try_to_number(ISSUER_CIK) is not null
), k as (select * from f where FORM='10-K' and q between '2024Q2' and '2025Q2'),
km as (select k.ADSH, max(iff(abs(datediff(day, ap.fpe, k.pd))<=7,1,0)) hit from k left join ap on ap.cik=k.cik group by 1),
nomatch as (select k.* from k join km on km.ADSH=k.ADSH where km.hit=0),
lastap as (
  select cik, FIRM_NAME, fpe, AUDIT_REPORT_DATE, AUDIT_REPORT_TYPE, row_number() over (partition by cik order by fpe desc, AUDIT_REPORT_DATE desc) rn,
    count(*) over (partition by cik) n_ap from ap
)
select n.q, n.cik, n.NAME, n.AFS, n.SIC, n.COUNTRYBA, n.STPRBA, n.pd, n.fd, n.days, n.days > n.hard_deadline late,
  l.FIRM_NAME last_firm, l.fpe last_fpe, l.AUDIT_REPORT_DATE last_report, l.n_ap, l.AUDIT_REPORT_TYPE
from nomatch n left join lastap l on l.cik=n.cik and l.rn=1
order by l.FIRM_NAME nulls first, n.q;

-- [q07] statement 7
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
order by 1 desc, 2, 7 desc;

-- [q08] statement 8
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
from per p left join ka on ka.cik=p.cik group by 1 order by 1;

-- [q09] statement 9
-- Eyeball: the 10 ex-Borgers companies whose post-bar 10-Ks have no new-auditor Form AP within 7 days: every such 10-K and every Form AP on file for them
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
, ten as (select column1 cik from values (1318268),(1342936),(1467761),(1514443),(1657045),(1688126),(894501),(1444839),(1627469),(1685766)),
ks as (select f.q, f.cik, f.NAME, f.FORM, f.pd, f.fd, f.days, f.AFS, f.STPRBA, f.SIC from f join ten using (cik) where f.FORM in ('10-K','10-K/A') and f.fd >= '2024-05-03'),
aps as (select ap.cik, listagg(ap.FIRM_NAME || ' fpe ' || ap.fpe || ' rpt ' || ap.AUDIT_REPORT_DATE || ' p ' || ap.ENGAGEMENT_PARTNER_ID, ' ; ') within group (order by ap.fpe) all_ap from ap join ten using (cik) where ap.fpe >= '2022-01-01' group by 1)
select ks.*, aps.all_ap from ks left join aps using (cik) order by ks.cik, ks.fd;

-- [q10] statement 10
-- Peer ranking: late share of NON-accelerated 10-K/10-Q filings (my five quarters) by the auditor on file at filing time (latest Form AP report dated on/before the filing)
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
, p as (select * from f where FORM in ('10-K','10-Q') and AFS='4-NON' and q between '2024Q2' and '2025Q2'),
pa as (
  select p.ADSH, p.cik, p.days, p.hard_deadline, ap.FIRM_ID, ap.FIRM_NAME
  from p join ap on ap.cik=p.cik and ap.AUDIT_REPORT_DATE <= p.fd
  qualify row_number() over (partition by p.ADSH order by ap.AUDIT_REPORT_DATE desc, ap.fpe desc)=1
),
cl as (select FIRM_ID, cik, count(*) n, count_if(days>hard_deadline) late from pa group by 1,2),
fm as (
  select pa.FIRM_ID, any_value(pa.FIRM_NAME) firm, count(*) filings, count(distinct pa.cik) clients, count_if(days>hard_deadline) late,
    round(100*count_if(days>hard_deadline)/count(*),1) late_pct, count(distinct iff(days>hard_deadline, pa.cik, null)) late_clients,
    count_if(days>hard_deadline+90) late90
  from pa group by 1 having count(*) >= 40
),
top3 as (select FIRM_ID, sum(late) top3_late from (select FIRM_ID, late, row_number() over (partition by FIRM_ID order by late desc) r from cl) where r<=3 group by 1)
select 'firm' k, fm.firm, fm.filings, fm.clients, fm.late, fm.late_pct, fm.late_clients, fm.late90, t.top3_late,
  (select count(*) from p) all_non_filings, (select count(*) from pa) with_auditor
from fm left join top3 t on t.FIRM_ID=fm.FIRM_ID
union all
select 'median_of_firms', null, count(*), median(clients), median(late), median(late_pct), median(late_clients), null, null, null, null from fm
order by 1 desc, 6 desc;

-- [q11] statement 11
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
from lat l join grow g on g.FIRM_ID=l.FIRM_ID order by late_pct_nonborg desc;

-- [q12] statement 12
-- Holdout: firms picked on 2024Q2-2025Q2 (late>=20%, 40+ filings) scored on 2025Q3-2026Q1, vs median firm in the holdout window
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
, p as (select * from f where FORM in ('10-K','10-Q') and AFS='4-NON'),
pa as (
  select p.q, p.ADSH, p.cik, p.days, p.hard_deadline, iff(p.days>p.hard_deadline,1,0) late, ap.FIRM_ID, ap.FIRM_NAME
  from p join ap on ap.cik=p.cik and ap.AUDIT_REPORT_DATE <= p.fd
  qualify row_number() over (partition by p.ADSH order by ap.AUDIT_REPORT_DATE desc, ap.fpe desc)=1
),
a as (select FIRM_ID, count(*) n, avg(late) r from pa where q between '2024Q2' and '2025Q2' group by 1),
b as (select FIRM_ID, any_value(FIRM_NAME) firm, count(*) n, sum(late) late, avg(late) r, count(distinct cik) clients, count(distinct iff(late=1,cik,null)) late_clients
      from pa where q between '2025Q3' and '2026Q1' group by 1)
select 'picked' k, b.firm, round(100*a.r,1) pick_window_pct, b.n holdout_n, b.clients, b.late, round(100*b.r,1) holdout_pct, b.late_clients
from a join b on a.FIRM_ID=b.FIRM_ID where a.n>=40 and a.r>=0.2
union all
select 'median_all_firms_holdout_30plus', null, null, count(*), median(clients), median(late), round(100*median(r),1), null from b where n>=30
union all
select 'all_filings_holdout', null, null, count(*), null, sum(late), round(100*avg(late),1), null from pa where q between '2025Q3' and '2026Q1'
order by 1 desc, 7 desc;

-- [q13] statement 13
-- Shared business addresses: street line + ZIP5 held by 5+ distinct filers across my five quarters, split by SIC family
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
, m as (select * from f where q between '2024Q2' and '2025Q2' and a1 is not null and a1 <> '')
select a1, zip, any_value(CITYBA) city, any_value(STPRBA) st, any_value(COUNTRYBA) ctry,
  count(distinct cik) ciks, count(distinct iff(SIC='6770',cik,null)) spac, count(distinct iff(left(SIC,2)='67' and SIC<>'6770',cik,null)) funds_67,
  count(distinct iff(SIC in ('6189','6221'),cik,null)) abs_pools, count(distinct iff(SIC is null or SIC='',cik,null)) nosic,
  count(distinct iff(left(coalesce(SIC,'00'),2) not in ('67') and coalesce(SIC,'') not in ('6189','6221',''),cik,null)) operating,
  count(distinct ph) phones, count(distinct iff(AFS='4-NON',cik,null)) non_acc,
  listagg(distinct left(NAME,28), ' | ') within group (order by left(NAME,28)) names
from m group by 1,2 having count(distinct cik) >= 5 order by operating desc, ciks desc limit 40;

-- [q14] statement 14
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
group by 1 order by stale_filings desc, max_days desc;

-- [q15] statement 15
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
order by 1 desc, 6 desc;

-- [q16] statement 16
-- Ex-Borgers clients still filing after the bar: 10-Qs vs 10-Ks after 2024-05-03, newest audit on file, ticker/exchange
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
, borg as (select cik from ap where FIRM_NAME ilike '%borgers%' and AUDIT_REPORT_DATE between '2023-01-01' and '2024-12-31' group by 1),
aft as (
  select f.cik, any_value(f.NAME) name, any_value(f.STPRBA) st,
    count_if(FORM in ('10-Q','10-Q/A')) q_n, count_if(FORM in ('10-K','10-K/A')) k_n,
    max(iff(FORM='10-Q', pd, null)) last_q_period, max(iff(FORM='10-Q', fd, null)) last_q_filed, max(iff(FORM like '10-K%', pd, null)) last_k_period
  from f join borg using (cik) where f.fd >= '2024-05-03' and FORM in ('10-K','10-Q','10-K/A','10-Q/A') group by 1
),
newest as (select cik, FIRM_NAME newest_firm, fpe newest_fpe, AUDIT_REPORT_DATE newest_report from ap qualify row_number() over (partition by cik order by fpe desc, AUDIT_REPORT_DATE desc)=1),
tk as (select CIK cik, listagg(distinct TICKER, '/') tickers, listagg(distinct EXCHANGE, '/') exch from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_EDGAR_COMPANY_TICKERS_EXCHANGE group by 1)
select a.*, n.newest_firm, n.newest_fpe, n.newest_report, tk.tickers, tk.exch
from aft a left join newest n on n.cik=a.cik left join tk on tk.cik=a.cik
where n.newest_firm ilike '%borgers%' or a.k_n = 0 or n.newest_fpe < dateadd(day, -400, a.last_q_period)
order by a.k_n, a.last_q_filed desc;

-- [q17] statement 17
-- Miss test: search Form AP by ISSUER NAME (any CIK, any row version) for the no-audit-on-file companies, in case the audit sits under a wrong or blank CIK
with names as (select column1 k, column2 pat from values
  ('GOLD ROCK','%GOLD ROCK HOLD%'),('BRAVO','%BRAVO MULTI%'),('PHOTOZOU','%PHOTOZOU%'),('MIDNIGHT','%MIDNIGHT GAMING%'),
  ('FRANKSPEECH','%FRANKSPEECH%'),('INTERNET SCI','%INTERNET SCIENCES%'),('GEX','%GEX MANAGEMENT%'),('PHI','PHI GROUP%'),
  ('MCX','%MCX TECH%'),('COLLECTIVE','%COLLECTIVE AUDIENCE%'),('RESONATE','%RESONATE BLENDS%'),('DOGECOIN','%DOGECOIN CASH%'),
  ('AMERICANN','%AMERICANN%'),('FCCC','FCCC%'),('INNOVATIVE DESIGNS','%INNOVATIVE DESIGNS%'),('NFINITI','%NFINITI%'),
  ('IRONSTONE','%IRONSTONE PROP%'),('SCANTECH','%SCANTECH%'),('MOVEIX','%MOVEIX%'),('NEXT-CHEMX','%NEXT%CHEMX%'),('MADISON TECH','%MADISON TECHNOLOGIES%'),
  ('CAN B','CAN B%'),('VNUE','VNUE%'))
select n.k, a.ISSUER_NAME, a.ISSUER_CIK, a.ISSUER_CIK_NONE, a.FIRM_NAME, a.FISCAL_PERIOD_END_DATE, a.AUDIT_REPORT_DATE, a.LATEST_FORM_AP_FILING, a.IS_MULTIPLE_AUDIT_PERIOD, a.AUDIT_PERIOD_INFORMATION
from names n left join LIBRARY_MARTS.FINANCE.FINANCE__FED_PCAOB_FORM_AP_FILINGS a on upper(a.ISSUER_NAME) like n.pat and a.FISCAL_PERIOD_END_DATE >= '2023-06-01'
order by n.k, a.FISCAL_PERIOD_END_DATE;

-- [q18] statement 18
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
order by 1 desc, 6 desc nulls last;

-- [q19] statement 19
-- 10-Ks (my five quarters) whose matching audit reports (same CIK, fiscal period end within 7 days) are ALL dated after the 10-K was filed
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
  select try_to_number(ISSUER_CIK) cik, FISCAL_PERIOD_END_DATE fpe, FIRM_NAME, AUDIT_REPORT_DATE, DUAL_DATED, AUDIT_DUAL_DATE, IS_MULTIPLE_AUDIT_PERIOD
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_PCAOB_FORM_AP_FILINGS
  where LATEST_FORM_AP_FILING='1' and try_to_number(ISSUER_CIK) is not null
), k as (select * from f where FORM='10-K' and q between '2024Q2' and '2025Q2'),
m as (
  select k.q, k.cik, k.NAME, k.AFS, k.STPRBA, k.pd, k.fd, k.days,
    count(*) n_ap, min(ap.AUDIT_REPORT_DATE) first_report, max(ap.AUDIT_REPORT_DATE) last_report,
    listagg(distinct ap.FIRM_NAME, ' / ') firms, max(ap.DUAL_DATED) dual
  from k join ap on ap.cik=k.cik and abs(datediff(day, ap.fpe, k.pd))<=7
  group by 1,2,3,4,5,6,7,8
),
kk as (select cik, pd, count(*) n_k, listagg(fd::text, ',') within group (order by fd) k_filed_dates from f where FORM in ('10-K','10-K/A') group by 1,2)
select 'summary' k, null q, count(*)::text n_10k_matched, count_if(first_report > fd)::text report_after_filing,
  count_if(first_report > dateadd(day, 3, fd))::text report_4plus_days_after, count_if(first_report > dateadd(day, 30, fd))::text report_31plus_days_after,
  null a, null b, null c, null d, null e
from m
union all
select 'row', m.q, m.NAME, m.AFS, m.fd::text, m.first_report::text, datediff(day, m.fd, m.first_report)::text, m.firms, m.pd::text, kk.k_filed_dates, m.dual
from m left join kk on kk.cik=m.cik and kk.pd=m.pd
where m.first_report > dateadd(day, 3, m.fd)
order by 1 desc, 7 desc;

-- [q20] statement 20
-- Rule out the version filter: recompute filed-before-audit 10-Ks using EVERY Form AP version (latest or not); add ticker/exchange
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
, apv as (
  select try_to_number(ISSUER_CIK) cik, FISCAL_PERIOD_END_DATE fpe, FIRM_NAME, AUDIT_REPORT_DATE, LATEST_FORM_AP_FILING, AMENDMENT_PREVIOUS_FILING
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_PCAOB_FORM_AP_FILINGS where try_to_number(ISSUER_CIK) is not null
), k as (select * from f where FORM='10-K' and q between '2024Q2' and '2025Q2'),
m as (
  select k.q, k.cik, k.NAME, k.AFS, k.pd, k.fd,
    count(*) ap_versions, min(apv.AUDIT_REPORT_DATE) earliest_any_version, max(apv.AUDIT_REPORT_DATE) latest_report,
    listagg(distinct apv.FIRM_NAME, ' / ') firms,
    listagg(apv.LATEST_FORM_AP_FILING || ':' || apv.AUDIT_REPORT_DATE || ':' || coalesce(apv.AMENDMENT_PREVIOUS_FILING,''), ' ; ') versions
  from k join apv on apv.cik=k.cik and abs(datediff(day, apv.fpe, k.pd))<=7 group by 1,2,3,4,5,6
),
ka as (select cik, pd, listagg(FORM || ' ' || fd::text, ', ') within group (order by fd) later_filings from f where FORM in ('10-K','10-K/A') group by 1,2),
tk as (select CIK cik, listagg(distinct TICKER, '/') tickers, listagg(distinct EXCHANGE, '/') exch from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_EDGAR_COMPANY_TICKERS_EXCHANGE group by 1)
select m.cik, m.NAME, m.AFS, m.pd, m.fd k_filed, m.earliest_any_version, datediff(day, m.fd, m.earliest_any_version) gap_days, m.ap_versions, m.firms, m.versions, ka.later_filings, tk.tickers, tk.exch
from m left join ka on ka.cik=m.cik and ka.pd=m.pd left join tk on tk.cik=m.cik
where m.earliest_any_version > dateadd(day, 3, m.fd)
order by gap_days desc;

-- [q21] statement 21
-- Late share by exchange (ticker table), and chronic late filers (3+ late 10-K/10-Q in my five quarters) listed on Nasdaq/NYSE
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
, tk as (select CIK cik, listagg(distinct TICKER, '/') tickers, max(EXCHANGE) exch from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_EDGAR_COMPANY_TICKERS_EXCHANGE group by 1),
p as (select f.*, coalesce(tk.exch,'(no ticker)') exch, tk.tickers from f left join tk on tk.cik=f.cik
      where FORM in ('10-K','10-Q') and q between '2024Q2' and '2025Q2'),
c as (select cik, any_value(NAME) name, any_value(exch) exch, any_value(tickers) tickers, any_value(STPRBA) st, any_value(COUNTRYBA) ctry, max(AFS) afs,
        count(*) n, count_if(days>hard_deadline) late, max(days - hard_deadline) worst_days_over, listagg(iff(days>hard_deadline, q, null), ',') within group (order by q) late_qs
      from p group by 1)
select 'exch' k, exch, null, null, null, null, count(*) filings, count_if(days>hard_deadline) late, round(100*count_if(days>hard_deadline)/count(*),1) late_pct,
  count(distinct cik) ciks, null
from p where AFS='4-NON' group by 2
union all
select 'chronic', exch, name, tickers, afs, st || ' ' || ctry, n, late, round(100*late/n,1), worst_days_over, late_qs
from c where late >= 3 and exch in ('Nasdaq','NYSE')
order by 1 desc, 8 desc, 9 desc;

-- [q22] statement 22
-- Rename waves: latest name change per filer (FORMER/CHANGED, all nine quarters), by quarter of change, split by buzzword in the NEW name and not in the old one
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
),
r as (
  select try_to_number(CIK) cik, NAME, FORMER, try_to_date(CHANGED,'YYYYMMDD') chg, AFS, SIC, COUNTRYBA
  from u where FORMER is not null and trim(FORMER)<>''
  qualify row_number() over (partition by try_to_number(CIK), try_to_date(CHANGED,'YYYYMMDD') order by q desc)=1
),
t as (
  select *, 
    iff(regexp_like(upper(NAME), '.*(\bAI\b|\.AI\b|ARTIFICIAL INTELLIGENCE).*') and not regexp_like(upper(FORMER), '.*(\bAI\b|\.AI\b|ARTIFICIAL INTELLIGENCE).*'),1,0) to_ai,
    iff(regexp_like(upper(NAME), '.*(BITCOIN|\bBTC\b|CRYPTO|BLOCKCHAIN|DIGITAL ASSET|TOKEN|ETHEREUM|\bETH\b|SOLANA|\bSOL\b|DOGE|\bXRP\b|TREASURY).*') and not regexp_like(upper(FORMER), '.*(BITCOIN|\bBTC\b|CRYPTO|BLOCKCHAIN|DIGITAL ASSET|TOKEN|ETHEREUM|\bETH\b|SOLANA|\bSOL\b|DOGE|\bXRP\b|TREASURY).*'),1,0) to_crypto,
    iff(regexp_like(upper(NAME), '.*QUANTUM.*') and not regexp_like(upper(FORMER), '.*QUANTUM.*'),1,0) to_quantum
  from r where chg >= '2022-01-01'
)
select 'qtr' k, year(chg)||'Q'||quarter(chg) qtr, count(*) renames, sum(to_ai) to_ai, sum(to_crypto) to_crypto, sum(to_quantum) to_quantum,
  count_if(AFS='4-NON') non_acc, null a, null b
from t group by 2
union all
select 'name', year(chg)||'Q'||quarter(chg), NAME, iff(to_ai=1,'AI',iff(to_crypto=1,'CRYPTO','QUANTUM')), FORMER, AFS, SIC, COUNTRYBA, cik::text
from t where (to_ai+to_crypto+to_quantum)>0 and chg >= '2024-04-01'
order by 1 desc, 2, 4;

-- [q23] statement 23
-- (re-run of q22 with text casts) Rename waves: latest name change per filer (FORMER/CHANGED, all nine quarters), by quarter of change, split by buzzword in the NEW name and not in the old one
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
),
r as (
  select try_to_number(CIK) cik, NAME, FORMER, try_to_date(CHANGED,'YYYYMMDD') chg, AFS, SIC, COUNTRYBA
  from u where FORMER is not null and trim(FORMER)<>''
  qualify row_number() over (partition by try_to_number(CIK), try_to_date(CHANGED,'YYYYMMDD') order by q desc)=1
),
t as (
  select *, 
    iff(regexp_like(upper(NAME), '.*(\bAI\b|\.AI\b|ARTIFICIAL INTELLIGENCE).*') and not regexp_like(upper(FORMER), '.*(\bAI\b|\.AI\b|ARTIFICIAL INTELLIGENCE).*'),1,0) to_ai,
    iff(regexp_like(upper(NAME), '.*(BITCOIN|\bBTC\b|CRYPTO|BLOCKCHAIN|DIGITAL ASSET|TOKEN|ETHEREUM|\bETH\b|SOLANA|\bSOL\b|DOGE|\bXRP\b|TREASURY).*') and not regexp_like(upper(FORMER), '.*(BITCOIN|\bBTC\b|CRYPTO|BLOCKCHAIN|DIGITAL ASSET|TOKEN|ETHEREUM|\bETH\b|SOLANA|\bSOL\b|DOGE|\bXRP\b|TREASURY).*'),1,0) to_crypto,
    iff(regexp_like(upper(NAME), '.*QUANTUM.*') and not regexp_like(upper(FORMER), '.*QUANTUM.*'),1,0) to_quantum
  from r where chg >= '2022-01-01'
)
select 'qtr' k, year(chg)||'Q'||quarter(chg) qtr, count(*)::text renames, sum(to_ai)::text to_ai, sum(to_crypto)::text to_crypto, sum(to_quantum)::text to_quantum,
  count_if(AFS='4-NON')::text non_acc, null a, null b
from t group by 2
union all
select 'name', year(chg)||'Q'||quarter(chg), NAME, iff(to_ai=1,'AI',iff(to_crypto=1,'CRYPTO','QUANTUM')), FORMER, AFS, SIC, COUNTRYBA, cik::text
from t where (to_ai+to_crypto+to_quantum)>0 and chg >= '2024-04-01'
order by 1 desc, 2, 4;

-- [q24] statement 24
-- PREVRPT trap: originals that the index itself shows were later amended (same CIK + period, a /A filed later), and how many carry PREVRPT=1; plus EIN width check
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
),
o as (select q, ADSH, CIK, PERIOD, FORM, PREVRPT, FILED, EIN from u where FORM in ('10-K','10-Q')),
a as (select CIK, PERIOD, replace(FORM,'/A','') base, min(FILED) first_amend from u where FORM in ('10-K/A','10-Q/A') group by 1,2,3)
select o.q, count(*) originals, count_if(o.PREVRPT='1') prevrpt1,
  count_if(a.CIK is not null and a.first_amend >= o.FILED) amended_later_in_index,
  count_if(a.CIK is not null and a.first_amend >= o.FILED and o.PREVRPT='1') amended_and_flagged,
  count_if(length(o.EIN) <> 9) ein_not_9, count_if(o.EIN = '000000000') ein_zero
from o left join a on a.CIK=o.CIK and a.PERIOD=o.PERIOD and a.base=o.FORM
group by 1 order by 1;

-- [q25] statement 25
-- Harm join: insider open-market trades (Form 4, code S/P) at the 15 filed-before-audit companies, inside [10-K filed, audit report date] vs the 365 days before filing
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
, apv as (select try_to_number(ISSUER_CIK) cik, FISCAL_PERIOD_END_DATE fpe, AUDIT_REPORT_DATE from LIBRARY_MARTS.FINANCE.FINANCE__FED_PCAOB_FORM_AP_FILINGS where try_to_number(ISSUER_CIK) is not null),
k as (select * from f where FORM='10-K' and q between '2024Q2' and '2025Q2'),
w as (
  select k.cik, k.NAME, k.fd, min(apv.AUDIT_REPORT_DATE) rpt
  from k join apv on apv.cik=k.cik and abs(datediff(day, apv.fpe, k.pd))<=7 group by 1,2,3
  having min(apv.AUDIT_REPORT_DATE) > dateadd(day, 3, k.fd)
),
subm as (
  select s.ACCESSION_NUMBER, try_to_number(s.ISSUER_CIK) cik from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_SUBMISSION s
  where try_to_number(s.ISSUER_CIK) in (select cik from w) and s.FILING_DATE between '2023-01-01' and '2026-09-30'
),
tr as (
  select subm.cik, t.TRANSACTION_DATE td, t.TRANSACTION_CODE code, t.SHARES, t.TRANSACTION_VALUE val
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_NONDERIV_TRANS t join subm on subm.ACCESSION_NUMBER=t.ACCESSION_NUMBER
  where t.TRANSACTION_CODE in ('S','P') and t.TRANSACTION_DATE between '2023-01-01' and '2026-09-30'
)
select w.NAME, w.fd k_filed, w.rpt audit_report, datediff(day, w.fd, w.rpt) window_days,
  count_if(tr.code='S' and tr.td between w.fd and w.rpt) sales_in_window, round(sum(iff(tr.code='S' and tr.td between w.fd and w.rpt, tr.val, 0))) sale_value_in_window,
  count_if(tr.code='P' and tr.td between w.fd and w.rpt) buys_in_window,
  count_if(tr.code='S' and tr.td between dateadd(day,-365,w.fd) and dateadd(day,-1,w.fd)) sales_prior_365, round(sum(iff(tr.code='S' and tr.td between dateadd(day,-365,w.fd) and dateadd(day,-1,w.fd), tr.val, 0))) sale_value_prior_365,
  count(tr.td) all_sp_trades_2023_26
from w left join tr on tr.cik=w.cik group by 1,2,3,4 order by sale_value_in_window desc;

-- [q26] statement 26
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
order by 1 desc, 2;

-- [q27] statement 27
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
order by 1 desc, 5 desc;

-- [q28] statement 28
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
order by 1 desc, 6 desc;

-- [q29] statement 29
-- Miss test for filed-before-audit: search Form AP by ISSUER NAME (any CIK, any version) for an audit report dated on/before each original 10-K
with t as (select column1 k, column2 pat, column3::date k_filed, column4::date pd from values
  ('ECD','%ECD AUTO%','2024-05-03','2023-12-31'),('ARTISAN','%ARTISAN CONSUMER%','2024-08-16','2024-06-30'),
  ('SINGULARITY','%SINGULARITY FUTURE%','2024-10-15','2024-06-30'),('GEV','%GENERAL ENTERPRISE VENTURES%','2024-04-15','2023-12-31'),
  ('CANNONAU','%CANNONAU%','2024-04-12','2023-12-31'),('BIOSTAX','%BIOSTAX%','2024-04-16','2023-12-31'),
  ('HCTI','%HEALTHCARE TRIANGLE%','2024-03-18','2023-12-31'),('YONGBAI','%YONG BAI%','2025-04-10','2024-12-31'),
  ('BIMERGEN','%BIMERGEN%','2025-05-30','2024-12-31'),('ITC','ITC HOLDINGS%','2025-02-14','2024-12-31'),
  ('BANCORP','%BANCORP, INC%','2025-03-03','2024-12-31'),('1895','1895 BANCORP%','2024-03-29','2023-12-31'))
select t.k, t.k_filed, a.ISSUER_NAME, a.ISSUER_CIK, a.FIRM_NAME, a.FISCAL_PERIOD_END_DATE, a.AUDIT_REPORT_DATE, a.LATEST_FORM_AP_FILING,
  iff(a.AUDIT_REPORT_DATE <= t.k_filed, 'ON/BEFORE 10-K', 'after') timing
from t left join LIBRARY_MARTS.FINANCE.FINANCE__FED_PCAOB_FORM_AP_FILINGS a
  on upper(a.ISSUER_NAME) like t.pat and abs(datediff(day, a.FISCAL_PERIOD_END_DATE, t.pd)) <= 7
order by t.k, a.AUDIT_REPORT_DATE;
