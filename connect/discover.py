"""Discover the REAL connections across the whole landed Library.

Reads the fingerprints, forms candidate pairs (two tables that carry the same
live key), runs the overlap engine on each, and keeps the ones that actually
return matched rows. The result is an honest, weighted edge-list: the graph the
explorer draws.

Tiers are computed strongest-first (STEEL/STRONG/GEO/PROBABILISTIC). Name/address
("PROBABILISTIC") joins over very large tables are skipped by default and LOGGED
— never silently dropped — because fuzzy name-matching at multi-million-row scale
is slow and low-trust. Raise --name-max-rows to include them.

Output: outputs/connect_graph.json  { nodes:[...], edges:[...], meta:{...} }
"""

from __future__ import annotations

import json
from pathlib import Path

from . import db
from .fingerprint import OUT as FP_PATH
from .keys import TIER_RANK, normalize_sql, quote_ident
from .overlap import _is_lon, spatial_overlap

GRAPH_OUT = Path(__file__).resolve().parents[1] / "outputs" / "connect_graph.json"

# Set-based discovery materializes every table's distinct normalized keys here,
# then ONE self-join finds all co-occurring pairs + overlap counts -- instead of
# a live full-scan query per candidate pair (the O(n^2) crawl).
CONNECT_DB, CONNECT_SCHEMA = "LIBRARY_META", "CONNECT"   # CONNECT is reserved -> always quote
KEYSET_FQN = f'"{CONNECT_DB}"."{CONNECT_SCHEMA}"."KEYSET_SCRATCH"'

MIN_POP_PCT = 1.0          # a key must be at least this populated to count as live
NAME_MAX_ROWS = 2_000_000  # skip name/address joins when EITHER table exceeds this
SPATIAL_POINT_MAX = 100_000  # skip point-in-polygon when the point table exceeds this
SPATIAL_MAX_PAIRS = 1500     # backstop: cap spatial pair-queries so they can't explode at scale
VALUE_FANOUT_CAP = 50        # a single value shared across > this many tables is a "stopword" -- skip it
PROBABILISTIC = {"NAME", "ADDRESS"}

# --- confidence: refuse to draw a fluke. A connection isn't real just because one
# normalized value coincided. Require an absolute floor AND that the match count
# beats what random collision would produce over the key's value space. This is
# what kills the Alabama/Puerto-Rico-style phantom STEEL edge.
MIN_MATCH = 3            # value joins: at least this many matched distinct keys
MIN_MATCH_PROB = 5       # name/address: stricter (common-name noise)
COLLISION_MULT = 5.0     # matched must beat expected-by-chance by this factor
KEY_DOMAIN = {           # ~size of each key's value space, for the collision math
    "NPI": 10**10, "EIN": 10**9, "CIK": 10**7, "DUNS": 10**9, "PATENT": 10**8,
    "IMO": 10**7, "MMSI": 10**9, "UEI": 36**12, "LEI": 36**20,
    "CCN": 10**6, "NAICS": 10**6, "NCES": 10**7, "DOCKET": 10**6, "SIC": 10**4,
    "FIPS": 10**5, "ZIP": 10**5, "COUNTRY": 300,
    # Politician IDs (Step-K politics). BIOGUIDE = 1 letter + 6 digits -> 26 * 10^6.
    # ICPSR = a small integer member number (live values up to ~40k; historical span
    # comfortably inside 10^6). Honest value-space sizes so the collision math runs.
    "BIOGUIDE": 26 * 10**6, "ICPSR": 10**6,
    # DEA registrant number (2026-07-28 fix): 2 letters + 7 digits (e.g. "AB1234563",
    # keys.py NORM_RULES mode "alnum_upper") -> 26^2 * 10^7. Was wired into
    # entity_index_specs.py on 2026-06-26 but never added here -- validate_key_config()
    # has been blocking every `connect discover` run since then; the live CONNECT_EDGES
    # (11,206 rows) predates this key and was stale relative to the current spine config.
    "DEA_NO": 26**2 * 10**7,
    # --- 2026-07-30 spine wiring. Value spaces read off LIVE landing values, not
    # assumed from the ID spec, so the collision math is honest.
    # FRS_ID  -- EPA Facility Registry Service, 12-digit numeric -> 10^12.
    # PWSID   -- 2-letter state prefix + 7 digits ('FL6581003') -> 26^2 * 10^7.
    # MINE_ID -- MSHA, 7-digit numeric AFTER stripping the literal double quotes the
    #            landing values are wrapped in ('"1600354"') -> 10^7.
    # FEC_CMTE_ID / FEC_CAND_ID -- 9-char, leading letter is the committee class or
    #            the chamber, remaining 8 alphanumeric ('C00035006' / 'H0NJ07261');
    #            26 * 36^8 is the honest space. Two separate keys on purpose: a
    #            committee is an organization, a candidate is a person.
    "FRS_ID": 10**12, "PWSID": 26**2 * 10**7, "MINE_ID": 10**7,
    "FEC_CMTE_ID": 26 * 36**8, "FEC_CAND_ID": 26 * 36**8,
    # 2026-08 spine batch (staged behind keys.ENABLE_SPINE_BATCH_2026_08 -- see
    # the comment there). Value spaces read off live values, not assumed:
    # CL person ids are small integers (10^6 honest headroom); CL court ids are
    # ~2-8 char slugs from one curated registry of 3,361 courts (10^4, not
    # 36^8 -- the collision math must know the namespace is tiny and dense);
    # NPDES permit ids are 2-letter state prefix + 7 digits; NCUA charters are
    # small integers (~4.2k live, 10^5 headroom); ICE facility codes are a
    # curated roster of ~1,470 site codes (10^4).
    "CL_PERSON_ID": 10**6, "CL_COURT_ID": 10**4,
    "NPDES_ID": 26**2 * 10**7, "NCUA_CHARTER": 10**5, "ICE_FACILITY": 10**4,
    # COMPANY_NO backfill (2026-08-17): wired 2026-08-05 with NORM_RULES + specs
    # but never given a value-space here, so a COMPANY_NO edge scored through
    # the un-domained chance_free=0.9 branch -- the exact footgun
    # validate_key_config() exists to catch (it couldn't: COMPANY_NO lives in
    # EXACT_TOKEN_KEYS, which that check doesn't iterate). 8-char alphanumeric,
    # zero-padded at source -> 36^8.
    "COMPANY_NO": 36**8,
}

# D17: classification codes are NOT entity identifiers. NAICS/SIC/NCES describe
# "same industry / same school district", not "same thing" -- many orgs share one
# NAICS. Worse, the collision math above uses a THEORETICAL value space (NAICS 10^6)
# while only ~2,500 codes are actually in use, so any two industry tables overlap far
# above chance and pass the gate as false STRONG edges (~70% of the headline graph was
# this vocabulary co-occurrence). They stay tagged + in the keyset (a future
# "shared dimensions" surface can use them), but they never become graph edges.
# Mirrors connect/spine_entity.py's _CLASSIFICATION_CODES exclusion from the spine.
VOCAB_KEYS = {"NAICS", "SIC", "NCES"}

# 2026-07-28 repair pass (audit: reports/library_spine_audit_2026-07-28.md):
# CONNECT_EDGES was scanning ~456 distinct tables (fingerprint.py's landed_tables()
# is effectively "everything in LANDING") while ENTITY_INDEX only ever covers
# entity_index_specs.py's curated DISPLAY_SPECS -- 98.2% of edges referenced a
# table the entity layer never indexed. Two causes, filtered here (not in
# fingerprint.py, which stays a broad diagnostic tool -- only edge GENERATION
# narrows scope):
#   1. PORTAL_* tables (367 of the 426 orphaned tables) -- the open "finish or
#      prune the portal crawl" question from the 2026-07-27 table-inventory
#      audit, deliberately left unresolved. Excluded from edges until decided.
#   2. Raw tables already flagged in that same audit as abandoned duplicates,
#      superseded by a canonical table that IS in DISPLAY_SPECS -- generating
#      edges against a stale duplicate just recreates the mart-layer confusion
#      one level down in the raw layer.
EDGE_UNIVERSE_EXCLUDE_PREFIXES = ("PORTAL_",)
EDGE_UNIVERSE_EXCLUDE_TABLES = {
    # FED_FEC_BULK is a GENUINE duplicate and stays excluded: verified 2026-07-30, its
    # 18 columns are byte-identical to FED_FEC_BULK_COMMITTEES minus CYCLE, so the
    # _COMMITTEES table strictly supersedes it.
    "FED_FEC_BULK",
    # FED_FEC_BULK_CANDIDATES and _COMMITTEES were REMOVED from this set on 2026-07-30
    # for the same reason as the USASPENDING entry below: reason #2 above only justifies
    # excluding a table "superseded by a canonical table that IS in DISPLAY_SPECS", and
    # NO FEC table was in DISPLAY_SPECS at all. They are also not duplicates of each
    # other -- one is the candidate master (CAND_ID, office, party, district), the other
    # the committee master (FEC_CMTE_ID, treasurer, committee type). A candidate is a
    # person; a committee is an organization. Both are now wired to the spine.
    # FED_USASPENDING_ASSISTANCE_FULL was REMOVED from this set on 2026-07-30. It was
    # never actually a duplicate: reason #2 above says "superseded by a canonical table
    # that IS in DISPLAY_SPECS", and there is NO federal-assistance table in
    # DISPLAY_SPECS -- only FED_USASPENDING_CONTRACTS. Contracts (procurement: the
    # government buys a thing) and assistance (grants and loans: the government funds
    # an organization) are different money with different recipients. Verified live:
    # the table carries 223,721 distinct recipient UEIs, of which 175,699 appear
    # NOWHERE in the spine (which held only 152,895 UEIs total), so excluding it was
    # hiding the single largest new-entity population available. Now wired.
    # NOTE the trap it also revealed: recipient_uei reads as 100% non-null, but 61% of
    # rows are EMPTY STRINGS -- 7.8M joinable rows, not 19.9M. COUNT(col) lies here
    # exactly as CLAUDE.md section 7 warns.
    "FED_USASPENDING_CONTRACTS_FULL",   # genuine duplicate of the spine's _CONTRACTS
    "FED_USASPENDING_BULK",
    "FED_IRS_EO_PR", "FED_CMS_HOSPITAL_COMPARE",
    "FED_SEC_EDGAR", "FED_US_SEC_EDGAR",  # already self-documented as stale below in entity_index_specs.py
}


def _scope_fingerprint(fp: dict) -> dict:
    """Narrow the edge-discovery candidate universe to non-portal, non-abandoned
    tables (see EDGE_UNIVERSE_EXCLUDE_* above). fingerprint.py's own output/report
    stays untouched and broad for diagnostics -- only the persisted CONNECT_EDGES
    graph built from it is scoped."""
    return {
        t: info for t, info in fp.items()
        if t not in EDGE_UNIVERSE_EXCLUDE_TABLES
        and not t.startswith(EDGE_UNIVERSE_EXCLUDE_PREFIXES)
    }


def validate_key_config() -> None:
    """Fail LOUD if a value key is half-configured -- the Step-K footgun.

    Adding a new join key takes coordinated edits in several files. Miss the
    KEY_DOMAIN entry here and ``confidence()`` silently falls through to the
    ``chance_free = 0.9`` branch (meant for spatial, where geometry already
    verifies the match) -- so the new key would pass random collisions as
    high-confidence STEEL edges. Miss the NORM_RULES entry and ``normalize_sql``
    raises mid-run. Catch both up front, before any Snowflake work.

    Every STEEL/STRONG value key MUST have a NORM_RULES entry (to canonicalize)
    AND a KEY_DOMAIN entry (so the collision math runs). PROBABILISTIC keys
    (NAME/ADDRESS) are intentionally exempt -- they're scored separately and never
    use the value-space collision model. Spatial keys (LATLON/GEOM) don't reach
    this path. Run at the top of run().
    """
    from .keys import KEY_TOKENS, NORM_RULES
    SPATIAL = {"LATLON", "GEOM"}
    missing: list[str] = []
    for key, (tier, _toks) in KEY_TOKENS.items():
        if tier not in ("STEEL", "STRONG") or key in SPATIAL:
            continue
        if key not in NORM_RULES:
            missing.append(f"{key} ({tier}): no NORM_RULES entry in connect/keys.py")
        if key not in KEY_DOMAIN:
            missing.append(f"{key} ({tier}): no KEY_DOMAIN entry in connect/discover.py "
                           "(would silently get chance_free=0.9 with no collision guard)")
    if missing:
        raise ValueError(
            "Join-key config is incomplete -- finish the Step-K edits before wiring:\n  "
            + "\n  ".join(missing))


def confidence(key, tier, a_distinct, b_distinct, matched):
    """Return (score 0-1, keep?). A coincidental handful of matches on a short
    numeric key scores ~0 and is dropped; a dense overlap on a hard ID scores ~1."""
    if matched <= 0:
        return 0.0, False
    if key in VOCAB_KEYS:                    # D17: classification code, not an entity link
        return 0.0, False
    floor = MIN_MATCH_PROB if tier in ("PROBABILISTIC", "CORROBORATED") else MIN_MATCH
    if matched < floor:
        return 0.0, False
    if a_distinct <= 0 or b_distinct <= 0:
        return 0.0, False
    cover = matched / min(a_distinct, b_distinct)      # coverage of the smaller set
    # STEEL keys are globally unique identifiers (EIN, NPI, IMO, CIK, etc.)
    # Skip the collision-chance gate, but require a minimum evidence floor to
    # exclude sentinel/masked-value traps (e.g. 'PENDING' EINs).
    if tier == "STEEL" and key not in VOCAB_KEYS:
        if matched >= 25 or cover >= 0.01:
            score = 0.4 + 0.6 * min(cover, 1.0)
            return round(min(score, 1.0), 3), True
        # Below floor: fall through to normal collision gate
    dom = KEY_DOMAIN.get(key)
    if dom:
        expected = (a_distinct * b_distinct) / dom          # ~random collisions over the value space
        if matched < COLLISION_MULT * expected:             # indistinguishable from chance -> drop
            return round(matched / (matched + expected + 1e-9), 3), False
        chance_free = matched / (matched + expected)        # fraction of matches not explained by chance
    elif tier == "CORROBORATED":
        chance_free = 0.85                                  # name pinned to a place -> trustworthy
    elif key in PROBABILISTIC:
        chance_free = 0.5                                   # name/address alone: unscored -> medium-low
    else:
        # Spatial only (GEO_IN): geometry already verifies the match. A VALUE key can
        # never reach here un-domained -- validate_key_config() refuses to run() with a
        # STEEL/STRONG key missing from KEY_DOMAIN, so it'd be caught long before this.
        chance_free = 0.9
    score = chance_free * (0.4 + 0.6 * min(cover, 1.0))     # reward covering the smaller set (subset joins)
    if tier == "PROBABILISTIC":
        score *= 0.5
    return round(min(score, 1.0), 3), True

# table -> investigation domain (drives node color in the explorer). Prefix fallback.
DOMAIN_KEYWORDS = [
    ("health", ("CMS", "CLINICAL", "FDA", "NPPES", "HCRIS", "OIG_LEIE", "HHS")),
    ("justice", ("DOJ", "FJC", "SCDB", "OYEZ", "HUDOC", "NAAG", "CRT")),
    ("economics", ("SEC", "TREASURY", "FDIC", "EDGAR", "ISTAT", "EMBER")),
    ("foreign_influence", ("FARA",)),
    ("governance", ("REVOLVINGDOOR", "USASPENDING", "FEDERAL_REGISTER")),
    ("maritime", ("NOAA", "AIS")),
    ("hazards", ("USGS", "EARTHQUAKE")),
    ("housing", ("MAPPING_INEQUALITY",)),
    ("corporate_registry", ("ZEFIX", "BORME", "GEMI", "CRO", "SERCOP")),
    ("history", ("SLAVE", "WPA", "NARA", "WAYBACK", "EPSTEIN", "BIORXIV", "WIKIPEDIA")),
]


def domain_of(table: str) -> str:
    t = table.upper()
    for dom, kws in DOMAIN_KEYWORDS:
        if any(k in t for k in kws):
            return dom
    return "other"


def _best_value_col(keys: list[dict], key: str) -> dict | None:
    cands = [k for k in keys if k["key"] == key and k["mode"] == "value"
             and k["populated_pct"] >= MIN_POP_PCT]
    return max(cands, key=lambda k: k["distinct"]) if cands else None


def _latlon_cols(keys: list[dict]) -> tuple[str, str] | None:
    ll = [k["column"] for k in keys if k["key"] == "LATLON" and k["populated_pct"] >= MIN_POP_PCT]
    lat = next((c for c in ll if not _is_lon(c)), None)
    lon = next((c for c in ll if _is_lon(c)), None)
    return (lat, lon) if lat and lon else None


def _geom_col(keys: list[dict]) -> str | None:
    cands = [k for k in keys if k["key"] == "GEOM" and k["nonnull"] > 0]
    return max(cands, key=lambda k: k["nonnull"])["column"] if cands else None


def _wgs84_poly_tables(conn, poly_raw: dict) -> dict:
    """Keep only geometry tables that parse as WGS84 lon/lat GEOGRAPHY. Projected
    coordinate systems (state-plane, huge x/y) make TO_GEOGRAPHY throw -- test each
    table ONCE here and skip the bad ones, instead of erroring on every spatial pair."""
    good = {}
    for t, geom in poly_raw.items():
        qi = quote_ident(geom)
        try:
            ok = db.scalar(conn, f"""
                SELECT COUNT(*) FROM (
                    SELECT TRY_TO_GEOGRAPHY({qi}) AS g FROM {db.fqn(t)}
                    WHERE {qi} IS NOT NULL LIMIT 50
                ) WHERE g IS NOT NULL""")
        except Exception:
            ok = 0
        if ok and int(ok) > 0:
            good[t] = geom
        else:
            print(f"  [skip spatial-poly] {t}: geometry not WGS84/parseable")
    return good


def run(name_max_rows: int = NAME_MAX_ROWS, write: bool = True,
        bridge_on: bool = True, fanout_max: int = 40) -> dict:
    validate_key_config()   # fail loud on a half-added Step-K key BEFORE any Snowflake work
    fp = _scope_fingerprint(json.loads(FP_PATH.read_text()))
    conn = db.connect()
    tested = skipped = gated = 0
    edges: list[dict] = []
    bridge_stats: dict = {}

    try:
        # ---- value-key connections (set-based: keyset table + one self-join) --
        v_edges, v_gated, v_skipped, v_tested = _value_edges_bulk(conn, fp, name_max_rows)
        edges += v_edges
        gated += v_gated
        skipped += v_skipped
        tested += v_tested

        # ---- spatial (point-in-polygon): WGS84 geometry only, hard-capped --
        pt_tables = {t: ll for t, info in fp.items()
                     if (ll := _latlon_cols(info["keys"])) and info["rows"] <= SPATIAL_POINT_MAX}
        poly_tables = _wgs84_poly_tables(
            conn, {t: g for t, info in fp.items() if (g := _geom_col(info["keys"]))})
        print(f"  [spatial] {len(pt_tables)} point tables x {len(poly_tables)} WGS84 polygon tables")
        sp = 0
        for pt, (lat, lon) in pt_tables.items():
            if sp >= SPATIAL_MAX_PAIRS:
                break
            for poly, geom in poly_tables.items():
                if pt == poly:
                    continue
                if sp >= SPATIAL_MAX_PAIRS:
                    print(f"  [cap] spatial reached {SPATIAL_MAX_PAIRS} pairs; skipping the rest")
                    break
                sp += 1
                tested += 1
                try:
                    ov = spatial_overlap(conn, pt, lat, lon, poly, geom)
                except Exception as e:
                    print(f"  [err] spatial {pt} in {poly}: {str(e)[:60]}")
                    continue
                if ov["matched"] > 0:
                    conf, keep = confidence("GEO_IN", "GEO", ov["a_distinct"], ov["b_distinct"], ov["matched"])
                    if keep:
                        edges.append(_edge(pt, poly, "GEO_IN", "GEO", f"{lat}/{lon}", geom, ov, conf))
                    else:
                        gated += 1

        # ---- bridged (transitive) connections through dual-key crosswalk tables --
        bridge_stats: dict = {}
        if bridge_on:
            from . import bridge
            direct_pairs = {frozenset((e["a"], e["b"])) for e in edges}
            try:
                bridged, bridge_stats = bridge.discover_bridged(conn, fp, direct_pairs, fanout_max=fanout_max)
                edges += bridged
                tested += bridge_stats.get("crosswalk_pairs", 0)
                gated += bridge_stats.get("gated", 0)
            except Exception as ex:
                print(f"  [bridge] failed (skipping): {str(ex)[:120]}")
    finally:
        conn.close()

    nodes = [{
        "id": t,
        "rows": info["rows"],
        "domain": domain_of(t),
        "keys": sorted({k["key"] for k in info["keys"] if k["populated_pct"] >= MIN_POP_PCT}),
    } for t, info in fp.items()]

    by_tier: dict = {}
    for e in edges:
        by_tier[e["tier"]] = by_tier.get(e["tier"], 0) + 1

    graph = {
        "meta": {"pairs_tested": tested, "pairs_skipped": skipped, "gated_out": gated,
                 "edges": len(edges), "name_max_rows": name_max_rows,
                 "by_tier": by_tier, "bridge": bridge_stats},
        "nodes": nodes,
        "edges": sorted(edges, key=lambda e: (-e.get("confidence", 0), -e["matched"])),
    }
    tier_str = ", ".join(f"{t}={n}" for t, n in sorted(by_tier.items(), key=lambda x: -x[1]))
    print(f"\n{len(edges)} real connections kept ({gated} flukes gated out) "
          f"from {tested} pairs tested ({skipped} skipped).")
    print(f"  by tier: {tier_str}")
    if write:
        GRAPH_OUT.write_text(json.dumps(graph, indent=2))
        print(f"wrote {GRAPH_OUT}")
        # persist the SAME edges to Snowflake so the graph is queryable from SQL
        # (and therefore evidence.dev), not just the gitignored JSON projection.
        # Lazy import: store imports discover, so a top-level import would cycle.
        import uuid
        from . import store
        wconn = db.connect()
        try:
            n = store.write_edges(wconn, graph["edges"], uuid.uuid4().hex[:16])
            print(f"wrote {n:,} edges -> {store.cfqn(store.EDGES_TABLE)}")
        except Exception as ex:   # never lose the JSON write over a Snowflake hiccup
            print(f"  [edges] Snowflake write failed (JSON still written): {str(ex)[:160]}")
        finally:
            wconn.close()
    return graph


# --- set-based value discovery ---------------------------------------------- #
def _build_keysets(conn, fp, name_max_rows) -> tuple[dict, int]:
    """Materialize every table's DISTINCT normalized keys into ONE scratch table.
    Returns {(table,key): (column, tier)} and the count of skipped name-keysets.
    One INSERT per (table,key) -- linear in tables, not pairs."""
    db.rows(conn, f'CREATE SCHEMA IF NOT EXISTS "{CONNECT_DB}"."{CONNECT_SCHEMA}"')
    db.rows(conn, f"CREATE OR REPLACE TRANSIENT TABLE {KEYSET_FQN} "
                  f"(table_name STRING, key STRING, val STRING)")
    members, skipped = {}, 0
    for tbl, info in fp.items():
        seen = set()
        for k in info["keys"]:
            key = k["key"]
            if k["mode"] != "value" or key in seen:
                continue
            best = _best_value_col(info["keys"], key)
            if not best:
                continue
            seen.add(key)
            if key in PROBABILISTIC:
                # D-name-gate: bare NAME/ADDRESS alone is never trustworthy at scale.
                # Only the corroborated composite (NAME@ZIP, NAME@FIPS) emits edges.
                skipped += 1
                continue
            if key == "DOCKET" and tbl.startswith("PORTAL_"):
                # Docket numbers are court-local (cv-00001 exists in every district).
                # Curated federal court sources (Oyez/SCDB use unique SCOTUS dockets)
                # can still match; portal docket columns are untrusted and collide.
                skipped += 1
                continue
            members[(tbl, key)] = (best["column"], _tier(fp, key))
            # ZIP country-gate (Chris 2026-08-09): if this table also carries a
            # country column, foreign-country rows contribute no ZIP keys.
            ccol = _best_value_col(info["keys"], "COUNTRY") if key == "ZIP" else None
            norm = normalize_sql(key, quote_ident(best["column"]),
                                 country_col=quote_ident(ccol["column"]) if ccol else None)
            db.rows(conn, f"INSERT INTO {KEYSET_FQN} "
                          f"SELECT DISTINCT '{tbl}', '{key}', {norm} "
                          f"FROM {db.fqn(tbl)} WHERE {norm} IS NOT NULL")

        # --- corroborated composite key: NAME pinned to a place (ZIP, else FIPS).
        # A name alone is noise ("JOHN SMITH"); a name + the same ZIP is a real
        # entity match. It's selective, so it runs at ANY table size (no name cap)
        # and unlocks the 379 NAME x 338 ZIP tables without the false-positive swamp.
        name_col = _best_value_col(info["keys"], "NAME")
        for geo in ("ZIP", "FIPS"):
            geo_col = _best_value_col(info["keys"], geo)
            if name_col and geo_col:
                ck = f"NAME@{geo}"
                nexpr = normalize_sql("NAME", quote_ident(name_col["column"]))
                ccol = _best_value_col(info["keys"], "COUNTRY") if geo == "ZIP" else None
                gexpr = normalize_sql(geo, quote_ident(geo_col["column"]),
                                      country_col=quote_ident(ccol["column"]) if ccol else None)
                members[(tbl, ck)] = (f"{name_col['column']}+{geo_col['column']}", "CORROBORATED")
                db.rows(conn, f"INSERT INTO {KEYSET_FQN} "
                              f"SELECT DISTINCT '{tbl}', '{ck}', {nexpr} || '|' || {gexpr} "
                              f"FROM {db.fqn(tbl)} WHERE {nexpr} IS NOT NULL AND {gexpr} IS NOT NULL")
                break   # one composite per table (prefer ZIP) to bound the keyset
    return members, skipped


def _value_edges_bulk(conn, fp, name_max_rows) -> tuple[list, int, int, int]:
    members, skipped = _build_keysets(conn, fp, name_max_rows)
    if not members:
        return [], 0, skipped, 0

    counts = {(r["TABLE_NAME"], r["KEY"]): int(r["ND"])
              for r in db.dicts(conn, f"SELECT table_name, key, COUNT(*) nd FROM {KEYSET_FQN} GROUP BY 1, 2")}

    # ONE self-join: all co-occurring (table_a, table_b) pairs per key + overlap + a sample.
    # D-fanout: exclude "stopword" values that appear in too many tables for a given key.
    # Without this, a hot ZIP shared across 1,500 portal tables generates ~1M pairs.
    pairs = db.dicts(conn, f"""
        WITH capped AS (
            SELECT key, val, table_name
            FROM {KEYSET_FQN}
            QUALIFY COUNT(DISTINCT table_name) OVER (PARTITION BY key, val) <= {VALUE_FANOUT_CAP}
        )
        SELECT a.key AS jkey, a.table_name AS ta, b.table_name AS tb,
               COUNT(*) AS matched,
               ARRAY_SLICE(ARRAY_AGG(a.val), 0, 4) AS samp
        FROM capped a
        JOIN capped b ON a.key = b.key AND a.val = b.val AND a.table_name < b.table_name
        GROUP BY 1, 2, 3
        HAVING COUNT(*) >= {MIN_MATCH}
    """)

    edges, gated = [], 0
    for r in pairs:
        key, ta, tb, matched = r["JKEY"], r["TA"], r["TB"], int(r["MATCHED"])
        a_d, b_d = counts.get((ta, key), 0), counts.get((tb, key), 0)
        col_a, tier = members.get((ta, key), ("", "PROBABILISTIC"))
        col_b = members.get((tb, key), ("", ""))[0]
        conf, keep = confidence(key, tier, a_d, b_d, matched)
        if not keep:
            gated += 1
            continue
        samp = r["SAMP"]
        samp = json.loads(samp) if isinstance(samp, str) else (samp or [])
        ov = {"mode": "value", "a_distinct": a_d, "b_distinct": b_d, "matched": matched,
              "match_rate": round(matched / (min(a_d, b_d) or 1) * 100, 1), "sample": samp[:4]}
        edges.append(_edge(ta, tb, key, tier, col_a, col_b, ov, conf))
    print(f"  [value] {len(edges)} kept / {gated} gated from {len(pairs)} co-occurring pairs (set-based)")
    return edges, gated, skipped, len(pairs)


# --- small helpers ---------------------------------------------------------- #
def _tier(fp: dict, key: str) -> str:
    from .keys import KEY_TOKENS
    return KEY_TOKENS.get(key, ("PROBABILISTIC",))[0]


def _edge(a, b, key, tier, a_col, b_col, ov, conf) -> dict:
    return {
        "a": a, "b": b, "key": key, "tier": tier,
        "a_col": a_col, "b_col": b_col,
        "mode": ov["mode"], "matched": ov["matched"],
        "a_distinct": ov["a_distinct"], "b_distinct": ov["b_distinct"],
        "match_rate": ov["match_rate"], "confidence": conf,
        "sample": ov.get("sample", []),
    }


if __name__ == "__main__":
    run()
