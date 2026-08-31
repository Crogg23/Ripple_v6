# Chart card - the whole loop is: edit the SQL or the plug kwargs below, then
#     python q01_name_join_lead.py
# and refresh the browser tab (the .html next to this file is rewritten in place).
# Deeper: `ripple chart eject q01_name_join_lead.py` inlines the plug's real Plotly code here.

import os
import sys
from pathlib import Path

# Find the repo root (the directory holding ripple.py) so `import viz` works
# from ANY current directory: RIPPLE_REPO env wins, then walking up from this
# file, then the repo this card was generated from.
_d = Path(os.environ.get("RIPPLE_REPO") or Path(__file__).resolve().parent)
while not (_d / "ripple.py").exists() and _d.parent != _d:
    _d = _d.parent
if not (_d / "ripple.py").exists():
    _d = Path('C:\\Code\\Ripple_v6')  # where this card was generated
if str(_d) not in sys.path:
    sys.path.insert(0, str(_d))

from viz import plugs, safety, sqlrun, theme  # noqa: E402

if os.environ.get("RIPPLE_CARD_DRY"):
    print("[OK] card imports resolve (dry run)")
    raise SystemExit(0)

SQL = """\
SELECT l.COMPANY_NAME, r.ORG_NAME FROM (SELECT 'ACME LLC' AS COMPANY_NAME) l JOIN (SELECT 'ACME LLC' AS ORG_NAME) r ON l.COMPANY_NAME = r.ORG_NAME
"""

df, meta = sqlrun.run(SQL)
print("[OK] " + str(len(df)) + " rows in " + str(meta["elapsed_s"]) + "s on "
      + str(meta["warehouse"]) + " | " + str(meta["budget"]))

# --- plug call (ripple chart eject inlines this) ---
fig = plugs.table(df, as_of=meta["as_of"])
# --- end plug call ---
fig = safety.badge(fig, 'lead', 'name-based match - investigative lead, not established fact')

OUT = Path(__file__).with_suffix(".html")
import webbrowser  # noqa: E402
fig.write_html(OUT, include_plotlyjs="directory", config=theme.PLOT_CONFIG)
print("[OK] wrote " + OUT.name)
if not os.environ.get("RIPPLE_NO_OPEN"):
    webbrowser.open(OUT.resolve().as_uri())
