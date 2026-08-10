{{ config(materialized='view') }}

/*
  Generated 2026-08-09 (73-source backlog, wave 2c) from live-verified specs.
  NTSB aviation accident database, events table: one row per accident/incident (ev_id unique) with location, weather, and injury totals.
  Grain: one row = one aviation event.
*/

with source as (
    select * from {{ source('ripple_raw', 'FED_NTSB_AVIATION_EVENTS') }}
),

renamed as (
    select
        nullif(trim(EV_ID), '')                                    as ev_id,
        nullif(trim(NTSB_NO), '')                                  as ntsb_no,
        nullif(trim(EV_TYPE), '')                                  as ev_type,
        try_to_date(left(nullif(trim(EV_DATE), ''), 10))           as ev_date,
        nullif(trim(EV_DOW), '')                                   as ev_dow,
        nullif(trim(EV_TIME), '')                                  as ev_time,
        nullif(trim(EV_TMZN), '')                                  as ev_tmzn,
        nullif(trim(EV_CITY), '')                                  as ev_city,
        nullif(trim(EV_STATE), '')                                 as ev_state,
        nullif(trim(EV_COUNTRY), '')                               as ev_country,
        nullif(trim(EV_SITE_ZIPCODE), '')                          as ev_site_zipcode,
        nullif(trim(EV_YEAR), '')                                  as ev_year,
        nullif(trim(EV_MONTH), '')                                 as ev_month,
        nullif(trim(MID_AIR), '')                                  as mid_air,
        nullif(trim(ON_GROUND_COLLISION), '')                      as on_ground_collision,
        nullif(trim(LATITUDE), '')                                 as latitude,
        nullif(trim(LONGITUDE), '')                                as longitude,
        nullif(trim(LATLONG_ACQ), '')                              as latlong_acq,
        nullif(trim(APT_NAME), '')                                 as apt_name,
        nullif(trim(EV_NR_APT_ID), '')                             as ev_nr_apt_id,
        nullif(trim(EV_NR_APT_LOC), '')                            as ev_nr_apt_loc,
        nullif(trim(APT_DIST), '')                                 as apt_dist,
        nullif(trim(APT_DIR), '')                                  as apt_dir,
        nullif(trim(APT_ELEV), '')                                 as apt_elev,
        nullif(trim(WX_BRIEF_COMP), '')                            as wx_brief_comp,
        nullif(trim(WX_SRC_IIC), '')                               as wx_src_iic,
        nullif(trim(WX_OBS_TIME), '')                              as wx_obs_time,
        nullif(trim(WX_OBS_DIR), '')                               as wx_obs_dir,
        nullif(trim(WX_OBS_FAC_ID), '')                            as wx_obs_fac_id,
        nullif(trim(WX_OBS_ELEV), '')                              as wx_obs_elev,
        nullif(trim(WX_OBS_DIST), '')                              as wx_obs_dist,
        nullif(trim(WX_OBS_TMZN), '')                              as wx_obs_tmzn,
        nullif(trim(LIGHT_COND), '')                               as light_cond,
        nullif(trim(SKY_COND_NONCEIL), '')                         as sky_cond_nonceil,
        nullif(trim(SKY_NONCEIL_HT), '')                           as sky_nonceil_ht,
        nullif(trim(SKY_CEIL_HT), '')                              as sky_ceil_ht,
        nullif(trim(SKY_COND_CEIL), '')                            as sky_cond_ceil,
        nullif(trim(VIS_RVR), '')                                  as vis_rvr,
        nullif(trim(VIS_RVV), '')                                  as vis_rvv,
        nullif(trim(VIS_SM), '')                                   as vis_sm,
        nullif(trim(WX_TEMP), '')                                  as wx_temp,
        nullif(trim(WX_DEW_PT), '')                                as wx_dew_pt,
        nullif(trim(WIND_DIR_DEG), '')                             as wind_dir_deg,
        nullif(trim(WIND_DIR_IND), '')                             as wind_dir_ind,
        nullif(trim(WIND_VEL_KTS), '')                             as wind_vel_kts,
        nullif(trim(WIND_VEL_IND), '')                             as wind_vel_ind,
        nullif(trim(GUST_IND), '')                                 as gust_ind,
        nullif(trim(GUST_KTS), '')                                 as gust_kts,
        nullif(trim(ALTIMETER), '')                                as altimeter,
        nullif(trim(WX_DENS_ALT), '')                              as wx_dens_alt,
        nullif(trim(WX_INT_PRECIP), '')                            as wx_int_precip,
        nullif(trim(METAR), '')                                    as metar,
        nullif(trim(EV_HIGHEST_INJURY), '')                        as ev_highest_injury,
        try_to_number(nullif(trim(INJ_F_GRND), ''), 18, 4)         as inj_f_grnd,
        try_to_number(nullif(trim(INJ_M_GRND), ''), 18, 4)         as inj_m_grnd,
        try_to_number(nullif(trim(INJ_S_GRND), ''), 18, 4)         as inj_s_grnd,
        try_to_number(nullif(trim(INJ_TOT_F), ''), 18, 4)          as inj_tot_f,
        try_to_number(nullif(trim(INJ_TOT_M), ''), 18, 4)          as inj_tot_m,
        try_to_number(nullif(trim(INJ_TOT_N), ''), 18, 4)          as inj_tot_n,
        try_to_number(nullif(trim(INJ_TOT_S), ''), 18, 4)          as inj_tot_s,
        try_to_number(nullif(trim(INJ_TOT_T), ''), 18, 4)          as inj_tot_t,
        nullif(trim(INVEST_AGY), '')                               as invest_agy,
        nullif(trim(NTSB_DOCKET), '')                              as ntsb_docket,
        nullif(trim(NTSB_NOTF_FROM), '')                           as ntsb_notf_from,
        try_to_date(left(nullif(trim(NTSB_NOTF_DATE), ''), 10))    as ntsb_notf_date,
        nullif(trim(NTSB_NOTF_TM), '')                             as ntsb_notf_tm,
        nullif(trim(FICHE_NUMBER), '')                             as fiche_number,
        try_to_date(left(nullif(trim(LCHG_DATE), ''), 10))         as lchg_date,
        nullif(trim(LCHG_USERID), '')                              as lchg_userid,
        nullif(trim(WX_COND_BASIC), '')                            as wx_cond_basic,
        nullif(trim(FAA_DIST_OFFICE), '')                          as faa_dist_office,
        try_to_number(nullif(trim(DEC_LATITUDE), ''), 18, 4)       as dec_latitude,
        try_to_number(nullif(trim(DEC_LONGITUDE), ''), 18, 4)      as dec_longitude,
        to_timestamp_ntz(INGESTED_AT, 6)                           as _ingested_at,
        nullif(trim(SOURCE_RUN_ID), '')                            as _source_run_id
    from source
)

select * from renamed
