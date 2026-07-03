"""viz/ — the Investigator Instrument's core: plug-and-play, code-visible Plotly.

Modules (import them directly; this __init__ stays EMPTY on purpose so that
`import viz` never drags in plotly, pandas, or a Snowflake connection):

    viz.theme    — the one house Plotly template (ripple_dark) + validated palette
    viz.plugs    — the plug library: plug(df, ...) -> real, editable Plotly figure
    viz.guard    — pure SQL statement guard (allowlist + token denylist)
    viz.sqlrun   — the guarded read lane to Snowflake (the ONE chokepoint)
    viz.catalog  — live table/column discovery off CATALOG + INFORMATION_SCHEMA
    viz.safety   — facts-vs-leads classification + chart badges
    viz.card     — chart cards: standalone runnable .py per question + eject

Dependency rule (keep it one-way): viz may import connect.keys (a leaf) and
library-onboarding/snow.py; nothing in connect/ or serve/ may import anything
from viz except viz.theme.
"""
