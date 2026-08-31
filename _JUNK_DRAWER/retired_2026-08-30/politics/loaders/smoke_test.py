"""Phase 1 SMOKE TEST -- the must-pass gate.

Picks a well-known SITTING senator and confirms END TO END, against live data:
  (a) bioguide -> icpsr  resolves to their real Voteview DW-NOMINATE ideology score
  (b) bioguide -> fec_id (via the member_fec_id bridge) resolves to real FEC
      committee data (FED_FEC_BULK committee master, already landed).

Read-only. Prints a plain-English receipt and PASS/FAIL.
"""
from __future__ import annotations
import sys
from pathlib import Path as _RepoPath
_REPO = _RepoPath(__file__).resolve().parents[2]
sys.path.insert(0, str(_REPO / "library-onboarding"))
import snow  # noqa: E402

MARTS = "LIBRARY_MARTS.POLITICS"
# Recognizable sitting senators to prefer (any that resolves both legs wins).
PREFER = ["Sanders", "Warren", "Schumer", "McConnell", "Cruz", "Murkowski", "Sinema", "Booker"]


def q(cur, sql, params=()):
    cur.execute(sql, params)
    cols = [c[0] for c in cur.description]
    return [dict(zip(cols, r)) for r in cur.fetchall()]


def main():
    conn = snow.connect()
    cur = conn.cursor()
    try:
        # Candidates: current senators with BOTH an ideology score AND >=1 fec_id
        # that appears as a candidate in the FEC committee master.
        cands = q(cur, f"""
            SELECT DISTINCT s.bioguide, s.full_name, s.party, s.state,
                   s.icpsr, s.dw_nominate_dim1, s.ideology_label
            FROM {MARTS}.POLITICS__MEMBER_SPINE s
            JOIN {MARTS}.POLITICS__MEMBER_FEC_ID b ON b.bioguide = s.bioguide
            JOIN LIBRARY_RAW.LANDING.FED_FEC_BULK fb ON fb.FEC_CAND_ID = b.fec_id
            WHERE s.legislator_set = 'current'
              AND s.last_term_type = 'sen'
              AND s.has_ideology
        """)
        if not cands:
            print("FAIL: no current senator resolves both legs.")
            sys.exit(1)

        target = None
        for name in PREFER:
            for c in cands:
                if name.lower() in (c["FULL_NAME"] or "").lower():
                    target = c
                    break
            if target:
                break
        target = target or sorted(cands, key=lambda c: c["FULL_NAME"])[0]

        bio = target["BIOGUIDE"]
        print("=" * 74)
        print(f"SMOKE TEST -- {target['FULL_NAME']}  ({target['PARTY']}-{target['STATE']})")
        print(f"bioguide = {bio}")
        print("=" * 74)

        # --- Leg A: bioguide -> icpsr -> Voteview ideology (independent re-pull) ---
        legA = q(cur, """
            SELECT v.icpsr, v.bioname, v.party_code, v.state_abbrev,
                   v.nominate_dim1, v.nominate_dim2, v.congress
            FROM LIBRARY_STAGING.POLITICS.STG_FED_VOTEVIEW_MEMBERS__IDEOLOGY v
            WHERE v.icpsr = %s
            ORDER BY v.congress DESC LIMIT 1
        """, (target["ICPSR"],))
        print("\n[A] bioguide -> icpsr -> Voteview DW-NOMINATE ideology")
        print(f"    crosswalk icpsr            : {target['ICPSR']}")
        if legA:
            a = legA[0]
            print(f"    Voteview bioname           : {a['BIONAME']}")
            print(f"    Voteview latest congress   : {a['CONGRESS']}  ({a['PARTY_CODE']}, {a['STATE_ABBREV']})")
            print(f"    DW-NOMINATE dim1 (ideology): {a['NOMINATE_DIM1']}   dim2: {a['NOMINATE_DIM2']}")
            print(f"    spine ideology_label       : {target['IDEOLOGY_LABEL']}")
            legA_ok = a["NOMINATE_DIM1"] is not None and a["ICPSR"] == target["ICPSR"]
        else:
            legA_ok = False
            print("    NO Voteview row -- FAIL")

        # --- Leg B: bioguide -> fec_id (bridge) -> FEC committee master ---
        legB = q(cur, f"""
            SELECT b.fec_id, fb.FEC_CMTE_ID, fb.CMTE_NM, fb.CMTE_TP, fb.CMTE_DSGN,
                   fb.CMTE_PTY_AFFILIATION, fb.CMTE_ST
            FROM {MARTS}.POLITICS__MEMBER_FEC_ID b
            JOIN LIBRARY_RAW.LANDING.FED_FEC_BULK fb ON fb.FEC_CAND_ID = b.fec_id
            WHERE b.bioguide = %s
            ORDER BY fb.CMTE_DSGN
        """, (bio,))
        print("\n[B] bioguide -> fec_id (bridge) -> FEC committee master (FED_FEC_BULK)")
        all_fec = q(cur, f"SELECT fec_id FROM {MARTS}.POLITICS__MEMBER_FEC_ID WHERE bioguide=%s", (bio,))
        print(f"    member_fec_id bridge       : {[r['FEC_ID'] for r in all_fec]}")
        for r in legB:
            print(f"    cand {r['FEC_ID']} -> cmte {r['FEC_CMTE_ID']}  "
                  f"[{r['CMTE_TP']}/{r['CMTE_DSGN']}]  {r['CMTE_NM']}")
        legB_ok = len(legB) > 0

        print("\n" + "=" * 74)
        print(f"  Leg A (icpsr -> ideology)      : {'PASS' if legA_ok else 'FAIL'}")
        print(f"  Leg B (fec_id -> FEC committee): {'PASS' if legB_ok else 'FAIL'}")
        verdict = "PASS" if (legA_ok and legB_ok) else "FAIL"
        print(f"  SMOKE TEST: {verdict}")
        print("=" * 74)
        sys.exit(0 if verdict == "PASS" else 1)
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    main()
