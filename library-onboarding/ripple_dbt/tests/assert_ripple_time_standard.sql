-- THE DATETIME GUARD. Fails the build if any repair from the 2026-08-20
-- time-index scan regresses.
--
-- Companion to macros/ripple_time.sql (the rules) and
-- tests/assert_no_epoch_or_pivot_dates.sql (the older, narrower epoch-1970
-- guard, which this does not replace).
--
-- Why a guard at all: every one of the defects below sat in the warehouse for
-- months without anyone noticing, because a wrong date does not raise an error
-- -- it just quietly answers the wrong question. The scan that found them cost
-- real money and took an afternoon. This file costs a few seconds per build and
-- means none of it can come back silently.
--
-- Each SELECT returns rows ONLY when something is wrong; dbt fails the test if
-- any row comes back.

-- 1. INGEST STAMPS ARE MICROSECONDS. A bare to_timestamp reads them as seconds
--    and lands the row in the year 56,596,956. Nine staging models were fixed
--    with the `, 6` scale argument on 2026-08-20.
select 'corporate_registry__fed_icij_offshoreleaks_entities' as model,
       'ingest stamp not a real timestamp'                   as defect,
       count(*)                                              as n
from {{ ref('corporate_registry__fed_icij_offshoreleaks_entities') }}
where _ingested_at is not null
  and (year(_ingested_at) < 2020 or year(_ingested_at) > year(current_date()) + 1)
having count(*) > 0

union all

select 'corporate_registry__fed_icij_offshoreleaks_relationships',
       'ingest stamp not a real timestamp', count(*)
from {{ ref('corporate_registry__fed_icij_offshoreleaks_relationships') }}
where _ingested_at is not null
  and (year(_ingested_at) < 2020 or year(_ingested_at) > year(current_date()) + 1)
having count(*) > 0

union all

select 'immigration__fed_ice_detainers',
       'ingest stamp not a real timestamp', count(*)
from {{ ref('immigration__fed_ice_detainers') }}
where _ingested_at is not null
  and (year(_ingested_at) < 2020 or year(_ingested_at) > year(current_date()) + 1)
having count(*) > 0

union all

-- 2. TWO-DIGIT YEARS MUST BE CENTURY-PIVOTED. EPA ships DD-MON-YY
--    ('02-JUN-16'); a bare parse read the year literally and put 5,300,149
--    facility create dates and 2,782,106 update dates in years 0000-0026.
--    The registry postdates 1990, so nothing here may predate it.
select 'environment__fed_epa_frs_facilities',
       'facility date before the registry existed (century lost again)', count(*)
from {{ ref('environment__fed_epa_frs_facilities') }}
where (create_date is not null and year(create_date) < 1990)
   or (update_date is not null and year(update_date) < 1990)
having count(*) > 0

-- NOTE: the twin of the model above, uncategorized__fed_epa_frs_full, is
-- deliberately NOT guarded here. Its dbt model is DISABLED, and referencing a
-- disabled model disables this whole test. Its table is nonetheless live in the
-- warehouse with 5,300,149 rows -- a byte-for-byte-sized duplicate of the
-- facilities model above -- still carrying the year-0026 dates, because nothing
-- rebuilds a disabled model. The SQL fix has been applied to that file anyway so
-- it is correct if ever re-enabled. Flagged 2026-08-20 as a DROP candidate.

union all

-- 3. THE FJC "NOT APPLICABLE" MARKER MUST STAY NULL. The Integrated Database
--    writes 01/01/1900 for a thing that never happened -- 5.26M defendants have
--    a fugitive-end-date because they were never fugitives. The database begins
--    in 1970, so ANY 1900 date here means the sentinel came back.
select 'justice__fed_fjc_idb_criminal',
       'the 1900 not-applicable marker is back', count(*)
from {{ ref('justice__fed_fjc_idb_criminal') }}
where fugitive_end_date   = '1900-01-01'::date
   or fugitive_start_date = '1900-01-01'::date
   or sentence_date       = '1900-01-01'::date
   or disposition_date    = '1900-01-01'::date
   or term_date           = '1900-01-01'::date
having count(*) > 0

union all

select 'justice__fed_fjc_idb_appellate',
       'the 1900 not-applicable marker is back', count(*)
from {{ ref('justice__fed_fjc_idb_appellate') }}
where court_record_date = '1900-01-01'::date
   or hearing_date      = '1900-01-01'::date
   or submission_date   = '1900-01-01'::date
   or transfer_date     = '1900-01-01'::date
having count(*) > 0

union all

select 'justice__fed_fjc_idb_civil',
       'the 1900 not-applicable marker is back', count(*)
from {{ ref('justice__fed_fjc_idb_civil') }}
where term_date = '1900-01-01'::date
having count(*) > 0

union all

-- 4. THE CALENDAR MUST COVER THE TRUSTED WINDOW. If the calendar is shorter
--    than the window the parser accepts, a legal timestamp has no row to join
--    to and silently drops out of every dense/gap query.
select 'reference__calendar',
       'calendar does not span the trusted window', count(*)
from (
    select min(date_day) as lo, max(date_day) as hi
    from {{ ref('reference__calendar') }}
)
where year(lo) > {{ ripple_time_floor() }}
   or year(hi) < {{ ripple_time_ceiling() }}
having count(*) > 0

union all

-- 5. THE CALENDAR MUST BE DENSE AND UNIQUE. One row per day, no gaps, no
--    duplicates -- otherwise "months with no events" counts are wrong in a way
--    nothing else would reveal.
select 'reference__calendar',
       'calendar is not one row per day', count(*)
from (
    select count(*) as n_rows, count(distinct date_day) as n_days,
           datediff('day', min(date_day), max(date_day)) + 1 as n_expected
    from {{ ref('reference__calendar') }}
)
where n_rows <> n_days or n_days <> n_expected
having count(*) > 0
