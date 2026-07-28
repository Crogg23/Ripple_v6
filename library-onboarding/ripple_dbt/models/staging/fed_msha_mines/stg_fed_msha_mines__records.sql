{{ config(tags=['minimal_staging']) }}

-- GRAIN: one row per mine (mine_id)
-- Fix: strip embedded quote characters from MSHA pipe-delimited source.

with source as (

    select * from {{ source('ripple_raw', 'FED_MSHA_MINES') }}

),

cleaned as (

    select
        {{ strip_quotes('MINE_ID') }}                   as mine_id,
        {{ strip_quotes('CURRENT_MINE_NAME') }}         as current_mine_name,
        {{ strip_quotes('COAL_METAL_IND') }}            as coal_metal_ind,
        {{ strip_quotes('CURRENT_MINE_TYPE') }}         as current_mine_type,
        {{ strip_quotes('CURRENT_MINE_STATUS') }}       as current_mine_status,
        {{ strip_quotes('CURRENT_STATUS_DT') }}         as current_status_dt,
        {{ strip_quotes('CURRENT_CONTROLLER_ID') }}     as current_controller_id,
        {{ strip_quotes('CURRENT_CONTROLLER_NAME') }}   as current_controller_name,
        {{ strip_quotes('CURRENT_OPERATOR_ID') }}       as current_operator_id,
        {{ strip_quotes('CURRENT_OPERATOR_NAME') }}     as current_operator_name,
        {{ strip_quotes('STATE') }}                     as state,
        {{ strip_quotes('BOM_STATE_CD') }}              as bom_state_cd,
        {{ strip_quotes('FIPS_CNTY_CD') }}              as fips_cnty_cd,
        {{ strip_quotes('FIPS_CNTY_NM') }}              as fips_cnty_nm,
        {{ strip_quotes('CONG_DIST_CD') }}              as cong_dist_cd,
        {{ strip_quotes('COMPANY_TYPE') }}              as company_type,
        {{ strip_quotes('CURRENT_CONTROLLER_BEGIN_DT') }} as current_controller_begin_dt,
        {{ strip_quotes('DISTRICT') }}                  as district,
        {{ strip_quotes('OFFICE_CD') }}                 as office_cd,
        {{ strip_quotes('OFFICE_NAME') }}               as office_name,
        {{ strip_quotes('ASSESS_CTRL_NO') }}            as assess_ctrl_no,
        {{ strip_quotes('PRIMARY_SIC_CD') }}            as primary_sic_cd,
        {{ strip_quotes('PRIMARY_SIC') }}               as primary_sic,
        {{ strip_quotes('PRIMARY_SIC_CD_1') }}          as primary_sic_cd_1,
        {{ strip_quotes('PRIMARY_SIC_CD_SFX') }}        as primary_sic_cd_sfx,
        {{ strip_quotes('SECONDARY_SIC_CD') }}          as secondary_sic_cd,
        {{ strip_quotes('SECONDARY_SIC') }}             as secondary_sic,
        {{ strip_quotes('SECONDARY_SIC_CD_1') }}        as secondary_sic_cd_1,
        {{ strip_quotes('SECONDARY_SIC_CD_SFX') }}      as secondary_sic_cd_sfx,
        {{ strip_quotes('PRIMARY_CANVASS_CD') }}        as primary_canvass_cd,
        {{ strip_quotes('PRIMARY_CANVASS') }}           as primary_canvass,
        {{ strip_quotes('SECONDARY_CANVASS_CD') }}      as secondary_canvass_cd,
        {{ strip_quotes('SECONDARY_CANVASS') }}         as secondary_canvass,
        {{ strip_quotes('CURRENT_103I') }}              as current_103i,
        {{ strip_quotes('CURRENT_103I_DT') }}           as current_103i_dt,
        {{ strip_quotes('PORTABLE_OPERATION') }}        as portable_operation,
        {{ strip_quotes('PORTABLE_FIPS_ST_CD') }}       as portable_fips_st_cd,
        {{ strip_quotes('DAYS_PER_WEEK') }}             as days_per_week,
        {{ strip_quotes('HOURS_PER_SHIFT') }}           as hours_per_shift,
        {{ strip_quotes('PROD_SHIFTS_PER_DAY') }}       as prod_shifts_per_day,
        {{ strip_quotes('MAINT_SHIFTS_PER_DAY') }}      as maint_shifts_per_day,
        {{ strip_quotes('NO_EMPLOYEES') }}              as no_employees,
        {{ strip_quotes('PART48_TRAINING') }}           as part48_training,
        {{ strip_quotes('LONGITUDE') }}                 as longitude,
        {{ strip_quotes('LATITUDE') }}                  as latitude,
        {{ strip_quotes('AVG_MINE_HEIGHT') }}           as avg_mine_height,
        {{ strip_quotes('MINE_GAS_CATEGORY_CD') }}      as mine_gas_category_cd,
        {{ strip_quotes('METHANE_LIBERATION') }}        as methane_liberation,
        {{ strip_quotes('NO_PRODUCING_PITS') }}         as no_producing_pits,
        {{ strip_quotes('NO_NONPRODUCING_PITS') }}      as no_nonproducing_pits,
        {{ strip_quotes('NO_TAILING_PONDS') }}          as no_tailing_ponds,
        {{ strip_quotes('PILLAR_RECOVERY_USED') }}      as pillar_recovery_used,
        {{ strip_quotes('HIGHWALL_MINER_USED') }}       as highwall_miner_used,
        {{ strip_quotes('MULTIPLE_PITS') }}             as multiple_pits,
        {{ strip_quotes('MINERS_REP_IND') }}            as miners_rep_ind,
        {{ strip_quotes('SAFETY_COMMITTEE_IND') }}      as safety_committee_ind,
        {{ strip_quotes('MILES_FROM_OFFICE') }}         as miles_from_office,
        {{ strip_quotes('DIRECTIONS_TO_MINE') }}        as directions_to_mine,
        {{ strip_quotes('NEAREST_TOWN') }}              as nearest_town,
        _INGESTED_AT                                    as _loaded_at,
        'https://arlweb.msha.gov/opengovernmentdata/DataSets/Mines.zip' as _source_url

    from source

)

select * from cleaned
