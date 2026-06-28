{{ config(materialized='table') }}

-- ============================================================================
-- health__pharma_meal_cap_fingerprint
-- ----------------------------------------------------------------------------
-- The "meal-cap fingerprint": manufacturer-level share of Food & Beverage
-- transfers priced JUST BELOW the $125 sunshine-disclosure / per-meal cap.
--
-- The signal (discovery sweep 2026-06-27, findings #8 / #40 / #75):
--   Open Payments Food & Beverage transfers cluster HARD one cent under $125.
--   $124.99 alone shows up 20,733 times in 2024 (19,883 in 2023), and payments
--   in the just-BELOW band [124.00, 124.99] outnumber the just-ABOVE band
--   (125.00, 126.00] by roughly 4-10x, industry-wide. A meal priced at $124.99
--   is a meal priced to sit under a cap -- the manufacturers that do it the
--   most have a measurable behavioural fingerprint.
--
-- This mart turns that into a panel: one row per manufacturer per program year,
-- with the meal-cap SHARE (how much of their F&B spend hugs the cap) and the
-- CLIFF RATIO (just-below vs just-above). High share + high cliff = a payer
-- systematically pricing meals to clear the threshold.
--
-- Grain: one row = one (payment-making manufacturer/GPO) x (program year).
-- Source: int_open_payments_all_years (Open Payments 2023 + 2024 union).
-- Filter: NATURE_OF_PAYMENT_OR_TRANSFER_OF_VALUE = 'Food and Beverage'.
-- Volume floor: only manufacturers with >= 100 F&B payments in the year are
--   kept -- below that, the share is statistical noise.
-- ============================================================================

with

fb as (

    select
        nullif(trim(applicable_manufacturer_or_applicable_gpo_making_payment_name), '')
            as payment_maker_name,
        applicable_manufacturer_or_applicable_gpo_making_payment_id
            as payment_maker_id,
        try_to_number(program_year)                            as program_year,
        try_to_double(total_amount_of_payment_usdollars)       as amount_usd
    from {{ ref('int_open_payments_all_years') }}
    where nature_of_payment_or_transfer_of_value = 'Food and Beverage'

),

filtered as (

    -- keep only rows we can actually attribute and price
    select *
    from fb
    where payment_maker_name is not null
      and program_year is not null
      and amount_usd is not null

),

agg as (

    select

        payment_maker_name,
        -- a single representative id per maker-year (ids are stable per maker)
        min(payment_maker_id)                                  as payment_maker_id,
        program_year,

        -- ---------------------------------------------------------------
        -- Volume + dollars
        -- ---------------------------------------------------------------
        count(*)                                               as total_fb_payments,
        round(sum(amount_usd), 2)                              as total_fb_amount_usd,
        round(avg(amount_usd), 2)                              as avg_fb_amount_usd,
        round(median(amount_usd), 2)                           as median_fb_amount_usd,

        -- ---------------------------------------------------------------
        -- The meal-cap fingerprint bands
        --   meal_cap     : F&B payments in [124.00, 124.99]  (just BELOW $125)
        --   exactly_12499: F&B payments at exactly $124.99   (the spike itself)
        --   just_above   : F&B payments in (125.00, 126.00]  (just ABOVE $125)
        -- ---------------------------------------------------------------
        count_if(amount_usd between 124.00 and 124.99)         as n_meal_cap,
        count_if(amount_usd = 124.99)                          as n_exactly_124_99,
        count_if(amount_usd > 125.00 and amount_usd <= 126.00) as n_just_above,
        count_if(amount_usd = 125.00)                          as n_exactly_125_00

    from filtered
    group by 1, 3

),

final as (

    select

        -- ---------------------------------------------------------------
        -- Grain key (one row = one manufacturer x program year)
        -- ---------------------------------------------------------------
        {{ dbt_utils.generate_surrogate_key(['payment_maker_name', 'program_year']) }}
                                                               as meal_cap_key,
        payment_maker_name,
        payment_maker_id,
        program_year,

        -- ---------------------------------------------------------------
        -- Food & Beverage footprint
        -- ---------------------------------------------------------------
        total_fb_payments,
        total_fb_amount_usd,
        avg_fb_amount_usd,
        median_fb_amount_usd,

        -- ---------------------------------------------------------------
        -- Meal-cap fingerprint counts
        -- ---------------------------------------------------------------
        n_meal_cap,
        n_exactly_124_99,
        n_just_above,
        n_exactly_125_00,

        -- ---------------------------------------------------------------
        -- Fingerprint metrics
        --   meal_cap_share : fraction of this maker's F&B spend that hugs the
        --                    cap (just below $125). The headline ranking signal.
        --   cliff_ratio    : just-below / just-above. >1 means the maker prices
        --                    meals to clear the cap; industry-wide this runs
        --                    ~4-10x. null when there is nothing just above.
        -- ---------------------------------------------------------------
        round(n_meal_cap / total_fb_payments, 6)               as meal_cap_share,
        round(n_meal_cap / nullif(n_just_above, 0), 4)         as cliff_ratio,
        round(n_exactly_124_99 / total_fb_payments, 6)         as exactly_124_99_share,

        -- ---------------------------------------------------------------
        -- Convenience flag: pronounced fingerprint
        --   >= 2% of F&B spend at the cap AND a real cliff (>= 3x just-above,
        --   or nothing just-above at all while still hitting the cap).
        -- ---------------------------------------------------------------
        case
            when n_meal_cap / total_fb_payments >= 0.02
             and (n_just_above = 0 or n_meal_cap / nullif(n_just_above, 0) >= 3)
            then true
            else false
        end                                                    as is_pronounced_fingerprint

    from agg
    -- volume floor: below 100 F&B payments the share is noise
    where total_fb_payments >= 100

)

select * from final
