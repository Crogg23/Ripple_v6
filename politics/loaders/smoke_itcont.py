"""TASK A REFEREE -- the itcont (itemized individual donations) reconciliation gate.

This is the whole point of Task A: a naive "donations per member" off the 84M-row
itcont firehose gave a plausible-but-WRONG answer THREE times before it was right.
This referee ties our itcont sum to an INDEPENDENT FEC truth for clean committees,
so a money mart that doesn't reconcile never gets trusted (the publish-safety
cardinal sin: a wrong figure about a named person).

The PROVEN definition (locked by this referee 2026-06-30): itemized individual
contributions = SUM of transaction types 15 (direct) + 15E (earmarked-received),
MEMO_CD <> 'X', NET of reattributions/redesignations (the negative 15/15E lines --
do NOT filter amt>0, or you OVERSTATE a long-lived committee: Cruz +2.33% un-netted,
-0.10% netted), cycle assigned by TRANSACTION_DT year. The conduit copies (ActBlue/
WinRed 15/24T) never appear because we restrict to a member's authorized (P/A)
committees, so there is no earmark double-count to undo.

Two referees, strongest first:

  [1] OpenFEC committee totals (network, strong).  For a clean candidate committee,
      our itcont itemized-individual sum (the proven definition above) must tie to
      OpenFEC /committee/{id}/totals/ -> individual_itemized_contributions, within a
      tight tolerance. ABORTS on non-200 (never reconcile against an error/throttle
      page). Uses OPENFEC_API_KEY if set, else DEMO_KEY (proven in smoke_money.py).

  [2] FED_FEC_BULK_SUMMARY ratio (offline, no key).  Rolled up committee->candidate,
      our itemized individual sum must be > 0 and <= the FEC's own per-candidate
      TTL_INDIV_CONTRIB (itemized is a SUBSET of total individual -- itcont has no
      unitemized), with the ratio in a sane band. Runs with zero network so the gate
      is never blind.

It also prints, per test committee, the sum under several candidate transaction-type
definitions next to the OpenFEC figure -- so the EXACT correct definition is proven
empirically, not assumed, then baked into build_indiv_donations.py.

Read-only. Prints a receipt + PASS/FAIL; exit 0 = pass.

  python politics/loaders/smoke_itcont.py
"""
from __future__ import annotations

import os
import sys

from pathlib import Path as _RepoPath
_REPO = _RepoPath(__file__).resolve().parents[2]
sys.path.insert(0, str(_REPO))
sys.path.insert(0, str(_REPO / "library-onboarding"))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(str(_REPO / "library-onboarding" / ".env"), override=True)

import snow  # noqa: E402

from loadkit import smoke  # noqa: E402

ITCONT = "LIBRARY_RAW.LANDING.FED_FEC_INDIV_CONTRIBUTIONS"
M = "LIBRARY_MARTS.POLITICS"
CYCLE = "2024"
CYCLE_YEARS = ("2023", "2024")  # TRANSACTION_DT (MMDDYYYY) years that map to the 2024 cycle
OPENFEC_KEY = os.environ.get("OPENFEC_API_KEY", "").strip() or "DEMO_KEY"

# Clean test committees: single-authorized-committee 2024 Senate principals. New-cycle
# campaigns first (zero cross-cycle date leakage), then a long-lived well-known one.
TESTS = [
    ("Elissa Slotkin",       "S001208", "C00834218"),
    ("Angela D. Alsobrooks", "A000382", "C00840017"),
    ("Bernie Moreno",        "M001242", "C00837484"),
    ("Ted Cruz",             "C001098", "C00492785"),
]

# The reconcile tolerance. itcont (bulk) vs OpenFEC (live) differ by the cycle-by-date
# vs cycle-by-file boundary + late amendments. NETTED, the 4 test committees land
# within 0.54% (conservative -- at/under FEC), so 0.8% OR $75k catches a real
# definitional error (the un-netted +2.33% bug) without false-failing on bulk noise.
TOL_PCT = 0.008
TOL_ABS = 75_000.0
RATIO_BAND = (0.40, 1.001)  # itemized / TTL_INDIV_CONTRIB sane band (itemized <= total)


def itcont_breakdown(cur, cmte_id: str):
    """All candidate definitions for one committee+cycle, in ONE pass over itcont.
    Dollar sums are NETTED (all signs -> reattributions/redesignations net out, as in
    the FEC reported total); n_pos is the positive contribution count (a volume proxy
    -- reattribution adjustments are not new contributions)."""
    cur.execute(
        f"""
        SELECT
          SUM(IFF(TRANSACTION_TP IN ('15','15E'), amt, 0))                    AS def_15_15e,
          SUM(IFF(TRANSACTION_TP IN ('15','15E','15C'), amt, 0))              AS def_plus_15c,
          SUM(IFF(TRANSACTION_TP IN ('15','15E','15C','11'), amt, 0))         AS def_plus_11,
          SUM(IFF(TRANSACTION_TP IN ('15','15E') AND amt > 0, amt, 0))        AS def_pos_only,
          SUM(IFF(TRANSACTION_TP = '15',  amt, 0))                            AS t15,
          SUM(IFF(TRANSACTION_TP = '15E', amt, 0))                            AS t15e,
          SUM(IFF(TRANSACTION_TP = '15C', amt, 0))                            AS t15c,
          SUM(IFF(TRANSACTION_TP = '11',  amt, 0))                            AS t11,
          SUM(IFF(amt < 0, 1, 0))                                             AS n_neg,
          SUM(IFF(amt < 0, amt, 0))                                           AS neg_sum,
          SUM(IFF(amt > 0, 1, 0))                                             AS n_pos
        FROM (
          SELECT TRANSACTION_TP, TRY_TO_DECIMAL(TRANSACTION_AMT,18,2) AS amt, MEMO_CD
          FROM {ITCONT}
          WHERE CMTE_ID = %s
            AND TRANSACTION_TP IN ('15','15E','15C','11')
            AND SUBSTR(TRANSACTION_DT,5,4) IN ({','.join("'%s'" % y for y in CYCLE_YEARS)})
        )
        WHERE COALESCE(MEMO_CD,'') <> 'X'
        """,
        (cmte_id,),
    )
    cols = [c[0] for c in cur.description]
    return dict(zip(cols, cur.fetchone()))


def openfec_committee_totals(cmte_id: str) -> dict | None:
    """OpenFEC /committee/{id}/totals/ for the cycle. ABORTS (raises) on non-200."""
    url = f"https://api.open.fec.gov/v1/committee/{cmte_id}/totals/"
    data = smoke.fetch_referee(
        url, params={"api_key": OPENFEC_KEY, "cycle": CYCLE, "per_page": 1}
    )
    res = data.get("results") or []
    return res[0] if res else None


def candidate_rollup(cur, bioguide: str):
    """Our itemized individual sum rolled up to the member, vs FEC TTL_INDIV_CONTRIB."""
    cur.execute(
        f"""
        WITH cmte AS (
          SELECT DISTINCT lk.cmte_id
          FROM {M}.POLITICS__FEC_CAND_CMTE_LINK lk
          JOIN {M}.POLITICS__MEMBER_FEC_ID b ON b.fec_id = lk.cand_id
          WHERE b.bioguide = %s AND lk.cmte_dsgn IN ('P','A')
        ),
        itc AS (
          SELECT SUM(TRY_TO_DECIMAL(i.TRANSACTION_AMT,18,2)) AS itemized
          FROM {ITCONT} i JOIN cmte c ON c.cmte_id = i.CMTE_ID
          WHERE i.TRANSACTION_TP IN ('15','15E')
            AND COALESCE(i.MEMO_CD,'') <> 'X'
            AND SUBSTR(i.TRANSACTION_DT,5,4) IN ({','.join("'%s'" % y for y in CYCLE_YEARS)})
        ),
        fec AS (
          SELECT SUM(ttl_indiv_contrib) AS ttl_indiv_contrib
          FROM {M}.POLITICS__FEC_CANDIDATE_SUMMARY fs
          JOIN {M}.POLITICS__MEMBER_FEC_ID b ON b.fec_id = fs.cand_id
          WHERE b.bioguide = %s AND fs.cycle = %s
        )
        SELECT itc.itemized, fec.ttl_indiv_contrib FROM itc, fec
        """,
        (bioguide, bioguide, CYCLE),
    )
    r = cur.fetchone()
    return float(r[0] or 0), float(r[1] or 0)


def main() -> int:
    conn = snow.connect()
    cur = conn.cursor()
    openfec_passes, openfec_attempts, openfec_real_fail, openfec_unavail = 0, 0, 0, 0
    offline_pass = True
    chosen_def = None
    try:
        print("=" * 78)
        print(f"itcont REFEREE -- itemized individual donations, cycle {CYCLE}")
        print(f"OpenFEC key: {'OPENFEC_API_KEY (env)' if OPENFEC_KEY != 'DEMO_KEY' else 'DEMO_KEY'}")
        print("=" * 78)

        for name, bioguide, cmte_id in TESTS:
            print(f"\n### {name}  (bioguide={bioguide}, cmte={cmte_id})")
            bd = itcont_breakdown(cur, cmte_id)
            print(f"  itcont txns (memo<>X, {'+'.join(CYCLE_YEARS)}): "
                  f"{int(bd['N_POS']):,} positive, {int(bd['N_NEG']):,} negative "
                  f"(reattrib/redesig ${float(bd['NEG_SUM']):,.2f})")
            print(f"    type 15  (direct, netted)      : ${float(bd['T15']):>16,.2f}")
            print(f"    type 15E (earmarked, netted)   : ${float(bd['T15E']):>16,.2f}")
            print(f"    DEF 15+15E pos-only (un-netted): ${float(bd['DEF_POS_ONLY']):>16,.2f}  <- overstates")
            print(f"    DEF 15+15E NETTED (publishable): ${float(bd['DEF_15_15E']):>16,.2f}")

            # [1] OpenFEC -- the strong referee. A throttle/error (non-200, e.g. DEMO_KEY
            # 429) is UNAVAILABILITY: degrade to the offline gate, do NOT fail. ONLY a real
            # reconcile MISMATCH (got data, numbers disagree) fails the referee -- that's the
            # signal the definition is off, which is the whole point of the gate.
            tot = None
            try:
                tot = openfec_committee_totals(cmte_id)   # raises SmokeFailure on non-200
            except smoke.SmokeFailure as e:
                openfec_unavail += 1
                print(f"  [OpenFEC] unavailable: {e}")
            except Exception as e:  # network -- degrade to offline, don't crash
                openfec_unavail += 1
                print(f"  [OpenFEC] unavailable ({type(e).__name__}: {e})")
            if tot:
                openfec_attempts += 1
                iic = float(tot.get("individual_itemized_contributions") or 0)
                iuc = float(tot.get("individual_unitemized_contributions") or 0)
                ic = float(tot.get("individual_contributions") or 0)
                print(f"  [OpenFEC] individual_itemized_contributions : ${iic:>16,.2f}")
                print(f"  [OpenFEC] individual_unitemized             : ${iuc:>16,.2f}")
                print(f"  [OpenFEC] individual_contributions (total)  : ${ic:>16,.2f}")
                # which of our defs ties to OpenFEC itemized? (netted defs + the un-netted control)
                for key in ("DEF_15_15E", "DEF_PLUS_15C", "DEF_PLUS_11", "DEF_POS_ONLY"):
                    mv = float(bd[key])
                    diff = abs(mv - iic)
                    allowed = max(TOL_ABS, abs(iic) * TOL_PCT)
                    tag = "MATCH" if diff <= allowed else "no"
                    print(f"      {key:<14} ${mv:>16,.2f}  | diff ${diff:>14,.2f} ({(mv-iic)/iic:+.2%})  {tag}")
                # the referee assertion: our headline def (netted 15+15E) ties to OpenFEC itemized
                try:
                    res = smoke.reconcile(
                        float(bd["DEF_15_15E"]), iic,
                        label=f"{name} itemized indiv", tol_abs=TOL_ABS, tol_pct=TOL_PCT,
                    )
                    print(f"  [OpenFEC] RECONCILE netted 15+15E vs itemized: PASS  ({res.detail})")
                    openfec_passes += 1
                    chosen_def = "15+15E, memo<>'X', NET of reattributions (all signs), cycle-by-date"
                except smoke.SmokeFailure as e:
                    openfec_real_fail += 1
                    print(f"  [OpenFEC] RECONCILE FAILED (definition off): {e}")
            else:
                print("  [OpenFEC] -> relying on offline referee for this committee")

            # [2] offline ratio referee vs FEC bulk summary
            itemized, ttl = candidate_rollup(cur, bioguide)
            ratio = (itemized / ttl) if ttl else 0.0
            print(f"  [bulk-summary] member itemized rollup : ${itemized:>16,.2f}")
            print(f"  [bulk-summary] FEC TTL_INDIV_CONTRIB  : ${ttl:>16,.2f}   ratio={ratio:.3f}")
            ok = (itemized > 0) and (ttl > 0) and (RATIO_BAND[0] <= ratio <= RATIO_BAND[1])
            print(f"  [bulk-summary] {'PASS' if ok else 'FAIL'} "
                  f"(itemized>0 & 0<ratio<=1 in band {RATIO_BAND})")
            offline_pass = offline_pass and ok

        # verdict
        print("\n" + "=" * 78)
        print(f"  [1] OpenFEC reconcile : {openfec_passes} tied / {openfec_real_fail} mismatched "
              f"/ {openfec_unavail} unavailable (of {len(TESTS)} committees)")
        print(f"  [2] bulk-summary offline ratio gate    : {'PASS' if offline_pass else 'FAIL'}")
        if chosen_def:
            print(f"  PROVEN DEFINITION: itemized individual = types {chosen_def}")
        # FAIL only on: a real OpenFEC reconcile MISMATCH (definition off), or the offline
        # gate breaking. Throttle/unavailability degrades to the offline gate -- the referee
        # stays runnable even when DEMO_KEY is exhausted (offline gate is independent evidence).
        hard = offline_pass and (openfec_real_fail == 0)
        if openfec_real_fail:
            print(f"  NOTE: {openfec_real_fail} committee(s) had a real OpenFEC mismatch -> definition off.")
        if openfec_passes == 0 and openfec_unavail:
            print("  NOTE: OpenFEC was unavailable (throttled) -- leaned on the offline ratio gate.")
        print(f"  REFEREE: {'PASS' if hard else 'FAIL'}")
        print("=" * 78)
        return 0 if hard else 1
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    sys.exit(main())
