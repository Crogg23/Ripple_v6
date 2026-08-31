"""Guard tests for the canonical typing layer (2026-08-22 rollout).

The contract: every column the rulings file says is cast, and whose model
actually carries the ripple_num/ripple_dt macro, must (1) be a real numeric/
date type in the live mart and (2) for dates, hold no values outside the
1800-2100 range guard. A tag-vs-value contradiction fails loudly — the same
shape as the clock layer's guard.

Self-scoping: tables whose model file does not yet carry the macros are
skipped, so the suite stays green mid-rollout without a ledger.
"""
from __future__ import annotations

import csv
import re
from collections import defaultdict
from pathlib import Path

import pytest

pytestmark = pytest.mark.snowflake  # queries live marts via scripts/_snowflake_conn

_REPO = Path(__file__).resolve().parents[1]
RULINGS = _REPO / "reports" / "typing_index" / "typing_rulings.csv"
MODELS = _REPO / "library-onboarding" / "ripple_dbt" / "models" / "marts"

NUMERIC_TYPES = {"NUMBER", "FLOAT"}
DATE_TYPES = {"DATE", "TIMESTAMP_NTZ", "TIMESTAMP_TZ", "TIMESTAMP_LTZ"}


def _applied_tables():
    """(schema, table) -> {column: ruling} for models carrying the macros."""
    if not RULINGS.exists():
        return {}
    by_table = defaultdict(dict)
    for r in csv.DictReader(open(RULINGS, newline="", encoding="utf-8")):
        if r["ruling"] in ("cast_double", "cast_date",
                          "ambiguous_number", "ambiguous_date"):
            by_table[(r["schema"], r["table"])][r["column"]] = r["ruling"]
    applied = {}
    for (schema, table), cols in by_table.items():
        model = MODELS / schema.lower() / f"{table.lower()}.sql"
        if not model.exists():
            continue
        text = model.read_text(encoding="utf-8")
        live = {c: ru for c, ru in cols.items()
                if re.search(rf"ripple_(num|dt)\([^)]*\)\s*}}}}\s+as\s+{c}\b",
                             text, flags=re.IGNORECASE)}
        if live:
            applied[(schema, table)] = live
    return applied


APPLIED = _applied_tables()


@pytest.fixture(scope="module")
def cur():
    import sys
    sys.path.insert(0, str(_REPO))
    from scripts._snowflake_conn import connect
    return connect().cursor()


@pytest.mark.skipif(not APPLIED, reason="typing layer not applied to any model yet")
def test_ruled_columns_are_really_typed(cur):
    """Every macro-carrying ruled column must be a real type in the warehouse."""
    wrong = []
    for (schema, table), cols in sorted(APPLIED.items()):
        cur.execute(
            "select column_name, data_type from LIBRARY_MARTS.INFORMATION_SCHEMA.COLUMNS "
            f"where table_schema = '{schema}' and table_name = '{table}'")
        types = dict(cur.fetchall())
        for col, ruling in cols.items():
            want = NUMERIC_TYPES if "num" in ruling or ruling == "cast_double" else DATE_TYPES
            got = types.get(col)
            if got is None:
                wrong.append(f"{schema}.{table}.{col}: column missing from live mart")
            elif got not in want:
                wrong.append(f"{schema}.{table}.{col}: ruled {ruling} but live type is {got} "
                             "(model edited but mart not rebuilt, or the cast silently failed)")
    assert not wrong, "typing rulings and live warehouse disagree:\n  " + "\n  ".join(wrong)


@pytest.mark.skipif(not APPLIED, reason="typing layer not applied to any model yet")
def test_cast_dates_stay_inside_range_guard(cur):
    """No cast date column may hold values outside 1800-2100 (epoch/typo trap)."""
    bad = []
    for (schema, table), cols in sorted(APPLIED.items()):
        date_cols = [c for c, ru in cols.items() if ru in ("cast_date", "ambiguous_date")]
        if not date_cols:
            continue
        checks = ", ".join(
            f"count_if({c} < '1800-01-01' or {c} > '2100-01-01')" for c in date_cols)
        cur.execute(f"select {checks} from LIBRARY_MARTS.{schema}.{table}")
        for c, n in zip(date_cols, cur.fetchone()):
            if n:
                bad.append(f"{schema}.{table}.{c}: {n} rows outside 1800-2100")
    assert not bad, "range guard breached (epoch-trap class):\n  " + "\n  ".join(bad)
