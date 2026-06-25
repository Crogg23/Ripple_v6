"""Match-quality eval harness for the fuzzy resolver — the gate before any auto-merge.

Ground truth comes from the hard IDs we already trust: among blocked candidate
pairs where BOTH sides carry an NPI, same-NPI = a true match (positive), different-
NPI = a true non-match (negative). Pairs missing an NPI on either side are 'unknown'
and excluded from precision/recall (they're the leads, not labels).

Sweeps the score threshold, reports precision/recall/F1, and recommends:
  HIGH      lowest threshold with precision >= --target (default 0.99) — the auto-merge bar
  BEST_F1   the threshold maximizing F1 — a sensible MIN_SCORE floor

Writes outputs/resolve_eval.json, persists LIBRARY_META.CONNECT.GOLD_PAIRS, and
freezes tests/fixtures/gold_pairs_sample.csv for the offline test suite.

    python -m connect eval --pair leie_nppes
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

from . import db, store
from .resolve import HIGH, MAX_EDIT_LAST, MIN_SCORE, NICK_FQN, PAIRS, SCRATCH_FQN, _build_scratch, _ensure_nickname_map

OUT = Path(__file__).resolve().parents[1] / "outputs"
FIXTURE = Path(__file__).resolve().parents[1] / "tests" / "fixtures" / "gold_pairs_sample.csv"
GOLD_FQN = store.cfqn("GOLD_PAIRS")


def _labeled_sql() -> str:
    """Score blocked candidate pairs where BOTH sides have an NPI; label by same-NPI."""
    return f"""
        WITH l AS (SELECT * FROM {SCRATCH_FQN} WHERE SIDE = 'L' AND ID_N IS NOT NULL),
             r AS (SELECT * FROM {SCRATCH_FQN} WHERE SIDE = 'R' AND ID_N IS NOT NULL),
             le AS (SELECT l.*, COALESCE(nk.CANONICAL, SPLIT_PART(l.FIRST_N, ' ', 1)) AS FX
                    FROM l LEFT JOIN {NICK_FQN} nk ON nk.VARIANT = SPLIT_PART(l.FIRST_N, ' ', 1)),
             re AS (SELECT r.*, COALESCE(nk.CANONICAL, SPLIT_PART(r.FIRST_N, ' ', 1)) AS FX
                    FROM r LEFT JOIN {NICK_FQN} nk ON nk.VARIANT = SPLIT_PART(r.FIRST_N, ' ', 1))
        SELECT le.LAST_N AS L_LAST, le.FX AS L_FIRST, re.LAST_N AS R_LAST, re.FX AS R_FIRST,
               le.PLACE AS PLACE, (le.ID_N = re.ID_N) AS LABEL,
               ROUND(0.70 * JAROWINKLER_SIMILARITY(le.LAST_N, re.LAST_N) / 100.0
                   + 0.30 * JAROWINKLER_SIMILARITY(le.FX, re.FX) / 100.0, 3) AS SCORE
        FROM le JOIN re ON le.BLOCK = re.BLOCK AND le.REF <> re.REF
        WHERE EDITDISTANCE(le.LAST_N, re.LAST_N) <= {MAX_EDIT_LAST}
    """


def sweep(rows: list[dict], thresholds) -> tuple[list[dict], int]:
    pos_total = sum(1 for r in rows if r["LABEL"])
    table = []
    for t in thresholds:
        sel = [r for r in rows if float(r["SCORE"]) >= t]
        tp = sum(1 for r in sel if r["LABEL"])
        fp = len(sel) - tp
        prec = tp / len(sel) if sel else 0.0
        rec = tp / pos_total if pos_total else 0.0
        f1 = 2 * prec * rec / (prec + rec) if (prec + rec) else 0.0
        table.append({"t": round(t, 2), "n": len(sel), "tp": tp, "fp": fp,
                      "precision": round(prec, 4), "recall": round(rec, 4), "f1": round(f1, 4)})
    return table, pos_total


def _freeze_fixture(rows: list[dict], limit: int = 1500) -> None:
    FIXTURE.parent.mkdir(parents=True, exist_ok=True)
    # balanced-ish sample: keep all positives + a cap of negatives
    pos = [r for r in rows if r["LABEL"]]
    neg = [r for r in rows if not r["LABEL"]]
    sample = (pos[:limit] + neg[:limit])
    with FIXTURE.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["l_last", "l_first", "r_last", "r_first", "place", "label"])
        for r in sample:
            w.writerow([r["L_LAST"], r["L_FIRST"], r["R_LAST"], r["R_FIRST"], r["PLACE"],
                        int(bool(r["LABEL"]))])
    print(f"  froze {len(sample):,} labeled pairs -> {FIXTURE}")


def run(pair: str = "leie_nppes", target: float = 0.99, freeze: bool = True) -> dict:
    if pair not in PAIRS:
        raise SystemExit(f"unknown pair '{pair}'. known: {list(PAIRS)}")
    conn = db.connect()
    try:
        store.ensure_schema(conn)
        _ensure_nickname_map(conn)
        _build_scratch(conn, PAIRS[pair])
        rows = db.dicts(conn, _labeled_sql())
        # persist the labeled gold set
        db.rows(conn, f"CREATE OR REPLACE TABLE {GOLD_FQN} AS {_labeled_sql()}")
    finally:
        conn.close()

    thresholds = [0.80 + 0.01 * i for i in range(0, 20)]  # 0.80 .. 0.99
    table, pos_total = sweep(rows, thresholds)
    labeled = len(rows)            # _labeled_sql forces both sides' NPI non-null -> never None
    pos = pos_total
    neg = labeled - pos

    # Precision is only meaningful with negatives to be wrong about; with neg==0 every
    # threshold is trivially precision 1.0, which must NOT recommend an auto-merge bar.
    high = (None if neg == 0 else
            next((row["t"] for row in table if row["precision"] >= target and row["n"] > 0), None))
    best_f1 = max(table, key=lambda x: x["f1"]) if table else None

    report = {"pair": pair, "labeled_pairs": labeled, "positives": pos, "negatives": neg,
              "target_precision": target, "recommend_HIGH": high,
              "recommend_MIN_SCORE_bestF1": best_f1["t"] if best_f1 else None,
              "current_HIGH": HIGH, "current_MIN_SCORE": MIN_SCORE, "sweep": table}
    OUT.mkdir(exist_ok=True)
    (OUT / "resolve_eval.json").write_text(json.dumps(report, indent=2))

    print(f"\neval [{pair}]: {labeled:,} labeled pairs ({pos:,} same-person / {neg:,} different)")
    print(f"  {'thr':>5} {'n':>7} {'prec':>7} {'recall':>7} {'f1':>7}")
    for row in table:
        mark = "  <- HIGH" if row["t"] == high else ("  <- bestF1" if best_f1 and row["t"] == best_f1["t"] else "")
        print(f"  {row['t']:>5} {row['n']:>7} {row['precision']:>7.3f} {row['recall']:>7.3f} {row['f1']:>7.3f}{mark}")
    print(f"\n  recommend HIGH (precision>={target}) = {high}   "
          f"best-F1 MIN_SCORE = {best_f1['t'] if best_f1 else None}   "
          f"(current HIGH={HIGH}, MIN_SCORE={MIN_SCORE})")
    print(f"  wrote {OUT / 'resolve_eval.json'} + {GOLD_FQN}")
    if freeze:
        _freeze_fixture(rows)
    return report


if __name__ == "__main__":
    run()
