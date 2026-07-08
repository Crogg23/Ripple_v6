#!/usr/bin/env python3
"""Auto-generate evidence.dev pages from the card catalog (THE_LIBRARY.PUBLIC.START_HERE).

Turns the 232-dataset reading room into a browsable Evidence site instead of 232 unused
views. For every dataset in START_HERE it emits:

  evidence/sources/library/<src>.sql   -- the data the page reads
      <=100k rows :  select * from <BROWSE_AT>                       (parquet-safe as-is)
      >100k  rows :  a bounded GROUP BY (year / category, LIMITed)   (parquet-safe by construction)
  evidence/pages/<slug>.md             -- title + BigValue(row_count) + DataTable
      + a LineChart/BarChart ONLY when a CONFIDENT typed date(+numeric) pair is detected in the
        view's real columns (INFORMATION_SCHEMA). Raw all-TEXT views get DataTable + BigValue only
        -- we never guess-parse a text date (the 8-digit MMDDYYYY epoch footgun).
  evidence/pages/index.md              -- a generated "Browse all shelves" block spliced in between
        <!-- BEGIN GENERATED BROWSE -->/<!-- END GENERATED BROWSE --> markers (idempotent; the
        hand-written intro above the markers is never touched).

GATING (must hold before you --apply this into the live site):
  * Run AFTER the typed-view layer lands, so pages don't template un-typed/broken views.
  * Run AFTER the giant pre-agg marts land, so a raw page never points at an 84M-row view.
  This generator is SAFE regardless (giants are pre-aggregated here), but chart quality tracks
  how typed the underlying views are.

This writes FILES, not warehouse objects -- so there is no DDL, no grants concern (D04 N/A).
  "preview" = print the plan (page count, <=100k vs >100k split, chart count) + write 3 sample
              pages/sources to the scratchpad so Chris can eyeball quality. NOTHING under evidence/.
  "--apply" = write every page/source into evidence/ + splice the browse block into index.md.

    python3 scripts/gen_evidence_pages.py            # PREVIEW (no writes under evidence/)
    python3 scripts/gen_evidence_pages.py --apply     # write the pages + sources + index block

Idempotent + re-runnable: --apply overwrites generated files in place and re-splices the same
index block between its markers. Hand-authored pages/sources are on a reserve list and never
clobbered; the datasets behind them are skipped so we don't emit a competing auto-page.
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
SCRATCH = Path("/private/tmp/claude-501/-Users-chrisr--Documents-GitHub-Ripple-v6/"
               "b35255f7-a351-4641-a12f-d605c501c1f2/scratchpad")

PAGES_DIR = REPO / "evidence" / "pages"
SRC_DIR = REPO / "evidence" / "sources" / "library"
INDEX = PAGES_DIR / "index.md"
BEGIN = "<!-- BEGIN GENERATED BROWSE -->"
END = "<!-- END GENERATED BROWSE -->"

BIG_ROWS = 100_000
DATE_TYPES = {"DATE", "TIMESTAMP_NTZ", "TIMESTAMP_LTZ", "TIMESTAMP_TZ"}
NUM_TYPES = {"NUMBER", "FLOAT"}

# Hand-authored pages/sources -- never clobber, and skip their datasets so we don't
# emit a competing auto-page. (Keyed by BROWSE_AT so it survives a friendly-name rename.)
RESERVED_PAGE_SLUGS = {"index", "national-debt", "banned-providers", "fatal-force",
                       "foreign-agents", "gun-checks", "scotus"}
RESERVED_SRC = {"national_debt", "banned_providers", "fatal_force", "foreign_agents",
                "gun_checks", "scotus_by_term", "catalog"}
SKIP_BROWSE_AT = {
    "THE_LIBRARY.ECONOMY.NATIONAL_DEBT_DAILY",
    "THE_LIBRARY.HEALTH.BANNED_HEALTHCARE_PROVIDERS",
    "THE_LIBRARY.CRIME_SECURITY.POLICE_FATAL_SHOOTINGS",
    "THE_LIBRARY.INVESTIGATIONS.FOREIGN_AGENTS",
    "THE_LIBRARY.CRIME_SECURITY.GUN_BACKGROUND_CHECKS",
    "THE_LIBRARY.JUSTICE.SCOTUS_CASES_AND_VOTES",
}

# Names that make a bounded GROUP BY meaningful on a giant (kept SMALL by nature or by LIMIT).
YEAR_RE = re.compile(r".*(YEAR|PROGRAM_YEAR|FISCAL_YEAR|CYCLE|TERM|FY)$")
CAT_NAMES = {"STATE", "STATE_CODE", "STATE_ABBR", "STATE_NAME", "ST", "COUNTRY",
             "COUNTRY_CODE", "CATEGORY", "TYPE", "STATUS", "SECTOR", "PARTY",
             "AGENCY", "ENTITY_TP", "TRANSACTION_TP", "PROVIDER_TYPE", "CLASS"}
# Numeric columns that are codes/ids, not measures -- presence must NOT trigger a chart.
NUM_BLOCK_RE = re.compile(r".*(ZIP|FIPS|NPI|EIN|CIK|UEI|LEI|_ID|ID$|CODE|LAT|LON|"
                          r"LATITUDE|LONGITUDE|PHONE|YEAR)$")
# Metadata / pipeline columns that are date-typed but NOT the data's real timeline
# (every raw landing view carries _INGESTED_AT TIMESTAMP_NTZ -- charting it is garbage).
META_COL_RE = re.compile(r"^_|.*(INGEST|LOADED|_LOAD|SCRAPED|HARVEST|_RUN_ID|SHA256|EXTRACTED).*")


def qi(name: str) -> str:
    """Quote an identifier so keyword/odd column names (e.g. DATE) are safe in Snowflake + DuckDB."""
    return '"' + name.replace('"', '""') + '"'


def slugify(name: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", (name or "").lower()).strip("-")
    return s or "dataset"


def title_of(dataset: str) -> str:
    return " ".join(w.capitalize() for w in dataset.replace("_", " ").split())


def fetch(conn):
    from connect import db
    sh = db.dicts(conn, "SELECT SHELF,DATASET,WHAT_IT_IS,ROW_COUNT,STATUS,SOURCE_ID,"
                        "BROWSE_AT,REAL_TABLE FROM THE_LIBRARY.PUBLIC.START_HERE "
                        "ORDER BY SHELF, DATASET")
    cols = db.dicts(conn, "SELECT TABLE_SCHEMA,TABLE_NAME,COLUMN_NAME,DATA_TYPE,ORDINAL_POSITION "
                          "FROM THE_LIBRARY.INFORMATION_SCHEMA.COLUMNS "
                          "WHERE TABLE_SCHEMA NOT IN ('INFORMATION_SCHEMA','PUBLIC') "
                          "ORDER BY TABLE_SCHEMA,TABLE_NAME,ORDINAL_POSITION")
    by = defaultdict(list)
    for c in cols:
        by[(c["TABLE_SCHEMA"], c["TABLE_NAME"])].append((c["COLUMN_NAME"], c["DATA_TYPE"]))
    return sh, by


def cols_for(browse_at: str, by) -> list[tuple[str, str]]:
    p = browse_at.split(".")
    return by.get((p[1], p[2]), []) if len(p) == 3 else []


def pick(cols, pred):
    for name, dt in cols:
        if pred(name, dt):
            return name
    return None


def plan_dataset(r, cols):
    """Return the plan for one dataset: slug/src/title + source_sql + page_md."""
    ds, shelf, what = r["DATASET"], r["SHELF"], (r["WHAT_IT_IS"] or "")
    n, status, browse = int(r["ROW_COUNT"]), r["STATUS"], r["BROWSE_AT"]
    title = title_of(ds)
    date_col = pick(cols, lambda nm, dt: dt in DATE_TYPES and not META_COL_RE.match(nm))
    num_col = pick(cols, lambda nm, dt: dt in NUM_TYPES and not NUM_BLOCK_RE.match(nm)
                   and not META_COL_RE.match(nm))
    giant = n > BIG_ROWS
    chart = None  # ('line'|'bar', details)

    if not giant:
        src_sql = (f"-- {what}\n-- Auto-generated by scripts/gen_evidence_pages.py from "
                   f"THE_LIBRARY.PUBLIC.START_HERE (<=100k rows -> full copy is parquet-safe).\n"
                   f"select * from {browse}\n")
        # Confident chart: a typed date AND a real numeric measure -> count-over-time line.
        if date_col and num_col:
            chart = ("line", date_col)
    else:
        # >100k: pre-aggregate so the source is parquet-safe BY CONSTRUCTION.
        year_named = pick(cols, lambda nm, dt: bool(YEAR_RE.match(nm)))
        cat = pick(cols, lambda nm, dt: nm in CAT_NAMES)
        head = (f"-- {what}\n-- Auto-generated by scripts/gen_evidence_pages.py: {n:,} rows > 100k, "
                f"so this is a BOUNDED pre-aggregate (parquet-safe by construction), not select *.\n")
        if date_col:
            src_sql = (head + f"select year({qi(date_col)}) as year, count(*) as records\n"
                       f"from {browse}\nwhere {qi(date_col)} is not null\ngroup by 1\norder by 1\n")
            chart = ("bar", "year")
        elif year_named:
            src_sql = (head + f"-- grouped on year-like text/number column {year_named} "
                       f"(NOT date-cast -- avoids the 8-digit epoch trap); LIMIT bounds it.\n"
                       f"select {qi(year_named)} as year, count(*) as records\n"
                       f"from {browse}\ngroup by 1\norder by 1\nlimit 1000\n")
            chart = ("bar", "year")
        elif cat:
            src_sql = (head + f"-- top categories by {cat}; LIMIT keeps the parquet bounded.\n"
                       f"select {qi(cat)} as category, count(*) as records\n"
                       f"from {browse}\ngroup by 1\norder by 2 desc\nlimit 200\n")
            chart = ("bar", "category")
        else:
            # No safe grouping column -> a single-row count. No chart.
            src_sql = (head + f"-- no typed date or known category column; single-row count only.\n"
                       f"select count(*) as row_count from {browse}\n")
    return {"dataset": ds, "shelf": shelf, "what": what, "rows": n, "status": status,
            "browse": browse, "title": title, "giant": giant, "chart": chart,
            "src_sql": src_sql}


def render_page(p, src) -> str:
    """Build the .md page body. `src` is the evidence source name (library.<src>)."""
    L = [f"---\ntitle: {p['title']}\n---\n"]
    prose = p["what"] or f"{p['title']} -- from the Ripple Library reading room."
    if not p["giant"]:
        L.append(f"```sql rows\nselect * from library.{src}\n```\n")
        L.append(f"```sql n\nselect count(*) as row_count from library.{src}\n```\n")
        if p["chart"]:
            _, dcol = p["chart"]
            L.append(f"```sql trend\nselect date_trunc('month', {qi(dcol)}) as period, "
                     f"count(*) as records\nfrom library.{src}\nwhere {qi(dcol)} is not null\n"
                     f"group by 1\norder by 1\n```\n")
        L.append(f"{prose}\n\nSource: `{p['browse']}` ({p['status']}).\n")
        L.append('<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />\n')
        if p["chart"]:
            L.append(f'<LineChart\n    data={{trend}}\n    x=period\n    y=records\n'
                     f'    title="{p["title"]} over time (records per month)"\n/>\n')
        L.append('<DataTable data={rows} search=true rows=20 />\n')
    else:
        # Giant: literal row_count (no 84M scan) + the bounded aggregate.
        L.append(f"```sql n\nselect {p['rows']} as row_count\n```\n")
        L.append(f"{prose}\n\nSource: `{p['browse']}` ({p['status']}, {p['rows']:,} rows). "
                 f"This page reads a bounded pre-aggregate of that view, not every row.\n")
        L.append('<BigValue data={n} value=row_count title="Rows in the full source" fmt="#,##0" />\n')
        if p["chart"]:
            kind, key = p["chart"]
            L.append(f"```sql agg\nselect * from library.{src}\n```\n")
            xax = "year" if key == "year" else "category"
            swap = "\n    swapXY=true" if key == "category" else ""
            L.append(f'<BarChart\n    data={{agg}}\n    x={xax}\n    y=records{swap}\n'
                     f'    title="{p["title"]} by {xax}"\n    fmt="#,##0"\n/>\n')
            L.append('<DataTable data={agg} rows=25 />\n')
    return "\n".join(L)


def build_index_block(plans) -> str:
    by_shelf = defaultdict(list)
    for p in plans:
        by_shelf[p["shelf"]].append(p)
    out = [BEGIN, "", "## Browse all shelves", "",
           "Every dataset in the reading room, auto-generated from the card catalog.", ""]
    for shelf in sorted(by_shelf):
        out.append(f"### {shelf.replace('_', ' ').title()}")
        out.append("")
        for p in sorted(by_shelf[shelf], key=lambda x: x["dataset"]):
            what = (p["what"][:110] + "...") if len(p["what"]) > 110 else p["what"]
            dash = f" — {what}" if what else ""
            out.append(f"- [{title_of(p['dataset'])}](/{p['slug']}){dash}")
        out.append("")
    out.append(END)
    return "\n".join(out)


def splice_index(block: str) -> str:
    text = INDEX.read_text(encoding="utf-8") if INDEX.exists() else "---\ntitle: The Library\n---\n"
    if BEGIN in text and END in text:
        pre = text[: text.index(BEGIN)]
        post = text[text.index(END) + len(END):]
        return pre.rstrip() + "\n\n" + block + "\n" + post.lstrip("\n")
    return text.rstrip() + "\n\n" + block + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate evidence.dev pages from START_HERE.")
    ap.add_argument("--apply", action="store_true",
                    help="write into evidence/ (default: preview + samples to scratchpad)")
    args = ap.parse_args()

    from connect import db
    conn = db.connect()
    try:
        sh, by = fetch(conn)
    finally:
        conn.close()

    plans, skipped = [], 0
    seen_slug, seen_src = set(RESERVED_PAGE_SLUGS), set(RESERVED_SRC)
    for r in sh:
        if r["BROWSE_AT"] in SKIP_BROWSE_AT:
            skipped += 1
            continue
        p = plan_dataset(r, cols_for(r["BROWSE_AT"], by))
        slug = slugify(p["dataset"])
        src = slug.replace("-", "_")
        if slug in seen_slug or src in seen_src:  # de-collide with source_id stem
            stem = slugify(r["SOURCE_ID"] or r["BROWSE_AT"].split(".")[-1])
            slug = f"{slug}-{stem}"
            src = slug.replace("-", "_")
        seen_slug.add(slug)
        seen_src.add(src)
        p["slug"], p["src"] = slug, src
        plans.append(p)

    smalls = [p for p in plans if not p["giant"]]
    giants = [p for p in plans if p["giant"]]
    charts = [p for p in plans if p["chart"]]
    line = [p for p in charts if p["chart"][0] == "line"]
    bar = [p for p in charts if p["chart"][0] == "bar"]
    gcount_only = [p for p in giants if not p["chart"]]

    mode = "APPLY" if args.apply else "PREVIEW"
    print(f"[{mode}] gen_evidence_pages -- {len(sh)} datasets in START_HERE")
    print(f"   skipped (hand-authored, reserved): {skipped}")
    print(f"   pages to emit:                     {len(plans)}")
    print(f"     <=100k (select *):               {len(smalls)}")
    print(f"     >100k  (bounded pre-agg):        {len(giants)}"
          f"  ({len(gcount_only)} count-only, no safe group col)")
    print(f"   charts (confident typed pair):     {len(charts)}"
          f"   [line: {len(line)}  bar: {len(bar)}]")
    print(f"   text-only (DataTable + BigValue):  {len(plans) - len(charts)}")

    if not args.apply:
        # Pick 3 representative samples: chartable small (most rows), largest giant, text-only small.
        SCRATCH.mkdir(parents=True, exist_ok=True)
        small_typed = sorted([p for p in smalls if p["chart"]], key=lambda x: -x["rows"])
        big = sorted(giants, key=lambda x: -x["rows"])
        text_only = sorted([p for p in smalls if not p["chart"]], key=lambda x: -x["rows"])
        samples, seen = [], set()
        for grp in (small_typed, big, text_only):
            if grp and grp[0]["slug"] not in seen:
                samples.append(grp[0])
                seen.add(grp[0]["slug"])
        print(f"\n   writing {len(samples)} sample page/source pairs -> {SCRATCH}")
        for p in samples:
            md = render_page(p, p["src"])
            (SCRATCH / f"sample_{p['slug']}.md").write_text(md, encoding="utf-8")
            (SCRATCH / f"sample_{p['src']}.sql").write_text(p["src_sql"], encoding="utf-8")
            kind = p["chart"][0] if p["chart"] else "no-chart"
            print(f"     - {p['slug']:<40} {p['rows']:>12,} rows  {p['status']:<8} {kind}")
        # also dump the full plan manifest so Chris can scan every page before --apply
        man = SCRATCH / "gen_evidence_plan.tsv"
        with man.open("w", encoding="utf-8") as f:
            f.write("slug\tshelf\trows\tstatus\tgiant\tchart\tbrowse_at\n")
            for p in sorted(plans, key=lambda x: (x["shelf"], x["dataset"])):
                ck = p["chart"][0] if p["chart"] else ""
                f.write(f"{p['slug']}\t{p['shelf']}\t{p['rows']}\t{p['status']}\t"
                        f"{int(p['giant'])}\t{ck}\t{p['browse']}\n")
        idx_preview = SCRATCH / "gen_evidence_index_block.md"
        idx_preview.write_text(build_index_block(plans), encoding="utf-8")
        print(f"   full plan manifest -> {man}")
        print(f"   index browse block preview -> {idx_preview}")
        print("\n   PREVIEW only -- nothing written under evidence/. Re-run with --apply.")
        return 0

    # --- APPLY: write every page + source, then splice the index block ---
    PAGES_DIR.mkdir(parents=True, exist_ok=True)
    SRC_DIR.mkdir(parents=True, exist_ok=True)
    for p in plans:
        (SRC_DIR / f"{p['src']}.sql").write_text(p["src_sql"], encoding="utf-8")
        (PAGES_DIR / f"{p['slug']}.md").write_text(render_page(p, p["src"]), encoding="utf-8")
    INDEX.write_text(splice_index(build_index_block(plans)), encoding="utf-8")
    print(f"\n   wrote {len(plans)} pages -> {PAGES_DIR}")
    print(f"   wrote {len(plans)} sources -> {SRC_DIR}")
    print(f"   spliced browse block into {INDEX}")
    print("   DONE.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
