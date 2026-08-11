"""Fixed NIH RePORTER loader -- recursive date-window bisection.

HISTORY OF THE BUG (two fixes deep now):
  1. Original loader did a single unpaginated pull, capped at 5,000 rows total.
  2. First fix looped FISCAL_YEAR x offset/limit pagination -- better, but every
     single fiscal-year query is ITSELF capped by the API at ~15,000 total matches
     (offset-based pagination silently stalls once offset reaches ~14,999-15,000,
     regardless of the query's true total). Landed exactly 15,000 rows for EVERY
     one of 27 fiscal years -- a flat number that was the tell. FY2024's true total
     is 83,516 projects; the old loader landed 15,000 of them and stopped.

THIS FIX: recursive date-window bisection per fiscal year.
  Every query still carries `criteria.fiscal_years=[fy]` (the real narrowing --
  this is what decides which records belong to the year), but ALSO carries a
  `criteria.<date_field>` from/to range that keeps getting halved until each
  leaf's total is safely under the ~15k window cap (WINDOW_CAP=14,000), at which
  point that leaf is paginated normally via offset/limit.

  PRIMARY bisection field: `date_added` (when the record was added to NIH
  RePORTER's system -- NOT when the grant was awarded). Verified live on
  2026-08-05 across 8 sampled fiscal years (2000, 2005, 2010, 2015, 2020, 2024,
  2025, 2026, old and new) that a `date_added` criteria spanning 1980-01-01
  through +400 days from today returns a total EXACTLY equal to the
  `fiscal_years`-alone total for every one of those years -- i.e. date_added is
  populated on 100% of sampled records, unlike `award_notice_date` (confirmed
  ~6% gap on FY2024 alone: 83,516 fiscal_years-alone vs 78,488 with an
  award_notice_date filter over the naive Oct-Sep fiscal-year window -- some
  records have no award_notice_date, or one that falls outside that naive
  window). That 8-year sample is not a proof it holds for all 27 years, so this
  loader does NOT just assume it: every year gets its own live gap check (see
  below), and a fallback field chain fires automatically if date_added leaves
  ANY of that year's records unaccounted for.

  THREE MORE PROBLEMS SURFACED DURING LIVE VERIFICATION, each with a real fix
  (see fetch_year / _bisect_date_field / _bisect_amount docstrings for the code-
  level detail; this is the narrative version):

  (a) DENSITY: FY2000's date_added has a DENSE CLUSTER, ~60,344 of its 72,013
  records sharing the exact same to-the-second timestamp (almost certainly a
  2011 bulk backfill/re-index event). No amount of date_added bisection can
  split that below the window cap -- there's no time resolution left once
  every record in the slice has an IDENTICAL timestamp. A naive "give up and
  fetch anyway" would silently truncate ~46,000 rows -- the exact bug this
  loader exists to fix, just relocated to one leaf instead of a whole year.
  FIX: when a date field's bisection bottoms out and the slice is still over
  cap, switch the splitting axis to the NUMERIC `award_amount_range` criteria
  (a genuine min/max dollar-amount filter, confirmed via the API's own swagger
  schema) for that exact slice. Verified live: [0, 5B] on that cluster returns
  60,344 of 60,344 -- zero gap, and dollar amounts don't cluster the way one
  bulk-import timestamp does.

  (b) A second date field is the WRONG rescue axis: the first attempt at fix
  (a) chained into award_notice_date as the rescue field instead of an amount
  range, and silently lost 20,754 of the 60,344-record cluster, because
  award_notice_date is null on ~35% of it -- nesting a second date field as an
  AND-constraint means its nulls silently drop whatever it doesn't cover, with
  no further chance to recover those records. This is why the rescue axis is
  numeric (award_amount_range), not another date field.

  (c) `budget_start_date` IS NOT A REAL CRITERIA KEY. An earlier version of
  this loader used it as a fallback field because querying it WIDE always
  returned a total suspiciously equal to the true fiscal_years-alone total --
  which looked exactly like "100% coverage" but was actually the API silently
  IGNORING an unrecognized criteria key (verified live: a deliberately made-up
  key name, e.g. "this_is_not_a_real_field_xyz", produces the identical
  behavior -- always returns the unfiltered total, no matter what range is
  sent, and errors on nothing). The tell was a bisection trace showing DIFFERENT
  narrowed windows all reporting the SAME total -- a field that's actually
  filtering can't do that. The real, documented, swagger-verified fields are
  date_added, award_notice_date, project_start_date, project_end_date, and
  award_notice_date (dates), plus award_amount_range (numeric) -- confirmed by
  checking each one returns 0 for an impossible future range (2100-2101),
  which a truly-ignored key cannot do.

  Given (a)-(c), the final design has two independent layers:

  OUTER coverage cascade (fetch_year): try each of DATE_FIELDS in turn as a
  full whole-year pass, INDEPENDENT of each other (not nested/AND'd together),
  merging into one APPL_ID-deduped dict, stopping early once the true total is
  reached. This is what catches a field's null-coverage gap -- a null gap never
  overflows any single leaf's cap, so nothing inside the bisection itself would
  notice; only re-measuring against the true total after a full field pass
  catches it, and running the next field as an independent pass (not nested)
  means its own nulls can't compound with the previous field's.

  INNER density rescue (_bisect_date_field -> _bisect_amount): within one
  field's own pass, a single over-dense leaf gets rescued via award_amount_range
  for just that slice, never chained into another date field.

  Only if amount-range rescue is ALSO exhausted (an extreme edge case never hit
  in live verification) or every DATE_FIELDS pass is exhausted and the year is
  still short of true_total do we fetch/accept what we have as-is -- logged
  loudly as a truncation or residual gap, never silently.

  GLOBAL DEDUPE: even though the per-year Python-side dict is already deduped by
  APPL_ID as records are collected, the very last step before the data replaces
  the live table is a SQL-side `QUALIFY ROW_NUMBER() OVER (PARTITION BY APPL_ID
  ...) = 1` pass over the whole staged load -- a hard guarantee against
  double-landing regardless of what path a record was found through.

  HONESTY: every fiscal year's true `fiscal_years`-alone API total is captured
  live (both at fetch time, to decide whether to run fallback fields, and again
  at report time, to give the final numbers). If ANY year still shows a gap
  after the full fallback chain, or after the final live re-check, it's printed
  plainly -- never silently dropped. See the printed FINAL REPORT block at the
  end of a run for the authoritative per-year numbers.

Landing table: LIBRARY_RAW.LANDING.FED_NIH_REPORTER (overwritten in full, via
an atomic staging-table SWAP so a crash mid-run never leaves the live table
half-written).

CHECKPOINTING: outputs/_nih_reporter_checkpoint.json is a SMALL manifest (run_id,
started timestamp, done fiscal years, per-year stats) -- NOT the raw rows (2.1M
rows of grant abstracts would make that file gigabytes and rewriting it every
year would be its own bottleneck). Each fiscal year's data is written straight to
LIBRARY_RAW.LANDING.FED_NIH_REPORTER__STAGING (overwrite on the very first year of
a fresh run, append every year after) the moment that year finishes fetching, so
a restart resumes at the next undone year with the already-landed years intact in
the staging table.
"""
from __future__ import annotations
import datetime as dt
import hashlib
import json
import os
import sys
import time
import uuid
from pathlib import Path

import pandas as pd
import requests

_REPO = Path(__file__).resolve().parents[1]
_LIB = _REPO / "library-onboarding"
sys.path.insert(0, str(_LIB))
try:
    from dotenv import load_dotenv
    load_dotenv(_LIB / ".env", override=True)
except Exception:
    pass

import snow  # noqa: E402
import ingest  # noqa: E402


def _as_text(v):
    """Stringify for an all-VARCHAR landing table WITHOUT inventing the text 'nan'.

    THE BUG THIS FIXES (2026-08-11). Every loader here did
    `None if v is None else str(v)`. pandas does not keep a JSON null as None --
    it becomes float NaN as soon as the column is built -- so `v is None` was
    False and str(NaN) wrote the four characters n-a-n into the warehouse. The
    column then reads as populated: FDIC's LEI showed 6,260 non-null values, of
    which 4,008 were the string 'nan'. That is exactly the sentinel-masked-blank
    trap that has already fooled this platform on two other join keys, and it is
    worse for a KEY column, because 'nan' joins to 'nan'.

    Also catches pandas' NA/NaT and the whitespace-only strings that some of
    these APIs return in place of a null.
    """
    if v is None:
        return None
    try:
        if pd.isna(v):
            return None
    except (TypeError, ValueError):
        pass  # arrays/lists raise here; they are real values, fall through
    s = str(v)
    return None if s.strip() == "" else s


API = "https://api.reporter.nih.gov/v2/projects/search"
TABLE = "FED_NIH_REPORTER"
STAGING_TABLE = f"{TABLE}__STAGING"
DEDUP_TABLE = f"{TABLE}__DEDUP"
DATABASE = "LIBRARY_RAW"
SCHEMA = "LANDING"
LIMIT = 500  # page size for the actual record fetch (API max)

# The API silently refuses/degrades offset-based pagination once offset reaches
# ~14,999-15,000 within a single query's result set. 14,000 keeps every leaf
# window safely clear of that cliff.
WINDOW_CAP = 14000

# NIH RePORTER covers back to ~1985; 2000-2026 matches the source's ranking scope
# used elsewhere in this repo and is plenty for the platform's purposes.
FISCAL_YEARS = list(range(2000, 2027))
# Smoke-test override: NIH_ONLY_YEARS="2026" (or "2024,2025,2026") to run a small
# subset without editing this file.
_only = os.environ.get("NIH_ONLY_YEARS", "").strip()
if _only:
    FISCAL_YEARS = [int(y.strip()) for y in _only.split(",") if y.strip()]

# OUTER coverage-cascade fields, in priority order. All three were verified LIVE
# against the API's swagger schema (https://api.reporter.nih.gov/swagger/v2/
# swagger.json) as genuine, working date-range criteria keys -- confirmed by
# checking that an impossible future range (2100-2101) returns 0, not the
# unfiltered total. This matters because an EARLIER version of this loader used
# "budget_start_date" as a fallback field and it is NOT a real criteria key at
# all: the API silently ignores unknown keys instead of erroring (verified: a
# deliberately made-up key name produced the exact same total as no filter),
# so "budget_start_date" always returned the FULL unfiltered total no matter
# what range was sent -- which looked exactly like "100% coverage" until a
# same-value-repeated bisection trace gave it away. date_added was empirically
# verified (2026-08-05) to exactly match the fiscal_years-alone total across 8
# sampled years (2000/2005/2010/2015/2020/2024/2025/2026) -- i.e. 100% populated
# -- so it's primary; award_notice_date and project_start_date are real but have
# real null-coverage gaps (e.g. award_notice_date missing on ~35% of one dense
# FY2000 cluster), so they're fallback-only, tried whole-year at a time.
DATE_FIELDS = ["date_added", "award_notice_date", "project_start_date"]

# Wide enough to bound literally any record's date value without assuming the
# naive Oct 1 - Sep 30 fiscal-year window (records legitimately fall outside
# it -- that assumption is exactly what caused the award_notice_date gap). The
# fiscal_years criterion does the real narrowing; this window only needs to be
# wide enough to catch every record's date value in whichever field is active.
WINDOW_FROM = "1980-01-01T00:00:00"
WINDOW_TO = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(days=400)).strftime("%Y-%m-%dT00:00:00")

# Minimum meaningful bisection resolution PER FIELD. date_added carries genuine
# time-of-day precision (verified live: an AM/PM half-day split on a real date_added
# cluster produced a correct non-trivial split, e.g. 0 vs 1,449 -- not a fluke).
# award_notice_date/project_start_date were verified live to carry DATE-ONLY values
# (every sample ends "T00:00:00", no exceptions) -- bisecting them below 1 day is
# worse than pointless: the API compares at day granularity regardless of the
# sub-day bounds sent, so two DIFFERENT sub-day windows on the same day both report
# the FULL day's total, the recursion never sees a shrinking total, and it runs all
# the way to MAX_BISECT_DEPTH along BOTH branches of every split -- a combinatorial
# blowup (2^17-ish probe calls for one stuck day) caught live during verification.
# Capping their resolution at 1 day makes a stuck day fail fast (~14 halvings from
# the wide window to 1 day) and switch to amount-range rescue immediately instead.
FIELD_MIN_RESOLUTION = {
    "date_added": dt.timedelta(seconds=1),
}
DEFAULT_MIN_RESOLUTION = dt.timedelta(days=1)

# Numeric density-rescue axis, used ONLY when a date field's own bisection bottoms
# out (down to its minimum resolution) and the slice is STILL over cap -- e.g.
# FY2000's date_added has ~60,344 of 72,013 records sharing one to-the-second
# timestamp (a 2011 bulk backfill/re-index event), which no amount of date_added
# splitting can shrink below the window cap.
#
# Chaining into ANOTHER date field for the rescue (the first version of this fix)
# turned out to be the wrong move: that field's own nulls silently drop whatever
# it doesn't cover, and since the rescue is a nested AND-constraint, there's no
# later opportunity to recover those records (verified live: award_notice_date
# rescue silently dropped 20,754 of the 60,344-record cluster because award_notice
# _date is null on a third of it). award_amount_range -- a genuine documented
# NUMERIC range filter (min_amount/max_amount), confirmed via the API's own
# swagger schema -- doesn't have that failure mode for a cluster of REAL awarded
# grants: verified live that [0, AMOUNT_HI] exactly matches the FY2000 dense
# cluster's total (60,344 of 60,344, zero gap), and integer dollar amounts bisect
# cleanly with no tie-cluster risk anywhere near the date field's.
AMOUNT_LO = 0
# The API 500s on any max_amount above 2,147,483,647 (2^31-1) -- a 32-bit signed
# integer overflow on the server side, confirmed live (2,147,483,647 -> 200 OK;
# 2,147,483,648 -> 500). 2,000,000,000 stays comfortably under that ceiling while
# still being far above any realistic single NIH award (the largest known awards
# top out in the hundreds of millions).
AMOUNT_HI = 2_000_000_000

CKPT = _REPO / "outputs" / "_nih_reporter_checkpoint.json"

REQUEST_PAUSE_S = 0.05  # light politeness pacing between API calls
MAX_BISECT_DEPTH = 50

_SESSION = requests.Session()


def _post(body: dict) -> dict | None:
    """POST with retry/backoff. Returns parsed JSON, or None after exhausting retries."""
    for attempt in range(6):
        try:
            r = _SESSION.post(API, json=body, timeout=60)
            if r.status_code == 200:
                time.sleep(REQUEST_PAUSE_S)
                return r.json()
            time.sleep(2 * (attempt + 1))
        except Exception:
            time.sleep(2 * (attempt + 1))
    return None


def _total(fy: int) -> int | None:
    """The fiscal_years-alone total -- the ground truth this whole loader chases."""
    d = _post({"criteria": {"fiscal_years": [fy]}, "offset": 0, "limit": 1})
    if d is None:
        return None
    return d.get("meta", {}).get("total", 0)


def _criteria_for(fy: int, fixed: dict) -> dict:
    """`fixed` maps date field names to (from,to) ISO-string tuples, plus an
    optional "__amount__" key mapping to an (min,max) integer tuple for the
    award_amount_range density-rescue axis."""
    c = {"fiscal_years": [fy]}
    for field, bounds in fixed.items():
        if field == "__amount__":
            lo, hi = bounds
            c["award_amount_range"] = {"min_amount": lo, "max_amount": hi}
        else:
            d_from, d_to = bounds
            c[field] = {"from_date": d_from, "to_date": d_to}
    return c


def _total_fixed(fy: int, fixed: dict) -> int | None:
    d = _post({"criteria": _criteria_for(fy, fixed), "offset": 0, "limit": 1})
    if d is None:
        return None
    return d.get("meta", {}).get("total", 0)


def _bisect_amount(fy: int, fixed: dict, lo: int, hi: int, depth: int = 0):
    """Recursively narrow an award_amount_range [lo,hi] (both inclusive; verified
    live the API's amount bounds are inclusive on both ends, so children split at
    mid / mid+1 to avoid double-counting the boundary dollar) until each leaf's
    total is <= WINDOW_CAP. Yields (fixed_snapshot, total)."""
    trial = dict(fixed)
    trial["__amount__"] = (lo, hi)
    t = _total_fixed(fy, trial)
    if t is None:
        print(f"    FY{fy} {trial}: total probe failed after retries -- SKIPPING (will show as a gap)")
        return
    if t == 0:
        return
    if t <= WINDOW_CAP:
        yield (trial, t)
        return
    if depth >= MAX_BISECT_DEPTH or hi <= lo:
        print(f"    FY{fy} {trial}: EXHAUSTED amount-range rescue (lo={lo},hi={hi}), total={t} still > cap {WINDOW_CAP} -- fetching anyway, WILL TRUNCATE at the API's window cap")
        yield (trial, t)
        return
    mid = lo + (hi - lo) // 2
    if mid <= lo:
        print(f"    FY{fy} {trial}: amount range can't be split further (lo={lo},hi={hi}), total={t} -- fetching anyway, WILL TRUNCATE")
        yield (trial, t)
        return
    yield from _bisect_amount(fy, fixed, lo, mid, depth + 1)
    yield from _bisect_amount(fy, fixed, mid + 1, hi, depth + 1)


def _bisect_date_field(fy: int, field: str, d_from: str, d_to: str, depth: int = 0):
    """Recursively halve [d_from, d_to) on ONE date field (half-open -- verified
    live: a shared midpoint boundary between two adjacent windows produces
    neither an overlap nor a gap) until each leaf's total is <= WINDOW_CAP.
    Yields (fixed_snapshot, total).

    If this field's own resolution bottoms out (FIELD_MIN_RESOLUTION) and the
    slice is STILL over cap, switches to award_amount_range as a numeric density-
    rescue axis for that exact slice (see AMOUNT_LO/AMOUNT_HI docs for why a
    numeric axis, not another date field)."""
    trial = {field: (d_from, d_to)}
    t = _total_fixed(fy, trial)
    if t is None:
        print(f"    FY{fy} {trial}: total probe failed after retries -- SKIPPING (will show as a gap)")
        return
    if t == 0:
        return
    if t <= WINDOW_CAP:
        yield (trial, t)
        return

    a = dt.datetime.fromisoformat(d_from)
    b = dt.datetime.fromisoformat(d_to)
    min_res = FIELD_MIN_RESOLUTION.get(field, DEFAULT_MIN_RESOLUTION)
    if depth < MAX_BISECT_DEPTH and (b - a) > min_res:
        mid = a + (b - a) / 2
        if min_res >= dt.timedelta(days=1):
            mid = mid.replace(hour=0, minute=0, second=0, microsecond=0)  # snap to a day boundary -- sub-day bounds are meaningless for this field
        else:
            mid = mid.replace(microsecond=0)
        if mid <= a or mid >= b:
            mid = a + min_res
        mid_s = mid.strftime("%Y-%m-%dT%H:%M:%S")
        yield from _bisect_date_field(fy, field, d_from, mid_s, depth + 1)
        yield from _bisect_date_field(fy, field, mid_s, d_to, depth + 1)
        return

    # This field is out of splitting power for this slice (down to its minimum
    # meaningful resolution and still over cap -- a dense same-timestamp/same-day
    # cluster, e.g. a bulk backfill event). Switch the splitting axis to
    # award_amount_range for this exact fixed window, rather than chaining into
    # another date field (see AMOUNT_LO/AMOUNT_HI docstring for why: a second date
    # field's nulls would silently drop whatever it doesn't cover, with no
    # further chance to recover those records).
    print(f"    FY{fy} {field} [{d_from},{d_to}) stuck at total={t} (no more resolution below {min_res}) -- switching to award_amount_range for density rescue")
    yield from _bisect_amount(fy, {field: (d_from, d_to)}, AMOUNT_LO, AMOUNT_HI)


def _fetch_window(fy: int, fixed: dict, leaf_total: int) -> list[dict]:
    """Paginate one narrow leaf window (leaf_total already known to be <= WINDOW_CAP)."""
    rows = []
    offset = 0
    criteria = _criteria_for(fy, fixed)
    while offset < leaf_total:
        body = {"criteria": criteria, "offset": offset, "limit": LIMIT,
                 "sort_field": "appl_id", "sort_order": "asc"}
        d = _post(body)
        if d is None:
            print(f"      FY{fy} {fixed} offset={offset}: giving up after retries")
            break
        batch = d.get("results", [])
        if not batch:
            break
        rows.extend(batch)
        offset += LIMIT
        if offset >= 14999:
            print(f"      FY{fy} {fixed}: STILL hit the window cap at offset {offset} despite leaf_total={leaf_total} -- bisection math was wrong somewhere, this leaf is truncated")
            break
    return rows


def fetch_year(fy: int) -> tuple[list[dict], dict]:
    """Fetch every record for a fiscal year via TWO layered mechanisms:

      1. OUTER coverage cascade: try each field in DATE_FIELDS, in order, as a
         full whole-year INDEPENDENT primary pass (not AND-nested with each
         other), merging into the same APPL_ID-deduped dict. Stop as soon as
         landed distinct records reach true_total (the common case -- date_added
         alone gets there for most years). This is what catches a field with a
         NULL-coverage gap: a null gap doesn't make any single leaf overflow the
         window cap, so nothing inside the bisection itself would ever notice;
         only re-measuring against true_total after a full field pass catches it,
         and trying the NEXT field as an independent (not nested) whole-year pass
         means its own nulls can't compound with the previous field's.

      2. INNER density rescue (see _bisect_date_field / _bisect_amount): within
         ONE field's own pass, a single over-dense leaf that field's own
         resolution can't shrink below WINDOW_CAP (e.g. FY2000's ~60k-record
         single-timestamp date_added cluster) gets rescued by switching to the
         numeric award_amount_range axis for just that slice -- never chained
         into another date field (see AMOUNT_LO/AMOUNT_HI docstring for why).

    Returns (records, stats).
    """
    true_total = _total(fy)
    if true_total is None:
        raise RuntimeError(f"FY{fy}: could not get the fiscal_years-alone total after retries -- aborting this year")

    by_appl: dict = {}
    total_leaves = 0
    total_rescued_leaves = 0
    fields_used = []
    for field in DATE_FIELDS:
        if len(by_appl) >= true_total:
            break
        before = len(by_appl)
        leaves = list(_bisect_date_field(fy, field, WINDOW_FROM, WINDOW_TO))
        rescued = sum(1 for fixed, _ in leaves if "__amount__" in fixed)
        total_leaves += len(leaves)
        total_rescued_leaves += rescued
        for fixed, leaf_total in leaves:
            recs = _fetch_window(fy, fixed, leaf_total)
            for r in recs:
                appl_id = r.get("appl_id")
                if appl_id is not None and appl_id not in by_appl:
                    by_appl[appl_id] = r
        added = len(by_appl) - before
        fields_used.append(field)
        print(f"    FY{fy} pass via {field}: {len(leaves)} leaves ({rescued} needed amount-range rescue), "
              f"+{added} new -- distinct {len(by_appl)}/{true_total}")

    print(f"    FY{fy}: {total_leaves} total leaves across {len(fields_used)} field pass(es) {fields_used} "
          f"({total_rescued_leaves} needed amount-range rescue) -- distinct {len(by_appl)}/{true_total}")

    gap = true_total - len(by_appl)
    stats = {
        "true_total": true_total,
        "landed_distinct": len(by_appl),
        "gap": gap,
        "leaves": total_leaves,
        "leaves_amount_rescued": total_rescued_leaves,
        "field_passes": fields_used,
    }
    if gap > 0:
        print(f"    FY{fy}: RESIDUAL GAP -- {gap} of {true_total} records not found via any of {DATE_FIELDS} (+ award_amount_range rescue)")
    elif gap < 0:
        print(f"    FY{fy}: landed {len(by_appl)} distinct, {-gap} MORE than the {true_total} probed at fetch start -- "
              "NIH RePORTER data changed during the fetch (new records added live); not a bisection failure")
    return list(by_appl.values()), stats


def flatten(rec: dict) -> dict:
    org = rec.get("organization") or {}
    pi = rec.get("principal_investigators") or []
    po = rec.get("program_officers") or []
    terms = rec.get("terms") or ""
    return {
        "APPL_ID": rec.get("appl_id"),
        "SUBPROJECT_ID": rec.get("subproject_id"),
        "FISCAL_YEAR": rec.get("fiscal_year"),
        "PROJECT_NUM": rec.get("project_num"),
        "CORE_PROJECT_NUM": rec.get("core_project_num"),
        "ORG_NAME": org.get("org_name"),
        "ORG_CITY": org.get("city"),
        "ORG_STATE": org.get("state"),
        "ORG_STATE_NAME": org.get("state_name") if isinstance(org.get("state_name"), str) else None,
        "ORG_COUNTRY": org.get("country"),
        "ORG_DUNS": ",".join(org.get("org_duns") or []) if isinstance(org.get("org_duns"), list) else org.get("org_duns"),
        "ORG_UEI": org.get("org_ueis") if isinstance(org.get("org_ueis"), str) else ",".join(org.get("org_ueis") or []) if isinstance(org.get("org_ueis"), list) else None,
        "ORG_IPF_CODE": org.get("ipf_code"),
        "ORG_ZIP": org.get("zip"),
        "ORG_FIPS": org.get("fips_country_code"),
        "DEPT_TYPE": org.get("dept_type"),
        "ORG_DEPT": org.get("org_dept"),
        "PI_NAMES": "; ".join(f"{p.get('first_name','')} {p.get('last_name','')}".strip() for p in pi) if pi else None,
        "PI_PROFILE_IDS": ",".join(str(p.get("profile_id")) for p in pi if p.get("profile_id")) if pi else None,
        "PO_NAMES": "; ".join(f"{p.get('first_name','')} {p.get('last_name','')}".strip() for p in po) if po else None,
        "PROJECT_TITLE": rec.get("project_title"),
        "ABSTRACT_TEXT": rec.get("abstract_text"),
        "PROJECT_START_DATE": rec.get("project_start_date"),
        "PROJECT_END_DATE": rec.get("project_end_date"),
        "BUDGET_START_DATE": rec.get("budget_start"),
        "BUDGET_END_DATE": rec.get("budget_end"),
        "AWARD_NOTICE_DATE": rec.get("award_notice_date"),
        "DATE_ADDED": rec.get("date_added"),
        "AWARD_AMOUNT": rec.get("award_amount"),
        "DIRECT_COST_AMT": rec.get("direct_cost_amt"),
        "INDIRECT_COST_AMT": rec.get("indirect_cost_amt"),
        "AGENCY_CODE": rec.get("agency_code") or (rec.get("agency_ic_admin") or {}).get("code"),
        "ACTIVITY_CODE": rec.get("activity_code"),
        "AWARD_TYPE": rec.get("award_type"),
        "FUNDING_MECHANISM": rec.get("funding_mechanism"),
        "OPPORTUNITY_NUMBER": rec.get("opportunity_number"),
        "CFDA_CODE": ",".join(str(c) for c in rec.get("cfda_code")) if isinstance(rec.get("cfda_code"), list) else rec.get("cfda_code"),
        "ARRA_FUNDED": rec.get("arra_funded"),
        "COVID_RESPONSE": ",".join(rec.get("covid_response")) if isinstance(rec.get("covid_response"), list) else rec.get("covid_response"),
        "SPENDING_CATEGORIES": json.dumps(rec.get("spending_categories")) if rec.get("spending_categories") else None,
        "STUDY_SECTION": (rec.get("study_section") or {}).get("srg_code") if isinstance(rec.get("study_section"), dict) else None,
        "STUDY_SECTION_NAME": (rec.get("study_section") or {}).get("srg_flex") if isinstance(rec.get("study_section"), dict) else None,
        "SRG_CODE": (rec.get("study_section") or {}).get("srg_code") if isinstance(rec.get("study_section"), dict) else None,
        "CONG_DIST": rec.get("cong_dist"),
        "REPORTER_PROJECT_URL": rec.get("reporter_project_url") or rec.get("project_detail_url"),
        "TERMS": terms if isinstance(terms, str) else json.dumps(terms),
    }


def _fqt(table: str) -> str:
    return f'"{DATABASE}"."{SCHEMA}"."{table}"'


def _save_manifest(run_id: str, started: str, done_years: set, year_stats: dict) -> None:
    CKPT.parent.mkdir(parents=True, exist_ok=True)
    CKPT.write_text(json.dumps({
        "run_id": run_id,
        "started": started,
        "done_years": sorted(done_years),
        "year_stats": year_stats,
    }, indent=None))


def main():
    conn = snow.connect()

    run_id: str
    started_iso: str
    done_years: set = set()
    year_stats: dict = {}
    if CKPT.exists():
        ck = json.loads(CKPT.read_text())
        run_id = ck["run_id"]
        started_iso = ck["started"]
        done_years = set(ck.get("done_years", []))
        year_stats = ck.get("year_stats", {})
        print(f"resuming run {run_id}: {len(done_years)} fiscal years already landed in {STAGING_TABLE} -- {sorted(done_years)}")
    else:
        run_id = str(uuid.uuid4())
        started_iso = dt.datetime.now(dt.timezone.utc).isoformat()
        print(f"fresh run {run_id}, {len(FISCAL_YEARS)} fiscal years to fetch: {FISCAL_YEARS}")

    started = dt.datetime.fromisoformat(started_iso)
    ingested_at = started.replace(tzinfo=None)

    chunk_shas: list[str] = []
    is_fresh_start = not done_years  # only recreate the staging table on a truly clean start

    # Pre-create the staging table with EXPLICIT all-VARCHAR columns. Relying on
    # write_pandas(auto_create_table=True) type inference bit twice on 2026-08-09:
    # even with every value stringified, a column that is entirely NULL across the
    # first-written year (FY2000: ORG_CITY, SPENDING_CATEGORIES, ...) still gets
    # inferred as NUMBER via the parquet null type, and the first later-year row
    # with real text in it kills the COPY ("Numeric value '[276, 320]' is not
    # recognized"). Explicit DDL removes inference from the picture entirely.
    _DATA_COLS = list(flatten({}).keys())
    if is_fresh_start:
        cols_ddl = ", ".join(f"{c} VARCHAR" for c in _DATA_COLS)
        cur0 = conn.cursor()
        cur0.execute(f"CREATE OR REPLACE TABLE {_fqt(STAGING_TABLE)} ({cols_ddl}, "
                     f"_INGESTED_AT TIMESTAMP_NTZ, _SOURCE_RUN_ID VARCHAR, _SRC_SHA256 VARCHAR)")
        cur0.close()

    for fy in FISCAL_YEARS:
        if fy in done_years:
            continue
        t0 = time.time()
        recs, stats = fetch_year(fy)
        year_stats[str(fy)] = stats
        print(f"FY{fy}: {len(recs)} distinct records ({time.time()-t0:.1f}s) -- "
              f"true_total={stats['true_total']} landed_distinct={stats['landed_distinct']} gap={stats['gap']}")

        if recs:
            flat = [flatten(r) for r in recs]
            df = pd.DataFrame(flat)
            df = df.where(pd.notnull(df), None)
            # Land EVERYTHING as text (the landing-layer convention). Leaving
            # native ints/floats here let write_pandas auto-type the staging
            # table off whatever FY2000-2002 happened to contain -- columns
            # that were all-None in those years (ORG_CITY, SPENDING_CATEGORIES,
            # ...) came out NUMBER, and the first later-year row with real text
            # in one of them killed the COPY (live crash 2026-08-09:
            # SPENDING_CATEGORIES '[276, 320]' vs a NUMBER column).
            for c in df.columns:
                df[c] = df[c].apply(_as_text)

            csv_bytes = df.to_csv(index=False).encode("utf-8")
            chunk_sha = hashlib.sha256(csv_bytes).hexdigest()
            chunk_shas.append(chunk_sha)

            df["_INGESTED_AT"] = ingested_at
            df["_SOURCE_RUN_ID"] = run_id
            df["_SRC_SHA256"] = chunk_sha  # per-year provenance (matches the chunked-load pattern elsewhere in this repo)

            from snowflake.connector.pandas_tools import write_pandas
            ok, _c, nrows, _ = write_pandas(
                conn, df, table_name=STAGING_TABLE,
                database=DATABASE, schema=SCHEMA,
                auto_create_table=False, overwrite=False, quote_identifiers=False,
            )
            if not ok:
                raise RuntimeError(f"write_pandas reported failure landing FY{fy} into {STAGING_TABLE}")
            is_fresh_start = False
            print(f"  -> wrote {nrows} rows to {STAGING_TABLE} (sha {chunk_sha[:12]})")
        else:
            print(f"  -> FY{fy} produced 0 records; nothing written")

        done_years.add(fy)
        _save_manifest(run_id, started_iso, done_years, year_stats)

    if not done_years:
        print("No fiscal years processed -- aborting.")
        sys.exit(1)

    # --- Global dedupe by APPL_ID (SQL-side, belt-and-suspenders on top of the
    # per-year Python-side dedupe) then atomic swap into the live table. ---
    print(f"\nDeduping {STAGING_TABLE} by APPL_ID and swapping into {TABLE} ...")
    snow.execute(conn, f"""
        CREATE OR REPLACE TABLE {_fqt(DEDUP_TABLE)} AS
        SELECT * EXCLUDE (_RN) FROM (
            SELECT *, ROW_NUMBER() OVER (PARTITION BY APPL_ID ORDER BY FISCAL_YEAR, _INGESTED_AT) AS _RN
            FROM {_fqt(STAGING_TABLE)}
        )
        WHERE _RN = 1
    """)
    snow.execute(conn, f"CREATE TABLE IF NOT EXISTS {_fqt(TABLE)} LIKE {_fqt(DEDUP_TABLE)}")
    snow.execute(conn, f"ALTER TABLE {_fqt(DEDUP_TABLE)} SWAP WITH {_fqt(TABLE)}")
    snow.execute(conn, f"DROP TABLE IF EXISTS {_fqt(DEDUP_TABLE)}")
    snow.execute(conn, f"DROP TABLE IF EXISTS {_fqt(STAGING_TABLE)}")

    cur = conn.cursor()
    cur.execute(f"SELECT COUNT(*), COUNT(DISTINCT APPL_ID) FROM {_fqt(TABLE)}")
    total_rows, distinct_appl = cur.fetchone()
    print(f"\nFINAL (post-dedupe, live table): {total_rows} rows, {distinct_appl} distinct APPL_ID")

    # --- Final honest per-year report: live landed counts vs a FRESH true-total
    # re-check (not just the numbers captured mid-fetch, which can drift over a
    # multi-hour run as NIH RePORTER data changes -- most visibly for the current,
    # still-open fiscal year). ---
    cur.execute(f"SELECT FISCAL_YEAR, COUNT(*), COUNT(DISTINCT APPL_ID) FROM {_fqt(TABLE)} GROUP BY FISCAL_YEAR ORDER BY FISCAL_YEAR")
    landed_by_year = {int(r[0]): (r[1], r[2]) for r in cur.fetchall() if r[0] is not None}

    print("\n--- PER-YEAR REPORT (live table vs a fresh API re-check at report time) ---")
    report_lines = []
    any_residual_gap = False
    for fy in sorted(FISCAL_YEARS):
        fetch_stats = year_stats.get(str(fy), {})
        fresh_true_total = _total(fy)
        landed_rows, landed_distinct = landed_by_year.get(fy, (0, 0))
        report_gap = (fresh_true_total - landed_distinct) if fresh_true_total is not None else None
        line = (f"FY{fy}: landed={landed_distinct} (rows={landed_rows}) | "
                f"true_total@fetch={fetch_stats.get('true_total')} gap@fetch={fetch_stats.get('gap')} | "
                f"true_total@report={fresh_true_total} gap@report={report_gap}")
        if report_gap and report_gap > 0:
            any_residual_gap = True
            line += "  <-- RESIDUAL GAP"
        elif report_gap is not None and report_gap < 0:
            line += "  (landed >= re-check total; likely fetched before/during new NIH submissions -- not a truncation)"
        print("  " + line)
        report_lines.append(line)

    ended = dt.datetime.now(dt.timezone.utc)
    manifest_sha = hashlib.sha256("".join(chunk_shas).encode("utf-8")).hexdigest()
    message = (f"Recursive date-window bisection fix ({len(FISCAL_YEARS)} fiscal years, "
               f"primary field=date_added, fallback={DATE_FIELDS[1:]}). "
               f"Final: {total_rows} rows / {distinct_appl} distinct APPL_ID. "
               + ("RESIDUAL GAPS FOUND -- see per-year report in run logs." if any_residual_gap
                  else "No residual gaps vs fresh per-year API re-check."))
    status = "partial" if any_residual_gap else "success"
    ingest._log_run(conn, source_id="fed_nih_reporter", run_id=run_id,
                     status=status, row_count=total_rows, file_bytes=None,
                     sha=manifest_sha, url="https://api.reporter.nih.gov/",
                     started=started, ended=ended, message=message)

    if CKPT.exists():
        CKPT.unlink()

    print(f"\n{message}")
    if any_residual_gap:
        print("NOTE: residual gaps are logged above plainly, not hidden -- see the per-year report.")
        print("Logged status=partial -- exiting non-zero.")
        sys.exit(1)


if __name__ == "__main__":
    main()
