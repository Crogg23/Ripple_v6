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
order by 1 desc, 8 desc, 9 desc
