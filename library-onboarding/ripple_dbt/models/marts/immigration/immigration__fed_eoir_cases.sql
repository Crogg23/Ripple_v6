{{ config(materialized='table', schema='IMMIGRATION') }}

-- One row per immigration court case (A_tblCase), typed. 12.6M rows.
-- Source: stg_fed_eoir__cases, the 39-way split of the one-column landing table.
-- No judge: that column is in B_TblProceeding, never landed. See the staging model.

with s as (
    select * from {{ ref('stg_fed_eoir__cases') }}
)

select
    try_to_number(idncase)                              as case_id,
    update_site                                         as court_code,
    custody                                             as custody,
    case custody
        when 'N' then 'never detained'
        when 'D' then 'detained'
        when 'R' then 'released'
    end                                                 as custody_label,
    case_type                                           as case_type,
    nat                                                 as nationality,
    lang                                                as language,
    gender                                              as gender,
    try_to_timestamp_ntz(latest_hearing)                as latest_hearing_at,
    latest_time                                         as latest_hearing_time,
    latest_cal_type                                     as latest_hearing_calendar_type,
    try_to_timestamp_ntz(date_of_entry)                 as date_of_entry,
    try_to_timestamp_ntz(date_detained)                 as date_detained,
    try_to_timestamp_ntz(date_released)                 as date_released,
    try_to_timestamp_ntz(c_release_date)                as earliest_possible_release_date,
    try_to_timestamp_ntz(detention_date)                as detention_facility_entered_at,
    c_asy_type                                          as asylum_clock_type,
    c_birthdate                                         as birth_month_year,
    case lpr when '1' then true when '0' then false end as is_lpr,
    correctional_fac                                    as correctional_facility_code,
    inmate_housing                                      as inmate_housing_code,
    detention_location                                  as detention_location,
    dco_location                                        as detention_location_address,
    detention_facility_type                             as detention_facility_type,
    casepriority_code                                   as case_priority_code,
    alien_city,
    alien_state,
    alien_zipcode,
    updated_city,
    updated_state,
    updated_zipcode,
    try_to_timestamp_ntz(address_changedon)             as address_changed_at,
    site_type                                           as hearing_notice_type,
    atty_nbr                                            as attorney_count_legacy,
    field_count,
    _loaded_at,
    _source_run_id,
    'fed_eoir_case_data'                                as source_id
from s
