"""
doors — check both doors into the warehouse and say which one is broken, if any.

  Door 1: the Python scripts (connect/db.py -> library-onboarding/snow.py, PAT or key-pair)
  Door 2: the chat plug-in (Snowflake MCP server configured for Claude Code; its own token)

Never say "the warehouse is down." Say which door.
"""
from __future__ import annotations

import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def door_scripts() -> dict:
    t = time.time()
    try:
        from connect import db
        c = db.connect()
        (u, r, w, a) = db.rows(c, "select current_user(), current_role(), current_warehouse(), current_account()")[0]
        return {"door": "python scripts", "works": True, "user": u, "role": r, "warehouse": w, "secs": round(time.time() - t, 1)}
    except Exception as e:  # noqa: BLE001
        return {"door": "python scripts", "works": False, "error": str(e)[:160], "secs": round(time.time() - t, 1)}


def door_plugin() -> dict:
    """The plug-in runs inside Claude Code; from here we can only check its config and token freshness."""
    cands = [os.path.expanduser("~/.claude.json"), os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".mcp.json")]
    for p in cands:
        if os.path.exists(p):
            try:
                cfg = json.load(open(p, encoding="utf-8"))
            except Exception:  # noqa: BLE001
                continue
            servers = cfg.get("mcpServers", {}) or {}
            for k, v in servers.items():
                if "snow" in k.lower():
                    hdr = (v.get("headers") or {}).get("Authorization", "")
                    return {"door": "chat plug-in", "works": None, "config": p, "server": k,
                            "note": "token present — validity only known when Claude Code connects (401 = rejected, get a new token)" if hdr else "no Authorization header configured"}
    return {"door": "chat plug-in", "works": None, "note": "no Snowflake MCP server found in config"}


def main() -> int:
    rows = [door_scripts(), door_plugin()]
    for r in rows:
        print(" | ".join(f"{k}={v}" for k, v in r.items()))
    admin = any(r.get("role") == "ACCOUNTADMIN" for r in rows)
    if admin:
        print("WARNING: the scripts door runs as ACCOUNTADMIN — a wrong command has no safety net. RIPPLE_SERVE_ROLE exists in .env for a read-only login.")
    return 0 if rows[0]["works"] else 1


if __name__ == "__main__":
    sys.exit(main())
