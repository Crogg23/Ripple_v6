"""TASK A -- the itcont money mart: itemized individual donations per member.

Builds, ADDITIVELY in LIBRARY_MARTS.POLITICS:

  POLITICS__MEMBER_INDIV_DONATIONS   (BIOGUIDE, CYCLE)   the payoff stat

off the 84M-row FED_FEC_INDIV_CONTRIBUTIONS firehose, using the definition PROVEN by
the referee (politics/loaders/smoke_itcont.py), which a naive query got wrong THREE
times. The locked chain + rules:

  itcont.CMTE_ID
    -> POLITICS__FEC_CAND_CMTE_LINK   (WHERE cmte_dsgn IN ('P','A') -- a member's OWN
                                       authorized committees; DISTINCT cmte_id -> bioguide.
                                       This excludes the $232M mis-linked national PAC
                                       C00027466 and sidesteps the ActBlue/WinRed conduit
                                       double-count -- the conduit copies live under the
                                       conduit's CMTE_ID, never an authorized committee.)
    -> POLITICS__MEMBER_FEC_ID        (fec_id -> bioguide)
    -> POLITICS__MEMBER_SPINE         (current members)

  itemized individual = SUM(TRANSACTION_TP IN ('15','15E'))   -- direct + earmarked-received
    WHERE MEMO_CD <> 'X'                                       -- drop double-count memo lines
    NET of reattributions/redesignations (all signs -- the negative 15/15E net out, as in
      the FEC reported total; filtering amt>0 OVERSTATES: Cruz +2.33% un-netted, -0.10% netted)
    cycle assigned by TRANSACTION_DT year (2023-24 -> '2024', 2025-26 -> '2026')

Reconciles to OpenFEC /committee/{id}/totals individual_itemized_contributions within
0.54% (conservative -- at/under FEC) across 4 test committees. itcont carries ONLY
itemized contributions (>$200 aggregate); unitemized small-dollar is not in the file,
so this figure is itemized-only by construction (it ties to OpenFEC's *itemized* line,
NOT total individual).

SCOPE (read before interpreting the number):
  * itemized_indiv = donations from OTHER individuals to the member's authorized
    committees. The candidate's OWN money (type 15C) is carried separately in
    self_contrib_15c, NOT added in -- so a self-funder's itemized_indiv looks (correctly)
    small. unitemized (<$200 aggregate) is not in itcont at all.
  * Money a member's donors give through a Joint Fundraising Committee (dsgn 'J') or a
    Leadership PAC (dsgn 'D') is OUT OF SCOPE by the P/A restriction -- it lands under
    that committee's own CMTE_ID, not the authorized committee. This is correct for the
    committee-level OpenFEC tie; do not re-read the stat as "all money raised for X".
  * cycle is by TRANSACTION_DT (the file lost its source-cycle column). Accurate for
    members up in that cycle and for combined-across-cycles totals; an OFF-cycle member's
    per-cycle split carries ~0.5% date-bucket noise (their early next-race money buckets
    into the prior cycle). reattrib_amount/itemized > ~5% flags a member to verify (a
    refund miscoded as a negative 15 would net like a reattribution -- build() reports them).
  * A committee whose FEC linkage resolves to >1 current member is EXCLUDED as
    unattributable (reported with its $ exposure); a cross-cycle reassignment lands there
    too -- fail-safe (no wrong number), but watch the excluded list.

Safety: CREATE OR REPLACE on this domain's own mart only. Append-only registry.
The referee is run as a PRECONDITION (skip with --skip-referee for pure rebuilds).

  python politics/loaders/build_indiv_donations.py                 # referee + build
  python politics/loaders/build_indiv_donations.py --skip-referee  # rebuild mart only
"""
from __future__ import annotations

import sys

sys.path.insert(0, r"c:\Code\Ripple_v6")
sys.path.insert(0, r"c:\Code\Ripple_v6\library-onboarding")
sys.path.insert(0, r"c:\Code\Ripple_v6\politics\loaders")

from dotenv import load_dotenv  # noqa: E402

load_dotenv(r"c:\Code\Ripple_v6\library-onboarding\.env", override=True)

import snow  # noqa: E402

MART = "LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_INDIV_DONATIONS"

# Shared sub-CTEs: a member's OWN authorized committees, cmte_id -> bioguide.
#   raw   = DISTINCT cmte_id -> bioguide (trap-#1 fanout guard: the link carries a cycle
#           dimension, so joining on cmte_id alone would multiply each contribution).
#   clean = only committees that resolve to EXACTLY ONE current member. A committee with
#           an ambiguous FEC linkage (e.g. C00783480, the "Jason Minnicozzi for Congress"
#           record the ccl wrongly ties to 3 unrelated candidates) is UNATTRIBUTABLE --
#           we never guess which member gets the money. It is excluded and its dollar
#           exposure reported (build() aborts if that exposure is ever material).
CMTE_MEMBER_RAW = """
  cmte_member_raw AS (
    SELECT DISTINCT lk.cmte_id, b.bioguide
    FROM LIBRARY_MARTS.POLITICS.POLITICS__FEC_CAND_CMTE_LINK lk
    JOIN LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_FEC_ID b ON b.fec_id = lk.cand_id
    JOIN LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_SPINE  s ON s.bioguide = b.bioguide
                                                          AND s.legislator_set = 'current'
    WHERE lk.cmte_dsgn IN ('P','A')
  )
"""
CMTE_MEMBER_CLEAN = """
  cmte_member AS (   -- unambiguous only: cmte_id -> exactly one member
    SELECT cmte_id, MAX(bioguide) AS bioguide
    FROM cmte_member_raw
    GROUP BY cmte_id
    HAVING COUNT(*) = 1   -- raw is DISTINCT(cmte_id,bioguide), so COUNT(*)=1 => one member
  )
"""

# itcont projected to (cmte_id, cycle, type, netted amount), referee-proven filters.
#   - 15/15E = itemized individual (the headline). 15C = candidate's OWN money, carried
#     separately (NOT in itemized -- it's not a donation FROM another individual; keeping
#     it out is what ties to OpenFEC's individual_itemized line).
#   - RLIKE '[0-9]{8}' guards the SUBSTR cycle slice against malformed TRANSACTION_DT
#     (spaced/slashed dates that could mis-slice). On the clean MMDDYYYY bulk data this
#     drops nothing the IN-list didn't already drop, so reconciled numbers are unchanged.
ITC_CTE = """
  itc AS (
    SELECT
      i.CMTE_ID                                                   AS cmte_id,
      CASE WHEN SUBSTR(i.TRANSACTION_DT,5,4) IN ('2023','2024') THEN '2024'
           WHEN SUBSTR(i.TRANSACTION_DT,5,4) IN ('2025','2026') THEN '2026' END AS cycle,
      i.TRANSACTION_TP                                            AS tp,
      TRY_TO_DECIMAL(i.TRANSACTION_AMT,18,2)                      AS amt
    FROM LIBRARY_RAW.LANDING.FED_FEC_INDIV_CONTRIBUTIONS i
    WHERE i.TRANSACTION_TP IN ('15','15E','15C')
      AND COALESCE(i.MEMO_CD,'') <> 'X'
      AND i.TRANSACTION_DT RLIKE '[0-9]{8}'
      AND SUBSTR(i.TRANSACTION_DT,5,4) IN ('2023','2024','2025','2026')
  )
"""

MART_DDL = f"""
CREATE OR REPLACE TABLE {MART} AS
WITH
{CMTE_MEMBER_RAW},
{CMTE_MEMBER_CLEAN},
{ITC_CTE},
joined AS (
  SELECT cm.bioguide, itc.cmte_id, itc.cycle, itc.tp, itc.amt
  FROM cmte_member cm
  JOIN itc ON itc.cmte_id = cm.cmte_id
  WHERE itc.cycle IS NOT NULL AND itc.amt IS NOT NULL
)
SELECT
  j.bioguide,
  j.cycle,
  ANY_VALUE(s.full_name)                              AS full_name,
  ANY_VALUE(s.party)                                  AS party,
  ANY_VALUE(s.state)                                  AS state,
  ANY_VALUE(s.last_term_type)                         AS chamber,
  -- THE STAT: itemized individual donations (15+15E, netted), ties to OpenFEC itemized line
  SUM(IFF(j.tp IN ('15','15E'), j.amt, 0))            AS itemized_indiv,
  -- the composition: direct cheques vs small-dollar earmarked (ActBlue/WinRed) online
  SUM(IFF(j.tp = '15',  j.amt, 0))                    AS direct_indiv,
  SUM(IFF(j.tp = '15E', j.amt, 0))                    AS earmarked_indiv,
  ROUND(SUM(IFF(j.tp = '15E', j.amt, 0))
        / NULLIFZERO(SUM(IFF(j.tp IN ('15','15E'), j.amt, 0))), 4) AS earmarked_share,
  -- candidate's OWN money, carried SEPARATELY (excluded from itemized_indiv on purpose --
  -- it's not a donation from another individual; surfaced so the exclusion is visible)
  SUM(IFF(j.tp = '15C', j.amt, 0))                    AS self_contrib_15c,
  -- reattribution/redesignation netting: the negative 15/15E lines we net out. A large
  -- |reattrib_amount|/itemized ratio is the fingerprint of a miscoded refund -> verify
  -- before publishing that member (see build()'s outlier report).
  SUM(IFF(j.tp IN ('15','15E') AND j.amt < 0, j.amt, 0)) AS reattrib_amount,
  -- volume proxies (NOT distinct donors -- individuals can't be de-duped reliably)
  SUM(IFF(j.tp IN ('15','15E') AND j.amt > 0, 1, 0))  AS n_contributions,
  SUM(IFF(j.tp IN ('15','15E') AND j.amt < 0, 1, 0))  AS n_reattributions,
  COUNT(DISTINCT j.cmte_id)                           AS n_authorized_cmtes,
  ARRAY_AGG(DISTINCT j.cmte_id) WITHIN GROUP (ORDER BY j.cmte_id) AS cmte_ids
FROM joined j
JOIN LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_SPINE s ON s.bioguide = j.bioguide
GROUP BY j.bioguide, j.cycle
"""

# Fanout report: committees that resolve to >1 current member are UNATTRIBUTABLE and
# excluded from the mart. Report each one's itcont $ exposure so a future ambiguous
# committee carrying REAL money is flagged loudly, never silently dropped.
AMBIG_SQL = f"""
WITH {CMTE_MEMBER_RAW},
ambig AS (
  SELECT cmte_id, ARRAY_AGG(DISTINCT bioguide) bios
  FROM cmte_member_raw GROUP BY cmte_id HAVING COUNT(*) > 1
),
exposure AS (
  -- GROSS positive (not netted): be conservative about how much money we'd be dropping
  -- when we exclude an ambiguous committee (a netted-to-~0 committee can still carry
  -- real gross dollars whose attribution is genuinely uncertain).
  SELECT i.CMTE_ID cmte_id,
         SUM(IFF(TRY_TO_DECIMAL(i.TRANSACTION_AMT,18,2) > 0, TRY_TO_DECIMAL(i.TRANSACTION_AMT,18,2), 0)) amt
  FROM LIBRARY_RAW.LANDING.FED_FEC_INDIV_CONTRIBUTIONS i
  WHERE i.TRANSACTION_TP IN ('15','15E') AND COALESCE(i.MEMO_CD,'') <> 'X'
    AND i.CMTE_ID IN (SELECT cmte_id FROM ambig)
  GROUP BY 1
)
SELECT a.cmte_id, a.bios, COALESCE(e.amt, 0) AS exposure
FROM ambig a LEFT JOIN exposure e ON e.cmte_id = a.cmte_id
ORDER BY exposure DESC
"""
MATERIAL_EXPOSURE = 50_000.0  # a single excluded committee above this halts for a human call

# Publish-safety assertion: conduits must NEVER surface as a member's recipient.
CONDUIT_SQL = f"""
SELECT COUNT(*) FROM {MART}
WHERE ARRAY_CONTAINS('C00401224'::variant, cmte_ids)
   OR ARRAY_CONTAINS('C00694323'::variant, cmte_ids)
"""


def q1(cur, sql, p=()):
    cur.execute(sql, p)
    return cur.fetchone()


def build():
    conn = snow.connect()
    cur = conn.cursor()
    try:
        # 0. fanout report -- ambiguous committees are excluded; report $ exposure -------
        cur.execute(AMBIG_SQL)
        ambig = cur.fetchall()
        if ambig:
            worst = max(float(r[2] or 0) for r in ambig)
            print(f"  [gate] {len(ambig)} committee(s) resolve to >1 current member -- "
                  f"EXCLUDED as unattributable (worst $ exposure ${worst:,.2f}):")
            for r in ambig:
                bios = str(r[1]).replace("\n", " ").replace("  ", " ")
                print(f"         cmte {r[0]}  exposure ${float(r[2] or 0):>14,.2f}  -> {bios}")
            if worst > MATERIAL_EXPOSURE:
                print(f"\nABORT: an excluded committee carries material money (>${MATERIAL_EXPOSURE:,.0f}). "
                      f"A human must resolve the linkage before this money is dropped.")
                sys.exit(2)
            print(f"  [gate] all excluded exposure < ${MATERIAL_EXPOSURE:,.0f} -- safe to drop, proceeding")
        else:
            print("  [gate] no committee maps to >1 current member (no fanout)")

        # 1. build -----------------------------------------------------------
        cur.execute(MART_DDL)
        conn.commit()
        print(f"  built {MART}")

        # 2. integrity + publish-safety assertions ---------------------------
        rows = q1(cur, f"SELECT COUNT(*) FROM {MART}")[0]
        members = q1(cur, f"SELECT COUNT(DISTINCT bioguide) FROM {MART}")[0]
        dupe = q1(cur, f"SELECT COUNT(*) FROM (SELECT bioguide,cycle FROM {MART} GROUP BY 1,2 HAVING COUNT(*)>1)")[0]
        neg_headline = q1(cur, f"SELECT COUNT(*) FROM {MART} WHERE itemized_indiv <= 0")[0]
        conduit = q1(cur, CONDUIT_SQL)[0]
        sully = q1(cur, f"""SELECT itemized_indiv FROM {MART}
                            WHERE bioguide='S001198' AND cycle='2026'""")  # Dan Sullivan -- the trap victim

        print("\nINTEGRITY:")
        print(f"  rows (member x cycle)            {rows:,}")
        print(f"  distinct members                 {members:,}")
        print(f"  duplicate (bioguide,cycle) keys  {dupe}   (must be 0)")
        print(f"  rows with itemized_indiv <= 0    {neg_headline}")
        print(f"  conduit as a member recipient    {conduit}   (must be 0)")
        if sully:
            print(f"  [trap check] Dan Sullivan 2026 itemized = ${float(sully[0] or 0):,.2f} "
                  f"(NOT the $232M mis-link)")

        assert dupe == 0, "duplicate (bioguide,cycle) -- fanout!"
        assert conduit == 0, "a conduit surfaced as a member recipient -- double-count risk!"

        # 2b. amount-cast health: TEXT TRANSACTION_AMT that fails TRY_TO_DECIMAL is silently
        #     dropped -- if that rate ever spikes (upstream format change: commas/$), money
        #     vanishes with no error. Assert it stays ~0 on the rows we actually consume.
        null_cast = q1(cur, f"""
          SELECT COUNT(*) FROM LIBRARY_RAW.LANDING.FED_FEC_INDIV_CONTRIBUTIONS
          WHERE TRANSACTION_TP IN ('15','15E','15C') AND COALESCE(MEMO_CD,'')<>'X'
            AND TRANSACTION_DT RLIKE '[0-9]{{8}}' AND SUBSTR(TRANSACTION_DT,5,4) IN ('2023','2024','2025','2026')
            AND TRANSACTION_AMT IS NOT NULL AND TRY_TO_DECIMAL(TRANSACTION_AMT,18,2) IS NULL""")[0]
        print(f"  amount-cast failures (must be ~0)  {null_cast:,}")
        assert null_cast < 100, f"{null_cast} TRANSACTION_AMT values failed numeric cast -- money is vanishing!"

        # 2c. reattribution-netting outlier report (red-team risk (c)): a member whose
        #     |reattrib_amount| is a large share of itemized may have a refund miscoded as a
        #     negative 15/15E (not a true reattribution). Flag for a look-before-publish; not
        #     fatal (normal churn is ~1-3%; Cruz 2.3%).
        cur.execute(f"""
          SELECT full_name, cycle,
                 TO_CHAR(itemized_indiv,'999,999,999.00'),
                 TO_CHAR(reattrib_amount,'999,999,999.00'),
                 ROUND(ABS(reattrib_amount)/NULLIFZERO(itemized_indiv),4)
          FROM {MART}
          WHERE itemized_indiv > 0 AND ABS(reattrib_amount)/NULLIFZERO(itemized_indiv) > 0.05
          ORDER BY ABS(reattrib_amount)/NULLIFZERO(itemized_indiv) DESC LIMIT 15""")
        outliers = cur.fetchall()
        print(f"  reattrib-ratio outliers (>5%)      {len(outliers)}   (verify these before publishing)")
        for r in outliers:
            print(f"     {r[0]:<26} {r[1]}  itemized ${r[2].strip()}  reattrib ${r[3].strip()}  ratio={r[4]}")

        # 3. by-cycle headline ----------------------------------------------
        print("\nBY CYCLE:")
        cur.execute(f"""SELECT cycle, COUNT(*) members,
                               TO_CHAR(SUM(itemized_indiv),'999,999,999,999.00') total
                        FROM {MART} GROUP BY 1 ORDER BY 1""")
        for r in cur.fetchall():
            print(f"  {r[0]}  {r[1]:>4} members   total itemized ${r[2].strip()}")

        # 4. the receipt: top 12, cycle 2024 --------------------------------
        print("\nTOP 12 -- itemized individual donations, cycle 2024:")
        cur.execute(f"""SELECT full_name, party, state, chamber,
                               TO_CHAR(itemized_indiv,'999,999,999.00') itemized,
                               TO_CHAR(earmarked_share,'0.00') esh, n_contributions
                        FROM {MART} WHERE cycle='2024'
                        ORDER BY itemized_indiv DESC LIMIT 12""")
        for r in cur.fetchall():
            print(f"  {r[0]:<26} {r[1][:3]}-{r[2]:<2} {r[3]:<4} "
                  f"${r[4].strip():>15}  earmark%={r[5]}  n={r[6]:,}")
    finally:
        cur.close()
        conn.close()


def main(skip_referee: bool):
    if not skip_referee:
        print("PRECONDITION -- run referee (smoke_itcont) ...")
        import smoke_itcont  # noqa: E402
        rc = smoke_itcont.main()
        if rc != 0:
            print("ABORT: referee FAILED -- not building the mart on un-reconciled data.")
            sys.exit(rc)
        print("referee PASS -> building mart.\n")
    print("BUILD MART:")
    build()
    print("\nDONE.")


if __name__ == "__main__":
    main(skip_referee="--skip-referee" in sys.argv)
