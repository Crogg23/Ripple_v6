"""Peer-cohort outlier detection on workplace injury rates.

THE MISSION ARGUMENT (CLAUDE.md section 1)
"Recon on power. We look at all of them, the same way, with the same lens. No targets.
No favorites." This module is that sentence in code. It never takes a company name as
input. It scores EVERY establishment that filed an OSHA 300A, assigns each to a peer
cohort, and lets the outliers surface themselves. Picking a target first is the failure
mode; this makes it structurally impossible.

WHY A COHORT AND NOT A RAW RANKING
Raw injury counts rank by size -- the biggest employer always "wins", which is a
finding about headcount, not about safety. Raw rates rank by industry -- a slaughter-
house always beats an insurance office, which is a finding about what the work IS.
Neither tells you whether an employer is worse THAN ITS OWN KIND.

So the unit of comparison is the cohort: same industry (NAICS), same size band. Inside
a cohort, the work and the scale are held roughly constant, and what is left is how
this employer treats the people doing that work. That is the accountability question.

THE RATE IS OSHA'S OWN, NOT OURS
    incidence rate = (cases x 200,000) / hours worked
200,000 = 100 full-time workers x 40 hours x 50 weeks, i.e. "cases per 100 full-time
workers per year". This is the formula OSHA publishes and the one employers already
compute for themselves, so the arithmetic is not ours to defend. Using hours worked
(not headcount) as the denominator is what makes part-time, seasonal and high-turnover
workforces comparable -- and it is the field 99.6% of 2024 rows actually populate.

HONESTY CONSTRAINTS BUILT IN
  - Establishments with too few hours are EXCLUDED, not ranked. At 5,000 hours a
    single injury produces a rate of 40, which would top the list on noise alone.
    Small denominators manufacture outliers; this is the single most common way a
    rate-based ranking lies.
  - Cohorts with too few members are EXCLUDED. "Worst in a cohort of 2" is not a
    finding.
  - A z-score AND a fold-vs-median are both reported. z alone is misleading on the
    skewed distributions injury data actually has; the fold is what a human can read.
  - TOTAL_DEATHS is reported separately and never folded into the rate. A death is not
    a more-severe injury, it is a different event, and averaging it away is exactly how
    a fatality becomes invisible in a summary statistic.
  - Nothing here publishes. Output is a ranked table for human review, per the
    constitution's hard rule on sign-off.

    python -m connect.cohort                     # 2024, default thresholds
    python -m connect.cohort --year 2023
    python -m connect.cohort --naics-digits 4    # broader cohorts
    python -m connect.cohort --write             # persist COHORT_OUTLIERS
"""

from __future__ import annotations

import argparse
import csv
import os
import uuid

from . import db, store

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "outputs")

OSHA_TABLES = {
    2023: "FED_OSHA_ITA_300A_SUMMARY_2023",
    2024: "FED_OSHA_ITA_300A_SUMMARY_2024",
    2025: "FED_OSHA_ITA_300A_SUMMARY_2025",
}

# OSHA's standard base: 100 full-time equivalents working a 2,000-hour year.
OSHA_BASE_HOURS = 200_000

# An establishment needs this many hours before its rate is stable enough to rank.
# 20,000 hours = 10 full-time workers for a year. Below that, one injury swings the
# rate by 10+ points and the ranking measures luck, not safety.
MIN_HOURS = 20_000
# A cohort needs this many establishments before "outlier" means anything.
MIN_COHORT = 10


def _rate_sql(case_col: str) -> str:
    return f"({case_col} * {OSHA_BASE_HOURS}) / NULLIF(hours, 0)"


def build_sql(year: int, naics_digits: int, min_hours: int, min_cohort: int) -> str:
    """The whole analysis as one SQL statement, so it is copy-pasteable as a receipt.

    Grain note: OSHA 300A is filed per ESTABLISHMENT (a physical worksite), and one
    company files many. We aggregate to (EIN, establishment) rather than to EIN alone
    because a company-level rate would average a dangerous plant together with its
    head office and hide the plant. ESTABLISHMENT_ID is used when present, falling
    back to the normalized street address -- 300A filings reuse ESTABLISHMENT_ID
    inconsistently across years.
    """
    tbl = OSHA_TABLES[year]
    return f"""
WITH raw AS (
    SELECT
        LPAD(REGEXP_REPLACE(EIN, '[^0-9]', ''), 9, '0')            AS ein,
        NULLIF(TRIM(COMPANY_NAME), '')                             AS company,
        NULLIF(TRIM(ESTABLISHMENT_NAME), '')                       AS establishment,
        COALESCE(NULLIF(TRIM(ESTABLISHMENT_ID), ''),
                 UPPER(TRIM(STREET_ADDRESS)))                      AS est_key,
        UPPER(TRIM(STATE))                                         AS state,
        UPPER(TRIM(CITY))                                          AS city,
        LEFT(REGEXP_REPLACE(NAICS_CODE, '[^0-9]', ''), {naics_digits}) AS naics,
        NULLIF(TRIM(INDUSTRY_DESCRIPTION), '')                     AS industry,
        TRY_TO_NUMBER(TOTAL_HOURS_WORKED)                          AS hours,
        TRY_TO_NUMBER(ANNUAL_AVERAGE_EMPLOYEES)                    AS employees,
        TRY_TO_NUMBER(TOTAL_DEATHS)                                AS deaths,
        TRY_TO_NUMBER(TOTAL_DAFW_CASES)                            AS dafw_cases,
        TRY_TO_NUMBER(TOTAL_DAFW_DAYS)                             AS dafw_days,
        TRY_TO_NUMBER(TOTAL_DJTR_CASES)                            AS djtr_cases,
        TRY_TO_NUMBER(TOTAL_INJURIES)                              AS injuries,
        TRY_TO_NUMBER(TOTAL_OTHER_CASES)                            AS other_cases
    FROM LIBRARY_RAW.LANDING.{tbl}
    WHERE TRIM(EIN) <> ''
      AND TRY_TO_NUMBER(NAICS_CODE) IS NOT NULL
),
est AS (
    -- One row per physical worksite. SUM across duplicate filings for the same site.
    SELECT ein, est_key,
           MAX(company) AS company, MAX(establishment) AS establishment,
           MAX(state) AS state, MAX(city) AS city,
           MAX(naics) AS naics, MAX(industry) AS industry,
           SUM(hours) AS hours, SUM(employees) AS employees,
           SUM(deaths) AS deaths,
           SUM(dafw_cases) AS dafw_cases, SUM(dafw_days) AS dafw_days,
           SUM(djtr_cases) AS djtr_cases, SUM(other_cases) AS other_cases,
           SUM(injuries) AS injuries
    FROM raw
    GROUP BY ein, est_key
),
dup_denom AS (
    -- COPY-PASTED DENOMINATOR DETECTOR.
    -- Verified failure this guards against: Beth Israel Lahey Health filed six
    -- separate Boston establishments (Deaconess Medical Center, New England Baptist,
    -- Joslin, ...) each reporting the IDENTICAL 56 employees and 56,777 hours. BIDMC
    -- alone employs thousands. One denominator was entered once and repeated across
    -- every site, so any site that also reported real injuries got a rate inflated by
    -- roughly the number of sites sharing the number -- which put it 83x above its
    -- cohort on arithmetic, not on safety.
    -- A denominator reused verbatim across 3+ of one filer's establishments is not a
    -- measurement, so those establishments are excluded rather than ranked.
    SELECT ein, employees, hours
    FROM est
    WHERE employees > 0 AND hours > 0
    GROUP BY ein, employees, hours
    HAVING COUNT(DISTINCT est_key) >= 3
),
dup_site AS (
    -- SAME-SITE DOUBLE-FILING DETECTOR (verified in the 2024 file, entity-quality
    -- pass): a small number of establishments are filed TWICE under two different
    -- ESTABLISHMENT_ID values for what is the identical physical site -- same EIN,
    -- same establishment name, same city/state, same employee count, hours agreeing
    -- to within rounding (e.g. Commodity Forwarders LAX-5814: 552,815 hours filed
    -- under two IDs; US Foods Norcross: 362,230 vs 362,231 hours). ESTABLISHMENT_ID
    -- is otherwise fully populated and unique in this file (no address-key fallback
    -- was needed), so this is a genuine double-filing, not the fallback-collision
    -- risk the grain comment above warns about. Ranking both would count one
    -- workplace as two entries in the finding, so -- same policy as dup_denom --
    -- both copies are excluded rather than one being guessed as authoritative.
    SELECT ein, UPPER(TRIM(establishment)) AS est_name, city, state, employees
    FROM est
    WHERE establishment IS NOT NULL AND employees > 0
    GROUP BY ein, UPPER(TRIM(establishment)), city, state, employees
    HAVING COUNT(DISTINCT est_key) >= 2 AND MAX(hours) - MIN(hours) <= 5
),
scored AS (
    SELECT *,
           -- DART = Days Away, Restricted, or Transferred. The OSHA severity measure
           -- that matters: it counts injuries that actually cost someone work, and
           -- excludes first-aid-only cases an employer can classify away.
           dafw_cases + djtr_cases                        AS dart_cases,
           {_rate_sql('(dafw_cases + djtr_cases)')}       AS dart_rate,
           {_rate_sql('(dafw_cases + djtr_cases + other_cases)')} AS trir,
           -- Severity: days lost per days-away case. High days-per-case with a low
           -- case count is a DIFFERENT signal (few but catastrophic injuries) and
           -- would be invisible in a rate alone.
           dafw_days / NULLIF(dafw_cases, 0)              AS days_per_case,
           -- Size band. Boundaries chosen to match how OSHA/BLS report and how
           -- regulatory thresholds actually fall (11+, 20+, 50+, 250+).
           CASE WHEN employees < 20  THEN '1-19'
                WHEN employees < 50  THEN '20-49'
                WHEN employees < 100 THEN '50-99'
                WHEN employees < 250 THEN '100-249'
                WHEN employees < 1000 THEN '250-999'
                ELSE '1000+' END                          AS size_band,
           hours / NULLIF(employees, 0)                   AS hours_per_emp
    FROM est e
    WHERE hours >= {min_hours}
      -- PLAUSIBILITY GATE. 300A is self-reported and both denominator fields are
      -- dirty. Two distinct failures, both verified in the 2024 file:
      --
      -- (a) Absurdly HIGH hours. 103 rows claim >100M hours; the worst ("CDI", 133
      --     employees) claims 862,847,000,000 hours = 6.5 BILLION hours per employee.
      --     Left in, the summed total came to 995 billion hours -- about four times
      --     the entire US labor supply -- and each such row silently deflated the
      --     pooled rate of its cohort by contributing vast denominator and no
      --     numerator.
      --
      -- (b) Implausibly LOW hours against headcount, which INFLATES a rate. Cypress
      --     Skilled Nursing's Haralson site reported 155 employees but only 95,341
      --     hours = 615 hours each. Its 101 injuries then scored a DART rate of 212,
      --     ~95x its cohort. At a normal full-time year the same injuries score ~65 --
      --     still bad, but a third of the headline. The rate was measuring a short
      --     denominator, not a dangerous workplace.
      --
      -- So hours per employee must land in a real range. 800-3,500 spans roughly
      -- 0.4 FTE (genuine part-time/seasonal) to 1.75 FTE (heavy overtime). Outside
      -- that band the two self-reported fields contradict each other and neither can
      -- be trusted as the denominator.
      AND employees > 0
      AND hours / employees BETWEEN 800 AND 3500
      -- and the denominator must not be a number copy-pasted across sites
      AND NOT EXISTS (SELECT 1 FROM dup_denom d
                      WHERE d.ein = e.ein AND d.employees = e.employees
                        AND d.hours = e.hours)
      -- and the site must not be the identical physical location double-filed
      -- under a second ESTABLISHMENT_ID (dup_site, see above)
      AND NOT EXISTS (SELECT 1 FROM dup_site d
                      WHERE d.ein = e.ein AND d.est_name = UPPER(TRIM(e.establishment))
                        AND d.city = e.city AND d.state = e.state AND d.employees = e.employees)
),
cohort AS (
    SELECT naics, size_band,
           COUNT(*)                        AS cohort_n,
           MEDIAN(dart_rate)               AS cohort_median_dart,
           AVG(dart_rate)                  AS cohort_mean_dart,
           STDDEV_SAMP(dart_rate)          AS cohort_sd_dart,
           SUM(dart_cases)                 AS cohort_dart_cases,
           SUM(hours)                      AS cohort_hours,
           -- Cohort-wide rate: total cases over total hours. Not the mean of rates --
           -- that would weight a 10-person site the same as a 10,000-person one.
           (SUM(dart_cases) * {OSHA_BASE_HOURS}) / NULLIF(SUM(hours), 0) AS cohort_pooled_dart
    FROM scored
    GROUP BY naics, size_band
    HAVING COUNT(*) >= {min_cohort}
       -- The cohort itself must have a measurable injury rate. Dividing by a pooled
       -- rate near zero manufactures enormous folds out of nothing -- the exact
       -- failure the median version of this query produced (cohorts whose median was
       -- 0.00 or 0.15 generated 448x "outliers" that were pure denominator noise).
       AND (SUM(dart_cases) * {OSHA_BASE_HOURS}) / NULLIF(SUM(hours), 0) >= 0.25
)
SELECT
    s.ein, s.est_key, s.company, s.establishment, s.city, s.state,
    s.naics, s.industry, s.size_band,
    s.employees, s.hours,
    s.deaths, s.dart_cases, s.dafw_days,
    ROUND(s.dart_rate, 2)              AS dart_rate,
    ROUND(s.trir, 2)                   AS trir,
    ROUND(s.days_per_case, 1)          AS days_per_case,
    c.cohort_n,
    ROUND(c.cohort_median_dart, 2)     AS cohort_median_dart,
    ROUND(c.cohort_pooled_dart, 2)     AS cohort_pooled_dart,
    -- PRIMARY COMPARATOR: fold vs the cohort's POOLED rate (total cases / total
    -- hours). Pooled, not median: a median collapses to 0.00 in any cohort where
    -- half the filers report no DART cases, and dividing by that produced garbage.
    -- Pooled is stable because it is one ratio over the whole cohort's exposure.
    ROUND(s.dart_rate / NULLIF(c.cohort_pooled_dart, 0), 2) AS fold_vs_pooled,
    -- Kept for reference only, NOT for ranking, so the skew stays visible.
    ROUND(s.dart_rate / NULLIF(c.cohort_median_dart, 0), 2) AS fold_vs_median,
    -- z-score, reported alongside the fold and never alone. Injury-rate
    -- distributions are right-skewed, so a z of 3 does not carry its
    -- normal-distribution meaning here.
    ROUND((s.dart_rate - c.cohort_mean_dart) / NULLIF(c.cohort_sd_dart, 0), 2) AS z_score,
    -- Percentile within cohort. Distribution-free, so it survives the skew.
    ROUND(PERCENT_RANK() OVER (PARTITION BY s.naics, s.size_band
                               ORDER BY s.dart_rate), 4) AS pct_rank_in_cohort
FROM scored s
JOIN cohort c ON c.naics = s.naics AND c.size_band = s.size_band
WHERE s.dart_rate > 0
"""


def run(year: int = 2024, naics_digits: int = 4, min_hours: int = MIN_HOURS,
        min_cohort: int = MIN_COHORT, top: int = 25, write: bool = False) -> dict:
    if year not in OSHA_TABLES:
        raise SystemExit(f"no OSHA table for {year}; have {sorted(OSHA_TABLES)}")
    sql = build_sql(year, naics_digits, min_hours, min_cohort)
    run_id = uuid.uuid4().hex[:16]
    conn = db.connect()
    try:
        print(f"cohort: scoring every {year} OSHA 300A establishment "
              f"(NAICS-{naics_digits} x size band, >={min_hours:,}h, cohort >={min_cohort})")

        # Coverage first -- what fraction of filings survive the honesty filters, so
        # nobody reads the ranking as if it covered everyone.
        cov = db.dicts(conn, f"""
            WITH ranked_est AS ({sql})
            SELECT COUNT(*) AS ranked,
                   COUNT(DISTINCT ein) AS employers,
                   COUNT(DISTINCT naics || '|' || size_band) AS cohorts,
                   SUM(deaths) AS deaths,
                   SUM(dart_cases) AS dart_cases,
                   SUM(hours) AS hours,
                   ROUND(MEDIAN(dart_rate),2) AS median_dart
            FROM ranked_est""")[0]
        total_filed = db.scalar(conn, f"""
            SELECT COUNT(*) FROM LIBRARY_RAW.LANDING.{OSHA_TABLES[year]}
            WHERE TRIM(EIN) <> ''""")
        print(f"  {cov['RANKED']:,} establishments ranked from {int(total_filed or 0):,} "
              f"filings ({cov['EMPLOYERS']:,} employers, {cov['COHORTS']:,} cohorts)")
        print(f"  covering {int(cov['HOURS'] or 0):,} hours worked, "
              f"{int(cov['DART_CASES'] or 0):,} DART cases, "
              f"{int(cov['DEATHS'] or 0):,} deaths; median DART rate {cov['MEDIAN_DART']}")

        # The ranking. Ordered by fold, with a floor on cases so a 1-case site cannot
        # top the list on a small denominator.
        rows = db.dicts(conn, f"""
            WITH ranked_est AS ({sql})
            SELECT * FROM ranked_est
            WHERE dart_cases >= 5 AND fold_vs_pooled >= 2
            ORDER BY fold_vs_pooled DESC, dart_cases DESC
            LIMIT {top}""")

        print(f"\n  worst {len(rows)} vs their own cohort "
              f"(>=5 DART cases, >=2x cohort median):\n")
        print(f"  {'fold':>5}  {'DART':>6}  {'cohort':>7}  {'cases':>6}  {'deaths':>6}  "
              f"{'n':>5}  employer / site")
        for r in rows:
            name = (r["COMPANY"] or r["ESTABLISHMENT"] or r["EIN"])[:44]
            site = f"{r['CITY'] or ''}, {r['STATE'] or ''}".strip(", ")[:20]
            print(f"  {r['FOLD_VS_POOLED']:>5}x {r['DART_RATE']:>6}  "
                  f"{r['COHORT_POOLED_DART']:>7}  {int(r['DART_CASES']):>6}  "
                  f"{int(r['DEATHS'] or 0):>6}  {int(r['COHORT_N']):>5}  {name} ({site})")

        # Deaths get their own list. A fatality must never be reachable only by
        # scrolling a rate ranking.
        fatal = db.dicts(conn, f"""
            WITH ranked_est AS ({sql})
            SELECT company, establishment, city, state, industry, employees,
                   deaths, dart_cases, dart_rate, cohort_pooled_dart, fold_vs_pooled
            FROM ranked_est WHERE deaths >= 1
            ORDER BY deaths DESC, fold_vs_pooled DESC NULLS LAST LIMIT 15""")
        print(f"\n  establishments reporting a WORKPLACE DEATH (top {len(fatal)} of "
              f"{int(cov['DEATHS'] or 0):,} total deaths):\n")
        for r in fatal:
            name = (r["COMPANY"] or r["ESTABLISHMENT"] or "?")[:44]
            site = f"{r['CITY'] or ''}, {r['STATE'] or ''}".strip(", ")[:20]
            fold = r["FOLD_VS_POOLED"]
            print(f"  {int(r['DEATHS'])} death(s)  DART {r['DART_RATE']:>6} "
                  f"({'—' if fold is None else str(fold) + 'x'} cohort)  {name} ({site})")

        os.makedirs(OUT_DIR, exist_ok=True)
        full = db.dicts(conn, f"""
            WITH ranked_est AS ({sql})
            SELECT * FROM ranked_est WHERE dart_cases >= 5 AND fold_vs_pooled >= 2
            ORDER BY fold_vs_pooled DESC""")
        path = os.path.join(OUT_DIR, f"cohort_outliers_{year}.csv")
        if full:
            with open(path, "w", newline="", encoding="utf-8") as fh:
                w = csv.DictWriter(fh, fieldnames=list(full[0].keys()))
                w.writeheader()
                w.writerows(full)
            print(f"\n  {len(full):,} outliers -> {path}")

        if write:
            store.ensure_schema(conn)
            fqn = store.cfqn(f"COHORT_OUTLIERS_{year}")
            db.rows(conn, f"""CREATE OR REPLACE TABLE {fqn} AS
                WITH ranked_est AS ({sql})
                SELECT *, '{run_id}' AS RUN_ID, CURRENT_TIMESTAMP() AS BUILT_AT
                FROM ranked_est""")
            n = db.scalar(conn, f"SELECT COUNT(*) FROM {fqn}")
            print(f"  persisted {int(n or 0):,} scored establishments -> {fqn}")
        return {"ranked": int(cov["RANKED"] or 0), "outliers": len(full)}
    finally:
        conn.close()


def main() -> int:
    ap = argparse.ArgumentParser(prog="connect.cohort")
    ap.add_argument("--year", type=int, default=2024, choices=sorted(OSHA_TABLES))
    ap.add_argument("--naics-digits", type=int, default=4,
                    help="cohort industry granularity (2=sector, 6=exact); default 4")
    ap.add_argument("--min-hours", type=int, default=MIN_HOURS)
    ap.add_argument("--min-cohort", type=int, default=MIN_COHORT)
    ap.add_argument("--top", type=int, default=25)
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    run(year=a.year, naics_digits=a.naics_digits, min_hours=a.min_hours,
        min_cohort=a.min_cohort, top=a.top, write=a.write)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
