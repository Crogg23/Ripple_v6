"""score_warehouse -- the ruler. One number, from checks, not from an opinion.

The 2026-09-20 pre-launch audit (reports/warehouse_preflight_qa_2026-09-20.md) graded the
warehouse 58 of 100 with no formula. This pins the score to that audit's own 23 findings:

    severe 3.5 points, moderate 1.2, minor 0.3
    9 x 3.5 + 7 x 1.2 + 7 x 0.3 = 42 points lost  ->  58

Each finding is one check. A check returns a share of its points:
    1.0  closed and proven   (a live query or a file fact says so)
    0.75 mostly closed       (the mechanism is fixed, a named remainder is not)
    0.5  labelled only       (a caveat is written, nothing stops a bad query)
    0.0  open, or not checked -- not checked is never counted as closed
Problems found AFTER the audit are debt: they take points off until closed, so the score
can fall as well as rise.

Everything here is read-only: SELECT and information_schema through the Python door
(connect/db.py), plus reads of files in this repo. It never runs dbt and never writes to
the warehouse. A few items cannot be proven by a query; they live in
reports/score_manual_items.tsv and print as MANUAL so nobody mistakes them for measured.

    python scripts/score_warehouse.py            # full run, about 4 minutes
    python scripts/score_warehouse.py --fast     # skips the 254-view fetch and the ARCOS key scan
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DBT = REPO / "library-onboarding" / "ripple_dbt"
MARTS = DBT / "models" / "marts"
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

from connect import db  # noqa: E402
import guard_mart_casts as casts  # noqa: E402

SEVERE, MODERATE, MINOR, DEBT = 3.5, 1.2, 0.3, 0.5
MANUAL = REPO / "reports" / "score_manual_items.tsv"
CONN = None
FAST = False


# ---------- helpers ----------

def rows(sql: str):
    return db.rows(CONN, sql)


def one(sql: str):
    return rows(sql)[0][0]


def mart_table(pattern: str) -> str | None:
    """Fully qualified name of the one LIBRARY_MARTS base table or view matching pattern (not TIMELINE)."""
    r = rows(f"""select table_schema, table_name from LIBRARY_MARTS.information_schema.tables
        where table_schema <> 'TIMELINE' and table_name ilike '{pattern}' and table_name not ilike '%__PREV_%'
        order by length(table_name)""")
    return f"LIBRARY_MARTS.{r[0][0]}.{r[0][1]}" if r else None


def has_column(fqn: str, column: str) -> bool:
    d, s, t = fqn.split(".")
    return bool(rows(f"""select 1 from {d}.information_schema.columns
        where table_schema='{s}' and table_name='{t}' and column_name='{column.upper()}'"""))


def file_says(rel_glob: str, pattern: str) -> bool:
    rx = re.compile(pattern, re.I | re.S)
    return any(rx.search(p.read_text(encoding="utf-8", errors="replace")) for p in DBT.glob(rel_glob))


def bare_casts(root: Path, need_source: bool) -> tuple[int, int]:
    """(files, calls) still holding a bare cast, by the same rules guard_mart_casts.py rewrites."""
    files = calls = 0
    for p in sorted(root.rglob("*.sql")):
        raw = p.read_text(encoding="utf-8", errors="replace")
        if re.search(r"enabled\s*=\s*false", raw, re.I):
            continue
        if need_source != ("source(" in raw):
            continue
        n = len(casts.plan_file(p)[1])
        if n:
            files, calls = files + 1, calls + n
    return files, calls


def manual(item: str) -> tuple[float, str]:
    if MANUAL.exists():
        with MANUAL.open(encoding="utf-8", newline="") as fh:
            for r in csv.DictReader(fh, delimiter="\t"):
                if r["item"] == item:
                    return float(r["share"]), f"MANUAL {r['date']}: {r['proof']}"
    return 0.0, "MANUAL: no entry in reports/score_manual_items.tsv, counted open"


# ---------- the 9 severe ----------

def s1_bare_casts():
    sf, sc = bare_casts(MARTS, need_source=True)
    rf, rc = bare_casts(MARTS, need_source=False)
    share = 1.0 if sc == 0 and rc == 0 else 0.75 if sc == 0 else 0.0
    return share, f"marts reading source(): {sc} bare casts in {sf} files; marts reading staging: {rc} in {rf} files"


def s2_rounding():
    pos = one("select count_if(physn_cnt <> floor(physn_cnt)) from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER")
    pd_ = one("select count_if(total_30day_fills <> floor(total_30day_fills)) from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PARTD_PRESCRIBERS")
    nan = one("select count_if(cost_accounting_standards_clause = 'NaN'::float) from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS_FULL")
    ok = pos > 0 and pd_ > 0 and nan == 0
    return (1.0 if ok else 0.0), f"rows keeping a fraction: POS_OTHER {pos:,}, Part D fills {pd_:,}; NaN left in contracts_full {nan:,}"


def s3_fec_memo():
    flag = has_column("LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_COMMITTEE_TO_CANDIDATE", "IS_MEMO_TRANSACTION")
    agg = "LIBRARY_MARTS.PUBLIC.MONEY_IN_POLITICS__FEC_INDIV_BY_STATE_CYCLE_AGG"
    cycles, recs = rows(f"select count(distinct cycle_year), sum(n_records) from {agg}")[0]
    # same rule the aggregate applies: memo rows out, and transaction years outside 1979-2026 out (junk dates)
    want = one("""select count(*) from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS
        where not coalesce(is_memo_transaction, false) and year(transaction_date) between 1979 and 2026""")
    agg_ok = int(recs or 0) == int(want)
    share = 1.0 if flag and agg_ok else 0.5 if flag else 0.0
    return share, f"mart memo flag {'present' if flag else 'MISSING'}; public aggregate {cycles} cycles, {int(recs or 0):,} records vs {int(want):,} non-memo in the mart"


def s4_usaspending_cap():
    bad = one("select count_if(year(_loaded_at) > 2100) from LIBRARY_MARTS.TIMELINE.ECONOMICS__FED_USASPENDING_CONTRACTS_FULL")
    capped = rows("""select count(*), count_if(n = 1000000) from (
        select action_date_fiscal_year fy, count(*) n from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_ASSISTANCE_FULL group by 1)""")[0]
    share = 1.0 if bad == 0 and capped[1] == 0 else 0.5 if bad == 0 else 0.0
    return share, f"contracts timeline rows with a broken clock {bad:,}; assistance mart fiscal years sitting at exactly 1,000,000 rows: {capped[1]} of {capped[0]}"


def s5_capped_samples():
    out, ok = [], True
    for mart, land in [("LIBRARY_MARTS.CRIMINAL_JUSTICE.CRIMINAL_JUSTICE__FED_BJS_DATA", "FED_BJS_DATA_FULL"),
                       ("LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_HUDOC", "INTL_HUDOC_FULL")]:
        m, l = one(f"select count(*) from {mart}"), one(f"select count(*) from LIBRARY_RAW.LANDING.{land}")
        ok &= m == l
        out.append(f"{land} {l:,} -> mart {m:,}")
    return (1.0 if ok else 0.0), "; ".join(out)


def _label_or_lock(table_pattern: str, lock_column: str, yml_glob: str, label_rx: str):
    t = mart_table(table_pattern)
    if t and has_column(t, lock_column):
        return 1.0, f"lock column {lock_column} is live on {t.split('.')[-1]}"
    if file_says(yml_glob, label_rx):
        return 0.5, f"label written in schema, no {lock_column} column live"
    return 0.0, "no label, no lock"


def s6_partb():
    # Skeptic 2026-09-21: a per-row coverage column is a strong label, not a lock -- a careless sum is still short.
    # Full credit only when a plain sum off the service table matches the provider totals.
    t = mart_table("%PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER_AND_SERVI%")
    base = _label_or_lock("%PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER_AND_SERVI%", "SERVICE_ROWS_COVER_PCT",
                          "models/marts/health/schema_fed_cms_medicare_physician_other_practitioners_by_provider_and_servi.yml",
                          r"suppress|fewer than 11|under 11|floor")
    if base[0] < 1.0:
        return base
    nul, over, seen = rows(f"select count_if(service_rows_cover_pct is null), count_if(service_rows_cover_pct > 100.5), sum(est_mdcr_pymt_amt) from {t}")[0]
    true_total = one("select sum(tot_mdcr_pymt_amt) from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER")
    pct = 100 * float(seen) / float(true_total)
    if over or nul > 50:
        return 0.5, f"coverage column misbehaves: {nul:,} null, {over:,} over 100"
    share = 1.0 if pct >= 99.5 else 0.75
    return share, f"coverage column live, {nul} null, 0 over 100; a plain sum off the table reaches {pct:.1f} percent of the provider totals"


def s7_dme():
    # the family-undercount trap lives in the by-referrer mart; the by-supplier mart has no family or flag columns.
    # Skeptic 2026-09-21: is_suppressed can never be null, so its presence proves nothing. Full credit only when the
    # three families plus a remainder column add back to the total on every row.
    t = mart_table("%DURABLE_MEDICAL_EQUIPMENT%BY_REFER%")
    base = _label_or_lock("%DURABLE_MEDICAL_EQUIPMENT%BY_REFER%", "IS_SUPPRESSED",
                          "models/marts/health/schema_fed_cms_medicare_durable_medical_equipment_devices_supplies_by_refer.yml", r"suppress|undercount")
    if base[0] < 1.0:
        return base
    if not has_column(t, "UNASSIGNED_SUPLR_MDCR_PYMT_AMT"):
        return 0.5, "flag and coverage columns live, but a family sum is still short and nothing reconciles it"
    off = one(f"""select count_if(abs(coalesce(dme_suplr_mdcr_pymt_amt,0) + coalesce(pos_suplr_mdcr_pymt_amt,0) + coalesce(drug_suplr_mdcr_pymt_amt,0)
        + coalesce(unassigned_suplr_mdcr_pymt_amt,0) - coalesce(suplr_mdcr_pymt_amt,0)) > 0.01) from {t}""")
    return (1.0 if off == 0 else 0.5), f"families plus the unassigned remainder miss the total on {off:,} rows"


def s8_public_shelf():
    if FAST:
        return 0.0, "skipped by --fast, counted open"
    shelves = [("THE_LIBRARY", "select table_schema, table_name from THE_LIBRARY.information_schema.views where table_schema <> 'INFORMATION_SCHEMA'"),
               ("LIBRARY_MARTS", "select table_schema, table_name from LIBRARY_MARTS.information_schema.views where table_schema in ('TIMELINE', 'FINDINGS')")]
    total, bad = 0, []
    for dbname, sql in shelves:
        for s, t in rows(sql):
            total += 1
            try:
                rows(f'select * from {dbname}."{s}"."{t}" limit 1')
            except Exception:  # noqa: BLE001
                bad.append(f"{dbname}.{s}.{t}")
    return (1.0 if not bad else 0.0), f"{total - len(bad)} of {total} public, timeline and findings views return a real row{'; broken: ' + ', '.join(bad[:5]) if bad else ''}"


def s9_arcos_key():
    t = "LIBRARY_MARTS.HEALTH.HEALTH__FED_DEA_ARCOS"
    if has_column(t, "ARCOS_ROW_KEY"):
        if FAST:
            return 0.5, "ARCOS_ROW_KEY exists; uniqueness scan skipped by --fast"
        n, d, nul = rows(f"select count(*), count(distinct arcos_row_key), count_if(arcos_row_key is null) from {t}")[0]
        return (1.0 if n == d and nul == 0 else 0.5), f"ARCOS_ROW_KEY {d:,} distinct over {n:,} rows, {nul:,} null"
    lab = file_says("models/marts/health/schema_fed_dea_arcos.yml", r"never count or dedupe on transaction_id")
    return (0.5 if lab else 0.0), "no row key column; label " + ("written" if lab else "missing")


# ---------- the 7 moderate ----------

def m1_orphan_staging_views():
    live = {r[0] for r in rows("select table_name from LIBRARY_STAGING.information_schema.views where table_schema='DBT_CROGERS'")}
    files = {p.stem.upper() for p in (DBT / "models").rglob("*.sql")}
    orphans = sorted(live - files)
    return (1.0 if not orphans else 0.0), f"{len(orphans)} live staging views have no model file behind them, e.g. {', '.join(orphans[:3])}"


def m2_staging_outside_sweep():
    f, c = bare_casts(DBT / "models" / "staging", need_source=True)
    return (1.0 if c == 0 else 0.0), f"{c} bare casts in {f} staging files"


def m3_partd_vintage():
    # two live Part D marts; the by-drug raw twin is enabled=false in dbt_project.yml and has no table
    live = ("HEALTH__FED_CMS_PARTD_PRESCRIBERS", "HEALTH__FED_CMS_PART_D_PRESCRIBERS")
    got = [t for t in live if has_column(f"LIBRARY_MARTS.HEALTH.{t}", "DATA_YEAR")]
    if len(got) == len(live):
        yrs = [one(f"select listagg(distinct data_year, ',') from LIBRARY_MARTS.HEALTH.{t}") for t in live]
        return 1.0, f"DATA_YEAR live on both Part D marts: {yrs[0]} and {yrs[1]}; typed by hand from CMS docs, the landing tables carry no year"
    lab = file_says("models/marts/health/schema_fed_cms_part*d*.yml", r"DY20\d\d|data year|vintage")
    return (0.5 if lab else 0.0), f"DATA_YEAR on {len(got)} of {len(live)} live Part D marts; label " + ("written" if lab else "missing")


def m4_chow_constant():
    t, col = "LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME", "PROVIDER_CHANGED_OWNERSHIP_IN_LAST_12_MONTHS"
    if not has_column(t, col):
        return 1.0, "constant column removed from the nursing home mart"
    d = one(f"select count(distinct {col}) from {t}")
    if d > 1:
        return 1.0, f"column now holds {d} values"
    lab = file_says("models/**/*nursing*home*.yml", r"changed_ownership.{0,400}(constant|always 'N'|all 14,7|every row)") or file_says("models/staging/fed_cms_nursing_home/schema.yml", r"changed_ownership.{0,400}(constant|always 'N'|all 14,7|every row)")
    return (0.5 if lab else 0.0), "column is one constant value; label " + ("written" if lab else "missing")


def m5_fake_unique_tests():
    names = ["int_nursing_home_prf_match", "economics__fed_sba_ppp", "environment__fed_epa_frs_facilities",
             "finance__fed_sec_insider_submission", "labor__fed_msha_mines", "procurement__fed_sam_exclusions"]
    ok = [n for n in names if any(re.search(r"KEY RE-PROOF|key_is_real|key_is_unique_within_each_load|dropped `unique`", p.read_text(encoding="utf-8", errors="replace"))
                                  and n in p.read_text(encoding="utf-8", errors="replace") for p in (DBT / "models").rglob("*.yml"))]
    return (1.0 if len(ok) == 6 else 0.0), f"{len(ok)} of 6 models carry the per-load key re-proof"


def m6_junk_public_views():
    out, ok = [], True
    for s, t in (("JUSTICE", "FRAUD_SETTLEMENTS"), ("COMPANIES", "BENEFICIAL_OWNERSHIP_REGISTRY")):
        live = rows(f"select 1 from THE_LIBRARY.information_schema.views where table_schema='{s}' and table_name='{t}'")
        n = one(f"select count(*) from THE_LIBRARY.{s}.{t}") if live else None
        good = (not live) or n > 100
        ok &= good
        out.append(f"{t}: {'gone' if not live else f'{n:,} rows'}")
    return (1.0 if ok else 0.0), "; ".join(out)


def m7_sdwa_grain():
    glob = "models/marts/environment/schema_fed_epa_sdwa_sdwa_violations_enforcement.yml"
    grain = file_says(glob, r"one row\s*=.{0,120}violation|violation.{0,40}enforcement.{0,80}grain")
    tested = file_says(glob, r"unique_combination_of_columns|key_is_real")
    return (1.0 if grain and tested else 0.5 if grain else 0.0), f"grain documented: {grain}; compound key tested: {tested}"


# ---------- the 7 minor ----------

def n1_views_hiding_rows():
    return manual("views_hiding_rows")


def n2_frozen_schema_copy():
    live = rows("select 1 from LIBRARY_STAGING.information_schema.schemata where schema_name='DBT_CROGERS_RIPPLE'")
    return (0.0 if live else 1.0), "DBT_CROGERS_RIPPLE " + ("still live" if live else "gone")


def n3_macro_script_sync_test():
    hit = list(REPO.glob("tests/**/test_staging_cast_sync*.py")) + list(REPO.glob("scripts/tests/**/test_staging_cast_sync*.py"))
    return (1.0 if hit else 0.0), "sync test " + (hit[0].name if hit else "does not exist")


def n4_facility_affiliation_label():
    lab = file_says("models/marts/health/*.yml", r"affiliation.{0,200}under-?report")
    return (1.0 if lab else 0.0), "label " + ("written" if lab else "missing")


def n5_untested_marts():
    mf = DBT / "target" / "manifest.json"
    if not mf.exists():
        return 0.0, "no target/manifest.json; run dbt compile first. Counted open"
    m = json.loads(mf.read_text(encoding="utf-8"))
    nodes = m["nodes"]
    marts = {k for k, v in nodes.items() if v.get("resource_type") == "model" and "/marts/" in v.get("original_file_path", "").replace("\\", "/")
             and v.get("config", {}).get("enabled", True)}
    tested = {d for v in nodes.values() if v.get("resource_type") == "test" for d in v.get("depends_on", {}).get("nodes", [])}
    bare = sorted(marts - tested)
    return (1.0 if not bare else 0.0), f"{len(bare)} of {len(marts)} enabled marts have no test at all"


def n6_id_shaped_column_notes():
    a = file_says("models/marts/health/schema_fed_cms_partd_prescriber*.yml", r"npi.{0,200}(not a row key|not unique|repeats)")
    b = file_says("models/marts/corporate_registry/*.yml", r"company_number.{0,200}(not a row key|not unique|repeats)")
    return (1.0 if a and b else 0.0), f"Part D NPI note: {a}; UK company number note: {b}"


def n7_dead_sam_copy():
    r = rows("select row_count from LIBRARY_RAW.information_schema.tables where table_schema='LANDING' and table_name='FED_SAM_EXCLUSIONS'")
    return (0.0 if r else 1.0), "capped FED_SAM_EXCLUSIONS " + (f"still in landing, {r[0][0]:,} rows" if r else "gone")


# ---------- debt booked after the audit ----------

# the 10 schema files whose not_null tests were moved to warn on 2026-09-20 and 2026-09-21
DOWNGRADED = ["staging/intl_hudoc/schema.yml", "**/schema_fed_dol_form5500.yml", "**/schema_fed_noaa_weather_api.yml",
              "**/schema_fed_usgs_minerals.yml", "**/schema_fed_cms_pos_other.yml", "**/schema_fed_cms_medicare_provider.yml",
              "**/schema_intl_eu_sanctions.yml", "**/schema_fed_nursinghome411.yml", "**/schema_fed_cms_hospice.yml",
              "**/schema_fed_noaa_storm_events.yml"]
WARN_RX = re.compile(r"- not_null:\s*\n\s*config:\s*\n\s*severity:\s*warn")


def d1_warn_only_tests():
    base = DBT / "models"
    here = sum(len(WARN_RX.findall(p.read_text(encoding="utf-8", errors="replace"))) for g in DOWNGRADED for p in base.glob(g))
    everywhere = sum(len(WARN_RX.findall(p.read_text(encoding="utf-8", errors="replace"))) for p in base.rglob("*.yml"))
    return (1.0 if here == 0 else 0.0), f"{here} warn-only not_null tests in the 10 downgraded schema files; {everywhere} project-wide, most older than the audit"


def d2_loader_timestamp():
    return manual("loader_epoch_timestamp")


def d3_shelf_refresh_safe():
    return manual("shelf_refresh_safe")


def d4_rollbacks_runnable():
    return manual("rollback_files_runnable")


def d5_stale_catalog_types():
    """Select-star public views whose catalog types disagree with the mart under them."""
    import collections
    vc, mc = collections.defaultdict(dict), collections.defaultdict(dict)
    for s, t, col, typ in rows("select table_schema, table_name, column_name, data_type from THE_LIBRARY.information_schema.columns"):
        vc[(s, t)][col] = typ
    for s, t, col, typ in rows("select table_schema, table_name, column_name, data_type from LIBRARY_MARTS.information_schema.columns"):
        mc[(s, t)][col] = typ
    stale = []
    for s, t, d in rows("select table_schema, table_name, view_definition from THE_LIBRARY.information_schema.views where table_schema <> 'INFORMATION_SCHEMA'"):
        m = re.search(r"as\s+select\s+\*\s+from\s+LIBRARY_MARTS\.(\w+)\.(\w+)\s*;?\s*$", d or "", re.I)
        if m and any(mc.get((m.group(1).upper(), m.group(2).upper()), {}).get(k, v) != v for k, v in vc[(s, t)].items()):
            stale.append(t)
    return (1.0 if not stale else 0.0), f"{len(stale)} public views with stale catalog types{': ' + ', '.join(stale[:4]) if stale else ''}"


CHECKS = [
    ("S1", "Bare casts in marts", SEVERE, s1_bare_casts),
    ("S2", "Silent rounding and NaN live", SEVERE, s2_rounding),
    ("S3", "FEC memo double-count", SEVERE, s3_fec_memo),
    ("S4", "USASpending 1M-per-year cap", SEVERE, s4_usaspending_cap),
    ("S5", "BJS and HUDOC capped samples", SEVERE, s5_capped_samples),
    ("S6", "Part B floor of 11", SEVERE, s6_partb),
    ("S7", "DME family undercount", SEVERE, s7_dme),
    ("S8", "Public views open", SEVERE, s8_public_shelf),
    ("S9", "ARCOS row key", SEVERE, s9_arcos_key),
    ("M1", "Orphan staging views", MODERATE, m1_orphan_staging_views),
    ("M2", "Staging files with bare casts", MODERATE, m2_staging_outside_sweep),
    ("M3", "Part D vintage", MODERATE, m3_partd_vintage),
    ("M4", "CHOW flag constant", MODERATE, m4_chow_constant),
    ("M5", "Unique tests that cannot fail", MODERATE, m5_fake_unique_tests),
    ("M6", "Junk public views", MODERATE, m6_junk_public_views),
    ("M7", "SDWA violation id grain", MODERATE, m7_sdwa_grain),
    ("N1", "Staging views hiding rows", MINOR, n1_views_hiding_rows),
    ("N2", "Frozen schema copy", MINOR, n2_frozen_schema_copy),
    ("N3", "Macro and script sync test", MINOR, n3_macro_script_sync_test),
    ("N4", "Facility affiliation label", MINOR, n4_facility_affiliation_label),
    ("N5", "Marts with no test", MINOR, n5_untested_marts),
    ("N6", "ID-shaped column notes", MINOR, n6_id_shaped_column_notes),
    ("N7", "Dead capped SAM copy", MINOR, n7_dead_sam_copy),
]
DEBTS = [
    ("D1", "Tests downgraded to warn-only", DEBT, d1_warn_only_tests),
    ("D2", "Loader writes the ingest stamp wrong", DEBT, d2_loader_timestamp),
    ("D3", "Shelf refresh unsafe to run", DEBT, d3_shelf_refresh_safe),
    ("D4", "Rollback files are not runnable undo", DEBT, d4_rollbacks_runnable),
    ("D5", "Stale catalog types on public views", DEBT, d5_stale_catalog_types),
]


def main() -> int:
    global CONN, FAST
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--fast", action="store_true", help="skip the 254-view fetch and the ARCOS key scan (both then count as open)")
    FAST = ap.parse_args().fast
    CONN = db.connect()

    out, score = [], 58.0
    for cid, name, weight, fn in CHECKS + DEBTS:
        try:
            share, why = fn()
        except Exception as exc:  # noqa: BLE001  (a check that cannot run is an open finding, not a crash)
            share, why = 0.0, "CHECK FAILED TO RUN, counted open: " + str(exc).replace("\n", " ")[:140]
        is_debt = cid.startswith("D")
        pts = -weight * (1 - share) if is_debt else weight * share
        score += pts
        state = {1.0: "PASS", 0.0: "OPEN"}.get(share, "HALF" if share == 0.5 else f"{share:.2f}")
        out.append((cid, name, weight, state, round(pts, 2), why))
        print(f"{cid:<3} {state:<5} {pts:+6.2f} of {'-' if is_debt else ''}{weight:<4} {name:<38} {why}")
    CONN.close()

    print(f"\nSCORE {score:.1f} of 100   (58 base, {'fast run' if FAST else 'full run'}, {dt.datetime.now():%Y-%m-%d %H:%M})")
    path = REPO / "reports" / f"warehouse_score_{dt.date.today():%Y-%m-%d}.tsv"
    with path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["id", "finding", "weight", "state", "points", "evidence"])
        w.writerows(out)
        w.writerow(["", "SCORE", "", "", round(score, 1), "fast run" if FAST else "full run"])
    print("written:", path.relative_to(REPO))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
