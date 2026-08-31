"""ALL SQL for the Playground's own reads (the user's ad-hoc SQL goes
through viz/sqlrun untouched). Parameterized — user/pack values are BOUND,
never interpolated. FQNs from packs are validated through viz/guard before
they touch SQL text (they are repo-authored constants, but the guard is
cheap and the habit is the point).
"""
from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from viz import guard  # noqa: E402

COLUMN_CATALOG = "LIBRARY_META.REGISTRY.COLUMN_CATALOG"


def column_catalog_sql(fqns: list[str]) -> str:
    """COLUMN_CATALOG rows for a pack's tables. The read lane (viz/sqlrun)
    takes no bind parameters, so every FQN is passed through
    viz/guard.validate_fqn FIRST — it raises on anything that isn't a clean
    2-3 part identifier — and only then placed in SQL text as a quoted
    string literal. A hostile string cannot survive the guard."""
    safe = [guard.validate_fqn(f) for f in fqns]
    in_list = ", ".join("'" + s.replace("'", "") + "'" for s in safe)
    return (f"SELECT FQN, COLUMN_NAME, ORDINAL, SF_TYPE, CHART_ROLE, "
            f"DIGIT_DATE, NONNULL_PCT, DISTINCT_SAMPLED, DETECTED_KEY, "
            f"KEY_TIER, KEY_POPULATED_PCT, PLAIN_GLOSS, GLOSS_SOURCE, "
            f"SAMPLE_VALUES, PROFILED_AT "
            f"FROM {COLUMN_CATALOG} WHERE FQN IN ({in_list}) "
            f"ORDER BY FQN, ORDINAL")


def live_count_sql(fqn: str) -> str:
    """COUNT(*) for one pack table. The FQN is a repo-authored constant,
    validated by viz/guard (raises on anything that isn't a clean
    identifier) before being placed in SQL text — identifiers cannot be
    bound as parameters in SQL."""
    safe = guard.validate_fqn(fqn)
    return f"SELECT COUNT(*) AS N FROM {safe}"
