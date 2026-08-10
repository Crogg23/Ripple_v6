{{ config(materialized='view') }}

-- LOADER DEFECT (documented, not fixable here): the report title row was
-- consumed as the header, so the landing columns are the title
-- (PURPLE_BOOK_MONTHLY_HISTORICAL_DATA_CHANGES_REPORT_JUNE_2026) plus
-- UNNAMED_1..27, and preamble / section / header rows are embedded as DATA
-- rows. Columns are renamed POSITIONALLY onto the real header found in the
-- data, and non-record rows are filtered out by keeping only rows whose
-- BLA Number position is numeric.

with

source as (

    select * from {{ source('ripple_raw', 'FED_FDA_PURPLE_BOOK') }}
    -- keep only real license rows (numeric BLA number in position 3); drops
    -- the embedded title / preamble / section / header rows
    where regexp_like(trim(UNNAMED_2), '^[0-9]+$')

),

keyed as (

    -- Grain was NOT pre-verified post-filter. (bla_number, product_number,
    -- supplement_number) is the expected natural grain, so a row_number()
    -- over the full-row hash is appended as a deterministic provenance
    -- tiebreaker to make purple_book_record_id fully unique regardless.
    select
        source.*,
        {{ dbt_utils.generate_surrogate_key(['UNNAMED_2', 'UNNAMED_20', 'UNNAMED_16']) }}
            || '-'
            || row_number() over (
                   partition by UNNAMED_2, UNNAMED_20, UNNAMED_16
                   order by hash(*)
               ) as purple_book_record_id
    from source

),

renamed as (

    select

        -- identifiers (positional rename onto the real embedded header)
        purple_book_record_id,
        trim(UNNAMED_2)                                as bla_number,
        trim(UNNAMED_20)                               as product_number,
        trim(UNNAMED_16)                               as supplement_number,
        trim(UNNAMED_19)                               as license_number,

        -- dimensions
        trim(PURPLE_BOOK_MONTHLY_HISTORICAL_DATA_CHANGES_REPORT_JUNE_2026)
                                                       as change_type,
        trim(UNNAMED_1)                                as applicant,
        trim(UNNAMED_3)                                as proprietary_name,
        trim(UNNAMED_4)                                as proper_name,
        trim(UNNAMED_5)                                as license_type,
        trim(UNNAMED_6)                                as strength,
        trim(UNNAMED_7)                                as dosage_form,
        trim(UNNAMED_8)                                as route_of_administration,
        trim(UNNAMED_9)                                as product_presentation,
        trim(UNNAMED_10)                               as marketing_status,
        trim(UNNAMED_11)                               as licensure,
        -- Dates arrive like '2-Jan-59' / '19-Dec-25'. 'DD-MON-YY' relies on
        -- Snowflake's TWO_DIGIT_CENTURY_START pivot (default 1970): '59' -> 2059
        -- unless the session pivot says otherwise — genuinely ambiguous for
        -- pre-1970 approvals; flagged, not silently fixed.
        try_to_date(trim(UNNAMED_12), 'DD-MON-YY')     as approval_date,
        try_to_date(trim(UNNAMED_13), 'DD-MON-YY')     as interchangeable_approval_date,
        trim(UNNAMED_14)                               as ref_product_proper_name,
        trim(UNNAMED_15)                               as ref_product_proprietary_name,
        trim(UNNAMED_17)                               as submission_type,
        trim(UNNAMED_18)                               as interchangeable_supplement_number,
        trim(UNNAMED_21)                               as center,
        try_to_date(trim(UNNAMED_22), 'DD-MON-YY')     as date_of_first_licensure,
        try_to_date(trim(UNNAMED_23), 'DD-MON-YY')     as exclusivity_expiration_date,
        try_to_date(trim(UNNAMED_24), 'DD-MON-YY')     as first_interchangeable_exclusivity_exp_date,
        try_to_date(trim(UNNAMED_25), 'DD-MON-YY')     as ref_product_exclusivity_exp_date,
        try_to_date(trim(UNNAMED_26), 'DD-MON-YY')     as orphan_exclusivity_exp_date,
        trim(UNNAMED_27)                               as patent_list_provided,

        -- metadata
        to_timestamp_ntz(INGESTED_AT, 6)               as _ingested_at,
        SOURCE_RUN_ID                                  as _source_run_id,
        SRC_SHA256                                     as _src_sha256

    from keyed

)

select * from renamed
