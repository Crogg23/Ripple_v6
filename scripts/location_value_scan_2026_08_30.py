"""Value scan of every location-shaped mart column (2026-08-30).

The 08-29 location index (reports/location_index/location_columns_all.csv) was a NAME scan: 2,244
columns in 386 marts that look like places. This measures each one live: fill, distinct values,
top values, sentinel share, and a shape test per kind (2-letter state code? 5-digit ZIP? FIPS
length? lat/lon in range? ...). One query per table; read-only; checkpointed per table.

Output: reports/location_index/location_values_2026-08-30.json (+ .log)
Then:  python scripts/location_value_scan_2026_08_30.py --report   -> LOCATION_VALUES.md + location_columns_verified.csv
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
import time
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
REPO = os.path.dirname(HERE)
IDX = os.path.join(REPO, "reports", "location_index", "location_columns_all.csv")
OUT = os.path.join(REPO, "reports", "location_index", "location_values_2026-08-30.json")
LOGP = os.path.join(REPO, "reports", "location_index", "location_values_2026-08-30.log")
MD = os.path.join(REPO, "reports", "location_index", "LOCATION_VALUES.md")
VCSV = os.path.join(REPO, "reports", "location_index", "location_columns_verified.csv")
DB = "LIBRARY_MARTS"

STATES = ("AL AK AZ AR CA CO CT DE DC FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA "
          "RI SC SD TN TX UT VT VA WA WV WI WY PR VI GU AS MP").split()
STATE_LIST = ",".join(f"'{s}'" for s in STATES)
SENTINELS = "'', 'NAN', 'NULL', 'NONE', 'N/A', 'NA', 'UNKNOWN', 'UNK', 'XX', 'ZZ', '0', '00', '000', '00000', '99999', '-', '.', '?', 'NOT AVAILABLE', 'NOT APPLICABLE', 'NOT REPORTED', 'UNSPECIFIED'"


def q(col):
    return col if re.fullmatch(r"[A-Z_][A-Z0-9_]*", col) else '"' + col.replace('"', '""') + '"'


def frag(i, col, kind, dtype):
    """Per-column SELECT fragments. Text-cast everything; landing/marts are mostly VARCHAR anyway."""
    c = q(col)
    t = f"NULLIF(TRIM(TO_VARCHAR({c})),'')"
    u = f"UPPER({t})"
    parts = [
        f"COUNT({t}) AS f{i}_filled",
        f"APPROX_COUNT_DISTINCT({u}) AS f{i}_distinct",
        f"COUNT_IF({u} IN ({SENTINELS})) AS f{i}_sentinel",
        f"APPROX_TOP_K({u}, 5) AS f{i}_top",
    ]
    if kind == "state":
        parts += [f"COUNT_IF({u} IN ({STATE_LIST})) AS f{i}_shape",
                  f"COUNT_IF(LENGTH({u}) > 2 AND {u} NOT IN ({SENTINELS})) AS f{i}_shape2"]  # full names
    elif kind == "zip":
        parts += [f"COUNT_IF(REGEXP_LIKE({t}, '^[0-9]{{5}}(-?[0-9]{{4}})?$')) AS f{i}_shape",
                  f"COUNT_IF(REGEXP_LIKE({t}, '^[0-9]{{1,4}}$')) AS f{i}_shape2"]  # leading zeros lost
    elif kind == "fips":
        parts += [f"COUNT_IF(REGEXP_LIKE({t}, '^[0-9]{{2}}$|^[0-9]{{5}}$|^[0-9]{{11}}$|^[0-9]{{15}}$')) AS f{i}_shape",
                  f"MODE(LENGTH({t})) AS f{i}_shape2"]
    elif kind == "coordinates":
        parts += [f"COUNT_IF(TRY_TO_DOUBLE({t}) BETWEEN -180 AND 180 AND TRY_TO_DOUBLE({t}) <> 0) AS f{i}_shape",
                  f"COUNT_IF(TRY_TO_DOUBLE({t}) = 0) AS f{i}_shape2"]  # 0,0 = Gulf of Guinea trap
    elif kind == "county":
        parts += [f"COUNT_IF(REGEXP_LIKE({t}, '^[0-9]{{3}}$|^[0-9]{{5}}$')) AS f{i}_shape",
                  f"COUNT_IF(REGEXP_LIKE({u}, '[A-Z]')) AS f{i}_shape2"]  # code vs name
    elif kind == "country":
        parts += [f"COUNT_IF(REGEXP_LIKE({u}, '^[A-Z]{{2,3}}$')) AS f{i}_shape",
                  f"COUNT_IF({u} IN ('US','USA','UNITED STATES','UNITED STATES OF AMERICA')) AS f{i}_shape2"]
    elif kind == "census_tract":
        parts += [f"COUNT_IF(REGEXP_LIKE({t}, '^[0-9]{{11}}$|^[0-9]{{4}}(\\\\.[0-9]{{2}})?$|^[0-9]{{6}}$')) AS f{i}_shape",
                  f"MODE(LENGTH({t})) AS f{i}_shape2"]
    elif kind == "cong_district":
        parts += [f"COUNT_IF(REGEXP_LIKE({u}, '^[A-Z]{{2}}-?[0-9]{{1,2}}$|^[0-9]{{1,2}}$')) AS f{i}_shape",
                  f"MODE(LENGTH({t})) AS f{i}_shape2"]
    else:  # city / address / facility_site / region / metro / airport_port / geometry / watershed
        parts += [f"COUNT_IF(REGEXP_LIKE({u}, '[A-Z]')) AS f{i}_shape",
                  f"MODE(LENGTH({t})) AS f{i}_shape2"]
    return parts


def table_sql(schema, table, cols):
    sel = ["COUNT(*) AS n_rows"]
    for i, (col, kind, dtype) in enumerate(cols):
        sel += frag(i, col, kind, dtype)
    return f"SELECT {', '.join(sel)} FROM {DB}.{schema}.{table}"


def scan():
    import _snowflake_conn as sf
    groups = defaultdict(list)
    with open(IDX, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            groups[(r["domain"], r["table"])].append((r["column"], r["kind"], r["dtype"]))
    done = json.load(open(OUT, encoding="utf-8")) if os.path.exists(OUT) else {}
    log = open(LOGP, "a", encoding="utf-8")

    def L(m):
        line = f"{time.strftime('%H:%M:%S')} {m}"
        print(line, flush=True)
        log.write(line + "\n")
        log.flush()

    conn = sf.connect()
    cur = conn.cursor()
    cur.execute("ALTER SESSION SET QUERY_TAG='location_value_scan_2026_08_30'")
    cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 900")
    L(f"{len(groups)} tables, {sum(len(v) for v in groups.values())} columns; {len(done)} already done")
    t0 = time.time()
    for n, ((schema, table), cols) in enumerate(sorted(groups.items()), 1):
        key = f"{schema}.{table}"
        if key in done and "error" not in done[key]:
            continue
        try:
            cur.execute(table_sql(schema, table, cols))
            row = cur.fetchone()
            names = [d[0].lower() for d in cur.description]
            rec = dict(zip(names, row))
            n_rows = rec["n_rows"]
            out_cols = []
            for i, (col, kind, dtype) in enumerate(cols):
                top = rec.get(f"f{i}_top")
                if isinstance(top, str):
                    try:
                        top = json.loads(top)
                    except Exception:  # noqa: BLE001
                        pass
                out_cols.append(dict(column=col, kind=kind, dtype=dtype, filled=rec.get(f"f{i}_filled"),
                                     distinct=rec.get(f"f{i}_distinct"), sentinel=rec.get(f"f{i}_sentinel"),
                                     shape=rec.get(f"f{i}_shape"), shape2=rec.get(f"f{i}_shape2"), top=top))
            done[key] = dict(schema=schema, table=table, n_rows=n_rows, columns=out_cols)
            L(f"[{n}/{len(groups)}] {key}: {n_rows:,} rows, {len(cols)} cols  ({time.time()-t0:.0f}s)")
        except Exception as ex:  # noqa: BLE001
            done[key] = dict(schema=schema, table=table, error=str(ex)[:400], columns=[dict(column=c, kind=k, dtype=d) for c, k, d in cols])
            L(f"[{n}/{len(groups)}] ERR {key}: {str(ex)[:160]}")
        json.dump(done, open(OUT, "w", encoding="utf-8"), indent=0, default=str)
    L("DONE")


# ------------------------------------------------------------------ report

def _top_values(c):
    top = c.get("top") or []
    out = []
    for t in top:
        if isinstance(t, (list, tuple)) and t:
            out.append(str(t[0]))
    return out


def verdict(c, n_rows):
    """Plain-English read of one column from its numbers.

    Note: Snowflake REGEXP_LIKE matches the WHOLE string, so the '[A-Z]' letters test in the
    scan is useless for free-text kinds; those are judged from the top-5 value sample instead.
    """
    filled = c.get("filled") or 0
    if c.get("error") or filled is None:
        return "not measured", ""
    if n_rows == 0:
        return "empty table", ""
    real = filled - (c.get("sentinel") or 0)
    fill = real / n_rows if n_rows else 0
    dist = c.get("distinct") or 0
    shape = c.get("shape") or 0
    shape2 = c.get("shape2") or 0
    kind = c["kind"]
    if real <= 0:
        return "empty", "no real values (blank or sentinel only)"
    if dist <= 1:
        return "constant", "one value for the whole table"
    shape_share = shape / real if real else 0
    tops = _top_values(c)
    digits_share = (sum(1 for t in tops if re.fullmatch(r"-?[0-9.]+", t)) / len(tops)) if tops else 0
    datey = any(re.fullmatch(r"\d{4}-\d{2}-\d{2}.*", t) for t in tops)
    note = ""
    if kind == "state":
        if shape_share >= 0.95:
            v = "clean 2-letter state"
        elif (shape2 / real if real else 0) >= 0.9 and digits_share < 0.5:
            v = "state names (not codes)"
        elif digits_share >= 0.6:
            v = "state as a numeric code (FIPS / ICPSR)"
            note = "not a 2-letter code -- needs a code translation before joining"
        else:
            v = "mixed / not a state"
            note = f"only {shape_share:.0%} are 2-letter US codes (foreign provinces, money, or free text)"
    elif kind == "zip":
        lost = shape2 / real if real else 0
        if shape_share >= 0.95:
            v = "clean ZIP"
        elif lost >= 0.2:
            v = "ZIP with leading zeros lost"
            note = f"{lost:.0%} are 1-4 digits (00501 -> 501)"
        elif shape_share < 0.3 and any(re.search(r"[A-Z]", t) for t in tops):
            v = "foreign postal code"
            note = f"only {shape_share:.0%} look like US ZIPs"
        else:
            v = "mixed / not a ZIP"
            note = f"only {shape_share:.0%} look like ZIPs"
    elif kind == "fips":
        short = sum(1 for t in tops if re.fullmatch(r"[0-9]{1}|[0-9]{3,4}", t))
        if shape_share >= 0.95:
            v = f"clean FIPS ({shape2}-digit)"
        elif short >= 2 or (0.5 <= shape_share < 0.95 and digits_share >= 0.8):
            v = "FIPS with leading zeros lost"
            note = f"{shape_share:.0%} have a FIPS length; modal length {shape2} -- pad before joining"
        else:
            v = "mixed / not FIPS"
            note = f"only {shape_share:.0%} have a FIPS length; modal length {shape2}"
    elif kind == "coordinates":
        zero = (shape2 or 0) / filled if filled else 0
        if shape_share >= 0.95:
            v = "clean coordinate"
        elif shape_share + zero >= 0.9 and zero >= 0.02:
            v = "coordinate with 0,0 trap"
            note = f"{zero:.0%} are exactly 0 (Gulf of Guinea rows)"
        elif shape_share >= 0.5:
            v = "coordinate, partly out of range"
            note = f"{shape_share:.0%} parse in range"
        else:
            v = "not a coordinate (name-scan false hit)"
            note = "the name matched LONG/LAT but the values are counts or money"
    elif kind == "county":
        v = "county code" if shape_share >= 0.9 else ("county name" if digits_share < 0.5 else "mixed county")
    elif kind == "country":
        us = (shape2 or 0) / real if real else 0
        v = "country code" if shape_share >= 0.9 else "country name"
        if us >= 0.98:
            v += " (98%+ US)"
            note = "almost no foreign rows -- weak as a join axis"
    else:  # free-text kinds: judged from the sample
        if datey:
            v = "not a place (dates)"
            note = "name-scan false hit"
        elif digits_share >= 0.8:
            v = "coded place (numbers)"
            note = "codes, not names -- needs a lookup to become a place"
        else:
            v = "text place"
    if fill < 0.05:
        note = (note + "; " if note else "") + f"only {fill:.1%} of rows filled"
    return v, note


def report():
    done = json.load(open(OUT, encoding="utf-8"))
    rows = []
    for key, t in sorted(done.items()):
        for c in t["columns"]:
            v, note = verdict(dict(c, error=t.get("error")), t.get("n_rows") or 0)
            rows.append(dict(domain=t["schema"], table=t["table"], column=c["column"], kind=c["kind"], rows=t.get("n_rows"),
                             filled=c.get("filled"), real=(c.get("filled") or 0) - (c.get("sentinel") or 0),
                             distinct=c.get("distinct"), sentinel=c.get("sentinel"), verdict=v, note=note,
                             top=json.dumps(c.get("top"))[:200] if c.get("top") is not None else ""))
    with open(VCSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    n_tables = len(done)
    errs = [k for k, t in done.items() if t.get("error")]
    by_kind = defaultdict(lambda: defaultdict(int))
    for r in rows:
        by_kind[r["kind"]][r["verdict"]] += 1
    lines = [f"# Location columns, value-verified -- 2026-08-30", "",
             f"{len(rows)} columns in {n_tables} marts, measured live (fill, distinct, sentinel share, shape test per kind). "
             f"Name-scan index: location_columns_all.csv. This file's CSV twin: location_columns_verified.csv. "
             f"{len(errs)} tables failed to scan.", "",
             "## Verdicts by kind", "", "| kind | verdict | columns |", "|---|---|---:|"]
    for k in sorted(by_kind):
        for v, n in sorted(by_kind[k].items(), key=lambda x: -x[1]):
            lines.append(f"| {k} | {v} | {n} |")
    lines += ["", "## Columns that are NOT what their name says (empty, constant, mixed, trapped)", "",
              "| table | column | kind | verdict | note | top values |", "|---|---|---|---|---|---|"]
    bad = [r for r in rows if r["verdict"] in ("empty", "constant") or r["verdict"].startswith(("mixed", "not a", "foreign", "coded", "state as"))
           or "trap" in r["verdict"] or "lost" in r["verdict"] or "98%+" in r["verdict"] or "partly" in r["verdict"]]
    for r in bad:
        lines.append(f"| {r['table']} | {r['column']} | {r['kind']} | {r['verdict']} | {r['note']} | {r['top'][:80].replace('|', '/')} |")
    lines += ["", "## Every column", ""]
    cur_t = None
    for r in rows:
        if r["table"] != cur_t:
            cur_t = r["table"]
            lines += [f"### {cur_t}  ({(r['rows'] or 0):,} rows)", "", "| column | kind | real fill | distinct | verdict | note |", "|---|---|---:|---:|---|---|"]
        fill = f"{(r['real'] / r['rows']):.0%}" if r["rows"] else "-"
        lines.append(f"| {r['column']} | {r['kind']} | {fill} | {r['distinct'] or 0:,} | {r['verdict']} | {r['note']} |")
    if errs:
        lines += ["", "## Tables that failed to scan", ""] + [f"- {k}: {done[k]['error'][:200]}" for k in errs]
    open(MD, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print(f"wrote {MD} and {VCSV}: {len(rows)} columns, {len(bad)} flagged, {len(errs)} table errors")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args()
    report() if a.report else scan()
