"""Shared Plotly look for the tier-1 deep dive. One system, 21 stories.

Palette = the validated dataviz reference palette (light mode).
Usage:
    from _shared.viz import PAL, SEQ, base_fig, write_story
    fig = base_fig(title="...", subtitle="...")   # then add traces
    write_story(out_html, title, lede, sections=[(heading, prose, fig), ...], footer)
"""
from __future__ import annotations
import html
import plotly.graph_objects as go
import plotly.io as pio

# categorical, fixed slot order - never cycle, never reorder
PAL = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7", "#e34948"]
# sequential blue 100->700
SEQ = ["#cde2fb", "#b7d3f6", "#9ec5f4", "#86b6ef", "#6da7ec", "#5598e7", "#3987e5",
       "#2a78d6", "#256abf", "#1c5cab", "#184f95", "#104281", "#0d366b"]
DIV = ["#2a78d6", "#f0efec", "#e34948"]      # blue - gray - red
STATUS = {"good": "#008300", "warning": "#eda100", "serious": "#eb6834", "critical": "#e34948"}
SURFACE = "#fcfcfb"
TEXT = "#0b0b0b"
TEXT2 = "#52514e"
GRID = "#e6e5e1"

_template = go.layout.Template(
    layout=go.Layout(
        font=dict(family="-apple-system, Inter, Segoe UI, Helvetica, Arial, sans-serif", size=14, color=TEXT),
        paper_bgcolor=SURFACE, plot_bgcolor=SURFACE,
        colorway=PAL,
        margin=dict(l=70, r=30, t=90, b=60),
        title=dict(x=0, xanchor="left", font=dict(size=20)),
        xaxis=dict(showgrid=False, zeroline=False, linecolor=GRID, tickfont=dict(color=TEXT2)),
        yaxis=dict(gridcolor=GRID, zeroline=False, showline=False, tickfont=dict(color=TEXT2)),
        legend=dict(orientation="h", y=-0.18, x=0, bgcolor="rgba(0,0,0,0)"),
        hoverlabel=dict(bgcolor="#ffffff", font=dict(color=TEXT)),
        bargap=0.35,
    )
)
pio.templates["ripple"] = _template
pio.templates.default = "ripple"


def base_fig(title: str, subtitle: str | None = None, height: int = 480) -> go.Figure:
    fig = go.Figure()
    t = f"<b>{html.escape(title)}</b>"
    if subtitle:
        t += f"<br><span style='font-size:13px;color:{TEXT2}'>{html.escape(subtitle)}</span>"
    fig.update_layout(title=dict(text=t), height=height)
    return fig


def bar_style(fig: go.Figure) -> go.Figure:
    """Thin bars, no outline. Call after adding traces."""
    fig.update_traces(marker_line_width=0, selector=dict(type="bar"))
    return fig


_CSS = f"""
<style>
:root {{ --bg:{SURFACE}; --ink:{TEXT}; --ink2:{TEXT2}; --rule:{GRID}; --accent:{PAL[0]}; --hot:{PAL[7]}; }}
body {{ margin:0; background:var(--bg); color:var(--ink); font:16px/1.5 -apple-system, Inter, "Segoe UI", Helvetica, Arial, sans-serif; }}
main {{ max-width:1100px; margin:0 auto; padding:40px 24px 80px; }}
h1 {{ font-size:34px; line-height:1.15; margin:0 0 8px; }}
.lede {{ font-size:19px; color:var(--ink2); margin:0 0 36px; max-width:820px; }}
.hero {{ display:flex; gap:32px; flex-wrap:wrap; margin:0 0 36px; }}
.tile {{ border-top:3px solid var(--accent); padding:12px 0 0; min-width:180px; }}
.tile .n {{ font-size:40px; font-weight:700; line-height:1; }}
.tile .l {{ color:var(--ink2); font-size:14px; margin-top:6px; }}
section {{ display:grid; grid-template-columns: 300px 1fr; gap:28px; align-items:start; padding:28px 0; border-top:1px solid var(--rule); }}
section h2 {{ font-size:20px; margin:0 0 10px; }}
section p {{ margin:0 0 12px; color:var(--ink); }}
section .prose {{ font-size:15.5px; }}
.chart {{ min-width:0; overflow-x:auto; }}
footer {{ margin-top:40px; padding-top:20px; border-top:1px solid var(--rule); color:var(--ink2); font-size:13px; }}
footer code {{ font-size:12px; }}
@media (max-width:800px) {{ section {{ grid-template-columns:1fr; }} }}
</style>
"""


def write_story(out_path, title: str, lede: str, sections, footer: str = "", hero=None):
    """sections: list of (heading, prose_html, fig_or_None). hero: list of (number_str, label)."""
    parts = [f"<!doctype html><html><head><meta charset='utf-8'><title>{html.escape(title)}</title>{_CSS}</head><body><main>"]
    parts.append(f"<h1>{html.escape(title)}</h1><p class='lede'>{lede}</p>")
    if hero:
        parts.append("<div class='hero'>" + "".join(
            f"<div class='tile'><div class='n'>{html.escape(str(n))}</div><div class='l'>{html.escape(l)}</div></div>" for n, l in hero) + "</div>")
    first = True
    for heading, prose, fig in sections:
        chart = ""
        if fig is not None:
            chart = fig.to_html(full_html=False, True if first else False,
                                config=dict(displayModeBar=False, responsive=True))
            first = False
        parts.append(f"<section><div class='prose'><h2>{html.escape(heading)}</h2>{prose}</div><div class='chart'>{chart}</div></section>")
    parts.append(f"<footer>{footer}</footer></main></body></html>")
    with open(out_path, "w") as f:
        f.write("".join(parts))
    return out_path
