"""skeptic runner: one read-only statement per call. usage: python q.py K01 file.sql"""
import sys, re, time
from pathlib import Path
REPO = Path(r"C:\Code\Ripple_v6")
sys.path.insert(0, str(REPO))
from connect import db
import pandas as pd
HERE = Path(__file__).parent
sid, path = sys.argv[1], sys.argv[2]
s = Path(path).read_text(encoding='utf-8').strip().rstrip(';')
head = re.sub(r'^\s*(--[^\n]*\n\s*)*', '', s).lstrip('(').upper()
assert head.startswith('SELECT') or head.startswith('WITH'), 'read-only guard'
body = re.sub(r"'[^']*'", "''", s).upper()
for w in [x[::-1] for x in ["ETAERC","TRESNI","ETADPU","ETELED","PORD","RETLA","EGREM","ETACNURT","TNARG","YPOC","TUP"]]:
    assert not re.search(r'\b'+w+r'\b', body), w
c = db.connect(); cur = c.cursor()
cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
cur.execute("ALTER SESSION SET QUERY_TAG = 'deep3-skeptic-2026-09-24'")
t = time.time(); cur.execute(s)
cols = [d[0] for d in cur.description]
df = pd.DataFrame(cur.fetchall(), columns=cols)
qid = cur.sfqid; cur.close(); c.close()
df.to_csv(HERE / f"out_{sid}.csv", index=False)
with open(HERE / "log.sql", 'a', encoding='utf-8') as f:
    f.write(f"\n-- {sid} [{len(df)} rows, {time.time()-t:.1f}s, qid {qid}]\n{s};\n")
pd.set_option('display.width', 250); pd.set_option('display.max_columns', 60); pd.set_option('display.max_colwidth', 50); pd.set_option('display.max_rows', 200)
print(f"{sid}: {len(df)} rows, {time.time()-t:.1f}s"); print(df.head(120).to_string())
