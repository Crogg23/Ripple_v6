"""Grow-the-wiring pass — first new edge batch: the politics cluster + the
politics->campaign-finance bridge.

Landmine 3 (docs/RIPPLES.md): "Politics has zero verified hard links to the
rest." The scout (grow_wiring_scout.py, same day) found the fix sitting in
plain sight: the member tables share BIOGUIDE ids internally at 100%, and the
member->FEC crosswalk carries real FEC candidate ids that hard-match the FEC
candidate master at 66% (misses are mostly pre-FEC-era members).

Usage:
    python3 scripts/ripples/grow_wiring_pass.py            # preview only
    python3 scripts/ripples/grow_wiring_pass.py --apply    # insert edges

Preview measures every proposed edge live (distinct keys, match rate, value
sample) and prints the exact rows it would insert. --apply inserts into
LIBRARY_META."CONNECT".CONNECT_EDGES — that table is ACCOUNTADMIN-owned, so
apply must run under a role that can write it; the read-only reader PAT will
fail loudly, which is the intended guardrail.
"""
import sys
import os

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
sys.path.insert(0, os.path.join(BASE, "scripts"))

# (node_a, table_a, col_a, node_b, table_b, col_b, key_label, tier)
PROPOSED = [
    ("BILLS", 'POLITICS."POLITICS__BILLS"', "SPONSOR_BIOGUIDE",
     "MEMBER_SPINE", 'POLITICS."POLITICS__MEMBER_SPINE"', "BIOGUIDE",
     "BIOGUIDE", "STEEL"),
    ("BILL_COSPONSORS", 'POLITICS."POLITICS__BILL_COSPONSORS"',
     "COSPONSOR_BIOGUIDE",
     "MEMBER_SPINE", 'POLITICS."POLITICS__MEMBER_SPINE"', "BIOGUIDE",
     "BIOGUIDE", "STEEL"),
    ("MEMBER_CROSSWALK", 'POLITICS."POLITICS__MEMBER_CROSSWALK"', "BIOGUIDE",
     "MEMBER_SPINE", 'POLITICS."POLITICS__MEMBER_SPINE"', "BIOGUIDE",
     "BIOGUIDE", "STEEL"),
    ("MEMBER_FEC_ID", 'POLITICS."POLITICS__MEMBER_FEC_ID"', "BIOGUIDE",
     "MEMBER_SPINE", 'POLITICS."POLITICS__MEMBER_SPINE"', "BIOGUIDE",
     "BIOGUIDE", "STEEL"),
    # THE BRIDGE: politics cluster -> FEC cluster (already on the spine)
    ("MEMBER_FEC_ID", 'POLITICS."POLITICS__MEMBER_FEC_ID"', "FEC_ID",
     "FED_FEC_CANDIDATES", 'FINANCE."FINANCE__FED_FEC_CANDIDATES"', "CAND_ID",
     "FEC_CAND_ID", "STEEL"),
    # ---- batch 2 (2026-08-22): scout hits with real hard IDs ----
    ("EPA_PENALTY_GAP", 'ENVIRONMENT."ENVIRONMENT__EPA_PENALTY_GAP"', "FRS_ID",
     "FED_EPA_FRS_FRS_FACILITIES",
     'ENVIRONMENT."ENVIRONMENT__FED_EPA_FRS_FRS_FACILITIES"', "REGISTRY_ID",
     "FRS_ID", "STEEL"),
    ("FEC_CANDIDATE", 'POLITICS."POLITICS__FEC_CANDIDATE"', "CAND_ID",
     "FED_FEC_CANDIDATES", 'FINANCE."FINANCE__FED_FEC_CANDIDATES"', "CAND_ID",
     "FEC_CAND_ID", "STEEL"),
    ("FEC_CAND_CMTE_LINK", 'POLITICS."POLITICS__FEC_CAND_CMTE_LINK"', "CMTE_ID",
     "FED_FEC_BULK_COMMITTEES",
     'FINANCE."FINANCE__FED_FEC_BULK_COMMITTEES"', "FEC_CMTE_ID",
     "FEC_CMTE_ID", "STEEL"),
    # the COURTS bridge -- the CL<->FJC crosswalk table joins the two court
    # systems at 99.9% on docket number (courts were graph dark matter)
    ("FED_COURTLISTENER_FJC_IDB_CL_LINKED",
     'JUSTICE."JUSTICE__FED_COURTLISTENER_FJC_IDB_CL_LINKED"', "DOCKET_NUMBER",
     "FED_FJC_IDB_CIVIL", 'JUSTICE."JUSTICE__FED_FJC_IDB_CIVIL"', "DOCKET",
     "DOCKET", "STEEL"),
]

MIN_RATE = 0.5   # refuse to propose an edge whose live match rate fell below


def measure(cur, ta, ca, tb, cb):
    cur.execute(
        f'select count(distinct a."{ca}"), '
        f'count(distinct case when b."{cb}" is not null then a."{ca}" end) '
        f'from LIBRARY_MARTS.{ta} a '
        f'left join LIBRARY_MARTS.{tb} b on a."{ca}" = b."{cb}"')
    total, matched = cur.fetchone()
    cur.execute(f'select distinct "{ca}" from LIBRARY_MARTS.{ta} '
                f'where "{ca}" is not null limit 3')
    sample = [str(r[0])[:30] for r in cur.fetchall()]
    return total, matched, sample


def main():
    apply = "--apply" in sys.argv
    from _snowflake_conn import connect
    conn = connect()
    cur = conn.cursor()

    cur.execute('select A, B from LIBRARY_META."CONNECT".CONNECT_EDGES')
    existing = {frozenset(r) for r in cur.fetchall()}

    rows = []
    print(f'{"edge":55s} {"key":12s} {"tier":6s} {"matched":>15s} {"rate":>6s}')
    for na, ta, ca, nb, tb, cb, key, tier in PROPOSED:
        if frozenset({na, nb}) in existing:
            print(f'{na+" <-> "+nb:55s} SKIP — edge already on the spine')
            continue
        total, matched, sample = measure(cur, ta, ca, tb, cb)
        rate = matched / total if total else 0.0
        ok = rate >= MIN_RATE and total > 50
        flag = "" if ok else "  REFUSED (below floor)"
        print(f'{na+" <-> "+nb:55s} {key:12s} {tier:6s} '
              f'{matched:>7,}/{total:<7,} {rate:6.1%}{flag}   sample {sample}')
        if ok:
            rows.append((na, nb, key, tier, matched, round(rate, 4)))

    if not rows:
        print("nothing to do")
        conn.close()
        return

    if apply:
        cur.executemany(
            'insert into LIBRARY_META."CONNECT".CONNECT_EDGES '
            '(A, B, KEY, TIER, MATCHED, MATCH_RATE) values '
            '(%s, %s, %s, %s, %s, %s)', rows)
        conn.commit()
        print(f"\nAPPLIED: {len(rows)} edges inserted.")
    else:
        print(f"\nPREVIEW ONLY — {len(rows)} edges ready. "
              f"Re-run with --apply (needs a write-capable role) to insert.")
    conn.close()


if __name__ == "__main__":
    main()
