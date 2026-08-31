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

    # --- Utah open-data portal, checked 2026-08-31 by sampling the joined
    # names out of the entity index. Three CCN pairs and one NPDES pair, all
    # four the same shape: the CCN or NPDES_ID is right and the join is real,
    # the two publishers just name different things about it.

    # CCN: the federal enrollment file names the LEGAL OWNER, the Utah cost
    # report names the FACILITY. One owner runs many facilities, so the strings
    # cannot match: IHC HEALTH SERVICES INC appears against LDS HOSPITAL,
    # INTERMOUNTAIN MEDICAL CENTER and UTAH VALLEY REGIONAL MED CTR, which are
    # three separate hospitals under one company. Same pattern already
    # acknowledged above for the CMS nursing-home pairs.
    ("FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS", "PORTAL_SOC_UTAH_OPEN_DATA_P_A5AE4FD7A4"):
        "owning legal entity vs facility name, Utah 2019 nursing cost report",
    ("FED_CMS_HOSPITAL_ENROLLMENTS", "PORTAL_SOC_UTAH_OPEN_DATA_P_A9B7E273C8"):
        "owning legal entity vs facility name, Utah 2019 hospital cost report",
    ("FED_CMS_HOSPITAL_ENROLLMENTS", "PORTAL_SOC_UTAH_OPEN_DATA_P_DCD75231F6"):
        "owning legal entity vs facility name, Utah 2015 hospital cost report",

    # NPDES_ID: the EPA facility file names the SITE, Utah's assessed-waters
    # file names the PERMITTEE. These are mostly construction stormwater
    # permits, so the site is a subdivision or a lot and the permittee is the
    # builder: LEDGES OF ST GEORGE PHASE 7 against JENNINGS MANAGEMENT INC.
    # Where the permittee is a company the token overlap already agrees, e.g.
    # UNION PACIFIC RAILROAD CLEARFIELD YARD against UNION PACIFIC RAILROAD.
    # WATCH THIS ONE: some permittees are private individuals, so BOWEN
    # RESIDENCE joins ROBERT BOWEN. The permit is one thing but the entity
    # carries both a place name and a person's name. Anything downstream that
    # treats an NPDES entity as a facility will occasionally get a human.
    ("FED_EPA_NPDES_ICIS_FACILITIES", "PORTAL_SOC_UTAH_OPEN_DATA_P_589CC47A29"):
        "permitted site name vs permit holder, Utah assessed waters",
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
