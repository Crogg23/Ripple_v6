{{ config(materialized='view') }}

-- Grain (verified live by orchestrator): one row per tsn (993,346 rows).
-- ITIS (Integrated Taxonomic Information System, USDA/USGS) reference data.

with

source as (

    select * from {{ source('ripple_raw', 'FED_ITIS_TAXONOMIC_UNITS') }}

),

renamed as (

    select

        try_to_number(trim(TSN))                                as tsn,
        trim(UNIT_IND1)                                         as unit_ind1,
        trim(UNIT_NAME1)                                        as unit_name1,
        trim(UNIT_IND2)                                         as unit_ind2,
        trim(UNIT_NAME2)                                        as unit_name2,
        trim(UNIT_IND3)                                         as unit_ind3,
        trim(UNIT_NAME3)                                        as unit_name3,
        trim(UNIT_IND4)                                         as unit_ind4,
        trim(UNIT_NAME4)                                        as unit_name4,
        trim(UNNAMED_TAXON_IND)                                 as unnamed_taxon_ind,
        trim(NAME_USAGE)                                        as name_usage,
        trim(UNACCEPT_REASON)                                   as unaccept_reason,
        trim(CREDIBILITY_RTNG)                                  as credibility_rtng,
        trim(COMPLETENESS_RTNG)                                 as completeness_rtng,
        trim(CURRENCY_RATING)                                   as currency_rating,
        try_to_number(trim(PHYLO_SORT_SEQ))                     as phylo_sort_seq,
        try_to_timestamp_ntz(trim(INITIAL_TIME_STAMP))          as initial_time_stamp,
        try_to_number(trim(PARENT_TSN))                         as parent_tsn,
        try_to_number(trim(TAXON_AUTHOR_ID))                    as taxon_author_id,
        try_to_number(trim(HYBRID_AUTHOR_ID))                   as hybrid_author_id,
        try_to_number(trim(KINGDOM_ID))                         as kingdom_id,
        try_to_number(trim(RANK_ID))                            as rank_id,
        try_to_date(trim(UPDATE_DATE), 'YYYY-MM-DD')            as update_date,
        trim(UNCERTAIN_PRNT_IND)                                as uncertain_prnt_ind,
        trim(N_USAGE)                                           as n_usage,
        trim(COMPLETE_NAME)                                     as complete_name,

        -- metadata (no-underscore variant on ITIS tables; INGESTED_AT is an epoch-microseconds NUMBER)
        to_timestamp_ntz(INGESTED_AT, 6)                        as _loaded_at,
        SOURCE_RUN_ID                                           as _source_run_id,
        SRC_SHA256                                              as _src_sha256

    from source

),

keyed as (

    select
        *
    from renamed
    where tsn is not null

),

deduped as (

    select *,
        row_number() over (
            partition by tsn
            order by _loaded_at desc
        ) as _row_num
    from keyed

)

select
    tsn,
    unit_ind1,
    unit_name1,
    unit_ind2,
    unit_name2,
    unit_ind3,
    unit_name3,
    unit_ind4,
    unit_name4,
    unnamed_taxon_ind,
    name_usage,
    unaccept_reason,
    credibility_rtng,
    completeness_rtng,
    currency_rating,
    phylo_sort_seq,
    initial_time_stamp,
    parent_tsn,
    taxon_author_id,
    hybrid_author_id,
    kingdom_id,
    rank_id,
    update_date,
    uncertain_prnt_ind,
    n_usage,
    complete_name,
    _loaded_at,
    _source_run_id,
    _src_sha256
from deduped
where _row_num = 1
