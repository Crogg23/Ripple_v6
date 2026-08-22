-- BACKEND SQUARE-AWAY BATCH — 2026-08-21
-- One paste, run as ACCOUNTADMIN in Snowsight. Two catalog-label fixes.
-- (The 5 wiring edges from earlier tonight are ALREADY applied — not repeated here.)

-- 1. The drinking-water service-area source: give it a real domain label.
--    (Its physical mart still lives under the immigration schema — that rename
--    is queued as a dbt cleanup; this fixes the catalog label people see.)
update LIBRARY_META.REGISTRY.SOURCE_REGISTRY
   set DOMAIN_PRIMARY = 'energy_environment',
       NOTES = coalesce(NOTES, '') || ' [2026-08-21: domain label set; mart schema rename queued]'
 where SOURCE_ID = 'fed_epa_sdwa_sdwa_service_areas';

-- 2. Retraction Watch landed twice; keep the classified copy, exclude the dupe.
update LIBRARY_META.REGISTRY.SOURCE_REGISTRY
   set INCLUDE = 'N',
       NOTES = coalesce(NOTES, '') || ' [2026-08-21: duplicate of xc_retraction_watch, same data landed twice]'
 where SOURCE_ID = 'fed_retraction_watch';

-- Expect: "1 row updated" twice.
