"""macros/staging_casts.sql and scripts/check_staging_casts.py must emit the same SQL.

The script's cast_sql() is a hand copy of the dbt macros, so the live check
would silently drift the day one side changes. This renders each macro with
jinja2 and compares it, whitespace-blind, to the script's string.
"""
import re
import sys
from pathlib import Path

import jinja2
import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import check_staging_casts as script  # noqa: E402

MACROS = jinja2.Template((REPO / "library-onboarding/ripple_dbt/macros/staging_casts.sql").read_text(encoding="utf-8")).module
COL = '"SOME_COL"'


def squash(sql: str) -> str:
    return re.sub(r"\s+", "", sql)


CASES = [
    ("stg_int", None, lambda: MACROS.stg_int(COL)),
    ("stg_float", None, lambda: MACROS.stg_float(COL)),
    ("stg_date", None, lambda: MACROS.stg_date(COL)),
    ("stg_date", "MMDDYYYY", lambda: MACROS.stg_date(COL, "MMDDYYYY")),
    ("stg_ts", None, lambda: MACROS.stg_ts(COL)),
    ("stg_bool", None, lambda: MACROS.stg_bool(COL)),
    ("stg_ts_tz", None, lambda: MACROS.stg_ts_tz(COL)),
    ("stg_id_text", None, lambda: MACROS.stg_id_text(COL)),
]
MACRO_FILE = REPO / "library-onboarding/ripple_dbt/macros/staging_casts.sql"


def test_every_public_macro_is_covered():
    """A cast macro added to the file without a case here is the drift this test exists to catch."""
    public = set(re.findall(r"\{%\s*macro\s+(stg_\w+)\(", MACRO_FILE.read_text(encoding="utf-8")))
    assert public == {m for m, _, _ in CASES}


def test_unknown_macro_is_an_error_not_a_boolean():
    with pytest.raises(ValueError):
        script.cast_sql("stg_made_up", COL, None)


@pytest.mark.parametrize("macro,fmt,render", CASES, ids=[f"{m}{'-' + f if f else ''}" for m, f, _ in CASES])
def test_macro_matches_script(macro, fmt, render):
    assert squash(render()) == squash(script.cast_sql(macro, COL, fmt))
