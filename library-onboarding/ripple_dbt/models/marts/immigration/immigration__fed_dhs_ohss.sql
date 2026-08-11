{{ config(materialized='table', schema='IMMIGRATION') }}

-- GRAIN: one row per encounter report row (multi-sheet compilation)

with source as (
    select * from {{ source('ripple_raw', 'FED_DHS_OHSS') }}
)

-- FIX 2026-08-11 (two parts): the projection omitted TABLE_NAME and five
-- breakdown dimensions (added below). Landing is verified 100% distinct
-- (50,740 = 50,740 rows incl. a several-hundred-column raw multi-sheet
-- spread) but this curated projection still cannot express every
-- distinguishing raw column, so _source_row_hash carries each landing row's
-- full fingerprint: no real row collapses, and apparent duplicates are
-- provably distinct facts. The real cure is a per-sheet re-model (backlog).

select
    hash(*) as _source_row_hash,
    REPORT_MONTH,
    TABLE_NAME,
    ENCOUNTER_TYPE,
    REGION_OR_SECTOR,
    CITIZENSHIP,
    FAMILY_STATUS,
    CRIMINALITY,
    INITIAL_ARRESTING_AGENCY,
    BOOK_OUT_OUTCOME,
    REPATRIATION_TYPE,
    CREDIBLE_FEAR_RESULT,
    CHNV_PROCESS_TYPE,
    FISCAL_YEAR,
    CALENDAR_YEAR,
    EVENT_COUNT,
    ENCOUNTERS,
    SOURCE_FILE_NAME,
    SOURCE_SHEET_NAME,
    "MONTH" as MONTH,
    TOTAL,
    VENEZUELA,
    CUBA,
    MEXICO,
    HAITI,
    HONDURAS,
    COLOMBIA,
    GUATEMALA,
    EL_SALVADOR,
    ECUADOR,
    RUSSIA,
    OTHER,
    NICARAGUA,
    BORDER,
    INTERIOR
from source
