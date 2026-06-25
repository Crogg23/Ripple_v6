"""Calibrate the Fellegi-Sunter scorer against ground truth, honestly.

Build 5. The hand-set m/u in match.py were a conservative guess; this estimates them from
the data and sets the confidence-tier cut-points from MEASURED precision. Two integrity rails
the design review demanded:

  * TRAIN/TEST SPLIT BY PERSON. Parameters are estimated on half the left entities (by a hash
    of the LEIE NPI) and every reported number is measured on the OTHER half — out-of-sample,
    so tuning on the labels can't inflate the score. (NPI is split-key + label only, never a
    scored feature.)
  * TIERS FROM MEASURED PRECISION, not the model's self-opinion. A rung's label (CONFIRMED /
    STRONG / LEAD) is the widest-coverage match-weight band whose HELD-OUT Wilson-lower
    precision clears a bar — so 'CONFIRMED' always means 'measured >= the bar on unseen data'.

It also settles the open question from Build 4's verification: surname is partly a blocking key
(SOUNDEX), so the global-TF rarity weight may over-credit it. We score BOTH a TF-rarity surname
and a flat surname and keep whichever wins out-of-sample.

Persistence: every field comparison is THREE-VALUED (agree / disagree / can't-compare→NULL→0 bits)
to match match.py and the design's §2 rule. The model is written to a CONTENT-ADDRESSED version
(`fs_emp_<hash>` of the m/u + start + mode) so distinct calibrations are append-versioned (a prior
run's weights survive) while an identical re-run is idempotent; the DELETE+INSERT is wrapped in a
transaction so an abort can't leave a torn model. Tables: LIBRARY_META.CONNECT.MATCH_MODEL
(field, m, u_base, surname_mode, start) + MATCH_RUNGS (rung, min match weight, measured precision,
coverage). For surname in 'tf' mode the AGREE weight is log2(m/TF) — the stored U is the disagree
u_base only.

    python -m connect calibrate --pair leie_nppes
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

from . import db, store
from .evaluate import wilson_lower
from .match import TF_FQN, _build_tf
from .resolve import MAX_EDIT_LAST, NICK_FQN, PAIRS, SCRATCH_FQN, _build_scratch, _ensure_nickname_map

OUT = Path(__file__).resolve().parents[1] / "outputs"
MODEL_FQN = store.cfqn("MATCH_MODEL")
RUNGS_FQN = store.cfqn("MATCH_RUNGS")
MODEL_FAMILY = "fs_emp"            # full version = MODEL_FAMILY + '_' + content hash (append-versioned)
FLOOR = 1e-5                       # TF floor: nothing treated as rarer than 1-in-100k
AGREE = 0.90                       # JaroWinkler agree threshold (scaled 0-1)
# tier bars on HELD-OUT Wilson-lower precision (highest first)
RUNGS = [("CONFIRMED", 0.85), ("STRONG", 0.50), ("LEAD", 0.10)]


def _feat_cte() -> str:
    """WITH ... feat AS (one row per candidate pair: label, split, per-field AGREE flags
    (1 / 0 / NULL three-state — NULL = can't compare, never folded in as a disagreement),
    surname TF, and the legacy name-only score)."""
    return f"""
        WITH l AS (SELECT * FROM {SCRATCH_FQN} WHERE SIDE='L' AND ID_N IS NOT NULL),
             r AS (SELECT * FROM {SCRATCH_FQN} WHERE SIDE='R' AND ID_N IS NOT NULL),
             le AS (SELECT l.*, COALESCE(nk.CANONICAL, SPLIT_PART(l.FIRST_N,' ',1)) AS FX
                    FROM l LEFT JOIN {NICK_FQN} nk ON nk.VARIANT=SPLIT_PART(l.FIRST_N,' ',1)),
             re AS (SELECT r.*, COALESCE(nk.CANONICAL, SPLIT_PART(r.FIRST_N,' ',1)) AS FX
                    FROM r LEFT JOIN {NICK_FQN} nk ON nk.VARIANT=SPLIT_PART(r.FIRST_N,' ',1)),
             feat AS (
               SELECT IFF(le.ID_N = re.ID_N, 1, 0) AS LABEL,
                      MOD(ABS(HASH(le.ID_N)), 2) AS SPL,
                      IFF(le.LAST_N IS NOT NULL AND re.LAST_N IS NOT NULL,
                          IFF(JAROWINKLER_SIMILARITY(le.LAST_N,re.LAST_N)/100.0 >= {AGREE},1,0), NULL) AS A_SUR,
                      IFF(le.FX IS NOT NULL AND re.FX IS NOT NULL,
                          IFF(JAROWINKLER_SIMILARITY(le.FX,re.FX)/100.0 >= {AGREE},1,0), NULL) AS A_FST,
                      IFF(NULLIF(le.PLACE,'') IS NOT NULL AND NULLIF(re.PLACE,'') IS NOT NULL,
                          IFF(le.PLACE = re.PLACE,1,0), NULL) AS A_ZIP,
                      IFF(NULLIF(le.ADDR,'') IS NOT NULL AND NULLIF(re.ADDR,'') IS NOT NULL,
                          IFF(JAROWINKLER_SIMILARITY(le.ADDR,re.ADDR)/100.0 >= {AGREE},1,0), NULL) AS A_ADDR,
                      IFF(NULLIF(le.MID,'') IS NOT NULL AND NULLIF(re.MID,'') IS NOT NULL,
                          IFF(le.MID = re.MID,1,0), NULL) AS A_MID,
                      GREATEST(COALESCE(tf.TF, {FLOOR}), {FLOOR}) AS TF
               FROM le JOIN re ON le.BLOCK = re.BLOCK AND le.REF <> re.REF
                    LEFT JOIN {TF_FQN} tf ON tf.V = re.LAST_N
               WHERE EDITDISTANCE(le.LAST_N, re.LAST_N) <= {MAX_EDIT_LAST}
               QUALIFY ROW_NUMBER() OVER (PARTITION BY le.REF, re.REF ORDER BY le.BLOCK) = 1 )"""


def _estimate(conn) -> tuple[dict, float]:
    """Per-field m = P(agree|same) and u = P(agree|not), measured on the TRAIN split only.
    AVG over a 1/0/NULL flag ignores NULLs, so these are rates over COMPARABLE pairs (3-state).
    A field that is never comparable in a class (AVG -> NULL) is neutralized to m=u=0.5 (0 bits)."""
    rows = db.dicts(conn, _feat_cte() + """
        SELECT LABEL, COUNT(*) N, AVG(A_SUR) SUR, AVG(A_FST) FST,
               AVG(A_ZIP) ZIP, AVG(A_ADDR) ADDR, AVG(A_MID) MID
        FROM feat WHERE SPL = 0 GROUP BY LABEL""")
    by = {int(r["LABEL"]): r for r in rows}
    if 0 not in by or 1 not in by:
        raise SystemExit("calibrate: TRAIN split lacks both label classes — not enough ground "
                         "truth to estimate m/u (check the pair / blocking).")
    fields = {"surname": "SUR", "first": "FST", "zip": "ZIP", "address": "ADDR", "middle": "MID"}
    model = {}
    for f, c in fields.items():
        m = None if by[1][c] is None else float(by[1][c])
        u = None if by[0][c] is None else float(by[0][c])
        if m is None or u is None:        # never comparable in a class -> field contributes 0 bits
            m = u = 0.5
        model[f] = {"m": m, "u": u}
    prior = float(by[1]["N"]) / (float(by[1]["N"]) + float(by[0]["N"]))
    return model, prior


def _weight(flag: str, m: float, u: float) -> str:
    m, u = min(max(m, 1e-6), 1 - 1e-6), min(max(u, 1e-6), 1 - 1e-6)
    return (f"CASE WHEN {flag}=1 THEN LOG(2,{m}/{u}) "
            f"WHEN {flag}=0 THEN LOG(2,(1-{m})/(1-{u})) ELSE 0 END")


_FLAG = {"first": "A_FST", "zip": "A_ZIP", "address": "A_ADDR", "middle": "A_MID"}


def _m_expr(model: dict, start: float, surname_mode: str) -> str:
    s = model["surname"]
    sm = min(max(s["m"], 1e-6), 1 - 1e-6)
    su = min(max(s["u"], 1e-6), 1 - 1e-6)
    if surname_mode == "tf":   # rare exact surname is loud: agree-u = the surname's term frequency
        w_sur = (f"CASE WHEN A_SUR=1 THEN LOG(2,{sm}/TF) "
                 f"WHEN A_SUR=0 THEN LOG(2,(1-{sm})/(1-{su})) ELSE 0 END")
    else:                      # flat: surname agreement is near-useless (it's a blocking key)
        w_sur = _weight("A_SUR", s["m"], s["u"])
    parts = [str(round(start, 4)), f"({w_sur})"]
    for f, flag in _FLAG.items():
        parts.append(f"({_weight(flag, model[f]['m'], model[f]['u'])})")
    return " + ".join(parts)


def _curve(conn, m_expr: str) -> tuple[list, int]:
    """Histogram the held-out (TEST) match weights into integer bands, then cumulate from the
    top down into a precision/recall curve. Only small aggregates leave the warehouse."""
    hist = db.dicts(conn, _feat_cte() + f"""
        SELECT ROUND({m_expr}) AS B, COUNT(*) AS N, SUM(LABEL) AS TP
        FROM feat WHERE SPL = 1 GROUP BY B ORDER BY B DESC""")
    pos = sum(int(h["TP"]) for h in hist)
    cn = ct = 0
    curve = []
    for h in hist:
        cn += int(h["N"]); ct += int(h["TP"])
        prec = ct / cn if cn else 0.0
        curve.append({"M": float(h["B"]), "n": cn, "tp": ct,
                      "precision": round(prec, 4), "precision_lo95": round(wilson_lower(ct, cn), 4),
                      "recall": round(ct / pos, 4) if pos else 0.0})
    return curve, pos


def _prec_at_recall(curve, floor):
    ok = [c for c in curve if c["recall"] >= floor]
    return min(ok, key=lambda c: c["recall"]) if ok else None   # tightest band still >= floor


def _rungs(curve) -> list[dict]:
    out = []
    for name, bar in RUNGS:
        # the widest-coverage (lowest-M) band whose HELD-OUT lower-bound precision still clears the bar
        clearers = [c for c in curve if c["precision_lo95"] >= bar]
        band = max(clearers, key=lambda c: c["recall"]) if clearers else None
        out.append({"rung": name, "bar": bar,
                    "min_M": band["M"] if band else None,
                    "precision": band["precision"] if band else None,
                    "precision_lo95": band["precision_lo95"] if band else None,
                    "coverage_recall": band["recall"] if band else None,
                    "n": band["n"] if band else None})
    return out


def _version(model: dict, start: float, mode: str) -> str:
    """Content-addressed model version: identical inputs -> identical version (idempotent re-run);
    any parameter change -> a NEW version, so prior calibrations are retained (append-versioned)."""
    payload = repr([(f, round(model[f]["m"], 6), round(model[f]["u"], 6)) for f in sorted(model)])
    payload += f"|start={round(start, 4)}|mode={mode}"
    return f"{MODEL_FAMILY}_" + hashlib.md5(payload.encode()).hexdigest()[:8]


def _persist(conn, version, model, start, mode, rungs) -> None:
    """Atomic upsert of one model version (DELETE the same version + INSERT, inside a transaction
    so an abort can't leave a torn model). CREATED_AT defaults so VALUES carry only literals."""
    db.rows(conn, f"""CREATE TABLE IF NOT EXISTS {MODEL_FQN} (
        MODEL_VERSION STRING, FIELD STRING, M FLOAT, U FLOAT, SURNAME_MODE STRING,
        START_BITS FLOAT, CREATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP())""")
    db.rows(conn, f"""CREATE TABLE IF NOT EXISTS {RUNGS_FQN} (
        MODEL_VERSION STRING, RUNG STRING, MIN_M FLOAT, MEASURED_PRECISION FLOAT,
        MEASURED_PRECISION_LO95 FLOAT, COVERAGE_RECALL FLOAT, CREATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP())""")
    model_vals = ", ".join(
        f"('{version}','{f}',{mu['m']},{mu['u']},'{mode}',{round(start, 4)})" for f, mu in model.items())
    rung_vals = ", ".join(
        f"('{version}','{r['rung']}',{r['min_M']},{r['precision']},{r['precision_lo95']},{r['coverage_recall']})"
        for r in rungs if r["min_M"] is not None)
    db.rows(conn, "BEGIN")
    try:
        db.rows(conn, f"DELETE FROM {MODEL_FQN} WHERE MODEL_VERSION = '{version}'")
        db.rows(conn, f"DELETE FROM {RUNGS_FQN} WHERE MODEL_VERSION = '{version}'")
        db.rows(conn, f"INSERT INTO {MODEL_FQN} "
                      f"(MODEL_VERSION,FIELD,M,U,SURNAME_MODE,START_BITS) VALUES {model_vals}")
        if rung_vals:
            db.rows(conn, f"INSERT INTO {RUNGS_FQN} "
                          f"(MODEL_VERSION,RUNG,MIN_M,MEASURED_PRECISION,MEASURED_PRECISION_LO95,"
                          f"COVERAGE_RECALL) VALUES {rung_vals}")
        db.rows(conn, "COMMIT")
    except Exception:
        db.rows(conn, "ROLLBACK")
        raise


def run(pair: str = "leie_nppes") -> dict:
    if pair not in PAIRS:
        raise SystemExit(f"unknown pair '{pair}'. known: {list(PAIRS)}")
    conn = db.connect()
    try:
        store.ensure_schema(conn)
        _ensure_nickname_map(conn)
        _build_scratch(conn, PAIRS[pair])
        _build_tf(conn, PAIRS[pair])
        model, prior = _estimate(conn)
        start = math.log2(min(max(prior, 1e-9), 1 - 1e-9) / (1 - min(max(prior, 1e-9), 1 - 1e-9)))
        # settle surname mode out-of-sample: TF-rarity vs flat
        variants = {}
        for mode in ("tf", "flat"):
            curve, pos = _curve(conn, _m_expr(model, start, mode))
            variants[mode] = {"curve": curve, "pos": pos,
                              "at": {f: _prec_at_recall(curve, f) for f in (0.5, 0.3, 0.2)}}
        # winner = higher precision at recall>=0.3 (the lead-generation operating point)
        def score(v):
            c = v["at"][0.3]
            return c["precision"] if c else -1.0
        win = max(variants, key=lambda m: score(variants[m]))
        if variants[win]["at"][0.3] is None:
            print("  WARNING: neither surname mode reached recall>=0.30 — winner is undefined; review.")
        curve, pos = variants[win]["curve"], variants[win]["pos"]
        rungs = _rungs(curve)
        version = _version(model, start, win)
        persisted = any(r["min_M"] is not None for r in rungs)
        if persisted:
            _persist(conn, version, model, start, win, rungs)
        else:
            print("  WARNING: no rung cleared its precision bar — NOT persisting (prior model left intact).")
    finally:
        conn.close()

    out = {"pair": pair, "model_version": version, "persisted": persisted, "surname_mode": win,
           "start_bits": round(start, 3), "test_positives": pos,
           "model": {f: {"m": round(mu["m"], 4), "u": round(mu["u"], 5)} for f, mu in model.items()},
           "rungs": rungs,
           "precision_at_recall": {m: {f: (v["at"][f]["precision"] if v["at"][f] else None)
                                       for f in (0.5, 0.3, 0.2)} for m, v in variants.items()}}
    OUT.mkdir(exist_ok=True)
    (OUT / "calibrate.json").write_text(json.dumps(out, indent=2, default=str))

    print(f"\ncalibrate [{pair}] — held-out (test) results, model {version}"
          + ("" if persisted else "  (NOT persisted)"))
    print("  empirical m (agree|same)  /  u (agree|different):")
    for f, mu in model.items():
        print(f"    {f:8} m={mu['m']:.4f}  u={mu['u']:.5f}")
    print(f"  prior start = {start:.2f} bits")
    print("\n  surname mode bake-off (precision at fixed recall, held-out):")
    print(f"  {'recall>=':>9} {'TF-rarity':>11} {'flat':>11}")
    for f in (0.5, 0.3, 0.2):
        tf = variants["tf"]["at"][f]
        fl = variants["flat"]["at"][f]
        tfs = f"{tf['precision']:.3f}" if tf else "  —  "
        fls = f"{fl['precision']:.3f}" if fl else "  —  "
        print(f"  {f:>9} {tfs:>11} {fls:>11}")
    print(f"  -> winner: surname '{win}'")
    print("\n  CALIBRATED TIERS (held-out, measured — this is what 'confident' MEANS now):")
    print(f"  {'rung':>10} {'M>=':>6} {'precision':>10} {'prec_lo95':>10} {'coverage':>9} {'n':>8}")
    for r in rungs:
        if r["min_M"] is None:
            print(f"  {r['rung']:>10}  (no band clears {r['bar']:.2f})")
        else:
            print(f"  {r['rung']:>10} {r['min_M']:>6.0f} {r['precision']:>10.3f} "
                  f"{r['precision_lo95']:>10.3f} {r['coverage_recall']:>9.3f} {r['n']:>8,}")
    print(f"\n  {'persisted' if persisted else 'would persist'} {MODEL_FQN} + {RUNGS_FQN}; "
          f"wrote {OUT / 'calibrate.json'}")
    return out


if __name__ == "__main__":
    run()
