{{ config(materialized='view') }}

-- HAND-EDITED 2026-09-19: dedupe is a whole-raw-row hash (_row_hash), see the
-- comment in deduped. The staging generator skips files carrying this marker.

with source as (

    -- _row_hash: hash of every landing column except the load stamps
    select *, hash(* exclude (_INGESTED_AT, _SOURCE_RUN_ID, _SRC_SHA256)) as _row_hash
    from {{ source('ripple_raw', 'INTL_CH_ZEFIX') }}

),

renamed as (

    select
        -- primary / surrogate key
        -- 2026-09-19: _row_hash added -- (UID, EHRAID, CHID) alone repeats
        -- across real rows, so without it the key is not one-per-row.
        {{ dbt_utils.generate_surrogate_key(['UID', 'EHRAID', 'CHID', '_row_hash']) }} as company_id,

        -- identifiers
        UID                                          as uid,
        EHRAID                                       as ehraid,
        CHID                                         as chid,

        -- core attributes
        NAME                                         as name,
        LEGAL_FORM                                   as legal_form,
        STATUS                                       as status,

        -- address
        ADDRESS_STREET                               as address_street,
        ADDRESS_HOUSE_NUMBER                         as address_house_number,
        ADDRESS_ZIP                                  as address_zip,
        ADDRESS_CITY                                 as address_city,
        ADDRESS_CANTON                               as address_canton,

        -- registration
        REGISTRY_OF_COMMERCE                         as registry_of_commerce,
        OLD_NAMES                                    as old_names,
        {{ stg_date('SOGC_PUBLICATION_DATE') }}           as sogc_publication_date,
        MUTATION_TYPE                                as mutation_type,
        {{ stg_int('COMMUNITY_BFS_ID') }}              as community_bfs_id,

        -- geography
        COUNTRY                                      as country,

        -- metadata
        _ingested_at,
        _source_run_id,

        -- whole-raw-row hash, carried for the dedupe only
        _row_hash

    from source

),

deduped as (

    -- 2026-09-19: the old partition was company_id (hash of UID, EHRAID, CHID).
    -- It hid 17 of 18 landing rows on a single load -- that key does not
    -- identify a row. The dedupe is now the whole-raw-row hash, so only exact
    -- copies are dropped (0 exact copies in landing).
    select *,
        row_number() over (
            partition by _row_hash
            order by _ingested_at desc
        ) as _row_num
    from renamed

)

select * exclude (_row_num, _row_hash)
from deduped
where _row_num = 1
