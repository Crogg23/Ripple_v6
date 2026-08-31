# Chart card - the whole loop is: edit the SQL or the plug kwargs below, then
#     python q01_hpi_by_state.py
# and refresh the browser tab (the .html next to this file is rewritten in place).
# Deeper: `ripple chart eject q01_hpi_by_state.py` inlines the plug's real Plotly code here.

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
SELECT TRY_TO_NUMBER(YR) AS YEAR, PLACE_NAME, AVG(TRY_TO_NUMBER(INDEX_NSA)) AS AVG_INDEX_NSA FROM LIBRARY_RAW.LANDING.FED_FHFA_HPI WHERE LEVEL = 'State' AND PLACE_ID IN ('CA','TX','NY','FL','OH','WA') GROUP BY 1, 2 ORDER BY 1
"""

df, meta = sqlrun.run(SQL)
print("[OK] " + str(len(df)) + " rows in " + str(meta["elapsed_s"]) + "s on "
      + str(meta["warehouse"]) + " | " + str(meta["budget"]))

# --- ejected from viz/plugs.py: this is the plug's real code, tune freely ---
import datetime as _dt  # noqa: E402
META_COLS = {'_SRC_SHA256', '_SOURCE_RUN_ID', '_INGESTED_AT'}
MAX_CATEGORIES = 8
MAX_TABLE_ROWS = 200
_US_STATES = {'IL', 'IA', 'OR', 'WI', 'NC', 'AZ', 'NM', 'RI', 'MO', 'DC', 'ND', 'WY', 'UT', 'TX', 'SC', 'IN', 'PA', 'NY', 'VT', 'OK', 'MT', 'KY', 'MD', 'CA', 'GA', 'DE', 'AL', 'HI', 'CO', 'AK', 'MA', 'TN', 'AR', 'MS', 'MI', 'VA', 'WA', 'NV', 'OH', 'PR', 'ID', 'CT', 'LA', 'WV', 'NH', 'FL', 'MN', 'SD', 'ME', 'KS', 'NJ', 'NE'}

def column_roles(df) -> dict:
    """Classify columns into roles: numeric / date / category / state / year.

    All-digit strings classify as NUMERIC, never date — Snowflake's (and
    pandas') date parsers happily read '15020000001' as an epoch, which is how
    FEC image numbers end up on a time axis. Numbers win; a real date column
    has separators or month names.
    """
    import pandas as pd

    roles = {"numeric": [], "date": [], "category": [], "state": [], "year": []}
    for col in df.columns:
        if col.upper() in META_COLS:
            continue
        s = df[col].dropna()
        if s.empty:
            continue
        sample = s.iloc[:200]
        name = col.upper()

        as_num = pd.to_numeric(sample, errors="coerce")
        numeric_rate = float(as_num.notna().mean())
        if numeric_rate > 0.9:
            vals = as_num.dropna()
            if ("YEAR" in name or name in ("YR", "FY")) and vals.between(1790, 2100).all():
                roles["year"].append(col)
            else:
                roles["numeric"].append(col)
            continue

        looks_dateish_name = any(t in name for t in ("DATE", "_DT", "TIME", "MONTH", "DAY"))
        try:
            as_date = pd.to_datetime(sample, errors="coerce", format="mixed")
        except (ValueError, TypeError):
            as_date = pd.Series([pd.NaT] * len(sample))
        if float(as_date.notna().mean()) > 0.9 and (looks_dateish_name or as_date.nunique() > 1):
            roles["date"].append(col)
            continue

        up = sample.astype(str).str.strip().str.upper()
        if (up.isin(_US_STATES)).mean() > 0.9 and up.nunique() > 1:
            roles["state"].append(col)
            continue

        roles["category"].append(col)
    return roles


def _fold_categories(df, col: str, keep: int = MAX_CATEGORIES - 1):
    """Keep the top-N categories by frequency, fold the rest into 'Other'.

    The validated palette has 8 fixed slots; a 9th hue is never generated."""
    if col is None or col not in df.columns:
        return df
    counts = df[col].value_counts()
    if len(counts) <= keep + 1:
        return df
    top = set(counts.index[:keep])
    out = df.copy()
    out[col] = out[col].where(out[col].isin(top), "Other")
    return out


def _title(y, x, title, source):
    """Neutral noun phrase. ASCII ' - ' only (Windows consoles are cp1252)."""
    if title:
        return title
    base = f"{y} by {x}" if y and x else (str(y or x or "result"))
    return f"{base} - {source}" if source else base


def _finish(fig, *, title=None, as_of=None):
    """House template + the honesty stamp ('data as of ...')."""
    theme.apply(fig)
    if title:
        fig.update_layout(title_text=title)
    stamp = f"data as of {as_of} | queried {_dt.date.today().isoformat()}" if as_of else None
    if stamp:
        fig.add_annotation(
            text=stamp, xref="paper", yref="paper", x=0, y=-0.14,
            showarrow=False, font=dict(color=theme.MUTED, size=11), align="left",
        )
    return fig


def _pick(roles, kind, taken=()):
    for c in roles.get(kind, []):
        if c not in taken:
            return c
    return None


def line(df, x=None, y=None, color=None, title=None, source=None, as_of=None, **px_kwargs):
    """A value over time. Defaults: first date/year column x, first numeric y."""
    import pandas as pd
    import plotly.express as px
    roles = column_roles(df)
    x = x or _pick(roles, "date") or _pick(roles, "year")
    y = y or _pick(roles, "numeric", taken=(x,))
    d = _fold_categories(df, color) if color else df
    d = d.sort_values(x) if x in d.columns else d
    if x in roles.get("date", []):
        d = d.assign(**{x: pd.to_datetime(d[x], errors="coerce", format="mixed")})
    fig = px.line(d, x=x, y=y, color=color, **px_kwargs)
    fig.update_traces(line_width=2)
    return _finish(fig, title=_title(y, x, title, source), as_of=as_of)
# --- end ejected code ---

# --- plug call (now local - the function above) ---
fig = line(df, x='YEAR', y='AVG_INDEX_NSA', color='PLACE_NAME', as_of=meta["as_of"])
# --- end plug call ---

OUT = Path(__file__).with_suffix(".html")
import webbrowser  # noqa: E402
fig.write_html(OUT, include_plotlyjs="directory", config=theme.PLOT_CONFIG)
print("[OK] wrote " + OUT.name)
if not os.environ.get("RIPPLE_NO_OPEN"):
    webbrowser.open(OUT.resolve().as_uri())
