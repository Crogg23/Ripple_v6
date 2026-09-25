"""g43 deep3 runner. Read-only SELECT/WITH. Usage: python run.py <batch.sql>
Batch file holds statements split by lines starting '-- [' (the tag line).
Each result lands as g43/<tag>.json and the statement is appended to g43/_ran.sql.
"""
import sys, json, re, datetime, decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[3]))
from connect import db  # noqa: E402

def conv(v):
    if isinstance(v, decimal.Decimal):
        return float(v)
    if isinstance(v, (datetime.date, datetime.datetime)):
        return v.isoformat()
    return v

text = Path(sys.argv[1]).read_text(encoding="utf-8")
parts = re.split(r"(?m)^(-- \[\d+\][^\n]*)\n", text)
stmts = []
for i in range(1, len(parts), 2):
    tag, body = parts[i], parts[i + 1].strip().rstrip(";")
    first = re.sub(r"(?s)^(\s*--[^\n]*\n)*", "", body).lstrip().lower()
    if not (first.startswith("select") or first.startswith("with")):
        raise SystemExit(f"refusing non-read statement: {tag}")
    stmts.append((tag, body))

c = db.connect()
cur = c.cursor()
cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
cur.execute("ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24'")
with open(HERE / "_ran.sql", "a", encoding="utf-8") as log:
    log.write("-- new connection: ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300; ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24';\n\n")
    for tag, body in stmts:
        name = re.sub(r"[^a-z0-9_]+", "_", tag.lower()).strip("_")
        try:
            cur.execute(body)
            cols = [d[0] for d in cur.description]
            rows = [[conv(v) for v in r] for r in cur.fetchall()]
            out = {"tag": tag, "cols": cols, "rows": rows}
            status = f"{len(rows)} rows"
        except Exception as e:  # keep going, record the error
            out = {"tag": tag, "error": str(e)}
            status = "ERROR " + str(e)[:200]
        (HERE / f"{name}.json").write_text(json.dumps(out, indent=1, default=str), encoding="utf-8")
        log.write(f"{tag}\n{body};\n\n")
        print(f"{tag}: {status}")
        if "rows" in out:
            print("  " + " | ".join(out["cols"]))
            for r in out["rows"][:40]:
                print("  " + " | ".join(str(v) for v in r))
cur.close()
c.close()
