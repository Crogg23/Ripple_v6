"""Fellegi-Sunter match-weight scorer — the confidence ladder's scoring core (v2).

The multi-pass blocker (resolve.py) reaches ~96% of findable matches but floods the candidate
set with name-twins; a name-only score can't separate them (precision ~0.04). This scores each
candidate pair as a Fellegi-Sunter MATCH WEIGHT in bits of evidence:

    M = start + Σ_field weight(field)

    weight = log2(m / u)          when the field AGREES         (evidence FOR)
           = log2((1-m) / (1-u))  when it DISAGREES             (evidence AGAINST)
           = 0                    when it can't be compared     (NULL — the three-state rule)

v2 features: surname (TF rarity — a rare shared surname is loud, a shared 'Smith' nearly mute),
first name (nickname-aware), ZIP/place, **street address** (splits same-clinic name-twins), and
**middle initial** (the MOVE-STABLE disambiguator: a second 'John Smith' rarely also matches on
'A.' for Aloysius — a different middle initial is strong evidence they are NOT the same person,
and unlike ZIP/address it survives a relocation). Address and ZIP have LOW m by design — a true
match often moves — so a mismatch barely penalizes a mover while a match strongly corroborates.

m/u are HAND-SET for v2 (they graduate to a MERGE-loaded MATCH_MODEL table + EM later). Honesty
rules from design-confidence-ladder.md: NPI is LABEL-ONLY (never scored); the run reports a
3-WAY head-to-head — name-only vs name+ZIP vs +address+middle — on the IDENTICAL candidate set
at fixed recall, so each feature's contribution is isolated and the lift can't be faked.

    python -m connect match --pair leie_nppes
"""

from __future__ import annotations

import json
from pathlib import Path

from . import db, store
from .evaluate import wilson_lower
from .keys import quote_ident
from .resolve import MAX_EDIT_LAST, NICK_FQN, PAIRS, SCRATCH_FQN, _build_scratch, _ensure_nickname_map

OUT = Path(__file__).resolve().parents[1] / "outputs"
TF_FQN = store.cfqn("MATCH_TF_SURNAME")

# v2 hand-set Fellegi-Sunter SEED model (bits). m = P(field agrees | same person); u = P(agrees | not).
# NOTE: these are a CONSERVATIVE PRE-CALIBRATION SEED for the standalone `match` demo. The OPERATING
# model is the empirical, held-out-calibrated one that `connect calibrate` measures and persists to
# LIBRARY_META.CONNECT.MATCH_MODEL — its m/u and M-scale differ from (and SUPERSEDE) these, so do
# not compare match.py's printed M thresholds against calibrate's rung cut-points (different scale).
MODEL = {
    "start": -10.0,                                               # within-block prior log2(λ/(1-λ)), λ≈1e-3
    "surname": {"m": 0.95, "u_base": 0.01, "floor": 1e-5, "agree": 0.90},  # agree-u = per-value TF (rarity)
    "first":   {"m": 0.85, "u": 0.15, "agree": 0.90},
    "zip":     {"m": 0.25, "u": 0.005},                          # m LOW: true matches move ZIPs
    "address": {"m": 0.35, "u": 0.001, "agree": 0.90},           # m LOW (movers); u tiny -> strong when it agrees
    "middle":  {"m": 0.90, "u": 0.05},                           # middle-INITIAL equality; move-stable
}


def _build_tf(conn, spec: dict) -> None:
    """Surname term-frequency over the RIGHT (large) corpus — u for a surname agreement is how
    common that surname is, so a rare shared surname earns far more bits than a shared 'Smith'."""
    R = spec["right"]
    last_n = f"UPPER(TRIM({quote_ident(R['last'])}))"
    db.rows(conn, f"""
        CREATE OR REPLACE TEMPORARY TABLE {TF_FQN} AS
        WITH t AS (SELECT {last_n} AS V FROM {db.fqn(R['table'])} WHERE {last_n} <> '')
        SELECT V, COUNT(*)::FLOAT / NULLIF((SELECT COUNT(*) FROM t), 0) AS TF FROM t GROUP BY V""")


def _scored_sql() -> str:
    """Per-pair match weights: name-only SCORE, name+ZIP (M_NZ), and the full v2 weight (M).
    Every field is three-valued (NULL -> 0 bits) and LOG-guarded (no LOG(0)/divide-by-zero)."""
    s, f, z, a, mid = (MODEL["surname"], MODEL["first"], MODEL["zip"],
                       MODEL["address"], MODEL["middle"])
    w_sur = (f"CASE WHEN le.LAST_N IS NULL OR re.LAST_N IS NULL THEN 0 "
             f"WHEN JAROWINKLER_SIMILARITY(le.LAST_N, re.LAST_N)/100.0 >= {s['agree']} "
             f"THEN LOG(2, {s['m']} / GREATEST(COALESCE(tf.TF, {s['floor']}), {s['floor']})) "
             f"ELSE LOG(2, GREATEST(1-{s['m']}, 1e-6) / GREATEST(1-{s['u_base']}, 1e-6)) END")
    w_fst = (f"CASE WHEN le.FX IS NULL OR re.FX IS NULL THEN 0 "
             f"WHEN JAROWINKLER_SIMILARITY(le.FX, re.FX)/100.0 >= {f['agree']} "
             f"THEN LOG(2, {f['m']}/{f['u']}) "
             f"ELSE LOG(2, GREATEST(1-{f['m']}, 1e-6) / GREATEST(1-{f['u']}, 1e-6)) END")
    w_zip = (f"CASE WHEN NULLIF(le.PLACE,'') IS NULL OR NULLIF(re.PLACE,'') IS NULL THEN 0 "
             f"WHEN le.PLACE = re.PLACE THEN LOG(2, {z['m']}/{z['u']}) "
             f"ELSE LOG(2, GREATEST(1-{z['m']}, 1e-6) / GREATEST(1-{z['u']}, 1e-6)) END")
    w_addr = (f"CASE WHEN NULLIF(le.ADDR,'') IS NULL OR NULLIF(re.ADDR,'') IS NULL THEN 0 "
              f"WHEN JAROWINKLER_SIMILARITY(le.ADDR, re.ADDR)/100.0 >= {a['agree']} "
              f"THEN LOG(2, {a['m']}/{a['u']}) "
              f"ELSE LOG(2, GREATEST(1-{a['m']}, 1e-6) / GREATEST(1-{a['u']}, 1e-6)) END")
    w_mid = (f"CASE WHEN NULLIF(le.MID,'') IS NULL OR NULLIF(re.MID,'') IS NULL THEN 0 "
             f"WHEN le.MID = re.MID THEN LOG(2, {mid['m']}/{mid['u']}) "
             f"ELSE LOG(2, GREATEST(1-{mid['m']}, 1e-6) / GREATEST(1-{mid['u']}, 1e-6)) END")
    base_nz = f"{MODEL['start']} + ({w_sur}) + ({w_fst}) + ({w_zip})"
    return f"""
        WITH l AS (SELECT * FROM {SCRATCH_FQN} WHERE SIDE='L' AND ID_N IS NOT NULL),
             r AS (SELECT * FROM {SCRATCH_FQN} WHERE SIDE='R' AND ID_N IS NOT NULL),
             le AS (SELECT l.*, COALESCE(nk.CANONICAL, SPLIT_PART(l.FIRST_N,' ',1)) AS FX
                    FROM l LEFT JOIN {NICK_FQN} nk ON nk.VARIANT=SPLIT_PART(l.FIRST_N,' ',1)),
             re AS (SELECT r.*, COALESCE(nk.CANONICAL, SPLIT_PART(r.FIRST_N,' ',1)) AS FX
                    FROM r LEFT JOIN {NICK_FQN} nk ON nk.VARIANT=SPLIT_PART(r.FIRST_N,' ',1))
        SELECT (le.ID_N = re.ID_N) AS LABEL,
               ROUND({base_nz}, 3) AS M_NZ,
               ROUND({base_nz} + ({w_addr}) + ({w_mid}), 3) AS M,
               ROUND(0.70*JAROWINKLER_SIMILARITY(le.LAST_N, re.LAST_N)/100.0
                   + 0.30*JAROWINKLER_SIMILARITY(le.FX, re.FX)/100.0, 3) AS SCORE
        FROM le JOIN re ON le.BLOCK = re.BLOCK AND le.REF <> re.REF
             LEFT JOIN {TF_FQN} tf ON tf.V = re.LAST_N
        WHERE EDITDISTANCE(le.LAST_N, re.LAST_N) <= {MAX_EDIT_LAST}
        QUALIFY ROW_NUMBER() OVER (PARTITION BY le.REF, re.REF ORDER BY le.BLOCK) = 1
    """


def _sweep(rows, key, grid, pos_total):
    table = []
    for t in grid:
        sel = [r for r in rows if r[key] is not None and float(r[key]) >= t]
        n = len(sel)
        tp = sum(1 for r in sel if r["LABEL"])
        prec = tp / n if n else 0.0
        rec = tp / pos_total if pos_total else 0.0
        f1 = 2 * prec * rec / (prec + rec) if (prec + rec) else 0.0
        table.append({"t": round(t, 3), "n": n, "tp": tp, "precision": round(prec, 4),
                      "precision_lo95": round(wilson_lower(tp, n), 4), "recall": round(rec, 4),
                      "f1": round(f1, 4)})
    return table


def _at_recall(table, floor):
    """Tightest threshold (max precision) that still holds recall >= floor — apples-to-apples."""
    ok = [r for r in table if r["recall"] >= floor]
    return max(ok, key=lambda r: r["t"]) if ok else None


def run(pair: str = "leie_nppes") -> dict:
    if pair not in PAIRS:
        raise SystemExit(f"unknown pair '{pair}'. known: {list(PAIRS)}")
    conn = db.connect()
    try:
        store.ensure_schema(conn)
        _ensure_nickname_map(conn)
        _build_scratch(conn, PAIRS[pair])
        _build_tf(conn, PAIRS[pair])
        rows = db.dicts(conn, _scored_sql())
    finally:
        conn.close()

    pos = sum(1 for r in rows if r["LABEL"])
    bits = [round(-6 + i, 1) for i in range(0, 27)]                       # M from -6 .. +20
    sweeps = {"name_only": _sweep(rows, "SCORE", [round(0.80 + 0.01 * i, 2) for i in range(0, 20)], pos),
              "name_zip": _sweep(rows, "M_NZ", bits, pos),
              "full": _sweep(rows, "M", bits, pos)}

    pa_r = {}
    for floor in (0.90, 0.80, 0.70, 0.50, 0.30, 0.20):
        row = {}
        for name in ("name_only", "name_zip", "full"):
            b = _at_recall(sweeps[name], floor)
            row[name] = ({"precision": b["precision"], "precision_lo95": b["precision_lo95"],
                          "n": b["n"], "t": b["t"]} if b else None)
        pa_r[floor] = row

    out = {"pair": pair, "candidate_pairs": len(rows), "positives": pos, "model": MODEL,
           "precision_at_recall": pa_r, "sweeps": sweeps}
    OUT.mkdir(exist_ok=True)
    (OUT / "match_eval.json").write_text(json.dumps(out, indent=2))

    print(f"\nmatch [{pair}]: {len(rows):,} candidate pairs, {pos:,} true matches")
    print("  Full Fellegi-Sunter match weight (M, bits) — name + ZIP + address + middle:")
    print(f"  {'M>=':>5} {'n':>9} {'prec':>7} {'prec_lo':>7} {'recall':>7} {'f1':>7}")
    for r in sweeps["full"]:
        if r["n"]:
            print(f"  {r['t']:>5} {r['n']:>9} {r['precision']:>7.3f} {r['precision_lo95']:>7.3f} "
                  f"{r['recall']:>7.3f} {r['f1']:>7.3f}")
    print("\n  3-WAY HEAD-TO-HEAD — precision at fixed recall, IDENTICAL candidate set:")
    print(f"  {'recall>=':>9} {'name-only':>11} {'name+ZIP':>11} {'+addr+middle':>16}")
    for floor in (0.90, 0.80, 0.70, 0.50, 0.30, 0.20):
        cells = []
        for name in ("name_only", "name_zip", "full"):
            d = pa_r[floor][name]
            cells.append(f"{d['precision']:.3f}" if d else "  —  ")
        full = pa_r[floor]["full"]
        tail = f"  (M>={full['t']}, n={full['n']:,})" if full else ""
        print(f"  {floor:>9} {cells[0]:>11} {cells[1]:>11} {cells[2]:>16}{tail}")
    print(f"\n  wrote {OUT / 'match_eval.json'}")
    return out


if __name__ == "__main__":
    run()
