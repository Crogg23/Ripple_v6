"""Hunch sieve CLI — score the lattice, stage by stage, into HYPOTHESIS_CATALOG.

What it does, in order:
  1. Builds the gated lattice from fmt-2 fingerprints (hunch/census.py) and
     scores every direct pair against the null (hunch/score.py, hunch/sieve.py).
     Metadata stage is FREE — no warehouse compute.
  2. --measure runs the live matched-count query for each unmeasured
     STEEL/STRONG pair on the guarded READ lane (one distinct-join each,
     ~150 queries; GEO/PROBABILISTIC measurement is a later, separately
     costed stage — this script refuses to measure them today).
  3. Preview (default) prints the ranked feed head + band counts and writes
     NOTHING anywhere. --apply writes rows to
     LIBRARY_META.REGISTRY.HYPOTHESIS_CATALOG on the standard loader lane.

Guards, in order:
  1. Requires fmt-2 fingerprints (range data) — refuses on the old format,
     pointing at the sweep command. Before any credential is touched.
  2. --apply DELETEs only rows with VERDICT IS NULL and never inserts a
     (pair, key) that still carries a human verdict — verdicts are sacred,
     the sieve regenerates everything else.
  3. Loader lane import is deferred until after --apply (same discipline as
     build_column_catalog.py).

Usage:
  python scripts/hunch_sieve.py                      # metadata stage, preview
  python scripts/hunch_sieve.py --measure            # + live hard-ID counts (read lane)
  python scripts/hunch_sieve.py --measure --apply    # write the catalog
"""
from __future__ import annotations

import argparse
import json
import sys
import uuid
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from hunch import census, sieve  # noqa: E402
from hunch.sieve import best_col_entry  # noqa: E402

FINGERPRINTS = REPO / "outputs" / "connect_fingerprints.json"
GRAPH = REPO / "outputs" / "connect_graph.json"
MEASURED_CACHE = REPO / "outputs" / "hunch_measured.json"
ABSENCE_CACHE = REPO / "outputs" / "hunch_absence_verdicts.json"
CATALOG_FQN = 'LIBRARY_META.REGISTRY.HYPOTHESIS_CATALOG'
HARD_TIERS = ("STEEL", "STRONG")

COLS = ["PAIR_A", "PAIR_B", "KEY", "TIER", "A_COL", "B_COL", "A_DISTINCT",
        "B_DISTINCT", "MATCHED", "EXPECTED_CHANCE", "S_CHANCE", "BAND",
        "COVERAGE", "RANGE_REASON", "ABSENCE_VALID", "EXPECTED_FLUKES",
        "PROMOTABLE", "SAME_FAMILY", "TRAPS", "VERIFIED_TIER", "STAGE",
        "SCAFFOLD_SQL", "RUN_ID"]


def scaffold_sql(a: str, b: str, a_col: str, b_col: str, key: str) -> str:
    """The click-to-scaffold query the Hunches room will hand the SQL editor.
    Spatial keys (LATLON/GEOM) have no value normalizer by design — their
    scaffold is a bounding-box sketch pointing at the spatial layer."""
    from connect.keys import SPATIAL_KEYS, normalize_sql, quote_ident
    if key in SPATIAL_KEYS:
        return (f"-- spatial pairing ({key}): equi-join does not apply.\n"
                f"-- connect/overlap.py is the measured spatial path; sketch:\n"
                f"SELECT a.*, b.*\nFROM LIBRARY_RAW.LANDING.{a} a\n"
                f"JOIN LIBRARY_RAW.LANDING.{b} b\n"
                f"  ON ST_DWITHIN(TO_GEOGRAPHY(a.{quote_ident(a_col)}), "
                f"TO_GEOGRAPHY(b.{quote_ident(b_col)}), 1000)\nLIMIT 100")
    na = normalize_sql(key, "a." + quote_ident(a_col))
    nb = normalize_sql(key, "b." + quote_ident(b_col))
    return (f"SELECT a.*, b.*\nFROM LIBRARY_RAW.LANDING.{a} a\n"
            f"JOIN LIBRARY_RAW.LANDING.{b} b\n  ON {na} = {nb}\nLIMIT 100")


def measure_hard_pairs(membership: dict, fingerprints: dict, edge_map: dict,
                       cache: dict) -> dict:
    """Live matched counts for unmeasured STEEL/STRONG pairs, read lane.
    Cache keyed 'A|B|KEY' in outputs/hunch_measured.json so re-runs are free."""
    from dotenv import load_dotenv
    load_dotenv(REPO / "library-onboarding" / ".env", override=True)
    from connect.keys import normalize_sql, quote_ident
    from viz import sqlrun

    todo = []
    for key, slot in sorted(membership.items()):
        if slot["tier"] not in HARD_TIERS:
            continue
        gated = sorted(census._gated_members(slot))
        for i, a in enumerate(gated):
            for b in gated[i + 1:]:
                ck = f"{a}|{b}|{key}"
                if ck in cache or sieve.edge_matched(edge_map, a, b, key) is not None:
                    continue
                todo.append((a, b, key, ck))
    print(f"measuring {len(todo)} unmeasured hard-ID pairs on the read lane ...")
    for n, (a, b, key, ck) in enumerate(todo, 1):
        ca = best_col_entry(membership, key, a, fingerprints)["column"]
        cb = best_col_entry(membership, key, b, fingerprints)["column"]
        na, nb = normalize_sql(key, quote_ident(ca)), normalize_sql(key, quote_ident(cb))
        sql = (f"WITH xa AS (SELECT DISTINCT {na} AS v FROM LIBRARY_RAW.LANDING.{a} "
               f"WHERE {na} IS NOT NULL), "
               f"xb AS (SELECT DISTINCT {nb} AS v FROM LIBRARY_RAW.LANDING.{b} "
               f"WHERE {nb} IS NOT NULL) "
               f"SELECT COUNT(*) AS M FROM xa JOIN xb ON xa.v = xb.v")
        try:
            df, _ = sqlrun.run(sql)
            cache[ck] = int(df.iloc[0, 0])
            print(f"  [{n}/{len(todo)}] {a} x {b} [{key}] matched={cache[ck]:,}", flush=True)
        except Exception as exc:
            print(f"  [{n}/{len(todo)}] FAIL {a} x {b} [{key}]: {str(exc)[:100]}", flush=True)
        if n % 10 == 0:
            MEASURED_CACHE.write_text(json.dumps(cache, indent=1))
    MEASURED_CACHE.write_text(json.dumps(cache, indent=1))
    return cache


def verify_absences(rows: list[dict], membership: dict, fingerprints: dict) -> None:
    """Second-layer absence check (read lane), TWO histograms per pair:

    1. full-value buckets — catches high-order partitions (per-court dockets);
    2. suffix buckets (the digits AFTER the 2-char prefix, fixed-width keys
       only) — catches low-order partitions. CCN taught us this twice: the
       high digits are the STATE (shared by everyone), the facility-type
       partition lives in the low digits, so a full-range histogram buckets
       by state and calls a structurally impossible overlap "credible".

    Partitioned if EITHER histogram pair is disjoint. Rebands to S=0;
    sparse/non-numeric stays flagged, never silently confirmed.
    """
    from dotenv import load_dotenv
    load_dotenv(REPO / "library-onboarding" / ".env", override=True)
    from connect.keys import NORM_RULES, normalize_sql, quote_ident
    from hunch import score as hscore
    from viz import sqlrun

    todo = [r for r in rows if r["band"] == "absence"]
    if not todo:
        return
    vcache = json.loads(ABSENCE_CACHE.read_text()) if ABSENCE_CACHE.exists() else {}

    def hist(tbl, col, key, expr_of):
        nx = normalize_sql(key, quote_ident(col))
        expr, lo, hi = expr_of(nx)
        sql = (f"SELECT WIDTH_BUCKET({expr}, {lo}, {hi}, 40) AS B, "
               f"COUNT(DISTINCT {nx}) AS N FROM LIBRARY_RAW.LANDING.{tbl} "
               f"WHERE {nx} IS NOT NULL AND {expr} IS NOT NULL GROUP BY 1")
        df, _ = sqlrun.run(sql)
        return {int(b): int(n) for b, n in zip(df.iloc[:, 0], df.iloc[:, 1])}

    def apply(r, v, layer):
        r["range_reason"] += f" | {layer}: {v['reason']}"
        if v["verdict"] == "partitioned":
            r.update({"band": "partitioned", "s_chance": 0.0,
                      "absence_valid": False, "promotable": False})

    print(f"verifying {len(todo)} absence-band pairs (full + suffix histograms) ...",
          flush=True)
    n_done = 0
    for r in todo:
        ck = f"v2|{r['pair_a']}|{r['pair_b']}|{r['key']}"
        if ck in vcache:
            apply(r, vcache[ck], vcache[ck].get("layer", "histogram"))
            continue
        a_e = best_col_entry(membership, r["key"], r["pair_a"], fingerprints)
        b_e = best_col_entry(membership, r["key"], r["pair_b"], fingerprints)
        try:
            lo = min(float(a_e["min"]), float(b_e["min"]))
            hi = max(float(a_e["max"]), float(b_e["max"])) + 1
        except (TypeError, ValueError):
            r["range_reason"] += " | absence unverified (non-numeric key)"
            continue
        sides = ((r["pair_a"], a_e["column"]), (r["pair_b"], b_e["column"]))
        mode, width = NORM_RULES.get(r["key"], ("", 0))
        layers = [("full-hist", lambda nx: (f"TRY_TO_NUMBER({nx})", lo, hi))]
        if mode == "pad" and width >= 4:
            sfx = width - 2
            layers.append(("suffix-hist",
                           lambda nx, s=sfx: (f"TRY_TO_NUMBER(RIGHT({nx}, {s}))",
                                              0, 10 ** s)))
        verdict = None
        try:
            for layer, expr_of in layers:
                ha = hist(sides[0][0], sides[0][1], r["key"], expr_of)
                hb = hist(sides[1][0], sides[1][1], r["key"], expr_of)
                v = hscore.verify_absence(ha, hb)
                verdict = {"verdict": v["verdict"], "reason": v["reason"], "layer": layer}
                if v["verdict"] == "partitioned":
                    break
        except Exception as exc:
            r["range_reason"] += f" | absence unverified ({str(exc)[:60]})"
            print(f"  FAIL {r['pair_a']} x {r['pair_b']} [{r['key']}]: "
                  f"{str(exc)[:90]}", flush=True)
            continue
        vcache[ck] = verdict
        apply(r, verdict, verdict["layer"])
        n_done += 1
        if n_done % 10 == 0:
            ABSENCE_CACHE.write_text(json.dumps(vcache, indent=1))
        print(f"  {r['pair_a']} x {r['pair_b']} [{r['key']}]: "
              f"{verdict['verdict']} ({verdict['layer']})", flush=True)
    ABSENCE_CACHE.write_text(json.dumps(vcache, indent=1))


def write_catalog(rows: list[dict]) -> int:
    """Idempotent write on the loader lane: clear unverdicted rows, keep
    verdicted (pair, key) rows untouched, insert the rest."""
    sys.path.insert(0, str(REPO / "library-onboarding"))
    import snow
    conn = snow.connect()
    try:
        cur = conn.cursor()
        try:
            cur.execute(f"SELECT PAIR_A, PAIR_B, \"KEY\" FROM {CATALOG_FQN} "
                        "WHERE VERDICT IS NOT NULL")
            verdicted = {(a, b, k) for a, b, k in cur.fetchall()}
            cur.execute(f"DELETE FROM {CATALOG_FQN} WHERE VERDICT IS NULL")
            todo = [r for r in rows
                    if (r["pair_a"], r["pair_b"], r["key"]) not in verdicted]
            if verdicted:
                print(f"  keeping {len(verdicted)} verdicted rows untouched; "
                      f"skipping their re-insert")
            ph = ", ".join(["%s"] * (len(COLS) - 0))
            # TRAPS is ARRAY -> PARSE_JSON on a VARCHAR bind
            select_cols = []
            for c in COLS:
                select_cols.append(f"PARSE_JSON(COLUMN{len(select_cols)+1})::ARRAY"
                                   if c == "TRAPS" else f"COLUMN{len(select_cols)+1}")
            params, values_rows = [], []
            for r in rows:
                if (r["pair_a"], r["pair_b"], r["key"]) in verdicted:
                    continue
                values_rows.append(f"({ph})")
                params.extend([
                    r["pair_a"], r["pair_b"], r["key"], r["tier"], r["a_col"],
                    r["b_col"], r["a_distinct"], r["b_distinct"], r["matched"],
                    r["expected_chance"], r["s_chance"], r["band"], r["coverage"],
                    r["range_reason"], r["absence_valid"], r["expected_flukes"],
                    r["promotable"], r["same_family"], json.dumps(r["traps"]),
                    r["verified_tier"], r["stage"], r["scaffold_sql"], r["run_id"]])
            if values_rows:
                cur.execute(
                    f"INSERT INTO {CATALOG_FQN} ({', '.join(chr(34)+c+chr(34) for c in COLS)}) "
                    f"SELECT {', '.join(select_cols)} FROM VALUES {', '.join(values_rows)}",
                    params)
            return len(values_rows)
        finally:
            cur.close()
    finally:
        conn.close()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--measure", action="store_true",
                    help="live matched counts for unmeasured STEEL/STRONG pairs (read lane)")
    ap.add_argument("--floor-from-discover", action="store_true",
                    help="treat hard-ID pairs with no edge as measured-below-floor "
                         "(ONLY valid right after a discover run on these fingerprints); "
                         "skips per-pair matched queries, still verifies absences")
    ap.add_argument("--apply", action="store_true",
                    help="write to the warehouse (default: preview only)")
    ap.add_argument("--top", type=int, default=15, help="preview rows to print")
    args = ap.parse_args()

    if not FINGERPRINTS.exists() or not GRAPH.exists():
        print("REFUSED: missing outputs/connect_fingerprints.json or connect_graph.json")
        return 2
    fingerprints = json.loads(FINGERPRINTS.read_text(encoding="utf-8"))
    fmt2 = sum(1 for e in fingerprints.values() if e.get("fmt") == 2)
    if not fmt2:
        print("REFUSED: fingerprints are pre-fmt-2 (no range data) — run the sweep "
              "first: python -m connect fingerprint")
        return 2
    print(f"fingerprints: {len(fingerprints)} tables ({fmt2} fmt-2)")
    graph = json.loads(GRAPH.read_text(encoding="utf-8"))
    edge_map: dict = {}
    for e in graph.get("edges", []):
        edge_map.setdefault(census._canon(e["a"], e["b"]), []).append(e)

    membership = census.build_key_membership(fingerprints)
    cache = json.loads(MEASURED_CACHE.read_text()) if MEASURED_CACHE.exists() else {}
    if args.measure and not args.floor_from_discover:
        cache = measure_hard_pairs(membership, fingerprints, edge_map, cache)
    measured = {}
    for ck, m in cache.items():
        a, b, key = ck.split("|")
        measured[(a, b, key)] = m

    run_id = uuid.uuid4().hex[:12]
    rows = sieve.build_rows(membership, fingerprints, edge_map, measured, run_id,
                            floor_hard_unmeasured=args.floor_from_discover)
    if args.measure:
        verify_absences(rows, membership, fingerprints)
        sieve._annotate_flukes(rows)          # rebanding changes the family
    for r in rows:
        r["scaffold_sql"] = scaffold_sql(r["pair_a"], r["pair_b"],
                                         r["a_col"], r["b_col"], r["key"])

    bands: dict = {}
    for r in rows:
        bands[r["band"]] = bands.get(r["band"], 0) + 1
    print(f"\n{len(rows)} catalog rows. bands: "
          + ", ".join(f"{b} {n:,}" for b, n in sorted(bands.items())))
    ranked = [r for r in rows if r["s_chance"] is not None]
    ranked.sort(key=lambda r: r["s_chance"], reverse=True)
    # feed diversity: at most 2 rows per family-pair in the preview (the full
    # catalog keeps everything; this is the ranked VIEW, per the handoff's
    # "one anomaly must not produce 500 rows")
    shown, fam_seen = [], {}
    for r in ranked:
        fk = tuple(sorted(("_".join(r["pair_a"].split("_")[:2]),
                           "_".join(r["pair_b"].split("_")[:2]))))
        if fam_seen.get(fk, 0) >= 2:
            continue
        fam_seen[fk] = fam_seen.get(fk, 0) + 1
        shown.append(r)
        if len(shown) >= args.top:
            break
    print(f"\ntop {len(shown)} by surprise (max 2 per agency-family pair):")
    for r in shown:
        traps = f" traps={','.join(r['traps'])}" if r["traps"] else ""
        fam = " [same-family]" if r["same_family"] else ""
        print(f"  S={r['s_chance']:+6.2f} ef={r['expected_flukes']:<8} "
              f"{'PROMOTABLE ' if r['promotable'] else '           '}"
              f"{r['pair_a']} x {r['pair_b']} [{r['key']}]{fam}{traps}")
    neg = [r for r in ranked if r["band"] == "absence"]
    if neg:
        print(f"\ncredible absences (range-conditioned): {len(neg)}")
        for r in sorted(neg, key=lambda r: r["s_chance"])[:args.top]:
            print(f"  S={r['s_chance']:+6.2f} {r['pair_a']} x {r['pair_b']} [{r['key']}]")

    if not args.apply:
        print(f"\nPreview only. Re-run with --apply to write {CATALOG_FQN}.")
        return 0
    try:
        n = write_catalog(rows)
    except Exception as exc:
        print(f"HALT: catalog write failed ({exc}). If the table is missing, "
              "run infra/ddl/07_hypothesis_catalog.sql in Snowsight first.")
        return 1
    print(f"wrote {n} rows to {CATALOG_FQN}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
