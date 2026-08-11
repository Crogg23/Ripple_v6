"""Guards on mart domain routing (scripts/gen_mart_models.py).

Written 2026-08-11 after finding that bare-substring hint matching had mis-filed
real marts: "ice_" matched inside "hospice_"/"service_" (CMS hospice, CMS
fee-for-service, EPA drinking-water service areas all landed under immigration)
and "ed_" matched inside "fed_" (CFTC trader commitments landed under
education). Same failure mode as the 2026-08-10 cast-rule bug -- a rule that was
supposed to match a token was matching a substring.

These tests fail the build if either the token-boundary rule or the
earliest-match-wins tie-break is removed.
"""
import importlib.util
import os

import pytest

_GEN = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "scripts", "gen_mart_models.py")


def _gen():
    spec = importlib.util.spec_from_file_location("_gen_mart_models", _GEN)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


gen = _gen()


# The exact source ids that were mis-filed, plus the neighbours whose correct
# routing depends on the same hints still working.
@pytest.mark.parametrize("source_id,expected", [
    # "ice_" must not match inside another word.
    ("fed_cms_hospice_enrollments", "health"),
    ("fed_cms_medicare_fee_for_service_public_provider_enrollment", "health"),
    ("fed_epa_sdwa_sdwa_service_areas", "environment"),
    # ...but must still match the actual agency prefix.
    ("fed_ice_detainers", "immigration"),
    ("fed_ice_detention_facility_list", "immigration"),
    # "ed_" must not match inside "fed_".
    ("fed_cftc_cot_futures", "finance"),
    ("fed_cftc_cot_financial", "finance"),
    ("fed_bts_ontime", "transport"),
    # ...but must still match a real Education Department id.
    ("fed_ed_ocr", "education"),
    # EPA's enforcement tables carry "fec_" (Federal Enforcement & Compliance),
    # which is NOT the election commission. Earliest token wins.
    ("fed_epa_icis_fec_case_facilities", "environment"),
    ("fed_epa_icis_fec_case_enforcement_conclusion_facilities", "environment"),
    ("fed_epa_icis_fec_epa_informal_enforcement_actions", "environment"),
    ("fed_epa_icis_fec_icis_fec_epa_inspections", "environment"),
    # ...while a genuine FEC source still routes to finance.
    ("fed_fec_bulk_candidates", "finance"),
    # Sources that previously had no hint at all and only landed in a named
    # folder by accident. politics_lobbying, never politics -- that folder's
    # pre-hook guard makes anything generated into it unbuildable.
    ("fed_google_polads_advertiser_stats", "politics_lobbying"),
    ("fed_google_polads_creative_stats", "politics_lobbying"),
    ("fed_senate_lda_filings", "politics_lobbying"),
    ("fed_frb_h15_selected_rates", "finance"),
    ("fed_frb_z1_csv", "finance"),
    ("fed_cpsc_neiss_codes", "consumer_safety"),
    # Unaffected controls.
    ("fed_dea_arcos_full", "health"),
    ("fed_sec_13f_holdings", "finance"),
    ("fed_eoir_case_data", "immigration"),
    ("fed_osha_ita", "labor"),
    ("fed_hud_picture", "housing"),
])
def test_domain_folder_routing(source_id, expected):
    assert gen.domain_folder(source_id, None) == expected


def test_political_ads_and_lobbying_avoid_the_guarded_politics_folder():
    """models/marts/politics/ carries a pre-hook guard that hard-fails dbt
    run/build, because those models mirror hand-reconciled Python-built tables.
    The congressional/election hints (govinfo, voteview, medsl, eac_) point there
    ON PURPOSE -- those sources ARE the mirror set. The advertising and lobbying
    sources are not, so they must land somewhere buildable.
    """
    for hint in ("google_polads", "senate_lda"):
        target = dict(gen.ID_HINTS)[hint]
        assert target == "politics_lobbying", f"{hint} -> {target}"


def test_explicit_catalog_domain_still_wins_over_hints():
    """A real DOMAIN_PRIMARY from the catalog must override the id hints."""
    assert gen.domain_folder("fed_ice_detainers", "energy_environment") == "environment"


def test_hint_match_requires_token_boundary():
    assert gen._hint_match("fed_cms_hospice_enrollments", "ice_") == -1
    assert gen._hint_match("fed_ice_detainers", "ice_") == 4
    assert gen._hint_match("fed_cftc_cot_futures", "ed_") == -1
    assert gen._hint_match("ed_ocr_data", "ed_") == 0


def test_unmatched_source_falls_back_to_uncategorized():
    assert gen.domain_folder("xyz_nothing_matches_here", None) == "uncategorized"
