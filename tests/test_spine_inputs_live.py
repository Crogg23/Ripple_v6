"""Live guards on WHAT the spine reads — the 2026-08-11 spine-audit defect classes.

Two things went wrong at once and neither was visible offline:

  (1) STALE INPUT. The spine and the flagship debarment lens still pointed at a
      9,000-row capped SAM exclusions sample (2,940 UEIs) after the full
      167,928-row list (38,425 UEIs) landed under a NEW table name. Measured
      cost: 53 debarred firms with federal awards visible instead of 102. The
      dbt lead queue had been repointed; the connection engine had not, and
      nothing compared the two.

  (2) DEAD INPUT. Three spec'd tables nominated key columns the publisher never
      populates (FCC ULS EIN 0/1,689,338; NSF awards EIN 0/125; the retired NCUA
      dictionary table's EIN) — dead keys posing as wired ones.

Both guards hit the warehouse because both defects are properties of the DATA,
not of the code. Verified red on the pre-fix state before being trusted.
"""

import pytest

from connect import db
from connect.entity_index_specs import DISPLAY_SPECS, table_keys
from connect.keys import normalize_sql

# Newer/bigger landing siblings of a spec'd table that are NOT a fuller copy of
# it, with the reason. A sibling missing from here fails the test on purpose:
# somebody must look and say which it is.
ACKNOWLEDGED_SIBLINGS = {
    "FED_CFPB_HMDA_HISTORIC": "different grain (loan records), carries no LEI column",
    "FED_CFPB_HMDA_LAR": "different grain (loan application register), separate dataset",
    "FED_CFPB_HMDA_ARID2017_LEI_XREF": "a crosswalk, not a fuller HMDA copy",
    "FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS": "enrollment roster, not the quality file",
    "FED_CMS_HOSPICE_ENROLLMENTS": "enrollment roster, not the quality file",
    "FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER_AND_SERVI":
        "by-provider-AND-SERVICE grain (no bare NPI column); a different table",
    "FED_CMS_NURSING_HOME_PENALTIES": "penalties, a different dataset",
    "FED_CMS_NURSING_HOME_DEFICIENCIES": "deficiencies, a different dataset",
    "FED_CMS_NURSING_HOME_FIRE_DEFICIENCIES": "fire deficiencies, a different dataset",
    "FED_CMS_OPEN_PAYMENTS_PROFILE_SUPPLEMENT": "profile supplement, not payments",
    "FED_CMS_OPEN_PAYMENTS_2022": "already spec'd in its own right",
    "FED_CMS_OPEN_PAYMENTS_2023": "already spec'd in its own right",
    "FED_FEC_BULK_COMMITTEES": "committee file, separate spec",
    "FED_NCUA_CALL_REPORTS_FOICU": "carries no hard ID (see the spec file)",
    "FED_NCUA_CALL_REPORTS_FS220": "carries no hard ID (see the spec file)",
    "FED_SAM_EXCLUSIONS_FULL": "superseded by _FULL_R2, which IS the spec'd table",
    "FED_SEC_EDGAR_COMPANY_TICKERS_EXCHANGE": "adds an exchange column; same 10k tickers",
    "FED_IRS_990_EFILE_INDEX": "OPEN: 5.5M EINs vs the 200-row spec'd table — a real "
                               "recall gap, reported 2026-08-11, not yet wired",
    "FED_USASPENDING_CONTRACTS_FULL": "OPEN: 20M rows (itself loader-capped at a round "
                                      "20,000,000) with 420,990 UEIs vs 92,833 in the "
                                      "spec'd table — 343 debarred firms with awards "
                                      "instead of 102. Reported 2026-08-11; repointing "
                                      "waits on an uncapped re-pull",
    "INTL_GLEIF_RELATIONSHIPS": "parent/child relationships, not the LEI register",
    "INTL_GLEIF_REPEX": "already spec'd in its own right",
}


@pytest.mark.snowflake
def test_no_spec_table_is_shadowed_by_an_unacknowledged_newer_sibling(sf):
    meta = {r[0]: (r[1], r[2]) for r in db.rows(
        sf, "SELECT table_name, row_count, last_altered FROM "
            "LIBRARY_RAW.INFORMATION_SCHEMA.TABLES WHERE table_schema = 'LANDING'")}
    shadowed = []
    for t in DISPLAY_SPECS:
        rows, altered = meta[t]
        for sib, (srows, saltered) in meta.items():
            if sib.startswith(t + "_") and saltered > altered and (srows or 0) > (rows or 0):
                if sib not in ACKNOWLEDGED_SIBLINGS:
                    shadowed.append(f"{t} ({rows:,}) is shadowed by {sib} ({srows:,}, newer)")
    assert not shadowed, (
        "the spine is reading a table that a newer, bigger sibling may supersede -- "
        "exactly how the debarment lens spent three weeks on 5% of the exclusion "
        "list:\n  " + "\n  ".join(shadowed) +
        "\n\nRepoint the spec, or add the sibling to ACKNOWLEDGED_SIBLINGS with why "
        "it is NOT a fuller copy.")


@pytest.mark.snowflake
@pytest.mark.parametrize("table,key,key_col",
                         [(t, k, c) for t, s in DISPLAY_SPECS.items() for k, c in table_keys(s)])
def test_every_spine_key_column_carries_real_values(sf, table, key, key_col):
    """COUNT(col) is never enough here (constitution section 7): the FCC ULS EIN
    column is non-null on all 1.7M rows and usable on none. This counts values
    that survive normalization, which is what the spine actually joins on."""
    n = normalize_sql(key, f'"{key_col}"')
    rows, keyed, distinct = db.rows(
        sf, f'SELECT COUNT(*), COUNT({n}), COUNT(DISTINCT {n}) '
            f'FROM LIBRARY_RAW.LANDING."{table}"')[0]
    assert keyed > 0 and distinct > 1, (
        f"{table}.{key_col} is spec'd as a {key} spine key but carries "
        f"{keyed:,} usable values ({distinct:,} distinct) across {rows:,} rows. "
        f"A dead key wired into the spine looks like a connection and is not one.")
