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
from m group by 1,2 having count(distinct cik) >= 5 order by operating desc, ciks desc limit 40
