# Chart card - the whole loop is: edit the SQL or the plug kwargs below, then
#     python q01_deaths_by_region.py
# and refresh the browser tab (the .html next to this file is rewritten in place).
# Deeper: `ripple chart eject q01_deaths_by_region.py` inlines the plug's real Plotly code here.

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
SELECT TRY_TO_NUMBER(YEAR) AS YEAR, REGION, SUM(TRY_TO_NUMBER(BEST)) AS DEATHS_BEST_EST FROM LIBRARY_RAW.LANDING.INTL_UCDP_GED GROUP BY 1, 2 ORDER BY 1
"""

df, meta = sqlrun.run(SQL)
print("[OK] " + str(len(df)) + " rows in " + str(meta["elapsed_s"]) + "s on "
      + str(meta["warehouse"]) + " | " + str(meta["budget"]))

# --- plug call (ripple chart eject inlines this) ---
fig = plugs.line(df, x='YEAR', y='DEATHS_BEST_EST', color='REGION', as_of=meta["as_of"])
# --- end plug call ---

OUT = Path(__file__).with_suffix(".html")
import webbrowser  # noqa: E402
fig.write_html(OUT, include_plotlyjs="directory", config=theme.PLOT_CONFIG)
print("[OK] wrote " + OUT.name)
if not os.environ.get("RIPPLE_NO_OPEN"):
    webbrowser.open(OUT.resolve().as_uri())
