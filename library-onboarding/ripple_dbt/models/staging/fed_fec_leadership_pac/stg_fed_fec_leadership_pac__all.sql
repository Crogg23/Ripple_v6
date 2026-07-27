    with source as (
        select * from {{ source('ripple_raw', 'FED_FEC_LEADERSHIP_PAC') }}
    )

    select
        "CAND_ID" as FEC_CANDIDATE_ID,
"CMTE_ID" as FEC_COMMITTEE_ID,
_INGESTED_AT,
_SOURCE_RUN_ID
    from source
    qualify row_number() over (
        partition by FEC_CANDIDATE_ID
        order by _INGESTED_AT desc
    ) = 1
