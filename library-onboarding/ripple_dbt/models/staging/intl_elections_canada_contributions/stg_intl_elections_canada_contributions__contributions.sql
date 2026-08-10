{{ config(materialized='view') }}

-- GRAIN: one row = one reported contribution line from an Elections Canada financial
-- return (all entity types: parties, candidates, leadership contestants, etc.).
-- No natural key: even the composite (recipient_id, form_id, contributor_name,
-- contribution_received_date, monetary_amount) is NOT unique (9,817,007 distinct of
-- 12,646,465 rows, verified) -- repeated identical lines are LEGITIMATE (multiple
-- identical installments, aggregated part rows). contribution_record_id is a
-- surrogate: md5 over all business columns + a row_number tiebreaker.
-- NOTE: this table's metadata columns have NO leading underscore in the source
-- (INGESTED_AT / SOURCE_RUN_ID / SRC_SHA256); renamed to house style here.

with source as (

    select * from {{ source('ripple_raw', 'INTL_ELECTIONS_CANADA_CONTRIBUTIONS') }}

),

renamed as (

    select

        -- recipient (the political entity receiving the contribution)
        trim(POLITICAL_ENTITY)                          as political_entity,
        trim(RECIPIENT_ID)                              as recipient_id,
        trim(RECIPIENT)                                 as recipient,
        trim(RECIPIENT_LAST_NAME)                       as recipient_last_name,
        trim(RECIPIENT_FIRST_NAME)                      as recipient_first_name,
        trim(RECIPIENT_MIDDLE_INITIAL)                  as recipient_middle_initial,
        trim(POLITICAL_PARTY_OF_RECIPIENT)              as political_party_of_recipient,
        trim(ELECTORAL_DISTRICT)                        as electoral_district,
        trim(ELECTORAL_EVENT)                           as electoral_event,
        try_to_date(trim(FISCAL_ELECTION_DATE))         as fiscal_election_date,

        -- return / form context
        trim(FORM_ID)                                   as form_id,
        trim(FINANCIAL_REPORT)                          as financial_report,
        trim(PART_NUMBER_OF_RETURN)                     as part_number_of_return,
        trim(FINANCIAL_REPORT_PART)                     as financial_report_part,

        -- contributor
        trim(CONTRIBUTOR_TYPE)                          as contributor_type,
        trim(CONTRIBUTOR_NAME)                          as contributor_name,
        trim(CONTRIBUTOR_LAST_NAME)                     as contributor_last_name,
        trim(CONTRIBUTOR_FIRST_NAME)                    as contributor_first_name,
        trim(CONTRIBUTOR_MIDDLE_INITIAL)                as contributor_middle_initial,
        trim(CONTRIBUTOR_CITY)                          as contributor_city,
        trim(CONTRIBUTOR_PROVINCE)                      as contributor_province,
        trim(CONTRIBUTOR_POSTAL_CODE)                   as contributor_postal_code,

        -- contribution
        try_to_date(trim(CONTRIBUTION_RECEIVED_DATE))   as contribution_received_date,
        try_to_number(trim(MONETARY_AMOUNT))            as monetary_amount,
        try_to_number(trim(NON_MONETARY_AMOUNT))        as non_monetary_amount,
        trim(CONTRIBUTION_GIVEN_THROUGH)                as contribution_given_through,
        trim(LEADERSHIP_CONTESTANT)                     as leadership_contestant,

        -- metadata (no leading underscore in the source columns for this table)
        to_timestamp_ntz(INGESTED_AT, 6)                as _ingested_at,
        SOURCE_RUN_ID                                   as _source_run_id,
        SRC_SHA256                                      as _src_sha256

    from source

),

hashed as (

    select *,
        md5(
            coalesce(political_entity, '')                                || '||' ||
            coalesce(recipient_id, '')                                    || '||' ||
            coalesce(recipient, '')                                       || '||' ||
            coalesce(recipient_last_name, '')                             || '||' ||
            coalesce(recipient_first_name, '')                            || '||' ||
            coalesce(recipient_middle_initial, '')                        || '||' ||
            coalesce(political_party_of_recipient, '')                    || '||' ||
            coalesce(electoral_district, '')                              || '||' ||
            coalesce(electoral_event, '')                                 || '||' ||
            coalesce(cast(fiscal_election_date as varchar), '')           || '||' ||
            coalesce(form_id, '')                                         || '||' ||
            coalesce(financial_report, '')                                || '||' ||
            coalesce(part_number_of_return, '')                           || '||' ||
            coalesce(financial_report_part, '')                           || '||' ||
            coalesce(contributor_type, '')                                || '||' ||
            coalesce(contributor_name, '')                                || '||' ||
            coalesce(contributor_last_name, '')                           || '||' ||
            coalesce(contributor_first_name, '')                          || '||' ||
            coalesce(contributor_middle_initial, '')                      || '||' ||
            coalesce(contributor_city, '')                                || '||' ||
            coalesce(contributor_province, '')                            || '||' ||
            coalesce(contributor_postal_code, '')                         || '||' ||
            coalesce(cast(contribution_received_date as varchar), '')     || '||' ||
            coalesce(cast(monetary_amount as varchar), '')                || '||' ||
            coalesce(cast(non_monetary_amount as varchar), '')            || '||' ||
            coalesce(contribution_given_through, '')                      || '||' ||
            coalesce(leadership_contestant, '')
        ) as _record_hash
    from renamed

),

keyed as (

    select *,
        _record_hash || '-' || row_number() over (
            partition by _record_hash
            order by 1
        ) as contribution_record_id
    from hashed

)

select * exclude (_record_hash)
from keyed
