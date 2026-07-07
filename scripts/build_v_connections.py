"""Build the friendly connection views over LIBRARY_META.CONNECT.CONNECT_EDGES.

CONNECT_EDGES is the raw graph (one row per table-A / table-B / key edge, with the
join columns). These views make it queryable for a human / evidence.dev:

  V_CONNECTIONS         one row per edge, readable: table + column on each side, the
                        join key, tier, confidence, overlap, BOTH sides' domain, and a
                        ready-to-run JOIN skeleton (a.col = b.col). Ordered so the
                        hard-ID, high-overlap edges surface first.
  V_CONNECTION_SUMMARY  browse menu: edge counts per (domain_a, domain_b, tier) so you
                        can see which domains actually connect and how strongly.

    python3 scripts/build_v_connections.py           # PREVIEW: DDL + sample rows
    python3 scripts/build_v_connections.py --apply   # create/replace + grant + verify

COPY GRANTS + a RIPPLE_READER grant so the read lane keeps SELECT across rebuilds.
"""
from __future__ import annotations

import argparse
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")
REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

EDGES = 'LIBRARY_META."CONNECT".CONNECT_EDGES'
V_CONN = 'LIBRARY_META."CONNECT".V_CONNECTIONS'
V_SUMM = 'LIBRARY_META."CONNECT".V_CONNECTION_SUMMARY'
READ_ROLE = "RIPPLE_READER"

V_CONNECTIONS_SQL = f"""
CREATE OR REPLACE VIEW {V_CONN} COPY GRANTS
COMMENT='One row per connection-graph edge, human-readable. table_a.col_a = table_b.col_b
is a runnable join. tier STEEL/STRONG = hard identifier; GEO/CORROBORATED/PROBABILISTIC
are softer. Built over CONNECT_EDGES; regenerable.' AS
SELECT
    e.A                         AS table_a,
    e.A_COL                     AS col_a,
    e.B                         AS table_b,
    e.B_COL                     AS col_b,
    e.KEY                       AS join_key,
    e.TIER                      AS tier,
    e.CONFIDENCE                AS confidence,
    e.MATCHED                   AS matched_values,
    e.MATCH_RATE                AS match_rate_pct,
    e.A_DISTINCT                AS a_distinct,
    e.B_DISTINCT                AS b_distinct,
    ca.DOMAIN_PRIMARY           AS domain_a,
    cb.DOMAIN_PRIMARY           AS domain_b,
    CASE WHEN e.A_COL IS NOT NULL AND e.B_COL IS NOT NULL THEN
        'SELECT a.*, b.* FROM LIBRARY_RAW.LANDING.' || e.A || ' a '
        || 'JOIN LIBRARY_RAW.LANDING.' || e.B || ' b '
        || 'ON a.' || e.A_COL || ' = b.' || e.B_COL
    END                         AS join_hint,
    e."SAMPLE"                  AS sample_values,
    e.BUILT_AT                  AS built_at
FROM {EDGES} e
LEFT JOIN LIBRARY_META.REGISTRY.CATALOG ca ON UPPER(ca.SOURCE_ID) = e.A
LEFT JOIN LIBRARY_META.REGISTRY.CATALOG cb ON UPPER(cb.SOURCE_ID) = e.B
"""

V_SUMMARY_SQL = f"""
CREATE OR REPLACE VIEW {V_SUMM} COPY GRANTS
COMMENT='Browse menu for the connection graph: edge counts and best overlap per
(domain_a, domain_b, tier). Which domains connect, and how strongly.' AS
SELECT
    domain_a,
    domain_b,
    tier,
    COUNT(*)                    AS edges,
    COUNT(DISTINCT table_a)     AS distinct_a_tables,
    COUNT(DISTINCT table_b)     AS distinct_b_tables,
    MAX(matched_values)         AS max_overlap,
    ROUND(AVG(confidence), 3)   AS avg_confidence
FROM {V_CONN}
GROUP BY 1, 2, 3
"""


def main() -> int:
    ap = argparse.ArgumentParser(description="Build V_CONNECTIONS / V_CONNECTION_SUMMARY")
    ap.add_argument("--apply", action="store_true", help="create the views (default: preview)")
    args = ap.parse_args()

    from connect import db

    if not args.apply:
        print("=== V_CONNECTIONS DDL ===")
        print(V_CONNECTIONS_SQL)
        print("=== V_CONNECTION_SUMMARY DDL ===")
        print(V_SUMMARY_SQL)
        print("\n  PREVIEW only -- nothing created. Re-run with --apply.")
        return 0

    conn = db.connect()
    cur = conn.cursor()
    try:
        cur.execute(V_CONNECTIONS_SQL)
        cur.execute(V_SUMMARY_SQL)
        for v in (V_CONN, V_SUMM):
            cur.execute(f"GRANT SELECT ON VIEW {v} TO ROLE {READ_ROLE}")
        print("  views created + granted to", READ_ROLE)

        cur.execute(f"SELECT COUNT(*) FROM {V_CONN}")
        print(f"  V_CONNECTIONS rows: {cur.fetchone()[0]:,}")
        print("\n  top hard-ID connections (STEEL/STRONG, by overlap):")
        cur.execute(f"""SELECT table_a, col_a, table_b, col_b, join_key, matched_values, tier
                        FROM {V_CONN} WHERE tier IN ('STEEL','STRONG')
                        ORDER BY matched_values DESC LIMIT 8""")
        for r in cur.fetchall():
            print(f"   {r[0][:30]:<30}.{r[1]:<12} = {r[2][:30]:<30}.{r[3]:<12} "
                  f"[{r[4]}] m={r[5]:,} {r[6]}")
        print("\n  domains that connect (top by edge count):")
        cur.execute(f"""SELECT domain_a, domain_b, tier, edges FROM {V_SUMM}
                        WHERE domain_a IS NOT NULL AND domain_b IS NOT NULL
                        ORDER BY edges DESC LIMIT 10""")
        for r in cur.fetchall():
            print(f"   {str(r[0])[:22]:<22} <-> {str(r[1])[:22]:<22} [{r[2]:<13}] {r[3]:,} edges")
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
