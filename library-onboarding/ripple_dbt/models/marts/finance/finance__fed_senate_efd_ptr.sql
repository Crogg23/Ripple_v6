{{ config(materialized='table', schema='FINANCE') }}

-- GRAIN: one row per reported trade line, 2021 on. 6,855 rows.
--
-- THIS DOES NOT REPLACE FINANCE__FED_SENATE_STOCK_WATCHER. That table holds
-- 2012-06-14 to 2020-12-02 and stops dead; this one starts 2021. They do not
-- overlap, so a union across the seam needs no dedupe. Neither is complete on
-- its own.
--
-- THREE THINGS TO KNOW BEFORE COUNTING ANYTHING:
--
--   filing_kind = 'paper' is a SCANNED filing that could not be read. 100 of
--   them. The row exists with null trade fields so the hole is visible in the
--   data rather than silently absent. Filter them out of any trade count and
--   report how many you dropped.
--
--   is_amendment = 'True' on 1,030 rows. NOTHING supersedes an original with
--   its amendment yet. Summing across both double counts, the same way the FEC
--   independent expenditure mart did before its supersede flag.
--
--   amount is a RANGE, never a number: '$1,001 - $15,000'. There is no finer
--   resolution in the source. Any total is a bounded estimate and has to be
--   reported as one.
--
-- filer_last_clean has the suffix and any trailing comma stripped, because
-- 'Perdue , Jr' and 'Moran,' miss a plain crosswalk join outright. Join it to
-- POLITICS__MEMBER_CROSSWALK restricted to Senate seat holders in congresses
-- 116-119; the 116th is required or Perdue and Roberts fall out.

with source as (
    select * from {{ source('ripple_raw', 'FED_SENATE_EFD_PTR') }}
)

select
    FILING_ID                                       as filing_id,
    SENATOR                                         as senator,
    FILER_LAST_CLEAN                                as filer_last_clean,
    FILING_YEAR                                     as filing_year,
    FILING_KIND                                     as filing_kind,
    IS_AMENDMENT                                    as is_amendment,
    {{ ripple_num('LINE_NO') }}                     as line_no,
    try_to_date(nullif(trim(TRANSACTION_DATE), ''), 'MM/DD/YYYY') as transaction_date,
    try_to_date(nullif(trim(FILED_DATE), ''), 'MM/DD/YYYY')       as filed_date,
    OWNER                                           as owner,
    TICKER                                          as ticker,
    ASSET_DESCRIPTION                               as asset_description,
    ASSET_TYPE                                      as asset_type,
    TYPE                                            as transaction_type,
    AMOUNT                                          as amount_range,
    COMMENT                                         as comment,
    PTR_LINK                                        as ptr_link,
    'fed_senate_efd_ptr'                            as source_id,
    _INGESTED_AT                                    as _loaded_at
from source
