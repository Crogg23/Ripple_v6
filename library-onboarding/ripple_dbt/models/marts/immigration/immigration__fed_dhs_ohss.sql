{{ config(materialized='table', schema='IMMIGRATION') }}

-- GRAIN: one row per encounter report row (multi-sheet compilation)

with source as (
    select * from {{ source('ripple_raw', 'FED_DHS_OHSS') }}
)

-- FIX 2026-08-11: the projection omitted TABLE_NAME, INITIAL_ARRESTING_AGENCY,
-- BOOK_OUT_OUTCOME, REPATRIATION_TYPE, CREDIBLE_FEAR_RESULT, CHNV_PROCESS_TYPE,
-- which made distinct rows look 77% duplicated. Columns added; no dedupe --
-- the rows are real once the full grain is projected.

select
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
