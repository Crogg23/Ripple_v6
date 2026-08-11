"""The whole-map connection guard: every source-to-source join, measured.

Before 2026-08-11 exactly two join surfaces had ever been checked by hand. This
measures ALL of them in one query and fails on any NEW badly-disagreeing pair.

Why this catches real damage: two sources share an entity only when they share a
hard registry ID, so if they also both carry a name, those names should describe
the same thing. When they systematically do not, one of three things is true and
all three are bugs worth failing a build over:

  * the ID column on one side does not hold that entity's ID at all (a dialysis
    file carrying the medical director's personal ID fused clinics with doctors),
  * a child table is naming its parent (well "WELL #1" naming a whole water
    system), or
  * the name column describes something else entirely (a donation row's name is
    the DONOR, which named 3,883 political committees after their donors).

Disagreement is not always a bug: publishers legitimately use trade names, legal
names, and operator names for the same facility. Those pairs are listed below,
each with the reason, and each one is a claim a human made and can be re-checked.
"""

from __future__ import annotations

import pytest

from connect import db
from scripts.validate_all_connections import PAIR_SQL

# Minimum named pairs before a low score means anything - a handful of rows can
# disagree by chance.
MIN_PAIRS = 25
FLOOR_PCT = 50.0

# (source A, source B) pairs allowed to disagree, with WHY. Anything not listed
# here that drops below the floor fails the test.
ACKNOWLEDGED = {
    ("FED_CMS_NURSING_HOME", "FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS"):
        "facility trade name vs the legal entity that owns it - same facility ID",
    ("FED_CMS_FACILITY_LEVEL_MINIMUM_DATA_SET_FREQUENCY", "FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS"):
        "facility trade name vs owning legal entity",
    ("FED_CMS_NURSING_HOME_DEFICIENCIES", "FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS"):
        "facility trade name vs owning legal entity",
    ("FED_CMS_NURSING_HOME_FIRE_DEFICIENCIES", "FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS"):
        "facility trade name vs owning legal entity",
    ("FED_CMS_NURSING_HOME_PENALTIES", "FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS"):
        "facility trade name vs owning legal entity",
    ("FED_CMS_POS_OTHER", "FED_CMS_RURAL_HEALTH_CLINIC_ENROLLMENTS"):
        "clinic name vs the hospital/health system that operates it",
    ("FED_CMS_MEDICARE_DIALYSIS_FACILITIES", "FED_CMS_NPPES"):
        "clinic trade name vs the operator's legal business name in NPPES",
    ("FED_CMS_MEDICARE_DIALYSIS_FACILITIES", "FED_CMS_MEDICARE_FEE_FOR_SERVICE_PUBLIC_PROVIDER_ENROLLMENT"):
        "clinic trade name vs operator legal name",
    ("FED_FEC_BULK", "FED_FEC_COMMITTEE_TO_CANDIDATE"):
        "committee name vs the CANDIDATE the committee supports - a real "
        "relationship, deliberately not an identity claim",
    ("FED_FEC_BULK_COMMITTEES", "FED_FEC_COMMITTEE_TO_CANDIDATE"):
        "committee name vs supported candidate",
    ("FED_FEC_COMMITTEE_TO_CANDIDATE", "FED_FEC_INDIV_CONTRIBUTIONS"):
        "supported candidate vs donor - neither is the committee's own name",
}


@pytest.mark.snowflake
def test_no_new_join_disagrees_with_itself(sf):
    rows = db.dicts(sf, PAIR_SQL)
    assert len(rows) > 100, "the measurement returned almost nothing - check the index"

    bad = []
    for r in rows:
        named = r["NAMED_PAIRS"] or 0
        if named < MIN_PAIRS:
            continue
        pct = 100.0 * (r["AGREE"] or 0) / named
        if pct >= FLOOR_PCT:
            continue
        if (r["SRC_A"], r["SRC_B"]) in ACKNOWLEDGED:
            continue
        bad.append(f"{r['KEY_TYPE']} {r['SRC_A']} <-> {r['SRC_B']}: "
                   f"{r['ENTITIES']:,} entities, {pct:.1f}% name agreement "
                   f"({r['AGREE']:,}/{named:,})")

    assert not bad, (
        "these joins connect records whose names do NOT describe the same thing:\n  "
        + "\n  ".join(bad) +
        "\n\nEither the ID column on one side is not that entity's ID, or a name "
        "column describes something else. Fix the spec - or, if the publishers "
        "genuinely use different naming conventions for the same thing, add the "
        "pair to ACKNOWLEDGED with the reason.")


@pytest.mark.snowflake
def test_overall_agreement_stays_high(sf):
    """A single number for the whole map, so a broad regression cannot hide
    inside 847 individually-passing pairs. Measured 99.4% on 2026-08-11."""
    rows = db.dicts(sf, PAIR_SQL)
    named = sum(r["NAMED_PAIRS"] or 0 for r in rows)
    agree = sum(r["AGREE"] or 0 for r in rows)
    pct = 100.0 * agree / named
    assert pct >= 97.0, (
        f"map-wide name agreement fell to {pct:.1f}% ({agree:,}/{named:,}). "
        f"Something changed how entities are matched or named.")
