{{ config(materialized='table') }}

/*
  governance__fed_revolvingdoor_project
  ─────────────────────────────────────
  Analytics-ready, wide (one row per unique personnel position) table derived
  from the Revolving Door Project personnel map.  Key identifiers are surfaced
  as top-level columns to support cross-source joins in the governance domain.
*/

with stg as (

    select * from {{ ref('stg_fed_revolvingdoor_project__personnel_positions') }}

),

final as (

    select

        -- ── primary key ──────────────────────────────────────────────────────
        position_key,

        -- ── key identifiers (required for cross-source joins) ─────────────
        person_name,
        agency,
        industry_sector,

        -- ── position attributes ───────────────────────────────────────────
        position_type,
        position_name,
        position_department,
        position_description,

        -- ── sector / interest pairs (wide form retained for BI tools) ─────
        sector1,           sector1_interest,
        sector2,           sector2_interest,
        sector3,           sector3_interest,
        sector4,           sector4_interest,
        sector5,           sector5_interest,
        sector6,           sector6_interest,
        sector7,           sector7_interest,
        sector8,           sector8_interest,
        sector9,           sector9_interest,
        sector10,          sector10_interest,
        sector11,          sector11_interest,
        sector12,          sector12_interest,
        sector14,          sector14_interest,
        sector14_1,        sector14_interest_1,
        sector15,          sector15_interest,
        sector16,          sector16_interest,

        -- ── count of non-null sectors per position ────────────────────────
        (
            case when sector1  is not null and sector1  != '' then 1 else 0 end +
            case when sector2  is not null and sector2  != '' then 1 else 0 end +
            case when sector3  is not null and sector3  != '' then 1 else 0 end +
            case when sector4  is not null and sector4  != '' then 1 else 0 end +
            case when sector5  is not null and sector5  != '' then 1 else 0 end +
            case when sector6  is not null and sector6  != '' then 1 else 0 end +
            case when sector7  is not null and sector7  != '' then 1 else 0 end +
            case when sector8  is not null and sector8  != '' then 1 else 0 end +
            case when sector9  is not null and sector9  != '' then 1 else 0 end +
            case when sector10 is not null and sector10 != '' then 1 else 0 end +
            case when sector11 is not null and sector11 != '' then 1 else 0 end +
            case when sector12 is not null and sector12 != '' then 1 else 0 end +
            case when sector14 is not null and sector14 != '' then 1 else 0 end +
            case when sector14_1 is not null and sector14_1 != '' then 1 else 0 end +
            case when sector15 is not null and sector15 != '' then 1 else 0 end +
            case when sector16 is not null and sector16 != '' then 1 else 0 end
        )                                                    as sector_count,

        -- ── boolean convenience flags ──────────────────────────────────────
        case
            when lower(position_type) in ('appointee', 'political appointee')
            then true else false
        end                                                  as is_political_appointee,

        case
            when lower(position_type) like '%revolv%'
            then true else false
        end                                                  as is_revolving_door,

        -- ── metadata ──────────────────────────────────────────────────────
        _ingested_at,
        _source_run_id,

        -- ── source attribution ────────────────────────────────────────────
        'fed_revolvingdoor_project'                          as _source_id

    from stg

)

select * from final
