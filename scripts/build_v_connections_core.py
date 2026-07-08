"""Build the trustworthy-core connection view: LIBRARY_META.CONNECT.V_CONNECTIONS_CORE.

V_CONNECTIONS exposes ALL 41,241 edges from CONNECT_EDGES with NO tier filter -- and 53%
(~21,900) are bare ZIP/FIPS geographic coincidence (tier GEO) or PROBABILISTIC name-only
matches. For evidence.dev's connection browse that means the default view is majority noise.

V_CONNECTIONS_CORE is the SAME projection as V_CONNECTIONS, filtered to the hard-ID /
corroborated tiers only:

    tier IN ('STEEL','STRONG','CORROBORATED')   -- ~4,308 edges (STEEL 473 + STRONG 2224 + CORROBORATED 1611)

It selects straight FROM V_CONNECTIONS (not CONNECT_EDGES) so the projection can never drift
from the base view -- add a column there, it shows up here for free.

    python3 scripts/build_v_connections_core.py           # PREVIEW: DDL + the rowcount/tier split it WOULD have
    python3 scripts/build_v_connections_core.py --apply    # create/replace + grant + verify

COPY GRANTS + explicit re-GRANT SELECT to RIPPLE_READER and CLAUDE_MCP_READONLY so the
evidence read lane keeps SELECT across every rebuild (audit D04). Rollback DDL snapshotted
to outputs/ on --apply.
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")
REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

V_CONN = 'LIBRARY_META."CONNECT".V_CONNECTIONS'
V_CORE = 'LIBRARY_META."CONNECT".V_CONNECTIONS_CORE'
READ_ROLES = ("RIPPLE_READER", "CLAUDE_MCP_READONLY")
CORE_TIERS = ("STEEL", "STRONG", "CORROBORATED")

_TIER_LIST = ", ".join(f"'{t}'" for t in CORE_TIERS)

V_CORE_SQL = f"""
CREATE OR REPLACE VIEW {V_CORE} COPY GRANTS
COMMENT='Trustworthy core of the connection graph: the SAME projection as V_CONNECTIONS but
only tier IN ({"/".join(CORE_TIERS)}) -- hard identifiers + corroborated links, no bare
ZIP/FIPS geographic coincidence (GEO) or name-only (PROBABILISTIC) noise. This is the default
edge set evidence.dev should browse. Built over V_CONNECTIONS; regenerable.' AS
SELECT *
FROM {V_CONN}
WHERE tier IN ({_TIER_LIST})
"""


def _print_grants(cur, label: str) -> None:
    cur.execute(f"SHOW GRANTS ON VIEW {V_CORE}")
    rows = cur.fetchall()
    sel = sorted({str(r[4]) for r in rows if str(r[1]) == "SELECT"})
    print(f"  grants {label}: {len(rows)} total; SELECT -> {sel or 'NONE'}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Build V_CONNECTIONS_CORE (trustworthy tiers)")
    ap.add_argument("--apply", action="store_true", help="create the view (default: preview)")
    args = ap.parse_args()

    from connect import db
    conn = db.connect()
    cur = conn.cursor()
    try:
        # Live tier split off the base view -- proves the core rowcount before we build anything.
        cur.execute(f"""SELECT tier, COUNT(*) FROM {V_CONN} GROUP BY 1 ORDER BY 2 DESC""")
        split = cur.fetchall()
        total = sum(c for _t, c in split)
        core = sum(c for t, c in split if t in CORE_TIERS)
        print("=== live tier split on V_CONNECTIONS ===")
        for t, c in split:
            mark = "  <-- CORE" if t in CORE_TIERS else ""
            print(f"    {str(t):<15} {c:>7,}{mark}")
        print(f"    {'TOTAL':<15} {total:>7,}")
        print(f"\n  V_CONNECTIONS_CORE would have {core:,} rows "
              f"({core/total*100:.1f}% of {total:,}); "
              f"drops {total-core:,} GEO/PROBABILISTIC/BRIDGE edges.")

        print("\n=== V_CONNECTIONS_CORE DDL ===")
        print(V_CORE_SQL)
        for role in READ_ROLES:
            print(f"GRANT SELECT ON VIEW {V_CORE} TO ROLE {role};")

        if not args.apply:
            print("\n  PREVIEW only -- nothing created. Re-run with --apply.")
            return 0

        # --- APPLY --- snapshot rollback first (DROP; the view is net-new, so rollback = drop).
        ts = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
        cur.execute(f"SELECT COUNT(*) FROM INFORMATION_SCHEMA.VIEWS "
                    f"WHERE TABLE_CATALOG='LIBRARY_META' AND TABLE_SCHEMA='CONNECT' "
                    f"AND TABLE_NAME='V_CONNECTIONS_CORE'")
        existed = cur.fetchone()[0] > 0
        roll = REPO / "outputs" / f"_rollback_V_CONNECTIONS_CORE_{ts}.sql"
        if existed:
            cur.execute(f"SELECT GET_DDL('VIEW','{V_CORE}')")
            roll.write_text(cur.fetchone()[0].rstrip().rstrip(";") + ";\n")
            print(f"\n  view exists -- rollback = prior DDL snapshotted -> {roll}")
        else:
            roll.write_text(f"DROP VIEW IF EXISTS {V_CORE};\n")
            print(f"\n  view is net-new -- rollback = DROP snapshotted -> {roll}")

        print(f"  applying (CREATE OR REPLACE VIEW {V_CORE} ... COPY GRANTS) ...")
        cur.execute(V_CORE_SQL)
        _print_grants(cur, "after CREATE (COPY GRANTS)")
        for role in READ_ROLES:
            cur.execute(f"GRANT SELECT ON VIEW {V_CORE} TO ROLE {role}")
        _print_grants(cur, "after re-GRANT")

        cur.execute(f"SELECT COUNT(*) FROM {V_CORE}")
        live_core = cur.fetchone()[0]
        print(f"\n  V_CONNECTIONS_CORE rows live: {live_core:,} (expected {core:,}) "
              f"{'OK' if live_core == core else 'MISMATCH'}")
        cur.execute(f"SELECT tier, COUNT(*) FROM {V_CORE} GROUP BY 1 ORDER BY 2 DESC")
        for t, c in cur.fetchall():
            print(f"    {str(t):<15} {c:>7,}")
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
