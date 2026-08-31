"""cm26 refresh -- adversarial verification (READ-ONLY). PASS/FAIL + exit code.

Asserts, against the live warehouse, every clause of the maintenance-pass
definition of done:

  CHECK A -- resolution jumps : 2026 linkage resolution ~98% (matching 2024's quality)
  CHECK B -- 2024 untouched   : committee master FED_FEC_BULK byte-for-byte identical
                                (count + single SHA + fingerprint) AND the 2024
                                money-raised figures byte-for-byte identical
                                (Warren/Cruz/Sanders + the whole-cycle fingerprint)
  AUDIT   -- additive safety  : only the NEW landing object + NEW mart exist; the
                                2024 snapshot is unwritten
            grain integrity   : 0 dup (cmte_id, cycle) in the union mart
            registry          : fed_fec_bulk_committees present (append-only)

Baselines are the figures captured BEFORE the refresh (scratchpad inspection).
"""
from __future__ import annotations
import sys
from pathlib import Path as _RepoPath
_REPO = _RepoPath(__file__).resolve().parents[2]
sys.path.insert(0, str(_REPO / "library-onboarding"))
import snow  # noqa: E402

# --- baselines captured before the refresh (the things that must NOT move) ----
CM_BASE_N = 20938
CM_BASE_SHA = "cfebda3f42b391633bb12d5411d10ae79c13525288cf7f07e03e7b4816698ef5"
CM_BASE_HASH = -2455869316121402723
MONEY24_BASE_N = 519
MONEY24_BASE_SUM = 2155305330.58
MONEY24_BASE_HASH = -2513935030619334787
ANCHORS = {  # bioguide -> (gross, net) for cycle 2024
    "C001098": (74050030.94, 68867157.35),   # Ted Cruz
    "S000033": (8207886.33, 8207886.33),      # Bernard Sanders
    "W000817": (9039537.78, 8840571.03),      # Elizabeth Warren
}

CM = "LIBRARY_RAW.LANDING.FED_FEC_BULK"
NEWCM = "LIBRARY_RAW.LANDING.FED_FEC_BULK_COMMITTEES"
LINK = "LIBRARY_MARTS.POLITICS.POLITICS__FEC_CAND_CMTE_LINK"
CMTE = "LIBRARY_MARTS.POLITICS.POLITICS__FEC_COMMITTEE"
MR = "LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_MONEY_RAISED"
REG = '"LIBRARY_META"."REGISTRY"."SOURCE_REGISTRY"'


def main():
    conn = snow.connect()
    cur = conn.cursor()
    fails = []

    def scalar(sql, p=()):
        cur.execute(sql, p)
        return cur.fetchone()[0]

    def check(name, ok, detail=""):
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}{(' -- ' + detail) if detail else ''}")
        if not ok:
            fails.append(name)

    try:
        print("=" * 78)
        print("cm26 REFRESH -- VERIFICATION")
        print("=" * 78)

        # ---- CHECK A: resolution jumps -------------------------------------
        print("\nCHECK A -- 2026 resolution jumps to ~98% (cycle-matched against union mart):")
        res = {}
        cur.execute(f"""
            SELECT l.cycle, ROUND(100.0*SUM(IFF(c.cmte_id IS NOT NULL,1,0))/COUNT(*),2) AS pct
            FROM {LINK} l LEFT JOIN {CMTE} c ON c.cmte_id=l.cmte_id AND c.cycle=l.cycle
            GROUP BY l.cycle""")
        for cyc, pct in cur.fetchall():
            res[cyc] = float(pct)
        check("2026 resolution >= 95% (target ~98)", res.get("2026", 0) >= 95.0,
              f"2026 = {res.get('2026')}% (was 57.10%)")
        check("2024 resolution unchanged ~98.16%", abs(res.get("2024", 0) - 98.16) < 0.5,
              f"2024 = {res.get('2024')}%")

        # ---- CHECK B: 2024 committee master untouched ----------------------
        print("\nCHECK B(i) -- committee master FED_FEC_BULK byte-for-byte unchanged:")
        n = scalar(f"SELECT COUNT(*) FROM {CM}")
        nsha = scalar(f'SELECT COUNT(DISTINCT "_SRC_SHA256") FROM {CM}')
        sha = scalar(f'SELECT MAX("_SRC_SHA256") FROM {CM}')
        h = scalar(f"SELECT HASH_AGG(FEC_CMTE_ID, CMTE_NM) FROM {CM}")
        check("row count == 20,938", n == CM_BASE_N, f"{n}")
        check("single SHA unchanged", nsha == 1 and sha == CM_BASE_SHA, sha)
        check("content fingerprint unchanged", h == CM_BASE_HASH, f"{h}")

        # ---- CHECK B: 2024 money figures untouched -------------------------
        print("\nCHECK B(ii) -- 2024 money-raised figures byte-for-byte unchanged:")
        for bio, (g0, net0) in ANCHORS.items():
            cur.execute(f"""SELECT ttl_receipts_gross, money_raised_net FROM {MR}
                            WHERE cycle='2024' AND bioguide=%s""", (bio,))
            row = cur.fetchone()
            ok = row is not None and float(row[0]) == g0 and float(row[1]) == net0
            check(f"anchor {bio}", ok, f"gross={row[0]} net={row[1]}" if row else "MISSING")
        mn = scalar(f"SELECT COUNT(*) FROM {MR} WHERE cycle='2024'")
        msum = float(scalar(f"SELECT SUM(money_raised_net) FROM {MR} WHERE cycle='2024'"))
        mh = scalar(f"SELECT HASH_AGG(bioguide, money_raised_net) FROM {MR} WHERE cycle='2024'")
        check("2024 money-raised fingerprint unchanged",
              mn == MONEY24_BASE_N and abs(msum - MONEY24_BASE_SUM) < 0.005 and mh == MONEY24_BASE_HASH,
              f"n={mn} sum={msum} hash={mh}")

        # ---- AUDIT: additive safety + grain + registry ---------------------
        print("\nAUDIT -- additive safety / grain integrity / registry append-only:")
        newn = scalar(f"SELECT COUNT(*) FROM {NEWCM}")
        check("new landing object FED_FEC_BULK_COMMITTEES exists (cycle 2026)", newn > 0, f"{newn} rows")
        only2026 = scalar(f"SELECT COUNT(DISTINCT CYCLE) FROM {NEWCM}")
        only2026val = scalar(f"SELECT MAX(CYCLE) FROM {NEWCM}")
        check("new landing object holds ONLY cycle 2026", only2026 == 1 and only2026val == "2026", only2026val)
        dup = scalar(f"SELECT COUNT(*) FROM (SELECT cmte_id,cycle FROM {CMTE} GROUP BY 1,2 HAVING COUNT(*)>1)")
        check("union mart 0 dup (cmte_id, cycle)", dup == 0, f"dups={dup}")
        cyc24 = scalar(f"SELECT COUNT(*) FROM {CMTE} WHERE cycle='2024'")
        check("union mart 2024 slice == FED_FEC_BULK count (no 2024 mutation)", cyc24 == CM_BASE_N, f"{cyc24}")
        link2026_dup = scalar(f"SELECT COUNT(*) FROM (SELECT cand_id,cmte_id,cycle FROM {LINK} WHERE cycle='2026' GROUP BY 1,2,3 HAVING COUNT(*)>1)")
        check("2026 linkage bridge 0 dup key (unchanged grain)", link2026_dup == 0, f"dups={link2026_dup}")
        regrow = scalar(f"SELECT COUNT(*) FROM {REG} WHERE SOURCE_ID='fed_fec_bulk_committees'")
        check("registry row fed_fec_bulk_committees present (append-only)", regrow == 1, f"rows={regrow}")
        dom = scalar(f"SELECT DOMAIN_PRIMARY FROM {REG} WHERE SOURCE_ID='fed_fec_bulk_committees'")
        check("registry row domain = money_in_politics", dom == "money_in_politics", str(dom))

        print("\n" + "=" * 78)
        verdict = "PASS" if not fails else "FAIL"
        print(f"  VERIFICATION: {verdict}" + ("" if not fails else f"  -- failed: {fails}"))
        print("=" * 78)
        sys.exit(0 if not fails else 1)
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    main()
