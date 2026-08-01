"""Live check: a source modeled into TWO domain marts must not give TWO answers.

Found 2026-07-31, in two stages. First pass matched marts by their `__<name>`
filename suffix and found 14 sources modeled twice, 7 disagreeing. Widening the
grouping to the ACTUAL landing table each mart reads (resolved through source()/
ref(), the same way scripts/gen_mart_models.py's duplicate guard was fixed) found
7 more disagreeing pairs the filename match missed entirely -- because a filename
suffix is not source identity. `health__fed_dea_arcos` and
`uncategorized__fed_dea_arcos_full` read the exact same landing table but have
different name suffixes ('fed_dea_arcos' vs 'fed_dea_arcos_full'), so filename
matching never saw them as the same source. One of the pairs the wider check
caught (CMS Part D prescribers) was silently discarding real prescription-claims
and cost data via a stale dedupe key -- a materially worse bug than any of the
original 7.

Modeling one source under two domains is a legitimate editorial choice -- a
mine-safety violation genuinely is both a justice story and a labour story. Two
DIFFERENT purposeful models sharing a source (e.g. politics__member_spine vs a raw
VoteView members roster) is also legitimate and NOT what this checks -- those are
different derived shapes by design, not accidental duplicates, and are excluded via
NOT_ACCIDENTAL_DUPLICATES below (each with a citation to the model's own header
explaining its distinct purpose).

Them DISAGREEING when they claim to be the SAME grain is never a choice. That is
the platform contradicting itself, which is worse than the platform not knowing --
the whole premise is that the same public record gives the same answer wherever you
look at it from.

Marked `snowflake`: needs a live connection, self-skips without one.
"""

from __future__ import annotations

import glob
import os
import re

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DBT_MARTS = os.path.join(REPO, "library-onboarding", "ripple_dbt", "models", "marts")
DBT_STAGING = os.path.join(REPO, "library-onboarding", "ripple_dbt", "models", "staging")

_SOURCE_RE = re.compile(r"source\(\s*'[^']+'\s*,\s*'([^']+)'\s*\)")
_REF_RE = re.compile(r"ref\(\s*'([^']+)'\s*\)")


def _resolve_landing_source(sql_path):
    """The actual LANDING table a mart .sql reads, resolved through one ref() hop
    into staging if needed. Mirrors scripts/gen_mart_models.py's resolver -- kept as
    a second, independent implementation on purpose: if the generator's own guard
    ever regresses, a test sharing its exact logic could regress silently with it."""
    try:
        text = open(sql_path, encoding="utf-8", errors="ignore").read()
    except OSError:
        return None
    m = _SOURCE_RE.search(text)
    if m:
        return m.group(1).upper()
    m = _REF_RE.search(text)
    if m:
        hits = glob.glob(os.path.join(DBT_STAGING, "**", m.group(1) + ".sql"), recursive=True)
        if hits:
            stext = open(hits[0], encoding="utf-8", errors="ignore").read()
            m2 = _SOURCE_RE.search(stext)
            if m2:
                return m2.group(1).upper()
    return None


def _marts_by_landing_source():
    """{landing_table: [(schema, mart_name), ...]} for every mart in the project."""
    out = {}
    for path in glob.glob(os.path.join(DBT_MARTS, "*", "*.sql")):
        src = _resolve_landing_source(path)
        if not src:
            continue
        stem = os.path.splitext(os.path.basename(path))[0]
        schema = os.path.basename(os.path.dirname(path)).upper()
        out.setdefault(src, []).append((schema, stem.upper()))
    return out


# Sources genuinely modeled MORE THAN ONCE on purpose -- each a distinct derived
# shape, not an accidental raw-passthrough duplicate. Every entry cites the model
# whose own header explains why it's not a copy of its sibling.
NOT_ACCIDENTAL_DUPLICATES = {
    "FED_CDC_DRUG_POISONING_COUNTY",  # justice__county_double_burden: a specific
        # cross-referenced disparity metric, not a copy of the raw CDC county table.
    "FED_CONGRESS_LEGISLATORS",       # politics__member_crosswalk: an ID-mapping
        # bridge table, distinct purpose from the legislators roster.
    "FED_EPA_FRS_FULL",               # ref__dim_geography: a shared geography
        # dimension table, not a facilities copy (the environment__ mart IS a near-
        # duplicate of the uncategorized__ autogen twin and stays a checked pair).
    "FED_VOTEVIEW_MEMBERS",           # politics__member_spine / __member_voting_record:
        # distinct derived shapes (a spine + a voting-record fact table), not copies
        # of the raw VoteView members roster.
    "INTL_WB_IDS",                    # money__debt_repayment_cliff: a specific
        # derived metric, not a copy of the raw World Bank IDS extract.
    "XC_VERA_INCARCERATION_TRENDS",   # justice__racial_jail_disparity: a specific
        # Black/White jail-rate disparity metric computed FROM Vera's data, not a
        # copy of it -- verified via the model's own header.
}

# Divergence that is genuinely INTENDED for a pair we DO treat as accidental
# duplicates -- e.g. one copy is deliberately filtered to a subset. Add here only
# with a real reason.
KNOWN_DIVERGENT: dict[str, str] = {
    "V_LEADS_PUBLISHED": (
        "LEAD_QUEUE (one row per reviewable lead) and COHORT_QUEUE (one row "
        "per peer cohort of osha_cohort_outlier_2024 leads) both read the "
        "safe leads view AT DIFFERENT GRAINS by design -- the Reading Room's "
        "two desks (2026-08-01). They can never agree on row count; their "
        "own reconciliation lock is tests/assert_cohort_queue_reconciles.sql "
        "(SUM(n_outliers) == reviewable OSHA leads)."),
}

# A RATCHET, not an excuse list. Every entry here was already broken when the check
# that found it was written. Leaving the test permanently red trains everyone to
# ignore the suite -- the same failure mode as a corruption detector that cries
# wolf. So existing damage is baselined and the test blocks anything NEW, while
# test_the_baseline_never_grows keeps this from becoming a dumping ground.
#
# Every entry is a BUG owed a fix, tracked in CHRIS_DECISIONS.md. Delete entries as
# they're fixed; never add one without fixing something else first.
BASELINE_UNRESOLVED: dict[str, str] = {}
# All 8 confirmed real duplicates fixed 2026-07-31 (7 found by filename matching,
# 1 more -- CMS Part D prescribers -- found only once the check widened to resolve
# actual source tables). See CHRIS_DECISIONS.md for the full root-cause writeup of
# each. Every non-BIA case: the redundant auto-generated raw-passthrough twin is
# disabled in dbt_project.yml, so the duplication itself is gone, not just tolerated.


def _dup_report():
    """[(landing_table, [(schema, mart, row_count), ...]), ...] for every source
    modeled by 2+ marts, EXCLUDING known-intentional multi-model sources."""
    by_source = _marts_by_landing_source()
    return {src: copies for src, copies in by_source.items()
            if len(copies) > 1 and src not in NOT_ACCIDENTAL_DUPLICATES}


def _row_counts(sf, groups):
    from connect import db

    out = {}
    for src, copies in groups.items():
        rows = []
        for schema, mart in copies:
            n = db.scalar(sf, f"""
                SELECT ROW_COUNT FROM LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES
                WHERE TABLE_SCHEMA = '{schema}' AND TABLE_NAME = '{mart}'""")
            rows.append((schema, mart, n))
        out[src] = rows
    return out


@pytest.mark.snowflake
def test_duplicate_domain_marts_agree_on_row_count(sf):
    groups = _dup_report()
    counts = _row_counts(sf, groups)
    tolerated = set(KNOWN_DIVERGENT) | set(BASELINE_UNRESOLVED)

    divergent = []
    for src, rows in counts.items():
        if src in tolerated:
            continue
        distinct = {n for _, _, n in rows if n is not None}
        if len(distinct) > 1:
            divergent.append((src, rows))

    assert not divergent, (
        "a NEW source is modeled into several marts that DISAGREE on row count -- "
        "the platform now gives a different answer depending which one you open:\n" +
        "\n".join(f"    {src}: " + ", ".join(f"{s}.{m}={n:,}" if n is not None else f"{s}.{m}=?"
                                              for s, m, n in rows)
                   for src, rows in divergent) +
        "\n\nFix the models so the copies agree, or -- only if the difference is "
        "genuinely intended -- add the source to KNOWN_DIVERGENT with the reason.")


@pytest.mark.snowflake
def test_the_baseline_never_grows(sf):
    """The ratchet. BASELINE_UNRESOLVED records damage that predates the check that
    found it; it may only ever shrink."""
    groups = _dup_report()
    counts = _row_counts(sf, groups)
    actually_divergent = set()
    for src, rows in counts.items():
        distinct = {n for _, _, n in rows if n is not None}
        if len(distinct) > 1:
            actually_divergent.add(src)

    assert len(BASELINE_UNRESOLVED) == 0, (
        f"BASELINE_UNRESOLVED has {len(BASELINE_UNRESOLVED)} entries but was left "
        f"at 0 on 2026-07-31 -- it's a ratchet, fix a divergence and remove its "
        f"entry, never add one without a fix.")

    fixed = sorted(set(BASELINE_UNRESOLVED) - actually_divergent)
    assert not fixed, (
        f"good news -- these no longer diverge and their baseline entries are now "
        f"stale: {fixed}. Delete them from BASELINE_UNRESOLVED so the ratchet keeps "
        f"its teeth.")


@pytest.mark.snowflake
def test_duplicate_marts_are_at_least_visible(sf):
    """Not a failure -- a census. Duplication (even AGREEING duplication) costs
    storage and is a place the two copies can drift apart later. Printed so the
    count can't grow silently. Excludes NOT_ACCIDENTAL_DUPLICATES -- those are
    intentional distinct models, not redundant copies."""
    groups = _dup_report()
    counts = _row_counts(sf, groups)
    print(f"\n{len(counts)} source(s) modeled into more than one (accidentally "
          f"duplicate) mart:")
    for src, rows in sorted(counts.items()):
        distinct = {n for _, _, n in rows if n is not None}
        flag = "  <-- DISAGREE" if len(distinct) > 1 else ""
        detail = ", ".join(f"{s}.{m}={n:,}" if n is not None else f"{s}.{m}=?" for s, m, n in rows)
        print(f"    {src}: {detail}{flag}")
    assert isinstance(counts, dict)
