---
name: snowflake-pat-role-reality
description: "PAT sessions cannot USE ROLE, and CLAUDE_MCP_READONLY is not actually read-only — enforced read-only needs a role-bound PAT (RIPPLE_READER)"
metadata: 
  node_type: memory
  type: project
  originSessionId: e03a1979-3541-4dc9-b9f9-c707cf3c9528
---

Live-probed 2026-07-03: the repo's Snowflake PAT session is role-restricted — `USE ROLE`
raises "Current session is restricted", so every local query runs as ACCOUNTADMIN no
matter what serve_session.py or any code pins. And CLAUDE_MCP_READONLY holds CREATE
TABLE/VIEW/STAGE/FILE FORMAT on 18 schemas (some via FUTURE grants) + OPERATE on 2
warehouses — it is not read-only and a REVOKE sweep can't provably clean it.

**Why:** any "read-only lane" claim that rests on `USE ROLE` or on CLAUDE_MCP_READONLY
is fiction. The Instrument (viz/sqlrun.py) therefore verifies its lane at connect time
and never claims "enforced" from env-var presence.

**How to apply:** enforced read-only = a FRESH role granted only USAGE+SELECT
(`RIPPLE_READER`, DDL in scripts/instrument_snowflake_setup.sql) + a PAT minted with
ROLE_RESTRICTION to it, stored as SNOWFLAKE_SERVE_PAT in library-onboarding/.env.
Until Chris applies that, the wall is client-side guarding (viz/guard.py) +
single-statement cursor.execute. Check the live lane with `python ripple.py chart budget`.
Related: [[bridge-fuel-reality]]
