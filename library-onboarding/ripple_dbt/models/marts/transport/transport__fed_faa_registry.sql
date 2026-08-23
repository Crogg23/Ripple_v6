{{ config(enabled=false) }}

-- RETIRED 2026-08-22 (fix-session, item 11 of reports/the_fix_list_2026-08-22.md).
-- This was the stale July FAA registry twin: N_NUMBER 100% blank, four date
-- columns epoch-corrupted by a bare try_to_date on YYYYMMDD strings. The live
-- replacement is transport__fed_faa_aircraft_registry.sql (315,447 rows, key
-- verified unique, explicit date formats). Ruled for retirement 2026-08-11 (A2),
-- header here said so since 2026-08-18; disabled now. Deleting this file and
-- dropping the warehouse tables (LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_FAA_REGISTRY,
-- LIBRARY_MARTS.TIMELINE.TRANSPORT__FED_FAA_REGISTRY view,
-- LIBRARY_RAW.LANDING.FED_FAA_REGISTRY) is on Chris's drop list.

select 1 as retired
