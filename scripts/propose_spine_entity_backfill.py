#!/usr/bin/env python3
"""Propose SPINE_ENTITY for sources that have a PROVEN grain/natural_key but a
NULL spine_entity -- the "grain proven, entity unknown" backlog left by
scripts/profile_spine_backfill.py (the generic-id and winning-composite paths
resolve a per-row key but can't always say WHAT the row is about).

Scope: LIBRARY_META.REGISTRY.SOURCE_REGISTRY WHERE grain IS NOT NULL AND
spine_entity IS NULL. Sets ONLY spine_entity -- never touches GRAIN/NATURAL_KEY
(those are already proven and out of scope here).

Two evidence tiers, both preview-by-default (Chris runs --apply):

  TIER 1 -- NAME (auto-writable). Re-run the SAME deterministic name->entity map
    the base profiler uses (profile_spine_backfill.entity_for_columns:
    detect_key/verbose -> SPINE_ENTITY_BY_KEY, then a vocab word in the name)
    over the STORED natural_key columns. This recovers every composite key whose
    winning columns carry a recognized identifier (NPI->provider, FIPS/ZIP/
    LATLON->place, DOCKET->case, EIN/CIK/UEI->organization) that the generator's
    re-derivation step dropped. Zero queries, zero guessing -- pure name logic
    that was always available, just not applied to the winning composite.

  TIER 2 -- VALUES (place auto-writable; org/person report-only SUGGESTIONS).
    For what Tier 1 can't name, sample real column VALUES:
      * place  -- the natural_key column's values validate as US FIPS codes
        (2-digit state or 5-digit county, valid prefix) at >= PLACE_THRESHOLD.
        The grain IS geographic (one row per place), so this is a safe, grain-
        aligned entity call. Auto-written.
      * organization / person -- a prominent NAME column is dominated by org
        tokens (INC/LLC/CORP/...) or the table carries structured FIRST_NAME +
        LAST_NAME columns. These describe what a row is ABOUT but the row's grain
        may be a transaction/filing rather than the org/person itself, so they
        are SUGGESTIONS only: printed with evidence for Chris to adjudicate,
        never auto-written unless --include-suggested is passed.

Everything with no strong signal is left NULL -- an honest "grain proven, entity
still unknown" state, exactly like the profiler's AMBIGUOUS bucket.

    python3 scripts/propose_spine_entity_backfill.py                    # preview all
    python3 scripts/propose_spine_entity_backfill.py --limit 40          # preview first 40
    python3 scripts/propose_spine_entity_backfill.py --apply             # write TIER1 + place
    python3 scripts/propose_spine_entity_backfill.py --apply --include-suggested  # + org/person

Read-only in preview (SELECTs + samples only). --apply snapshots the registry to
a rollback table first. Companion to profile_spine_backfill.py; shares its
name->entity helper so the two never disagree.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO / "library-onboarding"))
sys.path.insert(0, str(_REPO / "connect"))
sys.path.insert(0, str(_REPO / "scripts"))
try:
    from dotenv import load_dotenv
    load_dotenv(_REPO / "library-onboarding/.env", override=True)
except Exception:  # pragma: no cover
    pass

import snow  # noqa: E402
from keys import detect_key, quote_ident  # noqa: E402
# Shared name->entity map + priority -- the SAME logic the base profiler applies,
# imported so a source resolves identically in both scripts.
from profile_spine_backfill import (  # noqa: E402
    entity_for_columns,
    _AUDIT_COLUMN_NAMES,
    SPINE_ENTITY_PRIORITY,
)

REGISTRY = "LIBRARY_META.REGISTRY.SOURCE_REGISTRY"
RAW_SCHEMA_FQN = "LIBRARY_RAW.LANDING"
BACKUP = "LIBRARY_META.REGISTRY._SOURCE_REGISTRY_BAK_SPINE_ENTITY_20260706"
REPORT_DIR = _REPO / "outputs"
REPORT_PATH = REPORT_DIR / "spine_entity_backfill_report_2026-07-06.md"

SAMPLE_ROWS = 1000          # fixed-size row sample per Tier-2 source (cheap)
MIN_NONNULL = 20            # need at least this many non-null sampled values to judge
PLACE_THRESHOLD = 0.90      # >= this fraction of key values must validate as FIPS
ORG_THRESHOLD = 0.45        # >= this fraction of name values carry an org token

# Valid US state/territory FIPS prefixes (2-digit). County FIPS = prefix + 3.
VALID_STATE_FIPS = {
    "01", "02", "04", "05", "06", "08", "09", "10", "11", "12", "13", "15", "16",
    "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29",
    "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42",
    "44", "45", "46", "47", "48", "49", "50", "51", "53", "54", "55", "56",
    "60", "66", "69", "72", "74", "78",  # AS GU MP PR UM VI
}

# Tokens that mark a column as holding an entity NAME (not an id/date/amount).
_NAME_COL_TOKENS = {
    "name", "nm", "company", "org", "organization", "entity", "business",
    "firm", "employer", "recipient", "vendor", "payee", "applicant", "owner",
    "contributor", "donor", "filer", "registrant", "grantee", "awardee",
}
_FIRST_TOKENS = {"first", "fname", "firstname", "givenname", "given"}
_LAST_TOKENS = {"last", "lname", "lastname", "surname", "familyname", "family"}
# A "first/last" match is only a NAME if the column isn't actually a timestamp --
# FIRST_SEEN / LAST_UPDATED / LAST_MODIFIED share the first/last token but are
# dates. Any of these tokens present disqualifies the column from the person test.
_DATE_AUDIT_TOKENS = {
    "seen", "date", "time", "datetime", "timestamp", "ts", "updated", "modified",
    "created", "changed", "edited", "login", "active", "loaded", "refreshed",
}
# A FIPS-VALUED key column is only trusted as 'place' when its NAME also carries a
# geographic token -- pure value validation false-positives on sequential
# surrogate ids (19256,19257,...) and domain codes (water-district ids) that
# happen to fall in valid FIPS prefix ranges. Name + value must corroborate.
_GEO_NAME_TOKENS = {
    "geo", "geoid", "fips", "county", "counties", "state", "statefp", "countyfp",
    "tract", "blockgroup", "block", "cbsa", "msa", "zcta", "place", "region",
    "location", "geography", "censusblock", "geocode", "geog",
}

# Org-name tokens -- if a name column's values carry one of these, it's an
# organization, not a person. Compact set of the common legal/institutional
# suffixes and forms seen across US public data.
_ORG_TOKENS = {
    "inc", "incorporated", "llc", "llp", "lp", "ltd", "limited", "corp",
    "corporation", "co", "company", "plc", "pllc", "pc", "associates",
    "association", "assn", "assoc", "foundation", "trust", "bank", "bancorp",
    "university", "college", "hospital", "institute", "institution",
    "department", "dept", "agency", "council", "commission", "authority",
    "district", "board", "bureau", "office", "services", "group", "holdings",
    "partners", "partnership", "systems", "solutions", "enterprises",
    "industries", "technologies", "international", "national", "federal",
    "management", "capital", "ventures", "fund", "committee", "pac", "union",
    "society", "center", "centre", "clinic", "laboratories", "labs",
}


def _tokens(name: str) -> set[str]:
    from tag_portal_index import tokens  # on sys.path via connect/keys.py
    return tokens(name)


def fetch_scope(cur, limit: int | None) -> list[dict]:
    cur.execute(
        f"""
        SELECT source_id, ARRAY_TO_STRING(natural_key, ',')
        FROM {REGISTRY}
        WHERE grain IS NOT NULL AND spine_entity IS NULL
        ORDER BY source_id
        """
    )
    rows = [{"source_id": r[0], "natural_key": [c for c in (r[1] or "").split(",") if c]}
            for r in cur.fetchall()]
    return rows[:limit] if limit else rows


def fetch_all_columns(cur) -> dict[str, list[tuple[str, str]]]:
    """{TABLE_NAME: [(COLUMN, DATA_TYPE), ...]} for every LANDING table, one query.
    Audit columns (leading-underscore AND the bare portal_* SOURCE_RUN_ID/
    INGESTED_AT/SRC_SHA256 triple) are excluded -- same rule as the profiler."""
    cur.execute(
        "SELECT table_name, column_name, data_type "
        "FROM LIBRARY_RAW.INFORMATION_SCHEMA.COLUMNS "
        "WHERE table_schema='LANDING' ORDER BY table_name, ordinal_position"
    )
    out: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for table, col, dtype in cur.fetchall():
        if col.startswith("_") or col in _AUDIT_COLUMN_NAMES:
            continue
        out[table].append((col, dtype))
    return out


# ---------------------------------------------------------------------------
# Tier-2 value detectors
# ---------------------------------------------------------------------------

def _is_fips(v: str) -> bool:
    v = (v or "").strip()
    if re.fullmatch(r"\d{5}", v):
        return v[:2] in VALID_STATE_FIPS
    if re.fullmatch(r"\d{2}", v):
        return v in VALID_STATE_FIPS
    return False


def _name_columns(columns: list[tuple[str, str]], key_cols: set[str]) -> list[str]:
    out = []
    for col, _dtype in columns:
        if col in key_cols:
            continue
        if _tokens(col) & _NAME_COL_TOKENS:
            out.append(col)
    return out


def _person_name_columns(columns: list[tuple[str, str]]) -> tuple[str | None, str | None]:
    first = last = None
    for col, _dtype in columns:
        toks = _tokens(col)
        if toks & _DATE_AUDIT_TOKENS:  # FIRST_SEEN / LAST_UPDATED are dates, not names
            continue
        if not first and toks & _FIRST_TOKENS:
            first = col
        if not last and toks & _LAST_TOKENS:
            last = col
    return first, last


def _org_token_rate(values: list[str]) -> float:
    if not values:
        return 0.0
    hits = 0
    for v in values:
        vt = {t for t in re.split(r"[^a-z0-9]+", (v or "").lower()) if t}
        if vt & _ORG_TOKENS:
            hits += 1
    return hits / len(values)


def sample_and_detect(cur, sid: str, key_cols: list[str],
                      columns: list[tuple[str, str]]) -> dict:
    """One bounded sample query per source; return the strongest entity signal.
    place (from key FIPS values) is auto-writable; organization/person are
    report-only suggestions."""
    key_set = set(key_cols)
    name_cols = _name_columns(columns, key_set)
    first_col, last_col = _person_name_columns(columns)
    pull = list(dict.fromkeys(key_cols + name_cols[:3] +
                              [c for c in (first_col, last_col) if c]))
    if not pull:
        return {"entity": None, "reason": "no-sampleable-columns"}

    fqn = f'{RAW_SCHEMA_FQN}."{sid.upper()}"'
    select = ", ".join(quote_ident(c) for c in pull)
    try:
        cur.execute(f"SELECT {select} FROM {fqn} SAMPLE ({SAMPLE_ROWS} ROWS)")
        rows = cur.fetchall()
    except Exception as e:  # keep going on a single bad table
        return {"entity": None, "reason": f"sample-failed: {str(e)[:80]}"}
    idx = {c: i for i, c in enumerate(pull)}

    def col_values(col):
        i = idx[col]
        return [r[i] for r in rows if r[i] is not None and str(r[i]).strip() != ""]

    # --- place: a GEO-NAMED key column whose values validate as FIPS. Both the
    # name and the values must agree -- value-only FIPS matching false-positives
    # on sequential surrogate ids and domain codes that fall in valid prefix
    # ranges (see _GEO_NAME_TOKENS). ---
    for kc in key_cols:
        if kc not in idx or not (_tokens(kc) & _GEO_NAME_TOKENS):
            continue
        vals = col_values(kc)
        if len(vals) >= MIN_NONNULL:
            rate = sum(_is_fips(v) for v in vals) / len(vals)
            if rate >= PLACE_THRESHOLD:
                sample = list(dict.fromkeys(str(v) for v in vals))[:5]
                return {"entity": "place", "tier": "value", "auto": True,
                        "evidence": f"{kc} (geo-named) FIPS-valid {rate:.0%} (n={len(vals)}); "
                                    f"e.g. {', '.join(sample)}"}

    # --- organization: a name column dominated by org tokens ---
    best_org = None
    for nc in name_cols:
        if nc not in idx:
            continue
        vals = col_values(nc)
        if len(vals) >= MIN_NONNULL:
            rate = _org_token_rate([str(v) for v in vals])
            if rate >= ORG_THRESHOLD and (best_org is None or rate > best_org[1]):
                sample = [str(v)[:40] for v in vals[:3]]
                best_org = (nc, rate, sample, len(vals))

    # --- person: structured first + last name columns present & populated ---
    person_sig = None
    if first_col and last_col:
        fv, lv = col_values(first_col), col_values(last_col)
        if len(fv) >= MIN_NONNULL and len(lv) >= MIN_NONNULL:
            person_sig = (first_col, last_col, len(fv))

    # org vs person: if a name column screams org, that wins over a bare
    # first/last pair (many person tables also carry an EMPLOYER_NAME);
    # otherwise a clean first+last is the stronger structural signal.
    if best_org and best_org[1] >= 0.60:
        nc, rate, sample, n = best_org
        return {"entity": "organization", "tier": "value", "auto": False,
                "evidence": f"{nc} org-token {rate:.0%} (n={n}); e.g. {', '.join(sample)}"}
    if person_sig:
        fc, lc, n = person_sig
        return {"entity": "person", "tier": "value", "auto": False,
                "evidence": f"structured {fc}+{lc} populated (n={n})"}
    if best_org:
        nc, rate, sample, n = best_org
        return {"entity": "organization", "tier": "value", "auto": False,
                "evidence": f"{nc} org-token {rate:.0%} (n={n}); e.g. {', '.join(sample)}"}

    return {"entity": None, "reason": "no-strong-value-signal"}


def main() -> int:
    ap = argparse.ArgumentParser(description="Backfill SPINE_ENTITY for grain-proven/entity-unknown sources.")
    ap.add_argument("--apply", action="store_true", help="write proposals (default previews)")
    ap.add_argument("--include-suggested", action="store_true",
                    help="also write org/person value SUGGESTIONS (default: place + name-tier only)")
    ap.add_argument("--limit", type=int, default=None, help="cap sources (validation runs)")
    ap.add_argument("--source-id", default=None, help="only this source (debugging)")
    args = ap.parse_args()

    conn = snow.connect()
    try:
        cur = conn.cursor()
        scope = fetch_scope(cur, args.limit)
        if args.source_id:
            scope = [s for s in scope if s["source_id"] == args.source_id]
        all_columns = fetch_all_columns(cur)
        cur.close()

        print("=" * 78)
        print(f"Spine-entity backfill  --  {len(scope)} grain-proven/entity-unknown sources "
              f"({'APPLY' if args.apply else 'PREVIEW'})")
        print("=" * 78)

        # buckets: NAME (tier1), PLACE (tier2 auto), SUGGESTED (tier2 org/person),
        # UNKNOWN (left NULL), NO_TABLE
        results = {"NAME": [], "PLACE": [], "SUGGESTED": [], "UNKNOWN": [], "NO_TABLE": []}
        t0 = time.time()
        cur = conn.cursor()
        for i, src in enumerate(scope, start=1):
            sid = src["source_id"]
            nk = src["natural_key"]
            columns = all_columns.get(sid.upper())
            if not columns:
                results["NO_TABLE"].append({"source_id": sid})
                continue

            # TIER 1 -- name map over the stored natural key
            ent = entity_for_columns(nk)
            if ent:
                results["NAME"].append({"source_id": sid, "entity": ent,
                                        "evidence": f"natural_key {'+'.join(nk)} -> {ent}"})
                continue

            # TIER 2 -- sample values
            det = sample_and_detect(cur, sid, nk, columns)
            if det.get("entity") == "place":
                results["PLACE"].append({"source_id": sid, "entity": "place",
                                         "evidence": det["evidence"]})
            elif det.get("entity"):
                results["SUGGESTED"].append({"source_id": sid, "entity": det["entity"],
                                             "evidence": det["evidence"]})
            else:
                results["UNKNOWN"].append({"source_id": sid, "reason": det.get("reason", "?")})

            if i % 50 == 0:
                print(f"  ...{i}/{len(scope)} profiled ({time.time() - t0:.0f}s)")
        cur.close()

        n_name, n_place = len(results["NAME"]), len(results["PLACE"])
        n_sug, n_unk, n_not = (len(results["SUGGESTED"]), len(results["UNKNOWN"]),
                               len(results["NO_TABLE"]))
        print(f"\nTIER 1 NAME (auto):        {n_name}")
        print(f"TIER 2 PLACE (auto):       {n_place}")
        print(f"TIER 2 SUGGESTED (org/person, review): {n_sug}")
        print(f"still UNKNOWN (left NULL):  {n_unk}")
        print(f"no physical table:         {n_not}")
        by_ent = Counter(r["entity"] for r in results["NAME"] + results["PLACE"] + results["SUGGESTED"])
        print("by entity: " + ", ".join(f"{e}={n}" for e, n in by_ent.most_common()))

        REPORT_DIR.mkdir(exist_ok=True)
        _write_report(REPORT_PATH, results, args)
        print(f"\nFull report -> {REPORT_PATH}")

        writable = results["NAME"] + results["PLACE"] + (
            results["SUGGESTED"] if args.include_suggested else [])
        if not args.apply:
            print(f"\nPREVIEW only. --apply would write {len(writable)} row(s) "
                  f"({'incl.' if args.include_suggested else 'excl.'} org/person suggestions).")
            print(f"Re-run with --apply  (rollback snapshot -> {BACKUP}).")
            return 0

        cur = conn.cursor()
        cur.execute(f"CREATE OR REPLACE TABLE {BACKUP} AS SELECT * FROM {REGISTRY}")
        print(f"\n  rollback snapshot -> {BACKUP}")
        n_written = 0
        for r in writable:
            cur.execute(
                f"UPDATE {REGISTRY} SET SPINE_ENTITY=%s "
                "WHERE source_id=%s AND spine_entity IS NULL AND grain IS NOT NULL",
                (r["entity"], r["source_id"]),
            )
            n_written += cur.rowcount or 0
        conn.commit()
        cur.close()
        print(f"  wrote spine_entity for {n_written} source(s). "
              f"UNKNOWN ({n_unk}) left NULL. Regenerate affected staging models next.")
        return 0
    finally:
        conn.close()


def _write_report(path: Path, results: dict, args) -> None:
    lines = ["# Spine-entity backfill proposal", ""]
    lines.append(f"NAME {len(results['NAME'])} | PLACE {len(results['PLACE'])} | "
                 f"SUGGESTED {len(results['SUGGESTED'])} | UNKNOWN {len(results['UNKNOWN'])} | "
                 f"NO_TABLE {len(results['NO_TABLE'])}")
    lines.append("")
    lines.append("Sets ONLY spine_entity on grain-proven/entity-unknown sources. "
                 "NAME + PLACE are auto-written by --apply; SUGGESTED needs "
                 "--include-suggested; UNKNOWN stays NULL.")
    lines.append("")
    for bucket, title in (("NAME", "TIER 1 -- NAME map (auto)"),
                          ("PLACE", "TIER 2 -- PLACE, FIPS values (auto)"),
                          ("SUGGESTED", "TIER 2 -- SUGGESTED org/person (review, --include-suggested to write)")):
        lines.append(f"## {title} ({len(results[bucket])})")
        lines.append("")
        lines.append("| source_id | spine_entity | evidence |")
        lines.append("|---|---|---|")
        for v in sorted(results[bucket], key=lambda x: x["source_id"]):
            lines.append(f"| {v['source_id']} | {v['entity']} | {v['evidence']} |")
        lines.append("")
    lines.append(f"## still UNKNOWN -- left NULL ({len(results['UNKNOWN'])})")
    lines.append("")
    lines.append("| source_id | reason |")
    lines.append("|---|---|")
    for v in sorted(results["UNKNOWN"], key=lambda x: x["source_id"]):
        lines.append(f"| {v['source_id']} | {v['reason']} |")
    lines.append("")
    if results["NO_TABLE"]:
        lines.append(f"## no physical LANDING table ({len(results['NO_TABLE'])})")
        lines.append("")
        for v in sorted(results["NO_TABLE"], key=lambda x: x["source_id"]):
            lines.append(f"- {v['source_id']}")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
