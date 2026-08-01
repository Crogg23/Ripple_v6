"""Build LIBRARY_META.REGISTRY.COLUMN_CATALOG — the per-column dictionary.

PERSISTS what the platform already computes and throws away:
  * viz/catalog.py columns() + profile()  -> type, chart role, fill rate,
    digit-date trap flag, distinct count (READER lane, cached)
  * connect/keys.py detect_key + normalize_sql -> hard-ID key, tier, and a
    VALUE-MEASURED populated% (imported, never re-implemented — the
    normalize_sql drift trap of 2026-07-31 is why)
  * a 5-value sample probe per column
  * plain-English gloss: curated glossary/column_gloss.py wins, else
    glossary.heuristic_gloss

Usage:
    python scripts/build_column_catalog.py                # preview: plan only
    python scripts/build_column_catalog.py --apply        # full rebuild
    python scripts/build_column_catalog.py --only FQN[,FQN...] [--apply]

Writes ride the standard loader lane (library-onboarding .env SNOWFLAKE_PAT —
the same lane that writes LIBRARY_META.REGISTRY). Reads ride the viz read
lane. The one-time CREATE+GRANT lives in infra/ddl/06_column_catalog.sql.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "library-onboarding"))

from dotenv import load_dotenv  # noqa: E402

# The read lane needs SNOWFLAKE_SERVE_PAT in the environment BEFORE sqlrun
# connects (repo rule: .env wins over stale shell env).
load_dotenv(REPO / "library-onboarding" / ".env", override=True)

import glossary  # noqa: E402
from glossary.column_gloss import COLUMN_GLOSS, STAR  # noqa: E402
from connect import keys as connect_keys  # noqa: E402
from viz import catalog as viz_catalog  # noqa: E402
from viz import guard as viz_guard  # noqa: E402
from viz import sqlrun  # noqa: E402

TABLE = "LIBRARY_META.REGISTRY.COLUMN_CATALOG"
SAMPLE_N = 5
SAMPLE_TRUNC = 60
PROFILE_N = 10_000
META_COLS = {"_INGESTED_AT", "_SOURCE_RUN_ID", "_SRC_SHA256",
             "INGESTED_AT", "SOURCE_RUN_ID", "SRC_SHA256"}


def target_fqns() -> list[str]:
    """The same two arms viz.catalog browses: landed catalog sources + the
    LIBRARY_MARTS base tables."""
    landed = sqlrun.run(
        """SELECT DISTINCT LANDING_FQN FROM LIBRARY_META.REGISTRY.CATALOG
           WHERE LIFECYCLE IN ('landed','modeled','sampled')
             AND LANDED_ROW_COUNT > 0 AND LANDING_FQN IS NOT NULL
           ORDER BY 1""", limit_rows=5000)[0]
    marts = sqlrun.run(
        """SELECT TABLE_CATALOG || '.' || TABLE_SCHEMA || '.' || TABLE_NAME AS FQN
           FROM LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES
           WHERE TABLE_TYPE = 'BASE TABLE'
             AND TABLE_SCHEMA <> 'INFORMATION_SCHEMA'
             AND NOT STARTSWITH(TABLE_SCHEMA, '_')
           ORDER BY 1""", limit_rows=5000)[0]
    out: list[str] = []
    for df in (landed, marts):
        col = df.columns[0]
        out.extend(str(v) for v in df[col].dropna().tolist())
    return sorted(set(out))


def resolve_gloss(fqn: str, column: str, detected_key: str | None,
                  chart_role: str | None) -> tuple[str, str]:
    cu = COLUMN_GLOSS.get((fqn, column.upper())) \
        or COLUMN_GLOSS.get((STAR, column.upper()))
    if cu:
        return cu, "curated"
    return glossary.heuristic_gloss(column, detected_key, chart_role), "heuristic"


def profile_fqn(fqn: str) -> list[dict]:
    """One table -> COLUMN_CATALOG rows (dicts)."""
    safe = viz_guard.validate_fqn(fqn)
    cols = viz_catalog.columns(safe)
    prof = {p["column"]: p for p in viz_catalog.profile(safe, n=PROFILE_N)}

    # sample values, one batched query (ARRAY_SLICE(ARRAY_AGG(DISTINCT ...)))
    probe_cols = [c["column"] for c in cols
                  if c["column"].upper() not in META_COLS][:60]
    samples: dict[str, list] = {}
    if probe_cols:
        exprs = ", ".join(
            f"ARRAY_SLICE(ARRAY_AGG(DISTINCT LEFT(TO_VARCHAR("
            f"{viz_guard.quote_ident(c)}), {SAMPLE_TRUNC})) , 0, {SAMPLE_N})"
            f" AS S_{i}"
            for i, c in enumerate(probe_cols))
        try:
            df = sqlrun.run(
                f"SELECT {exprs} FROM (SELECT * FROM {safe} LIMIT {PROFILE_N})",
                limit_rows=2)[0]
            if len(df):
                row = df.iloc[0]
                for i, c in enumerate(probe_cols):
                    samples[c] = row.get(f"S_{i}".upper()) or row.get(f"S_{i}")
        except Exception as exc:  # sampling is best-effort, never fatal
            print(f"  [warn] sample probe failed for {fqn}: {exc}")

    rows = []
    for ordinal, c in enumerate(cols, start=1):
        name, sf_type = c["column"], c["sf_type"]
        if name.upper() in META_COLS:
            continue
        p = prof.get(name, {})
        key, tier = connect_keys.detect_key(name)
        key_pop = None
        if key:
            try:
                norm = connect_keys.normalize_sql(key, viz_guard.quote_ident(name))
                df = sqlrun.run(
                    f"SELECT ROUND(100 * COUNT({norm}) / GREATEST(COUNT(*), 1), 1)"
                    f" AS P FROM (SELECT * FROM {safe} LIMIT {PROFILE_N})",
                    limit_rows=2)[0]
                key_pop = float(df.iloc[0]["P"]) if len(df) else None
            except Exception:
                key_pop = None  # unmeasurable key stays honest as NULL
        gloss_text, gloss_src = resolve_gloss(fqn, name, key, p.get("role"))
        rows.append({
            "FQN": fqn, "COLUMN_NAME": name, "ORDINAL": ordinal,
            "SF_TYPE": sf_type, "CHART_ROLE": p.get("role"),
            "DIGIT_DATE": bool(p.get("digit_date")),
            "NONNULL_PCT": p.get("nonnull_pct"),
            "DISTINCT_SAMPLED": p.get("distinct_sampled"),
            "DETECTED_KEY": key, "KEY_TIER": tier,
            "KEY_POPULATED_PCT": key_pop,
            "PLAIN_GLOSS": gloss_text, "GLOSS_SOURCE": gloss_src,
            "SAMPLE_VALUES": samples.get(name),
            "PROFILE_N": PROFILE_N,
        })
    return rows


def write_rows(conn, fqn: str, rows: list[dict]) -> None:
    """One DELETE + ONE multi-row INSERT per table. Built as a single
    INSERT ... SELECT ... FROM VALUES statement with a flat parameter list —
    the connector's executemany rewrite cannot handle an INSERT..SELECT
    form (error 252001, live 2026-08-01), so we do the batching ourselves."""
    import json
    cur = conn.cursor()
    cur.execute(f"DELETE FROM {TABLE} WHERE FQN = %s", (fqn,))
    if not rows:
        return
    tuple_sql = "(" + ",".join(["%s"] * 15) + ")"
    values_sql = ",".join([tuple_sql] * len(rows))
    flat: list = []
    for r in rows:
        flat.extend([
            r["FQN"], r["COLUMN_NAME"], r["ORDINAL"], r["SF_TYPE"],
            r["CHART_ROLE"], r["DIGIT_DATE"], r["NONNULL_PCT"],
            r["DISTINCT_SAMPLED"], r["DETECTED_KEY"], r["KEY_TIER"],
            r["KEY_POPULATED_PCT"], r["PLAIN_GLOSS"], r["GLOSS_SOURCE"],
            json.dumps(r["SAMPLE_VALUES"], default=str)
            if r["SAMPLE_VALUES"] is not None else None,
            r["PROFILE_N"]])
    cur.execute(
        f"""INSERT INTO {TABLE}
            (FQN, COLUMN_NAME, ORDINAL, SF_TYPE, CHART_ROLE, DIGIT_DATE,
             NONNULL_PCT, DISTINCT_SAMPLED, DETECTED_KEY, KEY_TIER,
             KEY_POPULATED_PCT, PLAIN_GLOSS, GLOSS_SOURCE, SAMPLE_VALUES,
             PROFILE_N)
            SELECT c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,
                   TRY_PARSE_JSON(c14),c15
            FROM VALUES {values_sql}
              AS v(c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,c14,c15)""",
        tuple(flat))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--apply", action="store_true",
                    help="write to the warehouse (default: preview plan only)")
    ap.add_argument("--only", default=None,
                    help="comma-separated FQNs to (re)profile")
    ap.add_argument("--packs", action="store_true",
                    help="profile ONLY the tables the Playground question "
                         "packs reference (~30 tables, minutes not hours) — "
                         "the fast path to a working dictionary")
    args = ap.parse_args()

    if args.only:
        fqns = [f.strip() for f in args.only.split(",") if f.strip()]
    elif args.packs:
        from playground.packs import PACKS
        fqns = sorted({t["fqn"] for p in PACKS for t in p["tables"]})
    else:
        fqns = target_fqns()
    print(f"COLUMN_CATALOG build plan: {len(fqns)} tables"
          f" ({'APPLY' if args.apply else 'PREVIEW - no writes'})")
    if not args.apply:
        for f in fqns[:40]:
            print("  ", f)
        if len(fqns) > 40:
            print(f"   ... and {len(fqns) - 40} more")
        print("re-run with --apply to profile and write.")
        return 0

    import snow  # the loader lane (library-onboarding .env), writes REGISTRY
    conn = snow.connect()
    done = failed = 0
    for fqn in fqns:
        try:
            rows = profile_fqn(fqn)
            write_rows(conn, fqn, rows)
            done += 1
            print(f"  ok  {fqn}  ({len(rows)} columns)")
        except Exception as exc:
            failed += 1
            print(f"  FAIL {fqn}: {exc}")
    print(f"done: {done} tables written, {failed} failed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
