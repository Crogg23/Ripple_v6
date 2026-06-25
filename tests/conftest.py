"""Pytest bootstrap — the repo's first automated tests.

Most tests are OFFLINE (no Snowflake): they assert the SQL the engine GENERATES and
pure-Python logic. Tests marked `@pytest.mark.snowflake` need a live connection
(PAT in library-onboarding/.env) and self-skip if it can't be opened.
"""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
for p in (ROOT, ROOT / "library-onboarding"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "snowflake: requires a live Snowflake connection (PAT in .env)")


@pytest.fixture(scope="session")
def sf():
    from connect import db
    try:
        conn = db.connect()
    except Exception as e:  # noqa: BLE001 - any connect failure -> skip, don't fail
        pytest.skip(f"no Snowflake connection: {e}")
    yield conn
    conn.close()
