{{ config(materialized='view') }}

with

source as (

    select * from {{ source('ripple_raw', 'FED_NCUA_FEDERALLY_INSURED_CU_LIST') }}

),

renamed as (

    select

        trim(CHARTER_NUMBER)                           as charter_number,
        trim(YEAR_AND_QUARTER)                         as year_and_quarter,
        trim(CREDIT_UNION_NAME)                        as credit_union_name,
        trim(STREET_MAILING_ADDRESS)                   as street_mailing_address,
        trim(CITY_MAILING_ADDRESS)                     as city_mailing_address,
        trim(STATE_MAILING_ADDRESS)                    as state_mailing_address,
        trim(ZIP_CODE_MAILING_ADDRESS)                 as zip_code_mailing_address,
        trim(CREDIT_UNION_TYPE)                        as credit_union_type,
        trim(NCUA_REGION)                              as ncua_region,
        trim(LOW_INCOME_DESIGNATION)                   as low_income_designation,
        try_to_number(trim(MEMBERS))                   as members,
        try_to_number(trim(TOTAL_ASSETS))              as total_assets,
        try_to_number(trim(TOTAL_LOANS))               as total_loans,
        try_to_number(trim(TOTAL_DEPOSITS))            as total_deposits,
        try_to_number(trim(RETURN_ON_AVERAGE_ASSETS))  as return_on_average_assets,
        try_to_number(trim(NET_WORTH_RATIO_EXCLUDES_CECL_TRANSITION_PROVISION)) as net_worth_ratio_excludes_cecl_transition_provision,
        try_to_number(trim(LOAN_TO_SHARE_RATIO))       as loan_to_share_ratio,
        try_to_number(trim(TOTAL_DEPOSITS_4_QUARTER_GROWTH)) as total_deposits_4_quarter_growth,
        try_to_number(trim(TOTAL_LOANS_4_QUARTER_GROWTH)) as total_loans_4_quarter_growth,
        try_to_number(trim(TOTAL_ASSETS_4_QUARTER_GROWTH)) as total_assets_4_quarter_growth,
        try_to_number(trim(MEMBERS_4_QUARTER_GROWTH))  as members_4_quarter_growth,
        try_to_number(trim(NET_WORTH_4_QUARTER_GROWTH_EXCLUDES_CECL_TRANSITION_PROVISION)) as net_worth_4_quarter_growth_excludes_cecl_transition_provision,
        try_to_number(trim(NCUA_INTERNAL_ID_JOIN_NUMBER)) as ncua_internal_id_join_number,
        INGESTED_AT                                    as _loaded_at,
        SOURCE_RUN_ID                                  as _source_run_id,
        SRC_SHA256                                     as _src_sha256

    from source

),

deduped as (

    select *,
        row_number() over (
            partition by charter_number
            order by _loaded_at desc
        ) as _row_num
    from renamed
    where charter_number is not null

)

select * exclude (_row_num) from deduped
where _row_num = 1
