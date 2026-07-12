"""Regression locks on the confidence ladder — Move 4 of RIPPLE_GOVERN_THYSELF.

OFFLINE: no Snowflake, no network. Fixtures were built by ONE warehouse read
(scripts/build_ladder_fixture.py, 2026-07-12) from the calibration's own held-out
split (by person, MOD(ABS(HASH(NPI)),2)=1):

  fixtures/ladder_holdout.parquet   54k test-split candidate pairs: three-state
                                    agree flags, surname TF, label, in-SQL M
  fixtures/ladder_blocking.parquet  block sets per record for 3,468 true persons
  fixtures/ladder_model.json        MATCH_MODEL m/u + rungs + live counts

The five locks, in order of importance:
  1. auto-merge (>=0.99 precision) structurally unreachable at current calibration
  2. NPI is a label, never a feature — structural + behavioral
  3. CONFIRMED precision stays in its measured band — fails on drop AND on a
     suspicious jump (a model that suddenly got better started cheating)
  4. 3-pass blocking recall >= 0.95 (the 23.7% -> 95.9% fix, now guarded)
  5. the publish gate refuses anything without a human sign-off

RED DRILL — a test that has never failed is a test you don't know works. Each
lock has a documented corruption, switched by the LADDER_RED env var, that MUST
make it fail: auto_merge | leakage | band | recall | gate. Run e.g.
  LADDER_RED=recall pytest tests/test_ladder_invariants.py -k recall   # must FAIL
"""
from __future__ import annotations

import json
import math
import os
import re
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from connect import calibrate, leads
from connect.evaluate import wilson_lower

FIX = Path(__file__).resolve().parent / "fixtures"
RED = os.environ.get("LADDER_RED", "")

AUTO_MERGE_BAR = 0.99          # recommend_HIGH: if any rung's lower CI clears this, STOP THE LINE
BAND_LO = 0.860                # CONFIRMED calibrated lower 95% CI
BAND_HI = 0.950                # suspicious-jump ceiling — better than this means cheating
RECALL_FLOOR = 0.95
COVERAGE_BAND = (0.40, 0.55)   # CONFIRMED coverage_recall, calibrated 0.4615


@pytest.fixture(scope="module")
def sidecar() -> dict:
    return json.loads((FIX / "ladder_model.json").read_text())


@pytest.fixture(scope="module")
def holdout() -> pd.DataFrame:
    df = pd.read_parquet(FIX / "ladder_holdout.parquet")
    if RED == "band":            # RED DRILL: the model 'improved' by 3 bits overnight
        df = df.assign(M_BAND=df["M_BAND"] + 3, M=df["M"] + 3)
    return df


@pytest.fixture(scope="module")
def blocking() -> pd.DataFrame:
    df = pd.read_parquet(FIX / "ladder_blocking.parquet")
    if RED == "recall":          # RED DRILL: naive single-pass blocking (ZIP pass only)
        df = df.assign(BLOCKS=df["BLOCKS"].map(
            lambda s: "||".join(b for b in s.split("||") if b.startswith("z#"))))
    return df


def offline_score(df: pd.DataFrame, model: dict, start: float, mode: str) -> np.ndarray:
    """Pure-python mirror of calibrate._m_expr: agree=log2(m/u), disagree=log2((1-m)/(1-u)),
    can't-compare=0 bits; surname in 'tf' mode uses the surname's term frequency as agree-u.
    Consumes ONLY the three-state flags + TF — no identifier columns exist to consume."""
    def clip(x: float) -> float:
        return min(max(x, 1e-6), 1 - 1e-6)

    M = np.full(len(df), float(start))
    s = model["surname"]
    sm, su = clip(s["m"]), clip(s["u"])
    a = df["A_SUR"].to_numpy(dtype=float)
    tf = df["TF"].to_numpy(dtype=float)
    M += np.where(np.isnan(a), 0.0,
                  np.where(a == 1,
                           np.log2(sm / tf) if mode == "tf" else math.log2(sm / su),
                           math.log2((1 - sm) / (1 - su))))
    for field, col in (("first", "A_FST"), ("zip", "A_ZIP"),
                       ("address", "A_ADDR"), ("middle", "A_MID")):
        m, u = clip(model[field]["m"]), clip(model[field]["u"])
        a = df[col].to_numpy(dtype=float)
        M += np.where(np.isnan(a), 0.0,
                      np.where(a == 1, math.log2(m / u), math.log2((1 - m) / (1 - u))))
    if RED == "leakage":         # RED DRILL: a simulated NPI leak (+5 bits when IDs agree)
        M += 5.0 * df["LABEL"].to_numpy(dtype=float)
    return M


def cum_precision_at(df: pd.DataFrame, min_m: float) -> tuple[float, int, int]:
    sel = df[df["M_BAND"] >= min_m]
    n, tp = len(sel), int(sel["LABEL"].sum())
    return (tp / n if n else 0.0), tp, n


# ── 1. the most important test in the repo ──────────────────────────────────

def test_auto_merge_is_unreachable(holdout, sidecar):
    """No rung — persisted or recomputed at ANY threshold — may clear the 0.99
    auto-merge bar. If this fails, Ripple can auto-publish a name-match as fact
    about a named human being. Nothing that serious rides on 'the numbers came
    out right' — it rides on this test."""
    for r in sidecar["rungs"]:
        assert float(r["MEASURED_PRECISION"]) < AUTO_MERGE_BAR, \
            f"persisted rung {r['RUNG']} claims precision >= {AUTO_MERGE_BAR}"
        assert float(r["MEASURED_PRECISION_LO95"]) < AUTO_MERGE_BAR
    # exhaustive: every possible cut-point on the held-out curve
    if RED == "auto_merge":      # RED DRILL: a cheating model — everything above 11 is 'true'
        holdout = holdout.assign(LABEL=np.where(holdout["M_BAND"] >= 11, 1, holdout["LABEL"]))
    for min_m in sorted(holdout["M_BAND"].unique()):
        _, tp, n = cum_precision_at(holdout, min_m)
        assert wilson_lower(tp, n) < AUTO_MERGE_BAR, \
            f"M>={min_m}: wilson-lower {wilson_lower(tp, n):.4f} clears the auto-merge bar"


# ── 2. NPI is a label, never a feature ──────────────────────────────────────

def test_no_hard_id_leakage(holdout, sidecar):
    """Structural: in the calibration SQL, ID_N may appear only as label / split /
    not-null filter — never inside a feature flag. Behavioral: the in-SQL M in the
    fixture must be reproducible from the NON-ID columns alone; if the SQL ever
    grows an ID-derived feature, recomputed M diverges and this fails."""
    cte = calibrate._feat_cte()
    # segment the SELECT list on its aliases: parts alternate [expr, alias, expr, alias, ...],
    # so each alias's expression is exactly the text since the previous alias — no regex
    # nesting games. ID_N is ALLOWED in LABEL (it IS the label) and SPL (the split key);
    # it is FORBIDDEN in every feature the scorer consumes (A_* and TF).
    parts = re.split(r"\s+AS\s+(LABEL|SPL|A_SUR|A_FST|A_ZIP|A_ADDR|A_MID|TF)\b", cte)
    exprs = {parts[i + 1]: parts[i] for i in range(0, len(parts) - 1, 2)}
    feature_cols = {"A_SUR", "A_FST", "A_ZIP", "A_ADDR", "A_MID", "TF"}
    assert feature_cols <= set(exprs), \
        f"_feat_cte changed shape — missing {feature_cols - set(exprs)}"
    for name in feature_cols:
        assert "ID_N" not in exprs[name] and "NPI" not in exprs[name], \
            f"identifier inside feature {name}"
    tf_join = [ln for ln in cte.splitlines() if "LEFT JOIN" in ln and "tf" in ln.lower()]
    assert tf_join and all("ID_N" not in ln for ln in tf_join)

    model, start, mode = sidecar["model"], sidecar["start_bits"], sidecar["surname_mode"]
    M_off = offline_score(holdout, model, start, mode)
    M_sql = holdout["M"].to_numpy(dtype=float)
    worst = float(np.max(np.abs(M_off - M_sql)))
    assert worst < 1e-4, \
        f"in-SQL M diverges from ID-blind recompute by {worst:.6f} bits — something " \
        f"besides the five features (or a leak) is feeding the score"

    # harness sanity: the metric must be able to see a broken relationship
    rng = np.random.default_rng(19)
    shuffled = holdout.assign(LABEL=rng.permutation(holdout["LABEL"].to_numpy()))
    p_shuf, _, _ = cum_precision_at(shuffled, 11)
    p_real, _, _ = cum_precision_at(holdout, 11)
    assert p_shuf < 0.25 and (RED == "band" or p_real > 0.5), \
        "label shuffle did not collapse precision — the metric has no teeth"


# ── 3. CONFIRMED precision band ─────────────────────────────────────────────

def test_confirmed_precision_band(holdout, sidecar):
    """Fails on a DROP below the calibrated lower CI — and on a suspicious JUMP
    above the ceiling. A model that suddenly got better is a model that started
    cheating. Coverage guarded too: precision held by answering nothing is a lie."""
    confirmed = next(r for r in sidecar["rungs"] if r["RUNG"] == "CONFIRMED")
    min_m = float(confirmed["MIN_M"])
    p, tp, n = cum_precision_at(holdout, min_m)
    assert n >= 300, f"only {n} pairs at CONFIRMED — too few to certify anything"
    assert p >= BAND_LO, f"CONFIRMED precision {p:.4f} fell below the calibrated CI {BAND_LO}"
    assert p <= BAND_HI, f"CONFIRMED precision {p:.4f} jumped above {BAND_HI} — suspicious"
    coverage = tp / sidecar["test_positives_total"]
    assert COVERAGE_BAND[0] <= coverage <= COVERAGE_BAND[1], \
        f"CONFIRMED coverage {coverage:.4f} left its band {COVERAGE_BAND}"


# ── 4. blocking recall ──────────────────────────────────────────────────────

def _editdistance(a: str, b: str) -> int:
    if abs(len(a) - len(b)) > 3:
        return 4
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def test_candidate_recall(blocking, sidecar):
    """Replay the blocking decision offline: a true pair is a candidate iff the two
    records share >=1 block AND surnames are within edit distance 3. The 3-pass
    union earned 95.9% from a naive 23.7% — this is that fix's guard."""
    max_edit = sidecar["blocking"]["max_edit_last"]
    univ = hits = 0
    for _id, grp in blocking.groupby("ID_N"):
        lefts = grp[grp["SIDE"] == "L"]
        rights = grp[grp["SIDE"] == "R"]
        for _, lrow in lefts.iterrows():
            lb = set(lrow["BLOCKS"].split("||")) - {""}
            for _, rrow in rights.iterrows():
                univ += 1
                if lb & set(rrow["BLOCKS"].split("||")) \
                        and _editdistance(lrow["LAST_N"], rrow["LAST_N"]) <= max_edit:
                    hits += 1
    assert univ > 3000, f"blocking universe suspiciously small ({univ})"
    recall = hits / univ
    assert recall >= RECALL_FLOOR, \
        f"blocking recall {recall:.4f} < {RECALL_FLOOR} — a true match can no longer find its block"
    if RED != "recall":   # replay must agree with the in-warehouse measurement
        live = sidecar["blocking"]["recall"]
        assert abs(recall - live) < 0.01, \
            f"offline replay ({recall:.4f}) disagrees with live measurement ({live}) — replay drifted"


# ── 5. the last door before someone's name goes on the internet ─────────────

def test_lead_gate_refuses_unsigned(monkeypatch):
    """leads._gate is the pure core of leads.published(). No human sign-off in
    DECISIONS -> nothing publishes. And the auto_ok hook stays hardwired False —
    the one edited line that could ever change that is pinned right here."""
    if RED == "gate":            # RED DRILL: someone flips the auto-publish hook
        monkeypatch.setattr(leads, "_auto_publishable", lambda r: True)

    juicy = {"LEAD_ID": "L1", "SCORE": 99.9, "CONF_TIER": "CONFIRMED"}
    assert leads._auto_publishable(juicy) is False, \
        "_auto_publishable no longer returns False unconditionally — auto-publish door is open"

    rows = [{"LEAD_ID": "L1", "SCORE": 99.9}, {"LEAD_ID": "L2", "SCORE": 0.1}]
    gated = leads._gate([dict(r) for r in rows], decisions={})
    assert all(r["PUBLISHED"] is False for r in gated), "a lead published with zero human decisions"
    assert all(r["REVIEW_STATE"] == "pending" for r in gated)
    assert leads._gate([dict(r) for r in rows], decisions={}, only_publishable=True) == []

    confirmed = leads._gate([dict(r) for r in rows], decisions={"L1": "confirmed"})
    by_id = {r["LEAD_ID"]: r for r in confirmed}
    assert by_id["L1"]["PUBLISHED"] is True and by_id["L2"]["PUBLISHED"] is False
