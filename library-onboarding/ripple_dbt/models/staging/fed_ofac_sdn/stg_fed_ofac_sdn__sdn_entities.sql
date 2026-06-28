{{ config(materialized='view') }}

{#
    OFAC SDN (Specially Designated Nationals) list -- one row per sanctioned entity.

    TRAP (finding #9): OFAC's raw CSV uses '-0- ' (literal dash-zero-dash WITH A
    TRAILING SPACE, LENGTH=4) as its null token across SDN_TYPE, TITLE, REMARKS,
    VESS_TYPE, VESS_FLAG, CALL_SIGN and friends. Because of the trailing space,
    even WHERE SDN_TYPE='-0-' returns ZERO rows -- you MUST trim first. We route
    every such column through clean_ofac_token() (trims, then nulls '' and '-0-').

    After cleaning SDN_TYPE, a NULL means the row is a sanctioned ORGANIZATION
    (the 9,785 '-0-' rows -- banks/airlines/trading cos like BANCO NACIONAL DE
    CUBA). The populated values are 'individual' / 'vessel' / 'aircraft'. So
    entity_kind = coalesce(cleaned sdn_type, 'organization').
#}

with source as (

    select * from {{ source('ripple_raw', 'FED_OFAC_SDN') }}

),

renamed_cast as (

    select

        -- identifiers (ENT_NUM is the SDN entity number; verified unique).
        -- nullif drops the one blank trailer row (ENT_NUM='' ) at the final filter.
        nullif(trim(ENT_NUM), '')                           as ent_num,
        trim(SDN_NAME)                                      as sdn_name,

        -- entity type: '-0- ' null token cleaned; null => organization
        {{ clean_ofac_token('SDN_TYPE') }}                  as sdn_type,
        coalesce({{ clean_ofac_token('SDN_TYPE') }}, 'organization') as entity_kind,

        -- program (sanctions program code, may be pipe-delimited list)
        {{ clean_ofac_token('PROGRAM') }}                   as program,

        -- individual attributes
        {{ clean_ofac_token('TITLE') }}                     as title,

        -- vessel / aircraft attributes (all '-0- '-laden)
        {{ clean_ofac_token('CALL_SIGN') }}                 as call_sign,
        {{ clean_ofac_token('VESS_TYPE') }}                 as vessel_type,
        try_to_double({{ clean_ofac_token('TONNAGE') }})    as tonnage,
        try_to_double({{ clean_ofac_token('GRT') }})        as gross_registered_tonnage,
        {{ clean_ofac_token('VESS_FLAG') }}                 as vessel_flag,
        {{ clean_ofac_token('VESS_OWNER') }}                as vessel_owner,
        {{ normalize_imo('IMO') }}                          as imo_number,

        -- free text
        {{ clean_ofac_token('REMARKS') }}                   as remarks,

        -- pipeline audit columns (_INGESTED_AT lands as micro-epoch NUMBER)
        to_timestamp_ntz(_INGESTED_AT, 6)                   as _ingested_at,
        nullif(trim(try_cast(_SOURCE_RUN_ID as text)), '')  as _source_run_id

    from source

),

deduped as (

    select
        *,
        row_number() over (
            partition by ent_num
            order by _ingested_at desc nulls last
        ) as _row_num
    from renamed_cast

)

select * exclude (_row_num)
from deduped
where _row_num = 1
  and ent_num is not null   -- drop the single blank/trailer row
