{{ config(materialized='table') }}

-- =====================================================================
-- money__debt_repayment_cliff
-- ---------------------------------------------------------------------
-- World Bank International Debt Statistics (IDS) carries REAL forward-
-- looking debt-service SCHEDULES out to 2032 -- contractual repayment
-- obligations already on the books, not estimates. (Discovery sweep
-- finding #25, 2026-06-27: ~12k numerically-valid future-year values
-- across TDS/AMT/INT debt-flow series, 134 countries+aggregates each.)
--
-- This mart isolates the three canonical TOTAL EXTERNAL-DEBT schedules
-- (World counterpart), unpivots the future-year columns to long, pivots
-- the three flow types side-by-side, and adds a year-over-year jump
-- signal -- the "repayment cliff finder".
--
--   TDS = DT.TDS.DECT.CD  Debt service on external debt, total
--   AMT = DT.AMT.DLXF.CD  Principal repayments on external debt, long-term
--   INT = DT.INT.DLXF.CD  Interest payments on external debt, long-term
--
-- Grain: one row per (country_code, data_year) for data_year >= 2026.
--        134 country/aggregate entities x 7 future years (2026-2032) = 938 rows.
--
-- NOTE on the entity set: the 134 entities include regional / income-group
-- AGGREGATES (e.g. "Low & middle income", "East Asia & Pacific", "IDA total")
-- alongside sovereigns. Use is_aggregate to filter to true countries. All
-- amounts are in current US dollars (CD series suffix).
-- =====================================================================

with

raw_ids as (

    select
        trim(country_name)  as country_name,
        trim(country_code)  as country_code,   -- trim: it is the cross-country ISO join key
        trim(series_code)   as series_code,
        c_2025,
        c_2026,
        c_2027,
        c_2028,
        c_2029,
        c_2030,
        c_2031,
        c_2032
    from {{ source('ripple_raw', 'INTL_WB_IDS') }}
    -- the three canonical TOTAL external-debt-service schedules, World counterpart
    where series_code in ('DT.TDS.DECT.CD', 'DT.AMT.DLXF.CD', 'DT.INT.DLXF.CD')
      and counterpart_area_code = 'WLD'

),

-- wide -> long: one row per (country, series, future year)
unpivoted as (

    select
        country_name,
        country_code,
        series_code,
        try_to_number(substr(year_col, 3, 4)) as data_year,
        try_to_double(year_value)             as value_usd
    from raw_ids
    unpivot (
        year_value for year_col in (
            c_2025, c_2026, c_2027, c_2028, c_2029, c_2030, c_2031, c_2032
        )
    )

),

-- long -> wide on flow type: TDS / principal / interest side-by-side per (country, year)
pivoted as (

    select
        country_name,
        country_code,
        data_year,
        max(case when series_code = 'DT.TDS.DECT.CD' then value_usd end) as total_debt_service_usd,
        max(case when series_code = 'DT.AMT.DLXF.CD' then value_usd end) as principal_repayment_usd,
        max(case when series_code = 'DT.INT.DLXF.CD' then value_usd end) as interest_payment_usd
    from unpivoted
    -- keep numerically-valid future-year values only (drops the blank/non-cast cells)
    where value_usd is not null
    group by 1, 2, 3

),

-- year-over-year jump: 2025 stays in scope only as the baseline for 2026
with_yoy as (

    select
        *,
        lag(total_debt_service_usd) over (
            partition by country_code order by data_year
        ) as prev_year_total_debt_service_usd
    from pivoted

),

final as (

    select

        -- -------------------------------------------------------
        -- Grain key (one row = one country-year debt-service schedule point)
        -- -------------------------------------------------------
        country_code || '_' || data_year       as country_year_id,     -- primary key
        country_code                            as country_code,        -- ISO-ish WB country/aggregate code (join key)
        country_name                            as country_name,
        data_year                               as data_year,           -- projection year (>= 2026)

        -- -------------------------------------------------------
        -- Forward-looking scheduled debt-service flows (current US$)
        -- -------------------------------------------------------
        total_debt_service_usd                  as total_debt_service_usd,   -- TDS = principal + interest
        principal_repayment_usd                 as principal_repayment_usd,  -- AMT
        interest_payment_usd                    as interest_payment_usd,     -- INT

        -- human-readable billions, rounded
        round(total_debt_service_usd / 1e9, 3)  as total_debt_service_usd_bn,
        round(principal_repayment_usd / 1e9, 3) as principal_repayment_usd_bn,
        round(interest_payment_usd / 1e9, 3)    as interest_payment_usd_bn,

        -- principal share of total service (bullet-repayment years skew high)
        case when total_debt_service_usd > 0
             then round(principal_repayment_usd / total_debt_service_usd, 4)
        end                                     as principal_share_of_service,

        -- -------------------------------------------------------
        -- Repayment-cliff signal (year-over-year jump in total service)
        -- -------------------------------------------------------
        prev_year_total_debt_service_usd                                      as prev_year_total_debt_service_usd,
        total_debt_service_usd - prev_year_total_debt_service_usd             as yoy_change_usd,
        case when prev_year_total_debt_service_usd > 0
             then round(
                    (total_debt_service_usd - prev_year_total_debt_service_usd)
                    / prev_year_total_debt_service_usd, 4)
        end                                                                   as yoy_change_pct,

        -- cliff flag: total service jumps >= 50% over the prior scheduled year
        case
            when prev_year_total_debt_service_usd > 0
                 and (total_debt_service_usd - prev_year_total_debt_service_usd)
                     / prev_year_total_debt_service_usd >= 0.50
            then true
            else false
        end                                                                   as is_repayment_cliff,

        -- is this the single peak debt-service year in the country's 2026-2032 window?
        case
            when total_debt_service_usd = max(total_debt_service_usd) over (
                     partition by country_code
                 )
            then true
            else false
        end                                                                   as is_peak_service_year,

        -- -------------------------------------------------------
        -- Convenience classifiers
        -- -------------------------------------------------------
        -- regional / income-group aggregates carry no 3-letter ISO sovereign code;
        -- WB aggregate codes are mostly non-ISO (e.g. LMY, EAP, IDA, OED, WLD)
        case
            when country_name ilike '%income%'
              or country_name ilike '%IDA%'
              or country_name ilike '%IBRD%'
              or country_name ilike '%excluding%'
              or country_name ilike '%& %'
              or country_name ilike '%developing%'
              or country_name ilike '%dividend%'
              or country_name ilike '%small states%'
              or country_name ilike '%Sub-Saharan%'
              or country_name ilike '%Middle East%'
              or country_name ilike '%Latin America%'
              or country_name ilike '%South Asia%'
              or country_name ilike '%Euro area%'
              or country_name ilike '%World%'
            then true
            else false
        end                                     as is_aggregate

    from with_yoy
    -- output horizon: future years only (2025 was carried solely as a YoY baseline)
    where data_year >= 2026

)

select * from final
