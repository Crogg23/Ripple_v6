{{ config(materialized='view', tags=['spine_generated']) }}

-- GRAIN: one row per complaint (CMPLID is unique)
-- SPINE_ENTITY: not determined (consumer complaints, no direct entity link)
-- Source: NHTSA ODI Complaints — ~2.2M complaints since 1995
-- Key joins: mfr_name → manufacturer entities; VIN → vehicle; state → geography
-- Spec: https://static.nhtsa.gov/odi/ffdd/cmpl/CMPL.txt

with source as (
    select * from {{ source('ripple_raw', 'FED_NHTSA_COMPLAINTS') }}
),

renamed as (
    select
        trim(C1)                                as cmplid,
        trim(C2)                                as odino,
        trim(C3)                                as mfr_name,
        trim(C4)                                as maketxt,
        trim(C5)                                as modeltxt,
        trim(C6)                                as yeartxt,
        trim(C7)                                as crash,
        try_to_date(trim(C8), 'YYYYMMDD')       as fail_date,
        trim(C9)                                as fire,
        try_to_number(C10)                      as injured,
        try_to_number(C11)                      as deaths,
        trim(C12)                               as compdesc,
        trim(C13)                               as city,
        trim(C14)                               as state,
        trim(C15)                               as vin,
        try_to_date(trim(C16), 'YYYYMMDD')      as date_added,
        try_to_date(trim(C17), 'YYYYMMDD')      as date_received,
        try_to_number(C18)                      as miles,
        try_to_number(C19)                      as occurrences,
        C20                                     as cdescr,
        trim(C21)                               as cmpl_type,
        trim(C22)                               as police_rpt_yn,
        try_to_date(trim(C23), 'YYYYMMDD')      as purch_dt,
        trim(C24)                               as orig_owner_yn,
        trim(C25)                               as anti_brakes_yn,
        trim(C26)                               as cruise_cont_yn,
        try_to_number(C27)                      as num_cyls,
        trim(C28)                               as drive_train,
        trim(C29)                               as fuel_sys,
        trim(C30)                               as fuel_type,
        trim(C31)                               as trans_type,
        try_to_number(C32)                      as veh_speed,
        trim(C33)                               as dot,
        trim(C34)                               as tire_size,
        trim(C35)                               as loc_of_tire,
        trim(C36)                               as tire_fail_type,
        trim(C37)                               as orig_equip_yn,
        try_to_date(trim(C38), 'YYYYMMDD')      as manuf_dt,
        trim(C39)                               as seat_type,
        trim(C40)                               as restraint_type,
        trim(C41)                               as dealer_name,
        trim(C42)                               as dealer_tel,
        trim(C43)                               as dealer_city,
        trim(C44)                               as dealer_state,
        trim(C45)                               as dealer_zip,
        trim(C46)                               as prod_type,
        trim(C47)                               as repaired_yn,
        trim(C48)                               as medical_attn,
        trim(C49)                               as vehicles_towed_yn,
        trim(C50)                               as state_of_incident,
        trim(C51)                               as vehicle_operator,
        "_INGESTED_AT"                          as _loaded_at,
        "_SOURCE_RUN_ID"                        as _source_run_id
    from source
)

select * from renamed
qualify row_number() over (
    partition by cmplid
    order by _loaded_at desc
) = 1
