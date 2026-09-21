{{ config(materialized='table', schema='LABOR') }}

-- GRAIN: one row per mine (mine_id is unique)
-- Answers: Where is every regulated mine in the US, who operates it, and what type?
-- Source: MSHA Mines (~92K records)
-- Key joins: mine_id â†’ msha_violations/accidents; fips_cnty_cd â†’ geography
--
-- KEY RE-PROOF (2026-09-20 -- same hole f41ebff9 closed in staging: 289 views
-- deduped on a key proven unique ONCE, at generation time, that silently stopped
-- identifying a row after a reload while `unique` stayed green forever, because
-- the test only ever checked the ALREADY-DEDUPED output). key_proof below re-runs
-- scripts/generate_staging_models.py's key_is_unique_within_each_load() math live,
-- every build: COUNT(*) vs COUNT(DISTINCT HASH(mine_id)), grouped by
-- _SOURCE_RUN_ID when that column is a genuine load id (>= 100 rows/run average --
-- some CMS tables stamp a per-ROW uuid there instead, which would make ANY key
-- "prove" unique; MIN_ROWS_PER_LOAD=100 mirrors the generator exactly). The
-- staging ref this model reads from is a pure strip-quotes passthrough (no
-- filter, no dedup), so this checks the LANDING table directly -- same row set,
-- and the only place _SOURCE_RUN_ID survives (the staging passthrough drops it).
-- Live-verified 2026-09-20: 91,906 rows, 91,906 distinct MINE_ID, 1 load to date,
-- zero collision -- proven, so the QUALIFY below partitions by mine_id alone. If
-- a future reload ever breaks that, would_collapse > 0 and the SAME QUALIFY
-- automatically falls back to a whole-row partition (every data column, so only
-- exact copies collapse) -- schema.yml's `unique` test should be dropped the day
-- this ever shows would_collapse > 0.

with key_load_shape as (

    select count(*) as total_rows, count(distinct _SOURCE_RUN_ID) as n_runs
    from {{ source('ripple_raw', 'FED_MSHA_MINES') }}

),

key_proof as (

    select coalesce(sum(n - d), 0) as would_collapse
    from (
        select
            case when ls.n_runs > 0 and ls.total_rows / ls.n_runs >= 100
                 then s._SOURCE_RUN_ID else '__ALL__' end    as _load_id,
            count(*)                                          as n,
            count(distinct hash(s.MINE_ID))                   as d
        from {{ source('ripple_raw', 'FED_MSHA_MINES') }} s
        cross join key_load_shape ls
        group by 1
    )

),

renamed as (

    select
        mine_id,
        current_mine_name,
        coal_metal_ind,
        current_mine_type,
        current_mine_status,
        try_to_date(current_status_dt, 'MM/DD/YYYY')   as current_status_dt,
        current_controller_id,
        current_controller_name,
        current_operator_id,
        current_operator_name,
        state,
        fips_cnty_cd,
        fips_cnty_nm,
        primary_sic_cd,
        primary_sic,
        {{ stg_int('no_employees') }}                     as no_employees,
        {{ stg_int('days_per_week') }}                    as days_per_week,
        {{ stg_int('hours_per_shift') }}                  as hours_per_shift,
        {{ stg_float('latitude') }}                         as latitude,
        {{ stg_float('longitude') }}                        as longitude,
        nearest_town,
        (current_mine_status = 'Active') as is_active,
        _loaded_at
    from {{ ref('stg_fed_msha_mines__records') }}

)

select
    r.mine_id, r.current_mine_name, r.coal_metal_ind, r.current_mine_type,
    r.current_mine_status, r.current_status_dt, r.current_controller_id,
    r.current_controller_name, r.current_operator_id, r.current_operator_name,
    r.state, r.fips_cnty_cd, r.fips_cnty_nm, r.primary_sic_cd, r.primary_sic,
    r.no_employees, r.days_per_week, r.hours_per_shift, r.latitude, r.longitude,
    r.nearest_town, r.is_active, r._loaded_at
from renamed r
cross join key_proof kp
-- partition: mine_id is unconditional; every other column only engages (goes
-- non-null) when kp.would_collapse != 0, i.e. the key is NOT proven -- at that
-- point this IS a whole-row partition, same shape as
-- generate_staging_models.py's fallback.
qualify row_number() over (partition by
             r.mine_id,
             case when kp.would_collapse != 0 then r.current_mine_name else null end,
             case when kp.would_collapse != 0 then r.coal_metal_ind else null end,
             case when kp.would_collapse != 0 then r.current_mine_type else null end,
             case when kp.would_collapse != 0 then r.current_mine_status else null end,
             case when kp.would_collapse != 0 then r.current_status_dt else null end,
             case when kp.would_collapse != 0 then r.current_controller_id else null end,
             case when kp.would_collapse != 0 then r.current_controller_name else null end,
             case when kp.would_collapse != 0 then r.current_operator_id else null end,
             case when kp.would_collapse != 0 then r.current_operator_name else null end,
             case when kp.would_collapse != 0 then r.state else null end,
             case when kp.would_collapse != 0 then r.fips_cnty_cd else null end,
             case when kp.would_collapse != 0 then r.fips_cnty_nm else null end,
             case when kp.would_collapse != 0 then r.primary_sic_cd else null end,
             case when kp.would_collapse != 0 then r.primary_sic else null end,
             case when kp.would_collapse != 0 then r.no_employees else null end,
             case when kp.would_collapse != 0 then r.days_per_week else null end,
             case when kp.would_collapse != 0 then r.hours_per_shift else null end,
             case when kp.would_collapse != 0 then r.latitude else null end,
             case when kp.would_collapse != 0 then r.longitude else null end,
             case when kp.would_collapse != 0 then r.nearest_town else null end
             order by r._loaded_at desc,
             -- tie-breakers 2026-09-18: the row's own values, so the same row wins every run
             r.current_mine_name nulls last, r.coal_metal_ind nulls last, r.current_mine_type nulls last,
             r.current_mine_status nulls last, r.current_status_dt nulls last,
             r.current_controller_id nulls last, r.current_controller_name nulls last,
             r.current_operator_id nulls last, r.current_operator_name nulls last, r.state nulls last,
             r.fips_cnty_cd nulls last, r.fips_cnty_nm nulls last, r.primary_sic_cd nulls last,
             r.primary_sic nulls last, r.no_employees nulls last, r.days_per_week nulls last,
             r.hours_per_shift nulls last, r.latitude nulls last, r.longitude nulls last,
             r.nearest_town nulls last
) = 1
