"""Ripple — The Playground. Question-driven exploration, Chris driving.

Two rooms:
  ASK          pick a plain-English question -> the tailored dictionary of
               tables, columns, joins, and traps in its realm -> write your
               own SQL -> chart it with editable Plotly -> save the card.
  SAVED CARDS  every chart kept so far, read-only, re-runnable.

All heavy machinery is the shared viz/ layer (read-only lane, SQL guard,
fact-vs-lead badges, chart plugs, cards) — this app is a shell. No AI at
runtime, no SQL generation, nothing here can write to the warehouse.
"""
from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from dotenv import load_dotenv  # noqa: E402

# The read lane needs SNOWFLAKE_SERVE_PAT in the environment BEFORE sqlrun
# connects (repo rule: .env wins over stale shell env).
load_dotenv(_ROOT / "library-onboarding" / ".env", override=True)

from playground import ask, cards_browser  # noqa: E402

st.set_page_config(page_title="Ripple — The Playground", page_icon="🧭",
                   layout="wide")

st.title("The Playground")
st.caption("you write the SQL and build the charts — the platform hands you "
           "the map: which tables, which columns, how they join, and where "
           "the traps are")

with st.sidebar:
    room = st.radio("Room", ["Ask", "Saved cards"], key="pg_room")

if room == "Saved cards":
    cards_browser.render_cards()
else:
    ask.render_ask()
