{{ config(materialized='table', schema='FINANCE') }}

-- GRAIN: one row per insider filing (accession_number is unique)
-- Answers: What insider trading filings have been made, for which companies?
-- Source: SEC EDGAR Form 3/4/5 â€” Submissions (~1.77M filings)
-- Key joins: issuercik â†’ SEC EDGAR companies; accession_number â†’ transactions + owners

select
    trim(accession_number)                           as accession_number,
    try_to_date(filing_date, 'DD-MON-YYYY')           as filing_date,
    try_to_date(period_of_report, 'DD-MON-YYYY')     as period_of_report,
    try_to_date(date_of_orig_sub, 'DD-MON-YYYY')     as date_of_original_submission,
    trim(document_type)                              as document_type,
    trim(issuercik)                                  as issuer_cik,
    trim(issuername)                                 as issuer_name,
    trim(issuertradingsymbol)                        as issuer_ticker,
    (trim(no_securities_owned) = '1') as no_securities_owned,
    (trim(not_subject_sec16) = '1') as not_subject_to_section16,
    trim(remarks)                                    as remarks,
    _loaded_at
from {{ ref('stg_fed_sec_insider_submission__records') }}
qualify row_number() over (
    partition by accession_number
    order by _loaded_at desc
) = 1
