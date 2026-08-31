"""The freshness/trap axis — standing POLICY data traps, mapped to source tables.

Mirrored VERBATIM from the canonical seed in scripts/build_registry_setup.py
(POLICY rows, mirrored 2026-07-21). This file is the build-time snapshot the
grader reads; if the registry seeds change, re-mirror here — the tripwire test
tests/test_honesty.py::test_traps_mirror_registry_seeds diffs the two.

Only SOURCE-DATA traps belong here (they poison numbers computed over a table).
Ops traps (no_selectorless_dbt_build, trap_rlike_whole_string) are real but
attach to workflows, not to data lineage — deliberately excluded.
"""

from __future__ import annotations

# policy key -> verbatim policy statement
TRAPS: dict[str, str] = {
    "trap_open_payments_split": (
        "Open Payments is split across THREE landing tables (base 15.4M / 2022 13.25M / "
        "2023 14.7M). Ad-hoc queries against one bare table under-count; the "
        "banned_but_paid detector already reads a unioned view."
    ),
    "trap_ais_snapshot": (
        "FED_NOAA_AIS is a stale 8-day snapshot: 58,106,517 rows spanning exactly "
        "2024-01-01..2024-01-08. It pre-dates the 2025-26 sanctions wave — any 'sanctioned "
        "vessel in US waters' match off it is reverse-causality unless date-checked. "
        "Never draw it as a time series."
    ),
    "trap_leie_npi_and_dates": (
        "FED_HHS_OIG_LEIE: NPI='0000000000' on 74,780/83,464 rows (89.6%) — a naive NPI join "
        "merges them all into one 'doctor' (the libel trap). EXCLDATE needs explicit date "
        "parsing; TRY_CAST collapses to 1970."
    ),
    "trap_ofac_sdn_type": (
        "FED_OFAC_SDN.SDN_TYPE uses the literal sentinel '-0- ' (trailing space, 9,785 rows) "
        "for entities; also one empty-string row. Filter explicitly."
    ),
    "trap_usaspending_grain": (
        "USASpending contracts are one row per TRANSACTION, not per award; a company "
        "fragments across child/parent UEIs (Lockheed: 77 child / 26 parent). "
        "Top-contractor rankings are floors, not truths."
    ),
    "trap_nppes_ein_masked": (
        "FED_CMS_NPPES.EMPLOYER_IDENTIFICATION_NUMBER_EIN is 100% non-null (9,606,683/9,606,683 "
        "rows) but only 2 distinct values exist: '' (7,669,321 rows) and '<UNAVAIL>' (1,937,362 "
        "rows) — zero real EINs. A bare COUNT(col) reads as fully populated; any join or "
        "entity-resolution on this column merges every provider into one or two buckets."
    ),
    "trap_fcc_uls_ein_masked": (
        "FED_FCC_LICENSING.EIN is 100% non-null (1,689,338/1,689,338 rows) but 100% empty "
        "string — zero real EINs. Same masked-ID shape as the NPPES EIN trap."
    ),
    "trap_ais_imo_masked": (
        "FED_NOAA_AIS.IMO is 100% non-null (58,106,517/58,106,517 rows) but ~55% are sentinel "
        "placeholders: '' (18,070,341 rows, 31.1%) and 'IMO0000000' (13,868,433 rows, 23.9%). "
        "A naive IMO join merges roughly a third of all vessels into one 'ship' via the blank "
        "sentinel alone."
    ),
    # 2026-08-18 join-key trust catalog sweep (census-grid fill-tables sentinel/degenerate-key
    # list, reports/census_grid_2026-08-12/fill/untrustworthy_keys_2026-08-18.csv): every trap
    # below was verified live this session with COUNT(*)/COUNT(col)/COUNT(DISTINCT col) plus a
    # value sample, per CLAUDE.md section 7 -- never a bare null check.
    "trap_foreignassistance_ein_masked": (
        "FED_FOREIGNASSISTANCE.EIN is 100% blank across all 95,658 deduped rows (mart "
        "economics__fed_foreignassistance) — zero real EINs. Same masked-ID shape as the "
        "NPPES/FCC EIN traps: a bare COUNT(col) reads as fully populated."
    ),
    "trap_hud_data_ein_masked": (
        "FED_HUD_DATA.EIN is 100% blank across all 77 rows — zero real EINs, same masked-ID "
        "shape as the NPPES/FCC EIN traps."
    ),
    "trap_ftc_datasets_ein_masked": (
        "FED_FTC_DATASETS.EIN is 100% blank across all 1,200 rows — zero real EINs, same "
        "masked-ID shape as the NPPES/FCC EIN traps."
    ),
    "trap_usgs_topoview_fips_masked": (
        "FED_USGS_TOPOVIEW.FIPS is 100% blank across all 250 rows — zero real FIPS codes "
        "despite the column name."
    ),
    "trap_dot_bts_carrier_code_masked": (
        "FED_DOT_BTS.CARRIER_CODE is 100% blank across all 21 rows — zero real carrier codes "
        "despite the column name."
    ),
    "trap_datagovgh_license_masked": (
        "INTL_GH_DATAGOVGH.LICENSE is 100% blank across all 10 rows — zero real license "
        "values."
    ),
    "trap_faa_data_portal_fips_masked": (
        "FED_FAA_DATA_PORTAL.FIPS is 100% blank across all 4 rows — zero real FIPS codes "
        "despite the column name."
    ),
    "trap_nara_wra_aad_family_number_masked": (
        "FED_NARA_WRA_AAD.FAMILY_NUMBER is blank on the table's only row — the entire column "
        "carries zero real family numbers."
    ),
    "trap_es_borme_issue_number_masked": (
        "INTL_ES_BORME.BORME_ISSUE_NUMBER is 100% blank across all 3 rows — zero real issue "
        "numbers despite the column name."
    ),
    "trap_fra_safety_county_fips_masked": (
        "FED_FRA_SAFETY.COUNTY_FIPS holds the literal text 'N/A' on its only row, not a real "
        "FIPS code — a text sentinel, not a blank."
    ),
    "trap_socta_europol_serial_number_garbage": (
        "INTL_EU_SOCTA_EUROPOL.SERIAL_NUMBER is not blank but garbage: every one of 26 rows "
        "holds the literal 3-char fragment 'ion', not a serial number — looks like an upstream "
        "column-mapping accident, worse than a masked ID."
    ),
    "trap_uscis_data_form_number_garbage": (
        "FED_USCIS_DATA.FORM_NUMBER is 87.5% blank; the surviving ~13% is not form numbers at "
        "all — it is caption/footnote text ('Notes:', full DHS/USCIS office names, "
        "'References:'). The whole column is untrustworthy, not just the blank part."
    ),
    "trap_nppes_license_number_mirage": (
        "FED_CMS_NPPES.PROVIDER_LICENSE_NUMBER_6 is 99.78% blank (9,585,443/9,606,683 rows); "
        "the surviving ~20,570 distinct values look like genuine license numbers, so unlike "
        "EIN this column is real but too sparse to trust as a join key — treating it as one "
        "is a mirage."
    ),
    "trap_nhtsa_vin_masked_and_truncated": (
        "FED_NHTSA_COMPLAINTS.VIN carries more junk than a bare null-count shows: beyond "
        "~334,604 blank rows, thousands more are free-text placeholders ('PLEASE FILL' "
        "x3,395, 'NOT AVAILAB' x1,934, 'PLEASE PROV' x1,756, 'FILL IN' x1,204, 'N/A' x1,052, "
        "'ADD' x983, '9999' x534), and every placeholder truncates at ~11 characters versus a "
        "real VIN's 17 — a masking trap plus a separate truncation defect."
    ),
}

# landing table (upper-case identifier) -> policy keys that poison it
SOURCE_TRAPS: dict[str, tuple[str, ...]] = {
    "FED_NOAA_AIS": ("trap_ais_snapshot", "trap_ais_imo_masked"),
    "FED_HHS_OIG_LEIE": ("trap_leie_npi_and_dates",),
    "FED_OFAC_SDN": ("trap_ofac_sdn_type",),
    "FED_USASPENDING_CONTRACTS": ("trap_usaspending_grain",),
    "FED_CMS_OPEN_PAYMENTS": ("trap_open_payments_split",),
    "FED_CMS_OPEN_PAYMENTS_2022": ("trap_open_payments_split",),
    "FED_CMS_OPEN_PAYMENTS_2023": ("trap_open_payments_split",),
    "FED_CMS_NPPES": ("trap_nppes_ein_masked", "trap_nppes_license_number_mirage"),
    "FED_FCC_LICENSING": ("trap_fcc_uls_ein_masked",),
    # 2026-08-18 join-key trust catalog sweep -- see TRAPS above for evidence.
    "FED_FOREIGNASSISTANCE": ("trap_foreignassistance_ein_masked",),
    "FED_HUD_DATA": ("trap_hud_data_ein_masked",),
    "FED_FTC_DATASETS": ("trap_ftc_datasets_ein_masked",),
    "FED_USGS_TOPOVIEW": ("trap_usgs_topoview_fips_masked",),
    "FED_DOT_BTS": ("trap_dot_bts_carrier_code_masked",),
    "INTL_GH_DATAGOVGH": ("trap_datagovgh_license_masked",),
    "FED_FAA_DATA_PORTAL": ("trap_faa_data_portal_fips_masked",),
    "FED_NARA_WRA_AAD": ("trap_nara_wra_aad_family_number_masked",),
    "INTL_ES_BORME": ("trap_es_borme_issue_number_masked",),
    "FED_FRA_SAFETY": ("trap_fra_safety_county_fips_masked",),
    "INTL_EU_SOCTA_EUROPOL": ("trap_socta_europol_serial_number_garbage",),
    "FED_USCIS_DATA": ("trap_uscis_data_form_number_garbage",),
    "FED_NHTSA_COMPLAINTS": ("trap_nhtsa_vin_masked_and_truncated",),
}


def traps_for_source(table_identifier: str) -> tuple[str, ...]:
    """Policy keys that poison this source table ('' -> none)."""
    return SOURCE_TRAPS.get((table_identifier or "").strip().upper(), ())
