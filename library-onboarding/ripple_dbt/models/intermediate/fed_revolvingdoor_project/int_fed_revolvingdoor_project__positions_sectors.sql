{{ config(materialized='view') }}

/*
  Unpivot the wide sector/interest columns into a tidy long table so that
  downstream mart and analytics queries can filter/aggregate on any sector
  without referencing 30+ columns.  One row per (position_key, sector_slot).

  Snowflake has no multi-column UNPIVOT, so we FLATTEN an array of one object
  per sector slot ({slot, name, interest}) and pull the pair back out.
*/

with stg as (

    select * from {{ ref('stg_fed_revolvingdoor_project__personnel_positions') }}

),

unpivoted as (

    select
        stg.position_key,
        stg.person_name,
        stg.agency,
        stg.industry_sector,
        stg.position_type,
        stg.position_name,
        stg.position_department,
        stg.position_description,
        stg._ingested_at,
        stg._source_run_id,
        f.value:slot::string     as sector_slot,
        f.value:name::string     as sector_name,
        f.value:interest::string as sector_interest
    from stg,
    lateral flatten(input => array_construct(
        object_construct_keep_null('slot', 'sector1',    'name', sector1,    'interest', sector1_interest),
        object_construct_keep_null('slot', 'sector2',    'name', sector2,    'interest', sector2_interest),
        object_construct_keep_null('slot', 'sector3',    'name', sector3,    'interest', sector3_interest),
        object_construct_keep_null('slot', 'sector4',    'name', sector4,    'interest', sector4_interest),
        object_construct_keep_null('slot', 'sector5',    'name', sector5,    'interest', sector5_interest),
        object_construct_keep_null('slot', 'sector6',    'name', sector6,    'interest', sector6_interest),
        object_construct_keep_null('slot', 'sector7',    'name', sector7,    'interest', sector7_interest),
        object_construct_keep_null('slot', 'sector8',    'name', sector8,    'interest', sector8_interest),
        object_construct_keep_null('slot', 'sector9',    'name', sector9,    'interest', sector9_interest),
        object_construct_keep_null('slot', 'sector10',   'name', sector10,   'interest', sector10_interest),
        object_construct_keep_null('slot', 'sector11',   'name', sector11,   'interest', sector11_interest),
        object_construct_keep_null('slot', 'sector12',   'name', sector12,   'interest', sector12_interest),
        object_construct_keep_null('slot', 'sector14',   'name', sector14,   'interest', sector14_interest),
        object_construct_keep_null('slot', 'sector14_1', 'name', sector14_1, 'interest', sector14_interest_1),
        object_construct_keep_null('slot', 'sector15',   'name', sector15,   'interest', sector15_interest),
        object_construct_keep_null('slot', 'sector16',   'name', sector16,   'interest', sector16_interest)
    )) f

)

select
    {{ dbt_utils.generate_surrogate_key(['position_key', 'sector_slot']) }} as position_sector_key,
    position_key,
    person_name,
    agency,
    industry_sector,
    position_type,
    position_name,
    position_department,
    position_description,
    sector_slot,
    nullif(trim(sector_name),    '') as sector_name,
    nullif(trim(sector_interest),'') as sector_interest,
    _ingested_at,
    _source_run_id
from unpivoted
where nullif(trim(sector_name), '') is not null
