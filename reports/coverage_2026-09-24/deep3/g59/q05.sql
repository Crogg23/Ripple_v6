-- SEC tickers (ECONOMICS copy) vs the FINANCE copy g30 already checked: lookup shape, load runs, overlap
with e as (select CIK, TICKER, COMPANY_TITLE, _SOURCE_RUN_ID, _INGESTED_AT from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_SEC_EDGAR_COMPANY_TICKERS),
f as (select CIK, TICKER from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_EDGAR_COMPANY_TICKERS_EXCHANGE)
select 'e_profile' k, count(*)::text a, count(distinct CIK)::text b, count(distinct CIK||'|'||TICKER)::text c, count(distinct TICKER)::text d,
  count(distinct _SOURCE_RUN_ID)::text e1, min(_INGESTED_AT)::text f1, max(_INGESTED_AT)::text g1 from e
union all
select 'top_ticker', TICKER, count(*)::text, null, null, null, null, null from e group by TICKER qualify row_number() over (order by count(*) desc) <= 3
union all
select 'top_cik', CIK::text, count(*)::text, any_value(COMPANY_TITLE), listagg(TICKER, ',') within group (order by TICKER), null, null, null from e group by CIK qualify row_number() over (order by count(*) desc) <= 3
union all
select 'overlap', (select count(*) from e where (CIK, TICKER) in (select CIK, TICKER from f))::text,
  (select count(*) from e where (CIK, TICKER) not in (select CIK, TICKER from f))::text,
  (select count(*) from f where (CIK, TICKER) not in (select CIK, TICKER from e))::text, null, null, null, null
