{{ config(materialized='view') }}

-- LOADER DEFECT (documented, not fixable here): the loader consumed the first
-- DATA row as the column header, so the landing column names are actually the
-- values of the first record (C_9, UNNAMED_1, HUMAN, C_00015741, TAPAZOLE, ...)
-- and that record is missing from the table. Columns are renamed POSITIONALLY
-- back to the Health Canada DPD drug.txt layout below.

with

source as (

    select * from {{ source('ripple_raw', 'INTL_HEALTHCANADA_DPD_DRUG') }}

),

renamed as (

    select

        -- identifiers (positional rename: landing names are eaten first-row values)
        trim(C_9)                                      as drug_code,
        trim(C_00015741)                               as drug_identification_number,

        -- dimensions
        trim(UNNAMED_1)                                as product_categorization,
        trim(HUMAN)                                    as drug_class,
        trim(TAPAZOLE)                                 as brand_name,
        trim(UNNAMED_5)                                as descriptor,
        trim(N)                                        as pediatric_flag,
        trim(C_00135)                                  as accession_number,
        try_to_number(trim(C_1))                       as number_of_ais,
        try_to_date(trim(C_24_DEC_2025), 'DD-MON-YYYY') as last_update_date,
        trim(C_0104552001)                             as ai_group_no,
        trim(HUMAIN)                                   as class_f,
        trim(UNNAMED_12)                               as brand_name_f,
        trim(UNNAMED_13)                               as descriptor_f,

        -- metadata
        to_timestamp_ntz(INGESTED_AT, 6)               as _ingested_at,
        SOURCE_RUN_ID                                  as _source_run_id,
        SRC_SHA256                                     as _src_sha256

    from source

)

select * from renamed
