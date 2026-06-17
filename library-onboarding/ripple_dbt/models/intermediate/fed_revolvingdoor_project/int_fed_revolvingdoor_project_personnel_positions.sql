{{ config(materialized='view') }}

/*
  Unpivot the wide sector/interest columns into a tidy long table so that
  downstream mart and analytics queries can filter/aggregate on any sector
  without referencing 30+ columns.  One row per (position_key, sector_slot).
*/

with stg as (

    select * from {{ ref('stg_fed_revolvingdoor_project__personnel_positions') }}

),

unpivoted as (

    select position_key, person_name, agency, industry_sector,
           position_type, position_name, position_department,
           position_description, _ingested_at, _source_run_id,
           sector_slot, sector_name, sector_interest
    from stg
    unpivot (
        (sector_name, sector_interest) for sector_slot in (
            (sector1,  sector1_interest)  as 'sector1',
            (sector2,  sector2_interest)  as 'sector2',
            (sector3,  sector3_interest)  as 'sector3',
            (sector4,  sector4_interest)  as 'sector4',
            (sector5,  sector5_interest)  as 'sector5',
            (sector6,  sector6_interest)  as 'sector6',
            (sector7,  sector7_interest)  as 'sector7',
            (sector8,  sector8_interest)  as 'sector8',
            (sector9,  sector9_interest)  as 'sector9',
            (sector10, sector10_interest) as 'sector10',
            (sector11, sector11_interest) as 'sector11',
            (sector12, sector12_interest) as 'sector12',
            (sector14, sector14_interest) as 'sector14',
            (sector14_1, sector14_interest_1) as 'sector14_1',
            (sector15, sector15_interest) as 'sector15',
            (sector16, sector16_interest) as 'sector16'
        )
    )

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
