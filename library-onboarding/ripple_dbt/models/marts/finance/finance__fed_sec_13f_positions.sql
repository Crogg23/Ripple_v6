{{ config(enabled=false, materialized='table', schema='FINANCE') }}

-- RETIRED 2026-08-23 (13F consolidation): this was a raw passthrough duplicate
-- of finance__fed_sec_13f_holdings (the authoritative view, which also carries
-- the value_usd unit fix). The built 101M-row table is a DROP candidate.
-- GRAIN: one row per 13F position holding

with source as (
    select * from {{ source('ripple_raw', 'FED_SEC_13F_POSITIONS') }}
)

select
    ACCESSION_NUMBER,
    INFOTABLE_SK,
    NAMEOFISSUER,
    TITLEOFCLASS,
    CUSIP,
    FIGI,
    VALUE,
    SSHPRNAMT,
    SSHPRNAMTTYPE,
    PUTCALL,
    INVESTMENTDISCRETION,
    OTHERMANAGER,
    VOTING_AUTH_SOLE,
    VOTING_AUTH_SHARED,
    VOTING_AUTH_NONE
from source
