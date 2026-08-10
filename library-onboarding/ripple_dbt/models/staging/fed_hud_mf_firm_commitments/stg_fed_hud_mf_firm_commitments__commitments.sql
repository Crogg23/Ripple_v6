{{ config(materialized='view') }}

-- The landed Excel arrives with a multi-row preamble (report title, source
-- system, fiscal-year coverage, a "Project Count" line) and the real header
-- row itself landed as data. Columns landed as a title column + UNNAMED_1..24.
-- The real header (25 fields) is renamed positionally below, and rows are
-- kept only where the FHA Number position is numeric — this drops the
-- preamble, header, and count rows (~25,557 data rows remain per the file's
-- own count line).

with

source as (

    select * from {{ source('ripple_raw', 'FED_HUD_MF_FIRM_COMMITMENTS') }}

),

positional as (

    select
        trim(DATABASE_OF_FHA_MULTIFAMILY_FIRM_COMMITMENT_ACTIVITY) as fha_number_raw,
        trim(UNNAMED_1)  as project_name,
        trim(UNNAMED_2)  as project_city,
        trim(UNNAMED_3)  as project_state,
        trim(UNNAMED_4)  as program_type,
        trim(UNNAMED_5)  as program_category,
        trim(UNNAMED_6)  as activity_description,
        trim(UNNAMED_7)  as activity_group,
        trim(UNNAMED_8)  as facility_type,
        trim(UNNAMED_9)  as program_subcategory,
        trim(UNNAMED_10) as firm_activity,
        trim(UNNAMED_11) as lender_name,
        trim(UNNAMED_12) as mortgage_amount_raw,
        trim(UNNAMED_13) as total_units_raw,
        trim(UNNAMED_14) as firm_activity_date_raw,
        trim(UNNAMED_15) as fiscal_year_raw,
        trim(UNNAMED_16) as map_or_tap,
        trim(UNNAMED_17) as lihtc,
        trim(UNNAMED_18) as tax_exempt_bonds,
        trim(UNNAMED_19) as home,
        trim(UNNAMED_20) as cdbg,
        trim(UNNAMED_21) as refi_202,
        trim(UNNAMED_22) as irp_decoupling,
        trim(UNNAMED_23) as hope_vi,
        trim(UNNAMED_24) as current_status,
        INGESTED_AT,
        SOURCE_RUN_ID,
        SRC_SHA256
    from source
    -- keep only real data rows: FHA Number is numeric
    where try_to_number(trim(DATABASE_OF_FHA_MULTIFAMILY_FIRM_COMMITMENT_ACTIVITY)) is not null

),

keyed as (

    -- FHA Number + firm activity date is NEAR-unique (a project can have
    -- multiple firm activities on the same date), so a row_number() over the
    -- full-row hash is appended as a deterministic tiebreaker to make
    -- commitment_record_id fully unique.
    select
        positional.*,
        {{ dbt_utils.generate_surrogate_key(['fha_number_raw', 'firm_activity_date_raw']) }}
            || '-'
            || row_number() over (
                   partition by fha_number_raw, firm_activity_date_raw
                   order by hash(*)
               ) as commitment_record_id
    from positional

)

select

    -- identifiers
    commitment_record_id,
    fha_number_raw                                     as fha_number,

    -- project
    project_name,
    project_city,
    project_state,
    facility_type,

    -- program / activity
    program_type,
    program_category,
    program_subcategory,
    activity_description,
    activity_group,
    firm_activity,
    lender_name,

    -- measures
    try_to_number(mortgage_amount_raw, 18, 2)          as mortgage_amount,
    try_to_number(total_units_raw)                     as total_units,
    coalesce(
        try_to_date(left(firm_activity_date_raw, 10), 'YYYY-MM-DD'),
        try_to_date(firm_activity_date_raw, 'MM/DD/YYYY')
    )                                                  as firm_activity_date,
    try_to_number(fiscal_year_raw)                     as fiscal_year_at_firm_activity,

    -- flags
    map_or_tap,
    lihtc,
    tax_exempt_bonds,
    home,
    cdbg,
    refi_202,
    irp_decoupling,
    hope_vi,
    current_status,

    -- metadata
    to_timestamp_ntz(INGESTED_AT, 6)                   as _ingested_at,
    SOURCE_RUN_ID                                      as _source_run_id,
    SRC_SHA256                                         as _src_sha256

from keyed
