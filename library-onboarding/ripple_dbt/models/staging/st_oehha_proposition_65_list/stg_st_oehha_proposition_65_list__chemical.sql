{{ config(materialized='view') }}

with source as (

    select *
    from {{ source('ripple_raw', 'ST_OEHHA_PROPOSITION_65_LIST') }}

),

renamed as (

    select

        -- key identifiers
        trim(CHEMICAL)                                      as chemical,
        trim(CAS_NO)                                        as cas_no,

        -- attributes
        trim(TYPE_OF_TOXICITY)                              as type_of_toxicity,
        trim(LISTING_MECHANISM)                             as listing_mechanism,
        -- 2026-08-09 fix: landed values are ISO (e.g. '1990-01-01'); the old
        -- 'MM/DD/YYYY' format string nulled out 100% of dates.
        try_to_date(trim(DATE_LISTED))                      as date_listed,
        try_to_double(trim(NSRL_OR_MADL_G_DAY_A))          as nsrl_or_madl_g_day,

        -- overflow / extra columns retained as-is
        trim(COL_6)                                         as col_6,
        trim(COL_7)                                         as col_7,
        trim(COL_8)                                         as col_8,

        -- pipeline metadata
        _ingested_at,
        _source_run_id

    from source
    where CHEMICAL is not null
      and trim(CHEMICAL) != ''

),

deduped as (

    select *,
        row_number() over (
            partition by chemical, cas_no
            order by _ingested_at desc
        ) as _row_num
    from renamed

)

select
    -- surrogate key
    {{ dbt_utils.generate_surrogate_key(['chemical', 'cas_no']) }} as chemical_key,

    chemical,
    cas_no,
    type_of_toxicity,
    listing_mechanism,
    date_listed,
    nsrl_or_madl_g_day,
    col_6,
    col_7,
    col_8,
    _ingested_at,
    _source_run_id

from deduped
where _row_num = 1
