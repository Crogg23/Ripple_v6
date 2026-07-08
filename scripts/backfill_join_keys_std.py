#!/usr/bin/env python3
"""Measure the REAL join keys every landed source carries and write them to the
catalog facet JOIN_KEYS_STD (+ JOIN_KEY_TIER + JOIN_KEY_TIER_PROVISIONAL=FALSE).

The problem (verified live 2026-07-07): of the 200 landed+modeled sources, 150
carry an EMPTY JOIN_KEYS_STD and 142 are PROVISIONAL (JOIN_KEY_TIER_PROVISIONAL=
TRUE == the key facet was guessed at onboard time, never measured from real
columns). Downstream (evidence.dev / V_SOURCE_KEY / the connection graph browse)
can only filter "everything carrying an EIN / IMO / NPI" on the sources whose keys
were actually MEASURED. This backfills that.

How it measures (reuses the exact connect discipline -- no new tagger)
---------------------------------------------------------------------
Per source, per non-provenance column:
  1. NAME detect  -- connect/keys.py detect_key() tags a standard join key
     (EIN/NPI/CIK/UEI/DUNS/LEI/IMO/MMSI/CCN/PATENT/DOCKET/NAICS/NCES/SIC/
      FIPS/ZIP/LATLON/COUNTRY/GEOM/NAME/ADDRESS), strongest tier wins. Tight by
     design -- a column literally named "npi", never a substring ("protein").
  2. VALUE measure -- go to the DATA (a bounded row sample) and prove the column
     actually HOLDS that key's shape, using connect/keys.py normalize_sql() (the
     same canonicalizer connect joins on): a column named EIN that's 100% empty,
     numeric noise, or the all-zero placeholder normalizes to NULL and is REJECTED.
     This is the half column-name tagging can't do -- a dead key never gets written.

A key is CONFIRMED for the source if any of its columns clears all three gates:
  nonnull >= MIN_NONNULL  AND  distinct >= MIN_DISTINCT  AND  populated_pct >= MIN_POP_PCT
JOIN_KEYS_STD = the confirmed keys (tier-sorted); JOIN_KEY_TIER = the strongest tier.

D20 guard (never downgrade a curated facet)
-------------------------------------------
We ONLY write rows where JOIN_KEY_TIER_PROVISIONAL = TRUE -- i.e. never-measured
guesses. The 58 already-measured sources (provisional=FALSE) are a curated,
trusted facet and are NEVER touched. The SET also uses register.py's exact D20
idiom -- JOIN_KEYS_STD = IFF(ARRAY_SIZE(measured)>0, measured, JOIN_KEYS_STD),
JOIN_KEY_TIER = COALESCE(NULLIF(measured,'NONE'), JOIN_KEY_TIER) -- so an empty
measure can never blank a populated value. A provisional row we measure NOTHING
on is left provisional (honest: still unmeasured), never flipped. Idempotent:
after --apply a written row is provisional=FALSE, so the WHERE excludes it on
re-run (0 rows) -- re-running is a safe no-op.

This is a CATALOG mutation -> classifier-gated. PREVIEW is the default (reads
only, prints per-source what it WOULD write). CHRIS runs --apply. --apply
snapshots the whole registry to a backup table AND writes a per-source rollback
UPDATE script to outputs/ before touching a single row.

    python3 scripts/backfill_join_keys_std.py               # PREVIEW (reads only)
    python3 scripts/backfill_join_keys_std.py --limit 40     # PREVIEW first 40 (validation)
    python3 scripts/backfill_join_keys_std.py --apply        # Chris: write measured keys
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO / "library-onboarding"))
sys.path.insert(0, str(_REPO / "connect"))
try:
    from dotenv import load_dotenv
    load_dotenv(_REPO / "library-onboarding/.env", override=True)
except Exception:  # pragma: no cover
    pass

import snow  # noqa: E402
from keys import (  # noqa: E402
    KEY_TOKENS, TIER_RANK, detect_key, join_mode, normalize_sql, quote_ident,
)

REGISTRY = "LIBRARY_META.REGISTRY.SOURCE_REGISTRY"
CATALOG = "LIBRARY_META.REGISTRY.CATALOG"
RAW_SCHEMA_FQN = "LIBRARY_RAW.LANDING"
REPORT_DIR = _REPO / "outputs"
_TS = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
BACKUP = f"LIBRARY_META.REGISTRY._SOURCE_REGISTRY_BAK_JOINKEYS_{_TS}"
ROLLBACK = REPORT_DIR / f"_rollback_join_keys_std_{_TS}.sql"
REPORT = REPORT_DIR / "join_keys_std_backfill_report.md"

# --- measurement gates (a key must clear ALL three, over the sample) ---
SAMPLE_ROWS = 50_000     # bounded row sample -> cheap even on the 13M/19M-row tables
MAX_KEY_COLS = 16        # guard against a runaway per-table aggregate (matches fingerprint.py)
MIN_NONNULL = 5          # at least this many rows carry a valid value
MIN_DISTINCT = 2         # a real key varies; a lone constant that happens to be valid-shaped is not one
MIN_POP_PCT = 0.5        # >= this % of sampled rows carry a valid value (survives placeholder-heavy real IDs)

# provenance columns never carry a real join key (CLAUDE.md audit cols, with and
# without the leading underscore -- the portal harvests dropped the underscore).
_AUDIT_COLUMN_NAMES = {"INGESTED_AT", "SOURCE_RUN_ID", "SRC_SHA256"}


# --------------------------------------------------------------------------- #
# scope + columns (one query each, up front -- never per-source round trips)
# --------------------------------------------------------------------------- #
def fetch_scope(cur) -> list[dict]:
    cur.execute(
        f"""
        SELECT c.source_id, c.lifecycle,
               r.JOIN_KEYS_STD, r.JOIN_KEY_TIER, r.JOIN_KEY_TIER_PROVISIONAL,
               (r.source_id IS NOT NULL) AS has_row
        FROM {CATALOG} c
        LEFT JOIN {REGISTRY} r ON r.source_id = c.source_id
        WHERE c.lifecycle IN ('landed','modeled')
        ORDER BY c.source_id
        """
    )
    out = []
    for sid, life, jks, tier, prov, has_row in cur.fetchall():
        cur_keys = []
        if jks:
            try:
                cur_keys = list(json.loads(jks)) if isinstance(jks, str) else list(jks)
            except (ValueError, TypeError):
                cur_keys = []
        out.append({
            "source_id": sid, "lifecycle": life,
            "cur_keys": cur_keys, "cur_tier": tier,
            "provisional": bool(prov) if prov is not None else True,
            "has_row": bool(has_row),
        })
    return out


def fetch_all_columns(cur) -> dict[str, list[str]]:
    """{TABLE_NAME: [col, ...]} for every LANDING table, one query. Provenance
    columns (leading '_' or a bare audit name) are dropped up front."""
    cur.execute(
        "SELECT table_name, column_name "
        "FROM LIBRARY_RAW.INFORMATION_SCHEMA.COLUMNS "
        "WHERE table_schema='LANDING' "
        "ORDER BY table_name, ordinal_position"
    )
    out: dict[str, list[str]] = defaultdict(list)
    for table, col in cur.fetchall():
        if col.startswith("_") or col in _AUDIT_COLUMN_NAMES:
            continue
        out[table].append(col)
    return out


# --------------------------------------------------------------------------- #
# measurement -- exactly connect/fingerprint.py's discipline, over a sample
# --------------------------------------------------------------------------- #
def key_columns(colnames: list[str]) -> list[dict]:
    out = []
    for c in colnames:
        key, tier = detect_key(c)
        if key:
            out.append({"column": c, "key": key, "tier": tier, "mode": join_mode(key)})
    return out


def _measure_exprs(kc: dict) -> tuple[str, str]:
    """(nonnull_expr, distinct_arg) for a key column. Value keys canonicalize via
    keys.py normalize_sql (NULL for non-conforming/placeholder values); spatial
    keys get a shape-appropriate validity check."""
    qc = quote_ident(kc["column"])
    if kc["mode"] == "value":
        expr = normalize_sql(kc["key"], qc)
        return f"COUNT({expr})", f"APPROX_COUNT_DISTINCT({expr})"
    if kc["key"] == "LATLON":
        expr = f"CASE WHEN TRY_TO_DOUBLE(TO_VARCHAR({qc})) BETWEEN -180 AND 180 THEN 1 END"
        return f"COUNT({expr})", f"APPROX_COUNT_DISTINCT(TRY_TO_DOUBLE(TO_VARCHAR({qc})))"
    # GEOM / other spatial: any non-empty value counts (name is the real signal)
    expr = f"NULLIF(TRIM(TO_VARCHAR({qc})),'')"
    return f"COUNT({expr})", f"APPROX_COUNT_DISTINCT({expr})"


def measure_source(cur, source_id: str, colnames: list[str]) -> dict:
    """Return the measured verdict for a source: confirmed keys, strongest tier,
    and per-column detail (for the report)."""
    keycols = key_columns(colnames)
    if not keycols:
        return {"keys": [], "tier": "NONE", "cols": [], "sampled": 0, "no_key_cols": True}

    measured = keycols[:MAX_KEY_COLS]
    selects = ["COUNT(*) AS n"]
    for i, kc in enumerate(measured):
        nn, nd = _measure_exprs(kc)
        selects.append(f"{nn} AS nn_{i}")
        selects.append(f"{nd} AS nd_{i}")

    fqn = f'{RAW_SCHEMA_FQN}."{source_id.upper()}"'
    cur.execute(f"SELECT {', '.join(selects)} FROM {fqn} SAMPLE ({SAMPLE_ROWS} ROWS)")
    row = cur.fetchone()
    n = int(row[0] or 0)

    best: dict[str, dict] = {}   # key -> best-column detail
    detail = []
    for i, kc in enumerate(measured):
        nn = int(row[1 + i * 2] or 0)
        nd = int(row[2 + i * 2] or 0)
        pop = (nn / n * 100) if n else 0.0
        ok = nn >= MIN_NONNULL and nd >= MIN_DISTINCT and pop >= MIN_POP_PCT
        d = {"column": kc["column"], "key": kc["key"], "tier": kc["tier"],
             "nonnull": nn, "distinct": nd, "pop_pct": round(pop, 2), "confirmed": ok}
        detail.append(d)
        if ok and (kc["key"] not in best or pop > best[kc["key"]]["pop_pct"]):
            best[kc["key"]] = d

    keys = sorted(best.keys(), key=lambda k: (TIER_RANK[KEY_TOKENS[k][0]], k))
    tier = KEY_TOKENS[keys[0]][0] if keys else "NONE"
    return {"keys": keys, "tier": tier, "cols": detail, "sampled": n, "no_key_cols": False}


# --------------------------------------------------------------------------- #
# the guarded UPDATE (D20): only provisional rows, never blank a populated value
# --------------------------------------------------------------------------- #
def _update_sql() -> str:
    return (
        f"UPDATE {REGISTRY}\n"
        f"   SET JOIN_KEYS_STD = IFF(ARRAY_SIZE(PARSE_JSON(%s))>0, PARSE_JSON(%s), JOIN_KEYS_STD),\n"
        f"       JOIN_KEY_TIER = COALESCE(NULLIF(%s,'NONE'), JOIN_KEY_TIER),\n"
        f"       JOIN_KEY_TIER_PROVISIONAL = FALSE\n"
        f" WHERE source_id = %s AND JOIN_KEY_TIER_PROVISIONAL = TRUE"
    )


def main() -> int:
    ap = argparse.ArgumentParser(description="Measure + backfill JOIN_KEYS_STD for landed sources.")
    ap.add_argument("--apply", action="store_true", help="write measured keys (default: preview only)")
    ap.add_argument("--limit", type=int, default=None, help="cap sources profiled (validation runs)")
    args = ap.parse_args()

    conn = snow.connect()
    try:
        cur = conn.cursor()
        scope = fetch_scope(cur)
        all_cols = fetch_all_columns(cur)
        if args.limit:
            scope = scope[: args.limit]

        print("=" * 80)
        print(f"JOIN_KEYS_STD backfill  --  {len(scope)} landed/modeled sources "
              f"({'APPLY' if args.apply else 'PREVIEW'})")
        print(f"gates: nonnull>={MIN_NONNULL}  distinct>={MIN_DISTINCT}  pop>={MIN_POP_PCT}%  "
              f"sample={SAMPLE_ROWS:,} rows")
        print("=" * 80)

        buckets = {"WRITE": [], "SKIP_MEASURED": [], "SKIP_NO_MEASURE": [],
                   "NO_TABLE": [], "NO_REGISTRY_ROW": []}
        t0 = time.time()
        for i, src in enumerate(scope, start=1):
            sid = src["source_id"]
            if not src["has_row"]:
                buckets["NO_REGISTRY_ROW"].append(src)
                continue
            colnames = all_cols.get(sid.upper())
            if not colnames:
                buckets["NO_TABLE"].append(src)
                continue

            m = measure_source(cur, sid, colnames)
            src["measured"] = m

            if not src["provisional"]:
                # already-measured / curated facet -- NEVER touched (D20)
                buckets["SKIP_MEASURED"].append(src)
            elif m["keys"]:
                buckets["WRITE"].append(src)
            else:
                # provisional but we measured nothing real -> leave provisional (honest)
                buckets["SKIP_NO_MEASURE"].append(src)

            if i % 50 == 0:
                print(f"  ...{i}/{len(scope)} measured ({time.time()-t0:.0f}s)")
        cur.close()

        # ---- preview per WRITE source: current -> measured ----
        print(f"\n{'-'*80}\nWOULD WRITE ({len(buckets['WRITE'])} sources) -- provisional, measured a real key:\n{'-'*80}")
        keyfreq: Counter = Counter()
        tierfreq: Counter = Counter()
        for src in sorted(buckets["WRITE"], key=lambda s: s["source_id"]):
            m = src["measured"]
            cur_disp = ",".join(src["cur_keys"]) or "(empty)"
            print(f"  {src['source_id']:<44} {cur_disp:<22} -> [{','.join(m['keys'])}] {m['tier']}")
            for k in m["keys"]:
                keyfreq[k] += 1
            tierfreq[m["tier"]] += 1

        print(f"\n{'-'*80}\nSUMMARY\n{'-'*80}")
        print(f"  WRITE (gain measured keys):     {len(buckets['WRITE'])}")
        print(f"  SKIP already-measured (D20):    {len(buckets['SKIP_MEASURED'])}  (provisional=FALSE, untouched)")
        print(f"  SKIP provisional, no real key:  {len(buckets['SKIP_NO_MEASURE'])}  (left provisional -- honest)")
        print(f"  NO physical LANDING table:      {len(buckets['NO_TABLE'])}")
        print(f"  NO SOURCE_REGISTRY row:         {len(buckets['NO_REGISTRY_ROW'])}")
        print(f"\n  key frequency across WRITE sources:")
        for k, c in sorted(keyfreq.items(), key=lambda kv: (TIER_RANK[KEY_TOKENS[kv[0]][0]], -kv[1], kv[0])):
            print(f"    {k:<10} [{KEY_TOKENS[k][0]:<13}] {c:>4}")
        print(f"\n  strongest-tier distribution of WRITE sources:")
        for t, c in sorted(tierfreq.items(), key=lambda kv: TIER_RANK.get(kv[0], 99)):
            print(f"    {t:<14} {c:>4}")

        _write_report(buckets)
        print(f"\n  full report -> {REPORT}")

        if not args.apply:
            print("\n  PREVIEW only -- nothing written. Chris: re-run with --apply.")
            print(f"  --apply will snapshot {REGISTRY} -> {BACKUP} and write a rollback to {ROLLBACK}")
            return 0

        # ---------------- APPLY ----------------
        writes = sorted(buckets["WRITE"], key=lambda s: s["source_id"])
        if not writes:
            print("\n  nothing eligible to write. done.")
            return 0

        cur = conn.cursor()
        # 1. full-table snapshot (fast rollback)
        cur.execute(f"CREATE OR REPLACE TABLE {BACKUP} AS SELECT * FROM {REGISTRY}")
        print(f"\n  registry snapshot -> {BACKUP}")

        # 2. precise per-source rollback DDL to outputs/
        REPORT_DIR.mkdir(exist_ok=True)
        with open(ROLLBACK, "w", encoding="utf-8") as f:
            f.write(f"-- Rollback for JOIN_KEYS_STD backfill {_TS}\n")
            f.write(f"-- Full snapshot also at {BACKUP}\n")
            for src in writes:
                keys_json = json.dumps(src["cur_keys"])
                tier = src["cur_tier"] or "NONE"
                f.write(
                    f"UPDATE {REGISTRY} SET "
                    f"JOIN_KEYS_STD=PARSE_JSON('{keys_json}'), "
                    f"JOIN_KEY_TIER='{tier}', JOIN_KEY_TIER_PROVISIONAL=TRUE "
                    f"WHERE source_id='{src['source_id']}';\n"
                )
        print(f"  rollback DDL -> {ROLLBACK}")

        # 3. guarded writes
        upd = _update_sql()
        written = 0
        for src in writes:
            keys_json = json.dumps(src["measured"]["keys"])
            cur.execute(upd, (keys_json, keys_json, src["measured"]["tier"], src["source_id"]))
            written += cur.rowcount or 0
        conn.commit()
        cur.close()
        print(f"  wrote {written}/{len(writes)} source(s) (guarded: provisional-only).")

        # 4. verify
        cur = conn.cursor()
        cur.execute(
            f"""SELECT COUNT_IF(ARRAY_SIZE(r.JOIN_KEYS_STD)=0), COUNT_IF(r.JOIN_KEY_TIER_PROVISIONAL), COUNT(*)
                FROM {CATALOG} c JOIN {REGISTRY} r USING(source_id)
                WHERE c.lifecycle IN ('landed','modeled')"""
        )
        empt, prov, tot = cur.fetchone()
        cur.close()
        print(f"  post-apply (landed/modeled): empty_std={empt}  provisional={prov}  total={tot}")
        print("  DONE.")
        return 0
    finally:
        conn.close()


def _write_report(buckets: dict) -> None:
    L = ["# JOIN_KEYS_STD backfill report", ""]
    L.append(f"WRITE {len(buckets['WRITE'])} | SKIP_MEASURED {len(buckets['SKIP_MEASURED'])} | "
             f"SKIP_NO_MEASURE {len(buckets['SKIP_NO_MEASURE'])} | "
             f"NO_TABLE {len(buckets['NO_TABLE'])} | NO_REGISTRY_ROW {len(buckets['NO_REGISTRY_ROW'])}")
    L += ["", "## WOULD WRITE (provisional -> measured)", "",
          "| source_id | current | measured keys | tier | confirmed columns |", "|---|---|---|---|---|"]
    for src in sorted(buckets["WRITE"], key=lambda s: s["source_id"]):
        m = src["measured"]
        cols = "; ".join(f"{d['column']}={d['key']}({d['pop_pct']}%/{d['distinct']}d)"
                         for d in m["cols"] if d["confirmed"])
        L.append(f"| {src['source_id']} | {','.join(src['cur_keys']) or '(empty)'} | "
                 f"{','.join(m['keys'])} | {m['tier']} | {cols} |")
    L += ["", "## SKIP -- provisional but no key survived value-measurement", "",
          "| source_id | name-detected but rejected |", "|---|---|"]
    for src in sorted(buckets["SKIP_NO_MEASURE"], key=lambda s: s["source_id"]):
        m = src.get("measured", {})
        rej = "; ".join(f"{d['column']}={d['key']}({d['pop_pct']}%/{d['distinct']}d)"
                        for d in m.get("cols", []) if not d["confirmed"]) or "(no key-named columns)"
        L.append(f"| {src['source_id']} | {rej} |")
    L += ["", "## SKIP -- already measured (provisional=FALSE, untouched)", ""]
    for src in sorted(buckets["SKIP_MEASURED"], key=lambda s: s["source_id"]):
        L.append(f"- {src['source_id']} ({','.join(src['cur_keys']) or 'none'} / {src['cur_tier']})")
    for b, lbl in (("NO_TABLE", "No physical LANDING table"),
                   ("NO_REGISTRY_ROW", "No SOURCE_REGISTRY row")):
        L += ["", f"## {lbl} ({len(buckets[b])})", ""]
        for src in sorted(buckets[b], key=lambda s: s["source_id"]):
            L.append(f"- {src['source_id']} ({src['lifecycle']})")
    REPORT_DIR.mkdir(exist_ok=True)
    REPORT.write_text("\n".join(L), encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
