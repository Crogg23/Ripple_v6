{{ config(materialized='view') }}

with

source as (

    select * from {{ source('ripple_raw', 'UK_COMPANIES_HOUSE_PSC') }}

),

renamed as (

    select

        -- identifiers
        trim(LINK_SELF)                                as psc_link_self,
        trim(COMPANY_NUMBER)                           as company_number,
        trim(ETAG)                                     as etag,

        -- dimensions
        trim(KIND)                                     as kind,
        trim(NAME)                                     as name,
        trim(NAME_TITLE)                               as name_title,
        trim(NAME_FORENAME)                            as name_forename,
        trim(NAME_MIDDLE)                              as name_middle,
        trim(NAME_SURNAME)                             as name_surname,
        trim(NATIONALITY)                              as nationality,
        trim(COUNTRY_OF_RESIDENCE)                     as country_of_residence,
        try_to_number(trim(DOB_MONTH))                 as dob_month,
        try_to_number(trim(DOB_YEAR))                  as dob_year,
        trim(ADDRESS_PREMISES)                         as address_premises,
        trim(ADDRESS_LINE_1)                           as address_line_1,
        trim(ADDRESS_LOCALITY)                         as address_locality,
        trim(ADDRESS_POSTAL_CODE)                      as address_postal_code,
        trim(ADDRESS_COUNTRY)                          as address_country,
        trim(REGISTRATION_NUMBER)                      as registration_number,
        trim(LEGAL_FORM)                               as legal_form,
        trim(COUNTRY_REGISTERED)                       as country_registered,
        trim(NATURES_OF_CONTROL)                       as natures_of_control,
        try_to_date(trim(NOTIFIED_ON))                 as notified_on,
        try_to_date(trim(CEASED_ON))                   as ceased_on,

        -- metadata
        _ingested_at,
        _source_run_id,
        _src_sha256

    from source

),

deduped as (

    select *,
        row_number() over (
            partition by psc_link_self
            order by _ingested_at desc
        ) as _row_num
    from renamed
    where psc_link_self is not null

)

select
    psc_link_self,
    company_number,
    etag,
    kind,
    name,
    name_title,
    name_forename,
    name_middle,
    name_surname,
    nationality,
    country_of_residence,
    dob_month,
    dob_year,
    address_premises,
    address_line_1,
    address_locality,
    address_postal_code,
    address_country,
    registration_number,
    legal_form,
    country_registered,
    natures_of_control,
    notified_on,
    ceased_on,
    _ingested_at,
    _source_run_id,
    _src_sha256
from deduped
where _row_num = 1
