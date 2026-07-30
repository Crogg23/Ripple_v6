HANDOFF: Wire the modeled marts into the entity spine (CONNECT layer)

CONTEXT: THE DBT PIPELINE WAS DEAD. IT ISN'T ANYMORE.
========================================================
The previous session's handoff claimed dbt had run and hit 28 errors. That could not
have happened: dbt could not parse (962 duplicate source declarations, most from an
untracked catch-all YAML) and had no working credential (profiles.yml pointed at a
SNOWFLAKE_PAT that doesn't exist and a role, RIPPLE_TRANSFORM_RW, that was never
created). This session fixed both, put dbt on key-pair auth (new keypair registered on
CROGG23's RSA_PUBLIC_KEY_2 slot, private key at .keys/ripple_dbt.p8, gitignored), and
got a real `dbt build` running for the first time. 455 models build clean, 0 model
errors, 0 test errors.

Also fixed: `library-onboarding/snow.py` + `config.py` had the exact same dead-PAT
problem and are shared by every Ripple script (thelibrary_build.py, etc.), not just
dbt. They now use the same key-pair auth, so the whole script fleet works again.

WHAT ELSE THIS SESSION DID (skim, not the point of this handoff)
========================================================
- 219 -> 346 sources now have a real, verified mart (126 newly generated + fixes)
- Deleted 30 duplicate/stub registry rows that were inflating counts; made the
  CATALOG view case-insensitive so it can't happen again
- Fixed a mart that silently discarded 100% of its data (FDA drug recalls was reading
  an API envelope instead of the records inside it -- 1 null row instead of 17,816
  real ones) and 4 more that were a single unparsed JSON blob column
- Dropped 48 orphaned/superseded tables from a stray DBT_CROGERS schema, then found
  and repaired 36 THE_LIBRARY (the plain-English front-door layer) views that broke
  because they pointed at those dropped tables. All 252 THE_LIBRARY views now resolve.
- Populated verified JOIN_KEYS_STD/JOIN_KEY_TIER for 127 sources from real column
  evidence (not asserted). 169 more are flagged for manual review in
  outputs/join_key_tier_review.csv -- their claimed tier could not be confirmed with
  the current key-name catalog, which is deliberately incomplete (see script docstring
  for known gaps: CMS nursing homes key on PROVNUM, FDA FAERS on PRIMARYID, etc).
- Zero-copy backups exist if anything needs to be compared: LIBRARY_MARTS_PREDBT_20260729
  (full mart snapshot) and LIBRARY_META.REGISTRY.SOURCE_REGISTRY_BAK_20260729.

THE ACTUAL GAP THIS HANDOFF IS ABOUT
========================================================
346 sources are modeled (queryable). Only 42 are wired into the entity spine
(LIBRARY_META."CONNECT".ENTITY_INDEX) -- the hub that lets a query jump from one
dataset to another via a shared ID (an NPI, an EIN, a LEI). 307 modeled sources have a
verified STEEL/STRONG/GEO join key sitting right there in the mart and are NOT
connected to anything. Each one works fine standalone; none of them talk to each other
or to the spine yet.

Current spine (42 source tables, 25.3M records, 10 key types):
  NPI      9 tables   17.10M records   (providers)
  EIN      6 tables    4.16M records   (nonprofits/orgs)
  LEI      2 tables    3.38M records   (legal entities)
  CIK      4 tables  170.4K records    (SEC filers)
  UEI      3 tables  155.3K records    (federal contractors/grantees)
  DEA_NO   1 table   149.2K records    (controlled-substance handlers)
  CCN     10 tables  113.6K records    (healthcare facilities)
  BIOGUIDE 5 tables   27.2K records    (members of Congress)
  ICPSR    2 tables   13.3K records    (judges)
  IMO      2 tables    8.7K records    (vessels)

YOUR JOB: prioritize which of the 307 unconnected sources get wired in next, and in
what order. This is scope/sequencing, i.e. YELLOW lane per the constitution -- pick the
approach, then a one-line receipt to Chris. Whether the spine itself grows a new key
TYPE (e.g. should CUSIP or MINE_ID become spine-native) leans RED -- that's changing
how the entity spine connects things, which the constitution flags as Chris's call if
you're not sure.

STARTER CANDIDATES (already verified STEEL/STRONG keys, NOT yet in the spine, ranked
by mart size -- run the query below yourself for the live list, this is a snapshot):

  Biggest by row count:
    FED_SEC_13F_POSITIONS            202.5M  keys: ACCESSION_NUMBER, CUSIP
    fed_dea_arcos                    178.6M  keys: DEA_NO            <- SAME key type as spine's 1 DEA_NO table; likely fastest real win
    fed_fec_indiv_contributions        84.2M  keys: FEC_ID, STATE, ZIP
    FED_USASPENDING_ASSISTANCE_FULL    19.9M  keys: STATE, UEI       <- SAME key type as spine's 3 UEI tables
    intl_gleif_repex                    6.3M  keys: LEI              <- SAME key type as spine's 2 LEI tables
    FED_MSHA_VIOLATIONS                 6.2M  keys: MINE_ID          <- new key type, not yet spine-native
    FED_EPA_FRS_FULL                    5.3M  keys: FRS_ID, county/state/zip

  Many more small-to-mid NPI sources (~500K rows each) already share the spine's
  dominant key type and look like low-effort additions:
    fed_cms_quality_payment_program_experience, fed_cms_order_and_referring,
    fed_cms_medicare_physician_other_practitioners_by_provider(_and_service),
    fed_cms_medicare_fee_for_service_public_provider_enrollment,
    fed_cms_medicare_dialysis_facilities, fed_cms_fiscal_intermediary_shared_system_...

  A large EPA cluster shares FRS_ID (not yet spine-native, but internally consistent --
  wiring ONE of them in establishes the pattern for the rest):
    fed_epa_air_emissions_poll_rpt_combined_emissions, fed_epa_npdes_npdes_sics,
    fed_epa_npdes_npdes_informal_enforcement_actions, fed_epa_frs_frs_naics_codes,
    fed_epa_frs_frs_program_links, fed_epa_frs_frs_sic_codes, fed_epa_npdes_npdes_qncr_history,
    fed_epa_sdwa_sdwa_facilities, fed_epa_npdes_npdes_inspections,
    fed_epa_icis_air_icis_air_titlev_certs/_stack_tests, fed_epa_sdwa_sdwa_site_visits,
    fed_epa_sdwa_sdwa_violations_enforcement, fed_epa_sdwa_sdwa_lcr_samples

RE-RUN THIS TO GET THE LIVE LIST (don't trust the snapshot above once you've wired
anything in):

    SELECT c.SOURCE_ID, c.JOIN_KEY_TIER, c.JOIN_KEYS_STD, c.MART_ROW_COUNT, c.DOMAIN_PRIMARY
    FROM LIBRARY_META.REGISTRY.CATALOG c
    WHERE c.LIFECYCLE = 'modeled'
      AND c.JOIN_KEY_TIER IN ('STEEL','STRONG')
      AND ARRAY_SIZE(c.JOIN_KEYS_STD) > 0
      AND NOT EXISTS (
        SELECT 1 FROM LIBRARY_META."CONNECT".ENTITY_INDEX ei
        WHERE UPPER(ei.SOURCE_TABLE) = UPPER(c.SOURCE_ID)
      )
    ORDER BY c.MART_ROW_COUNT DESC NULLS LAST;

QUESTIONS TO ANSWER BEFORE WIRING ANYTHING IN
========================================================
1. Find how the existing 42 got INTO the spine (look for the loader/pour script that
   populates LIBRARY_META."CONNECT".ENTITY_INDEX -- likely in connect/ per this repo's
   layout). Understand its shape before adding to it; don't hand-roll a second pattern.
2. Same COUNT(col)-is-not-COUNT(DISTINCT col) trap applies here as everywhere else in
   this repo (see CLAUDE.md section 7) -- verify each candidate key is actually
   populated and distinct in the mart before wiring it in, don't trust the
   JOIN_KEY_TIER label alone. This session already caught two false positives this way
   (NPPES EIN, NOAA_AIS imo_number) and left 169 more unverified in
   outputs/join_key_tier_review.csv.
3. Decide the wiring order: value (does this actually let Chris ask a new question
   that matters to the mission) vs. effort (same key type as existing spine entries =
   cheap; new key type = you're deciding whether the spine grows a new dimension).
4. 265 additional sources have a mart but NO verified key at all (JOIN_KEY_TIER is
   NONE or unconfirmed) -- those are a separate, harder problem: finding a join key
   that was never identified, not just wiring up one that's already known. Don't
   conflate the two backlogs.

KEY FILES
========================================================
- library-onboarding/ripple_dbt/  -- the dbt project, now working (dbt parse/build/test
  all functional; profiles.yml documents the auth story in comments)
- library-onboarding/snow.py, config.py -- shared connection helper, now key-pair aware
- scripts/retier_join_keys.py -- the tool that verified 127 of the current keys; extend
  its STEEL_KEYS/GEO_KEYS dicts as you find more real key column names
- scripts/audit_dbt_sources.py -- pre-flight guard, run before any dbt change
- outputs/join_key_tier_review.csv -- 169 unverified tier claims, needs eyes
- .keys/ripple_dbt.p8 -- the private key (gitignored, machine-local; regenerate with
  scripts/rotate_dbt_keypair.py if this moves to a new machine)
