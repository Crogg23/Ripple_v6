"""Surgical repair for THE_LIBRARY views broken by the 2026-07-29 dbt rebuild.

Scope: THIS list only. This is NOT thelibrary_refresh.py -- that tool reconciles
against the full catalog, reassigns domains, and prunes, which would silently move
or drop views the user has not asked to touch. This script repoints the 34 known
broken views at their new mart locations and leaves everything else exactly as is.

Root causes, all from the 2026-07-29 dbt rebuild:
  - 32 views pointed at LIBRARY_MARTS.DBT_CROGERS.<model>, the schema every mart
    landed in before models were given a domain schema= config. Those tables were
    dropped once verified superseded; the views were never told where the data moved.
  - 2 views point at LIBRARY_RAW.LANDING tables whose columns drifted (a lowercase
    re-ingest, an XML-derived rename) since the view was written. Unrelated to the
    dbt rebuild, but broken all the same -- repointed at the equivalent mart, which
    has stable, already-cleaned column names.

Usage:
    python scripts/fix_thelibrary_broken_views.py            # dry run
    python scripts/fix_thelibrary_broken_views.py --apply
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _snowflake_conn as sc  # noqa: E402

# (library_schema, view_name) -> new fully-qualified source relation
REPOINT = {
    ("CAMPAIGN_FINANCE", "FOREIGN_AGENT_REGISTRATIONS"): "LIBRARY_MARTS.FOREIGN_INFLUENCE.FOREIGN_INFLUENCE__FED_FARA_BULK",
    ("COMPANIES", "IRELAND_COMPANIES"): "LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__INTL_IE_CRO",
    ("COMPANIES", "SPAIN_COMPANY_FILINGS"): "LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__INTL_ES_BORME",
    ("ECONOMY", "FAILED_BANKS"): "LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_FDIC_FAILED_BANKS",
    ("ECONOMY", "ITALY_STATISTICS"): "LIBRARY_MARTS.ECONOMICS.ECONOMICS__INTL_IT_ISTAT",
    ("ECONOMY", "NATIONAL_DEBT_DAILY"): "LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_TREASURY_DEBT_TO_PENNY",
    ("ECONOMY", "SEC_COMPANY_TICKERS"): "LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_SEC_EDGAR_COMPANY_TICKERS",
    ("ECONOMY", "TREASURY_INTEREST_RATES"): "LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_TREASURY_AVG_INTEREST_RATES",
    ("ENERGY_ENVIRONMENT", "ELECTRICITY_BY_COUNTRY"): "LIBRARY_MARTS.ENERGY.ENERGY__INTL_EMBER_ELEC",
    ("GOVERNMENT", "CONSUMER_FINANCE_COMPLAINTS"): "LIBRARY_MARTS.CONSUMER_PROTECTION.CONSUMER_PROTECTION__FED_CFPB_COMPLAINTS",
    ("GOVERNMENT", "FEDERAL_REGISTER_DOCUMENTS"): "LIBRARY_MARTS.REGULATORY.REGULATORY__FED_FEDERAL_REGISTER_DOCUMENTS",
    ("GOVERNMENT", "REVOLVING_DOOR_APPOINTEES"): "LIBRARY_MARTS.GOVERNANCE.GOVERNANCE__FED_REVOLVINGDOOR_PROJECT",
    ("HEALTH", "CLINICAL_TRIALS"): "LIBRARY_MARTS.HEALTH.HEALTH__FED_CLINICALTRIALS",
    ("HEALTH", "DRUG_RECALLS"): "LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_DRUG_ENFORCEMENT",
    ("HEALTH", "HEALTHCARE_PROVIDERS"): "LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES",
    ("HEALTH", "HOSPITAL_COST_REPORTS"): "LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HCRIS",
    ("HEALTH", "NURSING_HOMES"): "LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME",
    ("HEALTH", "PHARMA_MEAL_CAP_GAMING"): "LIBRARY_MARTS.HEALTH.HEALTH__PHARMA_MEAL_CAP_FINGERPRINT",
    ("HISTORY", "INTRA_AMERICAN_SLAVE_VOYAGES"): "LIBRARY_MARTS.HISTORICAL_RECORDS.HISTORICAL_RECORDS__FED_SLAVEVOYAGES_INTRAAMERICAN",
    ("HISTORY", "SLAVE_NARRATIVES_1936_1938"): "LIBRARY_MARTS.HISTORY.HISTORY__FED_WPA_SLAVE_NARRATIVES",
    ("HOUSING", "REDLINING_MAPS"): "LIBRARY_MARTS.HOUSING.HOUSING__FED_MAPPING_INEQUALITY",
    ("INVESTIGATIONS", "FOREIGN_AGENTS"): "LIBRARY_MARTS.FOREIGN_INFLUENCE.FOREIGN_INFLUENCE__FED_FARA_BULK",
    ("JUSTICE", "AG_MULTISTATE_SETTLEMENTS"): "LIBRARY_MARTS.LEGAL_ENFORCEMENT.LEGAL_ENFORCEMENT__FED_NAAG_MULTISTATE_SETTLEMENTS",
    ("JUSTICE", "COUNTY_OVERDOSE_JAIL_BURDEN"): "LIBRARY_MARTS.JUSTICE.JUSTICE__COUNTY_DOUBLE_BURDEN",
    ("JUSTICE", "ECHR_COURT_CASES"): "LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_HUDOC",
    ("JUSTICE", "FRAUD_SETTLEMENTS"): "LIBRARY_MARTS.JUSTICE.JUSTICE__FED_DOJ_FCA_SETTLEMENTS",
    ("JUSTICE", "JAIL_RACIAL_DISPARITY_BY_COUNTY"): "LIBRARY_MARTS.JUSTICE.JUSTICE__RACIAL_JAIL_DISPARITY",
    ("JUSTICE", "SCOTUS_CASES_AND_VOTES"): "LIBRARY_MARTS.JUSTICE.JUSTICE__FED_SCDB",
    ("JUSTICE", "SUPREME_COURT_CASES"): "LIBRARY_MARTS.JUDICIARY.JUDICIARY__FED_OYEZ",
    ("MONEY", "COUNTRY_DEBT_REPAYMENT"): "LIBRARY_MARTS.MONEY_FINANCE.MONEY__DEBT_REPAYMENT_CLIFF",
    ("PROCUREMENT", "ECUADOR_GOV_CONTRACTS"): "LIBRARY_MARTS.PROCUREMENT.PROCUREMENT__INTL_EC_SERCOP",
    ("SCIENCE", "PREPRINTS"): "LIBRARY_MARTS.SCIENCE_RESEARCH.SCIENCE_RESEARCH__XC_BIORXIV_MEDRXIV",
    ("SPENDING", "HHS_GRANT_AWARDS"): "LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_HHS_TAGGS",
    ("TRANSPORT", "SHIP_POSITIONS"): "LIBRARY_MARTS.MARITIME.MARITIME__FED_NOAA_AIS",
    # Column drift unrelated to the dbt rebuild -- landing table columns changed
    # underneath the view since it was written. Repointed at the mart, whose columns
    # are stable and already cleaned, instead of chasing the landing table again.
    ("COMPANIES", "INTL_GLEIF"): "LIBRARY_MARTS.ECONOMICS.ECONOMICS__INTL_GLEIF",
    ("CAMPAIGN_FINANCE", "OUTSIDE_SPENDING"): "LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDEPENDENT_EXPENDITURES",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    conn = sc.connect()
    cur = conn.cursor()

    fixed, skipped = [], []
    for (schema, view), new_rel in REPOINT.items():
        cur.execute(
            f'select get_ddl(\'view\', \'THE_LIBRARY."{schema}"."{view}"\')'
        )
        ddl = cur.fetchone()[0]
        # Keep the COMMENT, drop the explicit column list -- it was written for the
        # old source's columns and a mismatched list is a hard error against a
        # different relation, even with `select *`.
        comment_match = re.search(r"COMMENT\s*=\s*'(?:[^'\\]|\\.)*'", ddl, re.S)
        comment_clause = f" {comment_match.group(0)}" if comment_match else ""
        new_ddl = (
            f'create or replace view THE_LIBRARY."{schema}"."{view}"'
            f"{comment_clause}\nas select * from {new_rel};"
        )

        # confirm the target actually exists before pointing at it
        db, sch, tbl = new_rel.split(".")
        cur.execute(
            f"select count(*) from {db}.information_schema.tables "
            f"where table_schema = %s and table_name = %s",
            (sch, tbl),
        )
        if cur.fetchone()[0] == 0:
            skipped.append((schema, view, new_rel, "target does not exist"))
            continue

        fixed.append((schema, view, new_rel))
        if args.apply:
            cur.execute(new_ddl)

    for s, v, rel in fixed:
        tag = "REPOINTED" if args.apply else "WOULD REPOINT"
        print(f"{tag}  {s}.{v}  -> {rel}")
    for s, v, rel, why in skipped:
        print(f"SKIP        {s}.{v}  -> {rel}  ({why})")

    if args.apply:
        print(f"\nverifying {len(fixed)} repointed views resolve...")
        still_broken = []
        for s, v, _rel in fixed:
            try:
                cur.execute(f'select * from THE_LIBRARY."{s}"."{v}" limit 0')
                cur.fetchall()
            except Exception as exc:
                still_broken.append((s, v, str(exc)[:150]))
        if still_broken:
            print(f"STILL BROKEN after fix: {len(still_broken)}")
            for s, v, msg in still_broken:
                print(f"   {s}.{v}: {msg}")
        else:
            print("all repointed views now resolve cleanly")

    conn.close()
    print(f"\n{len(fixed)} views {'repointed' if args.apply else 'would be repointed'}, "
          f"{len(skipped)} skipped")
    if not args.apply:
        print("DRY RUN -- rerun with --apply to write changes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
