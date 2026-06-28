#!/usr/bin/env python3
"""Preview (and optionally apply) DOMAIN_PRIMARY for the 49 UNCLASSIFIED landed/
modeled sources (discovery sweep finding #24: 49% of data-bearing sources sit in
UNCLASSIFIED, so browse-by-domain hides ~half the moat and returns false holes).

Design mirrors scripts/propose_catalog_domaining_fixes.py: preview by default,
rollback-snapshotted, idempotent, --apply gated (the auto-classifier blocks the
agent from writing the catalog, so Chris runs --apply). Rules are HIGH-PRECISION
on source_id -- a row is moved ONLY when the source identity leaves no domain
doubt, and ONLY when it is currently UNCLASSIFIED/blank (existing domains are never
overwritten). Genuinely ambiguous sources (food-security, cannabis policy) are
left for a human topic call (V_REVIEW_QUEUE), not guessed.

    python3 scripts/propose_domain_retag.py            # preview only
    python3 scripts/propose_domain_retag.py --apply    # Chris runs this
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO / "library-onboarding"))
try:
    from dotenv import load_dotenv
    load_dotenv(_REPO / "library-onboarding/.env", override=True)
except Exception:  # pragma: no cover
    pass

import snow  # noqa: E402

CATALOG = "LIBRARY_META.REGISTRY.CATALOG"            # read lifecycle + current domain
REGISTRY = "LIBRARY_META.REGISTRY.SOURCE_REGISTRY"   # write the base table
BACKUP = "LIBRARY_META.REGISTRY._SOURCE_REGISTRY_BAK_DOMAINRETAG_20260628"

# (rule_id, source_id regex, target_domain, why) -- governed vocab, high precision.
RULES = [
    ("health_cdc",   r"^fed_cdc_(overdose|drug|injury|anxiety|suicide|health_insurance)",
     "health_medicine", "CDC mortality/health-indicator panels"),
    ("health_cms",   r"^fed_cms_(open_payments|nadac|part_d|medicare)",
     "health_medicine", "CMS provider/payment/drug-price data"),
    ("health_va",    r"^fed_va_(allcause|suicide)",
     "health_medicine", "VA mortality/suicide appendices"),
    ("health_misc",  r"^xc_guttmacher",
     "health_medicine", "reproductive-health (abortion) panel"),
    ("crime_cyber",  r"^(fed_cisa_kev|xc_ransomwarelive)",
     "crime_security", "cyber exploitation / ransomware"),
    ("crime_arms",   r"(nics|nuclear_warhead|missile|terrorism_deaths|owid_homicide|russian_ops)",
     "crime_security", "firearms / weapons / armed-violence"),
    ("crime_conflict", r"^intl_ucdp_ged",
     "crime_security", "armed-conflict event data"),
    ("crime_force",  r"^xc_wapo_fatal_force",
     "crime_security", "police use-of-force fatalities"),
    ("sanctions",    r"^intl_opensanctions",
     "sanctions_enforcement", "consolidated sanctions targets"),
    ("energy_env",   r"(owid_co2|owid_fossil_share|owid_temp_anomaly|noaa_storm_events|epa_echo)",
     "energy_environment", "emissions / climate / environmental enforcement"),
    ("econ_ineq",    r"^xc_owid_gini",
     "economy_labor_trade", "income-inequality (Gini) panel"),
    ("money_fin",    r"(wb_ids|sec_edgar_financials)",
     "money_finance", "sovereign debt / corporate financial statements"),
    ("money_pol",    r"^fed_fec_bulk",
     "money_in_politics", "FEC campaign-finance committees"),
    ("corp_irs",     r"^fed_irs_revocation",
     "corporate_entities", "IRS tax-exempt (EIN) revocations"),
    ("justice_vera", r"^xc_vera_incarceration",
     "justice_courts", "incarceration / corrections panel"),
    ("gov_power",    r"(freedomhouse|owid_cpi|voeten_unga|owid_milspend)",
     "government_power", "governance / democracy / UN-voting / defense spend"),
    ("sci_ai",       r"^xc_owid_ai_incidents",
     "science_research", "AI incidents / technology"),
    ("geo_demo",     r"(owid_fertility|owid_life_expectancy)",
     "geo_demographics", "demographic panels"),
    ("immig",        r"^xc_owid_refugees",
     "immigration_migration", "refugee-population panel"),
    ("housing",      r"^fed_fhfa_hpi",
     "housing_social", "house-price index"),
]

# Intentionally NOT auto-tagged (ambiguous -> human review):
REVIEW = ["intl_fao_faostat_food_security", "intl_ipc_food_insecurity_global",
          "st_cannabis_policy_bundles"]


def preview(conn):
    cur = conn.cursor()
    cur.execute(
        f"""SELECT source_id, COALESCE(domain_primary,'') FROM {CATALOG}
            WHERE lifecycle IN ('landed','modeled')
              AND COALESCE(domain_primary,'UNCLASSIFIED') IN ('UNCLASSIFIED','')
            ORDER BY source_id""")
    unclassified = cur.fetchall()
    cur.close()
    proposals, claimed = [], set()
    for sid, cur_dom in unclassified:
        for rid, rx, target, why in RULES:
            if re.search(rx, sid):
                proposals.append({"rule": rid, "source_id": sid, "to": target, "why": why})
                claimed.add(sid)
                break
    leftover = [sid for sid, _ in unclassified if sid not in claimed]
    return proposals, leftover


def apply(conn, proposals):
    cur = conn.cursor()
    cur.execute(f"CREATE OR REPLACE TABLE {BACKUP} AS SELECT * FROM {REGISTRY}")
    print(f"  rollback snapshot -> {BACKUP}")
    for p in proposals:
        cur.execute(
            f"""UPDATE {REGISTRY}
                SET domain_primary = %s, domain_source = 'discovery_sweep_2026-06-28',
                    domain_confidence = 'high'
                WHERE source_id = %s
                  AND COALESCE(domain_primary,'UNCLASSIFIED') IN ('UNCLASSIFIED','')""",
            (p["to"], p["source_id"]))
    conn.commit()
    cur.close()
    print(f"  applied {len(proposals)} domain re-tags.")


def main() -> int:
    ap = argparse.ArgumentParser(description="Preview/apply DOMAIN_PRIMARY for UNCLASSIFIED landed sources")
    ap.add_argument("--apply", action="store_true", help="write the re-tags (default previews)")
    args = ap.parse_args()
    conn = snow.connect()
    try:
        proposals, leftover = preview(conn)
        mode = "APPLY" if args.apply else "PREVIEW (reads only)"
        print("=" * 78)
        print(f"DOMAIN RE-TAG of UNCLASSIFIED landed sources (#24)  --  {mode}")
        print("=" * 78)
        by_dom = {}
        for p in proposals:
            by_dom.setdefault(p["to"], []).append(p["source_id"])
        for dom in sorted(by_dom):
            print(f"\n  -> {dom}  ({len(by_dom[dom])})")
            for sid in by_dom[dom]:
                print(f"       {sid}")
        print(f"\n{len(proposals)} sources would be re-tagged into {len(by_dom)} domains.")
        review = [s for s in leftover]
        if review:
            print(f"\n  LEFT FOR HUMAN REVIEW ({len(review)}) -- ambiguous, not guessed:")
            for s in review:
                print(f"       {s}")
        if not args.apply:
            print(f"\nPREVIEW only. Re-run with --apply to write (snapshots first; rollback via {BACKUP}).")
            return 0
        apply(conn, proposals)
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
