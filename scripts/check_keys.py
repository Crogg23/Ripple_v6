#!/usr/bin/env python3
"""Cross-check the credential ledger against reality: env presence + decoded expiry.

Three sources of truth get reconciled here:
  1. infra/keys_ledger.json     -- what we CLAIM about every credential
  2. the process env (via .env) -- whether each credential is actually SET
  3. the live PAT's JWT exp     -- what the token ITSELF says (decoded locally,
                                   zero-network, never printed)

Prints one table row per ledger entry and exits nonzero when anything BLOCKs
(expiry inside the 7-day floor, or the ledger's PAT date drifting from the token's
own claim). WARN (<21 days, or unset optional keys) never fails the run — same
philosophy as scripts/secrets_check.py: only what stops a load stops the exit code.

    python scripts/check_keys.py
"""
from __future__ import annotations

import datetime as dt
import json
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
LIB = REPO / "library-onboarding"
LEDGER = REPO / "infra" / "keys_ledger.json"

if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

try:
    from dotenv import load_dotenv
    load_dotenv(LIB / ".env", override=True)
except Exception:  # pragma: no cover
    pass

from loadkit.preflight import decode_jwt_exp, pat_expiry_check  # noqa: E402

# Same calendar floors as pat_expiry_check -- one policy, two surfaces.
BLOCK_DAYS = 7.0
WARN_DAYS = 21.0
# Ledger vs decoded-token drift beyond this means someone rotated without updating
# the ledger (or vice versa) -- the ledger is lying, which defeats its purpose.
DRIFT_TOLERANCE_DAYS = 1.0


def _parse_expiry(raw):
    """Ledger dates are ISO (date or datetime, optional Z). None stays None."""
    if not raw:
        return None
    try:
        d = dt.datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
    except ValueError:
        return None
    if d.tzinfo is None:
        d = d.replace(tzinfo=dt.timezone.utc)
    return d


def check_entry(entry: dict, now: dt.datetime) -> dict:
    """One ledger row -> {env_var, set, expires, days_left, status, note}."""
    env_var = entry.get("env_var", "")
    val = os.getenv(env_var, "").strip()
    expires = _parse_expiry(entry.get("expires"))
    note = ""

    # The PAT gets the strongest treatment: decode the LIVE token and let the
    # token's own exp claim override the ledger, flagging drift between them.
    if env_var == "SNOWFLAKE_PAT" and val:
        decoded = decode_jwt_exp(val)
        if decoded is None:
            note = "live token is not a decodable JWT -- ledger date unverifiable"
        elif expires is None:
            expires, note = decoded, "ledger has no date; using the token's own exp claim"
        else:
            drift = abs((decoded - expires).total_seconds()) / 86400.0
            if drift > DRIFT_TOLERANCE_DAYS:
                return {"env_var": env_var, "set": True, "expires": decoded,
                        "days_left": (decoded - now).total_seconds() / 86400.0,
                        "status": "BLOCK",
                        "note": f"ledger says {expires:%Y-%m-%d} but the token says "
                                f"{decoded:%Y-%m-%d} -- fix infra/keys_ledger.json"}
            expires = decoded  # in tolerance: trust the token's exact timestamp

    if not val:
        # Unset SNOWFLAKE_PAT can't run anything -> BLOCK. Everything else in the
        # ledger is per-wave optional (secrets_check.py owns 'required'), so unset
        # is informational, not a failure.
        status = "BLOCK" if env_var == "SNOWFLAKE_PAT" else "UNSET"
        return {"env_var": env_var, "set": False, "expires": expires, "days_left": None,
                "status": status, "note": note or "not set in env/.env"}

    if expires is None:
        return {"env_var": env_var, "set": True, "expires": None, "days_left": None,
                "status": "OK", "note": note or "no expiry tracked"}

    days_left = (expires - now).total_seconds() / 86400.0
    chk = pat_expiry_check(expires, now, block_days=BLOCK_DAYS, warn_days=WARN_DAYS)
    status = "BLOCK" if not chk.ok else ("WARN" if chk.warn else "OK")
    return {"env_var": env_var, "set": True, "expires": expires,
            "days_left": days_left, "status": status, "note": note}


def main() -> int:
    now = dt.datetime.now(dt.timezone.utc)
    try:
        doc = json.loads(LEDGER.read_text(encoding="utf-8"))
        entries = doc.get("keys", [])
    except Exception as e:
        print(f"BLOCK: cannot read {LEDGER}: {e}")
        return 1
    if not entries:
        print(f"BLOCK: {LEDGER} has no 'keys' entries -- the ledger is the point")
        return 1

    print("== credential ledger check ==")
    print(f"{'STATUS':<7} {'ENV VAR':<22} {'SET':<4} {'EXPIRES':<21} {'DAYS':>6}  NOTE")
    blocked = 0
    for entry in entries:
        r = check_entry(entry, now)
        exp = f"{r['expires']:%Y-%m-%d %H:%M}Z" if r["expires"] else "-"
        days = f"{r['days_left']:.0f}" if r["days_left"] is not None else "-"
        print(f"{r['status']:<7} {r['env_var']:<22} {'yes' if r['set'] else '-':<4} "
              f"{exp:<21} {days:>6}  {r['note']}")
        if r["status"] == "BLOCK":
            blocked += 1
    # ASCII only -- the Windows console default codepage (cp1252) can't print
    # checkmark glyphs and a status tool must never crash on its own output.
    if blocked:
        print(f"\n  [FAIL] {blocked} BLOCK -- rotate/fix before any long-running load.")
        return 1
    print("\n  [PASS] no blocking credential problems.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
