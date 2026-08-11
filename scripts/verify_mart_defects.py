"""One-time checker: hard evidence for the mart-defect list (2026-08-10 sweep).

Phase A is metadata-only (information_schema + the catalog) and costs almost nothing:
  * column loss   -- mart column count vs the LANDING table behind it
  * row truth     -- real mart rows vs CATALOG.MART_ROW_COUNT vs the model's own
                     header comment, plus the page-cap signature (round numbers)
  * cast suspects -- replay gen_mart_models.infer_cast over the landing columns to
                     find text columns the generator wrapped in try_to_number /
                     try_to_double / try_to_date because of a substring accident
                     (COUNTRY contains "COUNT", INCORPORATION contains "RATIO").

Phase B scans only the columns phase A flagged: COUNT(*), COUNT(col),
COUNT(DISTINCT col) and a value sample. Per CLAUDE.md section 7 a bare null check is
not evidence -- this platform has twice been fooled by sentinel-masked blanks.

Writes reports/mart_defect_verification_2026-08-10.csv (durable; the platform must
not re-derive verdicts at runtime).

    python scripts/verify_mart_defects.py --phase a
    python scripts/verify_mart_defects.py --phase b
"""
import argparse
import csv
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _snowflake_conn as sc  # noqa: E402
from gen_mart_models import infer_cast, _resolve_landing_source  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARTS_DIR = os.path.join(REPO, "library-onboarding", "ripple_dbt", "models", "marts")
OUT_DIR = os.path.join(REPO, "reports")
PHASE_A_CSV = os.path.join(OUT_DIR, "mart_defect_verification_2026-08-10.csv")
PHASE_B_CSV = os.path.join(OUT_DIR, "mart_dead_columns_2026-08-10.csv")

# The counts a paginated loader stops on. A mart landing exactly here is a page cap
# until proven otherwise.
PAGE_CAPS = {1_000, 2_000, 5_000, 9_000, 10_000, 25_000, 50_000, 100_000, 200_000,
             250_000, 500_000, 1_000_000, 20_000_000}

SAMPLE_ABOVE = 20_000_000
SAMPLE_ROWS = 1_000_000

META_COLS = {"_INGESTED_AT", "_SOURCE_RUN_ID", "_SRC_SHA256",
             "INGESTED_AT", "SOURCE_RUN_ID", "SRC_SHA256"}

# Names that are text in the real world no matter what substring tripped the caster.
TEXT_NAME_HINTS = ("COUNTRY", "COUNTY", "NAME", "STATE", "TEXT", "ACTION",
                   "DESCRIPTION", "TITLE", "FREQUENCY", "TYPE", "ADDRESS", "CITY",
                   "FIPS", "PARISH", "INCORPORATION", "STATUS", "REGION",
                   "COMMENT", "NARRATIVE", "REMARK", "NOTE")

_HDR_ROWS = re.compile(r"^--\s*Source:.*?\(([\d,]+)\s*rows\)", re.M)


def looks_like_text_name(col):
    return any(h in col.upper() for h in TEXT_NAME_HINTS)


def disk_marts():
    """{MODEL_NAME: {...}} for every mart .sql, with the LANDING table it reads."""
    out = {}
    for path in glob.glob(os.path.join(MARTS_DIR, "*", "*.sql")):
        model = os.path.splitext(os.path.basename(path))[0]
        text = open(path, encoding="utf-8", errors="ignore").read()
        m = _HDR_ROWS.search(text)
        schema = re.search(r"schema\s*=\s*.([A-Za-z_0-9]+).", text)
        out[model.upper()] = {
            "path": os.path.relpath(path, REPO).replace("\\", "/"),
            "landing": _resolve_landing_source(path),
            "header_rows": int(m.group(1).replace(",", "")) if m else None,
            "schema": schema.group(1).upper() if schema else None,
        }
    return out


def fetch_metadata(conn):
    cur = conn.cursor()
    cur.execute("select table_name, column_name, data_type "
                "from LIBRARY_RAW.information_schema.columns "
                "where table_schema = 'LANDING'")
    landing = {}
    for tbl, col, dt in cur:
        landing.setdefault(tbl.upper(), []).append((col.upper(), dt))

    cur.execute("select table_schema, table_name, column_name "
                "from LIBRARY_MARTS.information_schema.columns")
    mart_cols = {}
    for sch, tbl, col in cur:
        mart_cols.setdefault((sch.upper(), tbl.upper()), []).append(col.upper())

    cur.execute("select table_schema, table_name, table_type, row_count "
                "from LIBRARY_MARTS.information_schema.tables")
    mart_rows = {(s.upper(), t.upper()): (tt, rc) for s, t, tt, rc in cur}

    cur.execute("select SOURCE_ID, MART_ROW_COUNT, LANDED_ROW_COUNT, LIFECYCLE "
                "from LIBRARY_META.REGISTRY.CATALOG")
    catalog = {r[0].upper(): r[1:] for r in cur}
    return landing, mart_cols, mart_rows, catalog


FIELDS = ["model", "path", "mart_schema", "landing_table", "landing_cols",
          "mart_cols", "col_loss_pct", "positional_names", "mart_rows_live",
          "mart_object_type", "catalog_mart_rows", "header_rows",
          "row_disagreement", "bad_cast_cols", "verdicts"]


def phase_a(conn):
    marts = disk_marts()
    landing, mart_cols, mart_rows, catalog = fetch_metadata(conn)
    rows = []
    for model, info in sorted(marts.items()):
        schema, lt = info["schema"], info["landing"]
        lcols_typed = [(c, d) for c, d in landing.get(lt or "", [])
                       if c not in META_COLS]
        lcols = [c for c, _ in lcols_typed]
        mcols = [c for c in mart_cols.get((schema, model), []) if c not in META_COLS]
        live_type, live_rows = mart_rows.get((schema, model), (None, None))
        cat_rows = catalog.get(lt or "", (None, None, None))[0]

        loss = None
        if lcols:
            loss = round(100.0 * (1 - len(mcols) / len(lcols)), 1)

        positional = sum(1 for c in mcols if re.fullmatch(r"C\d+", c))
        bad_casts = [f"{c}:{infer_cast(c, d)}" for c, d in lcols_typed
                     if infer_cast(c, d) and looks_like_text_name(c)]

        disagree = []
        for label, v in (("catalog", cat_rows), ("header", info["header_rows"])):
            if v and live_rows and abs(v - live_rows) > max(1, 0.01 * live_rows):
                disagree.append("%s=%s" % (label, v))

        verdicts = []
        if lcols and mcols and len(mcols) <= 2 and len(lcols) > 4:
            verdicts.append("SHELL_MART")
        if lcols and len(lcols) <= 2:
            verdicts.append("SHELL_LANDING")
        if positional:
            verdicts.append("POSITIONAL_NAMES(%d)" % positional)
        if bad_casts:
            verdicts.append("BAD_CAST(%d)" % len(bad_casts))
        if live_rows in PAGE_CAPS:
            verdicts.append("PAGE_CAP")
        if disagree:
            verdicts.append("ROW_DISAGREE")
        if lt and not mcols and live_type is None:
            verdicts.append("NOT_BUILT")

        rows.append({
            "model": model, "path": info["path"], "mart_schema": schema or "",
            "landing_table": lt or "", "landing_cols": len(lcols),
            "mart_cols": len(mcols), "col_loss_pct": loss,
            "positional_names": positional, "mart_rows_live": live_rows,
            "mart_object_type": live_type or "", "catalog_mart_rows": cat_rows,
            "header_rows": info["header_rows"], "row_disagreement": ";".join(disagree),
            "bad_cast_cols": ";".join(bad_casts),
            "verdicts": ",".join(verdicts) or "OK",
        })
    return rows


B_FIELDS = ["mart_schema", "mart_table", "column", "declared_cast", "total_rows",
            "non_null", "distinct_vals", "pct_populated", "sample", "scan", "verdict"]


def phase_b(conn):
    """Scan the columns phase A flagged. One query per table, not per column."""
    with open(PHASE_A_CSV, encoding="utf-8") as fh:
        flagged = [r for r in csv.DictReader(fh) if r["bad_cast_cols"]]
    cur = conn.cursor()
    out = []
    for i, r in enumerate(flagged, 1):
        schema, model = r["mart_schema"], r["model"]
        casts = dict(c.split(":") for c in r["bad_cast_cols"].split(";") if ":" in c)
        # Mart aliases are snake_case of the landing name; both resolve
        # case-insensitively in Snowflake, so the landing name is a safe handle.
        cols = [c for c in casts]
        if not cols:
            continue
        parts = ["count(*) as n"]
        for j, c in enumerate(cols):
            parts += ["count(%s) as nn_%d" % (c, j),
                      "count(distinct %s) as nd_%d" % (c, j),
                      "max(%s) as mx_%d" % (c, j)]
        # A dead cast is dead in every row, so a sample is proof enough on the giant
        # tables and keeps this one-time check inside its spend allowance.
        live = int(r["mart_rows_live"] or 0)
        sampled = live > SAMPLE_ABOVE
        tail = " sample (%d rows)" % SAMPLE_ROWS if sampled else ""
        sql = "select %s from LIBRARY_MARTS.%s.%s%s" % (
            ", ".join(parts), schema, model, tail)
        try:
            cur.execute(sql)
            row = cur.fetchone()
        except Exception as exc:  # a mart that no longer exists, or a type mismatch
            out.append({"mart_schema": schema, "mart_table": model, "column": "*",
                        "verdict": "QUERY_FAILED: %s" % str(exc)[:160]})
            continue
        total = row[0]
        for j, c in enumerate(cols):
            nn, nd, mx = row[1 + j * 3], row[2 + j * 3], row[3 + j * 3]
            pct = round(100.0 * nn / total, 2) if total else None
            if nn == 0:
                verdict = "DEAD_CAST"          # cast nulled the column outright
            elif nd is not None and nd <= 1:
                verdict = "SINGLE_VALUE"        # populated but carries no information
            elif pct is not None and pct < 5:
                verdict = "MOSTLY_DEAD"
            else:
                verdict = "SURVIVED"
            out.append({"mart_schema": schema, "mart_table": model, "column": c,
                        "declared_cast": casts[c], "total_rows": total,
                        "non_null": nn, "distinct_vals": nd, "pct_populated": pct,
                        "sample": str(mx)[:60] if mx is not None else "",
                        "scan": "sampled" if sampled else "full",
                        "verdict": verdict})
        if i % 25 == 0:
            print("  scanned %d/%d tables" % (i, len(flagged)), flush=True)
    return out


def write_csv(path, fields, rows):
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print("wrote %s" % os.path.relpath(path, REPO))


def tally(rows, key):
    counts = {}
    for r in rows:
        for v in str(r[key]).split(","):
            v = re.sub(r"\(.*\)", "", v)
            if v and v != "OK":
                counts[v] = counts.get(v, 0) + 1
    for k, v in sorted(counts.items(), key=lambda kv: -kv[1]):
        print("  %4d  %s" % (v, k))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", default="a", choices=["a", "b"])
    args = ap.parse_args()
    conn = sc.connect()
    try:
        if args.phase == "a":
            rows = phase_a(conn)
            write_csv(PHASE_A_CSV, FIELDS, rows)
            bad = [r for r in rows if r["verdicts"] != "OK"]
            print("%d marts checked, %d with at least one defect" % (len(rows), len(bad)))
            tally(bad, "verdicts")
        else:
            rows = phase_b(conn)
            write_csv(PHASE_B_CSV, B_FIELDS, rows)
            print("%d columns scanned" % len(rows))
            tally(rows, "verdict")
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
