"""Static conformance fence over the loader fleet (no network, no Snowflake, no DB).

The loading invariants (never register an empty load, chunked writes are atomic via
staging, failed runs leave a trace, provenance is TIMESTAMP-typed) are only as strong
as whichever loader a source happened to arrive through. This file reads the loader
SOURCES and pins the fixed sites so a refactor can't silently regress them.
Cheap and specific — a regression fence, not a framework.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
for _p in (SCRIPTS, ROOT / "library-onboarding", ROOT):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))


def _src(name: str) -> str:
    return (SCRIPTS / name).read_text(encoding="utf-8")


# --------------------------------------------------------------------------- #
# (a) register-on-empty refusal at the three fixed sites
# --------------------------------------------------------------------------- #
def test_issue_batch_load_refuses_register_on_empty():
    src = _src("issue_batch_load.py")
    # verdict comes from assess_density, not a re-derived threshold
    assert 'if dens["empty"]:' in src
    assert ">= 0.01" not in src
    # the empty branch RETURNS (refusing registration) before _register is reached
    gate = src.index('if dens["empty"]:')
    assert src.index("return False", gate) < src.index("_register(conn", gate)


def test_issue_batch_load2_refuses_register_on_empty():
    src = _src("issue_batch_load2.py")
    assert 'if dens["empty"]:' in src
    assert ">= 0.01" not in src
    gate = src.index('if dens["empty"]:')
    assert src.index("return False", gate) < src.index("_register(conn", gate)


def test_bridge_fuel_chunked_refuses_register_on_empty():
    src = _src("bridge_fuel_load.py")
    chunked = src[src.index("def _load_chunked("):]
    gate = chunked.index('if density["empty"]:')
    assert chunked.index("return", gate) < chunked.index("_register(conn", gate)


# --------------------------------------------------------------------------- #
# (b) bridge_fuel chunked atomicity is pinned to the staging swap
# --------------------------------------------------------------------------- #
def test_bridge_fuel_chunked_lands_via_staging():
    src = _src("bridge_fuel_load.py")
    chunked = src[src.index("def _load_chunked("):]
    assert "atomic_load.staging_name(" in chunked      # staging name comes from loadkit
    assert "table_name=stg" in chunked                 # chunks write to STAGING, never live
    assert "atomic_load.execute_swap(" in chunked      # promotion is the atomic swap


def test_bridge_fuel_crash_handler_drops_staging_never_live():
    src = _src("bridge_fuel_load.py")
    chunked = src[src.index("def _load_chunked("):]
    # every DROP in the chunked path targets the staging table
    drops = re.findall(r"DROP TABLE IF EXISTS[^']*", chunked)
    assert drops, "expected staging DROPs in the chunked path"
    assert all('"{stg}"' in d for d in drops)
    assert not any('"{table}"' in d for d in drops)    # the old catastrophic live-drop


def test_bridge_fuel_success_logged_only_after_swap():
    src = _src("bridge_fuel_load.py")
    chunked = src[src.index("def _load_chunked("):]
    assert chunked.index("atomic_load.execute_swap(") < chunked.index('"success"')


def test_bridge_fuel_register_guard_precedes_merge():
    # _register must check for an existing registry row BEFORE building the MERGE —
    # re-registering clobbers curated facets with non-null defaults.
    src = _src("bridge_fuel_load.py")
    body = src[src.index("def _register("):]
    assert body.index("_registry_has_row(") < body.index("cfg = {")


def test_bridge_fuel_outer_catch_logs_failed():
    # download/zip-member/parse failures before any landing write must leave a trace
    src = _src("bridge_fuel_load.py")
    assert "Load failed before landing" in src


# --------------------------------------------------------------------------- #
# (c) fec_itcont: failed-run trace + smoke never swaps
# --------------------------------------------------------------------------- #
def test_fec_itcont_has_failed_handler():
    src = _src("fec_itcont_load.py")
    handler = src[src.index("except Exception"):]
    assert '"failed"' in handler
    assert "raise" in handler                          # logging must not swallow the error


def test_fec_itcont_smoke_returns_before_swap():
    src = _src("fec_itcont_load.py")
    assert '"smoke"' in src
    # the smoke log/return sits BEFORE the swap call in main()
    assert src.index('"smoke"') < src.index("atomic_load.execute_swap(")


# --------------------------------------------------------------------------- #
# (d) fixed backfills stamp TIMESTAMP-style _INGESTED_AT (no epoch-int drift)
# --------------------------------------------------------------------------- #
def test_federal_register_backfill_stamps_timestamp():
    src = _src("federal_register_backfill.py")
    assert "int(started.timestamp()" not in src        # the epoch-micros INTEGER drift
    assert "df[ingest.META_INGESTED_AT] = started.replace(tzinfo=None)" in src


def test_noaa_storm_events_backfill_stamps_timestamp():
    src = _src("noaa_storm_events_backfill.py")
    assert 'META_INGESTED_AT = "_INGESTED_AT"' in src  # underscore prefix restored
    assert "int(started.timestamp()" not in src
    assert "started.replace(tzinfo=None)" in src


# --------------------------------------------------------------------------- #
# supporting fences
# --------------------------------------------------------------------------- #
def test_atomic_load_exists_check_is_database_qualified():
    src = (ROOT / "loadkit" / "atomic_load.py").read_text(encoding="utf-8")
    # unqualified INFORMATION_SCHEMA resolves against the SESSION database — it only
    # worked because the session default happened to be LIBRARY_RAW
    assert '"{database}".INFORMATION_SCHEMA.TABLES' in src


def test_grant_script_does_nothing_at_import_time():
    src = _src("grant_mcp_readonly_catalog.py")
    assert 'if __name__ == "__main__":' in src
    pre_main = src[:src.index("def main(")]
    assert "connect()" not in pre_main                 # no import-time GRANTs


def test_hygiene_rollback_filename_is_timestamped():
    src = _src("propose_catalog_hygiene_fixes.py")
    assert "_rollback_CATALOG_view_" in src
    assert "%Y%m%d_%H%M%S" in src                      # second apply can't clobber the first


def test_nppes_spec_is_wellformed():
    import bridge_fuel_specs as bfs
    specs = {d["source_id"]: d for d in bfs.SPECS}
    assert "fed_cms_nppes" in specs
    s = specs["fed_cms_nppes"]
    assert s["kind"] == "zip_csv" and s["chunked"] and s["chunk_rows"] == 50_000
    # NO aliasing: the 333 landed column names are the dbt/connect contract
    assert "key_cols" not in s
    # the member regex picks the data file and rejects its zip siblings
    rx = re.compile(s["member"], re.I)
    assert rx.search("npidata_pfile_20050523-20260607.csv")
    assert not rx.search("npidata_pfile_20050523-20260607_fileheader.csv")
    assert not rx.search("othername_pfile_20050523-20260607.csv")
    assert not rx.search("endpoint_pfile_20050523-20260607.csv")
    assert not rx.search("pl_pfile_20050523-20260607.csv")
