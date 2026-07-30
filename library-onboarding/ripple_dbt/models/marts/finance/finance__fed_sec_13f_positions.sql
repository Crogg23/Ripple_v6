{{ config(materialized='table', schema='FINANCE') }}

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
