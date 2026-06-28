#!/usr/bin/env python3
"""Preflight: confirm creds/secrets are in place before a backfill wave.

Exit 1 on any REQUIRED failure; 0 otherwise. OPTIONAL per-wave keys are reported,
never fail (keyless Wave-1 sources don't need them).

    python scripts/secrets_check.py

REQUIRED (a wave can't run without these):
  * library-onboarding/.env exists (warns if group/world-readable -> chmod 600).
  * Snowflake account + user + warehouse + (PAT or password).
  * Live smoke test: connect + SELECT CURRENT_ROLE() / CURRENT_VERSION().

OPTIONAL (reported; needed only by specific later waves):
  RIPPLE_CONTACT_UA  -- SEC/FFIEC return 403 without a real User-Agent (Wave 1/2)
  SAM_API_KEY        -- SAM.gov entity extract (Wave 2)
  CENSUS_API_KEY     -- Census ACS (Wave 2; TIGER bulk shapefiles need no key)
  COURTLISTENER_TOKEN-- RECAP court parties (Wave 4)
  SOCRATA_APP_TOKEN  -- higher portal rate limits (optional)
  ANTHROPIC_API_KEY  -- the LLM-agent loader path (deterministic loaders don't need it)
"""
from __future__ import annotations

import os
import stat
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
_LIB = _REPO / "library-onboarding"
if str(_LIB) not in sys.path:
    sys.path.insert(0, str(_LIB))

try:
    from dotenv import load_dotenv
    load_dotenv(_LIB / ".env", override=True)
except Exception:  # pragma: no cover
    pass

ENV_PATH = _LIB / ".env"
OPTIONAL = [
    ("RIPPLE_CONTACT_UA", "SEC/FFIEC 403 without it (must contain an email '@')"),
    ("SAM_API_KEY", "SAM.gov entity extract (Wave 2)"),
    ("CENSUS_API_KEY", "Census ACS (Wave 2)"),
    ("COURTLISTENER_TOKEN", "RECAP court parties (Wave 4)"),
    ("SOCRATA_APP_TOKEN", "higher portal rate limits (optional)"),
    ("ANTHROPIC_API_KEY", "LLM-agent loader path (deterministic loaders don't need it)"),
]


def _check_env_file(problems: list[str]) -> None:
    if not ENV_PATH.exists():
        problems.append(f".env not found at {ENV_PATH}")
        return
    mode = ENV_PATH.stat().st_mode
    if mode & (stat.S_IRWXG | stat.S_IRWXO):
        print(f"   [warn] {ENV_PATH} is group/world-accessible (mode {oct(mode & 0o777)}); "
              "run: chmod 600 library-onboarding/.env")
    else:
        print(f"   ok: {ENV_PATH} exists, perms {oct(mode & 0o777)}")


def _check_snowflake(problems: list[str]) -> None:
    from config import settings
    for attr, name in (("snowflake_account", "SNOWFLAKE_ACCOUNT"),
                       ("snowflake_user", "SNOWFLAKE_USER"),
                       ("snowflake_warehouse", "SNOWFLAKE_WAREHOUSE")):
        if not str(getattr(settings, attr, "")).strip():
            problems.append(f"{name} is not set")
    if not (settings.snowflake_pat.strip() or settings.snowflake_password.strip()):
        problems.append("neither SNOWFLAKE_PAT nor SNOWFLAKE_PASSWORD is set")
    # Live smoke test (authoritative — a present-but-revoked PAT fails here).
    try:
        import snow
        conn = snow.connect()
        try:
            cur = conn.cursor()
            cur.execute("SELECT CURRENT_ROLE(), CURRENT_VERSION()")
            role, ver = cur.fetchone()
            cur.close()
            print(f"   ok: Snowflake connected — role={role}, version={ver}")
        finally:
            conn.close()
    except Exception as e:
        problems.append(f"Snowflake connect/smoke-test FAILED: {str(e)[:120]}")


def _report_optional() -> None:
    print("   optional per-wave keys:")
    for var, why in OPTIONAL:
        val = os.getenv(var, "").strip()
        mark = "set" if val else "—  "
        extra = ""
        if var == "RIPPLE_CONTACT_UA" and val and "@" not in val:
            extra = "  [warn: should contain an email]"
        print(f"     [{mark}] {var:<20} {why}{extra}")


def main() -> int:
    print("== secrets / creds preflight ==")
    problems: list[str] = []
    _check_env_file(problems)
    _check_snowflake(problems)
    _report_optional()
    if problems:
        print("\n   REQUIRED problems:")
        for p in problems:
            print(f"     ✗ {p}")
        print("   -> fix these before running a wave.")
        return 1
    print("\n   ✓ required checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
