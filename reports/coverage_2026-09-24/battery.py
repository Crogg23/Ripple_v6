"""Battery A: one loud-number pass over every untouched single in the ledger.

Per table, read-only, at most three statements:
  Q1 profile   row count, lead number stats, date span, distinct actors
  Q2 actors    top 10 actors by the lead number, or by rows, plus totals
  Q3 tail      share of the lead number held by its top 1% of rows, and rows over 10x median
Tables with no number and no actor get Q4: APPROX_TOP_K on up to three category columns.

Output: battery.jsonl beside this file, one line per table. Reruns skip tables already done.
Every statement is tagged QUERY_TAG='battery-a-2026-09-24' so its cost can be read back.
Run from the repo root: python reports/coverage_2026-09-24/battery.py [--workers 8] [--only TABLE]
"""
import argparse
import json
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
import ledger as L  # noqa: E402
from connect import db  # noqa: E402

OUT = HERE / "battery.jsonl"
TAG = "battery-a-2026-09-24"
LOCK = threading.Lock()
LOCAL = threading.local()
FIRM_TOKENS = {"FIRM", "COMPANY", "MANUFACTURER", "OPERATOR", "OWNER", "FACILITY", "EMPLOYER", "AGENCY", "LENDER",
               "VENDOR", "CONTRACTOR", "RECIPIENT", "SPONSOR", "APPLICANT", "PETITIONER", "RESPONDENT", "DEFENDANT",
               "PLAINTIFF", "CARRIER", "MINE", "HOSPITAL", "PROVIDER", "SUPPLIER", "LABELER", "REGISTRANT",
               "COMMITTEE", "CANDIDATE", "DONOR", "CONTRIBUTOR", "PARTY", "ORGANIZATION", "ENTITY", "ISSUER"}
SKIP_TEXT = {"NARRATIVE", "DESCRIPTION", "SUMMARY", "REMARKS", "COMMENT", "COMMENTS", "NOTES", "ABSTRACT",
             "TEXT", "ADDRESS", "STREET", "URL", "EMAIL", "PHONE", "ID", "KEY", "UUID", "HASH", "NAME", "TITLE"}


def conn():
    c = getattr(LOCAL, "c", None)
    if c is None:
        c = db.connect()
        db.rows(c, "ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
        db.rows(c, f"ALTER SESSION SET QUERY_TAG = '{TAG}'")
        LOCAL.c = c
    return c


def run(sql):
    s = sql.lstrip().upper()
    assert s.startswith(("SELECT", "WITH")), "read-only battery"
    t0 = time.time()
    try:
        out = db.dicts(conn(), sql)
        return out, None, round(time.time() - t0, 1)
    except Exception as e:  # one bad column must not sink the table
        return None, str(e).splitlines()[0][:300], round(time.time() - t0, 1)


def q(c):
    return '"' + db.ident(c) + '"'


def expr(col, typ):
    """A number from a column. Text money gets $ and commas stripped; 'nan' and inf become null."""
    if typ == "TEXT":
        return (f"IFF(LOWER(TRIM({q(col)})) IN ('nan','inf','-inf','infinity'), NULL, "
                f"TRY_TO_DOUBLE(REGEXP_REPLACE({q(col)}, '[$, ]', '')))")
    if typ == "FLOAT":
        return f"NULLIF({q(col)}, 'NaN'::FLOAT)"
    return q(col)


def plan(t):
    types = {c: typ for c, typ, _ in t["cols"]}
    metrics = []
    for c in t["money"] + t["harm_num"] + t["metrics"]:
        if c not in metrics and types.get(c) in ("NUMBER", "FLOAT", "TEXT"):
            metrics.append(c)
    metrics = metrics[:3]
    actor = None
    for k in t["entity"]:
        if k not in L.RECORD_KEYS and t["keys"][k]:
            actor = t["keys"][k][0]
            break
    actor = actor or (t["names"][:1] or t["person"][:1] or [None])[0]
    if not actor:
        firm = [c for c, typ, _ in t["cols"] if typ == "TEXT" and not c.startswith("_")
                and set(L.toks(c)) & FIRM_TOKENS and not set(L.toks(c)) & {"ID", "CODE", "CD", "NUMBER", "ADDRESS",
                                                                          "CITY", "STATE", "ZIP", "PHONE"}]
        actor = (firm or [None])[0]
    cats = []
    if not metrics:
        for c, typ, _ in t["cols"]:
            if (typ == "TEXT" and c != actor and not c.startswith("_")
                    and not set(L.toks(c)) & (SKIP_TEXT | {"NUMBER", "NO", "NBR", "NUM", "ZIP", "CITY"})):
                cats.append(c)
        cats = cats[:3]
    return dict(metrics=[(m, types[m]) for m in metrics], actor=actor, date=(t["dates"][:1] or [None])[0], cats=cats)


def battery(t):
    fq = f"LIBRARY_MARTS.{db.ident(t['schema'])}.{db.ident(t['table'])}"
    p = plan(t)
    res = dict(table=t["table"], schema=t["schema"], catalog_rows=t["rows"], tags=t["tags"],
               metrics=[m for m, _ in p["metrics"]], actor=p["actor"], date=p["date"], cats=p["cats"], q={})
    sel = ["COUNT(*) AS N"]
    for i, (m, typ) in enumerate(p["metrics"]):
        e = expr(m, typ)
        sel += [f"COUNT({e}) AS NN{i}", f"APPROX_COUNT_DISTINCT({e}) AS ND{i}", f"MIN({e}) AS MN{i}",
                f"MAX({e}) AS MX{i}", f"SUM({e}) AS SM{i}", f"APPROX_PERCENTILE({e}, 0.5) AS P50_{i}",
                f"APPROX_PERCENTILE({e}, 0.99) AS P99_{i}"]
    if p["date"]:
        sel += [f"MIN({q(p['date'])})::VARCHAR AS D_MIN", f"MAX({q(p['date'])})::VARCHAR AS D_MAX"]
    if p["actor"]:
        sel += [f"COUNT({q(p['actor'])}) AS A_NN", f"APPROX_COUNT_DISTINCT({q(p['actor'])}) AS A_ND"]
    rows, err, secs = run(f"SELECT {', '.join(sel)} FROM {fq}")
    res["q"]["profile"] = dict(row=rows[0] if rows else None, err=err, secs=secs)
    prof = rows[0] if rows else {}

    if p["actor"] and not err:
        a = q(p["actor"])
        if p["metrics"]:
            e = expr(*p["metrics"][0])
            g = f"SELECT {a} AS K, COUNT(*) AS C, SUM({e}) AS S FROM {fq} GROUP BY 1"
            order = "COALESCE(S, 0) DESC, C DESC"
        else:
            g = f"SELECT {a} AS K, COUNT(*) AS C, NULL::FLOAT AS S FROM {fq} GROUP BY 1"
            order = "C DESC"
        sql = (f"WITH g AS ({g}) SELECT K, C, S, SUM(C) OVER () AS TC, SUM(S) OVER () AS TS, "
               f"COUNT(*) OVER () AS NK FROM g ORDER BY {order} LIMIT 10")
        rows, err2, secs = run(sql)
        res["q"]["actors"] = dict(rows=rows, err=err2, secs=secs)

    if p["metrics"] and prof.get("P99_0") is not None and prof.get("SM0"):
        e = expr(*p["metrics"][0])
        p99, p50 = float(prof["P99_0"]), float(prof.get("P50_0") or 0)
        sql = (f"SELECT SUM(IFF({e} >= {p99!r}, {e}, 0)) / NULLIF(SUM({e}), 0) AS TOP1_SHARE, "
               f"COUNT_IF({e} >= {p99!r}) AS TOP1_ROWS, "
               f"COUNT_IF({p50!r} > 0 AND {e} > 10 * {p50!r}) AS OVER10X FROM {fq}")
        rows, err3, secs = run(sql)
        res["q"]["tail"] = dict(row=rows[0] if rows else None, err=err3, secs=secs)

    if p["cats"] and not err:
        sel = [f"APPROX_TOP_K({q(c)}, 5) AS TK{i}" for i, c in enumerate(p["cats"])]
        rows, err4, secs = run(f"SELECT {', '.join(sel)} FROM {fq}")
        res["q"]["cats"] = dict(row=rows[0] if rows else None, err=err4, secs=secs)
    return res


def done_tables():
    if not OUT.exists():
        return set()
    return {json.loads(x)["table"] for x in OUT.read_text(encoding="utf-8").splitlines() if x.strip()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    T = L.load_catalog()
    todo = [r["table"] for r in L.read_tsv("singles") if r["status"] == "untouched"]
    if a.only:
        todo = [x for x in todo if x == a.only]
    seen = set() if a.only else done_tables()  # --only reruns; readers keep the newest line per table
    todo = [x for x in todo if x not in seen and T[x]["rows"]]
    todo.sort(key=lambda x: T[x]["rows"])  # small first: early rows land fast
    print(f"battery A: {len(todo)} tables to run, {len(seen)} already done", flush=True)
    n = 0
    with ThreadPoolExecutor(a.workers) as ex:
        futs = {ex.submit(battery, T[x]): x for x in todo}
        for f in as_completed(futs):
            x = futs[f]
            try:
                r = f.result()
            except Exception as e:
                r = dict(table=x, fatal=str(e)[:300])
            with LOCK:
                with OUT.open("a", encoding="utf-8") as fh:
                    fh.write(json.dumps(r, default=str) + "\n")
            n += 1
            if n % 25 == 0 or n == len(todo):
                print(f"  {n}/{len(todo)} done, last {x}", flush=True)


if __name__ == "__main__":
    main()
