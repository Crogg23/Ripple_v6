"""Saved cards — browse every chart card ever saved, read-only.

Cards are committed .py files under investigations/ (written by viz/card).
This room LISTS and SHOWS them; it never executes a card in-process — a card
is run from a terminal (`python <card>.py`), exactly as viz/README teaches.
"""
from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

INVESTIGATIONS = _ROOT / "investigations"


def _cards() -> list[Path]:
    if not INVESTIGATIONS.exists():
        return []
    return sorted(INVESTIGATIONS.glob("*/q*.py"),
                  key=lambda p: p.stat().st_mtime, reverse=True)


def render_cards():
    st.markdown("## 🗃 Saved cards")
    st.caption("Every chart you kept — committed, editable, re-runnable. "
               "Run one with `python <path>` in a terminal; it writes an "
               ".html next to itself.")
    cards = _cards()
    if not cards:
        st.info("No cards yet. Save one from the Ask room — the Code tab's "
                "'Save as card' button.")
        return
    by_inv: dict[str, list[Path]] = {}
    for p in cards:
        by_inv.setdefault(p.parent.name, []).append(p)
    for inv, paths in by_inv.items():
        with st.expander(f"**{inv}** — {len(paths)} card(s)",
                         expanded=len(by_inv) == 1):
            for p in paths:
                rel = p.relative_to(_ROOT)
                st.markdown(f"**{p.name}**  \n`{rel}`")
                html = p.with_suffix(".html")
                if html.exists():
                    st.caption(f"last rendered output: {html.name}")
                st.code(p.read_text(encoding="utf-8"), language="python")
                st.divider()
