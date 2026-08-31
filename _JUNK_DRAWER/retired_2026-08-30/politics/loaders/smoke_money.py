"""Phase 2 SMOKE TEST -- the money spine, end to end + FEC cross-check.

For a well-known sitting senator, confirms against live data:
  (1) the full identity chain resolves:
      bioguide -> fec_cand_id -> FEC_CANDIDATE -> FEC_CAND_CMTE_LINK -> committee master (fed_fec_bulk)
  (2) money-raised (net of inter-committee transfers) for a recent cycle is a sane $ figure
  (3) our gross total receipts MATCHES FEC's published total (OpenFEC API cross-check)

Read-only. Prints a receipt + PASS/FAIL.
"""
from __future__ import annotations
import sys
from pathlib import Path as _RepoPath
_REPO = _RepoPath(__file__).resolve().parents[2]
sys.path.insert(0, str(_REPO / "library-onboarding"))
import snow  # noqa: E402
import requests  # noqa: E402

M = "LIBRARY_MARTS.POLITICS"
CYCLE = "2024"
PREFER = ["W000817", "S000033", "C001098", "S000148"]  # Warren, Sanders, Cruz, Schumer (up in 2024)


def q(cur, sql, p=()):
    cur.execute(sql, p)
    cols = [c[0] for c in cur.description]
    return [dict(zip(cols, r)) for r in cur.fetchall()]


def main():
    conn = snow.connect()
    cur = conn.cursor()
    try:
        # pick a preferred sitting senator who has a 2024 money-raised row
        target = None
        for bio in PREFER:
            rows = q(cur, f"""SELECT bioguide, full_name, party, state, chamber, n_candidate_ids,
                                     cand_ids, ttl_receipts_gross, trans_from_auth, money_raised_net, cash_on_hand_close
                              FROM {M}.POLITICS__MEMBER_MONEY_RAISED
                              WHERE bioguide=%s AND cycle=%s""", (bio, CYCLE))
            if rows:
                target = rows[0]
                break
        if not target:
            print("FAIL: no preferred senator has a 2024 money-raised row")
            sys.exit(1)

        bio = target["BIOGUIDE"]
        print("=" * 74)
        print(f"MONEY-SPINE SMOKE TEST -- {target['FULL_NAME']} ({target['PARTY']}-{target['STATE']}, {target['CHAMBER']})")
        print(f"bioguide={bio}  cycle={CYCLE}")
        print("=" * 74)

        # (1) identity chain: bioguide -> cand_id -> candidate -> linkage -> committee master
        chain = q(cur, f"""
            SELECT b.fec_id AS cand_id, c.cand_name, c.office, c.incumbent_challenger,
                   lk.cmte_id, lk.cmte_dsgn, cm.CMTE_NM
            FROM {M}.POLITICS__MEMBER_FEC_ID b
            JOIN {M}.POLITICS__FEC_CANDIDATE c        ON c.cand_id = b.fec_id AND c.cycle=%s
            JOIN {M}.POLITICS__FEC_CAND_CMTE_LINK lk  ON lk.cand_id = c.cand_id AND lk.cycle=%s
            JOIN LIBRARY_RAW.LANDING.FED_FEC_BULK cm  ON cm.FEC_CMTE_ID = lk.cmte_id
            WHERE b.bioguide=%s
            ORDER BY lk.cmte_dsgn""", (CYCLE, CYCLE, bio))
        print("\n[1] IDENTITY CHAIN  bioguide -> cand_id -> candidate -> linkage -> committee master")
        for r in chain:
            print(f"    cand {r['CAND_ID']} ({r['OFFICE']},{r['INCUMBENT_CHALLENGER']}) -> "
                  f"cmte {r['CMTE_ID']} [{r['CMTE_DSGN']}]  {r['CMTE_NM']}")
        chain_ok = len(chain) > 0

        # (2) the stat
        print("\n[2] MONEY RAISED (cycle 2024)")
        gross = float(target["TTL_RECEIPTS_GROSS"] or 0)
        transfers = float(target["TRANS_FROM_AUTH"] or 0)
        net = float(target["MONEY_RAISED_NET"] or 0)
        print(f"    cand_ids active in cycle : {target['CAND_IDS']} (n={target['N_CANDIDATE_IDS']})")
        print(f"    gross total receipts     : ${gross:,.2f}")
        print(f"    - inter-cmte transfers   : ${transfers:,.2f}")
        print(f"    = MONEY RAISED (net)     : ${net:,.2f}")
        print(f"    cash on hand (close)     : ${float(target['CASH_ON_HAND_CLOSE'] or 0):,.2f}")
        stat_ok = net > 0

        # (3) FEC cross-check via OpenFEC (DEMO_KEY)
        cand_id = (target["CAND_IDS"] or "").strip('[]\n" ').split(",")[0].strip().strip('"')
        print(f"\n[3] FEC CROSS-CHECK (OpenFEC) for cand {cand_id}, cycle {CYCLE}")
        fec_ok = None
        fec_receipts = None
        try:
            url = f"https://api.open.fec.gov/v1/candidate/{cand_id}/totals/"
            resp = requests.get(url, params={"api_key": "DEMO_KEY", "cycle": CYCLE,
                                             "full_election": "false"}, timeout=60)
            if resp.status_code == 200 and resp.json().get("results"):
                res = resp.json()["results"][0]
                fec_receipts = float(res.get("receipts") or 0)
                print(f"    OpenFEC published receipts: ${fec_receipts:,.2f}")
                print(f"    our gross total receipts  : ${gross:,.2f}")
                if fec_receipts > 0:
                    diff = abs(fec_receipts - gross) / fec_receipts
                    print(f"    relative difference       : {diff:.4%}")
                    fec_ok = diff < 0.01  # within 1%
            else:
                print(f"    OpenFEC unavailable (status {resp.status_code}); reporting our figure only.")
        except Exception as e:
            print(f"    OpenFEC call failed ({e}); reporting our figure only.")

        print("\n" + "=" * 74)
        print(f"  [1] identity chain resolves        : {'PASS' if chain_ok else 'FAIL'}")
        print(f"  [2] money-raised is a sane $ figure : {'PASS' if stat_ok else 'FAIL'}")
        fc = ('PASS' if fec_ok else 'MISMATCH') if fec_ok is not None else 'SKIPPED (API unavailable)'
        print(f"  [3] matches FEC published total     : {fc}")
        hard = chain_ok and stat_ok and (fec_ok is not False)  # FEC mismatch fails; skip is tolerated
        print(f"  SMOKE TEST: {'PASS' if hard else 'FAIL'}")
        print("=" * 74)
        sys.exit(0 if hard else 1)
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    main()
