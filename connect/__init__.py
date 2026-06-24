"""Ripple CONNECT — the exploratory connection engine.

Turns the Library's pile of landed tables into a graph of REAL connections:
which datasets actually share values on a join key (not just a key *type*),
how strongly, and a sample you can eyeball. Then renders it as an interactive
map you can wander.

Modules
-------
  db          short-lived Snowflake connection (reuses library-onboarding/snow.py)
  keys        key detection (reuses portal_recon tagger) + value normalizers
  fingerprint per-table: which keys does it carry, and are they really populated?
  overlap     the engine: do two columns actually share values, and how many?
  discover    compute the real edge-list across all landed sources
  explore     render the interactive Plotly connection explorer

Run:  python -m connect all        # fingerprint -> discover -> explore
"""

# Windows consoles default to cp1252 and choke on box-drawing / check marks in
# our progress output. Force UTF-8 (replace, never crash on an unprintable char).
import sys as _sys
for _s in (_sys.stdout, _sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
