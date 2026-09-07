{{ config(materialized='table', schema='POLITICS') }}

-- GRAIN: one row per Senate EFD Periodic Transaction Report filing, 2021 on.
-- 799 rows: 699 HTML and 100 scanned paper.
--
-- This is the INDEX, not the trades. It exists so any count of trade lines can
-- be checked against the number of filings that should have produced them, and
-- so the 100 unreadable paper filings are countable on their own.
--
-- filer_last_clean has the suffix and any trailing comma stripped. Raw
-- filer_last is kept beside it because the raw form is what the source says.

with source as (
    select * from {{ source('ripple_raw', 'FED_SENATE_EFD_FILINGS') }}
)

select
    FILING_ID                                       as filing_id,
    FILER_FULL                                      as filer_full,
    FILER_FIRST                                     as filer_first,
    FILER_LAST                                      as filer_last,
    FILER_LAST_CLEAN                                as filer_last_clean,
    REPORT_TITLE                                    as report_title,
    FILING_KIND                                     as filing_kind,
    IS_AMENDMENT                                    as is_amendment,
    FILING_YEAR                                     as filing_year,
    try_to_date(nullif(trim(FILED_DATE), ''), 'MM/DD/YYYY') as filed_date,
    FILING_LINK                                     as filing_link,
    'fed_senate_efd_filings'                        as source_id,
    _INGESTED_AT                                    as _loaded_at
from source
