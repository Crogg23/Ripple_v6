"""C0 -- assign DOMAIN_PRIMARY to the UNCLASSIFIED landed/modeled sources.

Live-driven + self-verifying (per stress-test): reads the ACTUAL UNCLASSIFIED
landed/modeled set, requires a mapping for every one (ABORTS if any is unmapped),
validates every target domain against FACET_VOCAB, then updates SOURCE_REGISTRY.
Gate: after apply, UNCLASSIFIED landed/modeled must be 0.

Usage: python scripts/thelibrary_c0_tag_domains.py [--apply]
"""
from __future__ import annotations
import sys
from pathlib import Path

_LIB = Path(__file__).resolve().parents[1] / "library-onboarding"
sys.path.insert(0, str(_LIB))
from snow import connect  # noqa: E402

APPLY = "--apply" in sys.argv

# Every UNCLASSIFIED landed/modeled source -> its governed FACET_VOCAB domain.
DOMAINS = {
    "fed_cdc_anxiety_depression": "health_medicine",
    "fed_cdc_drug_poisoning_county": "health_medicine",
    "fed_cdc_health_insurance": "health_medicine",
    "fed_cdc_injury_violence_county": "health_medicine",
    "fed_cdc_overdose": "health_medicine",
    "fed_cdc_suicide_rates": "health_medicine",
    "fed_cisa_kev": "crime_security",
    "fed_cms_medicare_provider": "health_medicine",
    "fed_cms_nadac": "health_medicine",
    "fed_cms_open_payments": "health_medicine",
    "fed_cms_open_payments_2023": "health_medicine",
    "fed_cms_part_d_prescribers": "health_medicine",
    "fed_epa_echo": "energy_environment",
    "fed_fbi_nics_checks": "crime_security",
    "fed_fhfa_hpi": "housing_social",
    "fed_irs_bmf": "corporate_entities",
    "fed_irs_revocation": "corporate_entities",
    "fed_naag_multistate_settlements": "justice_courts",
    "fed_noaa_storm_events": "energy_environment",
    "fed_sec_edgar_financials": "money_finance",
    "fed_slavevoyages_intraamerican": "history_culture",
    "fed_usgs_earthquakes": "science_research",
    "fed_va_allcause_mortality": "health_medicine",
    "fed_va_suicide_appendix": "health_medicine",
    "intl_fao_faostat_food_security": "economy_labor_trade",
    "intl_freedomhouse": "government_power",
    "intl_ipc_food_insecurity_global": "economy_labor_trade",
    "intl_leiden_russian_ops_europe": "targeted_investigation",
    "intl_nti_cns_dprk_missile_tests": "crime_security",
    "intl_opensanctions": "sanctions_enforcement",
    "intl_owid_milspend": "government_power",
    "intl_ucdp_ged": "crime_security",
    "intl_voeten_unga_votes": "government_power",
    "intl_wb_ids": "money_finance",
    "st_cannabis_policy_bundles": "government_power",
    "xc_guttmacher_monthly_abortion": "health_medicine",
    "xc_nagix_dprk_missile_tests": "crime_security",
    "xc_owid_ai_incidents_annual": "science_research",
    "xc_owid_co2": "energy_environment",
    "xc_owid_cpi": "government_power",
    "xc_owid_fertility": "geo_demographics",
    "xc_owid_fossil_share": "energy_environment",
    "xc_owid_gini": "economy_labor_trade",
    "xc_owid_homicide": "crime_security",
    "xc_owid_life_expectancy": "health_medicine",
    "xc_owid_nuclear_warheads": "crime_security",
    "xc_owid_refugees": "immigration_migration",
    "xc_owid_temp_anomaly": "energy_environment",
    "xc_owid_terrorism_deaths": "crime_security",
    "xc_ransomwarelive_victims": "crime_security",
    "xc_vera_incarceration_trends": "justice_courts",
    "xc_wapo_fatal_force": "crime_security",
}


def q(cur, sql, params=None):
    cur.execute(sql, params or ())
    cols = [c[0] for c in cur.description]
    return [dict(zip(cols, r)) for r in cur.fetchall()]


def main():
    conn = connect(); cur = conn.cursor()

    valid = {r["VALUE"] for r in q(cur, "SELECT VALUE FROM LIBRARY_META.REGISTRY.FACET_VOCAB WHERE FACET='DOMAIN'")}
    bad = {sid: d for sid, d in DOMAINS.items() if d not in valid}
    if bad:
        print("ABORT -- mapped domains not in FACET_VOCAB:", bad); return

    live = q(cur, """SELECT source_id FROM LIBRARY_META.REGISTRY.CATALOG
                     WHERE domain_primary='UNCLASSIFIED' AND lifecycle IN ('landed','modeled')""")
    live_ids = {r["SOURCE_ID"] for r in live}
    unmapped = sorted(live_ids - set(DOMAINS))
    if unmapped:
        print(f"ABORT -- {len(unmapped)} UNCLASSIFIED landed/modeled sources have no mapping:")
        for s in unmapped:
            print("   ", s)
        print("Add them to DOMAINS and re-run. No changes made.")
        return
    targets = sorted(live_ids)
    print(f"{len(targets)} UNCLASSIFIED landed/modeled sources -> mapped. "
          f"({len(set(DOMAINS)-live_ids)} dict entries already tagged/absent, harmless.)")

    # which classification columns exist on the base table
    cols = {r["COLUMN_NAME"] for r in q(cur, """SELECT COLUMN_NAME FROM LIBRARY_META.INFORMATION_SCHEMA.COLUMNS
             WHERE TABLE_SCHEMA='REGISTRY' AND TABLE_NAME='SOURCE_REGISTRY'""")}
    extra = []
    if "DOMAIN_SOURCE" in cols: extra.append("DOMAIN_SOURCE='human'")
    if "DOMAIN_CONFIDENCE" in cols: extra.append("DOMAIN_CONFIDENCE='high'")
    if "NEEDS_TOPIC" in cols: extra.append("NEEDS_TOPIC=FALSE")
    extra_sql = (", " + ", ".join(extra)) if extra else ""

    from collections import Counter
    dist = Counter(DOMAINS[s] for s in targets)
    print("\nDomain distribution to apply:")
    for d, n in dist.most_common():
        print(f"   {d:24} {n}")

    print(f"\n{'APPLYING' if APPLY else 'PREVIEW'} {len(targets)} updates:")
    for sid in targets:
        dom = DOMAINS[sid]
        if APPLY:
            cur.execute(
                f"UPDATE LIBRARY_META.REGISTRY.SOURCE_REGISTRY SET DOMAIN_PRIMARY=%s{extra_sql} WHERE SOURCE_ID=%s",
                (dom, sid))
    if not APPLY:
        for sid in targets[:8]:
            print(f"   {sid} -> {DOMAINS[sid]}")
        print(f"   ... ({len(targets)} total)")

    if APPLY:
        left = q(cur, """SELECT COUNT(*) n FROM LIBRARY_META.REGISTRY.CATALOG
                         WHERE domain_primary='UNCLASSIFIED' AND lifecycle IN ('landed','modeled')""")[0]["N"]
        print(f"\nGATE: UNCLASSIFIED landed/modeled remaining = {left}  {'PASS' if left == 0 else 'FAIL'}")

    print("\nDONE." + ("" if APPLY else "  (preview -- re-run with --apply)"))
    cur.close(); conn.close()


if __name__ == "__main__":
    main()
