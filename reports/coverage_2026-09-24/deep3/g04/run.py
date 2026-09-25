"""g04 read-only runner. Usage: python run.py <file.sql> [maxprint]
File holds blocks that start with a line '-- Sxx label'. Each block is one SELECT/WITH statement.
Guard (allowlist): the block must start with SELECT or WITH and hold no semicolon inside,
so only one read statement runs. Saves results to out_Sxx.json next to this file."""
import sys, json, re, datetime, decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO))
from connect import db  # noqa: E402


def blocks(text):
    cur = None
    out = []
    for line in text.splitlines():
        m = re.match(r'^--\s*(S\d+)\b(.*)$', line)
        if m:
            if cur:
                out.append(cur)
            cur = [m.group(1), m.group(2).strip(), []]
        elif cur is not None:
            cur[2].append(line)
    if cur:
        out.append(cur)
    return [(a, b, '\n'.join(c).strip().rstrip(';').strip()) for a, b, c in out]


def body_ok(sql):
    s = re.sub(r'--[^\n]*', '', sql).strip()
    first = s.split(None, 1)[0].upper() if s else ''
    return first in ('SELECT', 'WITH') and ';' not in s


def conv(v):
    if isinstance(v, (datetime.date, datetime.datetime)):
        return v.isoformat()
    if isinstance(v, decimal.Decimal):
        return float(v)
    return v


def main():
    path = Path(sys.argv[1])
    maxprint = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    todo = blocks(path.read_text(encoding='utf-8'))
    for sid, label, sql in todo:
        if not body_ok(sql):
            print(f'REFUSED {sid}: not a single SELECT/WITH')
            return
    c = db.connect()
    try:
        cur = c.cursor()
        cur.execute('ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300')
        cur.execute("ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24'")
        for sid, label, sql in todo:
            print(f'===== {sid} {label}')
            try:
                cur.execute(sql)
                cols = [d[0] for d in cur.description]
                rows = [[conv(v) for v in r] for r in cur.fetchall()]
            except Exception as e:  # keep going, record the error
                print('ERROR', e)
                (HERE / f'out_{sid}.json').write_text(json.dumps({'sid': sid, 'label': label, 'sql': sql, 'error': str(e)}, indent=1), encoding='utf-8')
                continue
            (HERE / f'out_{sid}.json').write_text(json.dumps({'sid': sid, 'label': label, 'sql': sql, 'cols': cols, 'rows': rows}, indent=1, default=str), encoding='utf-8')
            print(' | '.join(cols))
            for r in rows[:maxprint]:
                print(' | '.join('' if v is None else str(v) for v in r))
            print(f'({len(rows)} rows)')
        cur.close()
    finally:
        c.close()


if __name__ == '__main__':
    main()
