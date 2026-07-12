#!/usr/bin/env python3
"""Build the ladder-holdout test fixture (Move 4 of RIPPLE_GOVERN_THYSELF).

One Snowflake session; after this, tests/test_ladder_invariants.py never touches
the network again. Writes three checked-in artifacts:

  tests/fixtures/ladder_holdout.parquet   held-out (TEST-split) candidate pairs:
                                          three-state agree flags + surname TF +
                                          label + the in-SQL match weight M
  tests/fixtures/ladder_blocking.parquet  per-record block sets for TEST-split
                                          true-match persons (blocking replay)
  tests/fixtures/ladder_model.json        MATCH_MODEL m/u + rungs + live counts

WAREHOUSE FOOTPRINT: read-only on all shared objects. The two tables it creates
(RESOLVE_SCRATCH, MATCH_TF_SURNAME) are TEMPORARY — session-scoped, gone at
disconnect, exactly as `connect calibrate` builds them. Split is the calibration's
own: MOD(ABS(HASH(ID_N)), 2) = 1 — by person, out-of-sample.

Needs a role that can CREATE TEMPORARY TABLE (reader can't). Pass the token via
the LADDER_FIXTURE_PAT env var so .env stays on the reader lane:

    LADDER_FIXTURE_PAT=<token> python3 scripts/build_ladder_fixture.py
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "library-onboarding"))

import pandas as pd  # noqa: E402
import snow  # noqa: E402
from connect import db  # noqa: E402
from connect.calibrate import _feat_cte, _m_expr  # noqa: E402
from connect.match import TF_FQN, _build_tf  # noqa: E402
from connect.resolve import MAX_EDIT_LAST, PAIRS, SCRATCH_FQN, _build_scratch  # noqa: E402

FIX = REPO / "tests" / "fixtures"
M_FLOOR = -2          # keep pairs with ROUND(M) >= this; rung thresholds are 0/8/11
MODEL_VERSION = "fs_emp_95b289e0"


def load_model(conn) -> tuple[dict, float, str]:
    rows = db.dicts(conn, f"SELECT FIELD, M, U, SURNAME_MODE, START_BITS "
                          f"FROM LIBRARY_META.\"CONNECT\".MATCH_MODEL "
                          f"WHERE MODEL_VERSION = '{MODEL_VERSION}'")
    if not rows:
        raise SystemExit(f"model {MODEL_VERSION} not found in MATCH_MODEL")
    model = {r["FIELD"]: {"m": float(r["M"]), "u": float(r["U"])} for r in rows}
    return model, float(rows[0]["START_BITS"]), rows[0]["SURNAME_MODE"]


def main() -> int:
    pat = os.environ.get("LADDER_FIXTURE_PAT")
    conn = snow.connect(pat=pat, role="ACCOUNTADMIN" if pat else None,
                        warehouse="COMPUTE_WH" if pat else None)
    try:
        cur = conn.cursor()
        cur.execute("SELECT CURRENT_ROLE(), CURRENT_WAREHOUSE()")
        print("session:", cur.fetchone())

        model, start, mode = load_model(conn)
        rungs = db.dicts(conn, f"SELECT RUNG, MIN_M, MEASURED_PRECISION, MEASURED_PRECISION_LO95, "
                               f"COVERAGE_RECALL FROM LIBRARY_META.\"CONNECT\".MATCH_RUNGS "
                               f"WHERE MODEL_VERSION = '{MODEL_VERSION}'")
        print(f"model {MODEL_VERSION}: mode={mode} start={start:.4f} bits, {len(rungs)} rungs")

        print("building TEMPORARY scratch (blocking passes) + TF — session-scoped ...")
        _build_scratch(conn, PAIRS["leie_nppes"])
        _build_tf(conn, PAIRS["leie_nppes"])

        m_expr = _m_expr(model, start, mode)

        # ── 1. holdout candidate pairs with flags + in-SQL M ────────────────
        print("pulling TEST-split candidate pairs ...")
        feat_sql = _feat_cte() + f"""
            SELECT LABEL, A_SUR, A_FST, A_ZIP, A_ADDR, A_MID, TF,
                   ({m_expr}) AS M, ROUND({m_expr}) AS M_BAND
            FROM feat WHERE SPL = 1 AND ROUND({m_expr}) >= {M_FLOOR}"""
        pairs = pd.DataFrame(db.dicts(conn, feat_sql))
        pairs.columns = [c.upper() for c in pairs.columns]

        # totals for the bands below the floor (coverage/recall denominators)
        tot = db.dicts(conn, _feat_cte() + """
            SELECT COUNT(*) AS N_TEST, SUM(LABEL) AS POS_TEST FROM feat WHERE SPL = 1""")[0]
        n_test, pos_test = int(tot["N_TEST"]), int(tot["POS_TEST"])
        print(f"  kept {len(pairs):,} pairs at M_BAND >= {M_FLOOR} "
              f"(full test split: {n_test:,} pairs, {pos_test:,} positives)")

        # ── 2. blocking replay: block sets per record for true-match persons ─
        print("pulling blocking-replay records (TEST-split true persons) ...")
        blocking_sql = f"""
            WITH true_ids AS (
                SELECT DISTINCT l.ID_N
                FROM {SCRATCH_FQN} l JOIN {SCRATCH_FQN} r
                  ON r.SIDE='R' AND l.SIDE='L' AND l.ID_N = r.ID_N
                WHERE l.ID_N IS NOT NULL AND MOD(ABS(HASH(l.ID_N)), 2) = 1)
            SELECT s.REF, s.SIDE, s.ID_N, s.LAST_N,
                   ARRAY_TO_STRING(ARRAY_AGG(DISTINCT s.BLOCK), '||') AS BLOCKS
            FROM {SCRATCH_FQN} s JOIN true_ids t ON t.ID_N = s.ID_N
            GROUP BY s.REF, s.SIDE, s.ID_N, s.LAST_N"""
        blocking = pd.DataFrame(db.dicts(conn, blocking_sql))
        blocking.columns = [c.upper() for c in blocking.columns]
        n_persons = blocking["ID_N"].nunique()
        print(f"  {len(blocking):,} records covering {n_persons:,} true-match test persons")

        # live (in-warehouse) recall reference: true pairs sharing >=1 block + edit prune
        live = db.dicts(conn, f"""
            WITH l AS (SELECT * FROM {SCRATCH_FQN} WHERE SIDE='L' AND ID_N IS NOT NULL
                       AND MOD(ABS(HASH(ID_N)), 2) = 1),
                 r AS (SELECT * FROM {SCRATCH_FQN} WHERE SIDE='R' AND ID_N IS NOT NULL),
                 uni AS (SELECT DISTINCT l.REF AS LREF, r.REF AS RREF, l.ID_N
                         FROM l JOIN r ON l.ID_N = r.ID_N),
                 hit AS (SELECT DISTINCT l.REF AS LREF, r.REF AS RREF
                         FROM l JOIN r ON l.BLOCK = r.BLOCK AND l.ID_N = r.ID_N
                         WHERE EDITDISTANCE(l.LAST_N, r.LAST_N) <= {MAX_EDIT_LAST})
            SELECT COUNT(*) AS UNIVERSE,
                   COUNT_IF(h.LREF IS NOT NULL) AS CAPTURED
            FROM uni u LEFT JOIN hit h ON h.LREF = u.LREF AND h.RREF = u.RREF""")[0]
        universe, captured = int(live["UNIVERSE"]), int(live["CAPTURED"])
        print(f"  live blocking recall: {captured:,}/{universe:,} = {captured/universe:.4f}")

        # ── 3. write artifacts ───────────────────────────────────────────────
        FIX.mkdir(parents=True, exist_ok=True)
        pairs.to_parquet(FIX / "ladder_holdout.parquet", index=False)
        blocking.to_parquet(FIX / "ladder_blocking.parquet", index=False)
        sidecar = {
            "built_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "model_version": MODEL_VERSION,
            "surname_mode": mode,
            "start_bits": start,
            "model": model,
            "rungs": rungs,
            "m_floor": M_FLOOR,
            "test_pairs_total": n_test,
            "test_positives_total": pos_test,
            "blocking": {"universe": universe, "captured": captured,
                         "recall": round(captured / universe, 4),
                         "max_edit_last": MAX_EDIT_LAST},
            "split": "MOD(ABS(HASH(ID_N)),2)=1 — by person, same as connect calibrate",
            "pair": "leie_nppes",
        }
        (FIX / "ladder_model.json").write_text(json.dumps(sidecar, indent=2, default=float))
        for f in ("ladder_holdout.parquet", "ladder_blocking.parquet", "ladder_model.json"):
            print(f"  wrote {FIX / f}  ({(FIX / f).stat().st_size / 1024:.0f} KB)")
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
