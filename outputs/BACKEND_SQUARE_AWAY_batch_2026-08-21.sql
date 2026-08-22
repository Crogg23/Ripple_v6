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

-- 3. Let the reader role SEE the raw landing layer (read-only).
--    72+ live tests fail today only because RIPPLE_READER can't look at
--    LIBRARY_RAW.LANDING; the sessions have been reading it accidentally via
--    secondary roles (see item 4). This makes the intended read path real.
grant usage on database LIBRARY_RAW to role RIPPLE_READER;
grant usage on schema LIBRARY_RAW.LANDING to role RIPPLE_READER;
grant select on all tables in schema LIBRARY_RAW.LANDING to role RIPPLE_READER;
grant select on future tables in schema LIBRARY_RAW.LANDING to role RIPPLE_READER;

-- ============================================================
-- PASTE 2 (2026-08-22, after paste 1 was run and verified)
-- ============================================================

-- 5. Wiring batch 2 — four new verified edges (preview-measured live):
--    a 100% environmental-penalty wire, two more politics/FEC ids, and the
--    99.9% courts bridge (the two federal court systems joined on docket no).
insert into LIBRARY_META."CONNECT".CONNECT_EDGES (A, B, KEY, TIER, MATCHED, MATCH_RATE) values
('EPA_PENALTY_GAP',                     'FED_EPA_FRS_FRS_FACILITIES', 'FRS_ID',      'STEEL',   93798, 1.0),
('FEC_CANDIDATE',                       'FED_FEC_CANDIDATES',         'FEC_CAND_ID', 'STEEL',    9874, 0.746),
('FEC_CAND_CMTE_LINK',                  'FED_FEC_BULK_COMMITTEES',    'FEC_CMTE_ID', 'STEEL',    7214, 0.631),
('FED_COURTLISTENER_FJC_IDB_CL_LINKED', 'FED_FJC_IDB_CIVIL',          'DOCKET',      'STEEL', 1160909, 0.999);

-- 6. Last test grants: reader can read the connection layer's entity tables
--    (6 of the 7 remaining failures; the 7th needs the build role by design).
grant select on all tables in schema LIBRARY_META."CONNECT" to role RIPPLE_READER;
grant select on future tables in schema LIBRARY_META."CONNECT" to role RIPPLE_READER;

-- 4. OPTIONAL BUT RECOMMENDED — close the secondary-roles hole.
--    The session PAT logs in as RIPPLE_READER but currently inherits ALL of
--    the user's roles as secondary roles (including ACCOUNTADMIN). That means
--    "read-only by design" was not actually true tonight. Run item 3 first,
--    then this, and sessions keep working through the front door only:
-- alter user <the PAT's user> set default_secondary_roles = ();
--    (Left commented out: Chris's call — it affects every tool using this login.)
