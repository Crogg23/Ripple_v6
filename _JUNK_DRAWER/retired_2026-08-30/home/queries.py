"""Data layer for the one-door app - kept OUT of app.py so it is testable.

app.py is a rendering shell; every warehouse read lives here, and every read is
a plain SELECT through serve/'s read-only session. Nothing in this module can
write. Bound parameters everywhere - no f-string interpolation of user input.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
for _p in (_ROOT, _ROOT / "serve"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from serve_session import run_df  # noqa: E402

LEADS = '"LIBRARY_META"."CONNECT"."LEADS"'

# Plain-English names for the wired patterns. A rule with no entry still shows,
# under its raw name - never hide a finding just because nobody labelled it.
RULE_LABEL = {
    "debarred_but_funded": "Banned from federal contracts - still getting them",
    "banned_but_paid": "Banned from Medicare - still taking drug-company money",
    "excluded_but_billing": "Banned from Medicare - still appearing in billing data",
    "banned_but_operating": "Banned provider - still on an active facility roster",
    "sanctioned_vessel_broadcasting": "Sanctioned ship - still broadcasting its position",
    "sanctioned_vessel_broadcasting_v2": "Sanctioned ship - still broadcasting (wider net)",
    "sec_filer_in_irs_bmf": "Public-company filer also registered as a nonprofit",
    "osha_cohort_outlier_2024": "Workplace injury rates far above their industry peers",
}

# Only the LATEST run of each pattern is shown. The lead table keeps history, so
# a lead found by an older version of a rule and NOT re-found by the current one
# is still sitting there - showing it would inflate today's count with a hit the
# current rule no longer makes. (Seen live 2026-08-11: the debarment pattern read
# 344 in the table while the current rule finds 343.) History stays; the screen
# shows now.
_CURRENT = (f"SELECT * FROM {LEADS} "
            f"QUALIFY LAST_SEEN = MAX(LAST_SEEN) OVER (PARTITION BY RULE_NAME)")

RULE_COUNTS_SQL = (f"SELECT RULE_NAME, COUNT(*) AS N, MAX(LAST_SEEN) AS LAST_RUN "
                   f"FROM ({_CURRENT}) GROUP BY 1 ORDER BY 2 DESC")

LEADS_SQL = (f"SELECT TITLE, SCORE, EVIDENCE_COUNT, LEFT_KEY_TYPE, LEFT_KEY_VALUE, "
             f"LEFT_ENTITY_ID, RIGHT_ENTITY_ID, EVIDENCE, AS_OF_DATE, SQL_SHA256 "
             f"FROM ({_CURRENT}) WHERE RULE_NAME = %s "
             f"ORDER BY EVIDENCE_COUNT DESC NULLS LAST, SCORE DESC LIMIT %s")


def rule_counts():
    """One row per wired pattern: how many hits, when it was last computed."""
    return run_df(RULE_COUNTS_SQL)


def leads_for(rule: str, limit: int = 100):
    """The hits for one pattern, biggest first. `rule` and `limit` are BOUND."""
    return run_df(LEADS_SQL, (rule, int(limit)))


def evidence_bits(raw) -> str:
    """Evidence lands as a JSON blob; render it as plain 'key: value' text.

    Never raises: a lead with malformed evidence still has to display, because
    hiding the row would hide a real finding behind a formatting bug.
    """
    try:
        d = json.loads(raw) if isinstance(raw, str) else (raw or {})
    except Exception:
        return str(raw or "")
    if isinstance(d, dict):
        return " | ".join(f"{k}: {v}" for k, v in d.items() if v not in (None, "", []))
    if isinstance(d, list):
        return " | ".join(str(x) for x in d)
    return str(d)


def label_for(rule: str) -> str:
    return RULE_LABEL.get(rule, rule)
