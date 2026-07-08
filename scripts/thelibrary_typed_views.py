#!/usr/bin/env python3
"""Generate a TYPED tier over THE_LIBRARY reading-room views (evidence.dev readiness).

WHY: 171 reading-room views are `SELECT *` passthroughs over LIBRARY_RAW.LANDING, where
EVERY column is TEXT (raw-landing convention). evidence.dev chart queries therefore have to
hand-cast every number and date. This script auto-generates a typed projection per view so a
chart query can just `SELECT amount, event_date` and get a real NUMBER / DATE back -- no casts.

WHAT IT DOES (per landing-backed reading-room view):
  1. Enumerate targets from LIBRARY_META.REGISTRY.FRIENDLY_LAYER (LAYER='landing'). These are
     pure `SELECT * FROM <landing table>`, so the view's output columns == the table's columns 1:1.
  2. Profile each TEXT column over a SAMPLE(5000 ROWS): non-null%, TRY_TO_DOUBLE hit%, has-decimal%,
     all-8-digit%, GUARDED separator-date hit% (TRY_TO_DATE only on values with '-'/'/'), and the
     8-digit YYYYMMDD-vs-MMDDYYYY hit% (empirical, so we never guess the date order).
  3. Classify each column -- NAME HEURISTICS WIN over value sniffing (anti-corruption layer):
       - meta cols (_INGESTED_AT etc.) + hard-ID names (ZIP/NPI/FIPS/EIN/CIK/*_ID/*_CODE/...) -> keep TEXT
         (leading zeros + '0000000000' NPIs + 8-digit codes must survive; numbers would destroy them).
       - date-ish names -> DATE, using an EXPLICIT format for 8-digit ('YYYYMMDD'/'MMDDYYYY', never a
         bare TRY_TO_DATE -- TRY_TO_DATE('10042024') = 1970-04-27, the epoch trap) and a separator-GUARDED
         TRY_TO_DATE for '-'/'/'-style dates.
       - clean numerics (TRY_TO_DOUBLE >= 98% of non-null, not an 8-digit blob) -> NUMBER, cleaning
         'nan'/blank sentinels to NULL so they don't poison the column.
       - everything else -> TEXT passthrough. Worst case = status quo (a raw TEXT column), never a wrong cast.
  4. Emit CREATE OR REPLACE VIEW ... COPY GRANTS preserving the exact output column names + the view's
     COMMENT. This also RE-PINS the column list against the current table, which FIXES the views that
     re-landed wider than their pinned list and are currently compile-broken.

  A view is only rewritten if it gains >=1 typed column OR is currently broken (minimise churn).

*** COPY GRANTS is MANDATORY (audit D04). *** THE_LIBRARY views are granted SELECT to RIPPLE_READER +
CLAUDE_MCP_READONLY. A plain CREATE OR REPLACE VIEW STRIPS those grants and dark-outs the read lane.
COPY GRANTS preserves them; --apply also verifies (SHOW GRANTS) and re-grants belt-and-suspenders.

    python3 scripts/thelibrary_typed_views.py                 # PREVIEW: profile + print the plan (no writes)
    python3 scripts/thelibrary_typed_views.py --limit 10       # PREVIEW a first slice (faster)
    python3 scripts/thelibrary_typed_views.py --only FED_FEC_BULK,INTL_IE_CRO   # target specific tables
    python3 scripts/thelibrary_typed_views.py --apply          # rewrite the typed views (COPY GRANTS) + verify

Idempotent + reversible: re-running --apply regenerates the same typed views; the rollback snapshot
(outputs/_rollback_thelibrary_typed_views_<ts>.sql) restores every touched view to its plain
`SELECT *` passthrough -- the exact thelibrary_build.py baseline. CHRIS runs --apply, never the agent
(the classifier blocks shared-state writes); --apply must run under the role that owns THE_LIBRARY
(ACCOUNTADMIN).
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")
REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

READ_ROLES = ("RIPPLE_READER", "CLAUDE_MCP_READONLY")

# --- classification tunables ---
NUM_THRESH = 0.98      # TRY_TO_DOUBLE hit-rate (over non-null) to call a column NUMBER
DATE_THRESH = 0.85     # date-parse hit-rate (over non-null) to call a date-named column a DATE
EIGHT_DIGIT_BLOCK = 0.90  # if this fraction of non-null is an 8-digit blob, DON'T call it NUMBER (likely date/id)
MIN_NONNULL = 20       # need this many non-null sampled values before trusting any cast
SAMPLE_ROWS = 5000
BATCH = 40             # TEXT columns profiled per SQL round-trip (keeps wide tables sane)

# HARD-KEEP-TEXT: name check WINS. Leading zeros / sentinel-heavy identifiers must survive as TEXT.
KEEP_RE = re.compile(
    r"(_ID$|^ID$|ZIP|NPI|FIPS|EIN|CIK|UEI|DUNS|CAGE|_CODE|NAICS|NDC|CCN|PHONE|"
    r"_NUM|SSN|GEOID|_KEY|PIID|TRACT|BLOCK)", re.I)
# date-ish names -> DATE branch (value-sniff still has to agree, so misfires fall back to TEXT)
DATE_RE = re.compile(r"(DATE|_DT$|^DT$|_DT_)", re.I)


def esc(s: str) -> str:
    return (s or "").replace("'", "''")


def qi(name: str) -> str:
    """Double-quote an identifier (escape embedded quotes)."""
    return '"' + name.replace('"', '""') + '"'


def clean_expr(col: str) -> str:
    """Trim + null out 'nan'/'NaN'/'NAN'/blank sentinels before a numeric cast."""
    c = qi(col)
    return f"NULLIF(NULLIF(NULLIF(NULLIF(TRIM({c}),'nan'),'NaN'),'NAN'),'')"


# --------------------------------------------------------------------------- profiling

def _profile_batch(cur, table_fqn: str, cols: list[str]) -> dict[str, dict]:
    """One SQL round-trip: per TEXT column, guarded value-shape counts over a 5k-row sample."""
    sel = ["COUNT(*) AS N"]
    for i, c in enumerate(cols):
        q = qi(c)
        t = f"TRIM({q})"
        cl = clean_expr(c)
        sel += [
            f"COUNT({cl}) AS NN_{i}",
            f"SUM(IFF(TRY_TO_DOUBLE({cl}) IS NOT NULL,1,0)) AS DBL_{i}",
            # exactly-8-char pure integer (no '.', '-', '/') = an 8-digit blob
            f"SUM(IFF(LENGTH({t})=8 AND POSITION('.' IN {t})=0 AND POSITION('-' IN {t})=0 "
            f"AND POSITION('/' IN {t})=0 AND TRY_TO_DOUBLE({t}) IS NOT NULL,1,0)) AS D8_{i}",
            f"SUM(IFF(POSITION('.' IN {t})>0 AND TRY_TO_DOUBLE({t}) IS NOT NULL,1,0)) AS DEC_{i}",
            # GUARDED separator date: only when a separator is present (never bare on 8 digits)
            f"SUM(IFF(({t} LIKE '%-%' OR {t} LIKE '%/%') AND TRY_TO_DATE({t}) IS NOT NULL,1,0)) AS SEP_{i}",
            f"SUM(IFF(LENGTH({t})=8 AND TRY_TO_DATE({t},'YYYYMMDD') IS NOT NULL,1,0)) AS YMD_{i}",
            f"SUM(IFF(LENGTH({t})=8 AND TRY_TO_DATE({t},'MMDDYYYY') IS NOT NULL,1,0)) AS MDY_{i}",
            # long all-digit integer (>=15 chars) = an identifier/code, NOT a measure.
            # TRY_TO_NUMBER overflows (NULLs) past 38 digits -> keep these TEXT (anti-corruption).
            f"SUM(IFF(LENGTH({t})>=15 AND POSITION('.' IN {t})=0 AND POSITION('-' IN {t})=0 "
            f"AND TRY_TO_DOUBLE({t}) IS NOT NULL,1,0)) AS BIG_{i}",
        ]
    sql = f"SELECT {', '.join(sel)} FROM {table_fqn} SAMPLE ({SAMPLE_ROWS} ROWS)"
    cur.execute(sql)
    row = cur.fetchone()
    n = row[0] or 0
    out = {}
    for i, c in enumerate(cols):
        base = 1 + 8 * i
        nn, dbl, d8, dec, sep, ymd, mdy, big = row[base:base + 8]
        out[c] = {"n": n, "nn": nn or 0, "dbl": dbl or 0, "d8": d8 or 0,
                  "dec": dec or 0, "sep": sep or 0, "ymd": ymd or 0, "mdy": mdy or 0,
                  "big": big or 0}
    return out


def classify(col: str, s: dict) -> tuple[str, str]:
    """Return (kind, reason). kind in NUM_INT/NUM_DBL/DATE_YMD/DATE_MDY/DATE_SEP/TEXT."""
    U = col.upper()
    if U.startswith("_"):
        return "TEXT", "meta"
    if KEEP_RE.search(U):
        return "TEXT", "keep-id"
    nn = s["nn"]
    if nn < MIN_NONNULL:
        return "TEXT", "low-signal"
    r = lambda k: s[k] / nn if nn else 0.0
    if DATE_RE.search(U):
        if r("d8") >= 0.5:  # 8-digit dates: pick the format the data actually parses under
            if s["ymd"] >= s["mdy"] and r("ymd") >= DATE_THRESH:
                return "DATE_YMD", "date8-ymd"
            if r("mdy") >= DATE_THRESH:
                return "DATE_MDY", "date8-mdy"
            if r("ymd") >= DATE_THRESH:
                return "DATE_YMD", "date8-ymd"
        if r("sep") >= DATE_THRESH:
            return "DATE_SEP", "date-sep"
        return "TEXT", "datename-unparsed"
    if r("big") >= 0.5:  # long all-digit strings = identifiers/codes, not measures
        return "TEXT", "long-int-id"
    if r("dbl") >= NUM_THRESH and r("d8") < EIGHT_DIGIT_BLOCK:
        return ("NUM_INT", "num-int") if s["dec"] == 0 else ("NUM_DBL", "num-dbl")
    return "TEXT", "below-threshold"


def col_expr(col: str, kind: str) -> str:
    """The typed projection expression for one column, aliased back to its exact name."""
    c, cl = qi(col), clean_expr(col)
    t = f"TRIM({c})"
    if kind == "NUM_INT":
        return f"TRY_TO_NUMBER({cl}) AS {c}"
    if kind == "NUM_DBL":
        return f"TRY_TO_DOUBLE({cl}) AS {c}"
    if kind == "DATE_YMD":
        return f"TRY_TO_DATE({t},'YYYYMMDD') AS {c}"
    if kind == "DATE_MDY":
        return f"TRY_TO_DATE({t},'MMDDYYYY') AS {c}"
    if kind == "DATE_SEP":
        return f"CASE WHEN {t} LIKE '%-%' OR {t} LIKE '%/%' THEN TRY_TO_DATE({t}) END AS {c}"
    return c  # TEXT passthrough (name preserved, no alias needed)


# --------------------------------------------------------------------------- per-view build

def build_view(cur, view_fqn: str, object_fqn: str, comment: str):
    """Profile the underlying table, classify, and return (apply_ddl, rollback_ddl, stats)
    or None if the view needs no rewrite (0 typed cols and not broken)."""
    schema, name = view_fqn.split(".")[1], view_fqn.split(".")[2]
    # every column, ordinal order, with type (so non-TEXT passes through bare)
    cur.execute(f"""SELECT COLUMN_NAME, DATA_TYPE FROM {object_fqn.split('.')[0]}.INFORMATION_SCHEMA.COLUMNS
                    WHERE TABLE_SCHEMA='{object_fqn.split('.')[1]}' AND TABLE_NAME='{object_fqn.split('.')[2]}'
                    ORDER BY ORDINAL_POSITION""")
    all_cols = cur.fetchall()  # [(name, data_type)]
    if not all_cols:
        return None  # underlying table missing -- skip
    text_cols = [c for c, dtp in all_cols if dtp == "TEXT"]

    # profile TEXT cols in batches
    prof: dict[str, dict] = {}
    for i in range(0, len(text_cols), BATCH):
        prof.update(_profile_batch(cur, object_fqn, text_cols[i:i + BATCH]))

    # is the current view compile-broken? (re-landed wider than its pinned list)
    broken = False
    try:
        cur.execute(f"SELECT * FROM {view_fqn} LIMIT 0")
        cur.fetchall()
    except Exception:
        broken = True

    # classify + build projection (preserve ordinal order + exact names)
    proj, kinds = [], {"DATE": 0, "NUMBER": 0, "TEXT": 0, "PASS": 0}
    for c, dtp in all_cols:
        if dtp != "TEXT":
            proj.append(qi(c))
            kinds["PASS"] += 1
            continue
        kind, _reason = classify(c, prof.get(c, {"nn": 0}))
        proj.append(col_expr(c, kind))
        if kind.startswith("DATE"):
            kinds["DATE"] += 1
        elif kind.startswith("NUM"):
            kinds["NUMBER"] += 1
        else:
            kinds["TEXT"] += 1

    typed = kinds["DATE"] + kinds["NUMBER"]
    if typed == 0 and not broken:
        return None  # nothing to gain -- leave the plain SELECT * as-is

    cclause = f" COMMENT='{esc(comment)}'" if comment else ""
    projection = ",\n    ".join(proj)
    apply_ddl = (f"CREATE OR REPLACE VIEW {view_fqn} COPY GRANTS{cclause} AS\n"
                 f"SELECT\n    {projection}\nFROM {object_fqn}")
    rollback_ddl = (f"CREATE OR REPLACE VIEW {view_fqn} COPY GRANTS{cclause} AS "
                    f"SELECT * FROM {object_fqn}")
    stats = {"schema": schema, "name": name, "ncols": len(all_cols),
             "date": kinds["DATE"], "number": kinds["NUMBER"], "text": kinds["TEXT"],
             "passthrough": kinds["PASS"], "typed": typed, "broken": broken}
    return apply_ddl, rollback_ddl, stats


# --------------------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser(description="Generate typed views over THE_LIBRARY reading room")
    ap.add_argument("--apply", action="store_true", help="rewrite the views (default: preview)")
    ap.add_argument("--limit", type=int, default=0, help="only the first N target views (preview slicing)")
    ap.add_argument("--only", default="", help="comma-separated landing table names to target (e.g. FED_FEC_BULK)")
    args = ap.parse_args()

    from connect import db
    conn = db.connect()
    cur = conn.cursor()

    print(f"role: {db.scalar(conn, 'SELECT CURRENT_ROLE()')}")

    # ---- enumerate target views from the friendly layer -----------------
    targets = db.dicts(conn, """
        SELECT THE_LIBRARY_FQN, OBJECT_FQN, FRIENDLY_SCHEMA, FRIENDLY_NAME
        FROM LIBRARY_META.REGISTRY.FRIENDLY_LAYER
        WHERE LAYER='landing' AND OBJECT_FQN IS NOT NULL
        ORDER BY FRIENDLY_SCHEMA, FRIENDLY_NAME""")
    if args.only:
        want = {o.strip().upper() for o in args.only.split(",") if o.strip()}
        targets = [t for t in targets if t["OBJECT_FQN"].split(".")[-1].upper() in want]
    if args.limit:
        targets = targets[:args.limit]

    # comments (preserve exactly) keyed by (schema, name)
    comments = {(r[0], r[1]): r[2] for r in db.rows(conn,
        "SELECT TABLE_SCHEMA, TABLE_NAME, COMMENT FROM THE_LIBRARY.INFORMATION_SCHEMA.TABLES "
        "WHERE TABLE_TYPE='VIEW'")}

    print(f"target landing views: {len(targets)}  "
          f"(profiling {SAMPLE_ROWS}-row samples; name-heuristics win over value sniffing)\n")

    plans = []          # (view_fqn, object_fqn, apply_ddl, rollback_ddl, stats)
    tot = {"date": 0, "number": 0, "text": 0, "passthrough": 0, "ncols": 0}
    fixed, changed, skipped, errors = [], 0, 0, []

    for t in targets:
        vfqn, ofqn = t["THE_LIBRARY_FQN"], t["OBJECT_FQN"]
        comment = comments.get((t["FRIENDLY_SCHEMA"], t["FRIENDLY_NAME"]), "")
        try:
            res = build_view(cur, vfqn, ofqn, comment)
        except Exception as e:
            errors.append((vfqn, str(e)[:140]))
            print(f"  [ERR] {vfqn}: {str(e)[:120]}")
            continue
        if res is None:
            skipped += 1
            continue
        apply_ddl, rollback_ddl, s = res
        plans.append((vfqn, ofqn, apply_ddl, rollback_ddl, s))
        for k in ("date", "number", "text", "passthrough", "ncols"):
            tot[k] += s[k] if k != "ncols" else s["ncols"]
        changed += 1
        tag = "  << FIXED (was compile-broken)" if s["broken"] else ""
        print(f"  {s['schema']}.{s['name']:<40} {s['ncols']:>3} cols  "
              f"DATE={s['date']:>2} NUM={s['number']:>2} TEXT={s['text']:>2} pass={s['passthrough']:>2}{tag}")
        if s["broken"]:
            fixed.append(vfqn)

    # ---- validate every generated projection COMPILES (read-only, LIMIT 0) ----
    print(f"\nvalidating {len(plans)} generated projections compile (SELECT ... LIMIT 0) ...")
    compile_ok, compile_bad = 0, []
    for vfqn, ofqn, apply_ddl, _rb, s in plans:
        body = apply_ddl[apply_ddl.index("\nSELECT\n") + 1:]  # the SELECT ... FROM ... (single-line comment can't contain this)
        try:
            cur.execute(body + "\nLIMIT 0")
            cur.fetchall()
            compile_ok += 1
        except Exception as e:
            compile_bad.append((vfqn, str(e)[:140]))
    print(f"  compile OK: {compile_ok}/{len(plans)}")
    for v, e in compile_bad:
        print(f"  [COMPILE-FAIL] {v}: {e}")

    # ---- totals ----------------------------------------------------------
    print("\n" + "=" * 60)
    print(f"views to rewrite : {changed}   (unchanged/skipped: {skipped}   errors: {len(errors)})")
    print(f"columns touched  : {tot['ncols']:,} across rewritten views")
    print(f"  typed as DATE   : {tot['date']:,}")
    print(f"  typed as NUMBER : {tot['number']:,}")
    print(f"  kept  as TEXT   : {tot['text']:,}   (+ {tot['passthrough']:,} already-typed passthrough)")
    print(f"compile-broken views re-pinned/FIXED: {len(fixed)} -> {fixed}")
    print("=" * 60)

    # always snapshot the generated typed DDL for eyeballing
    ts = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    plan_file = REPO / "outputs" / f"_thelibrary_typed_views_plan_{ts}.sql"
    plan_file.parent.mkdir(parents=True, exist_ok=True)
    plan_file.write_text(
        "-- Generated typed-view DDL (preview). Apply with scripts/thelibrary_typed_views.py --apply.\n\n"
        + ";\n\n".join(p[2] for p in plans) + ";\n", encoding="utf-8")
    print(f"\ntyped DDL plan snapshot -> {plan_file}")

    if not args.apply:
        print("\nPREVIEW only -- nothing written to Snowflake. Re-run with --apply to rewrite the views.")
        conn.close()
        return 0
    if compile_bad:
        print("\nABORT: some projections did not compile (see [COMPILE-FAIL] above). "
              "No views rewritten -- fix the profiler/classifier first.")
        conn.close()
        return 2

    # --- APPLY ---
    rollback = REPO / "outputs" / f"_rollback_thelibrary_typed_views_{ts}.sql"
    rollback.write_text(
        "-- Rollback: restores every touched THE_LIBRARY view to its plain SELECT * passthrough\n"
        "-- (the thelibrary_build.py baseline; COPY GRANTS preserves the read-lane grants).\n"
        f"-- Snapshotted {ts} before --apply rewrote {len(plans)} views.\n\n"
        + ";\n\n".join(p[3] for p in plans) + ";\n", encoding="utf-8")
    print(f"\nrollback snapshot -> {rollback}")

    print(f"applying {len(plans)} CREATE OR REPLACE VIEW ... COPY GRANTS ...")
    applied, apply_err = 0, []
    for vfqn, ofqn, apply_ddl, _rb, s in plans:
        try:
            cur.execute(apply_ddl)
            # belt-and-suspenders re-grant (COPY GRANTS should already carry these)
            for role in READ_ROLES:
                cur.execute(f"GRANT SELECT ON VIEW {vfqn} TO ROLE {role}")
            applied += 1
        except Exception as e:
            apply_err.append((vfqn, str(e)[:160]))
            print(f"  [APPLY-FAIL] {vfqn}: {str(e)[:140]}")
    print(f"  applied: {applied}/{len(plans)}")

    # ---- verify grants preserved on a sample + the fixed views -----------
    print("\nverifying read-lane grants preserved (COPY GRANTS) ...")
    check = [p[0] for p in plans[:1]] + fixed
    for vfqn in check:
        cur.execute(f"SHOW GRANTS ON VIEW {vfqn}")
        gs = [str(g) for g in cur.fetchall()]
        for role in READ_ROLES:
            ok = any(role in g and "SELECT" in g for g in gs)
            print(f"  {vfqn}  {role}: {'OK' if ok else 'MISSING'}")
    if fixed:
        print("\nverifying re-pinned (formerly broken) views now SELECT cleanly ...")
        for vfqn in fixed:
            try:
                cur.execute(f"SELECT COUNT(*) FROM {vfqn}")
                print(f"  {vfqn}: OK ({cur.fetchone()[0]:,} rows)")
            except Exception as e:
                print(f"  {vfqn}: STILL BROKEN -- {str(e)[:120]}")

    print("\nDONE.")
    conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
