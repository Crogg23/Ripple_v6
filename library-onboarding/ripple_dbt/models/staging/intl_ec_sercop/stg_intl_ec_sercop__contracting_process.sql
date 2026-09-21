{{ config(materialized='view') }}

with source as (

    select * from {{ source('ripple_raw', 'INTL_EC_SERCOP') }}

),

renamed as (

    select

        -- key identifiers
        OCID                                                        as ocid,
        ID                                                          as id,
        TAG                                                         as tag,
        INITIATIONTYPE                                              as initiation_type,
        LANGUAGE                                                    as language,

        -- dates
        {{ stg_date('DATE') }}                                           as date,
        {{ stg_date('TENDER_DATEPUBLISHED') }}                           as tender_date_published,
        {{ stg_date('AWARD_DATE') }}                                     as award_date,
        {{ stg_date('CONTRACT_DATESIGNED') }}                            as contract_date_signed,

        -- buyer
        BUYER_ID                                                    as buyer_id,
        BUYER_NAME                                                  as buyer_name,

        -- tender
        TENDER_ID                                                   as tender_id,
        TENDER_TITLE                                                as tender_title,
        TENDER_STATUS                                               as tender_status,
        TENDER_PROCUREMENTMETHOD                                    as tender_procurement_method,
        {{ stg_float('TENDER_VALUE_AMOUNT') }}                          as tender_value_amount,
        TENDER_VALUE_CURRENCY                                       as tender_value_currency,

        -- award
        AWARD_ID                                                    as award_id,
        AWARD_STATUS                                                as award_status,
        {{ stg_float('AWARD_VALUE_AMOUNT') }}                           as award_value_amount,
        AWARD_VALUE_CURRENCY                                        as award_value_currency,

        -- supplier
        SUPPLIER_ID                                                 as supplier_id,
        SUPPLIER_NAME                                               as supplier_name,

        -- contract
        CONTRACT_ID                                                 as contract_id,
        {{ stg_float('CONTRACT_VALUE_AMOUNT') }}                        as contract_value_amount,
        CONTRACT_VALUE_CURRENCY                                     as contract_value_currency,

        -- parties
        PARTIES_ID                                                  as parties_id,
        PARTIES_NAME                                                as parties_name,
        PARTIES_ROLES                                               as parties_roles,

        -- planning
        {{ stg_float('PLANNING_BUDGET_AMOUNT') }}                       as planning_budget_amount,

        -- meta
        _ingested_at,
        _source_run_id

    from source

),

deduped as (

    select *,
        row_number() over (
            partition by ocid, id, tag
            order by _ingested_at desc
        ) as _row_num
    from renamed

)

select * exclude (_row_num)
from deduped
where _row_num = 1
