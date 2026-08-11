"""Every embedded copy of the key normalizer must match connect/keys.py exactly.

The staging models carry a GENERATED copy of normalize_sql inside their
`spine_entity_id` expression (scripts/generate_staging_models.py) so a mart can
join the who's-who without calling Python. On 2026-08-11 that copy was found
drifted in 53 files: it predated the 2026-07-28 digits-only guard, so a text
sentinel padded into a plausible 9-character value and hashed to an entity id
the spine had correctly refused to create -- a join to nothing, forever.

cohort_queue.sql has had this guard since audit F6; this extends it to every
generated copy, so ONE parity test now covers all of them.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from connect.keys import normalize_sql

MODELS = Path(__file__).resolve().parents[1] / "library-onboarding" / "ripple_dbt" / "models"
LINE = re.compile(
    r"^(\s*)'ENT_' \|\| LEFT\(MD5\('([A-Z_]+)' \|\| '\|' \|\| \((.*)\)\), 16\) as spine_entity_id")


def _embedded():
    for f in sorted(MODELS.rglob("*.sql")):
        for n, line in enumerate(f.read_text(encoding="utf-8").split("\n"), 1):
            m = LINE.match(line)
            if m:
                yield f, n, m.group(2), m.group(3)


def test_there_are_embedded_copies_to_check():
    assert sum(1 for _ in _embedded()) > 40, "the parity check found nothing to check"


@pytest.mark.parametrize("path,lineno,key,expr",
                         [(str(f), n, k, e) for f, n, k, e in _embedded()])
def test_embedded_spine_id_normalizer_is_verbatim_keys_py(path, lineno, key, expr):
    col = re.search(r"TO_VARCHAR\((.*?)\), ", expr).group(1)
    assert expr == normalize_sql(key, col), (
        f"{Path(path).name}:{lineno} embeds a {key} normalizer that has drifted from "
        f"connect/keys.py. Rows would resolve to entity ids the spine never created. "
        f"Regenerate with scripts/generate_staging_models.py -- never hand-edit.")
