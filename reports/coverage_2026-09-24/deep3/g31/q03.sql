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
group by 1 having count(*) >= 60 order by n desc
