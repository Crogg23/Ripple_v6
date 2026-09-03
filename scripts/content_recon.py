"""Content recon — gen 1 and gen 2, every LANDING table.

Gen 1, five atoms per table, from ONE scan:
  who        top values of name-like columns, by rows (and by dollars if an amount exists)
  what       every category column (<= 50 distinct), all values with counts
  when       rows per year for every date-like column
  where      rows per state for every state-like column
  how big    min / median / p99 / max / sum for every amount-like column
Gen 2, who x when: each top-20 name's own rows-per-year curve.

Everything is decided from CONTENT (top values), never from column names alone,
because 98.8% of landing columns are TEXT.

Output: reports/recon/content/json/<TABLE>.json (raw) and
        reports/recon/content/pages/<TABLE>.md   (one page per table)
        reports/recon/content/index.csv           (one row per table, cost + timing)

Resume-safe: a table with a json file is skipped. Read-only. Python door.

Usage:
  python scripts/content_recon.py --tables FED_X,FED_Y      # named
  python scripts/content_recon.py --limit 5 --min-rows 1000 # first N by size desc
  python scripts/content_recon.py --all                      # the sweep
"""
from __future__ import annotations

import argparse, csv, json, re, sys, time
from pathlib import Path
from statistics import median

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from connect import db  # noqa: E402

OUT = REPO / "reports" / "recon" / "content"
JSON_DIR, PAGE_DIR = OUT / "json", OUT / "pages"
INDEX = OUT / "index.csv"
DB, SCHEMA = "LIBRARY_RAW", "LANDING"
TOPK = 12
COL_CHUNK = 120
US = set("AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY DC PR GU VI AS MP".split())
DATE_ISO = re.compile(r"^(18|19|20)\d{2}-\d{2}-\d{2}([T ].*)?$")
DATE_US = re.compile(r"^\d{1,2}/\d{1,2}/(\d{2}|\d{4})([ T].*)?$")
DATE_YMD8 = re.compile(r"^(18|19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])$")
DATE_MDY8 = re.compile(r"^(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])(18|19|20)\d{2}$")
EPOCH_MS = re.compile(r"^1[0-9]{12}(\.0+)?$")
EPOCH_S = re.compile(r"^(8|9|1[0-9])[0-9]{8}(\.0+)?$")
DATE_DMON = re.compile(r"^\d{1,2}-[A-Za-z]{3}-(\d{2}|\d{4})$")
WHO_EXCL = re.compile(r"ZIP|CITY|UEI|DUNS|SHA|COUNTRY|STATE|COUNTY|ADDRESS|STREET|PHONE|EMAIL|URL|CODE|ID$|_ID_|DATE|DESCRIPTION|TEXT|COMMENT|NOTES", re.I)
EVENT_DATE0 = re.compile(r"TRANSACTION|ACTION|FILING|FILED|REPORT|RECEIPT|EVENT|INCIDENT|ISSUE|DECISION|AWARD|DISBURSE|PAYMENT|^DATE$", re.I)
EVENT_DATE = re.compile(r"ACTION|TRANSACTION|FILING|FILED|REPORT|EFFECTIVE|ISSUE|RECEIPT|EVENT|INCIDENT|ORDER|DECISION|AWARD|SIGNED|OPEN|START|BEGIN|DISBURSE|PAYMENT|^DATE|_DATE$|_DT$", re.I)
AUDIT_RX = re.compile(r"INGEST|LOADED|_LOADED|LOAD_TS|CREATED_AT|UPDATED_AT|_AT$|SNAPSHOT|RUN_ID|FILE_NAME", re.I)
NUM_RX = re.compile(r"^-?\$?\(?[\d,]*\.?\d+\)?$")
AMT_NAME = re.compile(r"AMOUNT|AMT|TOTAL|DOLLAR|COST|VALUE|PRICE|PAY|SALARY|OBLIG|AWARD|SUM|FEE|WAGE|REVENUE|BUDGET|SPEND|DISBURS|RECEIPT|CONTRIB", re.I)
NAME_NAME = re.compile(r"NAME|VENDOR|RECIPIENT|PAYEE|COMMITTEE|EMPLOYER|COMPANY|ORG|ENTITY|FACILITY|CONTRACTOR|OWNER|FILER|CANDIDATE|PROVIDER|AGENCY|LICENSEE|BUSINESS|MANUFACTURER|SPONSOR|APPLICANT|GRANTEE", re.I)
ID_NAME = re.compile(r"(^|_)(ID|KEY|CODE|NUM|NUMBER|NO|UEI|DUNS|EIN|NPI|CIK|SUB_ID|HASH|URL|LINK|GUID|UUID)(_|$)", re.I)


def q(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


def log(msg: str) -> None:
    print(msg, flush=True)


# ---------- inventory ----------
def inventory(conn, tables=None, limit=None, min_rows=0):
    sql = f"""select t.table_name, t.row_count, t.bytes
              from {DB}.information_schema.tables t
              where t.table_schema='{SCHEMA}' and t.table_type='BASE TABLE'
                and t.row_count >= {int(min_rows)}"""
    if tables:
        names = ",".join("'" + t.upper() + "'" for t in tables)
        sql += f" and t.table_name in ({names})"
    sql += " order by t.row_count desc"
    if limit:
        sql += f" limit {int(limit)}"
    return db.rows(conn, sql)


def columns(conn, table):
    return db.rows(conn, f"""select column_name, data_type from {DB}.information_schema.columns
        where table_schema='{SCHEMA}' and table_name='{table}' order by ordinal_position""")


# ---------- gen 1: the one scan ----------
def scan(conn, table, cols):
    """One pass per <=COL_CHUNK columns: distinct, blank count, top-K per column."""
    fq = f"{DB}.{SCHEMA}.{q(table)}"
    out = {}
    for i in range(0, len(cols), COL_CHUNK):
        chunk = cols[i:i + COL_CHUNK]
        parts = ["count(*)"]
        for name, typ in chunk:
            c = f"to_varchar({q(name)})" if typ != "TEXT" else q(name)
            parts.append(f"approx_count_distinct({c})")
            parts.append(f"count_if(nullif(trim({c}),'') is null)")
            parts.append(f"approx_top_k(left({c}, 200), {TOPK}, 200)")
        r = db.rows(conn, f"select {', '.join(parts)} from {fq}")[0]
        total = r[0]
        for j, (name, typ) in enumerate(chunk):
            nd, blank, top = r[1 + j * 3], r[2 + j * 3], r[3 + j * 3]
            top = json.loads(top) if isinstance(top, str) else (top or [])
            top = [(str(v), int(n)) for v, n in top if v is not None and str(v).strip() != ""]
            out[name] = {"type": typ, "distinct": int(nd or 0), "blank": int(blank or 0), "top": top}
    return total, out


def classify(name, prof, total):
    """Content-first typing. Returns a set of roles."""
    top = prof["top"]
    vals = [v for v, _ in top]
    nonblank = max(total - prof["blank"], 1)
    roles = set()
    if not vals:
        return {"empty"}
    frac = lambda rx: sum(1 for v in vals if rx.match(v.strip())) / len(vals)
    prof["date_fmt"] = None
    if prof["type"] in ("TIMESTAMP_NTZ", "DATE"):
        prof["date_fmt"] = "native"
    else:
        for fmt, rx in (("iso", DATE_ISO), ("us", DATE_US), ("ymd8", DATE_YMD8), ("mdy8", DATE_MDY8), ("dmon", DATE_DMON), ("epochms", EPOCH_MS)):
            if frac(rx) >= 0.8:
                prof["date_fmt"] = fmt
                break
        if not prof["date_fmt"] and re.search(r"DATE|_DT$|TIME", name, re.I) and frac(EPOCH_S) >= 0.8:
            prof["date_fmt"] = "epochs"
    if prof["date_fmt"]:
        roles.add("date")
        if AUDIT_RX.search(name):
            roles.add("audit")
    if AUDIT_RX.search(name):
        roles.add("audit")
    if frac(NUM_RX) >= 0.8 and "date" not in roles and "audit" not in roles and prof["distinct"] >= 2:
        decimals = any("." in v for v in vals)
        if decimals or AMT_NAME.search(name) or prof["type"] in ("NUMBER", "FLOAT"):
            id_like = ID_NAME.search(name) or re.search(r"(_ID|ID|_NO|_NUM|NUMBER|CODE|ZIP|FIPS|GEOID|_KEY|YEAR|_YR|LAT|LON|LONG)$", name, re.I)
            if not id_like and not re.search(r"DATE|_DT$|TIME", name, re.I):
                roles.add("amount")
    if all(len(v.strip()) == 2 and v.strip().upper() in US for v in vals) and len(vals) >= 3:
        roles.add("state")
    if prof["distinct"] <= 50 and prof["distinct"] >= 2 and not roles:
        roles.add("category")
    ratio = prof["distinct"] / nonblank
    avglen = sum(len(v) for v in vals) / len(vals)
    if roles <= {"audit"} and avglen >= 6 and 0.00001 <= ratio <= 0.6 and not ID_NAME.search(name) and not AUDIT_RX.search(name):
        roles.add("who")
    if roles <= {"audit"} and NAME_NAME.search(name) and prof["distinct"] > 1 and not AUDIT_RX.search(name):
        roles.add("who")
    if roles <= {"audit"} and ratio > 0.95 and prof["distinct"] > 1000:
        roles.add("id")
    return roles or {"other"}


def year_expr(col, typ, fmt="iso"):
    c = q(col)
    if fmt == "native":
        return f"year({c})"
    if fmt == "iso":
        return f"try_to_number(left({c}, 4))"
    if fmt == "us":
        y = f"try_to_number(split_part(split_part({c},' ',1),'/',3))"
        return f"iff({y} < 100, 2000 + {y}, {y})"
    if fmt == "ymd8":
        return f"try_to_number(left({c}, 4))"
    if fmt == "epochms":
        n = f"try_to_number({c}, 20, 0)"
        return f"iff({n} between 0 and 4000000000000, year(dateadd(second, floor({n} / 1000), '1970-01-01'::timestamp_ntz)), null)"
    if fmt == "epochs":
        n = f"try_to_number({c}, 20, 0)"
        return f"iff({n} between 0 and 4000000000, year(dateadd(second, {n}, '1970-01-01'::timestamp_ntz)), null)"
    if fmt == "dmon":
        return f"coalesce(year(try_to_date({c}, 'DD-MON-YY')), year(try_to_date({c}, 'DD-MON-YYYY')))"
    if fmt == "mdy8":
        return f"try_to_number(substr({c}, 5, 4))"
    return "null"


def amt_expr(col, typ):
    c = f"to_varchar({q(col)})" if typ != "TEXT" else q(col)
    return f"try_to_number(replace(replace(replace({c},',',''),'$',''),' ',''), 20, 2)"


def when(conn, fq, col, typ, fmt):
    r = db.rows(conn, f"select {year_expr(col, typ, fmt)} y, count(*) from {fq} group by 1 order by 1")
    return [(int(y), int(n)) for y, n in r if y and 1800 <= y <= 2035]


def how_big(conn, fq, col, typ):
    a = amt_expr(col, typ)
    r = db.rows(conn, f"""select count({a}), min({a}), median({a}), approx_percentile({a},0.99), max({a}), sum({a})
                          from {fq}""")[0]
    return dict(zip(["n", "min", "median", "p99", "max", "sum"], [float(x) if x is not None else None for x in r]))


def who_top(conn, fq, col, typ, amt=None, n=20):
    c = q(col)
    if amt:
        a = amt_expr(*amt)
        r = db.rows(conn, f"""select {c}, count(*), sum({a}) from {fq}
                              where nullif(trim({c}),'') is not null group by 1 order by 3 desc nulls last limit {n}""")
        by_sum = [(str(v), int(k), float(s or 0)) for v, k, s in r]
    else:
        by_sum = []
    r = db.rows(conn, f"""select {c}, count(*) from {fq}
                          where nullif(trim({c}),'') is not null group by 1 order by 2 desc limit {n}""")
    return [(str(v), int(k)) for v, k in r], by_sum


# ---------- gen 2: who x when ----------
def who_x_when(conn, fq, who, names, date, amt=None):
    c, y = q(who[0]), year_expr(*date)
    lst = ",".join("'" + n.replace("'", "''") + "'" for n in names)
    s = f", sum({amt_expr(*amt)})" if amt else ", null"
    r = db.rows(conn, f"select {c}, {y}, count(*){s} from {fq} where {c} in ({lst}) group by 1,2 order by 1,2")
    out = {}
    for v, yr, k, sm in r:
        if yr and 1800 <= yr <= 2035:
            out.setdefault(str(v), []).append((int(yr), int(k), float(sm) if sm is not None else None))
    return out


# ---------- driver ----------
def recon_table(conn, table, rowcount):
    t0 = time.time()
    fq = f"{DB}.{SCHEMA}.{q(table)}"
    cols = columns(conn, table)
    total, prof = scan(conn, table, cols)
    roles = {n: sorted(classify(n, p, total)) for n, p in prof.items()}
    typ = {n: t for n, t in cols}
    R = {"table": table, "rows": total, "ncols": len(cols), "profile": prof, "roles": roles,
         "when": {}, "where": {}, "how_big": {}, "who": {}, "who_x_when": {}, "what": {}}

    def with_role(r):
        return [n for n in prof if r in roles[n]]

    for n in with_role("category"):
        R["what"][n] = prof[n]["top"]
    for n in with_role("state"):
        R["where"][n] = prof[n]["top"]
    R["errors"] = {}
    for n in with_role("date")[:6]:
        try:
            R["when"][n] = when(conn, fq, n, typ[n], prof[n]["date_fmt"])
        except Exception as e:  # a bad column must not sink the table
            R["errors"][n] = str(e)[:160]
    amts = with_role("amount")[:6]
    for n in list(amts):
        try:
            R["how_big"][n] = how_big(conn, fq, n, typ[n])
        except Exception as e:
            R["errors"][n] = str(e)[:160]
            amts.remove(n)
    # the main amount = biggest sum
    main_amt = None
    if amts:
        best = min(amts, key=lambda n: (0 if AMT_NAME.search(n) else 1, -(R["how_big"][n]["n"] or 0)))
        main_amt = (best, typ[best])
    whos = sorted(with_role("who"), key=lambda n: (0 if "NAME" in n.upper() else 1, 1 if WHO_EXCL.search(n) else 0,
                                                    0 if NAME_NAME.search(n) else 1, -prof[n]["distinct"]))[:4]
    for n in list(whos):
        try:
            R["who"][n] = dict(zip(["by_rows", "by_sum"], who_top(conn, fq, n, typ[n], main_amt)))
        except Exception as e:
            R["errors"][n] = str(e)[:160]
            whos.remove(n)
    # gen 2
    dates = [n for n in R["when"] if "audit" not in roles[n]] or list(R["when"])
    if whos and dates:
        main_date = min(dates, key=lambda n: (0 if EVENT_DATE0.search(n) else 1 if EVENT_DATE.search(n) else 2, R["profile"][n]["blank"],
                                              -len([1 for y, k in R["when"].get(n, []) if k > R["rows"] * 0.001])))
        for n in whos[:2]:
            names = [v for v, _ in R["who"][n]["by_rows"]]
            if R["who"][n]["by_sum"]:
                names = list(dict.fromkeys(names + [v for v, _, _ in R["who"][n]["by_sum"]]))[:30]
            try:
                R["who_x_when"][n] = {"date": main_date, "amount": main_amt[0] if main_amt else None,
                                       "curves": who_x_when(conn, fq, (n, typ[n]), names, (main_date, typ[main_date], prof[main_date]["date_fmt"]), main_amt)}
            except Exception as e:
                R["errors"][n + " x " + main_date] = str(e)[:160]
    R["seconds"] = round(time.time() - t0, 1)
    return R


def fmt_n(x):
    if x is None:
        return "-"
    if abs(x) >= 1e9:
        return f"{x/1e9:.2f}B"
    if abs(x) >= 1e6:
        return f"{x/1e6:.2f}M"
    if abs(x) >= 1e3:
        return f"{x/1e3:.1f}K"
    return f"{x:,.2f}" if isinstance(x, float) and x != int(x) else f"{int(x):,}"


def bar(v, mx, w=30):
    return "#" * int(round(w * v / mx)) if mx else ""


def page(R):
    L = [f"# {R['table']}", "", f"rows {fmt_n(R['rows'])}  columns {R['ncols']}  scan {R['seconds']}s", ""]
    roles = R["roles"]
    summary = {}
    for n, rs in roles.items():
        for r in rs:
            summary[r] = summary.get(r, 0) + 1
    L.append("roles: " + ", ".join(f"{k} {v}" for k, v in sorted(summary.items())))
    L.append("")
    if R.get("errors"):
        L.append("## errors")
        for k, v in R["errors"].items():
            L.append(f"  {k}: {v}")
        L.append("")
    if R["when"]:
        L.append("## when")
        for col, hist in R["when"].items():
            L.append(f"\n{col}")
            mx = max((n for _, n in hist), default=0)
            for y, n in hist:
                L.append(f"  {y}  {fmt_n(n):>8}  {bar(n, mx)}")
        L.append("")
    if R["how_big"]:
        L.append("## how big")
        L.append("| column | n | min | median | p99 | max | sum |\n|---|---|---|---|---|---|---|")
        for col, s in R["how_big"].items():
            L.append(f"| {col} | {fmt_n(s['n'])} | {fmt_n(s['min'])} | {fmt_n(s['median'])} | {fmt_n(s['p99'])} | {fmt_n(s['max'])} | {fmt_n(s['sum'])} |")
        L.append("")
    if R["who"]:
        L.append("## who")
        for col, d in R["who"].items():
            L.append(f"\n{col} by rows")
            for v, k in d["by_rows"]:
                L.append(f"  {fmt_n(k):>8}  {v[:70]}")
            if d["by_sum"]:
                L.append(f"\n{col} by dollars")
                for v, k, s in d["by_sum"]:
                    L.append(f"  {fmt_n(s):>10}  {fmt_n(k):>7} rows  {v[:60]}")
        L.append("")
    if R["who_x_when"]:
        L.append("## who x when")
        for col, d in R["who_x_when"].items():
            stamp = "  LOAD STAMP, not an event date" if AUDIT_RX.search(d["date"]) else ""
            L.append(f"\n{col} by {d['date']}{stamp}" + (f", dollars = {d['amount']}" if d["amount"] else ""))
            for name, curve in d["curves"].items():
                yrs = " ".join(f"{y}:{fmt_n(s if s is not None else k)}" for y, k, s in curve)
                L.append(f"  {name[:40]:40}  {yrs}")
        L.append("")
    if R["where"]:
        L.append("## where")
        for col, top in R["where"].items():
            L.append(f"\n{col}: " + ", ".join(f"{v} {fmt_n(k)}" for v, k in top))
        L.append("")
    if R["what"]:
        L.append("## what")
        for col, top in R["what"].items():
            tot = sum(k for _, k in top) or 1
            L.append(f"\n{col}: " + ", ".join(f"{v[:30]} {100*k/tot:.0f}%" for v, k in top))
        L.append("")
    L.append("## every column")
    L.append("| column | roles | distinct | blank | top values |\n|---|---|---|---|---|")
    for n, p in R["profile"].items():
        tv = "; ".join(f"{v[:25]} {fmt_n(k)}" for v, k in p["top"][:4]).replace("|", "/")
        L.append(f"| {n} | {' '.join(roles[n])} | {fmt_n(p['distinct'])} | {fmt_n(p['blank'])} | {tv} |")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tables")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--min-rows", type=int, default=0)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--reclassify", action="store_true", help="rerun only tables whose roles change under the current classifier")
    a = ap.parse_args()
    JSON_DIR.mkdir(parents=True, exist_ok=True)
    PAGE_DIR.mkdir(parents=True, exist_ok=True)
    conn = db.connect()
    tables = a.tables.split(",") if a.tables else None
    if a.reclassify:
        changed = []
        for jp in JSON_DIR.glob("*.json"):
            R = json.loads(jp.read_text(encoding="utf-8"))
            new = {n: sorted(classify(n, dict(p), R["rows"])) for n, p in R["profile"].items()}
            bad = any("TRY_CAST" in v for v in (R.get("errors") or {}).values())
            if new != R["roles"] or bad:
                changed.append(jp.stem)
                jp.unlink()
        log(f"reclassify: {len(changed)} tables changed roles, rerunning")
        tables = changed or ["__NONE__"]
    inv = inventory(conn, tables, a.limit, a.min_rows)
    log(f"{len(inv)} tables in scope")
    new_index = not INDEX.exists()
    with INDEX.open("a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new_index:
            w.writerow(["table", "rows", "ncols", "seconds", "who", "when", "amount", "state", "category", "status"])
        for i, (t, rc, by) in enumerate(inv, 1):
            jp = JSON_DIR / f"{t}.json"
            if jp.exists() and not a.force:
                continue
            try:
                R = recon_table(conn, t, rc)
                jp.write_text(json.dumps(R, default=str), encoding="utf-8")
                (PAGE_DIR / f"{t}.md").write_text(page(R), encoding="utf-8")
                cnt = lambda r: sum(1 for rs in R["roles"].values() if r in rs)
                w.writerow([t, R["rows"], R["ncols"], R["seconds"], cnt("who"), cnt("date"), cnt("amount"), cnt("state"), cnt("category"), "ok"])
                log(f"[{i}/{len(inv)}] {t} rows={fmt_n(R['rows'])} cols={R['ncols']} {R['seconds']}s")
            except Exception as e:  # keep sweeping; one bad table must not kill the run
                w.writerow([t, rc, "", "", "", "", "", "", "", f"ERR {str(e)[:120]}"])
                log(f"[{i}/{len(inv)}] {t} ERROR {str(e)[:200]}")
            f.flush()
    conn.close()


if __name__ == "__main__":
    main()
