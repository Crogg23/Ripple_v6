# Timeline rebuild — blocked on Mac dbt auth, handoff

**Date:** 2026-08-31. Greenlights recorded: rebuild + destroy.
Destroy half is DONE (see icij_drop_log_2026-08-31.json).
Rebuild half is blocked: dbt cannot authenticate from this Mac.

## Why dbt fails here

- `profiles.yml` dev target reads `SNOWFLAKE_PRIVATE_KEY_PATH`,
  defaulting to `C:/Code/Ripple_v6/.keys/ripple_dbt.p8` — the Windows box's path.
- No `.keys/ripple_dbt.p8` exists in this repo copy on the Mac.
- The profile's own notes say the Mac holds the slot-2 private key
  somewhere, but it is not at any path this session could find.
- The Mac DOES have a working `SNOWFLAKE_PAT` — it is what the
  Python-scripts door uses, verified live as ACCOUNTADMIN today.
- The harness classifier blocked Claude from editing profiles.yml
  (auth config) and from probing the environment for key paths.

## Option A — point dbt at the Mac's key (if you know where it is)

```bash
export SNOWFLAKE_PRIVATE_KEY_PATH=/path/to/mac/ripple_dbt.p8
```

## Option B — add a PAT target to profiles.yml (paste under `outputs:`)

```yaml
    mac:
      type: snowflake
      account: "{{ env_var('SNOWFLAKE_ACCOUNT', 'ONEAFDA-UMB20733') }}"
      user: "{{ env_var('SNOWFLAKE_USER', 'CROGG23') }}"
      password: "{{ env_var('SNOWFLAKE_PAT') }}"
      role: "{{ env_var('SNOWFLAKE_ROLE', 'ACCOUNTADMIN') }}"
      warehouse: "{{ env_var('SNOWFLAKE_ETL_WAREHOUSE', env_var('SNOWFLAKE_WAREHOUSE', 'DBT_WH')) }}"
      database: LIBRARY_STAGING
      schema: DBT_CROGERS
      threads: 4
```

Note: the 2026-07-29 comment in profiles.yml says Snowflake's
BLOCKED_ROLES_LIST forbids PAT + ACCOUNTADMIN. Observed behavior today
contradicts that — the scripts door connects with this PAT as
ACCOUNTADMIN. If dbt still gets refused, that's the blocklist firing
on the dbt driver path; fall back to Option A.

## Then run (either option)

```bash
cd library-onboarding/ripple_dbt
dbt run -s "timeline__*_index" timeline__warehouse   # ~31 tables + 1 view, pennies
dbt test -s assert_ripple_timeline_registry           # the upgraded guard
```

Add `--target mac` to both commands if you used Option B.

## What the rebuild deploys

- 31 domain rollups now storing base clock kinds only, never 'planned'
- timeline__warehouse as a VIEW deriving planned/actual at read time
- guard test with two new checks: no frozen planned tags in rollups,
  no stray views in TIMELINE the registry doesn't claim
