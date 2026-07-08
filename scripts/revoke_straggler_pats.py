#!/usr/bin/env python3
"""Revoke the stale / over-privileged programmatic access tokens on CROGG23 and
refresh the key ledger (D-security cleanup, 2026-07-07).

THE PROBLEM: `SHOW USER PROGRAMMATIC ACCESS TOKENS` returns 10 live PATs, but
infra/keys_ledger.json tracks essentially one of them (the SNOWFLAKE_PAT row) --
a 9-token blind spot, several of which are unrestricted / ACCOUNTADMIN / already
expired. Any leaked PAT with role='' or ACCOUNTADMIN is a full-account key.

THIS SCRIPT drops exactly 5 stragglers by an EXPLICIT ALLOW-LIST (never a
"drop everything except" rule -- a mismatch must FAIL SAFE by dropping nothing):

  DROP (5):
    Ripple_v6           role=''            unrestricted, exp 2027  -> full-account key
    THE_LIBRARY         role=ACCOUNTADMIN  exp 2027                -> full-account key
    ripple_loader       role=RIPPLE_ROLE   superseded, exp 2027    -> old loader role
    RIPPLE_LOADER_PAT2  role=RIPPLE_LOADER  dup of RIPPLE_LOADER_PAT
    LIBRARY_CLAUDE_PAT  role=''            already EXPIRED

  KEEP (5) -- NEVER dropped:
    LIBRARY_PAT         the MAIN in-use session token (the live write lane)
    RIPPLE_LOADER_PAT   least-privilege loader
    CLAUDE_MCP_RO       read-only MCP token
    PORTAL_RECON        recon token
    WAVE3_LOAD          wave-3 load token

DDL per drop:  ALTER USER CROGG23 REMOVE PROGRAMMATIC ACCESS TOKEN "<name>"
Names are quoted to preserve the exact (mixed) case SHOW reports.

Guards (checked in BOTH preview and apply -- abort => nothing dropped):
  * every DROP-target name must exist live, or ABORT
  * every KEEP name must exist live, or ABORT
  * if any live token is neither in DROP nor KEEP it is LEFT ALONE (allow-list is
    drop-only), but it's reported so a surprise 11th token is visible.

REMOVE is irreversible (a PAT secret can't be recreated). --apply snapshots the
full metadata of every dropped token to outputs/ first, so Chris knows exactly
what to regenerate if one was still wired somewhere.

LEDGER: infra/keys_ledger.json is a multi-credential ledger (SAM / Anthropic /
Census / ... keyed by env_var). We do NOT clobber it. We refresh a dedicated
`programmatic_access_tokens` section listing the 5 KEPT PATs with real expiries.
Preview prints the diff; --apply writes it.

    python3 scripts/revoke_straggler_pats.py            # PREVIEW (reads only)
    python3 scripts/revoke_straggler_pats.py --apply    # drop + refresh ledger

Run this yourself -- the agent's auto-mode classifier blocks account mutations.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import warnings
from pathlib import Path
from datetime import timezone

warnings.filterwarnings("ignore")
REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

USER = "CROGG23"
LEDGER = REPO / "infra" / "keys_ledger.json"

# --- EXPLICIT ALLOW-LIST (drop-only). Mismatch => fail safe, drop nothing. ---
DROP_NAMES = frozenset({
    "Ripple_v6",
    "THE_LIBRARY",
    "ripple_loader",
    "RIPPLE_LOADER_PAT2",
    "LIBRARY_CLAUDE_PAT",
})
KEEP_NAMES = frozenset({
    "LIBRARY_PAT",
    "RIPPLE_LOADER_PAT",
    "CLAUDE_MCP_RO",
    "PORTAL_RECON",
    "WAVE3_LOAD",
})


def _utc_iso(x) -> str | None:
    if x is None:
        return None
    if isinstance(x, dt.datetime):
        if x.tzinfo is None:
            return x.strftime("%Y-%m-%dT%H:%M:%SZ")
        return x.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return str(x)


def _fetch_tokens(cur) -> list[dict]:
    cur.execute("SHOW USER PROGRAMMATIC ACCESS TOKENS")
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, r)) for r in cur.fetchall()]


def _print_inventory(tokens: list[dict]) -> None:
    print(f"\n  live PATs on {USER}: {len(tokens)}")
    print(f"    {'NAME':<20} {'ROLE_RESTRICTION':<22} {'EXPIRES (UTC)':<21} {'STATUS':<8} PLAN")
    print(f"    {'-'*20} {'-'*22} {'-'*21} {'-'*8} ----")
    for t in tokens:
        name = t["name"]
        role = t.get("role_restriction") or "(unrestricted)"
        exp = _utc_iso(t.get("expires_at")) or "(none)"
        status = t.get("status") or ""
        if name in DROP_NAMES:
            plan = "DROP"
        elif name in KEEP_NAMES:
            plan = "keep"
        else:
            plan = "?? (left alone)"
        print(f"    {name:<20} {role:<22} {exp:<21} {status:<8} {plan}")


def _validate(tokens: list[dict]) -> tuple[bool, list[str]]:
    """Fail-safe guard. Returns (ok, problems)."""
    live = {t["name"] for t in tokens}
    problems: list[str] = []
    for n in sorted(DROP_NAMES):
        if n not in live:
            problems.append(f"DROP target '{n}' NOT found live -- allow-list does not match reality")
    for n in sorted(KEEP_NAMES):
        if n not in live:
            problems.append(f"KEEP token '{n}' MISSING live -- refusing to proceed")
    unknown = sorted(live - DROP_NAMES - KEEP_NAMES)
    for n in unknown:
        problems.append(f"unexpected live token '{n}' -- not in DROP or KEEP; will be LEFT ALONE, "
                        f"but review it")
    # unknown tokens are a warning (left alone), not a hard stop for the DROPs.
    hard_stop = any(not p.startswith("unexpected live token") for p in problems)
    return (not hard_stop), problems


def _drop_ddls(tokens: list[dict]) -> list[str]:
    by_name = {t["name"] for t in tokens}
    return [f'ALTER USER {USER} REMOVE PROGRAMMATIC ACCESS TOKEN "{n}";'
            for n in sorted(DROP_NAMES) if n in by_name]


def _build_ledger(current: dict, tokens: list[dict]) -> dict:
    """Non-destructive: preserve everything, refresh the PAT section to the 5 kept."""
    kept = [t for t in tokens if t["name"] in KEEP_NAMES]
    kept.sort(key=lambda t: t["name"])
    pat_rows = []
    for t in kept:
        pat_rows.append({
            "name": t["name"],
            "user": t.get("user_name") or USER,
            "role_restriction": t.get("role_restriction") or "",
            "expires": _utc_iso(t.get("expires_at")),
            "status": t.get("status"),
        })
    new = dict(current)  # shallow copy; we only touch a few top-level keys
    new["updated"] = dt.date.today().isoformat()
    new["programmatic_access_tokens"] = {
        "_about": ("Every LIVE programmatic access token on CROGG23, refreshed by "
                   "scripts/revoke_straggler_pats.py. SHOW USER PROGRAMMATIC ACCESS TOKENS "
                   "is the source of truth; this mirrors the KEPT set so the ledger stops "
                   "being a blind spot. Stragglers were revoked 2026-07-07."),
        "tokens": pat_rows,
    }
    return new


def _ledger_diff(current: dict, new: dict) -> None:
    cur_pats = (current.get("programmatic_access_tokens") or {}).get("tokens") or []
    cur_names = {p.get("name") for p in cur_pats}
    new_names = {p["name"] for p in new["programmatic_access_tokens"]["tokens"]}
    print("\n  ledger (infra/keys_ledger.json) diff:")
    print(f"    updated: {current.get('updated')} -> {new['updated']}")
    if "programmatic_access_tokens" not in current:
        print("    + adds NEW section 'programmatic_access_tokens' (was absent -- the blind spot)")
    print(f"    PAT rows tracked: {len(cur_names)} -> {len(new_names)}")
    for p in new["programmatic_access_tokens"]["tokens"]:
        tag = "+" if p["name"] not in cur_names else " "
        print(f"    {tag} {p['name']:<20} role={p['role_restriction'] or '(none)':<20} "
              f"exp={p['expires']}  [{p['status']}]")
    preserved = [k for k in current if k not in ("updated", "programmatic_access_tokens")]
    print(f"    preserved untouched: {', '.join(preserved)}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Revoke straggler PATs + refresh ledger.")
    ap.add_argument("--apply", action="store_true", help="perform the drops + ledger write (else preview)")
    args = ap.parse_args()

    from connect import db
    conn = db.connect()
    cur = conn.cursor()
    try:
        tokens = _fetch_tokens(cur)
        _print_inventory(tokens)

        ok, problems = _validate(tokens)
        if problems:
            print("\n  guard notes:")
            for p in problems:
                print(f"    [!] {p}")
        if not ok:
            print("\n  ABORT: allow-list does not match live tokens. Nothing dropped, "
                  "ledger untouched. (Fail-safe.)")
            return 2

        ddls = _drop_ddls(tokens)
        print(f"\n  would DROP {len(ddls)} token(s):")
        for d in ddls:
            print(f"    {d}")
        keep_present = sorted(n for n in KEEP_NAMES if n in {t['name'] for t in tokens})
        print(f"  would KEEP {len(keep_present)} token(s): {', '.join(keep_present)}")

        current_ledger = json.loads(LEDGER.read_text()) if LEDGER.exists() else {}
        new_ledger = _build_ledger(current_ledger, tokens)
        _ledger_diff(current_ledger, new_ledger)

        if not args.apply:
            print("\n  PREVIEW only -- nothing dropped, ledger not written. Re-run with --apply.")
            return 0

        # --- APPLY ---
        ts = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
        snap = REPO / "outputs" / f"_dropped_pats_{ts}.sql"
        snap.parent.mkdir(parents=True, exist_ok=True)
        dropped_meta = [t for t in tokens if t["name"] in DROP_NAMES]
        with open(snap, "w", encoding="utf-8") as f:
            f.write(f"-- PATs REMOVED from {USER} on {ts} by revoke_straggler_pats.py\n")
            f.write("-- REMOVE is IRREVERSIBLE: a PAT secret cannot be recreated. This file\n")
            f.write("-- records each dropped token's metadata. To restore access, generate a\n")
            f.write("-- NEW token in Snowsight (Admin > Users > CROGG23 > Programmatic access\n")
            f.write("-- tokens) with the same role_restriction and rewire the consumer.\n--\n")
            for t in dropped_meta:
                f.write(f"--   name={t['name']} role_restriction={t.get('role_restriction')!r} "
                        f"expires={_utc_iso(t.get('expires_at'))} status={t.get('status')} "
                        f"created_on={_utc_iso(t.get('created_on'))}\n")
            f.write("--\n-- The DROP statements that were run:\n")
            for d in ddls:
                f.write(d + "\n")
        print(f"\n  metadata snapshot -> {snap}")

        for d in ddls:
            cur.execute(d)
            print(f"    ran: {d}")

        # verify: live set is now exactly the KEEP set
        after = _fetch_tokens(cur)
        after_names = {t["name"] for t in after}
        still_present = sorted(DROP_NAMES & after_names)
        missing_keeps = sorted(KEEP_NAMES - after_names)
        print(f"\n  post-drop live PATs: {len(after)}")
        if still_present:
            print(f"    [!] still present (drop failed?): {still_present}")
        else:
            print("    all 5 stragglers gone.")
        if missing_keeps:
            print(f"    [!] a KEEP token vanished: {missing_keeps}")
        else:
            print(f"    all 5 keeps intact: {sorted(KEEP_NAMES)}")

        # rebuild ledger against the POST-drop live state (real expiries of the keeps)
        final_ledger = _build_ledger(current_ledger, after)
        LEDGER.write_text(json.dumps(final_ledger, indent=2) + "\n")
        print(f"  ledger refreshed -> {LEDGER}")
        print("\n  DONE.")
        return 0
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
