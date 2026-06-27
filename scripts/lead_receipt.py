#!/usr/bin/env python3
"""Show the RECEIPTS for a banned-but-paid lead — how we know it's real, in plain English.

For each flagged provider it triangulates THREE independent federal sources on the same NPI and
prints what each one says, so a clerical error or a name collision can't hide:

  [1] NPPES        — the national registry: who that NPI actually belongs to
  [2] OIG-LEIE     — the exclusion: why they're banned + when
  [3] Open Payments — the money: how many manufacturer payments, total $, who paid

NPI is a unique national ID that is never reused, so a match on NPI IS the identity; the three-source
NAME agreement is the corroboration (a typo'd NPI would land on a different registry name → flagged
SUSPECT). The timeline (exclusion date vs payment dates) decides whether it's "paid WHILE banned".

    python scripts/lead_receipt.py --top 5            # the 5 most-paid flagged providers
    python scripts/lead_receipt.py --npi 1234567890   # one specific provider
    python scripts/lead_receipt.py --name MIRANDA     # by surname
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_LIB = Path(__file__).resolve().parents[1] / "library-onboarding"
if str(_LIB) not in sys.path:
    sys.path.insert(0, str(_LIB))
try:
    from dotenv import load_dotenv
    load_dotenv(_LIB / ".env", override=True)
except Exception:  # pragma: no cover
    pass
import snow  # noqa: E402

# OIG exclusion authorities -> plain English (the common ones in LEIE).
EXCL = {
    "1128a1": "Conviction of a Medicare/Medicaid program-related crime",
    "1128a2": "Conviction relating to patient abuse or neglect",
    "1128a3": "Felony conviction relating to health-care fraud",
    "1128a4": "Felony conviction relating to controlled substances",
    "1128b1": "Misdemeanor conviction relating to health-care fraud",
    "1128b4": "License revoked, suspended, or surrendered",
    "1128b5": "Exclusion/suspension under a federal/state health program",
    "1128b7": "Fraud, kickbacks, or other prohibited activities",
    "1128b8": "Entities controlled by a sanctioned individual",
}

RECEIPT_SQL = """
WITH leie AS (
  SELECT REGEXP_REPLACE(NPI,'[^0-9]','') npi, UPPER(TRIM(LASTNAME)) lname, UPPER(TRIM(FIRSTNAME)) fname,
         ANY_VALUE(EXCLTYPE) excltype, MIN(EXCLDATE) excldate,
         ANY_VALUE(CITY) city, ANY_VALUE(STATE) state, ANY_VALUE(SPECIALTY) specialty
  FROM LIBRARY_RAW.LANDING.FED_HHS_OIG_LEIE
  WHERE LENGTH(REGEXP_REPLACE(NPI,'[^0-9]',''))=10 AND REGEXP_REPLACE(NPI,'[^0-9]','')<>'0000000000'
  GROUP BY 1,2,3),
op AS (
  SELECT REGEXP_REPLACE(NPI,'[^0-9]','') npi, UPPER(TRIM(COVERED_RECIPIENT_LAST_NAME)) lname,
         COUNT(*) recs,
         ROUND(SUM(TRY_TO_DECIMAL(TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS,18,2)),2) total,
         MIN(TRY_TO_DATE(DATE_OF_PAYMENT,'MM/DD/YYYY')) min_pay,
         MAX(TRY_TO_DATE(DATE_OF_PAYMENT,'MM/DD/YYYY')) max_pay,
         ANY_VALUE(COVERED_RECIPIENT_PROFILE_ID) profile_id,
         ARRAY_SLICE(ARRAY_AGG(DISTINCT APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_NAME),0,5) payers,
         ARRAY_SLICE(ARRAY_AGG(DISTINCT NATURE_OF_PAYMENT_OR_TRANSFER_OF_VALUE),0,5) natures
  FROM LIBRARY_RAW.LANDING.FED_CMS_OPEN_PAYMENTS
  WHERE LENGTH(REGEXP_REPLACE(NPI,'[^0-9]',''))=10
  GROUP BY 1,2),
nppes AS (
  SELECT NPI npi, UPPER(TRIM(PROVIDER_LAST_NAME__LEGAL_NAME)) lname, UPPER(TRIM(PROVIDER_FIRST_NAME)) fname,
         UPPER(TRIM(PROVIDER_CREDENTIAL_TEXT)) cred, ENTITY_TYPE_CODE etype
  FROM LIBRARY_RAW.LANDING.FED_CMS_NPPES)
SELECT l.npi, l.lname l_l, l.fname l_f, l.excltype, l.excldate, l.city, l.state, l.specialty,
       o.recs, o.total, o.min_pay, o.max_pay, o.profile_id, o.payers, o.natures,
       n.lname n_l, n.fname n_f, n.cred, n.etype
FROM leie l JOIN op o ON o.npi=l.npi AND o.lname=l.lname
LEFT JOIN nppes n ON n.npi=l.npi
{where}
ORDER BY o.recs DESC, o.total DESC
LIMIT {limit}
"""


def _d(s):
    s = str(s or "")
    return f"{s[:4]}-{s[4:6]}-{s[6:8]}" if len(s) == 8 and s.isdigit() else (s or "?")


def _arr(v):
    import json
    try:
        return [x for x in json.loads(v) if x] if isinstance(v, str) else [x for x in (v or []) if x]
    except Exception:
        return []


def receipt(r: dict) -> str:
    npi = r["NPI"]
    leie_name = f"{r['L_F']} {r['L_L']}".title()
    nl, nf = (r["N_L"] or "").strip(), (r["N_F"] or "").strip()
    npp_name = f"{nf} {nl}".title().strip() or "(no name on file — NPI blank/deactivated)"
    excl_txt = EXCL.get((r["EXCLTYPE"] or "").lower(), r["EXCLTYPE"] or "?")
    # confidence: NPPES is the third source. blank registry = can't corroborate (2-source only);
    # a NON-blank registry surname that DIFFERS = genuine conflict (verify before use).
    nppes_blank = nl == ""
    surname_3 = (not nppes_blank) and nl == r["L_L"]
    conflict = (not nppes_blank) and nl != r["L_L"]
    excl_date = _d(r["EXCLDATE"])
    paid_after = r["MAX_PAY"] is not None and excl_date != "?" and str(r["MAX_PAY"]) >= excl_date
    payers = ", ".join(_arr(r["PAYERS"])[:4]) or "?"
    natures = ", ".join(_arr(r["NATURES"])[:3]) or "?"

    verdict = ("✅ PAID ON/AFTER EXCLUSION — paid while banned"
               if paid_after else "⚠️ payments predate the exclusion (later-excluded; weaker)")
    if surname_3:
        conf = "✅ FACT-grade: name agrees across all 3 federal sources (NPPES + LEIE + Open Payments)"
    elif conflict:
        conf = "🚩 CONFLICT: NPPES registry shows a DIFFERENT surname — verify before using"
    else:  # nppes_blank
        conf = ("🟡 2-SOURCE: LEIE + Open Payments agree on the name, but the NPPES registry record "
                "is blank/deactivated — can't add the third confirmation; manual check before publishing")
    prof = r["PROFILE_ID"]
    op_url = (f"https://openpaymentsdata.cms.gov/physician/{prof}" if prof else
              "https://openpaymentsdata.cms.gov/search")

    L = []
    L.append(f"━━━ {leie_name}  ·  NPI {npi}  ·  {r['CITY'] or ''} {r['STATE'] or ''} ━━━")
    L.append("HOW WE KNOW — three independent federal sources, same NPI:")
    L.append(f"  [1] NPPES registry  (who owns this NPI): {npp_name}"
             f"{' ' + r['CRED'] if r['CRED'] else ''}"
             f"{'  [individual]' if r['ETYPE']=='1' else '  [ORG/type-2!]' if r['ETYPE'] else ''}")
    L.append(f"  [2] OIG-LEIE        (the ban):           {leie_name} — excluded {excl_date}")
    L.append(f"        reason {r['EXCLTYPE']}: {excl_txt}"
             + (f"  ({r['SPECIALTY']})" if r['SPECIALTY'] else ""))
    L.append(f"  [3] Open Payments   (the money):         {r['RECS']:,} payments, "
             f"${(r['TOTAL'] or 0):,.2f}  ({_d2(r['MIN_PAY'])}→{_d2(r['MAX_PAY'])})")
    L.append(f"        payers: {payers}")
    L.append(f"        for: {natures}")
    L.append(f"  TIMELINE: {verdict}")
    L.append(f"  CONFIDENCE: {conf}")
    L.append(f"  VERIFY YOURSELF:")
    L.append(f"     OIG exclusions: https://oig.hhs.gov/exclusions/exclusions_list.asp  (search '{r['L_L'].title()}')")
    L.append(f"     Open Payments:  {op_url}")
    return "\n".join(L)


def _d2(v):
    return str(v)[:10] if v else "?"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Show receipts for banned-but-paid leads")
    ap.add_argument("--npi", help="one NPI")
    ap.add_argument("--name", help="filter by LEIE surname (uppercased)")
    ap.add_argument("--top", type=int, default=5, help="how many (by payment count)")
    args = ap.parse_args(argv)

    where = ""
    if args.npi:
        where = f"WHERE l.npi = '{args.npi.strip()}'"
    elif args.name:
        where = f"WHERE l.lname = '{args.name.strip().upper()}'"
    sql = RECEIPT_SQL.format(where=where, limit=int(args.top))

    conn = snow.connect()
    try:
        cur = conn.cursor()
        cur.execute(sql)
        cols = [d[0] for d in cur.description]
        rows = [dict(zip(cols, r)) for r in cur.fetchall()]
        if not rows:
            print("No matching banned-but-paid lead found.")
            return 0
        for r in rows:
            print("\n" + receipt(r))
        print(f"\n({len(rows)} shown. NPI is a unique national ID never reused → the match IS the "
              "identity; 3-source name agreement is the corroboration.)")
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    sys.exit(main())
