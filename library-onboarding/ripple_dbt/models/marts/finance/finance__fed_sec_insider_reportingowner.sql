{{ config(materialized='table', schema='FINANCE') }}

-- GRAIN: one row per filing-owner pair (accession_number + rptownercik is unique)
-- Answers: Who are the insiders making trades, what's their role at the company?
-- Source: SEC EDGAR Form 3/4/5 â€” Reporting Owners (~1.93M records)
-- Key joins: accession_number â†’ insider_submission + nonderiv_trans; rptownercik â†’ SEC entities

select
    trim(accession_number)                           as accession_number,
    trim(rptownercik)                                as owner_cik,
    trim(rptownername)                               as owner_name,
    trim(rptowner_relationship)                      as relationship,
    trim(rptowner_title)                             as title,
    trim(rptowner_street1)                           as street1,
    trim(rptowner_city)                              as city,
    trim(rptowner_state)                             as state,
    trim(rptowner_zipcode)                           as zip_code,
    _loaded_at
from {{ ref('stg_fed_sec_insider_reportingowner__records') }}
qualify row_number() over (
    partition by accession_number, rptownercik
    order by _loaded_at desc
) = 1
