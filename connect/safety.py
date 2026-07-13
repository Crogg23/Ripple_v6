"""The publish-safety spine — nothing about a NAMED real person ships without passing here.

From design-confidence-ladder.md §9. This is the half that turns a clever scorer into something
you can actually publish journalism with. Four guarantees:

  RETRACTION THAT STICKS   a human verdict (confirmed / rejected / retracted) is recorded in the
      rebuild-surviving DECISIONS table; every publish path anti-joins it, so a rejected claim can
      never be resurrected by the next CREATE-OR-REPLACE rebuild of leads / links / the spine.
  REVIEW IS A RECORDED ACT 'confirmed' means a person decided so (or the claim cleared an
      auto-confirm tier) — an unreviewed maybe is carried as 'pending', never shown as fact.
  STALENESS EXPIRES        a claim whose supporting rows vanish from the source is marked stale and
      drops out of publication, so nobody stays publicly accused on data that no longer supports it.
  TRUST-GATED CORPUS       the rarity (TF) corpus and the identity spine should read only trusted
      sources, so a junk / auto-harvested / thin dataset can't poison rarity weights or fuse a
      stranger into someone's entity. `trusted_source_predicate` is the gate (hook, ready to wire).

DECISIONS is an append-only audit log (who / when / what / why); the LATEST verdict per target wins.
"""

from __future__ import annotations

from . import db, store  # noqa: F401  (store still used by siblings importing through here)

# Decisions moved to the scoped review lane 2026-07-12 (Reading Room):
# LIBRARY_META.REVIEW.DECISIONS, written in production ONLY via the
# RIPPLE_REVIEW_WRITER role (INSERT+SELECT, nothing else — append-only is
# the database's guarantee). This constant is the single switch every
# consumer follows. The old CONNECT.DECISIONS stub (0 rows) was retired by
# scripts/provision_review_lane.sql.
DECISIONS_FQN = '"LIBRARY_META"."REVIEW"."DECISIONS"'

DECISIONS_DDL = f"""
CREATE TABLE IF NOT EXISTS {DECISIONS_FQN} (
    DECISION_ID    STRING DEFAULT UUID_STRING(),
    TARGET_KIND    STRING NOT NULL DEFAULT 'lead',  -- 'lead' | 'link' | 'entity'
    TARGET_ID      STRING NOT NULL,    -- the stable id of the claim (LEAD_ID, link hash, ...)
    DECISION       STRING NOT NULL,    -- 'confirmed' | 'rejected' | 'retracted' | 'stale' | 'needs_work'
    REASON         STRING,
    REVIEWER       STRING,
    MODEL_VERSION  STRING,             -- which scoring model produced the claim being judged
    QUEUE_SNAPSHOT VARIANT,            -- what the reviewer was shown at decision time
    DECIDED_AT     TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
)
"""

# needs_work is deliberately NON-suppressing: the claim stays visible
# (flagged) and unpublished — the Reading Room's third button.
VALID = {"confirmed", "rejected", "retracted", "stale", "needs_work"}
SUPPRESS = {"rejected", "retracted", "stale"}   # latest verdict in here -> never shown as fact


def ensure(conn) -> None:
    """Probe-first: the scoped review lane can SELECT but not CREATE, so
    DDL is attempted only when the table is genuinely absent (bootstrap or
    admin sessions). In production the table exists — provisioned by
    scripts/provision_review_lane.sql — and this is a no-op read."""
    try:
        db.rows(conn, f"SELECT 1 FROM {DECISIONS_FQN} LIMIT 1")
        return
    except Exception:
        pass
    db.rows(conn, 'CREATE SCHEMA IF NOT EXISTS "LIBRARY_META"."REVIEW"')
    db.rows(conn, DECISIONS_DDL)


def record(conn, kind: str, target_id: str, decision: str,
           reviewer: str = "", reason: str = "", model_version: str = "") -> None:
    """Append a human (or automated) verdict to the audit log."""
    if decision not in VALID:
        raise ValueError(f"decision must be one of {sorted(VALID)}, got {decision!r}")
    ensure(conn)
    db.rows(conn, f"""INSERT INTO {DECISIONS_FQN}
        (TARGET_KIND, TARGET_ID, DECISION, REASON, REVIEWER, MODEL_VERSION)
        SELECT %s, %s, %s, %s, %s, %s""",
        (kind, target_id, decision, reason, reviewer, model_version))


def latest(conn, kind: str) -> dict[str, str]:
    """The most recent verdict per target id (the audit log keeps the history; this is the view).
    The permanent SMOKE_TEST proof row (planted by verify_review_lane.sql) is filtered here,
    matching every SQL surface (V_LATEST_DECISIONS, V_STATE)."""
    ensure(conn)
    rows = db.dicts(conn, f"""
        SELECT TARGET_ID, DECISION FROM {DECISIONS_FQN}
        WHERE TARGET_KIND = %s AND TARGET_ID != 'SMOKE_TEST'
        QUALIFY ROW_NUMBER() OVER (PARTITION BY TARGET_ID ORDER BY DECIDED_AT DESC) = 1""", (kind,))
    return {r["TARGET_ID"]: r["DECISION"] for r in rows}


def suppressed(conn, kind: str) -> set[str]:
    """Target ids whose latest verdict means 'never publish' — the anti-join set for publish paths."""
    return {tid for tid, d in latest(conn, kind).items() if d in SUPPRESS}


def gate_rows(rows: list[dict], decisions: dict[str, str],
              id_key: str = "LEAD_ID", auto_key: str = "auto_ok") -> list[dict]:
    """PURE (no DB) so it is unit-testable: apply the publish gate to a list of claims.

    A claim is DROPPED if its latest verdict suppresses it (rejected / retracted / stale).
    Survivors carry REVIEW_STATE and PUBLISHED — PUBLISHED is true only if a human CONFIRMED it
    or it cleared an auto-confirm tier (auto_key truthy). An unreviewed claim survives but is
    marked 'pending' and PUBLISHED=False, so it is never presented as established fact.
    """
    out = []
    for r in rows:
        d = decisions.get(r.get(id_key))
        if d in SUPPRESS:
            continue
        r2 = dict(r)
        r2["REVIEW_STATE"] = d or "pending"
        r2["PUBLISHED"] = (d == "confirmed") or bool(r.get(auto_key, False))
        out.append(r2)
    return out


def trusted_source_predicate(reg_alias: str = "reg") -> str:
    """SQL predicate restricting a corpus to TRUSTED registry sources — a junk / thin / auto-harvested
    dataset can't then poison the rarity (TF) weights or fuse a stranger into the identity spine.
    Curated corpora pass today; this is the gate to apply as the TF/spine corpora widen to ~900 sources.

    CAVEAT: the returned string contains literal % (LIKE patterns). Only concatenate it into
    PARAMETERLESS SQL — the connector's pyformat binding runs `sql % params` whenever a non-empty
    params tuple is passed, which would mangle these %. If you must bind params in the same query,
    double the percents (%%) or keep this predicate in a separate parameterless statement."""
    notes = f"COALESCE(UPPER({reg_alias}.NOTES), '')"
    return (f"COALESCE({reg_alias}.INCLUDE, '') = 'Y' "
            f"AND {notes} NOT LIKE '%THIN%' AND {notes} NOT LIKE '%REVIEW%' "
            f"AND {notes} NOT LIKE '%DEMO%'")


def status(conn, kind: str | None = None) -> list[dict]:
    """Counts of current verdicts, for the `safety` CLI."""
    ensure(conn)
    where = "WHERE TARGET_KIND = %s" if kind else ""
    params = (kind,) if kind else ()
    return db.dicts(conn, f"""
        WITH cur AS (
          SELECT TARGET_KIND, TARGET_ID, DECISION FROM {DECISIONS_FQN} {where}
          QUALIFY ROW_NUMBER() OVER (PARTITION BY TARGET_KIND, TARGET_ID ORDER BY DECIDED_AT DESC) = 1 )
        SELECT TARGET_KIND, DECISION, COUNT(*) AS N FROM cur
        WHERE TARGET_ID != 'SMOKE_TEST'
        GROUP BY 1, 2 ORDER BY 1, 2""", params)
