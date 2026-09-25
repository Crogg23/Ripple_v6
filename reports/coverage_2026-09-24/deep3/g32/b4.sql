-- @opgen_insider_sale_rows
select s.accession_number, s.filing_date, s.issuer_name, s.document_type, n.transaction_date, n.transaction_code, n.shares, n.price_per_share, n.transaction_value, n.shares_owned_after
from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_SUBMISSION s
join LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_NONDERIV_TRANS n on n.accession_number = s.accession_number
where try_to_number(s.issuer_cik) = 1293818 and try_to_date(s.filing_date::string) between '2024-10-01' and '2024-12-31' and n.transaction_code = 'S'
-- @tickers_exchange_all
select cik, ticker, company_name, exchange, _loaded_at from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_EDGAR_COMPANY_TICKERS_EXCHANGE
