"""TASK B REFEREE -- prove POLITICS__WHO_WON is right against known truth, and show the
payoff: winners joined to Task A money.

MEDSL carries NO FEC/ICPSR (the brief was wrong), so the spine join is name+state+chamber
-- a fuzzy, LEAD-grade match. This referee measures it honestly and checks the winners
against facts you can verify (seat counts; named 2024 winners; the 2024 Senate = current
senators set).

Read-only. Prints a receipt + PASS/FAIL.
  python politics/loaders/smoke_who_won.py
"""
from __future__ import annotations
import sys
sys.path.insert(0, r"c:\Code\Ripple_v6"); sys.path.insert(0, r"c:\Code\Ripple_v6\library-onboarding")
from dotenv import load_dotenv
load_dotenv(r"c:\Code\Ripple_v6\library-onboarding\.env", override=True)
import snow  # noqa: E402

W = "LIBRARY_MARTS.POLITICS.POLITICS__WHO_WON"
M = "LIBRARY_MARTS.POLITICS"
fails = []


def q(cur, sql, p=()):
    cur.execute(sql, p); cols=[c[0] for c in cur.description]
    return [dict(zip(cols, r)) for r in cur.fetchall()]


def main():
    conn = snow.connect(); cur = conn.cursor()
    try:
        print("="*78); print("WHO_WON REFEREE"); print("="*78)

        # 1. SEAT-COUNT SANITY: a normal cycle = 435 House, 33-35 Senate, 51 President states.
        print("\n[1] seat-count sanity (recent cycles)")
        for r in q(cur, f"""SELECT office, year, COUNT(*) seats FROM {W}
                            WHERE (office='HOUSE' AND year IN (2016,2018))
                               OR (office='SENATE' AND year IN (2020,2022,2024))
                               OR (office='PRESIDENT' AND year IN (2012,2016))
                            GROUP BY 1,2 ORDER BY 1,2"""):
            print(f"    {r['OFFICE']:<9} {r['YEAR']}: {r['SEATS']} winners")
        house = q(cur, f"SELECT COUNT(*) n FROM {W} WHERE office='HOUSE' AND year=2018")[0]["N"]
        sen24 = q(cur, f"SELECT COUNT(*) n FROM {W} WHERE office='SENATE' AND year=2024")[0]["N"]
        ok1 = (420 <= house <= 440) and (30 <= sen24 <= 36)
        if not ok1: fails.append("seat-count sanity")
        print(f"    -> House 2018={house} (~435), Senate 2024={sen24} (~34): {'PASS' if ok1 else 'FAIL'}")

        # 2. NAMED 2024 WINNERS spot-check (facts you can verify by memory/news)
        print("\n[2] named 2024 winner spot-checks")
        known = {("SENATE","TX"):"Cruz", ("SENATE","MI"):"Slotkin", ("SENATE","OH"):"Moreno",
                 ("SENATE","AZ"):"Gallego", ("SENATE","PA"):"McCormick"}
        ok2 = True
        for (off,st),sur in known.items():
            r = q(cur, f"SELECT winner, bioguide, spine_name, ROUND(margin_pct*100,1) m FROM {W} "
                       f"WHERE office=%s AND state=%s AND year=2024 AND NOT is_special", (off,st))
            got = r[0] if r else {}
            hit = sur.upper() in (got.get("WINNER") or "").upper()
            ok2 = ok2 and hit
            print(f"    {off} {st} 2024: {got.get('WINNER','<none>'):<22} margin {got.get('M')}pp  "
                  f"-> {got.get('BIOGUIDE') or 'unmatched'}  {'OK' if hit else 'MISMATCH'}")
        if not ok2: fails.append("named winner spot-check")

        # 3. 2024 SENATE = the set of current senators who won in 2024 (the verifiable closed set)
        print("\n[3] 2024 Senate winners -> matched to a CURRENT senator")
        m = q(cur, f"""SELECT COUNT(*) winners, SUM(IFF(bioguide IS NOT NULL,1,0)) matched,
                         ROUND(SUM(IFF(bioguide IS NOT NULL,1,0))/COUNT(*),3) rate
                       FROM {W} WHERE office='SENATE' AND year=2024""")[0]
        print(f"    {m['MATCHED']}/{m['WINNERS']} matched = {m['RATE']}")
        un = q(cur, f"""SELECT state, winner FROM {W}
                        WHERE office='SENATE' AND year=2024 AND bioguide IS NULL ORDER BY state""")
        for r in un: print(f"      unmatched: {r['STATE']}  {r['WINNER']}  (name-normalization or non-member)")
        ok3 = m["RATE"] >= 0.90
        if not ok3: fails.append("2024 senate match rate")
        print(f"    -> match rate >= 0.90: {'PASS' if ok3 else 'FAIL'}")

        # 4. THE PAYOFF: 2024 Senate winners x Task A money (itemized individual donations)
        print("\n[4] PAYOFF -- 2024 Senate winners x money raised from individuals (Task A)")
        pay = q(cur, f"""
          SELECT w.state, w.spine_name, w.winner_party,
                 ROUND(w.margin_pct*100,1) margin_pp,
                 d.itemized_indiv
          FROM {W} w
          JOIN {M}.POLITICS__MEMBER_INDIV_DONATIONS d ON d.bioguide=w.bioguide AND d.cycle='2024'
          WHERE w.office='SENATE' AND w.year=2024 AND w.bioguide IS NOT NULL
          ORDER BY d.itemized_indiv DESC LIMIT 8""")
        print("    winner                     party  margin   itemized individual $")
        for r in pay:
            print(f"    {r['SPINE_NAME']:<26} {(r['WINNER_PARTY'] or '')[:3]:<4} {str(r['MARGIN_PP'])+'pp':>7}   "
                  f"${float(r['ITEMIZED_INDIV'] or 0):>15,.0f}")
        ok4 = len(pay) >= 5
        if not ok4: fails.append("money join payoff")
        print(f"    -> who-won joins to who-raised: {'PASS' if ok4 else 'FAIL'} ({len(pay)} winners with money)")

        # 5. margin sanity: every winner's margin >= 0 and vote_share in (0,1]
        bad = q(cur, f"""SELECT COUNT(*) n FROM {W}
                         WHERE margin_votes < 0 OR vote_share <= 0 OR vote_share > 1.0001""")[0]["N"]
        print(f"\n[5] margin/vote-share sanity (must be 0 bad rows): {bad}")
        if bad: fails.append("margin sanity")

        print("\n"+"="*78)
        print(f"  REFEREE: {'ALL PASS' if not fails else 'FAILURES: '+', '.join(fails)}")
        print("="*78)
        return 0 if not fails else 1
    finally:
        cur.close(); conn.close()


if __name__ == "__main__":
    sys.exit(main())
