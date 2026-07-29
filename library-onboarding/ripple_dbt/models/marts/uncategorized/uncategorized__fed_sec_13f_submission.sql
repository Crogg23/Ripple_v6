{{ config(materialized='table', schema='FINANCE') }}

-- GRAIN: one row per 13F submission filing

with source as (
    select * from {{ source('ripple_raw', 'FED_SEC_13F_SUBMISSIONS') }}
)

select
    ACCESSION_NUMBER,
    FILING_DATE,
    SUBMISSIONTYPE,
    CIK,
    PERIODOFREPORT,
    _SRC_FILE
from source
