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
    "FED_CMS_NPPES": ("trap_nppes_ein_masked",),
    "FED_FCC_LICENSING": ("trap_fcc_uls_ein_masked",),
}


def traps_for_source(table_identifier: str) -> tuple[str, ...]:
    """Policy keys that poison this source table ('' -> none)."""
    return SOURCE_TRAPS.get((table_identifier or "").strip().upper(), ())
