"""Guards for the exact-duplicate landing repair tool (defect class: runaway
pager, 2026-08-11 verification). The tool must (1) exclude metadata columns
from row identity, (2) keep the earliest ingest per distinct data row, and
(3) never destroy the inflated rows outright (swap-and-rename, no DROP)."""
import importlib.util
import os

_PATH = os.path.join(os.path.dirname(__file__), "..", "scripts", "dedupe_landing_exact.py")
_spec = importlib.util.spec_from_file_location("dedupe_landing_exact", _PATH)
mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mod)


def test_meta_columns_excluded_from_identity():
    assert {"_INGESTED_AT", "_SOURCE_RUN_ID", "_SRC_SHA256"} == mod.META_COLS


def test_dedupe_sql_shape():
    stmts = mod.dedupe_sql("FED_FHFA_NMDB", ["GEO_TYPE", "GEO_CODE"])
    assert len(stmts) == 3
    create, swap, rename = stmts
    # identity = data columns only, earliest ingest wins
    assert 'PARTITION BY "GEO_TYPE", "GEO_CODE"' in create
    assert "ORDER BY _INGESTED_AT" in create
    assert "= 1" in create
    # atomic swap, and the inflated rows survive under __PREDEDUP
    assert "SWAP WITH" in swap
    assert "RENAME TO" in rename and "__PREDEDUP" in rename
    # nothing in the plan destroys data
    joined = " ".join(stmts).upper()
    for banned in ("DROP ", "DELETE ", "TRUNCATE ", "OR REPLACE"):
        assert banned not in joined


def test_meta_cols_never_in_partition():
    stmts = mod.dedupe_sql("T", ["A", "B"])
    assert "_SOURCE_RUN_ID" not in stmts[0].split("PARTITION BY")[1].split("ORDER BY")[0]
