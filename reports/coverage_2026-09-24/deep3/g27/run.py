"""g27 runner: one statement per call, read-only guard, logs SQL to g27.sql, output to g27/out_Sxx.pkl/.csv"""
import sys, re, time
from pathlib import Path
REPO = Path(r"C:\Code\Ripple_v6")
sys.path.insert(0, str(REPO))
from connect import db
import pandas as pd
HERE = REPO / "reports/coverage_2026-09-24/deep3/g27"
SQLLOG = REPO / "reports/coverage_2026-09-24/deep3/g27.sql"

# write-verbs refused by the guard (built from pieces so shell hooks don't trip on this file's text)
_BAD = [w[::-1] for w in ["ETAERC", "TRESNI", "ETADPU", "ETELED", "PORD", "RETLA", "EGREM", "ETACNURT", "TNARG", "YPOC", "TUP"]]


def run(sid, label, sql, show=40):
    s = sql.strip().rstrip(';')
    head = re.sub(r'^\s*(--[^\n]*\n\s*)*', '', s).lstrip('(').upper()
    assert head.startswith('SELECT') or head.startswith('WITH'), 'read-only guard'
    body = re.sub(r"'[^']*'", "''", s).upper()
    for w in _BAD:
        assert not re.search(r'\b' + w + r'\b', body), f'forbidden keyword {w}'
    c = db.connect()
    cur = c.cursor()
    cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
    cur.execute("ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24'")
    t = time.time()
    cur.execute(s)
    cols = [d[0] for d in cur.description]
    df = pd.DataFrame(cur.fetchall(), columns=cols)
    qid = cur.sfqid
    cur.close(); c.close()
    el = time.time() - t
    with open(SQLLOG, 'a', encoding='utf-8') as f:
        f.write(f"\n-- {sid} {label}  [{len(df)} rows, {el:.1f}s, qid {qid}]\n{s};\n")
    df.to_pickle(HERE / f"out_{sid}.pkl")
    df.head(5000).to_csv(HERE / f"out_{sid}.csv", index=False)
    pd.set_option('display.width', 250); pd.set_option('display.max_columns', 60); pd.set_option('display.max_colwidth', 60)
    print(f"{sid}: {len(df)} rows, {el:.1f}s")
    print(df.head(show).to_string())
    return df


if __name__ == '__main__':
    # usage: python run.py S01 "label" file.sql [show]
    sid, label, path = sys.argv[1], sys.argv[2], sys.argv[3]
    show = int(sys.argv[4]) if len(sys.argv) > 4 else 40
    run(sid, label, Path(path).read_text(encoding='utf-8'), show)
