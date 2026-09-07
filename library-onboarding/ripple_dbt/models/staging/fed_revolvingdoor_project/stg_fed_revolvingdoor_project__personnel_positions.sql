{{ config(materialized='view') }}

-- 2026-09-07: this is a table of JOB SLOTS, not people. Measured on the
-- landed file: 409 rows, H (the "name" column) is the string 'nan' on 408 of
-- them and '3' on the one documentation row ("Text (See Position Type tab)").
-- There is no person and no date anywhere in the source. So:
--   * person_name is gone. A column that is 'nan' end to end is not a key.
--   * the documentation row is filtered out.
--   * position_key is md5 over (position_name, position_department,
--     position_type). Two landed rows share a key; dedupe keeps the newest.
-- The real revolving-door source is the LDA covered_position field, loaded
-- separately by scripts/senate_lda_load.py. This table cannot answer "who".

with source as (

    select * from {{ source('ripple_raw', 'FED_REVOLVINGDOOR_PROJECT') }}

),

renamed as (

    select

        -- header / identity. h is 'nan' on every real row; kept raw, never a name.
        nullif(trim(h), 'nan')                                   as h,
        trim(position_type)                                      as position_type,
        trim(position_name)                                      as position_name,
        trim(position_department)                                as position_department,
        trim(position_description)                               as position_description,

        -- sector / interest pairs (un-pivoted names kept for mart flexibility)
        trim(sector1)                                            as sector1,
        trim(sector1_interest)                                   as sector1_interest,
        trim(sector2)                                            as sector2,
        trim(sector2_interest)                                   as sector2_interest,
        trim(sector3)                                            as sector3,
        trim(sector3_interest)                                   as sector3_interest,
        trim(sector4)                                            as sector4,
        trim(sector4_interest)                                   as sector4_interest,
        trim(sector5)                                            as sector5,
        trim(sector5_interest)                                   as sector5_interest,
        trim(sector6)                                            as sector6,
        trim(sector6_interest)                                   as sector6_interest,
        trim(sector7)                                            as sector7,
        trim(sector7_interest)                                   as sector7_interest,
        trim(sector8)                                            as sector8,
        trim(sector8_interest)                                   as sector8_interest,
        trim(sector9)                                            as sector9,
        trim(sector9_interest)                                   as sector9_interest,
        trim(sector10)                                           as sector10,
        trim(sector10_interest)                                  as sector10_interest,
        trim(sector11)                                           as sector11,
        trim(sector11_interest)                                  as sector11_interest,
        trim(sector12)                                           as sector12,
        trim(sector12_interest)                                  as sector12_interest,
        -- note: source skips 13; sector14 appears twice with a _1 suffix
        trim(sector14)                                           as sector14,
        trim(sector14_interest)                                  as sector14_interest,
        trim(sector14_1)                                         as sector14_1,
        trim(sector14_interest_1)                                as sector14_interest_1,
        trim(sector_15)                                          as sector15,
        trim(sector15_interest)                                  as sector15_interest,
        trim(sector16)                                           as sector16,
        trim(sector16_interest)                                  as sector16_interest,

        -- derived / convenience columns
        -- primary agency is the position department
        trim(position_department)                                as agency,

        -- primary industry sector is sector1 (most-specific leading sector)
        trim(sector1)                                            as industry_sector,

        -- composite natural key for deduplication
        md5(
            coalesce(trim(position_name),'') || '||' ||
            coalesce(trim(position_department),'') || '||' ||
            coalesce(trim(position_type),'')
        )                                                        as position_key,

        -- ingestion metadata (populated by the loader; cast safely)
        to_timestamp_ntz(_ingested_at, 6)                        as _ingested_at,
        _source_run_id                                           as _source_run_id

    from source
    -- the one documentation row: H='3', position_type 'Text (See Position Type tab)'
    where trim(position_type) not ilike 'Text (See%'

),

deduped as (

    select *,
        row_number() over (
            partition by position_key
            order by _ingested_at desc nulls last
        ) as _row_num
    from renamed

)

select * exclude (_row_num)
from deduped
where _row_num = 1
