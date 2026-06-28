#!/usr/bin/env python3
"""Domain-tag the 40 issue-coverage sources landed this session (all currently
DOMAIN_PRIMARY=NULL -> show as UNCLASSIFIED in CATALOG, so invisible to the
faceted browse). Preview-by-default; --apply is gated and snapshots a rollback
SQL first. Maps each source to a governed FACET_VOCAB domain.

    python scripts/propose_issue_domain_tags.py            # preview (read-only)
    python scripts/propose_issue_domain_tags.py --apply     # write (Chris)
"""
from __future__ import annotations
import argparse, sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
_LIB = _REPO / "library-onboarding"
if str(_LIB) not in sys.path:
    sys.path.insert(0, str(_LIB))
try:
    from dotenv import load_dotenv
    load_dotenv(_LIB / ".env", override=True)
except Exception:
    pass
import snow  # noqa: E402

# source_id -> DOMAIN_PRIMARY (from the 22-value FACET_VOCAB DOMAIN axis)
DOMAINS = {
    "fed_cisa_kev": "crime_security",
    "intl_ucdp_ged": "crime_security",
    "xc_owid_nuclear_warheads": "crime_security",
    "intl_owid_milspend": "government_power",
    "xc_owid_ai_incidents_annual": "science_research",
    "xc_ransomwarelive_victims": "crime_security",
    "fed_fhfa_hpi": "housing_social",
    "xc_wapo_fatal_force": "crime_security",
    "xc_guttmacher_monthly_abortion": "health_medicine",
    "intl_nti_cns_dprk_missile_tests": "crime_security",
    "xc_nagix_dprk_missile_tests": "crime_security",
    "intl_fao_faostat_food_security": "economy_labor_trade",
    "intl_freedomhouse": "government_power",
    "fed_fbi_nics_checks": "crime_security",
    "xc_owid_co2": "energy_environment",
    "xc_owid_temp_anomaly": "energy_environment",
    "xc_owid_gini": "economy_labor_trade",
    "xc_owid_refugees": "immigration_migration",
    "xc_owid_fertility": "geo_demographics",
    "xc_owid_cpi": "government_power",
    "xc_owid_terrorism_deaths": "crime_security",
    "xc_owid_fossil_share": "energy_environment",
    "xc_owid_life_expectancy": "health_medicine",
    "xc_owid_homicide": "crime_security",
    "xc_vera_incarceration_trends": "justice_courts",
    "intl_leiden_russian_ops_europe": "crime_security",
    "intl_voeten_unga_votes": "government_power",
    "st_cannabis_policy_bundles": "government_power",
    "intl_wb_ids": "money_finance",
    "fed_cms_nadac": "health_medicine",
    "intl_ipc_food_insecurity_global": "economy_labor_trade",
    "fed_noaa_storm_events": "energy_environment",
    "fed_cdc_overdose": "health_medicine",
    "fed_cdc_drug_poisoning_county": "health_medicine",
    "fed_va_suicide_appendix": "health_medicine",
    "fed_va_allcause_mortality": "health_medicine",
    "fed_cdc_suicide_rates": "health_medicine",
    "fed_cdc_anxiety_depression": "health_medicine",
    "fed_cdc_injury_violence_county": "health_medicine",
    "fed_cdc_health_insurance": "health_medicine",
}
REG = "LIBRARY_META.REGISTRY.SOURCE_REGISTRY"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args(argv)
    conn = snow.connect(); cur = conn.cursor()
    try:
        il = "','".join(DOMAINS)
        cur.execute(f"SELECT source_id, domain_primary FROM {REG} WHERE source_id IN ('{il}')")
        cur_map = {r[0]: r[1] for r in cur.fetchall()}
        # validate against governed vocab
        cur.execute("SELECT value FROM LIBRARY_META.REGISTRY.FACET_VOCAB WHERE facet='DOMAIN'")
        vocab = {r[0] for r in cur.fetchall()}
        bad = {d for d in DOMAINS.values() if d not in vocab}
        if bad:
            print("ABORT — non-vocab domains:", bad); return 1

        print(f"{'source_id':34} {'current':14} -> proposed")
        changes = 0
        for sid, dom in DOMAINS.items():
            cur_d = cur_map.get(sid, "(absent!)")
            mark = "" if cur_d == dom else "  *"
            if cur_d != dom and sid in cur_map:
                changes += 1
            print(f"  {sid:32} {str(cur_d):14} -> {dom}{mark}")
        missing = [s for s in DOMAINS if s not in cur_map]
        print(f"\n{changes} sources to retag; {len(cur_map)}/{len(DOMAINS)} present"
              + (f"; MISSING from registry: {missing}" if missing else ""))

        if not args.apply:
            print("\nPREVIEW only — re-run with --apply to write.")
            return 0

        # snapshot rollback
        rb = _REPO / "outputs" / "_rollback_issue_domain_tags.sql"
        with open(rb, "w") as f:
            for sid, cur_d in cur_map.items():
                val = "NULL" if cur_d is None else f"'{cur_d}'"
                f.write(f"UPDATE {REG} SET DOMAIN_PRIMARY={val} WHERE SOURCE_ID='{sid}';\n")
        print(f"rollback snapshot -> {rb}")
        for sid, dom in DOMAINS.items():
            if sid not in cur_map:
                continue
            cur.execute(
                f"UPDATE {REG} SET DOMAIN_PRIMARY=%s, DOMAIN_SOURCE='human', "
                f"DOMAIN_CONFIDENCE='high', NEEDS_TOPIC=FALSE WHERE SOURCE_ID=%s", (dom, sid))
        print(f"APPLIED: retagged {len(cur_map)} sources.")
    finally:
        cur.close(); conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
