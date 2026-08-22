{#
    assert_ripple_timeline_registry.sql -- the guard on the canonical-clock layer.

    The registry (seeds/ripple_time_registry.csv) is the control table: it names
    every live mart table, which clock was chosen for it, and why. The views in
    LIBRARY_MARTS.TIMELINE are what actually exists. This test fails the build if
    those two drift apart, which is the failure mode that would quietly hollow
    the layer out: a generator re-run that skips a table, a mart renamed
    underneath a view, a clock label edited in the index but never regenerated.

    Six ways it can fail. Every row this returns is a violation, and the
    `problem` column says which.

    NOT tested here (deliberately): whether a clock label is CORRECT. That is a
    judgement about meaning, made by the 2026-08-20 review pass and revisable.
    This test only enforces that what the registry claims and what the warehouse
    holds are the same thing.
#}

with registry as (
    select * from {{ ref('ripple_time_registry') }}
),

-- What the warehouse actually holds in the canonical schema.
existing_views as (
    select table_name
    from LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES
    where table_schema = 'TIMELINE'
      and table_type = 'VIEW'
),

timeline as (
    select * from {{ ref('timeline__warehouse') }}
),

-- 1. The registry promises a view that does not exist.
missing_view as (
    select r.source as subject,
           'registry says has_view but no view exists in TIMELINE' as problem
    from registry r
    left join existing_views v on v.table_name = r.table_name
    where r.has_view and v.table_name is null
),

-- 2. A clock kind outside the standard's vocabulary (rule 4).
bad_clock as (
    select source as subject,
           'clock kind is not one of the five in the standard, or none' as problem
    from registry
    where clock not in ('happened', 'reported', 'decided',
                        'span_start', 'span_end', 'none')
),

-- 3. A grain outside the standard's vocabulary (rule 3).
bad_grain as (
    select source as subject,
           'grain is not day/month/quarter/year, or none' as problem
    from registry
    where grain not in ('day', 'month', 'quarter', 'year', 'none')
),

-- 4. A row that claims a clock but names no column to read it from, or the
--    reverse. Either way the registry is lying about something.
incoherent as (
    select source as subject,
           'clock and clock_column disagree about whether a clock exists' as problem
    from registry
    where (clock = 'none') != (nullif(trim(clock_column), '') is null)
),

-- 5. A source in the shared timeline that the registry does not know about.
--    Silent extra data is as bad as silent missing data.
orphan_source as (
    select t.ripple_source as subject,
           'source appears in the shared timeline but not in the registry' as problem
    from (select distinct ripple_source from timeline) t
    left join registry r on r.source = t.ripple_source
    where r.source is null
),

-- 6. A canonical timestamp outside the trusted window. The parser clamps to it,
--    so anything here means something bypassed the standard.
out_of_window as (
    select ripple_source as subject,
           'canonical timestamp outside the trusted window' as problem
    from timeline
    where ripple_day < date_from_parts({{ ripple_time_floor() }}, 1, 1)
       or ripple_day > date_from_parts({{ ripple_time_ceiling() }}, 12, 31)
),

-- 7. The planned/actual split (added 2026-08-21, see ripple_row_clock in
--    macros/ripple_time.sql) disagreeing with the value it is tagging: a
--    'planned' day that is not actually in the future, or a happened/reported/
--    decided day that silently is. Either means a FLOW rule reading this data
--    could mistake a scheduled, not-yet-final date for something that already
--    occurred -- the exact bug this split exists to prevent.
mistagged_planned as (
    select ripple_source as subject,
           'planned/actual split disagrees with the timestamp it is tagging' as problem
    from timeline
    where (ripple_clock = 'planned' and ripple_day <= current_date())
       or (ripple_clock in ('happened', 'reported', 'decided') and ripple_day > current_date())
)

select * from missing_view
union all select * from bad_clock
union all select * from bad_grain
union all select * from incoherent
union all select * from orphan_source
union all select * from out_of_window
union all select * from mistagged_planned
