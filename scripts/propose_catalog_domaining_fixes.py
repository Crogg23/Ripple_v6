#!/usr/bin/env python3
"""Preview (and optionally apply) DOMAIN_PRIMARY fixes for mis-filed catalog rows.

Addresses the 2026-06-26 audit "jump-out #4": a few SOURCE_REGISTRY rows sit under
the wrong DOMAIN_PRIMARY, so they hide from domain-scoped browsing (e.g.
xc_propublica_nonprofit filed under history_culture instead of corporate_entities).

Design mirrors scripts/propose_catalog_hygiene_fixes.py: **preview by default,
rollback-snapshotted, idempotent, --apply gated.** The auto-mode classifier blocks
the agent from writing the catalog directly, so this is handed to Chris to run with
--apply (or to eyeball and reject).

    python scripts/propose_catalog_domaining_fixes.py            # preview only
    python scripts/propose_catalog_domaining_fixes.py --apply    # Chris runs this

Each RULE is a (regex over source_id+name, current_domain_predicate, ->target_domain,
why). Rules are HIGH-PRECISION on purpose — we only move a row when the keyword leaves
no doubt. Anything ambiguous is left for a human topic call (V_REVIEW_QUEUE), not moved.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
_LIB = _REPO / "library-onboarding"
if str(_LIB) not in sys.path:
    sys.path.insert(0, str(_LIB))

# Load library-onboarding/.env explicitly (cwd-independent — the bug that bit the
# 2026-06-26 session: running from repo root left config with stale OS creds).
try:
    from dotenv import load_dotenv

    load_dotenv(_LIB / ".env", override=True)
except Exception:  # pragma: no cover
    pass

import snow  # noqa: E402

CATALOG = "LIBRARY_META.REGISTRY.SOURCE_REGISTRY"  # write the base table, not the view
BACKUP = "LIBRARY_META.REGISTRY._SOURCE_REGISTRY_BAK_DOMAINING_20260626"

# (rule_id, name_regex, NOT-already-this-domain, -> target_domain, why)
RULES = [
    (
        "nonprofit_to_corporate",
        r".*(nonprofit|irs[_ ]?990|eo[_ ]?bmf|exempt[_ ]?org|charit).*",
        "corporate_entities",
        "corporate_entities",
        "Nonprofit/990/exempt-org sources belong with the EIN corporate backbone, not history/other.",
    ),
    (
        "ofac_debar_to_sanctions",
        r".*(ofac[_ ]?sdn|denied[_ ]?person|debarred[_ ]?list|consolidated[_ ]?screen).*",
        "sanctions_enforcement",
        "sanctions_enforcement",
        "OFAC/denied-person/debarment lists are the sanctions_enforcement spine.",
    ),
]


def _conn():
    return snow.connect()


def preview(conn) -> list[dict]:
    cur = conn.cursor()
    proposals = []
    for rid, rx, not_dom, target, why in RULES:
        cur.execute(
            f"""SELECT source_id, domain_primary, name
                FROM {CATALOG}
                WHERE REGEXP_LIKE(LOWER(source_id || ' ' || COALESCE(name,'')), %s)
                  AND COALESCE(domain_primary,'') <> %s
                ORDER BY source_id""",
            (rx, not_dom),
        )
        for sid, cur_dom, name in cur.fetchall():
            proposals.append(
                {"rule": rid, "source_id": sid, "from": cur_dom or "(null)",
                 "to": target, "name": (name or "")[:60], "why": why}
            )
    return proposals


def apply(conn, proposals: list[dict]) -> None:
    cur = conn.cursor()
    # rollback snapshot first (idempotent: replace)
    cur.execute(f"CREATE OR REPLACE TABLE {BACKUP} AS SELECT * FROM {CATALOG}")
    print(f"  rollback snapshot -> {BACKUP}")
    for p in proposals:
        cur.execute(
            f"""UPDATE {CATALOG}
                SET domain_primary = %s, domain_source = 'audit_2026-06-26',
                    domain_confidence = 'high'
                WHERE source_id = %s""",
            (p["to"], p["source_id"]),
        )
    print(f"  applied {len(proposals)} domain fixes.")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Preview/apply catalog DOMAIN_PRIMARY fixes")
    ap.add_argument("--apply", action="store_true", help="write the fixes (default previews)")
    args = ap.parse_args(argv)

    conn = _conn()
    try:
        proposals = preview(conn)
        if not proposals:
            print("No mis-domained rows matched the high-precision rules. Catalog is clean.")
            return 0
        print(f"{len(proposals)} proposed domain fix(es):\n")
        for p in proposals:
            print(f"  [{p['rule']}] {p['source_id']:32s} {p['from']:18s} -> {p['to']}")
            print(f"      {p['name']}")
        if not args.apply:
            print("\nPREVIEW only. Re-run with --apply to write (snapshots first; rollback via "
                  f"{BACKUP}).")
            return 0
        apply(conn, proposals)
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    sys.exit(main())
