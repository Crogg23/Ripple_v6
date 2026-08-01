"""Snapshot the warehouse inventory the Playground's packs reference.

READ-ONLY. Prints the JSON for tests/fixtures/playground_inventory.json —
committing the file is a human act (review the diff first). The offline pack
tests validate every pack FQN against this committed snapshot, so a typo'd
table name fails in CI instead of in Chris's browser.

Usage:
    python scripts/snapshot_playground_inventory.py > tests/fixtures/playground_inventory.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from dotenv import load_dotenv  # noqa: E402

# The read lane needs SNOWFLAKE_SERVE_PAT in the environment BEFORE sqlrun
# connects (repo rule: .env wins over stale shell env).
load_dotenv(REPO / "library-onboarding" / ".env", override=True)

from viz import sqlrun  # noqa: E402  (the verified read-only lane)


def main() -> int:
    fqns: set[str] = set()
    for sql in (
        """SELECT TABLE_CATALOG || '.' || TABLE_SCHEMA || '.' || TABLE_NAME AS F
           FROM LIBRARY_RAW.INFORMATION_SCHEMA.TABLES
           WHERE TABLE_SCHEMA = 'LANDING'""",
        """SELECT TABLE_CATALOG || '.' || TABLE_SCHEMA || '.' || TABLE_NAME AS F
           FROM LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES
           WHERE TABLE_SCHEMA <> 'INFORMATION_SCHEMA'""",
    ):
        df, _ = sqlrun.run(sql, limit_rows=20_000)
        fqns.update(str(v) for v in df.iloc[:, 0].dropna().tolist())
    out = {"note": "committed inventory snapshot for pack validation - "
                   "regenerate with scripts/snapshot_playground_inventory.py",
           "fqns": sorted(fqns)}
    print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
