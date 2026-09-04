"""Brief 5 page: rows per year per date column, dead tables on top.
Reads reports/recon/studio/brief5_dead_tables_<date>.csv, writes outputs/dead_tables_<date>.html.
Zero warehouse queries."""
import json, sys, pandas as pd
from pathlib import Path
date = sys.argv[1] if len(sys.argv) > 1 else "2026-09-03"
d = pd.read_csv(f"reports/recon/studio/brief5_dead_tables_{date}.csv")
d = d[(d.year >= 1970) & (d.year <= 2027)]
Y0, Y1 = 1970, 2027
out = []
for (t, c), g in d.groupby(["table", "date_col"]):
    arr = [0] * (Y1 - Y0 + 1)
    for y, r in zip(g.year, g.rows): arr[y - Y0] = int(r)
    f = g.iloc[0]
    out.append([t, c, int(f.table_rows), int(f.first_year), int(f.last_year), int(f.years_dead), arr])
tpl = Path("viz/pages/dead_tables_tpl.html").read_text(encoding="utf-8")
dst = Path(f"outputs/dead_tables_{date}.html")
dst.write_text(tpl.replace("__DATA__", json.dumps({"y0": Y0, "y1": Y1, "s": out}, separators=(",", ":"))), encoding="utf-8")
print(dst, len(out), "series")
