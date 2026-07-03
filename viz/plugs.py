"""The plug library: point a plug at a query result, get a sane chart.

A plug is a SHORT, readable function — real Plotly Express / graph_objects code,
not a black box. The learning ramp is built in:

    week 1   fig = plugs.bar(df)                        # inference does the rest
    week 2   fig = plugs.bar(df, x="STATE", y="TOTAL")  # you pick the mapping
    week 3   fig = plugs.bar(df, color="PARTY", log_y=True)   # **px_kwargs pass
             # ...any plotly.express keyword goes straight through the plug...
    week 4   ripple chart eject <card.py>               # the plug's own body is
             # inlined into your card — hand-tune the raw px/go code from there.

House rules every plug enforces (they come from the dataviz method + the libel
discipline, not taste):
  * one axis — no dual-axis chart exists here and none will;
  * categorical colors in fixed validated order; >8 categories fold to 'Other';
  * titles are neutral noun phrases ("Y by X - SOURCE"), never causal claims,
    never present-tense claims over an archive;
  * every figure carries a "data as of" stamp when the runner knows it.

All plotly/pandas imports live INSIDE functions so offline tests can import
this module without the viz deps installed.
"""

from __future__ import annotations

import datetime as _dt

from viz import theme

# Landing-table provenance stamps — never offered as chart axes.
META_COLS = {"_INGESTED_AT", "_SOURCE_RUN_ID", "_SRC_SHA256"}

MAX_CATEGORIES = 8      # validated palette size; beyond this we fold to 'Other'
MAX_TABLE_ROWS = 200    # table plug displays at most this many rows

_US_STATES = {
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID",
    "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS",
    "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK",
    "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV",
    "WI", "WY", "DC", "PR",
}


# --------------------------------------------------------------------------- #
# Column-role sniffing (pure pandas — works on all-TEXT landing results too)
# --------------------------------------------------------------------------- #
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


# Entity-anchored colors: color follows the entity, never its rank. US parties
# have a fixed public convention — honoring it beats palette order.
PARTY_COLORS = {
    "DEMOCRAT": theme.CATEGORICAL[0], "DEMOCRATIC": theme.CATEGORICAL[0],
    "D": theme.CATEGORICAL[0], "DEM": theme.CATEGORICAL[0],
    "REPUBLICAN": theme.CATEGORICAL[5], "R": theme.CATEGORICAL[5],
    "REP": theme.CATEGORICAL[5], "GOP": theme.CATEGORICAL[5],
    "INDEPENDENT": theme.CATEGORICAL[2], "I": theme.CATEGORICAL[2],
    "IND": theme.CATEGORICAL[2], "LIBERTARIAN": theme.CATEGORICAL[2],
    "GREEN": theme.CATEGORICAL[3],
}


def _px_defaults(df, color, px_kwargs) -> dict:
    """px bakes trace colors from the ACTIVE template at figure-creation time —
    applying a template afterwards restyles the layout but not the traces. So
    every px plug passes the house template INTO the call (still overridable),
    plus the party color convention when the color column is a US party."""
    px_kwargs.setdefault("template", theme.register())
    # the name gate matters: a 'D'/'R' direction code or single-letter category
    # must not silently turn partisan blue/red - only columns NAMED party do
    if color and color in df.columns and "PARTY" in str(color).upper():
        vals = {str(v).strip().upper() for v in df[color].dropna().unique()}
        if vals and vals <= set(PARTY_COLORS):
            px_kwargs.setdefault(
                "color_discrete_map",
                {v: PARTY_COLORS[str(v).strip().upper()] for v in df[color].dropna().unique()})
    return px_kwargs


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


# --------------------------------------------------------------------------- #
# The plugs
# --------------------------------------------------------------------------- #
def bar(df, x=None, y=None, color=None, title=None, source=None, as_of=None, **px_kwargs):
    """Bars: a magnitude per category. Defaults: first category x, first numeric y."""
    import plotly.express as px
    roles = column_roles(df)
    x = x or _pick(roles, "category") or _pick(roles, "state") or _pick(roles, "year")
    y = y or _pick(roles, "numeric", taken=(x,))
    d = _fold_categories(df, color) if color else df
    if y is None:  # no numeric column -> count rows per category
        d = d.groupby(x, dropna=False).size().reset_index(name="COUNT")
        y = "COUNT"
    px_kwargs = _px_defaults(d, color, px_kwargs)
    fig = px.bar(d, x=x, y=y, color=color, **px_kwargs)
    fig.update_traces(marker_line_width=0)
    return _finish(fig, title=_title(y, x, title, source), as_of=as_of)


def line(df, x=None, y=None, color=None, title=None, source=None, as_of=None, **px_kwargs):
    """A value over time. Defaults: first date/year column x, first numeric y."""
    import pandas as pd
    import plotly.express as px
    roles = column_roles(df)
    x = x or _pick(roles, "date") or _pick(roles, "year")
    y = y or _pick(roles, "numeric", taken=(x,))
    d = _fold_categories(df, color) if color else df
    if x in roles.get("date", []):  # convert BEFORE sorting: '01/15/2024' text
        d = d.assign(**{x: pd.to_datetime(d[x], errors="coerce", format="mixed")})
    d = d.sort_values(x) if x in d.columns else d
    px_kwargs = _px_defaults(d, color, px_kwargs)
    fig = px.line(d, x=x, y=y, color=color, **px_kwargs)
    fig.update_traces(line_width=2)
    return _finish(fig, title=_title(y, x, title, source), as_of=as_of)


def area(df, x=None, y=None, color=None, title=None, source=None, as_of=None, **px_kwargs):
    """Stacked composition over time. Same defaults as line."""
    import pandas as pd
    import plotly.express as px
    roles = column_roles(df)
    x = x or _pick(roles, "date") or _pick(roles, "year")
    y = y or _pick(roles, "numeric", taken=(x,))
    d = _fold_categories(df, color) if color else df
    if x in roles.get("date", []):  # convert BEFORE sorting (see line())
        d = d.assign(**{x: pd.to_datetime(d[x], errors="coerce", format="mixed")})
    d = d.sort_values(x) if x in d.columns else d
    px_kwargs = _px_defaults(d, color, px_kwargs)
    fig = px.area(d, x=x, y=y, color=color, **px_kwargs)
    return _finish(fig, title=_title(y, x, title, source), as_of=as_of)


def scatter(df, x=None, y=None, color=None, title=None, source=None, as_of=None, **px_kwargs):
    """Two measures against each other. Defaults: first two numeric columns."""
    import plotly.express as px
    roles = column_roles(df)
    x = x or _pick(roles, "numeric")
    y = y or _pick(roles, "numeric", taken=(x,))
    d = _fold_categories(df, color) if color else df
    px_kwargs = _px_defaults(d, color, px_kwargs)
    fig = px.scatter(d, x=x, y=y, color=color, **px_kwargs)
    fig.update_traces(marker=dict(size=8))
    return _finish(fig, title=_title(y, x, title, source), as_of=as_of)


def hist(df, x=None, title=None, source=None, as_of=None, **px_kwargs):
    """Distribution of one measure. Default: first numeric column."""
    import plotly.express as px
    roles = column_roles(df)
    x = x or _pick(roles, "numeric")
    px_kwargs = _px_defaults(df, None, px_kwargs)
    fig = px.histogram(df, x=x, **px_kwargs)
    fig.update_traces(marker_line_width=0)
    return _finish(fig, title=_title(None, x, title or f"distribution of {x}", source), as_of=as_of)


def heatmap(df, x=None, y=None, z=None, title=None, source=None, as_of=None, **layout_kwargs):
    """A matrix of magnitude: two categories + a value (or a count when z=None).
    Sequential one-hue ramp — magnitude never gets a rainbow."""
    import pandas as pd
    import plotly.graph_objects as go
    roles = column_roles(df)
    x = x or _pick(roles, "category") or _pick(roles, "year")
    y = y or _pick(roles, "category", taken=(x,)) or _pick(roles, "state", taken=(x,))
    z = z or _pick(roles, "numeric", taken=(x, y))
    if z:
        grid = df.pivot_table(index=y, columns=x, values=z, aggfunc="sum")
    else:
        grid = pd.crosstab(df[y], df[x])
        z = "count"
    fig = go.Figure(go.Heatmap(
        z=grid.values, x=[str(c) for c in grid.columns], y=[str(i) for i in grid.index],
        colorscale=theme._scale(theme.SEQUENTIAL), colorbar=dict(title=z),
    ))
    fig.update_layout(**layout_kwargs)
    return _finish(fig, title=_title(z, f"{x} x {y}", title, source), as_of=as_of)


def choropleth_state(df, state=None, value=None, title=None, source=None, as_of=None, **px_kwargs):
    """US state map of one measure. Needs 2-letter state codes + a numeric."""
    import plotly.express as px
    roles = column_roles(df)
    state = state or _pick(roles, "state")
    value = value or _pick(roles, "numeric")
    px_kwargs = _px_defaults(df, None, px_kwargs)
    fig = px.choropleth(
        df, locations=state, locationmode="USA-states", color=value, scope="usa",
        color_continuous_scale=theme.SEQUENTIAL, **px_kwargs,
    )
    fig.update_geos(bgcolor=theme.BG, lakecolor=theme.BG, landcolor=theme.PANEL)
    return _finish(fig, title=_title(value, "state", title, source), as_of=as_of)


def treemap(df, path=None, values=None, title=None, source=None, as_of=None, **px_kwargs):
    """Part-of-whole across one or two category levels."""
    import plotly.express as px
    roles = column_roles(df)
    if path is None:
        cats = roles.get("category", [])[:2]
        path = cats or roles.get("state", [])[:1]
    values = values or _pick(roles, "numeric")
    px_kwargs = _px_defaults(df, None, px_kwargs)
    fig = px.treemap(df, path=path, values=values, **px_kwargs)
    fig.update_traces(marker_line=dict(color=theme.BG, width=2))
    return _finish(fig, title=_title(values, " / ".join(map(str, path)), title, source), as_of=as_of)


def big_number(df, value=None, label=None, title=None, source=None, as_of=None, **indicator_kwargs):
    """One headline number. The right 'chart' for a single-value answer."""
    import pandas as pd
    import plotly.graph_objects as go
    roles = column_roles(df)
    col = value or _pick(roles, "numeric") or df.columns[0]
    v = pd.to_numeric(df[col].dropna().iloc[0], errors="coerce") if len(df) else None
    fig = go.Figure(go.Indicator(
        mode="number", value=v,
        title={"text": label or col, "font": {"color": theme.MUTED, "size": 16}},
        number={"font": {"color": theme.FG, "size": 64}}, **indicator_kwargs,
    ))
    return _finish(fig, title=_title(None, None, title or (source or ""), None), as_of=as_of)


def table(df, title=None, source=None, as_of=None, **table_kwargs):
    """The always-works fallback: the result itself, dark-styled, capped at 200 rows."""
    import plotly.graph_objects as go
    d = df.head(MAX_TABLE_ROWS)
    fig = go.Figure(go.Table(
        header=dict(values=[str(c) for c in d.columns], fill_color=theme.PANEL,
                    font=dict(color=theme.FG, size=12), align="left"),
        cells=dict(values=[d[c].astype(str).tolist() for c in d.columns],
                   fill_color=theme.BG, font=dict(color=theme.MUTED, size=11), align="left"),
        **table_kwargs,
    ))
    note = f"first {MAX_TABLE_ROWS} rows" if len(df) > MAX_TABLE_ROWS else None
    t = _title(None, None, title or "result", source)
    return _finish(fig, title=f"{t} ({note})" if note else t, as_of=as_of)


PLUGS = {
    "bar": bar, "line": line, "area": area, "scatter": scatter, "hist": hist,
    "heatmap": heatmap, "choropleth_state": choropleth_state, "treemap": treemap,
    "big_number": big_number, "table": table,
}

# Helpers a plug body references — eject() inlines these alongside the plug so
# the ejected card is self-sufficient raw Plotly code.
EJECT_HELPERS = [column_roles, _fold_categories, _title, _finish, _pick, _px_defaults]


# --------------------------------------------------------------------------- #
# suggest(): rank plugs by the shape of the result (pure, offline-testable)
# --------------------------------------------------------------------------- #
def suggest(df) -> list[tuple[str, dict, str]]:
    """Ranked [(plug_name, kwargs, why)] for a result DataFrame."""
    roles = column_roles(df)
    n_rows = len(df)
    num, cat, date = roles["numeric"], roles["category"], roles["date"]
    year, state = roles["year"], roles["state"]
    out: list[tuple[str, dict, str]] = []

    if n_rows == 1 and len(num) == 1 and not cat:
        out.append(("big_number", {"value": num[0]}, "single value"))
    if (date or year) and num:
        x = (date or year)[0]
        out.append(("line", {"x": x, "y": num[0]}, f"{x} looks like time"))
    if state and num:
        out.append(("choropleth_state", {"state": state[0], "value": num[0]},
                    f"{state[0]} holds US state codes"))
    if cat and num:
        card = df[cat[0]].nunique() if n_rows else 0
        out.append(("bar", {"x": cat[0], "y": num[0]}, f"{card} categories vs a measure"))
        if len(cat) >= 2:
            out.append(("heatmap", {"x": cat[0], "y": cat[1], "z": num[0]}, "two categories + a measure"))
            out.append(("treemap", {"path": cat[:2], "values": num[0]}, "nested part-of-whole"))
    if len(num) >= 2:
        out.append(("scatter", {"x": num[0], "y": num[1]}, "two measures"))
    if len(num) == 1 and not cat and not date and n_rows > 20:
        out.append(("hist", {"x": num[0]}, "one measure, many rows"))
    if cat and not num:
        out.append(("bar", {"x": cat[0]}, "counts per category"))
    out.append(("table", {}, "always works"))
    return out
