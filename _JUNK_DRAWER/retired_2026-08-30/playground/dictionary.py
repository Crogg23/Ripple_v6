"""Dictionary-panel assembly — PURE functions (no streamlit, no snowflake,
no SQL execution). Takes a pack + COLUMN_CATALOG rows + live counts and
returns display-ready structures. Offline-testable by construction.
"""
from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import glossary  # noqa: E402
from honesty.traps import TRAPS  # noqa: E402
from playground.packs import PACK_TRAPS  # noqa: E402

TIER_BADGE = {
    "STEEL": "🔩 STEEL",
    "STRONG": "💪 STRONG",
    "PROBABILISTIC": "🎲 NAME-MATCH",
    "GEO": "📍 GEO",
}


def trap_text(key: str) -> str:
    """Resolve a trap key against the honesty registry first, then the
    pack-local politics traps. Unknown keys return a loud placeholder rather
    than nothing (a silent missing caveat is worse than an ugly one)."""
    return TRAPS.get(key) or PACK_TRAPS.get(key) or f"[unknown trap key: {key}]"


def short_name(fqn: str) -> str:
    return fqn.rsplit(".", 1)[-1]


def join_line(join: dict) -> str:
    """One join, in plain English with its strength badge and gotcha."""
    badge = TIER_BADGE.get(join.get("tier", ""), join.get("tier", ""))
    line = f"joins to **{short_name(join['to'])}** on `{join['on']}` ({badge})"
    if join.get("gotcha"):
        line += f" — {join['gotcha']}"
    return line


def key_gloss(column: str) -> str | None:
    """A one-line meaning for a key column, if the glossary knows it."""
    return glossary.gloss(column)


def table_panel(table: dict, catalog_rows: list[dict],
                live_count) -> dict:
    """Assemble one table's dictionary card.

    catalog_rows: COLUMN_CATALOG rows for this fqn (possibly empty),
    live_count: row count or None. Returns a dict the UI renders directly."""
    cols = []
    for r in sorted(catalog_rows, key=lambda r: (r.get("ordinal") or 0)):
        cols.append({
            "column": r.get("column_name"),
            "meaning": r.get("plain_gloss") or "",
            "kind": r.get("chart_role") or (r.get("sf_type") or "").lower(),
            "filled": (f"{r['nonnull_pct']:.0f}%"
                       if r.get("nonnull_pct") is not None else "—"),
            "key": (TIER_BADGE.get(r["key_tier"], r["key_tier"])
                    if r.get("detected_key") else ""),
            "samples": ", ".join(str(s) for s in (r.get("sample_values") or [])[:3]),
        })
    return {
        "fqn": table["fqn"],
        "name": short_name(table["fqn"]),
        "role": table["role"],
        "live_count": live_count,
        "key_columns": [
            {"column": k, "meaning": key_gloss(k) or ""}
            for k in table.get("key_columns", [])],
        "joins": [join_line(j) for j in table.get("joins", [])],
        "traps": [trap_text(k) for k in table.get("traps", [])],
        "columns": cols,
        "profiled_at": max((str(r.get("profiled_at")) for r in catalog_rows
                            if r.get("profiled_at")), default=None),
    }


def pack_panels(pack: dict, catalog_by_fqn: dict[str, list[dict]],
                counts_by_fqn: dict[str, int | None]) -> list[dict]:
    return [table_panel(t, catalog_by_fqn.get(t["fqn"], []),
                        counts_by_fqn.get(t["fqn"]))
            for t in pack.get("tables", [])]


def mentions_restricted(sql: str) -> bool:
    """True when the query touches the journalism-use-only trades table —
    the UI shows the legal banner whenever this fires."""
    return "FED_SENATE_STOCK_WATCHER" in (sql or "").upper()
