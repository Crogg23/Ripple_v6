"""Phase 0 loader -- APPEND-ONLY registration of the political domain catalogue.

Safety (per the handoff Step-0 rules):
  * APPEND-ONLY: every write is `INSERT ... FROM (SELECT 1) WHERE NOT EXISTS
    (SELECT 1 ... WHERE SOURCE_ID=?)`. It NEVER updates, truncates, deletes,
    rebuilds, or CREATE-OR-REPLACEs the registry. A SOURCE_ID that already
    exists is left exactly as the other session owns it.
  * IDEMPOTENT: re-running inserts nothing new.
  * CONCURRENCY-SAFE: only touches the political SOURCE_IDs in this catalogue.

Usage:
  python politics/registry/register_political_sources.py            # PREVIEW (no writes)
  python politics/registry/register_political_sources.py --apply    # do the INSERTs
"""
from __future__ import annotations
import json
import sys

sys.path.insert(0, r"c:\Code\Ripple_v6\library-onboarding")
import snow  # noqa: E402

sys.path.insert(0, r"c:\Code\Ripple_v6\politics\registry")
import political_sources as cat  # noqa: E402

FQT = '"LIBRARY_META"."REGISTRY"."SOURCE_REGISTRY"'


def _encode(col, val):
    if col in cat.ARRAY_COLUMNS:
        return json.dumps(list(val) if val else [])
    return val


def _insert_sql():
    select_exprs = ", ".join(
        f"PARSE_JSON(%s)" if c in cat.ARRAY_COLUMNS else "%s" for c in cat.INSERT_COLUMNS
    )
    cols = ", ".join(cat.INSERT_COLUMNS)
    return (
        f"INSERT INTO {FQT} ({cols}) "
        f"SELECT {select_exprs} FROM (SELECT 1) "
        f"WHERE NOT EXISTS (SELECT 1 FROM {FQT} WHERE SOURCE_ID = %s)"
    )


def main(apply: bool):
    rows = cat.all_rows()
    conn = snow.connect()
    cur = conn.cursor()

    # Which already exist right now (live check)?
    ids = [r["SOURCE_ID"] for r in rows]
    inlist = ", ".join("%s" for _ in ids)
    cur.execute(f"SELECT SOURCE_ID FROM {FQT} WHERE SOURCE_ID IN ({inlist})", tuple(ids))
    existing = {r[0] for r in cur.fetchall()}

    to_insert = [r for r in rows if r["SOURCE_ID"] not in existing]
    skipped = [r for r in rows if r["SOURCE_ID"] in existing]

    print("=" * 78)
    print(f"PHASE 0 REGISTRY -- {'APPLY' if apply else 'PREVIEW (no writes)'}")
    print("=" * 78)
    print(f"Catalogue rows : {len(rows)}  ({len(cat.SOURCES)} sources + {len(cat.GAP_BUCKETS)} gap buckets)")
    print(f"Already present: {len(skipped)}  -> SKIP (append-only, untouched)")
    print(f"To INSERT      : {len(to_insert)}")
    if skipped:
        print("  skip:", ", ".join(sorted(r["SOURCE_ID"] for r in skipped)))
    print("-" * 78)

    sql = _insert_sql()
    inserted = 0
    for r in to_insert:
        params = tuple(_encode(c, r[c]) for c in cat.INSERT_COLUMNS) + (r["SOURCE_ID"],)
        tag = "INC" if r.get("INCLUDE") == "Y" else "GAP"
        if apply:
            cur.execute(sql, params)
            n = cur.rowcount or 0
            inserted += n
            print(f"  [{tag}] {'INSERTED' if n else 'noop'}  {r['SOURCE_ID']:<34} {r['DOMAIN_PRIMARY']}")
        else:
            print(f"  [{tag}] WOULD INSERT {r['SOURCE_ID']:<34} {r['DOMAIN_PRIMARY']:<20} "
                  f"tier={r['PRIORITY_TIER']} jkt={r['JOIN_KEY_TIER']}")

    if apply:
        conn.commit()
        print("-" * 78)
        print(f"COMMITTED. Rows inserted: {inserted}")
        # Reviewable table: everything this session's provenance now owns.
        cur.execute(
            f"SELECT SOURCE_ID, DOMAIN_PRIMARY, PRIORITY_TIER, INCLUDE, JOIN_KEY_TIER, "
            f"LEFT(NAME, 46) AS NAME FROM {FQT} WHERE DOMAIN_SOURCE = %s ORDER BY INCLUDE DESC, "
            f"PRIORITY_TIER, SOURCE_ID",
            (cat.PROVENANCE,),
        )
        print("\nREVIEWABLE TABLE -- rows owned by DOMAIN_SOURCE='politics_domain':")
        print(f"{'SOURCE_ID':<34} {'DOMAIN':<20} {'T':<2} {'INC':<4} {'JKT':<14} NAME")
        for sid, dom, tier, inc, jkt, name in cur.fetchall():
            print(f"{sid:<34} {dom:<20} {tier:<2} {inc:<4} {jkt:<14} {name}")

    cur.close()
    conn.close()


if __name__ == "__main__":
    main(apply="--apply" in sys.argv)
