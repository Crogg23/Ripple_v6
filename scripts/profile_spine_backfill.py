#!/usr/bin/env python3
"""Deterministically profile every landed source and propose GRAIN / NATURAL_KEY /
SPINE_ENTITY for SOURCE_REGISTRY. No LLM calls -- pure column-name + uniqueness-
ratio heuristics, reusing connect/keys.py's battle-tested identifier tagger so a
column that resolves here resolves the same way connect/'s spine already does.

Scope (Chris, 2026-07-05): everything physically landed --
LIFECYCLE IN ('landed','modeled','sampled') on LIBRARY_META.REGISTRY.CATALOG.

Algorithm per source
---------------------
1. Pull the source's actual landed columns (INFORMATION_SCHEMA, one query for
   every table up front -- not per-source).
2. Run connect/spine_entity.py's tagger over the column names. Split hits into
   IDENTITY keys (NPI/CCN/IMO/MMSI/BIOGUIDE/ICPSR/EIN/CIK/UEI/DUNS/LEI/PATENT/
   DOCKET) and PLACE keys (FIPS/ZIP/LATLON/GEOM/COUNTRY). Identity beats place --
   a FIPS column on an EIN-keyed row is a descriptive attribute, not competing
   grain.
3. Zero identity hits, one or more place hits -> spine_entity='place', candidate
   key = best-ranked place column (FIPS > ZIP > LATLON > GEOM > COUNTRY).
4. Two or more DISTINCT spine_entity values among identity hits (e.g. an NPI
   column AND a CCN column -- a provider-facility bridge row) -> AMBIGUOUS. This
   is a real entity-disambiguation call ("which spine entity applies") -- per
   Chris's non-negotiable principle, we do not guess; it goes in the report.
5. Exactly one spine_entity candidate -> validate with ONE round-trip query:
   COUNT(*), COUNT(DISTINCT key_col), and COUNT(DISTINCT key_col||period_col)
   against the best-ranked period-like column (a DATE/TIMESTAMP-typed column,
   or a name token in {date,year,period,cycle,quarter,fy,...}) if the plain key
   isn't already unique.
     ratio >= 0.98 on the key alone      -> HIGH confidence, entity-grain
     ratio >= 0.98 on key+period only    -> MEDIUM confidence, composite grain
     neither clears 0.98                 -> AMBIGUOUS (ratios reported for Chris)
6. Zero identity/place hits at all -> fall back to the registry's own
   ENTITY_TYPES facet as a HINT only (never auto-applied without a key to
   validate against) -> AMBIGUOUS, hint attached.

--apply writes ONLY the HIGH and MEDIUM confidence rows. AMBIGUOUS and
NO-REGISTRY-ROW sources are never written -- they land in the markdown report
for Chris to adjudicate, and can be re-run through this script (or a follow-up
override list) once he calls them.

    python3 scripts/profile_spine_backfill.py                 # preview, all in-scope
    python3 scripts/profile_spine_backfill.py --limit 60       # preview, first 60 (validation)
    python3 scripts/profile_spine_backfill.py --apply           # write HIGH+MEDIUM rows

Requires scripts/add_spine_columns.py --apply to have run first (GRAIN/
NATURAL_KEY/SPINE_ENTITY columns must exist).
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from collections import defaultdict
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO / "library-onboarding"))
sys.path.insert(0, str(_REPO / "connect"))
try:
    from dotenv import load_dotenv
    load_dotenv(_REPO / "library-onboarding/.env", override=True)
except Exception:  # pragma: no cover
    pass

import snow  # noqa: E402
from keys import KEY_TOKENS, detect_key, quote_ident  # noqa: E402
from spine_entity import SPINE_ENTITY_BY_KEY, SPINE_ENTITY_VOCAB  # noqa: E402

REGISTRY = "LIBRARY_META.REGISTRY.SOURCE_REGISTRY"
RAW_SCHEMA_FQN = "LIBRARY_RAW.LANDING"
BACKUP = "LIBRARY_META.REGISTRY._SOURCE_REGISTRY_BAK_SPINEBACKFILL_20260705"
REPORT_DIR = _REPO / "outputs"

UNIQUE_THRESHOLD = 0.98
IDENTITY_KEYS = {k for k, v in SPINE_ENTITY_BY_KEY.items() if v != "place"}
PLACE_KEYS_RANKED = ["FIPS", "ZIP", "LATLON", "GEOM", "COUNTRY"]  # best -> worst
MAX_DIMENSIONS = 3  # cap on how many extra columns we'll add to a composite key

# CLAUDE.md's audit-column convention is _INGESTED_AT/_SOURCE_RUN_ID/_SRC_SHA256
# (leading underscore) -- but ~1,607 landing tables (almost all portal_*
# open-data-portal harvests, confirmed live via INFORMATION_SCHEMA, not
# assumed) carry the SAME three columns WITHOUT the underscore. Unfiltered,
# these are ingestion-batch metadata that changes on every reload -- if one
# ever ended up IN a natural_key (confirmed happening: 136 already-applied
# sources had bare SOURCE_RUN_ID baked into their composite key before this
# fix), every reload of the SAME real-world rows would look "new" forever,
# silently defeating the whole point of a natural key. Excluded everywhere a
# real column would be considered, exactly like the underscore-prefixed ones.
_AUDIT_COLUMN_NAMES = {"INGESTED_AT", "SOURCE_RUN_ID", "SRC_SHA256"}

_PERIOD_TOKENS = {
    "date", "year", "yr", "period", "cycle", "quarter", "qtr", "month", "fy",
    "fiscal", "reportdate", "asof", "snapshotdate", "vintage", "reportingperiod",
}
_PERIOD_TYPES = {"DATE", "TIMESTAMP_NTZ", "TIMESTAMP_LTZ", "TIMESTAMP_TZ", "TIMESTAMP", "DATETIME"}
# Second-tier dimension signal: a column named like a categorical breakdown key
# (industry code, ownership type, ...) is a common reason a "key" repeats -- e.g.
# BLS QCEW is one row per (FIPS, YEAR, INDUSTRY_CODE, OWNERSHIP), not just per FIPS.
_CATEGORICAL_TOKENS = {
    "type", "category", "code", "class", "classification", "group", "subtype",
    "status", "kind", "level", "tier", "segment", "subcategory", "program",
    "ownership", "industry", "sector",
}

# Priority order for picking ONE spine_entity when a row legitimately carries
# more than one identity column (a bridge/relationship row, e.g. NPI + CCN on a
# provider-facility affiliation). Most-concrete/singular identity first.
SPINE_ENTITY_PRIORITY = [
    "person", "provider", "facility", "vessel", "organization", "place",
    "asset", "case", "aircraft", "payment", "filing", "event",
]

# Verbose-name fallback -- the tight tagger in connect/keys.py only matches
# compact tokens ('ein', 'npi', ...) by design (a false steel tag is worse than
# no tag). This is a SEPARATE, local, second-pass matcher for spelled-out
# government-data column names that never abbreviate -- e.g. a SAM.gov extract
# column literally named "unique_entity_identifier" instead of "uei". Only
# consulted when the tight tagger finds nothing at all on a column, and every
# phrase requires ALL its words present (not just one) -- same "don't
# overclaim" discipline as PAIR_RULES in tag_portal_index.py. This does NOT
# touch connect/keys.py -- it stays local to this one-time backfill so it can
# never change connect/'s live entity-resolution behavior.
_VERBOSE_PHRASES: dict[str, list[frozenset[str]]] = {
    "EIN": [frozenset({"employer", "identification", "number"}),
            frozenset({"federal", "tax", "id"}), frozenset({"federal", "ein"})],
    "NPI": [frozenset({"national", "provider", "identifier"}),
            frozenset({"national", "provider", "id"})],
    "CCN": [frozenset({"cms", "certification", "number"}),
            frozenset({"provider", "certification", "number"})],
    "UEI": [frozenset({"unique", "entity", "identifier"}), frozenset({"unique", "entity", "id"})],
    "LEI": [frozenset({"legal", "entity", "identifier"})],
    "DUNS": [frozenset({"data", "universal", "numbering", "system"})],
    "CIK": [frozenset({"central", "index", "key"})],
    "BIOGUIDE": [frozenset({"bioguide", "id"})],
    "FIPS": [frozenset({"federal", "information", "processing"}),
             frozenset({"county", "fips", "code"}), frozenset({"state", "fips", "code"})],
    "DOCKET": [frozenset({"docket", "number"}), frozenset({"case", "docket"})],
}


def _verbose_key_for_column(col: str) -> str | None:
    toks = _tokens(col)
    for key, phrases in _VERBOSE_PHRASES.items():
        if any(phrase <= toks for phrase in phrases):
            return key
    return None


def _generic_id_candidates(columns: list[tuple[str, str]], exclude_cols: list[str]) -> list[str]:
    """Columns that are almost certainly a per-row record identifier BY NAME --
    a bare 'id' token (COMPLAINT_ID, ACK_ID, FACILITY_ID), never a substring
    match (so 'VALID'/'RESIDENT' etc. can't false-positive -- tokens() only
    splits on case/punctuation boundaries, so 'IDPER' stays one token and is
    correctly NOT caught here; that's a real, accepted miss, not a bug: a false
    'this column is an ID' claim is worse than leaving the source ambiguous).
    Does not overlap with the tight tagger or verbose matcher -- those already
    catch every column this function would also catch that has real entity
    semantics (EIN, NPI, ...); this only fires for what's left."""
    excl = set(exclude_cols)
    out = []
    for col, _dtype in columns:
        if col in excl or col.startswith("_"):
            continue
        key, _tier = detect_key(col)
        if key or _verbose_key_for_column(col):
            continue
        if "id" in _tokens(col):
            out.append(col)
    return out


def _dimension_candidates(columns: list[tuple[str, str]], exclude_cols: list[str],
                           priority_cols: list[str] | None = None) -> list[str]:
    """Rank a table's remaining columns by how likely they are a grain
    dimension (something that, combined with the base key, narrows down to one
    row per real-world thing). Priority order: explicit priority_cols (a known
    strong signal, e.g. a second identity column) > typed DATE/TIMESTAMP
    columns > period-token names > categorical-token names. Capped -- callers
    add at most MAX_DIMENSIONS, so a natural key never grows into an unreadable
    pile. Deliberately does NOT also fold in generic *_ID columns here --
    profile_candidate() tests those SEPARATELY as standalone candidates (a
    clean ID column alone almost always beats bolting it onto a weaker
    cumulative chain); doing it here too would consume the column before that
    better test ever ran."""
    excl = set(exclude_cols)
    priority = [c for c in (priority_cols or []) if c not in excl]
    typed, period_named, cat_named = [], [], []
    for col, dtype in columns:
        if col in excl or col.startswith("_") or col in priority:
            continue
        toks = _tokens(col)
        if (dtype or "").upper() in _PERIOD_TYPES:
            typed.append(col)
        elif toks & _PERIOD_TOKENS:
            period_named.append(col)
        elif toks & _CATEGORICAL_TOKENS:
            cat_named.append(col)
    return (priority + typed + period_named + cat_named)[:MAX_DIMENSIONS]


def _tokens(name: str) -> set[str]:
    from tag_portal_index import tokens  # already on sys.path via connect/keys.py
    return tokens(name)


def fetch_scope(cur) -> list[dict]:
    cur.execute(
        """
        SELECT c.source_id, c.lifecycle,
               ARRAY_TO_STRING(c.entity_types, ','),
               (r.source_id IS NOT NULL) AS has_registry_row
        FROM LIBRARY_META.REGISTRY.CATALOG c
        LEFT JOIN LIBRARY_META.REGISTRY.SOURCE_REGISTRY r ON r.source_id = c.source_id
        WHERE c.lifecycle IN ('landed','modeled','sampled')
        ORDER BY c.source_id
        """
    )
    return [
        {"source_id": r[0], "lifecycle": r[1],
         "entity_types": [x for x in (r[2] or "").split(",") if x],
         "has_registry_row": bool(r[3])}
        for r in cur.fetchall()
    ]


def fetch_all_columns(cur) -> dict[str, list[tuple[str, str]]]:
    """{TABLE_NAME: [(COLUMN_NAME, DATA_TYPE), ...]} for every LANDING table, one query."""
    cur.execute(
        "SELECT table_name, column_name, data_type "
        "FROM LIBRARY_RAW.INFORMATION_SCHEMA.COLUMNS "
        "WHERE table_schema='LANDING' "
        "ORDER BY table_name, ordinal_position"
    )
    out: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for table, col, dtype in cur.fetchall():
        if col.startswith("_") or col in _AUDIT_COLUMN_NAMES:
            continue
        out[table].append((col, dtype))
    return out


def classify(source_id: str, columns: list[tuple[str, str]], entity_types: list[str]) -> dict:
    """Pure, no-SQL classification: candidate identity column(s), so we know
    what to profile with a query. Returns a dict the caller enriches with
    profiling results. base_cols is always a list (length 1 normally, length
    2+ for a resolved multi-entity bridge)."""
    col_names = [c for c, _ in columns]
    identity_hits, place_hits = [], []
    for col in col_names:
        key, tier = detect_key(col)
        if not key or key not in SPINE_ENTITY_BY_KEY:
            continue
        entry = (col, key, SPINE_ENTITY_BY_KEY[key])
        (identity_hits if key in IDENTITY_KEYS else place_hits).append(entry)

    if identity_hits:
        distinct_entities = {e for _, _, e in identity_hits}
        if len(distinct_entities) > 1:
            # Multi-entity row (e.g. NPI + CCN -- a provider-facility bridge).
            # Resolve rather than give up: the natural key is ALL the identity
            # columns together (a bridge row's identity IS the combination),
            # and spine_entity picks the most-concrete type present. Whether
            # this combination is actually unique still gets verified by a
            # real query below -- this is a candidate, not an assumption.
            base_cols = sorted({c for c, _, _ in identity_hits})
            primary = min(distinct_entities, key=SPINE_ENTITY_PRIORITY.index)
            return {"status": "CANDIDATE", "base_cols": base_cols, "entity": primary,
                    "bridge_entities": sorted(distinct_entities),
                    "bridge_keys": sorted({k for _, k, _ in identity_hits})}
        col, key, entity = identity_hits[0]
        return {"status": "CANDIDATE", "base_cols": [col], "entity": entity}

    if place_hits:
        by_key = {key: col for col, key, _ in place_hits}
        for key in PLACE_KEYS_RANKED:
            if key in by_key:
                return {"status": "CANDIDATE", "base_cols": [by_key[key]], "entity": "place"}

    # Nothing matched the tight tagger -- try the verbose-name fallback before
    # giving up (e.g. a SAM.gov extract column literally named
    # "unique_entity_identifier" instead of "uei").
    for col in col_names:
        key = _verbose_key_for_column(col)
        if key and key in SPINE_ENTITY_BY_KEY:
            entity = SPINE_ENTITY_BY_KEY[key]
            return {"status": "CANDIDATE", "base_cols": [col], "entity": entity, "via": "verbose"}

    hint = entity_types[0] if len(entity_types) == 1 else None
    if hint == "company":
        hint = "organization"

    # Last resort: no identity/place/verbose signal at all, but the table has a
    # column that's clearly a per-row record identifier by NAME (e.g.
    # COMPLAINT_ID, ACK_ID, FACILITY_ID -- a bare "id" token, never a substring
    # match, so it can't false-positive the way KEY_TOKENS deliberately avoids
    # for e.g. 'doi'). This proves GRAIN/NATURAL_KEY even when we can't say
    # WHAT the row is about -- spine_entity only gets set from the hint (never
    # invented), so a resolved-grain/unknown-entity row is a real, honest state,
    # not a guess.
    generic_ids = _generic_id_candidates(columns, exclude_cols=[])
    if generic_ids:
        return {"status": "CANDIDATE", "base_cols": [generic_ids[0]], "entity": hint,
                "via": "generic-id", "extra_id_cols": generic_ids[1:]}

    return {"status": "AMBIGUOUS", "reason": "no-key-column", "hint": hint}


def _key_label_for(col: str) -> str:
    key, _tier = detect_key(col)
    return key or _verbose_key_for_column(col) or col


def _entity_from_column_name(col: str) -> str | None:
    """A generic *_ID column's OWN other tokens can name the entity directly
    (FACILITY_ID -> 'facility' is literally in SPINE_ENTITY_VOCAB) -- a naming-
    pattern inference, not a content guess. None if nothing matches."""
    toks = _tokens(col)
    for v in SPINE_ENTITY_VOCAB:
        if v in toks:
            return v
    return None


def entity_for_columns(cols: list[str]) -> str | None:
    """Deterministic spine_entity for a winning key column set, by NAME only,
    using the SAME map the base classify() path uses: detect_key / verbose
    matcher -> SPINE_ENTITY_BY_KEY first, then a spine_entity vocab word literally
    present in the column name. When several columns each imply an entity, the
    most-concrete one wins (SPINE_ENTITY_PRIORITY). None if nothing matches.

    Applied to a winning composite/rescue key so e.g. [NPI, YEAR] resolves to
    'provider' and [COUNTY_FIPS, YEAR] to 'place' -- previously these dropped to
    unknown because only the vocab-word-in-name check ran here, which never
    consulted the key->entity map. Pure name inference, no content guess; shared
    with scripts/propose_spine_entity_backfill.py so both agree."""
    found = []
    for c in cols:
        key, _tier = detect_key(c)
        if not key:
            key = _verbose_key_for_column(c)
        if key and key in SPINE_ENTITY_BY_KEY:
            found.append(SPINE_ENTITY_BY_KEY[key])
            continue
        ent = _entity_from_column_name(c)
        if ent:
            found.append(ent)
    if not found:
        return None
    return min(set(found), key=SPINE_ENTITY_PRIORITY.index)


def profile_candidate(cur, source_id: str, base_cols: list[str], entity: str | None,
                       columns: list[tuple[str, str]], bridge_entities: list[str] | None = None,
                       extra_id_cols: list[str] | None = None) -> dict:
    """Composite search, SMALLEST candidate first. Tries, in order: base_cols
    alone; each generic-id rescue column standalone (a clean ID column found
    elsewhere in the table almost always beats bolting it onto a weaker base --
    e.g. COMPLAINT_ID alone beats ZIP_CODE+DATE_RECEIVED+DATE_SENT+COMPLAINT_ID);
    then base_cols progressively combined with ranked dimension columns. ONE
    round-trip query computes every candidate's ratio at once; the first
    (smallest) to clear UNIQUE_THRESHOLD wins -- parsimony, not just "first
    found". entity may be None (a generic-id-only base with no registry hint)
    -- grain still gets proven, spine_entity is just left unset rather than
    invented. If a standalone rescue ID wins and DIFFERS from base_cols, the
    original entity is dropped (it described the wrong thing) in favor of
    whatever the winning column's own name implies, or None."""
    fqn = f'{RAW_SCHEMA_FQN}."{source_id.upper()}"'
    dims = _dimension_candidates(columns, exclude_cols=base_cols, priority_cols=extra_id_cols)
    rescue_ids = _generic_id_candidates(columns, exclude_cols=list(base_cols) + dims)

    candidates = [list(base_cols)] + [[rid] for rid in rescue_ids] + \
                 [list(base_cols) + dims[: i + 1] for i in range(len(dims))]
    if dims and rescue_ids:
        # last resort: neither the dimension chain nor a standalone rescue ID
        # alone worked -- try everything together.
        candidates.append(list(base_cols) + dims + rescue_ids)
    seen, uniq = set(), []
    for c in candidates:
        k = tuple(sorted(c))
        if k not in seen:
            seen.add(k)
            uniq.append(c)
    uniq.sort(key=len)

    # COALESCE guards against Snowflake's '||' returning NULL for the whole
    # concatenation when ANY one column is NULL -- unguarded, COUNT(DISTINCT)
    # would silently drop those rows from the distinct count (they'd all
    # collapse to NULL) while COUNT(*) still counts them, UNDERSTATING real
    # uniqueness and wrongly leaving a genuinely-unique composite ambiguous.
    select = ["COUNT(*) AS n"]
    for i, level_cols in enumerate(uniq):
        expr = " || '|' || ".join(
            f"COALESCE(TO_VARCHAR({quote_ident(c)}), '\\x01NULL')" for c in level_cols
        )
        select.append(f"COUNT(DISTINCT {expr}) AS d{i}")
    cur.execute(f"SELECT {', '.join(select)} FROM {fqn}")
    row = cur.fetchone()
    n = row[0] or 0
    if n == 0:
        return {"status": "AMBIGUOUS", "reason": "empty-table", "base_cols": base_cols, "entity": entity}

    ratios = [(row[i + 1] or 0) / n for i in range(len(uniq))]
    base_key_ratio = ratios[0]

    for i, level_cols in enumerate(uniq):
        if ratios[i] < UNIQUE_THRESHOLD:
            continue
        is_base = (level_cols == list(base_cols))
        if bridge_entities and is_base:
            entity_desc, level_entity = "-".join(bridge_entities) + " relationship", entity
        elif is_base:
            level_entity = entity
            entity_desc = entity or "record (spine_entity not determined -- no registry hint available)"
        else:
            # A different (usually smaller/cleaner) column set won -- the
            # original base's entity claim (often a weak place fallback) no
            # longer applies. Re-derive from the winning columns' own names,
            # consulting the FULL name->entity map (detect_key/verbose ->
            # SPINE_ENTITY_BY_KEY, then a vocab word in the name), not just the
            # vocab-word check -- so a winning [NPI, YEAR] keeps 'provider'.
            level_entity = entity_for_columns(level_cols)
            entity_desc = level_entity or "record (spine_entity not determined -- no registry hint available)"
        key_desc = "+".join(_key_label_for(c) for c in level_cols)
        confidence = "HIGH" if len(level_cols) == len(base_cols) and is_base else "MEDIUM"
        grain = (f"one row per {entity_desc} ({key_desc} is unique)" if confidence == "HIGH" else
                 f"one row per {entity_desc} ({key_desc} unique)")
        return {"status": confidence, "base_cols": base_cols, "entity": level_entity,
                "natural_key": level_cols, "key_ratio": round(base_key_ratio, 4),
                "composite_ratio": round(ratios[i], 4) if not is_base else None,
                "dims_tried": [c for c in level_cols if c not in base_cols], "grain": grain}

    return {"status": "AMBIGUOUS", "reason": "not-unique-after-dimension-search",
            "base_cols": base_cols, "entity": entity, "key_ratio": round(base_key_ratio, 4),
            "dims_tried": dims + rescue_ids, "ratios_tried": [round(r, 4) for r in ratios]}


def main() -> int:
    ap = argparse.ArgumentParser(description="Profile landed sources for GRAIN/NATURAL_KEY/SPINE_ENTITY.")
    ap.add_argument("--apply", action="store_true", help="write HIGH+MEDIUM rows (default previews)")
    ap.add_argument("--limit", type=int, default=None, help="cap number of sources profiled (validation runs)")
    args = ap.parse_args()

    conn = snow.connect()
    try:
        cur = conn.cursor()
        scope = fetch_scope(cur)
        all_columns = fetch_all_columns(cur)
        cur.close()
        if args.limit:
            scope = scope[: args.limit]

        print("=" * 78)
        print(f"Spine backfill profiling  --  {len(scope)} in-scope sources "
              f"({'APPLY' if args.apply else 'PREVIEW'})")
        print("=" * 78)

        results = {"HIGH": [], "MEDIUM": [], "AMBIGUOUS": [], "NO_TABLE": [], "NO_REGISTRY_ROW": []}
        t0 = time.time()
        cur = conn.cursor()
        for i, src in enumerate(scope, start=1):
            sid = src["source_id"]
            if not src["has_registry_row"]:
                results["NO_REGISTRY_ROW"].append({"source_id": sid, "lifecycle": src["lifecycle"]})
                continue
            columns = all_columns.get(sid.upper())
            if not columns:
                results["NO_TABLE"].append({"source_id": sid, "lifecycle": src["lifecycle"]})
                continue

            verdict = classify(sid, columns, src["entity_types"])
            if verdict["status"] == "CANDIDATE":
                verdict = profile_candidate(cur, sid, verdict["base_cols"], verdict["entity"],
                                             columns, bridge_entities=verdict.get("bridge_entities"),
                                             extra_id_cols=verdict.get("extra_id_cols"))
            verdict["source_id"] = sid
            results[verdict["status"]].append(verdict)

            if i % 100 == 0:
                elapsed = time.time() - t0
                print(f"  ...{i}/{len(scope)} profiled ({elapsed:.0f}s elapsed)")
        cur.close()

        n_high, n_med, n_amb = len(results["HIGH"]), len(results["MEDIUM"]), len(results["AMBIGUOUS"])
        n_notable, n_norow = len(results["NO_TABLE"]), len(results["NO_REGISTRY_ROW"])
        print(f"\nHIGH confidence:    {n_high}")
        print(f"MEDIUM confidence:  {n_med}")
        print(f"AMBIGUOUS:          {n_amb}  (never auto-written)")
        print(f"No physical table:  {n_notable}  (CATALOG says landed, LANDING has no table)")
        print(f"No registry row:    {n_norow}  (can't UPDATE a row that doesn't exist)")

        REPORT_DIR.mkdir(exist_ok=True)
        report_path = REPORT_DIR / "spine_backfill_report_2026-07-05.md"
        _write_report(report_path, results)
        print(f"\nFull report -> {report_path}")

        if not args.apply:
            print("\nPREVIEW only. Re-run with --apply to write HIGH+MEDIUM rows "
                  f"(rollback snapshot -> {BACKUP}).")
            return 0

        cur = conn.cursor()
        cur.execute(f"CREATE OR REPLACE TABLE {BACKUP} AS SELECT * FROM {REGISTRY}")
        print(f"\n  rollback snapshot -> {BACKUP}")

        # Retract first: a source resolved on a PRIOR run (e.g. before a
        # heuristic fix) that is now AMBIGUOUS must not keep its stale, no-
        # longer-trusted GRAIN/NATURAL_KEY/SPINE_ENTITY sitting in the
        # registry -- re-running this script is supposed to reflect the
        # CURRENT logic's judgment, not accumulate old verdicts forever. Only
        # resets in-scope sources that HAD a value and are no longer HIGH/MEDIUM
        # this run (never touches sources outside this script's scope).
        resolved_now = {v["source_id"] for b in ("HIGH", "MEDIUM") for v in results[b]}
        stale = [src["source_id"] for src in scope if src["source_id"] not in resolved_now]
        n_retracted = 0
        if stale:
            ph = ",".join(["%s"] * len(stale))
            cur.execute(
                f"UPDATE {REGISTRY} SET GRAIN=NULL, NATURAL_KEY=NULL, SPINE_ENTITY=NULL "
                f"WHERE source_id IN ({ph}) AND GRAIN IS NOT NULL",
                tuple(stale),
            )
            n_retracted = cur.rowcount or 0

        n_written = 0
        for bucket in ("HIGH", "MEDIUM"):
            for v in results[bucket]:
                cur.execute(
                    f"UPDATE {REGISTRY} SET GRAIN=%s, NATURAL_KEY=PARSE_JSON(%s), SPINE_ENTITY=%s "
                    "WHERE source_id=%s",
                    (v["grain"], json.dumps(v["natural_key"]), v["entity"], v["source_id"]),
                )
                n_written += cur.rowcount or 0
        conn.commit()
        cur.close()
        print(f"  wrote {n_written} source(s) (HIGH+MEDIUM). retracted {n_retracted} stale "
              f"resolution(s) that are now AMBIGUOUS. AMBIGUOUS (never-resolved) left untouched.")
        return 0
    finally:
        conn.close()


def _write_report(path: Path, results: dict) -> None:
    lines = ["# Spine backfill profiling report", ""]
    lines.append(f"HIGH {len(results['HIGH'])} | MEDIUM {len(results['MEDIUM'])} | "
                  f"AMBIGUOUS {len(results['AMBIGUOUS'])} | "
                  f"NO_TABLE {len(results['NO_TABLE'])} | NO_REGISTRY_ROW {len(results['NO_REGISTRY_ROW'])}")
    lines.append("")
    for bucket in ("HIGH", "MEDIUM"):
        lines.append(f"## {bucket} ({len(results[bucket])})")
        lines.append("")
        lines.append("| source_id | spine_entity | natural_key | grain |")
        lines.append("|---|---|---|---|")
        for v in sorted(results[bucket], key=lambda x: x["source_id"]):
            entity_col = v['entity'] or "(unresolved -- grain proven, entity unknown)"
            lines.append(f"| {v['source_id']} | {entity_col} | {','.join(v['natural_key'])} | {v['grain']} |")
        lines.append("")
    lines.append(f"## AMBIGUOUS ({len(results['AMBIGUOUS'])}) -- needs a human call, never auto-written")
    lines.append("")
    lines.append("| source_id | reason | detail |")
    lines.append("|---|---|---|")
    for v in sorted(results["AMBIGUOUS"], key=lambda x: x["source_id"]):
        reason = v.get("reason", "?")
        if reason == "no-key-column":
            detail = f"ENTITY_TYPES hint: {v.get('hint') or '(none)'}"
        elif reason == "not-unique-after-dimension-search":
            base = "+".join(v.get("base_cols", []))
            dims = ", ".join(v.get("dims_tried", [])) or "(none found)"
            ratios = v.get("ratios_tried", [])
            detail = (f"base={base} key_ratio={v.get('key_ratio')} "
                      f"dims_tried=[{dims}] ratios_at_each_level={ratios}")
        elif reason == "empty-table":
            detail = f"base={'+'.join(v.get('base_cols', []))}"
        else:
            detail = json.dumps({k: x for k, x in v.items() if k not in ("source_id", "status")})
        lines.append(f"| {v['source_id']} | {reason} | {detail} |")
    lines.append("")
    for bucket, label in (("NO_TABLE", "No physical LANDING table"), ("NO_REGISTRY_ROW", "No SOURCE_REGISTRY row")):
        lines.append(f"## {label} ({len(results[bucket])})")
        lines.append("")
        for v in sorted(results[bucket], key=lambda x: x["source_id"]):
            lines.append(f"- {v['source_id']} ({v['lifecycle']})")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
