"""Match-quality eval harness for the fuzzy resolver — the gate before any auto-merge.

Ground truth comes from the hard IDs we already trust: among blocked candidate
pairs where BOTH sides carry an NPI, same-NPI = a true match (positive), different-
NPI = a true non-match (negative). Pairs missing an NPI on either side are 'unknown'
and excluded from precision/recall (they're the leads, not labels).

NPI is LABEL-ONLY here — it never enters the SCORE, so there is no leakage. The
Fellegi-Sunter scorer (when it lands) must keep NPI held out during eval for the same
reason: a feature computed from the answer key fakes precision toward 1.0.

What this harness reports honestly (hardened 2026-06-25 after the design review):
  - precision / recall / F1 swept over the score threshold, on the FULL population
  - precision_lo95: the Wilson lower bound — a precision claim with no CI is a point guess
  - HIGH (auto-merge bar): the lowest threshold whose precision_lo95 >= target AND that
    selects at least MIN_BIN_N pairs (you cannot certify 0.99 on a handful of rows)
  - precision_at_recall: best precision while still holding recall >= RECALL_FLOOR, so a
    'win' can't be gamed by collapsing recall
  - blocking_recall: the recall CEILING imposed by blocking alone, independent of the
    scorer — of all findable cross-source true matches, how many even reach a block

Writes outputs/resolve_eval.json, persists LIBRARY_META.CONNECT.GOLD_PAIRS, and freezes
a seeded, balanced tests/fixtures/gold_pairs_sample.csv for the offline rank-separation
test (a balanced fixture is for logic regression, NOT a production-precision oracle —
precision is prevalence-dependent and is only ever read off the full population below).

    python -m connect eval --pair leie_nppes
"""

from __future__ import annotations

import csv
import json
import math
import random
from pathlib import Path

from . import db, store
from .keys import normalize_sql, quote_ident
from .resolve import HIGH, MAX_EDIT_LAST, MIN_SCORE, NICK_FQN, PAIRS, SCRATCH_FQN, _build_scratch, _ensure_nickname_map

OUT = Path(__file__).resolve().parents[1] / "outputs"
FIXTURE = Path(__file__).resolve().parents[1] / "tests" / "fixtures" / "gold_pairs_sample.csv"
GOLD_FQN = store.cfqn("GOLD_PAIRS")

MIN_BIN_N = 300      # don't certify an auto-merge precision bar on fewer selected pairs than this
RECALL_FLOOR = 0.80  # report best precision while still holding at least this recall


def wilson_lower(tp: int, n: int, z: float = 1.96) -> float:
    """95% Wilson score lower bound on a proportion tp/n. A precision point estimate
    with n small is nearly meaningless; the lower bound is what an auto-merge bar must clear."""
    if n <= 0:
        return 0.0
    p = tp / n
    denom = 1.0 + z * z / n
    centre = p + z * z / (2 * n)
    margin = z * math.sqrt((p * (1 - p) + z * z / (4 * n)) / n)
    return max(0.0, (centre - margin) / denom)


def _labeled_sql() -> str:
    """Score blocked candidate pairs where BOTH sides have an NPI; label by same-NPI.
    Emits NPI (label-only — never in SCORE) so we can count distinct true entities."""
    return f"""
        WITH l AS (SELECT * FROM {SCRATCH_FQN} WHERE SIDE = 'L' AND ID_N IS NOT NULL),
             r AS (SELECT * FROM {SCRATCH_FQN} WHERE SIDE = 'R' AND ID_N IS NOT NULL),
             le AS (SELECT l.*, COALESCE(nk.CANONICAL, SPLIT_PART(l.FIRST_N, ' ', 1)) AS FX
                    FROM l LEFT JOIN {NICK_FQN} nk ON nk.VARIANT = SPLIT_PART(l.FIRST_N, ' ', 1)),
             re AS (SELECT r.*, COALESCE(nk.CANONICAL, SPLIT_PART(r.FIRST_N, ' ', 1)) AS FX
                    FROM r LEFT JOIN {NICK_FQN} nk ON nk.VARIANT = SPLIT_PART(r.FIRST_N, ' ', 1))
        SELECT le.ID_N AS NPI, le.LAST_N AS L_LAST, le.FX AS L_FIRST,
               re.LAST_N AS R_LAST, re.FX AS R_FIRST,
               le.PLACE AS PLACE, (le.ID_N = re.ID_N) AS LABEL,
               ROUND(0.70 * JAROWINKLER_SIMILARITY(le.LAST_N, re.LAST_N) / 100.0
                   + 0.30 * JAROWINKLER_SIMILARITY(le.FX, re.FX) / 100.0, 3) AS SCORE
        FROM le JOIN re ON le.BLOCK = re.BLOCK AND le.REF <> re.REF
        WHERE EDITDISTANCE(le.LAST_N, re.LAST_N) <= {MAX_EDIT_LAST}
        QUALIFY ROW_NUMBER() OVER (PARTITION BY le.REF, re.REF ORDER BY le.BLOCK) = 1
    """


def _blocking_recall(conn, spec: dict) -> dict:
    """The findable-true-match universe (the denominator of the candidate-recall ceiling): all true
    cross-source matches that COULD be found — a left individual whose NPI also exists on the right
    side, both with a non-blank surname. The ceiling's numerator (counted in run()) is how many of
    these SURVIVE the whole candidate pipeline — blocking + the block-size cap + the EDITDISTANCE
    prune — into the scored set; no scorer can recover a true pair that never gets there."""
    L, R = spec["left"], spec["right"]
    l_npi = normalize_sql("NPI", quote_ident(L["id"]))
    r_npi = normalize_sql("NPI", quote_ident(R["id"]))
    l_last = f"UPPER(TRIM({quote_ident(L['last'])}))"
    r_last = f"UPPER(TRIM({quote_ident(R['last'])}))"
    findable = db.scalar(conn, f"""
        SELECT COUNT(*) FROM (
          SELECT DISTINCT {l_npi} AS NPI FROM {db.fqn(L['table'])}
            WHERE {l_last} <> '' AND {l_npi} IS NOT NULL
          INTERSECT
          SELECT DISTINCT {r_npi} FROM {db.fqn(R['table'])}
            WHERE {r_last} <> '' AND {r_npi} IS NOT NULL )""")
    return {"findable_true_matches": int(findable or 0)}


def sweep(rows: list[dict], thresholds) -> tuple[list[dict], int]:
    pos_total = sum(1 for r in rows if r["LABEL"])
    table = []
    for t in thresholds:
        sel = [r for r in rows if float(r["SCORE"]) >= t]
        n = len(sel)
        tp = sum(1 for r in sel if r["LABEL"])
        fp = n - tp
        prec = tp / n if n else 0.0
        rec = tp / pos_total if pos_total else 0.0
        f1 = 2 * prec * rec / (prec + rec) if (prec + rec) else 0.0
        table.append({"t": round(t, 2), "n": n, "tp": tp, "fp": fp,
                      "precision": round(prec, 4), "precision_lo95": round(wilson_lower(tp, n), 4),
                      "recall": round(rec, 4), "f1": round(f1, 4)})
    return table, pos_total


def _freeze_fixture(rows: list[dict], pos_cap: int = 1500, neg_cap: int = 1500, seed: int = 0) -> None:
    """Seeded, balanced sample for the OFFLINE rank-separation test. Balanced (not
    prevalence-preserving) on purpose — it checks the scorer ranks positives above
    negatives; it is NOT a production-precision oracle (precision is prevalence-dependent
    and is read only off the full population in resolve_eval.json). Seeded for reproducibility."""
    FIXTURE.parent.mkdir(parents=True, exist_ok=True)
    pos = [r for r in rows if r["LABEL"]]
    neg = [r for r in rows if not r["LABEL"]]
    rng = random.Random(seed)
    sample = (rng.sample(pos, min(len(pos), pos_cap)) + rng.sample(neg, min(len(neg), neg_cap)))
    with FIXTURE.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["l_last", "l_first", "r_last", "r_first", "place", "label"])
        for r in sample:
            w.writerow([r["L_LAST"], r["L_FIRST"], r["R_LAST"], r["R_FIRST"], r["PLACE"],
                        int(bool(r["LABEL"]))])
    print(f"  froze {len(sample):,} labeled pairs (seeded, balanced) -> {FIXTURE}")


def run(pair: str = "leie_nppes", target: float = 0.99, freeze: bool = True) -> dict:
    if pair not in PAIRS:
        raise SystemExit(f"unknown pair '{pair}'. known: {list(PAIRS)}")
    conn = db.connect()
    try:
        store.ensure_schema(conn)
        _ensure_nickname_map(conn)
        _build_scratch(conn, PAIRS[pair])
        rows = db.dicts(conn, _labeled_sql())
        block_rec = _blocking_recall(conn, PAIRS[pair])
        # persist the labeled gold set
        db.rows(conn, f"CREATE OR REPLACE TABLE {GOLD_FQN} AS {_labeled_sql()}")
    finally:
        conn.close()

    thresholds = [0.80 + 0.01 * i for i in range(0, 20)]  # 0.80 .. 0.99
    table, pos_total = sweep(rows, thresholds)
    labeled = len(rows)            # _labeled_sql forces both sides' NPI non-null -> never None
    pos = pos_total
    neg = labeled - pos

    # candidate-recall ceiling: true entities surviving block + size-cap + editdistance / findable
    blocked_entities = len({r["NPI"] for r in rows if r["LABEL"]})
    findable = block_rec["findable_true_matches"]
    block_ceiling = round(blocked_entities / findable, 4) if findable else None

    # HIGH (auto-merge bar): lowest threshold whose Wilson LOWER bound clears target AND that
    # selects enough pairs to be certifiable. neg==0 -> trivial precision 1.0 -> never recommend.
    high = (None if neg == 0 else
            next((row["t"] for row in table
                  if row["precision_lo95"] >= target and row["n"] >= MIN_BIN_N), None))
    best_f1 = max(table, key=lambda x: x["f1"]) if table else None
    # precision at the TIGHTEST threshold still meeting the recall floor (recall is monotone-
    # decreasing in t) — an apples-to-apples operating point, consistent with match._at_recall
    at_floor = [row for row in table if row["recall"] >= RECALL_FLOOR]
    pf = max(at_floor, key=lambda r: r["t"]) if at_floor else None

    report = {"pair": pair, "labeled_pairs": labeled, "positives": pos, "negatives": neg,
              "prevalence": round(pos / labeled, 6) if labeled else None,
              "target_precision": target, "min_bin_n": MIN_BIN_N,
              "recommend_HIGH": high, "recommend_MIN_SCORE_bestF1": best_f1["t"] if best_f1 else None,
              "precision_at_recall_floor": ({"recall_floor": RECALL_FLOOR, "threshold": pf["t"],
                                             "precision": pf["precision"],
                                             "precision_lo95": pf["precision_lo95"],
                                             "recall": pf["recall"]} if pf else None),
              "candidate_recall": {"findable_true_matches": findable,
                                   "survived_to_scoring": blocked_entities, "ceiling": block_ceiling,
                                   "note": "numerator = block + size-cap + editdistance-prune survivors"},
              "current_HIGH": HIGH, "current_MIN_SCORE": MIN_SCORE, "sweep": table}
    OUT.mkdir(exist_ok=True)
    (OUT / "resolve_eval.json").write_text(json.dumps(report, indent=2))

    print(f"\neval [{pair}]: {labeled:,} labeled pairs "
          f"({pos:,} same-person / {neg:,} different, prevalence {report['prevalence']})")
    print(f"  candidate ceiling: {blocked_entities:,}/{findable:,} findable true matches survive "
          f"blocking+cap+editdistance into the scored set = recall can't exceed {block_ceiling}")
    print(f"  {'thr':>5} {'n':>7} {'prec':>7} {'prec_lo':>7} {'recall':>7} {'f1':>7}")
    for row in table:
        mark = ("  <- HIGH" if row["t"] == high else
                ("  <- bestF1" if best_f1 and row["t"] == best_f1["t"] else ""))
        print(f"  {row['t']:>5} {row['n']:>7} {row['precision']:>7.3f} {row['precision_lo95']:>7.3f} "
              f"{row['recall']:>7.3f} {row['f1']:>7.3f}{mark}")
    if pf:
        print(f"\n  precision @ recall>={RECALL_FLOOR}: {pf['precision']:.3f} "
              f"(lo95 {pf['precision_lo95']:.3f}, recall {pf['recall']:.3f}, thr {pf['t']})")
    print(f"  recommend HIGH (precision_lo95>={target}, n>={MIN_BIN_N}) = {high}   "
          f"best-F1 MIN_SCORE = {best_f1['t'] if best_f1 else None}   "
          f"(current HIGH={HIGH}, MIN_SCORE={MIN_SCORE})")
    print(f"  wrote {OUT / 'resolve_eval.json'} + {GOLD_FQN}")
    if freeze:
        _freeze_fixture(rows)
    return report


if __name__ == "__main__":
    run()
