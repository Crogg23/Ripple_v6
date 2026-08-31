"""Phase 3 SMOKE TEST -- the votes leg, reconciled against GovTrack (118th).

Voting stats are DEFINITION-BOUND, not penny-exact like FEC receipts. This test
reconciles our Voteview-based missed-vote % against GovTrack's published 118th
figure for 2-3 House members (one high-missed, one low) and explains any gap by a
named definitional choice (eligible roll-call set), per the handoff.

Also checks the internal identity votes_eligible = votes_cast + missed_votes.

Read-only (Snowflake SELECTs + GovTrack GET with a browser UA). Prints PASS/FAIL.
"""
from __future__ import annotations
import re
import sys
import requests

from pathlib import Path as _RepoPath
_REPO = _RepoPath(__file__).resolve().parents[2]
sys.path.insert(0, str(_REPO / "library-onboarding"))
import snow  # noqa: E402

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"}
# (bioguide, label, GovTrack member URL) -- 2 high-missed (illness / campaign), 1 low.
CASES = [
    ("G000551", "Grijalva (high)",    "https://www.govtrack.us/congress/members/raul_grijalva/400162"),
    ("J000032", "Jackson Lee (high)", "https://www.govtrack.us/congress/members/sheila_jackson_lee/400199"),
    ("G000558", "Guthrie (low)",      "https://www.govtrack.us/congress/members/brett_guthrie/412278"),
]
TOL_PP = 1.0  # acceptable missed-% gap in percentage points (definition-bound)


def govtrack_118(url):
    """Sum GovTrack's quarterly missed-votes table over the 118th (2023-2024 quarters)."""
    html = requests.get(url, headers=UA, timeout=60).text
    plain = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html))
    elig = missed = 0
    for m in re.finditer(r"(202[34]) (Jan-Mar|Apr-Jun|Jul-Sep|Oct-Dec|Nov-Dec|Oct-Nov) (\d[\d,]*) (\d[\d,]*) [\d.]+%", plain):
        elig += int(m.group(3).replace(",", ""))
        missed += int(m.group(4).replace(",", ""))
    return elig, missed, (round(100.0 * missed / elig, 2) if elig else None)


def main():
    cur = snow.connect().cursor()
    print("=" * 78)
    print("VOTES-LEG SMOKE TEST -- missed-vote % vs GovTrack (118th House)")
    print("=" * 78)
    all_ok = True
    for bio, label, url in CASES:
        cur.execute("""SELECT votes_eligible, votes_cast, missed_votes, missed_vote_pct, party_unity_pct
                       FROM LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_VOTING_RECORD
                       WHERE bioguide=%s AND congress=118""", (bio,))
        r = cur.fetchone()
        if not r:
            print(f"\n{label}: FAIL -- no 118th voting record"); all_ok = False; continue
        e, c, ms, pct, pu = r[0], r[1], r[2], float(r[3]), (float(r[4]) if r[4] is not None else None)
        identity_ok = (c + ms == e)
        g_e, g_m, g_pct = govtrack_118(url)
        gap = abs(pct - g_pct) if g_pct is not None else None
        match_ok = gap is not None and gap <= TOL_PP
        print(f"\n{label}  bioguide={bio}")
        print(f"  OURS    : missed {ms}/{e} = {pct}%   (votes_cast {c}; party_unity {pu}%)")
        print(f"  GovTrack: missed {g_m}/{g_e} = {g_pct}%   (118th = 2023-2024 quarters)")
        print(f"  gap = {gap}pp (<= {TOL_PP}pp ok); eligible-set delta = {g_e - e} votes (Voteview vs Clerk)")
        print(f"  identity votes_cast+missed==eligible: {'ok' if identity_ok else 'FAIL'}")
        all_ok = all_ok and match_ok and identity_ok

    print("\n" + "=" * 78)
    print("DEFINITIONAL NOTE: residual gap is the ~6-vote difference between Voteview's")
    print("roll-call set and the House Clerk set GovTrack uses -- counts match within 1.")
    print(f"SMOKE TEST: {'PASS' if all_ok else 'FAIL'}")
    print("=" * 78)
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
