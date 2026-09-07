{{ config(materialized='view') }}

-- EOIR FOIA case file, A_tblCase. 12.6M rows.
--
-- The loader ate the header and stuffed every tab-separated line into ONE column
-- named CASE_TYPE (after its 13th field). This view splits that line back into the
-- 39 fields of A_tblCase. Field names come from the EOIR Case Data Code Key PDF
-- (justice.gov/eoir/page/file/eoir-case-data-code-key/download, May 2019),
-- checked position by position against the data on 2026-09-07: field 7 is a
-- 2-letter nationality, 9 is N/D/R custody, 13 is RMV/DEP/CFR, 14 is a base-city
-- code, 15 a hearing timestamp, 26 a masked MM/YYYY birth date, 31 M/F, 34 0/1.
-- The Code Key does not number UPDATED_ZIPCODE/UPDATED_CITY at 5-6, C_BIRTHDATE
-- at 26, ADDRESS_CHANGEDON at 29 or ZBOND_MRG_FLAG at 30; those names are the
-- FOIA file header as published. FNLDISP is in the Code Key and NOT in this file.
--
-- NUL bytes: field 10 carries \x00 on 4.26M rows, field 20 on 622K. They are
-- stripped before the split. About 100 rows carry a stray tab inside a free-text
-- field and shift right of it; field 1 (the case id) is safe on every row.
--
-- No judge here. IJ_CODE and the decision live in B_TblProceeding, which the zip
-- loader never landed (largest-member trap). Still missing as of 2026-09-07.

{% set fields = [
    'IDNCASE', 'ALIEN_CITY', 'ALIEN_STATE', 'ALIEN_ZIPCODE',
    'UPDATED_ZIPCODE', 'UPDATED_CITY', 'NAT', 'LANG', 'CUSTODY',
    'SITE_TYPE', 'E_28_DATE', 'ATTY_NBR', 'CASE_TYPE', 'UPDATE_SITE',
    'LATEST_HEARING', 'LATEST_TIME', 'LATEST_CAL_TYPE', 'UP_BOND_DATE',
    'UP_BOND_RSN', 'CORRECTIONAL_FAC', 'RELEASE_MONTH', 'RELEASE_YEAR',
    'INMATE_HOUSING', 'DATE_OF_ENTRY', 'C_ASY_TYPE', 'C_BIRTHDATE',
    'C_RELEASE_DATE', 'UPDATED_STATE', 'ADDRESS_CHANGEDON',
    'ZBOND_MRG_FLAG', 'GENDER', 'DATE_DETAINED', 'DATE_RELEASED', 'LPR',
    'DETENTION_DATE', 'DETENTION_LOCATION', 'DCO_LOCATION',
    'DETENTION_FACILITY_TYPE', 'CASEPRIORITY_CODE'
] %}

with source as (

    select replace(CASE_TYPE, '\x00', '') as line,
           _INGESTED_AT,
           _SOURCE_RUN_ID
    from {{ source('ripple_raw', 'FED_EOIR_CASE_DATA') }}

),

split as (

    select
        {%- for f in fields %}
        nullif(trim(split_part(line, '\t', {{ loop.index }})), '') as {{ f | lower }},
        {%- endfor %}
        regexp_count(line, '\t') + 1 as field_count,
        _INGESTED_AT as _loaded_at,
        _SOURCE_RUN_ID as _source_run_id

    from source

)

select * from split
