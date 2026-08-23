{{ config(enabled=false) }}

-- RETIRED 2026-08-22: clock view for the stale July FAA registry twin.
-- See models/marts/transport/transport__fed_faa_registry.sql for the story.
-- Its union-all block was removed from timeline__transport_index.sql and its
-- row from seeds/ripple_time_registry.csv the same day.

select 1 as retired
