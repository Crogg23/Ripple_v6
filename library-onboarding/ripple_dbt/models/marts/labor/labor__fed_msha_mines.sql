{{ config(materialized='table', schema='LABOR') }}

-- GRAIN: one row per mine (mine_id is unique)
-- Answers: Where is every regulated mine in the US, who operates it, and what type?
-- Source: MSHA Mines (~92K records)
-- Key joins: mine_id â†’ msha_violations/accidents; fips_cnty_cd â†’ geography

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
    try_to_number(no_employees)                     as no_employees,
    try_to_number(days_per_week)                    as days_per_week,
    try_to_number(hours_per_shift)                  as hours_per_shift,
    try_to_double(latitude)                         as latitude,
    try_to_double(longitude)                        as longitude,
    nearest_town,
    (current_mine_status = 'Active') as is_active,
    _loaded_at
from {{ ref('stg_fed_msha_mines__records') }}
qualify row_number() over (partition by mine_id order by _loaded_at desc) = 1
