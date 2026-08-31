"""Lattice census — Hunch Engine step 1. Pure functions only.

ONE primitive: two columns (in two different tables) that normalize to the
same join key are comparable. Everything the census reports is a rollup or an
annotation of that primitive — there is deliberately NO taxonomy of
"hypothesis shapes" (Chris's rule: patterns emerge, they are never named as
categories up front).

Purity contract (locked by tests/test_hunch_census_offline.py):
  * no SQL execution, no warehouse client, no file writes — callers pass
    parsed dicts/lists in and get dicts back
  * every key->tier fact comes from portal_recon KEY_TOKENS (the single tier
    truth); every gate/prior constant comes from connect.discover — nothing
    is re-declared here, so vocabulary drift is impossible
  * VOCAB_KEYS (NAICS/SIC/NCES, ruling D17) never become lattice members;
    they are counted in blind spots as foregone comparisons
  * registry-derived facts are absent (None) offline — never fabricated

The census is FACTORED (key -> member tables), not expanded: GEO alone would
expand to tens of thousands of pair rows. `expand_pair` builds one full row on
demand; step 2 (null models) expands lazily from the same structure.
"""
from __future__ import annotations

import random
import sys
from itertools import combinations
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from connect.discover import (  # noqa: E402
    EDGE_UNIVERSE_EXCLUDE_PREFIXES,
    EDGE_UNIVERSE_EXCLUDE_TABLES,
    KEY_DOMAIN,
    MIN_POP_PCT,
    VOCAB_KEYS,
)
from connect.bridge import HARD as BRIDGE_HARD_KEYS  # noqa: E402
from connect.keys import KEY_TOKENS, SPATIAL_KEYS, TIER_RANK, join_mode  # noqa: E402
from connect.spine_entity import SPINE_ENTITY_BY_KEY  # noqa: E402
from honesty.traps import traps_for_source  # noqa: E402

# Edge-only tiers (never a per-key tier in KEY_TOKENS). BRIDGE = 2-hop through a
# measured dual-ID crosswalk; CORROBORATED here means CANDIDATE only — the real
# thing needs co-population measurement, which is a later, costed step.
BRIDGE_TIER = "BRIDGE"
CORROBORATED_TIER = "CORROBORATED"
# GEO keys a NAME can be pinned to for a corroborated-candidate (mirrors
# discover.py's NAME@ZIP-else-NAME@FIPS composite).
_CORROB_GEO_KEYS = ("ZIP", "FIPS")


def _pairs(n: int) -> int:
    """C(n, 2)."""
    return n * (n - 1) // 2


def _canon(a: str, b: str) -> tuple[str, str]:
    return (a, b) if a < b else (b, a)


# ── membership ──────────────────────────────────────────────────────────────

def build_key_membership(fingerprints: dict, min_pop_pct: float = MIN_POP_PCT) -> dict:
    """key -> {tier, mode, key_domain, members: {table: {cols, best_pct, gated}}}.

    Scope mirrors discover._scope_fingerprint (PORTAL_* + abandoned duplicates
    excluded from the lattice; they are reported via scoped_out_tables()).
    VOCAB_KEYS are excluded per D17. Fingerprint-file tier is cross-checked
    against KEY_TOKENS and a mismatch RAISES — a silently drifted tier would
    poison every rollup downstream.
    """
    membership: dict[str, dict] = {}
    for table, info in fingerprints.items():
        if table in EDGE_UNIVERSE_EXCLUDE_TABLES or table.startswith(EDGE_UNIVERSE_EXCLUDE_PREFIXES):
            continue
        for entry in info.get("keys", []):
            key = entry["key"]
            if key in VOCAB_KEYS:
                continue
            truth_tier = KEY_TOKENS.get(key, (None,))[0]
            if truth_tier is None:
                raise ValueError(f"fingerprint key {key!r} on {table} is not in KEY_TOKENS")
            if entry.get("tier") and entry["tier"] != truth_tier:
                raise ValueError(
                    f"tier drift: fingerprint says {table}.{entry['column']} {key}={entry['tier']}, "
                    f"KEY_TOKENS says {truth_tier} — refresh connect_fingerprints.json")
            slot = membership.setdefault(key, {
                "tier": truth_tier,
                "mode": join_mode(key),
                "key_domain": KEY_DOMAIN.get(key),
                "members": {},
            })
            m = slot["members"].setdefault(table, {"cols": [], "best_pct": 0.0, "gated": False})
            pct = entry.get("populated_pct")
            m["cols"].append({"col": entry["column"], "populated_pct": pct})
            if pct is not None and pct > m["best_pct"]:
                m["best_pct"] = pct
            if pct is not None and pct >= min_pop_pct:
                m["gated"] = True
    return membership


def scoped_out_tables(fingerprints: dict) -> dict:
    """Fingerprinted tables the lattice deliberately excludes, with why."""
    portal = sorted(t for t in fingerprints if t.startswith(EDGE_UNIVERSE_EXCLUDE_PREFIXES))
    abandoned = sorted(t for t in fingerprints if t in EDGE_UNIVERSE_EXCLUDE_TABLES)
    return {"portal_crawl": portal, "abandoned_duplicates": abandoned}


def vocab_banned(fingerprints: dict) -> dict:
    """D17 blind spot: per classification code, member count + foregone pairs."""
    members: dict[str, set] = {k: set() for k in sorted(VOCAB_KEYS)}
    for table, info in fingerprints.items():
        for entry in info.get("keys", []):
            if entry["key"] in members:
                members[entry["key"]].add(table)
    return {k: {"tables": len(v), "foregone_table_pairs": _pairs(len(v))}
            for k, v in members.items()}


# ── direct lattice rollups ──────────────────────────────────────────────────

def _gated_members(slot: dict) -> dict:
    return {t: m for t, m in slot["members"].items() if m["gated"]}


def summarize(membership: dict) -> dict:
    """Per-key and per-tier counts, gated and ungated side by side.

    column_pairs uses the identity sum_{a<b} c_a*c_b = (S^2 - sum(c_i^2)) / 2 —
    no pair materialization.
    """
    per_key: dict[str, dict] = {}
    for key, slot in sorted(membership.items()):
        rows = {}
        for label, mem in (("gated", _gated_members(slot)), ("ungated", slot["members"])):
            ncols = [len(m["cols"]) for m in mem.values()]
            s = sum(ncols)
            rows[label] = {
                "tables": len(mem),
                "table_pairs": _pairs(len(mem)),
                "column_pairs": (s * s - sum(c * c for c in ncols)) // 2,
            }
        per_key[key] = {"tier": slot["tier"], "spatial": key in SPATIAL_KEYS, **rows}
    per_tier: dict[str, dict] = {}
    for key, row in per_key.items():
        t = per_tier.setdefault(row["tier"], {
            "table_pairs_gated": 0, "table_pairs_ungated": 0,
            "column_pairs_gated": 0, "column_pairs_ungated": 0,
            "of_which_spatial_pairs": 0, "keys": []})
        t["keys"].append(key)
        t["table_pairs_gated"] += row["gated"]["table_pairs"]
        t["table_pairs_ungated"] += row["ungated"]["table_pairs"]
        t["column_pairs_gated"] += row["gated"]["column_pairs"]
        t["column_pairs_ungated"] += row["ungated"]["column_pairs"]
        if row["spatial"]:
            t["of_which_spatial_pairs"] += row["gated"]["table_pairs"]
    return {"per_key": per_key, "per_tier": per_tier}


def direct_pair_tiers(membership: dict) -> dict:
    """Canonical (a, b) -> strongest direct tier, gated members only.

    Materialized on purpose: the strongest-tier dedup needs per-pair identity
    and the gated lattice is small enough (hundreds of thousands max) to hold.
    Keys are iterated strongest-tier-first so the first write wins.
    """
    out: dict[tuple[str, str], str] = {}
    for key, slot in sorted(membership.items(),
                            key=lambda kv: TIER_RANK[kv[1]["tier"]]):
        for a, b in combinations(sorted(_gated_members(slot)), 2):
            out.setdefault(_canon(a, b), slot["tier"])
    return out


# ── bridges (2-hop via measured crosswalks) ─────────────────────────────────

def bridge_pairs(fingerprints: dict, membership: dict, direct: dict,
                 xref_rows: list[dict] | None = None) -> dict:
    """2-hop pairs through dual-hard-ID crosswalk tables.

    Crosswalks are derived exactly the way connect/bridge.py derives them: any
    in-scope table carrying TWO gated hard-ID keys (both in bridge.HARD) is a
    crosswalk for that key pair. pairs = gated members(key_a) x gated
    members(key_b), minus self-pairs, minus pairs already directly connected
    (a direct tier always beats BRIDGE), minus the crosswalk table itself.

    xref_rows (outputs/xref_bridges.csv) is EVIDENCE only: where the xref sweep
    measured the same crosswalk, its co-population % is carried as annotation.
    Rows with a reject_reason never annotate.
    """
    evidence = {}
    for row in (xref_rows or []):
        if (row.get("reject_reason") or "").strip():
            continue
        evidence[(row["table"], frozenset((row["key_a"], row["key_b"])))] = {
            "copop_pct": float(row["copop_pct"]) if row.get("copop_pct") else None,
            "max_fanout": int(row["max_fanout"]) if row.get("max_fanout") else None,
        }

    crosswalks, pair_set = [], set()
    for xwalk in sorted(fingerprints):
        if xwalk in EDGE_UNIVERSE_EXCLUDE_TABLES or xwalk.startswith(EDGE_UNIVERSE_EXCLUDE_PREFIXES):
            continue
        hard = sorted({
            e["key"] for e in fingerprints[xwalk].get("keys", [])
            if e["key"] in BRIDGE_HARD_KEYS and e.get("mode", "value") == "value"
            and xwalk in _gated_members(membership.get(e["key"], {"members": {}}))})
        for i in range(len(hard)):
            for j in range(i + 1, len(hard)):
                ka, kb = hard[i], hard[j]
                ma = set(_gated_members(membership.get(ka, {"members": {}})))
                mb = set(_gated_members(membership.get(kb, {"members": {}})))
                found = set()
                for a in ma:
                    for b in mb:
                        if a == b or xwalk in (a, b):
                            continue
                        p = _canon(a, b)
                        if p in direct:
                            continue
                        found.add(p)
                ev = evidence.get((xwalk, frozenset((ka, kb))), {})
                crosswalks.append({
                    "crosswalk": xwalk, "key_a": ka, "key_b": kb,
                    "copop_pct": ev.get("copop_pct"),
                    "max_fanout": ev.get("max_fanout"),
                    "pair_count": len(found),
                })
                pair_set |= found
    return {"crosswalks": crosswalks, "pairs": pair_set}


# ── corroborated candidates (NAME pinned to a shared place) ─────────────────

def corroborated_candidates(membership: dict, direct: dict) -> set:
    """Table-pairs where both sides carry a NAME key AND share a GEO pin key
    (ZIP else FIPS — mirrors discover's composite). CANDIDATES only: whether
    the names actually co-populate is unmeasurable from metadata. Pairs already
    connected by a stronger direct key are excluded.
    """
    names = set(_gated_members(membership.get("NAME", {"members": {}})))
    out: set[tuple[str, str]] = set()
    for geo_key in _CORROB_GEO_KEYS:
        geo = set(_gated_members(membership.get(geo_key, {"members": {}})))
        both = sorted(names & geo)
        for a, b in combinations(both, 2):
            p = _canon(a, b)
            if direct.get(p) in (None, "PROBABILISTIC", "GEO"):
                out.add(p)
    return out


# ── verified overlay ────────────────────────────────────────────────────────

def overlay_verified(graph: dict, direct: dict, bridges: set) -> dict:
    """Where the measured 663-edge graph sits inside the lattice."""
    lattice = set(direct) | set(bridges)
    edge_map = {_canon(e["a"], e["b"]): e for e in graph.get("edges", [])}
    inside = [p for p in edge_map if p in lattice]
    missing = sorted(p for p in edge_map if p not in lattice)
    return {
        "verified_edges": len(edge_map),
        "verified_in_lattice": len(inside),
        "verified_missing_from_lattice": missing,   # any entry = census bug
        "prior_gated_out_total": graph.get("meta", {}).get("gated_out"),
        "never_tested": len(lattice) - len(inside),
        "edge_map": edge_map,
    }


# ── sample ──────────────────────────────────────────────────────────────────

def expand_pair(a: str, b: str, key: str, membership: dict, edge_map: dict,
                provenance: str = "measured-fingerprint") -> dict:
    """One fully-expanded lattice row (the schema step 2 consumes)."""
    slot = membership.get(key, {})
    ma = slot.get("members", {}).get(a, {})
    mb = slot.get("members", {}).get(b, {})
    edge = edge_map.get(_canon(a, b))
    tier = (BRIDGE_TIER if provenance.startswith("bridge:")
            else CORROBORATED_TIER if provenance == "candidate-not-measured"
            else slot.get("tier"))
    return {
        "a": a, "b": b, "key": key, "tier": tier,
        "mode": slot.get("mode"), "spatial": key in SPATIAL_KEYS,
        "a_cols": ma.get("cols", []), "b_cols": mb.get("cols", []),
        "key_domain": slot.get("key_domain"),
        "spine_entity": SPINE_ENTITY_BY_KEY.get(key),
        "a_traps": list(traps_for_source(a)), "b_traps": list(traps_for_source(b)),
        "verified": ({"tier": edge["tier"], "matched": edge["matched"],
                      "confidence": edge["confidence"]} if edge else None),
        "time_comparable": None,        # registry pass fills; never fabricated
        "provenance": provenance,
    }


def sample_pairs(membership: dict, bridges: dict, edge_map: dict,
                 n: int, seed: int) -> list[dict]:
    """Seeded, reproducible sample of ~n expanded pairs, gated lattice only.

    Keys are weighted by their gated C(n,2) so the sample reflects the lattice's
    real shape (GEO-heavy) instead of one row per key; bridge crosswalks join
    the draw as pseudo-keys weighted by their pair counts. Draw-with-rejection
    dedups; no full materialization.
    """
    rng = random.Random(seed)
    weights: list[tuple[str, str | None, int]] = []   # (kind_key, xwalk, weight)
    for key, slot in sorted(membership.items()):
        w = _pairs(len(_gated_members(slot)))
        if w:
            weights.append((key, None, w))
    for cw in sorted(bridges["crosswalks"], key=lambda c: c["crosswalk"]):
        if cw["pair_count"]:
            weights.append((f"{cw['key_a']}~{cw['key_b']}", cw["crosswalk"], cw["pair_count"]))
    total = sum(w for _, _, w in weights)
    if not total:
        return []
    bridge_list = sorted(bridges["pairs"])
    out, seen, attempts = [], set(), 0
    while len(out) < min(n, total) and attempts < n * 50:
        attempts += 1
        pick = rng.randrange(total)
        for key, xwalk, w in weights:
            if pick < w:
                break
            pick -= w
        if xwalk is None:
            members = sorted(_gated_members(membership[key]))
            a, b = rng.sample(members, 2)
            prov, real_key = "measured-fingerprint", key
        else:
            a, b = bridge_list[rng.randrange(len(bridge_list))]
            prov, real_key = f"bridge:{xwalk}", key.split("~")[0]
        p = _canon(a, b)
        if (p, prov) in seen:
            continue
        seen.add((p, prov))
        out.append(expand_pair(p[0], p[1], real_key, membership, edge_map, prov))
    return out


# ── blind spots ─────────────────────────────────────────────────────────────

def find_blind_spots(fingerprints: dict, membership: dict, registry: dict | None) -> dict:
    """What the census could NOT compare, and why. Registry-derived entries are
    None offline — absence is stated, never guessed."""
    keyed = {t for slot in membership.values() for t in slot["members"]}
    scoped = scoped_out_tables(fingerprints)
    in_scope = {t for t in fingerprints
                if t not in EDGE_UNIVERSE_EXCLUDE_TABLES
                and not t.startswith(EDGE_UNIVERSE_EXCLUDE_PREFIXES)}
    # split the unjoinable: literally no keys vs only D17-banned vocab codes
    # (the latter are already visible in vocab_banned_d17 — no double count)
    zero_key = sorted(t for t in in_scope
                      if t not in keyed and not fingerprints[t].get("keys"))
    vocab_only = sorted(t for t in in_scope
                        if t not in keyed and fingerprints[t].get("keys"))
    trapped = sorted({t for t in keyed if traps_for_source(t)})
    reg = registry or {}
    n_time = reg.get("time_axis_tables")
    return {
        "fingerprinted_tables": len(fingerprints),
        "landing_universe": reg.get("landing_universe"),          # None offline
        "unfingerprinted_landing": reg.get("unfingerprinted_landing"),
        "marts_uncovered": reg.get("marts_uncovered"),
        "column_catalog_status": reg.get("column_catalog_status",
                                         "not probed (offline run; A16 open)"),
        "scoped_out": {k: len(v) for k, v in scoped.items()},
        "zero_key_tables": zero_key,
        "vocab_only_tables": vocab_only,
        "vocab_banned_d17": vocab_banned(fingerprints),
        "trap_flagged_members": {t: list(traps_for_source(t)) for t in trapped},
        "time_only_universe": (None if n_time is None else
                               {"tables_with_time_axis": n_time,
                                "possible_time_only_comparisons": _pairs(n_time)}),
        "declared_vs_measured_tier_disagreements": reg.get("tier_disagreements"),
        "notes": [
            "fingerprint profiler caps at 80 text columns per table; columns past "
            "the cap are invisible to this census",
            "marts are not lattice members in step 1 (no fingerprints, no registry "
            "rows); the mart universe is counted, not paired",
        ],
    }


# ── assembly ────────────────────────────────────────────────────────────────

def build_census(fingerprints: dict, graph: dict, xref_rows: list[dict],
                 sample_n: int = 20, seed: int = 20260801,
                 registry: dict | None = None) -> dict:
    membership = build_key_membership(fingerprints)
    summary = summarize(membership)
    direct = direct_pair_tiers(membership)
    bridges = bridge_pairs(fingerprints, membership, direct, xref_rows)
    corrob = corroborated_candidates(membership, direct)
    overlay = overlay_verified(graph, direct, bridges["pairs"])
    edge_map = overlay.pop("edge_map")
    sample = sample_pairs(membership, bridges, edge_map, sample_n, seed)

    tier_totals: dict[str, int] = {}
    for tier in set(direct.values()):
        tier_totals[tier] = sum(1 for t in direct.values() if t == tier)
    rollup = {
        "distinct_pairs_strongest_tier": tier_totals,
        "distinct_direct_pairs": len(direct),
        "bridge_only_pairs": len(bridges["pairs"]),
        "corroborated_candidate_pairs": len(corrob),
        "total_distinct_pairs": len(set(direct) | bridges["pairs"]),
    }
    return {
        "meta": {"seed": seed, "sample_n": sample_n,
                 "gate_min_pop_pct": MIN_POP_PCT,
                 "registry_pass": registry is not None},
        "key_membership": {
            k: {"tier": s["tier"], "mode": s["mode"], "key_domain": s["key_domain"],
                "members": s["members"]}
            for k, s in sorted(membership.items())},
        "bridges": bridges["crosswalks"],
        "summary": summary,
        "rollup": rollup,
        "verified_overlay": overlay,
        "sample": sample,
        "blind_spots": find_blind_spots(fingerprints, membership, registry),
    }


# ── report ──────────────────────────────────────────────────────────────────

_TIER_ROWS = ["STEEL", "STRONG", "GEO", "PROBABILISTIC"]


def render_report(census: dict, generated: str = "") -> str:
    """The markdown Chris reads. Numbers only from the census dict."""
    s, roll, ov = census["summary"], census["rollup"], census["verified_overlay"]
    bs = census["blind_spots"]
    L = ["# Hunch Engine — Lattice Census" + (f" ({generated})" if generated else ""), ""]
    L += ["One primitive: two columns in two tables that normalize to the same join",
          "key are comparable. Gated = both sides' key column is >= "
          f"{census['meta']['gate_min_pop_pct']}% populated (measured, not declared).", ""]
    L += ["| Tier | Table-pairs (gated) | (ungated) | Column-pairs (gated) |",
          "|---|---:|---:|---:|"]
    for tier in _TIER_ROWS:
        t = s["per_tier"].get(tier, {})
        extra = ""
        if tier == "GEO" and t.get("of_which_spatial_pairs"):
            extra = f" (of which spatial: {t['of_which_spatial_pairs']:,})"
        L.append(f"| {tier}{extra} | {t.get('table_pairs_gated', 0):,} "
                 f"| {t.get('table_pairs_ungated', 0):,} "
                 f"| {t.get('column_pairs_gated', 0):,} |")
    L.append(f"| BRIDGE (2-hop, not directly connected) | {roll['bridge_only_pairs']:,} | — | — |")
    L.append(f"| CORROBORATED candidates* | {roll['corroborated_candidate_pairs']:,} | — | — |")
    L.append("")
    L += [f"**Distinct comparable table-pairs (each counted once, at its strongest "
          f"tier): {roll['total_distinct_pairs']:,}**",
          "", "Strongest-tier split of the direct pairs: " +
          ", ".join(f"{t} {n:,}" for t, n in sorted(
              roll["distinct_pairs_strongest_tier"].items(),
              key=lambda kv: TIER_RANK.get(kv[0], 99))), "",
          f"Already verified by connect/: {ov['verified_in_lattice']:,} of "
          f"{roll['total_distinct_pairs']:,} "
          f"({ov['verified_in_lattice'] / max(roll['total_distinct_pairs'], 1):.1%}). "
          f"Previously tested and gated out as flukes: {ov['prior_gated_out_total']:,} "
          f"(aggregate; per-pair identities not persisted). "
          f"Never tested: {ov['never_tested']:,}.", ""]
    if ov["verified_missing_from_lattice"]:
        L += ["**CENSUS BUG:** verified edges missing from the lattice: "
              + ", ".join(map(str, ov["verified_missing_from_lattice"])), ""]
    L += ["*CORROBORATED candidates = both sides carry a NAME column and share a "
          "ZIP/FIPS pin. Whether the names actually co-populate is unmeasurable "
          "from metadata — measuring it is a later, costed step.", ""]

    L += ["## Random sample "
          f"(seed {census['meta']['seed']}, weighted by pair count)", ""]
    L += ["| A | B | key | tier | fill A/B | traps | verified |", "|---|---|---|---|---|---|---|"]
    for p in census["sample"]:
        fa = (f"{p['a_cols'][0]['populated_pct']:.0f}%" if p["a_cols"] else "—")
        fb = (f"{p['b_cols'][0]['populated_pct']:.0f}%" if p["b_cols"] else "—")
        traps = ", ".join(p["a_traps"] + p["b_traps"]) or "—"
        ver = "yes" if p["verified"] else "no"
        tier = p["tier"] + (" (2-hop)" if p["provenance"].startswith("bridge:") else "")
        L.append(f"| {p['a']} | {p['b']} | {p['key']} | {tier} | {fa}/{fb} | {traps} | {ver} |")
    L.append("")

    L += ["## Blind spots — what this census could NOT compare", ""]
    lu = bs["landing_universe"]
    L.append(f"- Fingerprinted tables: {bs['fingerprinted_tables']:,}. Landing universe: "
             + (f"{lu:,} → {bs['unfingerprinted_landing']:,} landing tables have no "
                "fingerprint and are invisible here." if lu is not None else
                "unknown offline (run --with-registry for the real count)."))
    if bs["marts_uncovered"] is not None:
        L.append(f"- Marts: {bs['marts_uncovered']:,} mart tables are not lattice members "
                 "(no fingerprints, no registry rows) — step-1 scope decision.")
    else:
        L.append("- Marts: not lattice members in step 1; universe uncounted offline.")
    L.append(f"- COLUMN_CATALOG: {bs['column_catalog_status']}")
    so = bs["scoped_out"]
    L.append(f"- Deliberately scoped out (mirrors connect/ edge universe): "
             f"{so['portal_crawl']:,} PORTAL_* crawl tables, "
             f"{so['abandoned_duplicates']:,} abandoned duplicates.")
    L.append(f"- Zero-key tables (fingerprinted, nothing joinable): {len(bs['zero_key_tables']):,}; "
             f"tables whose only keys are banned classification codes: {len(bs['vocab_only_tables']):,}.")
    vb = bs["vocab_banned_d17"]
    L.append("- Classification codes banned as join keys (D17): "
             + "; ".join(f"{k}: {v['tables']:,} tables, {v['foregone_table_pairs']:,} "
                         "foregone pairs" for k, v in vb.items()) + ".")
    L.append(f"- Trap-flagged lattice members (honesty/traps.py): "
             f"{len(bs['trap_flagged_members']):,} tables — "
             + ", ".join(sorted(bs["trap_flagged_members"])) + ".")
    if bs["time_only_universe"] is not None:
        tu = bs["time_only_universe"]
        L.append(f"- Time-only comparisons (two tables with a time axis, no shared key): "
                 f"{tu['tables_with_time_axis']:,} tables carry a usable time axis → "
                 f"{tu['possible_time_only_comparisons']:,} possible comparisons. "
                 "Reported as one aggregate; not lattice rows (no join axis).")
    else:
        L.append("- Time axes: unknown offline (registry SOURCE_FRESHNESS fills this).")
    if bs["declared_vs_measured_tier_disagreements"] is not None:
        L.append(f"- Declared-vs-measured join-key tier disagreements: "
                 f"{bs['declared_vs_measured_tier_disagreements']:,} sources "
                 "(registry JOIN_KEY_TIER uses a different vocabulary — appendix only).")
    for note in bs["notes"]:
        L.append(f"- {note}")
    L.append("")
    return "\n".join(L)
