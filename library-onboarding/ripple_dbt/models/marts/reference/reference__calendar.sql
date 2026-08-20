{{ config(materialized='table', schema='REFERENCE') }}

-- The Ripple calendar. One row per day, 1700-01-01 through 2125-12-31, matching
-- the trusted window in macros/ripple_time.sql exactly (ripple_time_floor to
-- ripple_time_ceiling) so every canonical timestamp in the warehouse has a row
-- here to land on.
--
-- Grain: one row = one calendar day.
--
-- WHY A PHYSICAL TABLE (Snowflake can already do year()/date_trunc()):
--   1. GAPS. "Which months have no rows" is unanswerable from the fact table
--      alone -- a month with no events simply isn't there. Left-joining a dense
--      calendar is the only way to count silence, and silence (an agency that
--      stopped reporting) is a finding in its own right.
--   2. FISCAL YEARS. Federal money data runs on an Oct 1 start. Nothing computes
--      that for free.
--   3. RIPPLE-SPECIFIC SPINES. Election cycle and Congress number are how this
--      warehouse's political data is actually organised; no stock calendar has
--      them.
--   4. ONE SET OF LABELS so every chart says "2024-Q1" the same way.
--
-- Deliberately ONE ROW PER DAY, not per (day, grain). Coarse data snaps to the
-- start of its period (a month -> the 1st) and carries its own grain tag, per
-- rule 3 of the datetime standard. A multi-grain calendar buys nothing and makes
-- every join ambiguous.

with bounds as (
    select
        date_from_parts({{ ripple_time_floor() }}, 1, 1)   as floor_day,
        date_from_parts({{ ripple_time_ceiling() }}, 12, 31) as ceiling_day
),

days as (
    select dateadd(day, seq4(), (select floor_day from bounds)) as date_day
    from table(generator(rowcount => 160000))
),

bounded as (
    select date_day from days
    where date_day <= (select ceiling_day from bounds)
),

enriched as (
    select
        date_day,
        date_day::timestamp_ntz                          as date_ts,

        -- plain calendar parts
        year(date_day)                                   as year_num,
        quarter(date_day)                                as quarter_num,
        month(date_day)                                  as month_num,
        day(date_day)                                    as day_num,
        dayofweekiso(date_day)                           as day_of_week_iso,
        dayname(date_day)                                as day_name,
        monthname(date_day)                              as month_name,
        weekofyear(date_day)                             as week_of_year,
        yearofweekiso(date_day)                          as iso_year,
        weekiso(date_day)                                as iso_week,

        -- period starts: what a coarse-grained value snaps TO, so a monthly
        -- series joins here on month_start and a yearly one on year_start
        date_trunc('week',    date_day)::date            as week_start,
        date_trunc('month',   date_day)::date            as month_start,
        date_trunc('quarter', date_day)::date            as quarter_start,
        date_trunc('year',    date_day)::date            as year_start,
        last_day(date_day, 'month')                      as month_end,
        last_day(date_day, 'quarter')                    as quarter_end,
        last_day(date_day, 'year')                       as year_end,

        date_day = date_trunc('month', date_day)::date   as is_month_start,
        date_day = last_day(date_day, 'month')           as is_month_end,
        date_day = date_trunc('year', date_day)::date    as is_year_start,
        dayofweekiso(date_day) in (6, 7)                 as is_weekend,

        -- US federal fiscal year: starts Oct 1 and is NAMED for the year it ends,
        -- so 2025-10-01 falls in FY2026. All federal spending data uses this.
        case when month(date_day) >= 10
             then year(date_day) + 1 else year(date_day) end        as federal_fiscal_year,
        case when month(date_day) >= 10 then month(date_day) - 9
             else month(date_day) + 3 end                            as federal_fiscal_month,
        floor((case when month(date_day) >= 10 then month(date_day) - 9
                    else month(date_day) + 3 end - 1) / 3) + 1       as federal_fiscal_quarter,

        -- FEC two-year election cycle, named for the even year it ends in:
        -- 2023 and 2024 both belong to cycle 2024. This is how every campaign
        -- finance table in the warehouse is organised.
        case when mod(year(date_day), 2) = 0
             then year(date_day) else year(date_day) + 1 end         as election_cycle,
        mod(year(date_day), 2) = 0                                   as is_election_year,

        -- Congress number. The 1st Congress convened 1789-03-04; since the 20th
        -- Amendment each new Congress begins Jan 3 of the odd year, so the 119th
        -- began 2025-01-03. Dates on Jan 1-2 of an odd year still belong to the
        -- outgoing Congress. Null before 1789 -- there was no Congress.
        case
            -- no Congress before it first convened
            when date_day < date_from_parts(1789, 3, 4) then null
            -- odd year: the new Congress starts Jan 3, so Jan 1-2 still belongs
            -- to the outgoing one
            when mod(year(date_day), 2) = 1
                then floor((year(date_day) - 1789) / 2)
                     + iff(date_day >= date_from_parts(year(date_day), 1, 3), 1, 0)
            -- even year: always the Congress seated the previous January
            else floor((year(date_day) - 1790) / 2) + 1
        end                                                          as congress_number,

        -- ready-made labels so nothing invents its own
        to_varchar(date_day, 'YYYY-MM')                              as label_month,
        to_varchar(year(date_day)) || '-Q' || to_varchar(quarter(date_day)) as label_quarter,
        to_varchar(year(date_day))                                   as label_year
    from bounded
)

select * from enriched
