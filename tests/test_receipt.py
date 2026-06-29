"""Receipt tests — the run-it-yourself proof must be frozen, reproducible, and complete.

All offline (no warehouse): the load-bearing trust properties live in PURE code —
the frozen clock in compile_sql, the SQL hash, the source-table set, the receipt assembly.
"""

import json

from connect import leads, receipt
from connect.leads_specs import JOBS

_SPEC = JOBS["banned_but_operating"]      # has a recency window -> exercises the clock freeze
_FLAGSHIP = JOBS["banned_but_paid"]       # right side lives in LIBRARY_STAGING (the grant gap)


# ---- the frozen clock: as_of replaces CURRENT_DATE, making the SQL reproducible ----

def test_as_of_freezes_the_clock():
    sql = leads.compile_sql(_SPEC, as_of="2026-06-28")
    assert "DATE '2026-06-28'" in sql
    assert "CURRENT_DATE" not in sql            # the drift source is gone


def test_no_as_of_keeps_legacy_current_date():
    """Ad-hoc preview (no as_of) is unchanged — only persisted runs freeze the clock."""
    sql = leads.compile_sql(_SPEC)
    assert "CURRENT_DATE" in sql


def test_as_of_must_be_iso():
    for bad in ("2026/06/28", "June 28", "2026-6-8", "'; DROP TABLE", "26-06-28"):
        try:
            leads.compile_sql(_SPEC, as_of=bad)
            assert False, f"accepted bad as_of {bad!r}"
        except ValueError:
            pass


def test_compile_is_deterministic_given_as_of():
    a = leads.compile_sql(_SPEC, as_of="2026-06-28")
    b = leads.compile_sql(_SPEC, as_of="2026-06-28")
    assert a == b                                # byte-identical -> same SHA, same lead, forever


# ---- the SQL hash: the artifact's identity ----

def test_sql_sha256_stable_and_sensitive():
    a = leads.compile_sql(_SPEC, as_of="2026-06-28")
    b = leads.compile_sql(_SPEC, as_of="2026-06-29")
    assert receipt.sql_sha256(a) == receipt.sql_sha256(a)      # stable
    assert receipt.sql_sha256(a) != receipt.sql_sha256(b)      # a different clock => different proof
    assert len(receipt.sql_sha256(a)) == 64                    # hex sha256


# ---- the source set: what the skeptic must reach (and the grant gap) ----

def test_source_tables_cover_the_join():
    tabs = receipt.source_tables(_SPEC)
    assert any("FED_HHS_OIG_LEIE" in t for t in tabs)
    assert any("FED_CMS_FACILITY_AFFILIATION" in t for t in tabs)
    # enrich rosters (CCN -> facility name) are sources too
    assert any("FED_CMS_DIALYSIS" in t for t in tabs)


def test_flagship_evidence_lives_in_staging():
    """Regression guard for the verifier-reach bug: the flagship's evidence is in LIBRARY_STAGING,
    which the read-only role must be granted (scripts/grant_mcp_readonly_staging.py)."""
    tabs = receipt.source_tables(_FLAGSHIP)
    assert any(t.startswith("LIBRARY_STAGING.") for t in tabs)


# ---- the receipt assembles with every load-bearing field present ----

def test_assemble_has_the_contract_fields():
    lead = {
        "LEAD_ID": "LEAD_abc", "RULE_NAME": "banned_but_operating",
        "LEFT_KEY_TYPE": "NPI", "LEFT_KEY_VALUE": "1164450573",
        "TITLE": "Jane Doe — OIG-excluded; affiliated with 3 CMS facilities",
        "SCORE": 0.81, "EVIDENCE": json.dumps([{"ccn": "012345", "facility": "X HOSPITAL"}]),
        "EVIDENCE_COUNT": 1,
        "COMPILED_SQL": "SELECT 1", "SQL_SHA256": receipt.sql_sha256("SELECT 1"),
        "AS_OF_DATE": "2026-06-28", "REVIEW_STATE": "pending", "PUBLISHED": False,
    }
    snaps = [{"table": "LIBRARY_RAW.LANDING.FED_HHS_OIG_LEIE", "source_run_id": "r1",
              "ingest_sha256": "deadbeef", "ingest_status": "success", "rows": 83464}]
    rc = receipt.assemble(_SPEC, lead, snaps)
    for k in ("claim", "entity", "conflict", "query", "query_sha256",
              "as_of_date", "sources", "source_snapshots", "confidence", "review_state"):
        assert k in rc, f"receipt missing contract field {k}"
    assert rc["entity"]["key_value"] == "1164450573"
    assert rc["query"] == "SELECT 1"
    assert rc["query_sha256"] == receipt.sql_sha256("SELECT 1")
    assert rc["published"] is False               # unreviewed never reads as fact
    # render must not crash and must carry the proof + the verify instructions
    text = receipt.render(rc)
    assert "THE QUERY" in text and "HOW TO VERIFY" in text and "1164450573" in text


def test_assemble_marks_published_only_when_confirmed():
    base = {"LEAD_ID": "L", "RULE_NAME": "banned_but_operating", "LEFT_KEY_TYPE": "NPI",
            "LEFT_KEY_VALUE": "1", "TITLE": "x", "SCORE": 1.0, "EVIDENCE": "[]",
            "EVIDENCE_COUNT": 0, "COMPILED_SQL": "SELECT 1", "SQL_SHA256": "h", "AS_OF_DATE": "2026-06-28"}
    assert receipt.assemble(_SPEC, {**base, "REVIEW_STATE": "confirmed", "PUBLISHED": True}, [])["published"] is True
    assert receipt.assemble(_SPEC, {**base, "REVIEW_STATE": "pending", "PUBLISHED": False}, [])["published"] is False
