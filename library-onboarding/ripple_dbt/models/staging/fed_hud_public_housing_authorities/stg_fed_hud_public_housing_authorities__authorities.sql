{{ config(materialized='view') }}

with

source as (

    select * from {{ source('ripple_raw', 'FED_HUD_PUBLIC_HOUSING_AUTHORITIES') }}

),

renamed as (

    select

        -- identifiers
        trim(PARTICIPANT_CODE)                          as participant_code,
        try_to_number(trim(OBJECTID))                   as objectid,
        trim(FORMAL_PARTICIPANT_NAME)                   as formal_participant_name,

        -- contact
        trim(HA_PHN_NUM)                                as ha_phone_number,
        trim(HA_FAX_NUM)                                as ha_fax_number,
        trim(HA_EMAIL_ADDR_TEXT)                        as ha_email_address,
        trim(EXEC_DIR_PHONE)                            as exec_dir_phone,
        trim(EXEC_DIR_FAX)                              as exec_dir_fax,
        trim(EXEC_DIR_EMAIL)                            as exec_dir_email,

        -- classification
        trim(PHAS_DESIGNATION)                          as phas_designation,
        trim(HA_LOW_RENT_SIZE_CATEGORY)                 as ha_low_rent_size_category,
        trim(HA_SECTION_8_SIZE_CATEGORY)                as ha_section_8_size_category,
        trim(HA_COMBINED_SIZE_CATEGORY)                 as ha_combined_size_category,
        trim(HA_FYE)                                    as ha_fiscal_year_end,
        trim(HA_PROGRAM_TYPE)                           as ha_program_type,

        -- units / occupancy
        try_to_number(trim(SECTION8_UNITS_CNT))         as section8_units_count,
        try_to_number(trim(TOTAL_UNITS))                as total_units,
        try_to_number(trim(TOTAL_DWELLING_UNITS))       as total_dwelling_units,
        try_to_number(trim(ACC_UNITS))                  as acc_units,
        try_to_number(trim(PH_OCCUPIED))                as public_housing_occupied,
        try_to_number(trim(SECTION8_OCCUPIED))          as section8_occupied,
        try_to_number(trim(TOTAL_OCCUPIED))             as total_occupied,
        try_to_number(trim(PCT_OCCUPIED), 12, 4)        as pct_occupied,
        try_to_number(trim(REGULAR_VACANT))             as regular_vacant,
        try_to_number(trim(PHA_TOTAL_UNITS))            as pha_total_units,
        try_to_number(trim(NUMBER_REPORTED))            as number_reported,
        try_to_number(trim(PCT_REPORTED), 12, 4)        as pct_reported,

        -- funding / spending
        try_to_number(trim(OPFUND_AMNT))                as operating_fund_amount,
        try_to_number(trim(OPFUND_AMNT_PREV_YR))        as operating_fund_amount_prev_yr,
        try_to_number(trim(CAPFUND_AMNT))               as capital_fund_amount,
        try_to_number(trim(CAPFUND_AMNT_PREV_YR))       as capital_fund_amount_prev_yr,
        try_to_number(trim(ROSS_AMNT))                  as ross_amount,
        try_to_number(trim(FSS_AMNT))                   as fss_amount,
        try_to_number(trim(SPENDING_PER_MONTH))         as spending_per_month,
        try_to_number(trim(SPENDING_PER_MONTH_PREV_YR)) as spending_per_month_prev_yr,
        try_to_number(trim(ANNL_EXPNS_AMNT))            as annual_expense_amount,
        try_to_number(trim(ANNL_EXPNS_AMNT_PREV_YR))    as annual_expense_amount_prev_yr,

        -- resident demographics
        try_to_number(trim(CHLDRN_MBR_CNT))             as children_member_count,
        try_to_number(trim(ELDLY_PRCNT), 12, 4)         as elderly_percent,
        try_to_number(trim(PCT_DISABLED_LT62_ALL), 12, 4) as pct_disabled_lt62_all,
        try_to_number(trim(PCT_LT80_MEDIAN), 12, 4)     as pct_below_80pct_median_income,
        try_to_number(trim(MEDIAN_INC_AMNT))            as median_income_amount,

        -- census geography (2010/2020 geocode block)
        trim(STATE2KX)                                  as state_fips,
        trim(CNTY_NM2KX)                                as county_name,
        trim(CNTY2KX)                                   as county_fips,
        trim(TRACT2KX)                                  as census_tract,
        trim(BG2KX)                                     as block_group,
        trim(BLOCK2KX)                                  as census_block,
        DPVACT                                          as dpv_act,
        DPVNOST                                         as dpv_nost,
        trim(CURCNTY_NM)                                as current_county_name,
        trim(CURCNTY)                                   as current_county_fips,
        trim(CURCOSUB)                                  as current_county_subdivision,
        trim(CURCOSUB_NM)                               as current_county_subdivision_name,
        trim(PLACE2KX)                                  as place_fips,
        trim(PLACE_NM2KX)                               as place_name,
        PLACE_CC2KX                                     as place_class_code,
        PLACE_INC2KX                                    as place_incorporated_flag,
        trim(MSA)                                       as msa_code,
        trim(MSA_NM)                                    as msa_name,
        trim(CBSA)                                      as cbsa_code,
        trim(CBSA_NM)                                   as cbsa_name,
        trim(NECTA)                                     as necta_code,
        trim(NECTA_NM)                                  as necta_name,
        trim(METRO)                                     as metro_flag,
        trim(MICRO)                                     as micro_flag,
        trim(FCD_FIPS91)                                as fcd_fips91,
        trim(HLC)                                       as hlc_code,

        -- standardized address block
        trim(DPV)                                       as dpv_code,
        DPVRC                                           as dpv_return_code,
        trim(STD_ADDR)                                  as std_address,
        trim(URB_OUT)                                   as urbanization,
        trim(STD_CITY)                                  as std_city,
        trim(STD_ST)                                    as std_state,
        trim(STD_ZIP5)                                  as std_zip5,
        trim(STD_ZIP9)                                  as std_zip9,
        trim(ZIP_CLASS)                                 as zip_class,
        trim(ZCTA2KX)                                   as zcta,
        trim(DPBC)                                      as delivery_point_barcode,
        trim(DPBC_CKSUM)                                as delivery_point_barcode_checksum,
        trim(STD_ZIP11)                                 as std_zip11,
        trim(ADDR_TYPE)                                 as address_type,
        trim(APT_NO)                                    as apt_number,
        trim(APT_TYPE)                                  as apt_type,
        trim(C1PGRC)                                    as geocode_return_code,
        trim(C1PPRB)                                    as geocode_probability,
        trim(C1PDRC)                                    as geocode_drc,
        trim(C1PSRC)                                    as geocode_src,
        trim(C1PARC)                                    as geocode_arc,
        trim(C1PZRC)                                    as geocode_zrc,
        trim(MSGUSPS)                                   as usps_message,

        -- coordinates
        try_to_number(trim(X), 20, 10)                  as longitude,
        try_to_number(trim(Y), 20, 10)                  as latitude,
        try_to_number(trim(LAT), 20, 10)                as lat_geocoded,
        try_to_number(trim(LON), 20, 10)                as lon_geocoded,

        -- geocode quality
        trim(RC2KX)                                     as geocode_result_code,
        trim(STM2KX)                                    as geocode_match_type,
        trim(LVL2KX)                                    as geocode_level,
        trim(UR)                                        as urban_rural_flag,
        trim(MSG2KX)                                    as geocode_message,
        trim(COUNTY_LEVEL)                              as county_level_key,
        trim(PLACE_LEVEL)                               as place_level_key,
        trim(TRACT_LEVEL)                               as tract_level_key,
        trim(BLKGRP_LEVEL)                              as block_group_level_key,
        trim(UGLG_KEY)                                  as uglg_key,
        try_to_timestamp_ntz(trim(LAST_UPDT_DTTM), 'YYYY/MM/DD HH24:MI:SS+TZH') as last_updated_at,

        -- metadata
        to_timestamp_ntz(INGESTED_AT, 6)                as _ingested_at,
        SOURCE_RUN_ID                                   as _source_run_id,
        SRC_SHA256                                      as _src_sha256

    from source

),

deduped as (

    select *,
        row_number() over (
            partition by participant_code
            order by _ingested_at desc
        ) as _row_num
    from renamed
    where participant_code is not null

)

select * exclude _row_num
from deduped
where _row_num = 1
