"""The evidence.dev / Investigator read lane -- one command, Chris runs it.

Applies serve/serve_wh.sql + scripts/instrument_snowflake_setup.sql (steps 0-4)
statement-by-statement through the live PAT session (which authenticates as
ACCOUNTADMIN; a PAT session can't USE ROLE, so the files' USE ROLE line is
skipped -- the session already IS the right role).

What it creates (all idempotent, additive):
  SERVE_WH        X-Small serving warehouse, 60s auto-suspend
  SERVE_MON       5-credit/month monitor capping SERVE_WH (separate from RIPPLE_BUDGET)
  RIPPLE_READER   fresh SELECT/USAGE-only role (never granted a write -- provably read-only)
                  + the libel firewall: raw CONNECT claim tables revoked, only
                  V_LEADS_PUBLISHED readable
  INSTRUMENT_READER  a 90-day PAT on CROGG23, role-restricted to RIPPLE_READER;
                  secret written straight into library-onboarding/.env as
                  SNOWFLAKE_SERVE_PAT (never printed), expiry recorded in
                  infra/keys_ledger.json

Usage:
    python3 scripts/apply_read_lane.py            # preview: print the plan, touch nothing
    python3 scripts/apply_read_lane.py --apply    # do it, then verify

Verify afterwards from the repo:  python ripple.py chart budget
Expected: "lane: enforced" + role RIPPLE_READER.
"""
import argparse
import datetime as dt
import json
import re
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")
REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

ENV_PATH = REPO / "library-onboarding" / ".env"
LEDGER_PATH = REPO / "infra" / "keys_ledger.json"
PAT_NAME = "INSTRUMENT_READER"

STATEMENTS = [
    # ---- serve/serve_wh.sql ----
    ("create SERVE_WH", """CREATE WAREHOUSE IF NOT EXISTS SERVE_WH
        WAREHOUSE_SIZE='XSMALL' AUTO_SUSPEND=60 AUTO_RESUME=TRUE INITIALLY_SUSPENDED=TRUE
        COMMENT='Read-only reading-room serving WH; isolates analyst reads from ETL (RIPPLE_WH/DBT_WH).'"""),
    ("create SERVE_MON", """CREATE RESOURCE MONITOR IF NOT EXISTS SERVE_MON
        WITH CREDIT_QUOTA=5 FREQUENCY=MONTHLY START_TIMESTAMP=IMMEDIATELY
        TRIGGERS ON 80 PERCENT DO NOTIFY ON 100 PERCENT DO SUSPEND ON 110 PERCENT DO SUSPEND_IMMEDIATE"""),
    ("attach SERVE_MON to SERVE_WH", "ALTER WAREHOUSE SERVE_WH SET RESOURCE_MONITOR = SERVE_MON"),
    ("SERVE_WH usage -> CLAUDE_MCP_READONLY", "GRANT USAGE ON WAREHOUSE SERVE_WH TO ROLE CLAUDE_MCP_READONLY"),
    # ---- instrument_snowflake_setup.sql STEP 1 ----
    ("create RIPPLE_READER", """CREATE ROLE IF NOT EXISTS RIPPLE_READER
        COMMENT='Provably read-only serving role. USAGE + SELECT only - never granted a write privilege. If you are about to GRANT CREATE/INSERT/OPERATE on this role: do not.'"""),
    ("RIPPLE_READER -> CROGG23", "GRANT ROLE RIPPLE_READER TO USER CROGG23"),
]
for _db in ["LIBRARY_RAW", "LIBRARY_META", "LIBRARY_MARTS", "LIBRARY_STAGING", "THE_LIBRARY"]:
    STATEMENTS += [
        (f"usage on db {_db}", f"GRANT USAGE ON DATABASE {_db} TO ROLE RIPPLE_READER"),
        (f"usage on all schemas {_db}", f"GRANT USAGE ON ALL SCHEMAS IN DATABASE {_db} TO ROLE RIPPLE_READER"),
        (f"usage on future schemas {_db}", f"GRANT USAGE ON FUTURE SCHEMAS IN DATABASE {_db} TO ROLE RIPPLE_READER"),
    ]
for _db, _kinds in [
    ("LIBRARY_RAW", ["TABLES"]),
    ("LIBRARY_META", ["TABLES", "VIEWS"]),
    ("LIBRARY_MARTS", ["TABLES", "VIEWS"]),
    ("LIBRARY_STAGING", ["TABLES", "VIEWS"]),
    ("THE_LIBRARY", ["VIEWS"]),
]:
    for _k in _kinds:
        STATEMENTS += [
            (f"select on all {_k.lower()} {_db}", f"GRANT SELECT ON ALL {_k} IN DATABASE {_db} TO ROLE RIPPLE_READER"),
            (f"select on future {_k.lower()} {_db}", f"GRANT SELECT ON FUTURE {_k} IN DATABASE {_db} TO ROLE RIPPLE_READER"),
        ]
# ---- the libel firewall (raw claim tables stay dark; only the published view) ----
for _t in ["LEADS", "ENTITY_LINKS", "ENTITY_MAP", "ENTITY_GOLDEN", "MATCH_PAIRS"]:
    STATEMENTS.append((f"firewall: revoke {_t}",
                       f'REVOKE SELECT ON TABLE LIBRARY_META."CONNECT".{_t} FROM ROLE RIPPLE_READER'))
STATEMENTS.append(("firewall: allow V_LEADS_PUBLISHED",
                   'GRANT SELECT ON VIEW LIBRARY_META."CONNECT".V_LEADS_PUBLISHED TO ROLE RIPPLE_READER'))
# ---- STEP 3: warehouses (USAGE only, no OPERATE) + budget visibility ----
STATEMENTS += [
    ("SERVE_WH usage -> reader", "GRANT USAGE ON WAREHOUSE SERVE_WH TO ROLE RIPPLE_READER"),
    ("COMPUTE_WH usage -> reader", "GRANT USAGE ON WAREHOUSE COMPUTE_WH TO ROLE RIPPLE_READER"),
    ("monitor SERVE_MON -> reader", "GRANT MONITOR ON RESOURCE MONITOR SERVE_MON TO ROLE RIPPLE_READER"),
    ("monitor RIPPLE_BUDGET -> reader", "GRANT MONITOR ON RESOURCE MONITOR RIPPLE_BUDGET TO ROLE RIPPLE_READER"),
]


def _apply_grants(cur):
    ok, failed = 0, []
    for label, sql in STATEMENTS:
        try:
            cur.execute(sql)
            ok += 1
            print(f"  OK   {label}")
        except Exception as e:  # keep going -- grants are independent
            failed.append((label, str(e).splitlines()[0][:160]))
            print(f"  FAIL {label}: {str(e).splitlines()[0][:160]}")
    print(f"\n{ok}/{len(STATEMENTS)} statements OK, {len(failed)} failed")
    return failed


SNOWSIGHT_PAT_STEP = (
    "\n  [!] Serving PAT NOT minted from here -- Snowflake forbids a PAT session from\n"
    "      minting a PAT for the same user. Do this ONE step in Snowsight (as CROGG23):\n"
    "        Admin > Users & Roles > CROGG23 > Programmatic access tokens > Generate\n"
    "        name INSTRUMENT_READER, role restriction RIPPLE_READER, 90 days\n"
    "      Then paste the secret into library-onboarding/.env as:\n"
    "        SNOWFLAKE_SERVE_PAT=<secret>\n        RIPPLE_SERVE_ROLE=RIPPLE_READER\n"
    "      and add its expiry to infra/keys_ledger.json.\n"
    "      Until then evidence.dev + ripple chart run on the interim lane (works, just admin)."
)


def _mint_pat(cur):
    """Mint the role-restricted serving PAT; write the secret to .env only.

    Snowflake blocks a PAT session from minting a PAT for the same user, so on the
    live PAT session this raises 099413 -- caught, with Snowsight instructions.
    """
    cur.execute("SHOW USER PROGRAMMATIC ACCESS TOKENS FOR USER CROGG23")
    existing = [r for r in cur.fetchall() if r[0] == PAT_NAME and str(r[5]).upper() == "ACTIVE"]
    if existing:
        print(f"  PAT {PAT_NAME} already ACTIVE (expires {existing[0][4]}) -- keeping it; "
              f"no new secret (rotate in Snowsight if the secret is lost).")
        return None, str(existing[0][4])
    try:
        cur.execute(
            f"ALTER USER CROGG23 ADD PROGRAMMATIC ACCESS TOKEN {PAT_NAME} "
            f"ROLE_RESTRICTION = 'RIPPLE_READER' DAYS_TO_EXPIRY = 90 "
            f"COMMENT = 'evidence.dev + Investigator Instrument read lane. Rotate with the main PAT.'"
        )
    except Exception as e:
        if "099413" in str(e) or "programmatic access token" in str(e).lower():
            print(SNOWSIGHT_PAT_STEP)
            return None, None
        raise
    row = cur.fetchone()  # (token_name, token_secret)
    secret = row[1]
    expiry = (dt.datetime.utcnow() + dt.timedelta(days=90)).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"  PAT {PAT_NAME} minted (90 days, role-restricted to RIPPLE_READER). Secret NOT printed.")
    return secret, expiry


def _write_env(secret):
    text = ENV_PATH.read_text() if ENV_PATH.exists() else ""
    lines = [l for l in text.splitlines()
             if not l.startswith("SNOWFLAKE_SERVE_PAT=") and not l.startswith("RIPPLE_SERVE_ROLE=")]
    lines += [f"SNOWFLAKE_SERVE_PAT={secret}", "RIPPLE_SERVE_ROLE=RIPPLE_READER"]
    ENV_PATH.write_text("\n".join(lines) + "\n")
    ENV_PATH.chmod(0o600)
    print(f"  .env updated: SNOWFLAKE_SERVE_PAT + RIPPLE_SERVE_ROLE ({ENV_PATH})")


def _write_ledger(expiry):
    ledger = json.loads(LEDGER_PATH.read_text())
    ledger["keys"] = [k for k in ledger["keys"] if k.get("env_var") != "SNOWFLAKE_SERVE_PAT"]
    ledger["keys"].append({
        "name": f"Snowflake serving PAT ({PAT_NAME}, role-restricted to RIPPLE_READER)",
        "env_var": "SNOWFLAKE_SERVE_PAT",
        "expires": expiry,
        "renew_note": "90-day PAT for evidence.dev + ripple chart read lane. Re-mint: python3 scripts/apply_read_lane.py --apply (drops nothing; mints only if absent).",
    })
    ledger["updated"] = dt.date.today().isoformat()
    LEDGER_PATH.write_text(json.dumps(ledger, indent=2) + "\n")
    print(f"  keys_ledger.json updated (expires {expiry})")


def _verify(cur):
    print("\n--- VERIFY ---")
    cur.execute("SHOW WAREHOUSES LIKE 'SERVE_WH'")
    rows = cur.fetchall()
    print(f"SERVE_WH exists: {bool(rows)}")
    cur.execute("SHOW RESOURCE MONITORS LIKE 'SERVE_MON'")
    print(f"SERVE_MON exists: {bool(cur.fetchall())}")
    cur.execute("SHOW GRANTS TO ROLE RIPPLE_READER")
    grants = cur.fetchall()
    bad = [g for g in grants if g[1] not in ("USAGE", "SELECT", "MONITOR")]
    print(f"RIPPLE_READER grants: {len(grants)}; non-read privileges (MUST be []): {bad[:5]}")
    leads = [g for g in grants if g[3].endswith('"CONNECT".LEADS') or g[3].endswith("CONNECT.LEADS")]
    print(f"firewall: direct LEADS grant present (MUST be False): {bool(leads)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="actually run (default: preview)")
    args = ap.parse_args()
    if not args.apply:
        print(__doc__)
        print(f"PREVIEW -- {len(STATEMENTS)} statements would run, then PAT mint + .env + ledger. Re-run with --apply.")
        for label, _ in STATEMENTS:
            print(f"  - {label}")
        return
    from ripple.common import connect
    conn = connect()
    cur = conn.cursor()
    failed = _apply_grants(cur)
    secret, expiry = _mint_pat(cur)
    if secret:
        _write_env(secret)
        _write_ledger(expiry)
    _verify(cur)
    conn.close()
    if failed:
        print(f"\nNOTE: {len(failed)} grant statements failed (see above) -- usually a missing object, not fatal.")
    print("\nNext: python ripple.py chart budget   (expect: lane enforced, role RIPPLE_READER)")


if __name__ == "__main__":
    main()
