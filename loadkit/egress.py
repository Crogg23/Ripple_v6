"""Egress rule management for server-side bulk loads.

Parses all spec URLs, diffs against the current RIPPLE_BULK_EGRESS network rule,
and outputs the ALTER statement needed to add missing hosts. Integrated into
`ripple pour plan` for pre-flight visibility.

Usage (standalone):
    python -m loadkit.egress --check          # show missing hosts (read-only)
    python -m loadkit.egress --apply          # execute ALTER to add them

Design:
  - Pure `diff_hosts()` is unit-testable (no I/O).
  - `fetch_current_hosts()` queries Snowflake (DESCRIBE NETWORK RULE).
  - `patch_statement()` returns the SQL string; `apply()` runs it.
"""
from __future__ import annotations

import sys
from pathlib import Path
from urllib.parse import urlparse


# ---------------------------------------------------------------------------
# Pure logic (unit-testable)
# ---------------------------------------------------------------------------

def hosts_from_specs(specs: list[dict]) -> set[str]:
    """Extract all hostnames that server-side specs need egress access to."""
    hosts = set()
    for spec in specs:
        loader = spec.get("loader", "bridge_fuel")
        # Only server_side specs need egress (bridge_fuel fetches via laptop)
        if loader not in ("server_side",) and not spec.get("resolver"):
            # Also include bridge_fuel specs that HAVE a resolver (they use server-side fetch)
            if not spec.get("resolver"):
                continue
        for url_field in ("download_url", "url"):
            url = spec.get(url_field) or ""
            if url:
                h = urlparse(url).hostname
                if h:
                    hosts.add(h.lower())
        resolver = spec.get("resolver")
        if resolver and isinstance(resolver, dict):
            r_url = resolver.get("url", "")
            if r_url:
                h = urlparse(r_url).hostname
                if h:
                    hosts.add(h.lower())
    return hosts


def diff_hosts(needed: set[str], current: set[str]) -> set[str]:
    """Return hosts that are needed but not yet on the egress rule."""
    return needed - current


def patch_statement(missing: set[str], current: set[str],
                    rule_name: str = "LIBRARY_RAW.LANDING.RIPPLE_BULK_EGRESS") -> str:
    """Generate ALTER NETWORK RULE to add missing hosts to the VALUE_LIST.

    Snowflake's ALTER NETWORK RULE ... SET VALUE_LIST replaces the entire list,
    so we emit the full set (current + missing).
    """
    full = sorted(current | missing)
    values = ",\n    ".join(f"'{h}'" for h in full)
    return (
        f"ALTER NETWORK RULE {rule_name}\n"
        f"  SET VALUE_LIST = (\n    {values}\n  );"
    )


# ---------------------------------------------------------------------------
# Live I/O (not unit-tested)
# ---------------------------------------------------------------------------

def fetch_current_hosts(conn=None) -> set[str]:
    """Query the current VALUE_LIST from RIPPLE_BULK_EGRESS. Returns lowercase hostnames."""
    close = False
    if conn is None:
        try:
            sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "library-onboarding"))
            from snow import connect
            conn = connect()
            close = True
        except Exception:
            return set()

    try:
        cur = conn.cursor()
        cur.execute("DESCRIBE NETWORK RULE LIBRARY_RAW.LANDING.RIPPLE_BULK_EGRESS")
        rows = cur.fetchall()
        # The DESCRIBE output has columns: name, property, property_type, property_value
        # VALUE_LIST is one of the properties
        hosts = set()
        for row in rows:
            if len(row) >= 4 and row[1] and "VALUE_LIST" in str(row[1]).upper():
                # property_value is a comma-separated list of hosts
                val = str(row[3]) if row[3] else ""
                for h in val.replace("[", "").replace("]", "").replace("'", "").replace('"', '').split(","):
                    h = h.strip().lower()
                    if h:
                        hosts.add(h)
        return hosts
    except Exception:
        return set()
    finally:
        if close:
            try:
                conn.close()
            except Exception:
                pass


def check(specs: list[dict], conn=None) -> dict:
    """Check egress coverage. Returns {needed, current, missing, patch_sql}."""
    needed = hosts_from_specs(specs)
    current = fetch_current_hosts(conn)
    missing = diff_hosts(needed, current)
    patch_sql = patch_statement(missing, current) if missing else ""
    return {
        "needed": needed,
        "current": current,
        "missing": missing,
        "patch_sql": patch_sql,
    }


def apply(specs: list[dict], conn=None) -> str:
    """Check and apply egress patch if needed. Returns status message."""
    result = check(specs, conn)
    if not result["missing"]:
        return f"Egress OK: all {len(result['needed'])} hosts already allowed."
    # Execute the patch
    close = False
    if conn is None:
        sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "library-onboarding"))
        from snow import connect
        conn = connect()
        close = True
    try:
        cur = conn.cursor()
        cur.execute(result["patch_sql"])
        return f"Added {len(result['missing'])} hosts: {', '.join(sorted(result['missing']))}"
    finally:
        if close:
            try:
                conn.close()
            except Exception:
                pass


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Manage RIPPLE_BULK_EGRESS network rule")
    parser.add_argument("--apply", action="store_true", help="Execute ALTER to add missing hosts")
    parser.add_argument("--check", action="store_true", help="Show missing hosts (default)")
    args = parser.parse_args()

    # Load all spec modules
    repo = Path(__file__).resolve().parents[1]
    scripts = repo / "scripts"
    sys.path.insert(0, str(scripts))
    all_specs = []
    for mod_name in ("bridge_fuel_specs", "backfill_specs", "server_side_specs"):
        try:
            mod = __import__(mod_name)
            all_specs.extend(getattr(mod, "SPECS", []))
        except Exception:
            pass
    # Also load any sprint specs
    for p in (repo / "scripts").glob("sprint_*_specs.py"):
        try:
            import importlib.util
            spec_ = importlib.util.spec_from_file_location(p.stem, str(p))
            mod = importlib.util.module_from_spec(spec_)
            spec_.loader.exec_module(mod)
            all_specs.extend(getattr(mod, "SPECS", []))
        except Exception:
            pass

    result = check(all_specs)
    if result["missing"]:
        print(f"MISSING from egress rule ({len(result['missing'])} hosts):")
        for h in sorted(result["missing"]):
            print(f"  + {h}")
        if args.apply:
            msg = apply(all_specs)
            print(f"\n{msg}")
        else:
            print(f"\nSQL to fix:\n{result['patch_sql']}")
            print("\nRun with --apply to execute.")
    else:
        print(f"Egress OK: all {len(result['needed'])} needed hosts are on the rule.")
