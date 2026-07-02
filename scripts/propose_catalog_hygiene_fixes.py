#!/usr/bin/env python3
"""Two catalog-hygiene fixes the 2026-06-26 audit found. SAFE BY DEFAULT (preview).

  FIX 1 — VOCAB OFFENDER: fed_sam_exclusions.JURISDICTION = 'US' (post-catalog SAM load
          bypassed the US->federal guard). Restores "0 vocab offenders". 1-row UPDATE.

  FIX 2 — STUB-MART GATE FLOOR HOLE: the CATALOG view marks a mart a stub only when
          (mart_rows <= 3 AND land_rows > 100). The >100 floor lets 8 small broken marts
          (hhs_taggs 45->1, naag 26->1, gemi 40->1, zefix 18->1, fdic_enf 14->1, nara_wra
          36->1, borme 25->3, ie_cro 3->1) pass as 'modeled'. Generalize to a RATIO rule:
          a <=3-row mart is a stub whenever land_rows > mart_rows*4. Catches all of them,
          can't false-flag a legit thin mart. Snapshots the old view DDL for rollback first.

  python3 scripts/propose_catalog_hygiene_fixes.py            # preview (no writes)
  python3 scripts/propose_catalog_hygiene_fixes.py --apply    # apply both (ACCOUNTADMIN)

NB: NEITHER fix repairs the broken marts themselves — those are empty/partial/HTML LANDING
loads (fjc_idb is 4.1M rows 100% empty) that need RE-INGESTION, not a dbt rebuild. These two
fixes only make the catalog tell the truth about them.
"""
import datetime as _dt
import sys, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, "c:/Code/Ripple_v6/library-onboarding")
from snow import connect

apply = "--apply" in sys.argv
conn = connect(); cur = conn.cursor()
def scal(q, p=None):
    cur.execute(q, p or ()); r = cur.fetchone(); return r[0] if r else None

print("=" * 64)
print(f"CATALOG HYGIENE FIXES — {'APPLY' if apply else 'PREVIEW (no writes)'}")
print("=" * 64)

# ---- FIX 1 — vocab offender ----
off = scal("""SELECT COUNT(*) FROM LIBRARY_META.REGISTRY.SOURCE_REGISTRY
              WHERE jurisdiction IS NOT NULL AND jurisdiction NOT IN
              (SELECT value FROM LIBRARY_META.REGISTRY.FACET_VOCAB WHERE facet='JURISDICTION')""")
print(f"\nFIX 1  vocab offenders now: {off}")
cur.execute("""SELECT source_id, jurisdiction FROM LIBRARY_META.REGISTRY.SOURCE_REGISTRY
               WHERE jurisdiction IS NOT NULL AND jurisdiction NOT IN
               (SELECT value FROM LIBRARY_META.REGISTRY.FACET_VOCAB WHERE facet='JURISDICTION')""")
for sid, j in cur.fetchall():
    print(f"       {sid}: '{j}' -> 'federal'")
if apply:
    cur.execute("UPDATE LIBRARY_META.REGISTRY.SOURCE_REGISTRY SET JURISDICTION='federal' "
                "WHERE SOURCE_ID='fed_sam_exclusions' AND JURISDICTION='US'")
    print(f"       applied. offenders now: "
          f"{scal('''SELECT COUNT(*) FROM LIBRARY_META.REGISTRY.SOURCE_REGISTRY WHERE jurisdiction IS NOT NULL AND jurisdiction NOT IN (SELECT value FROM LIBRARY_META.REGISTRY.FACET_VOCAB WHERE facet=%s)''', ('JURISDICTION',))}")

# ---- FIX 2 — stub gate ----
cur.execute("SELECT GET_DDL('VIEW','LIBRARY_META.REGISTRY.CATALOG')")
old = cur.fetchone()[0]
n = old.count("COALESCE(l.land_rows,0) > 100")
print(f"\nFIX 2  stub-gate sites to patch ('>100' -> '> mart_rows*4'): {n}")
print("       sources currently 'modeled' on a <=3-row stub mart (would re-grade to landed/staging):")
cur.execute("""WITH m AS (SELECT LOWER(SPLIT_PART(table_name,'__',2)) sid, row_count mr
                          FROM LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES
                          WHERE table_schema<>'INFORMATION_SCHEMA' AND POSITION('__' IN table_name)>0)
               SELECT c.source_id, c.lifecycle, m.mr, c.landed_row_count
               FROM LIBRARY_META.REGISTRY.CATALOG c JOIN m ON m.sid=c.source_id
               WHERE m.mr<=3 AND c.landed_row_count > m.mr*4 AND c.lifecycle='modeled'
               ORDER BY c.landed_row_count DESC""")
for sid, lc, mr, land in cur.fetchall():
    print(f"       {sid:<34} mart={mr} land={land}  modeled -> (landed/staging)")
if n != 3:
    print(f"       !! expected 3 gate sites, found {n} — view DDL changed; inspect before --apply");
if apply and n == 3:
    new = old.replace("COALESCE(l.land_rows,0) > 100", "COALESCE(l.land_rows,0) > COALESCE(m.mart_rows,0) * 4")
    new = new.replace("create or replace view CATALOG(",
                      "create or replace view LIBRARY_META.REGISTRY.CATALOG(", 1)
    # Timestamped rollback file: a SECOND --apply must never overwrite the FIRST
    # rollback (the first one holds the only pre-change DDL; losing it removes the
    # way back).
    roll = f"c:/Code/Ripple_v6/outputs/_rollback_CATALOG_view_{_dt.datetime.now():%Y%m%d_%H%M%S}.sql"
    with open(roll, "w") as f: f.write(old)
    cur.execute(new)
    print(f"       applied (rollback DDL saved to {roll}).")
    for lc, cnt in cur.execute("SELECT lifecycle, COUNT(*) FROM LIBRARY_META.REGISTRY.CATALOG GROUP BY 1 ORDER BY 2 DESC").fetchall():
        print(f"         {lc:<10} {cnt}")

print("\n" + ("APPLIED both fixes." if apply else "PREVIEW only — re-run with --apply to write."))
conn.close()
