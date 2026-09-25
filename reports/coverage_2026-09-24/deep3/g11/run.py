"""g11 runner: read-only statements, one connection per call, results saved as JSON.

Usage: python run.py <batch_file.sql>
The batch file holds statements separated by lines that start with '-- S' labels.
Each labelled statement must be SELECT or WITH; anything else is refused.
"""
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO))
from connect import db  # noqa: E402

HERE = Path(__file__).resolve().parent


def split(text):
    parts = re.split(r"^(-- S\d+[^\n]*)\n", text, flags=re.M)
    out = []
    for i in range(1, len(parts), 2):
        label = parts[i].strip()
        sql = parts[i + 1].strip().rstrip(";").strip()
        body = "\n".join(l for l in sql.splitlines() if not l.strip().startswith("--")).strip()
        head = body.lstrip("( \n").upper()
        if not (head.startswith("SELECT") or head.startswith("WITH")):
            raise SystemExit(f"refused non-read statement: {label}")
        for bad in ("INSERT ", "UPDATE ", "DELETE ", "DROP ", "CREATE ", "ALTER ", "MERGE ", "TRUNCATE "):
            if re.search(r"\b" + bad.strip() + r"\b", body.upper()):
                raise SystemExit(f"refused: {bad.strip()} inside {label}")
        out.append((label, sql))
    return out


def main():
    batch = Path(sys.argv[1])
    stmts = split(batch.read_text(encoding="utf-8"))
    c = db.connect()
    try:
        db.rows(c, "ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
        db.rows(c, "ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24'")
        for label, sql in stmts:
            print("=" * 100)
            print(label)
            try:
                res = db.dicts(c, sql)
            except Exception as e:  # keep going, report
                print("ERROR:", str(e)[:800])
                res = {"error": str(e)[:2000]}
            tag = label.split()[1]
            (HERE / f"{tag}.json").write_text(json.dumps(res, default=str, indent=1), encoding="utf-8")
            if isinstance(res, list):
                for r in res[:60]:
                    print({k: (str(v)[:300] if v is not None else None) for k, v in r.items()})
                if len(res) > 60:
                    print(f"... {len(res)} rows")
    finally:
        c.close()


if __name__ == "__main__":
    main()
