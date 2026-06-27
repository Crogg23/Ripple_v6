"""The active-leads board — basic, legible, and actually correct.

Earlier this tried to burn the 353 leads on top of the full 720-node connection
web. With every dataset drawn as a marker sized by row count, a 9.6M-row node is a
~56px bubble and the spring layout collapses into an unreadable blob that buries
every edge. So this is the BASIC version: draw only the seven landing tables the
four live detectors actually touch, on a fixed two-column layout, and let edge
thickness carry the one finding that matters.

LEFT column  = the "flag" registries (excluded / sanctioned / debarred).
RIGHT column = where those same entities turn up (paid / operating / sailing / funded).
Each detector is one edge, flag -> activity, joined on a hard ID (NPI / IMO / UEI).
Edge WIDTH = how many leads that rule is firing right now. The 338 banned_but_paid
edge dwarfs the rest on purpose: 338 of 353 leads ride that single NPI bridge.

Run:  python -m connect.leads_overlay
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import plotly.graph_objects as go

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "leads_overlay.html"
GRAPH = ROOT / "outputs" / "connect_graph.json"

# ---- the four detectors, from leads_specs.JOBS (rule -> tables + the hard key) ----
DETECTORS = [
    # rule,                            flag table,             activity table,                 key
    ("banned_but_paid",               "FED_HHS_OIG_LEIE",      "FED_CMS_OPEN_PAYMENTS",        "NPI"),
    ("banned_but_operating",          "FED_HHS_OIG_LEIE",      "FED_CMS_FACILITY_AFFILIATION", "NPI"),
    ("sanctioned_vessel_broadcasting","FED_OFAC_SDN",          "FED_NOAA_AIS",                 "IMO"),
    ("debarred_but_funded",           "FED_SAM_EXCLUSIONS",    "FED_USASPENDING_CONTRACTS",    "UEI"),
]

# friendly labels + fixed positions (x: 0 = flag column, 1 = activity column)
LABEL = {
    "FED_HHS_OIG_LEIE":            "OIG exclusions\n(LEIE)",
    "FED_OFAC_SDN":                "OFAC sanctions\n(SDN)",
    "FED_SAM_EXCLUSIONS":          "SAM debarments",
    "FED_CMS_OPEN_PAYMENTS":       "CMS Open Payments",
    "FED_CMS_FACILITY_AFFILIATION":"CMS facility roster",
    "FED_NOAA_AIS":                "NOAA AIS\n(ship tracks)",
    "FED_USASPENDING_CONTRACTS":   "USASpending\ncontracts",
}
POS = {
    "FED_HHS_OIG_LEIE":            (0.0, 0.80),
    "FED_OFAC_SDN":                (0.0, 0.45),
    "FED_SAM_EXCLUSIONS":          (0.0, 0.12),
    "FED_CMS_OPEN_PAYMENTS":       (1.0, 0.88),
    "FED_CMS_FACILITY_AFFILIATION":(1.0, 0.60),
    "FED_NOAA_AIS":                (1.0, 0.34),
    "FED_USASPENDING_CONTRACTS":   (1.0, 0.10),
}
FLAGS = {"FED_HHS_OIG_LEIE", "FED_OFAC_SDN", "FED_SAM_EXCLUSIONS"}

KEY_COLOR = {"NPI": "#f4a23a", "IMO": "#3ab0c4", "UEI": "#b07cf0"}

# verified row counts (live snapshot 2026-06-27); overridden from connect_graph.json
# where the node id matches, falling back to these so the board always renders.
ROWS = {
    "FED_HHS_OIG_LEIE": 83464, "FED_OFAC_SDN": 19115, "FED_SAM_EXCLUSIONS": 1000,
    "FED_CMS_OPEN_PAYMENTS": 15385047, "FED_CMS_FACILITY_AFFILIATION": 2239952,
    "FED_NOAA_AIS": 7296275, "FED_USASPENDING_CONTRACTS": 6325622,
}

# fallback lead counts if the warehouse is unreachable (verified 2026-06-27)
FALLBACK_COUNTS = {
    "banned_but_paid": 338, "banned_but_operating": 11,
    "sanctioned_vessel_broadcasting": 2, "debarred_but_funded": 2,
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


def _rows(tid: str) -> int:
    return ROWS.get(tid, 0)


def _load_graph_rows() -> None:
    """Best-effort: refresh ROWS from the cached graph so counts stay live."""
    try:
        g = json.loads(GRAPH.read_text())
        by_id = {n["id"]: n for n in g.get("nodes", [])}
        for tid in ROWS:
            if tid in by_id and by_id[tid].get("rows"):
                ROWS[tid] = int(by_id[tid]["rows"])
    except Exception:
        pass


def _ewidth(cnt: int) -> float:
    return 2.5 + 5.0 * math.log10(max(cnt, 1))


def build_figure(counts: dict[str, int]) -> go.Figure:
    fig = go.Figure()

    # --- detector edges (flag -> activity), width by lead count, color by key ----
    for rule, lt, rt, key in DETECTORS:
        cnt = counts.get(rule, 0)
        if cnt <= 0:
            continue
        (x0, y0), (x1, y1) = POS[lt], POS[rt]
        fig.add_trace(go.Scatter(
            x=[x0, x1], y=[y0, y1], mode="lines",
            line=dict(color=KEY_COLOR.get(key, "#f4a23a"), width=_ewidth(cnt)),
            opacity=0.85, hoverinfo="text",
            hovertext=f"<b>{rule}</b><br>{cnt:,} active leads<br>"
                      f"{LABEL[lt].replace(chr(10),' ')} ↔ {LABEL[rt].replace(chr(10),' ')}<br>"
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
        ids = [t for t in POS if (t in FLAGS) == (group == "flag")]
        fig.add_trace(go.Scatter(
            x=[POS[t][0] for t in ids], y=[POS[t][1] for t in ids],
            mode="markers+text",
            text=[f"<b>{LABEL[t].splitlines()[0]}</b>"
                  + (f"<br>{LABEL[t].splitlines()[1]}" if "\n" in LABEL[t] else "")
                  + f"<br><span style='color:#8b949e'>{_rows(t):,} rows</span>"
                  for t in ids],
            textposition=tpos, textfont=dict(color=FG, size=12),
            marker=dict(size=22, color=BG, line=dict(color=ring, width=3),
                        symbol="circle"),
            hoverinfo="text",
            hovertext=[f"<b>{t}</b><br>{_rows(t):,} rows" for t in ids],
            showlegend=False,
        ))

    # --- a tiny legend for the three bridging keys -------------------------------
    for key, color in KEY_COLOR.items():
        fig.add_trace(go.Scatter(
            x=[None], y=[None], mode="lines",
            line=dict(color=color, width=6), name=f"{key} bridge",
        ))

    # --- callouts ---------------------------------------------------------------
    fig.add_annotation(  # the concentration finding
        x=0.5, y=0.985, xref="x", yref="paper",
        text="338 of 353 leads ride ONE edge — every other detector is firing 2–11",
        showarrow=False, font=dict(color="#f4a23a", size=12.5))
    fig.add_annotation(  # AIS island note, parked in the gap below AIS / above USASpending
        x=1.04, y=0.23, xref="x", yref="y", xanchor="left", yanchor="middle",
        text="⚠ NOAA AIS is an island in the 720-node graph<br>"
             "(the IMO bridge to OFAC was never built)",
        showarrow=False, font=dict(color="#3ab0c4", size=10), align="left")
    fig.add_annotation(  # the backlog: where to aim next
        x=0.5, y=-0.06, xref="x", yref="paper", xanchor="center",
        text="<b>Detector backlog</b> — fat hard-ID edges with NO rule yet:  "
             "STEEL 37  ·  CCN~NPI 39  ·  NPI 21  ·  CIK 1",
        showarrow=False, font=dict(color="#8b949e", size=11.5))

    total = sum(c for c in counts.values() if c > 0)
    nrules = sum(1 for c in counts.values() if c > 0)
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
