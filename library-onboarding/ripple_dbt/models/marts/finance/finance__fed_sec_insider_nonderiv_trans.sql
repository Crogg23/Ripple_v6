{{ config(materialized='table', schema='FINANCE') }}

-- GRAIN: one row per insider transaction (accession_number + nonderiv_trans_sk)
-- Answers: What non-derivative securities did insiders buy/sell, at what price?
-- Source: SEC EDGAR Form 3/4/5 â€” Non-Derivative Transactions (~2.67M records)
-- Key joins: accession_number â†’ insider_submission (issuer info) + reportingowner (who)

select
    trim(accession_number)                           as accession_number,
    trim(nonderiv_trans_sk)                          as transaction_sk,
    trim(security_title)                             as security_title,
    try_to_date(trans_date, 'DD-MON-YYYY')            as transaction_date,
    trim(trans_code)                                 as transaction_code,
    try_to_double(trans_shares)                      as shares,
    try_to_double(trans_pricepershare)               as price_per_share,
    try_to_double(trans_shares) * try_to_double(trans_pricepershare) as transaction_value,
    trim(trans_acquired_disp_cd)                     as acquired_disposed,
    try_to_double(shrs_ownd_folwng_trans)            as shares_owned_after,
    try_to_double(valu_ownd_folwng_trans)            as value_owned_after,
    trim(direct_indirect_ownership)                  as ownership_form,
    trim(nature_of_ownership)                        as nature_of_ownership,
    trim(trans_form_type)                            as form_type,
    (trim(trans_acquired_disp_cd) = 'A') as is_acquisition,
    (trim(trans_acquired_disp_cd) = 'D') as is_disposition,
    _loaded_at
from {{ ref('stg_fed_sec_insider_nonderiv_trans__records') }}
qualify row_number() over (
    partition by accession_number, nonderiv_trans_sk
    order by _loaded_at desc
) = 1
