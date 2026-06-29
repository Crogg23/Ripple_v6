"""The receipt — the "run it yourself" proof that travels with every lead.

The trust doctrine (design + memory: detective-trust-doctrine): AI is the forklift,
not the witness. A finding is only trustworthy if a HOSTILE skeptic who thinks the AI
is garbage can reproduce it with ZERO trust in the AI. That means a finding cannot rest
on "the AI looked at it" — it must ship the exact, frozen, runnable artifact the engine
ran, pinned to the exact data snapshot it ran against.

This module turns a LEADS row into that artifact. Three load-bearing pieces, each one a
thing the skeptic re-runs rather than reconstructs:

  COMPILED_SQL + SQL_SHA256   the EXACT query the engine executed (clock frozen to AS_OF,
                              so re-running reproduces the same numbers forever — not a
                              paraphrase a hand-typed query would diverge from).
  AS_OF_DATE                  the frozen wall-clock baked into the SQL (kills the
                              CURRENT_DATE drift that made "byte-stable" a lie).
  SOURCE_SNAPSHOTS            per source table: its _SOURCE_RUN_ID + the INGEST_RUNS
                              manifest SHA256 + status, so a later snapshot-replace of
                              LANDING can't silently rewrite a published number.

The pure helpers (sql_sha256 / source_tables / assemble) are DB-free so they unit-test
offline; resolve_snapshots / fetch_lead / source_urls / run touch Snowflake read-only.
"""

from __future__ import annotations

import hashlib
import json
import re

from . import db, store
from .leads_specs import JOBS

_ISO = re.compile(r"^\d{4}-\d{2}-\d{2}$")

INGEST_RUNS_FQN = "LIBRARY_META.INGEST_LOGS.INGEST_RUNS"
REGISTRY_FQN = "LIBRARY_META.REGISTRY.SOURCE_REGISTRY"


# --------------------------------------------------------------------------- #
# PURE helpers (no DB) — unit-testable offline.
# --------------------------------------------------------------------------- #
def sql_sha256(sql: str) -> str:
    """Content hash of the compiled SQL — the artifact's identity. A skeptic hashes the
    text they were handed and confirms it equals the published SQL_SHA256 before running."""
    return hashlib.sha256(sql.encode("utf-8")).hexdigest()


def source_tables(spec: dict) -> list[str]:
    """Every fully-qualified source object the spec's SQL reads — the tables a skeptic must
    be able to SELECT to reproduce the lead (and the ones we pin a snapshot for)."""
    tabs = [spec["left"]["table"], spec["right"]["table"]]
    en = spec.get("enrich_name")
    if en:
        tabs += [t for t, _name in en.get("tables", [])]
    seen, out = set(), []
    for t in tabs:
        f = db.fqn(t)
        if f not in seen:
            seen.add(f)
            out.append(f)
    return out


def assemble(spec: dict, lead: dict, snapshots: list[dict],
             source_urls: dict[str, dict] | None = None) -> dict:
    """Compose the full receipt object from a LEADS row + its spec + resolved provenance.

    PURE: every input is already-fetched data, so this is offline-testable. The receipt is
    the contract — a finding that cannot fill THE QUERY / SOURCES / SNAPSHOTS is not shippable.
    """
    source_urls = source_urls or {}
    L, R = spec["left"], spec["right"]
    ev = lead.get("EVIDENCE")
    if isinstance(ev, str):
        try:
            ev = json.loads(ev)
        except Exception:
            ev = []
    review = lead.get("REVIEW_STATE") or "pending"
    return {
        "lead_id": lead.get("LEAD_ID"),
        "claim": lead.get("TITLE"),  # neutral, templated — never causal/intent language
        "entity": {
            "key_type": lead.get("LEFT_KEY_TYPE"),
            "key_value": lead.get("LEFT_KEY_VALUE"),  # the hard ID IS the identity
        },
        "conflict": {
            "flag_source": db.fqn(L["table"]),     # the "should-be-banned" side
            "active_source": db.fqn(R["table"]),   # the "is-active" side
            "evidence_count": lead.get("EVIDENCE_COUNT"),
            "evidence_sample": (ev or [])[:5],
        },
        "query": lead.get("COMPILED_SQL"),         # run it yourself
        "query_sha256": lead.get("SQL_SHA256"),
        "as_of_date": str(lead.get("AS_OF_DATE") or ""),  # the frozen clock in the SQL
        "sources": [
            {"table": t,
             "url": source_urls.get(t, {}).get("url"),
             "publisher": source_urls.get(t, {}).get("publisher")}
            for t in source_tables(spec)
        ],
        "source_snapshots": snapshots,             # pinned data version per source
        "confidence": {
            "score": lead.get("SCORE"),
            "note": "uncalibrated composite score — a ranking signal, NOT a probability; "
                    "tier is the human review state below",
        },
        "review_state": review,
        "published": bool(lead.get("PUBLISHED")) if "PUBLISHED" in lead else (review == "confirmed"),
    }


def render(receipt: dict) -> str:
    """Plain-text receipt — the artifact a skeptic reads, then ignores the AI and runs the SQL."""
    e = receipt["entity"]
    c = receipt["conflict"]
    lines = [
        "━" * 70,
        f"RECEIPT — {receipt.get('lead_id')}",
        "━" * 70,
        f"CLAIM:    {receipt.get('claim')}",
        f"ENTITY:   {e.get('key_type')} {e.get('key_value')}   "
        f"(the government ID IS the identity — not an AI guess)",
        f"CONFLICT: {c.get('flag_source')}  ⟂  {c.get('active_source')}   "
        f"({c.get('evidence_count')} matched record(s))",
        f"AS OF:    {receipt.get('as_of_date')}   (clock frozen into the SQL → reproducible)",
        "",
        "SOURCES (primary, public — verify there, not here):",
    ]
    for s in receipt.get("sources", []):
        lines.append(f"   • {s['table']}{('  ' + s['url']) if s.get('url') else '  (no registry URL)'}")
    lines.append("")
    lines.append("DATA SNAPSHOT PINNED (a later reload can't silently move these):")
    for s in receipt.get("source_snapshots", []):
        if s.get("source_run_id"):
            lines.append(f"   • {s['table']}  run={s['source_run_id']}  "
                         f"sha={(s.get('ingest_sha256') or '')[:16]}…  "
                         f"status={s.get('ingest_status')}  rows={s.get('rows')}")
        else:
            lines.append(f"   • {s['table']}  ⚠ {s.get('note', 'snapshot unresolved')}")
    conf = receipt.get("confidence", {})
    lines += [
        "",
        f"CONFIDENCE: score={conf.get('score')}  ({conf.get('note')})",
        f"REVIEW:     {receipt.get('review_state')}   PUBLISHED={receipt.get('published')}",
        f"QUERY SHA256: {receipt.get('query_sha256')}",
        "",
        "── THE QUERY (run it yourself, read-only — this is the whole proof) ──",
        (receipt.get("query") or "(no compiled SQL stored — re-run `connect leads --run` to stamp it)"),
        "━" * 70,
        "HOW TO VERIFY (zero trust in the AI required):",
        "  1. sha256 the query text above; confirm it equals QUERY SHA256.",
        "  2. Run it under the read-only role against the PINNED snapshot.",
        "  3. Confirm this ENTITY's key appears with this evidence count.",
        "  4. Click the SOURCES; confirm the rows exist at the primary publisher.",
        "━" * 70,
    ]
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# DB helpers (read-only) — resolve provenance from the live warehouse.
# --------------------------------------------------------------------------- #
def resolve_snapshots(conn, spec: dict) -> list[dict]:
    """Pin every source table to its current snapshot identity.

    The AUTHORITATIVE pin is _SOURCE_RUN_ID (constant across chunks of one load), joined to
    INGEST_RUNS for the manifest SHA + status — NOT `SELECT DISTINCT _SRC_SHA256` (chunked
    loads write a different per-chunk SHA, so a DISTINCT set would never match one stored hash).
    A non-landing object (a dbt staging view) carries no _SOURCE_RUN_ID — recorded honestly as
    unresolved so the receipt never claims a pin it doesn't have.
    """
    out = []
    for t in source_tables(spec):
        rec = {"table": t}
        try:
            row = db.dicts(conn, f"SELECT ANY_VALUE(_SOURCE_RUN_ID) AS RID, COUNT(*) AS N FROM {t}")
            rid = row[0]["RID"] if row else None
            rec["rows"] = row[0]["N"] if row else None
            if rid:
                rec["source_run_id"] = rid
                ing = db.dicts(conn, f"SELECT SHA256, STATUS, STARTED_AT FROM {INGEST_RUNS_FQN} "
                                     f"WHERE RUN_ID = %s LIMIT 1", (rid,))
                if ing:
                    rec["ingest_sha256"] = ing[0].get("SHA256")
                    rec["ingest_status"] = ing[0].get("STATUS")
                    rec["ingest_started_at"] = str(ing[0].get("STARTED_AT") or "")
            else:
                rec["note"] = "non-landing object (dbt view?) — pin its underlying LANDING sources"
        except Exception as exc:  # missing column / no access / view — record, don't crash
            rec["note"] = f"unresolved: {type(exc).__name__}"
        out.append(rec)
    return out


def source_urls(conn, spec: dict) -> dict[str, dict]:
    """Map each source table -> its primary-source URL + publisher from SOURCE_REGISTRY.
    Landing table = UPPER(SOURCE_ID), so we match the registry on the bare table name."""
    urls: dict[str, dict] = {}
    for t in source_tables(spec):
        bare = t.split(".")[-1]
        try:
            r = db.dicts(conn, f"SELECT URL, PUBLISHER FROM {REGISTRY_FQN} "
                               f"WHERE UPPER(SOURCE_ID) = %s LIMIT 1", (bare,))
            if r:
                urls[t] = {"url": r[0].get("URL"), "publisher": r[0].get("PUBLISHER")}
        except Exception:
            pass
    return urls


def fetch_lead(conn, lead_id: str) -> dict | None:
    rows = db.dicts(conn, f"SELECT * FROM {store.cfqn('LEADS')} WHERE LEAD_ID = %s LIMIT 1", (lead_id,))
    return rows[0] if rows else None


def run(lead_id: str, sql_only: bool = False, as_json: bool = False, check: bool = False) -> None:
    """`connect receipt --id LEAD_xxx` — print the run-it-yourself receipt for one lead."""
    conn = db.connect()
    try:
        lead = fetch_lead(conn, lead_id)
        if not lead:
            raise SystemExit(f"no lead {lead_id} in {store.cfqn('LEADS')}")
        spec = JOBS.get(lead.get("RULE_NAME"))
        if not spec:
            raise SystemExit(f"lead {lead_id} has unknown rule {lead.get('RULE_NAME')!r} "
                             "(spec retired?) — cannot rebuild receipt")
        if sql_only:
            print(lead.get("COMPILED_SQL") or "(no compiled SQL stored)")
            return
        snaps = json.loads(lead["SOURCE_SNAPSHOTS"]) if isinstance(lead.get("SOURCE_SNAPSHOTS"), str) \
            else (lead.get("SOURCE_SNAPSHOTS") or [])
        rc = assemble(spec, lead, snaps, source_urls(conn, spec))
        if as_json:
            print(json.dumps(rc, indent=2, default=str))
            return
        print(render(rc))
        if check:
            _verify(conn, lead)
    finally:
        conn.close()


def _verify(conn, lead: dict) -> None:
    """Actually re-run the stored COMPILED_SQL read-only and confirm the entity still appears.
    This is the machine doing what the skeptic would do — the claim proving itself."""
    sql = lead.get("COMPILED_SQL")
    if not sql:
        print("\n[VERIFY] no compiled SQL stored — nothing to re-run.")
        return
    stored_sha = lead.get("SQL_SHA256")
    if stored_sha and sql_sha256(sql) != stored_sha:
        print("\n[VERIFY] ✗ stored SQL does not match its SHA256 — tampered/desynced.")
        return
    print("\n[VERIFY] re-running the stored SQL read-only against the live warehouse…")
    try:
        rows = db.dicts(conn, sql)
        key = str(lead.get("LEFT_KEY_VALUE"))
        hit = any(str(r.get("LEFT_KEY_VALUE")) == key for r in rows)
        print(f"[VERIFY] {'✓ reproduced' if hit else '✗ NOT reproduced'} — "
              f"{len(rows)} rows; entity {key} {'present' if hit else 'ABSENT'} "
              f"(note: live data may have moved off the pinned snapshot).")
    except Exception as exc:
        print(f"[VERIFY] could not re-run: {type(exc).__name__}: {exc} "
              "(likely the read-only role can't reach a source table — see the staging grant fix).")
