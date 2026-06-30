"""Phase 4 SMOKE TEST -- the bills leg, reconciled against GovTrack's 118th report card.

GovTrack's /report-card/2024 page summarizes the WHOLE 118th Congress (it says so in the
prose: "...in the 118th Congress"). It publishes three numbers that map straight to our stat:
  GovTrack "introduced N bills and resolutions" <-> bills_sponsored      (total, incl. resolutions)
  GovTrack "N bills that became law"             <-> bills_enacted        (became Public Law)
  GovTrack "cosponsored N bills"                 <-> cosponsored_count     (withdrawn excluded)

Members (per the handoff: one high-volume sponsor, one high-enactment/low-volume, one mid):
  Biggs   -- the SPAM example: 612 introduced, 0 enacted (validates we never headline the raw count).
  Graves  -- high-enactment/low-volume: 21 introduced, ~5 enacted (a clean enacted_rate).
  AOC     -- mid-volume control.

EXPECTED RECONCILIATION (reconcile by definition, not decimals):
  * introduced  -> EXACT match (objective sponsored count, incl. resolutions).
  * cosponsored -> EXACT match (withdrawn excluded, same as GovTrack/congress.gov).
  * became_law  -> ours == GovTrack OR ours = GovTrack - {0,1,2}. NAMED divergence: GovTrack counts a
                   bill as enacted "including via incorporation into other measures" (its text folded
                   into a larger enacted bill); we count only a bill's OWN <laws> public-law element --
                   the cleaner, more conservative signal. ours must never EXCEED GovTrack.

Read-only (Snowflake SELECTs + GovTrack GET with a browser UA). Prints PASS/FAIL.
"""
from __future__ import annotations
import re
import sys
import requests

sys.path.insert(0, r"c:\Code\Ripple_v6\library-onboarding")
import snow  # noqa: E402

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"}
# (bioguide, label, govtrack_id)
CASES = [
    ("B001302", "Biggs (high-volume / spam)",      412683),
    ("G000546", "Graves (high-enact / low-vol)",   400158),
    ("O000172", "Ocasio-Cortez (mid control)",     412804),
]
ENACTED_TOL = 2  # GovTrack's "incorporation" counting may exceed ours by a small margin


def _num(pat, text):
    m = re.search(pat, text)
    return int(m.group(1).replace(",", "")) if m else None


def govtrack_118(gtid: int):
    """Resolve the slug via the id redirect, then parse the 118th report card (/report-card/2024)."""
    base = requests.get(f"https://www.govtrack.us/congress/members/{gtid}", headers=UA,
                        timeout=60, allow_redirects=True)
    rc = requests.get(f"{base.url.rstrip('/')}/report-card/2024", headers=UA, timeout=60)
    rc.raise_for_status()
    plain = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", rc.text))
    return {
        "introduced":  _num(r"introduced\s+([\d,]+)\s+bills?\s+and\s+resolutions", plain),
        "enacted":     _num(r"([\d,]+)\s+bills?\s+that\s+became\s+law", plain),
        "cosponsored": _num(r"cosponsored\s+([\d,]+)\s+bills?", plain),
    }


def main():
    cur = snow.connect().cursor()
    print("=" * 80)
    print("BILLS-LEG SMOKE TEST -- vs GovTrack 118th report card (sponsored / enacted / cosponsored)")
    print("=" * 80)
    all_ok = True
    for bio, label, gtid in CASES:
        cur.execute("""SELECT bills_sponsored, bills_sponsored_substantive, resolutions_sponsored,
                              bills_enacted, enacted_rate, cosponsored_count
                       FROM LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_BILL_RECORD
                       WHERE bioguide=%s AND congress=118""", (bio,))
        r = cur.fetchone()
        if not r:
            print(f"\n{label}: FAIL -- no 118th bill record"); all_ok = False; continue
        spon, subst, resol, enac, rate, cospon = r
        g = govtrack_118(gtid)

        intro_ok  = g["introduced"]  == spon
        cospon_ok = g["cosponsored"] == cospon
        # ours must not exceed GovTrack; gap explained by GovTrack's "incorporation" counting
        enac_gap  = (g["enacted"] - enac) if g["enacted"] is not None else None
        enac_ok   = enac_gap is not None and 0 <= enac_gap <= ENACTED_TOL

        print(f"\n{label}  bioguide={bio}")
        print(f"  OURS    : sponsored {spon} (subst {subst} / resol {resol}), enacted {enac} "
              f"(rate {rate}%), cosponsored {cospon}")
        print(f"  GovTrack: introduced {g['introduced']}, became-law {g['enacted']}, cosponsored {g['cosponsored']}")
        print(f"  introduced  : {'MATCH' if intro_ok else 'DIFF'} ({spon} vs {g['introduced']})")
        print(f"  cosponsored : {'MATCH' if cospon_ok else 'DIFF'} ({cospon} vs {g['cosponsored']})")
        print(f"  became_law  : {'OK' if enac_ok else 'DIFF'} ({enac} vs {g['enacted']}; "
              f"gap {enac_gap} = GovTrack 'incorporation', ours = standalone <laws> only)")
        all_ok = all_ok and intro_ok and cospon_ok and enac_ok

    print("\n" + "=" * 80)
    print("DEFINITIONAL NOTE: sponsored + cosponsored match GovTrack to the integer; became_law is")
    print("ours = standalone <laws> public-law only, so GovTrack (which also counts text incorporated")
    print("into other enacted bills) is >= ours by 0-2. Reconciled by definition, not decimals.")
    print(f"SMOKE TEST: {'PASS' if all_ok else 'FAIL'}")
    print("=" * 80)
    cur.close()
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
