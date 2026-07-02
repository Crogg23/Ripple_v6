"""The active-leads board — basic, legible, and actually correct.

Earlier this tried to burn the leads on top of the full 720-node connection web.
With every dataset drawn as a marker sized by row count, a 9.6M-row node is a
~56px bubble and the spring layout collapses into an unreadable blob that buries
every edge. So this is the BASIC version: draw only the landing tables the live
detectors actually touch, on a fixed two-column layout, and let edge thickness
carry the one finding that matters.

The detector list is DERIVED from ``leads_specs.JOBS`` — the board can never again
silently omit a rule (it hardcoded 4 of 6 once; that's how overlays rot). Tables
the layout has never seen auto-stack into their column instead of KeyError-ing.

LEFT column  = the "flag" registries (excluded / sanctioned / debarred).
RIGHT column = where those same entities turn up (paid / operating / in the AIS
archive / funded). Each detector is one edge, flag -> activity, joined on a hard
ID (NPI / IMO / UEI). Edge WIDTH = how many leads that rule is firing right now;
the concentration callout is computed from the live counts, never hardcoded.

Run:  python -m connect.leads_overlay
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import plotly.graph_objects as go

from .leads_specs import JOBS

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "leads_overlay.html"
GRAPH = ROOT / "outputs" / "connect_graph.json"


def _table_id(table: str) -> str:
    """Display id for a spec table: staging FQNs (LIBRARY_STAGING...INT_*) reduce to the
    bare object name so the board treats them like any landing table."""
    return table.split(".")[-1].upper()


# ---- every detector, derived from leads_specs.JOBS (rule -> tables + hard key) ----
DETECTORS = [
    (rule, _table_id(spec["left"]["table"]), _table_id(spec["right"]["table"]),
     spec["left"]["key"])
    for rule, spec in JOBS.items()
]

# friendly labels for the tables we know; anything new falls back to _label()
LABEL = {
    "FED_HHS_OIG_LEIE":            "OIG exclusions\n(LEIE)",
    "FED_OFAC_SDN":                "OFAC sanctions\n(SDN)",
    "FED_SAM_EXCLUSIONS":          "SAM debarments",
    "INT_SANCTIONED_VESSELS":      "Sanctioned vessels\n(OFAC ∪ OpenSanctions)",
    "FED_CMS_OPEN_PAYMENTS":       "CMS Open Payments",
    "INT_OPEN_PAYMENTS_ALL_YEARS": "CMS Open Payments\n(all years)",
    "FED_CMS_FACILITY_AFFILIATION":"CMS facility roster",
    "FED_CMS_PART_D_PRESCRIBERS":  "Medicare Part D\nprescribers",
    "FED_NOAA_AIS":                "NOAA AIS archive\n(ship tracks)",
    "FED_USASPENDING_CONTRACTS":   "USASpending\ncontracts",
    "FED_SEC_EDGAR_FINANCIALS":    "SEC EDGAR\nfinancial filers",
    "FED_IRS_BMF":                 "IRS exempt-org\nmaster file (BMF)",
}

# hand-tuned vertical ORDER for the tables we know (top -> bottom per column).
# Layout y-coordinates are computed in _layout(), so an unknown table simply
# stacks after these instead of crashing the board.
_ORDER = {
    "FED_HHS_OIG_LEIE": 0, "FED_OFAC_SDN": 1, "INT_SANCTIONED_VESSELS": 2,
    "FED_SAM_EXCLUSIONS": 3,
    "INT_OPEN_PAYMENTS_ALL_YEARS": 0, "FED_CMS_OPEN_PAYMENTS": 1,
    "FED_CMS_FACILITY_AFFILIATION": 2, "FED_CMS_PART_D_PRESCRIBERS": 3,
    "FED_NOAA_AIS": 4, "FED_USASPENDING_CONTRACTS": 5,
}

KEY_COLOR = {"NPI": "#f4a23a", "IMO": "#3ab0c4", "UEI": "#b07cf0", "EIN": "#7ee08a"}

# verified row counts (live snapshot 2026-06-27); overridden from connect_graph.json
# where the node id matches. A table with no count renders as 0 (shown as '?') —
# never a KeyError.
ROWS = {
    "FED_HHS_OIG_LEIE": 83464, "FED_OFAC_SDN": 19115, "FED_SAM_EXCLUSIONS": 1000,
    "FED_CMS_OPEN_PAYMENTS": 15385047, "FED_CMS_FACILITY_AFFILIATION": 2239952,
    "FED_NOAA_AIS": 7296275, "FED_USASPENDING_CONTRACTS": 6325622,
    "FED_SEC_EDGAR_FINANCIALS": 55635, "FED_IRS_BMF": 1974830,
}

# fallback lead counts if the warehouse is unreachable — one entry per rule in JOBS
# (verified live 2026-07-02) so an offline render still draws every detector.
FALLBACK_COUNTS = {
    "banned_but_paid": 773, "excluded_but_billing": 236, "banned_but_operating": 11,
    "sanctioned_vessel_broadcasting_v2": 6, "sanctioned_vessel_broadcasting": 2,
    "debarred_but_funded": 2, "sec_filer_in_irs_bmf": 3,
}

BG = "#0d1117"
FG = "#e8eaed"


def active_lead_counts() -> tuple[dict[str, int], bool]:
    """ONE cheap read: active lead count per rule. Falls back if Snowflake is down."""
    try:
        from . import db
        conn = db.connect()
        try:
            rows = db.rows(
                conn,
                "SELECT RULE_NAME, COUNT(*) FROM LIBRARY_META.\"CONNECT\".LEADS "
                "WHERE COALESCE(STATUS,'active')='active' GROUP BY 1",
            )
        finally:
            conn.close()
        counts = {r[0]: int(r[1]) for r in rows}
        return (counts or FALLBACK_COUNTS), bool(counts)
    except Exception as e:  # offline / no creds -> still draw the board
        print(f"  (warehouse unreachable, using verified fallback counts: {e})")
        return dict(FALLBACK_COUNTS), False


def _label(tid: str) -> str:
    """Friendly label, or a readable fallback derived from the table name."""
    if tid in LABEL:
        return LABEL[tid]
    return tid.removeprefix("INT_").removeprefix("FED_").replace("_", " ").title()


def _rows(tid: str) -> int:
    return ROWS.get(tid, 0)


def _rows_txt(tid: str) -> str:
    n = _rows(tid)
    return f"{n:,} rows" if n else "row count unknown"


def _layout(detectors) -> tuple[dict[str, tuple[float, float]], set[str]]:
    """Positions for every table the detectors touch. x: 0 = flag column, 1 = activity.
    Known tables keep their hand-tuned top-to-bottom order; unknown tables stack after
    them, evenly spaced — a new rule can never KeyError the board."""
    flags, acts = [], []
    for _, lt, rt, _ in detectors:
        if lt not in flags:
            flags.append(lt)
        if rt not in acts and rt not in flags:
            acts.append(rt)

    def col(tables: list[str], x: float) -> dict[str, tuple[float, float]]:
        ordered = sorted(tables, key=lambda t: (_ORDER.get(t, 99), t))
        n = max(len(ordered) - 1, 1)
        return {t: (x, 0.90 - 0.80 * i / n) for i, t in enumerate(ordered)}

    pos = col(flags, 0.0)
    pos.update(col(acts, 1.0))
    return pos, set(flags)


def _ewidth(cnt: int) -> float:
    return 2.5 + 5.0 * math.log10(max(cnt, 1))


def _load_graph_rows() -> None:
    """Best-effort: refresh ROWS from the cached graph so counts stay live — including
    tables ROWS has never heard of (new detectors)."""
    try:
        g = json.loads(GRAPH.read_text())
        by_id = {n["id"]: n for n in g.get("nodes", [])}
        wanted = set(ROWS) | {t for _, lt, rt, _ in DETECTORS for t in (lt, rt)}
        for tid in wanted:
            if tid in by_id and by_id[tid].get("rows"):
                ROWS[tid] = int(by_id[tid]["rows"])
    except Exception:
        pass


def build_figure(counts: dict[str, int]) -> go.Figure:
    fig = go.Figure()
    pos, flags = _layout(DETECTORS)

    # --- detector edges (flag -> activity), width by lead count, color by key ----
    for rule, lt, rt, key in DETECTORS:
        cnt = counts.get(rule, 0)
        if cnt <= 0:
            continue
        (x0, y0), (x1, y1) = pos[lt], pos[rt]
        fig.add_trace(go.Scatter(
            x=[x0, x1], y=[y0, y1], mode="lines",
            line=dict(color=KEY_COLOR.get(key, "#f4a23a"), width=_ewidth(cnt)),
            opacity=0.85, hoverinfo="text",
            hovertext=f"<b>{rule}</b><br>{cnt:,} active leads<br>"
                      f"{_label(lt).replace(chr(10),' ')} ↔ {_label(rt).replace(chr(10),' ')}<br>"
                      f"joined on {key}",
            showlegend=False,
        ))
        # edge label at the midpoint
        fig.add_annotation(
            x=(x0 + x1) / 2, y=(y0 + y1) / 2 + 0.018,
            text=f"<b>{cnt:,}</b> · {rule}",
            showarrow=False, font=dict(color=FG, size=12),
            bgcolor="rgba(13,17,23,0.72)", borderpad=2,
        )

    # --- nodes: flags (left, red ring) and activity (right, blue ring) -----------
    for group, ring, tpos in (
        ("flag", "#e5534b", "middle left"),
        ("activity", "#4c9aff", "middle right"),
    ):
        ids = [t for t in pos if (t in flags) == (group == "flag")]
        fig.add_trace(go.Scatter(
            x=[pos[t][0] for t in ids], y=[pos[t][1] for t in ids],
            mode="markers+text",
            text=[f"<b>{_label(t).splitlines()[0]}</b>"
                  + (f"<br>{_label(t).splitlines()[1]}" if "\n" in _label(t) else "")
                  + f"<br><span style='color:#8b949e'>{_rows_txt(t)}</span>"
                  for t in ids],
            textposition=tpos, textfont=dict(color=FG, size=12),
            marker=dict(size=22, color=BG, line=dict(color=ring, width=3),
                        symbol="circle"),
            hoverinfo="text",
            hovertext=[f"<b>{t}</b><br>{_rows_txt(t)}" for t in ids],
            showlegend=False,
        ))

    # --- a tiny legend for the bridging keys actually in play --------------------
    for key in sorted({k for *_, k in DETECTORS}):
        fig.add_trace(go.Scatter(
            x=[None], y=[None], mode="lines",
            line=dict(color=KEY_COLOR.get(key, "#f4a23a"), width=6),
            name=f"{key} bridge",
        ))

    # --- callouts ---------------------------------------------------------------
    total = sum(c for c in counts.values() if c > 0)
    nrules = sum(1 for c in counts.values() if c > 0)
    if total:
        # the concentration finding, DERIVED from the live counts (never frozen prose)
        top_rule, top_cnt = max(counts.items(), key=lambda kv: kv[1])
        if nrules > 1 and top_cnt / total >= 0.5:
            fig.add_annotation(
                x=0.5, y=0.985, xref="x", yref="paper",
                text=f"{top_cnt:,} of {total:,} active leads ride ONE edge "
                     f"({top_rule}) — the rest fire {total - top_cnt:,} combined",
                showarrow=False, font=dict(color="#f4a23a", size=12.5))
    fig.add_annotation(  # the backlog: where to aim next
        x=0.5, y=-0.06, xref="x", yref="paper", xanchor="center",
        text="<b>Detector backlog</b> — fat hard-ID edges with NO rule yet:  "
             "STEEL 37  ·  CCN~NPI 39  ·  NPI 21  ·  CIK 1",
        showarrow=False, font=dict(color="#8b949e", size=11.5))

    fig.update_layout(
        title=dict(
            text=f"Ripple — Active Leads  ·  {total:,} leads across {nrules} detectors",
            font=dict(color=FG, size=21), x=0.5, xanchor="center", y=0.965),
        paper_bgcolor=BG, plot_bgcolor=BG,
        xaxis=dict(visible=False, range=[-0.55, 1.65]),
        yaxis=dict(visible=False, range=[-0.05, 1.05]),
        legend=dict(font=dict(color=FG), bgcolor="rgba(0,0,0,0)",
                    x=0.5, xanchor="center", y=1.04, orientation="h"),
        hoverlabel=dict(bgcolor="#161b22", font=dict(color=FG, size=12)),
        margin=dict(l=40, r=40, t=110, b=70), height=640,
    )
    return fig


def render(open_browser: bool = False) -> Path:
    _load_graph_rows()
    counts, live = active_lead_counts()
    fig = build_figure(counts)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(OUT, include_plotlyjs="cdn", config={"displaylogo": False})
    size_mb = OUT.stat().st_size / 1e6
    src = "live" if live else "fallback"
    print(f"active lead counts ({src}): {counts}")
    print(f"wrote {OUT}  ({size_mb:.2f} MB)")
    if open_browser:
        try:
            import webbrowser
            webbrowser.open(OUT.resolve().as_uri())
        except Exception:
            print(f"open it manually: {OUT}")
    return OUT


if __name__ == "__main__":
    render()
