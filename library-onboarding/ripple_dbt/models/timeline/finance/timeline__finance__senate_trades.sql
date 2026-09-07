{{ config(materialized='view', schema='TIMELINE', alias='FINANCE__SENATE_TRADES') }}

-- Written by hand 2026-09-07 to the gen_time_views.py template; the generator's
-- input reports/time_index/columns.csv is retired to the junk drawer, so it
-- cannot run. Clock rows for this mart sit in reports/time_index/clock_index.csv.
--
-- Canonical clock for FINANCE.FINANCE__SENATE_TRADES.
--   column : TRANSACTION_DATE   (DATE)
--   means  : reported -- the trade date on the PTR line; filed_date lags it by up to 45 days.
--   grain  : day
--
-- reported cannot be in the future -- if this row's value is, ripple_clock
-- reads 'planned' instead, not 'reported'. See ripple_row_clock in
-- macros/ripple_time.sql.
--
-- The original columns pass through untouched; the canonical four sit in front
-- of them. Rule 8 of the datetime standard: the raw column is never overwritten,
-- so a mis-parse is always recoverable.

select
    {{ ripple_window('src."TRANSACTION_DATE"::timestamp_ntz') }} as ripple_ts,
    {{ ripple_grain('day') }} as ripple_grain,
    {{ ripple_row_clock(ripple_window('src."TRANSACTION_DATE"::timestamp_ntz'), 'reported') }} as ripple_clock,
    'FINANCE.FINANCE__SENATE_TRADES'::varchar as ripple_source,
    src.*
from {{ ref('finance__senate_trades') }} as src
