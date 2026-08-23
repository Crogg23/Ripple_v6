{{ config(enabled=false) }}

-- RETIRED 2026-08-22: staging for the stale July FAA registry twin.
-- See models/marts/transport/transport__fed_faa_registry.sql for the story.
-- Replacement staging: staging/fed_faa_aircraft_registry/.

select 1 as retired
