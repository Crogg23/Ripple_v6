"""Batch-generate dbt mart models for landed sources that don't have one yet.

Rewritten 2026-07-29. The previous version produced models that could not build and a
project that could not parse. Fixed here:

1. Source declarations. It appended every table to the mart-level
   _<domain>__sources.yml without checking whether staging/<source>/schema.yml already
   declared it. Duplicate (source, table) pairs are a FATAL dbt compilation error, and
   this is what left `dbt parse` dead. Now every existing declaration in the project is
   indexed first and a table is only declared if nothing else claims it.
2. Aliases that cannot compile. A column named "1862_land_grant_college" was aliased
   verbatim, but an identifier cannot begin with a digit. Years now move to the end.
3. Reserved-word aliases. "GROUP" was quoted on the source side but aliased bare, which
   is a syntax error. Reserved aliases now get a _col suffix.
4. Duplicate output names. The old code had a comment about avoiding duplicate snake
   aliases but never did it, so two source columns could collide into one output name.
   Names are now de-duplicated with a numeric suffix.
5. Auth. It read SNOWFLAKE_PAT / SNOWFLAKE_PASSWORD, neither of which exists on this
   machine. It now uses the shared key-pair connection.
6. Cost. A straight passthrough of a 100M-row table as a physical table pays twice for
   the same bytes, so anything above VIEW_ROW_THRESHOLD is materialized as a view.

Usage:
    python scripts/gen_mart_models.py            # dry run, prints the plan
    python scripts/gen_mart_models.py --apply
"""
import argparse
import glob
import os
import re
import sys

import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _snowflake_conn as sc  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS = os.path.join(REPO, "library-onboarding", "ripple_dbt", "models")
MARTS = os.path.join(MODELS, "marts")

# A passthrough this big is not worth a second physical copy.
VIEW_ROW_THRESHOLD = 15_000_000

EXCLUDE_COLS = {"_INGESTED_AT", "_SOURCE_RUN_ID", "_SRC_SHA256",
                "INGESTED_AT", "SOURCE_RUN_ID", "SRC_SHA256"}

DOMAIN_MAP = {
    "health_medicine": "health", "money_in_politics": "finance",
    "money_finance": "finance", "corporate_entities": "economics",
    "spending_budget": "economics", "economy_labor_trade": "economics",
    "government_power": "politics", "elections_voting": "politics",
    "justice_courts": "justice", "crime_security": "justice",
    "sanctions_enforcement": "justice", "energy_environment": "environment",
    "transport_movement": "transport", "housing_social": "housing",
    "immigration_migration": "immigration", "history_culture": "history",
    "science_research": "science", "geo_demographics": "reference",
    "open_data_portal": "open_data", "targeted_investigation": "investigations",
    "procurement_intl": "procurement", "education": "education",
    None: "uncategorized", "None": "uncategorized", "UNCLASSIFIED": "uncategorized",
}

# Fallback when DOMAIN_PRIMARY is null/UNCLASSIFIED, which is true for a lot of the
# bulk-loaded sources. Without this, big obvious datasets (SEC 13F holdings,
# CourtListener dockets, FDA FAERS) get dumped in 'uncategorized', which is how the
# UNCATEGORIZED schema filled up with things that clearly belong elsewhere.
# First match on the source_id wins, so order matters.
ID_HINTS = [
    ("courtlistener", "justice"), ("uscourts", "justice"), ("scdb", "justice"),
    ("fjc", "justice"), ("eoir", "immigration"), ("uscis", "immigration"),
    ("cbp_", "immigration"), ("ice_", "immigration"), ("dhs_", "immigration"),
    ("fda_", "health"), ("cms_", "health"), ("cdc_", "health"),
    ("hrsa", "health"), ("nih_", "health"), ("hhs_", "health"), ("dea_", "health"),
    ("sec_", "finance"), ("fec_", "finance"), ("fdic", "finance"),
    ("ffiec", "finance"), ("ncua", "finance"), ("cfpb", "finance"),
    ("gleif", "economics"), ("irs_", "economics"), ("usaspending", "economics"),
    ("sba_", "economics"), ("treasury", "economics"), ("pbgc", "economics"),
    ("grants_gov", "economics"), ("fac_", "economics"),
    ("epa_", "environment"), ("noaa", "environment"), ("usgs", "environment"),
    ("osha", "labor"), ("msha", "labor"), ("dol_", "labor"), ("bls_", "labor"),
    ("nhtsa", "transport"), ("faa_", "transport"), ("fra_", "transport"),
    ("dot_", "transport"), ("bts_", "transport"),
    ("hud_", "housing"), ("fhfa", "housing"),
    ("nces", "education"), ("ed_", "education"),
    ("govinfo", "politics"), ("congress", "politics"), ("voteview", "politics"),
    ("medsl", "politics"), ("eac_", "politics"),
    ("wayback", "investigations"), ("epstein", "investigations"),
    ("portal_", "open_data"),
]


_SOURCE_RE = re.compile(r"source\(\s*'[^']+'\s*,\s*'([^']+)'\s*\)")
_REF_RE = re.compile(r"ref\(\s*'([^']+)'\s*\)")


def _resolve_landing_source(sql_path):
    """The actual LANDING table a mart .sql ultimately reads, resolved through one
    ref() hop into staging if needed. Returns None if it can't be determined.
    """
    try:
        text = open(sql_path, encoding="utf-8", errors="ignore").read()
    except OSError:
        return None
    m = _SOURCE_RE.search(text)
    if m:
        return m.group(1).upper()
    m = _REF_RE.search(text)
    if m:
        hits = glob.glob(os.path.join(MODELS, "staging", "**", m.group(1) + ".sql"),
                          recursive=True)
        if hits:
            stext = open(hits[0], encoding="utf-8", errors="ignore").read()
            m2 = _SOURCE_RE.search(stext)
            if m2:
                return m2.group(1).upper()
    return None


def existing_marts_by_source():
    """{landing_table_upper: 'folder/model.sql'} for EVERY mart already in the project.

    THE BUG THIS FIXES (found 2026-07-31, in two stages).

    Stage 1: the only duplicate guard was `os.path.exists(target)`, checking just the
    SAME domain folder the new mart was about to write into. A hand-built mart in a
    DIFFERENT domain was invisible to it, so this script published a raw passthrough
    twin. First fix: index every mart by its `__<name>` filename suffix instead of by
    path, so a same-named mart anywhere in the project is recognised.

    Stage 2 (the same day, found while auditing further): filename suffix is not
    source identity. `health__fed_dea_arcos` and `uncategorized__fed_dea_arcos_full`
    read the exact same landing table (FED_DEA_ARCOS_FULL) but have different name
    suffixes ('fed_dea_arcos' vs 'fed_dea_arcos_full'), so the Stage-1 fix STILL
    missed them -- along with 20 other pairs, one of which (CMS Part D prescribers)
    was silently discarding real claims and cost data via a stale dedupe key exposed
    by the duplicate. Filenames drift from the tables they read; the source()/ref()
    the SQL actually compiles against does not. This resolves through to the real
    LANDING table (one ref() hop into staging, matching how dbt itself resolves
    lineage) and keys on THAT.
    """
    out = {}
    for path in glob.glob(os.path.join(MARTS, "*", "*.sql")):
        src = _resolve_landing_source(path)
        if src:
            out.setdefault(src, os.path.relpath(path, MARTS).replace("\\", "/"))
    return out


def domain_folder(source_id, domain):
    folder = DOMAIN_MAP.get(domain, "uncategorized")
    if folder != "uncategorized":
        return folder
    sid = source_id.lower()
    for hint, target in ID_HINTS:
        if hint in sid:
            return target
    return "uncategorized"

RESERVED = {
    "GROUP", "ORDER", "SELECT", "FROM", "WHERE", "TABLE", "INDEX", "CREATE", "DROP",
    "ALTER", "CONNECT", "GRANT", "REVOKE", "DATE", "TIME", "YEAR", "MONTH", "DAY",
    "HOUR", "MINUTE", "SECOND", "VALUE", "VALUES", "KEY", "PRIMARY", "FOREIGN",
    "UNIQUE", "CHECK", "DEFAULT", "NULL", "NOT", "AND", "OR", "IN", "IS", "LIKE",
    "BETWEEN", "EXISTS", "CASE", "WHEN", "THEN", "ELSE", "END", "AS", "ON", "JOIN",
    "LEFT", "RIGHT", "FULL", "INNER", "OUTER", "CROSS", "NATURAL", "UNION", "ALL",
    "ANY", "SOME", "TRUE", "FALSE", "COMMENT", "COLUMN", "ROWS", "RANK", "PARTITION",
    "OVER", "WINDOW", "LIMIT", "OFFSET", "HAVING", "SET", "UPDATE", "DELETE",
    "INSERT", "INTO", "MERGE", "USING", "MATCHED", "LOCALTIME", "LOCALTIMESTAMP",
    "CURRENT_DATE", "CURRENT_TIME", "CURRENT_TIMESTAMP", "CURRENT_USER", "QUALIFY",
    "ASC", "DESC", "DISTINCT", "BY", "WITH", "SAMPLE", "TABLESAMPLE", "ILIKE", "RLIKE",
}


def index_declared_sources():
    """Every (source, table) already declared anywhere, so we never duplicate one."""
    declared = {}
    for path in glob.glob(os.path.join(MODELS, "**", "*.yml"), recursive=True):
        try:
            with open(path, encoding="utf-8") as fh:
                doc = yaml.safe_load(fh)
        except Exception:
            continue
        if not isinstance(doc, dict):
            continue
        for src in doc.get("sources") or []:
            for tbl in src.get("tables") or []:
                declared[(src.get("name"), tbl.get("name"))] = os.path.relpath(
                    path, MODELS)
    return declared


def snake_case(name):
    name = name.replace(".", "_")
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    name = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", name)
    name = re.sub(r"[^A-Za-z0-9]", "_", name)
    return re.sub(r"_+", "_", name).strip("_").lower()


def safe_alias(col_name, taken):
    """A legal, unique, non-reserved output name."""
    name = snake_case(col_name) or "col"
    # An identifier cannot start with a digit: 1862_land_grant -> land_grant_1862
    m = re.match(r"^(\d+)_?(.*)$", name)
    if m:
        name = f"{m.group(2)}_{m.group(1)}" if m.group(2) else f"col_{m.group(1)}"
    if name.upper() in RESERVED:
        name = f"{name}_col"
    base, i = name, 2
    while name in taken:
        name = f"{base}_{i}"
        i += 1
    taken.add(name)
    return name


def needs_quoting(col_name):
    if col_name.upper() in RESERVED:
        return True
    if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", col_name):
        return True
    return col_name != col_name.upper()


def infer_cast(col_name, data_type=None):
    """Pick a cast from the column name -- but only for text columns.

    Casting an already-typed column is a hard error, not a no-op: TRY_TO_DOUBLE on a
    NUMBER raises "TRY_CAST cannot be used with arguments of types NUMBER and FLOAT",
    and TRY_TO_DATE on a DATE raises "invalid type for parameter 'TO_DATE'". Two models
    died this way (fed_fac_single_audit, fed_osha_ita_case_detail_2024) before this
    guard existed.
    """
    if data_type is not None and not str(data_type).upper().startswith(
            ("TEXT", "VARCHAR", "STRING", "CHAR")):
        return None
    u = col_name.upper()
    if any(x in u for x in ("_DATE", "DATE_", "CREATED", "UPDATED", "EXPIR")):
        return "try_to_timestamp" if ("TIME" in u or "DATETIME" in u) else "try_to_date"
    if any(x in u for x in ("AMOUNT", "AMT", "COST", "PRICE", "DOLLARS", "PROCEEDS",
                            "OBLIGATION", "DISBURSEMENT")):
        return "try_to_double"
    if any(x in u for x in ("COUNT", "CNT", "NUM_", "NUMBER_OF", "QUANTITY",
                            "DEATHS", "INJURED")):
        return "try_to_number"
    if any(x in u for x in ("_PCT", "PERCENT", "RATIO", "_RATE", "LATITUDE",
                            "LONGITUDE")):
        return "try_to_double"
    if u in ("YEAR", "FISCAL_YEAR", "FY", "CONGRESS"):
        return "try_to_number"
    return None


def build_model_sql(table, columns, schema_folder, source_name, rows):
    """columns is a list of (name, data_type) pairs."""
    cols = [(c, t) for c, t in columns if c.upper() not in EXCLUDE_COLS]
    if not cols:
        return None
    materialized = "view" if (rows or 0) > VIEW_ROW_THRESHOLD else "table"
    label = (source_name or table).encode("ascii", "replace").decode("ascii")

    head = [
        f"{{{{ config(materialized='{materialized}', schema='{schema_folder.upper()}') }}}}",
        "",
        f"-- Source: {label} ({rows or '?'} rows)",
        "-- Generated by scripts/gen_mart_models.py",
    ]
    if materialized == "view":
        head += [
            "--",
            f"-- Materialized as a VIEW: this is a straight passthrough of a "
            f"{(rows or 0):,}-row",
            "-- landing table, so a physical copy would pay twice for the same bytes"
            " without",
            "-- precomputing any join, filter, or aggregation.",
        ]
    head += ["", "with source as (",
             f"    select * from {{{{ source('ripple_raw', '{table}') }}}}",
             ")", "", "select"]

    taken, lines = set(), []
    for col, dtype in cols:
        alias = safe_alias(col, taken)
        ref = f'"{col}"' if needs_quoting(col) else col
        cast = infer_cast(col, dtype)
        if cast:
            lines.append(f"    {cast}({ref}) as {alias}")
        elif ref.strip('"') != alias:
            lines.append(f"    {ref} as {alias}")
        else:
            lines.append(f"    {ref}")
    return "\n".join(head) + "\n" + ",\n".join(lines) + "\nfrom source\n"


def write_source_decl(schema_folder, table, declared, apply):
    """Declare the table only if nothing in the project already declares it."""
    if ("ripple_raw", table) in declared:
        return False
    path = os.path.join(MARTS, schema_folder, f"_{schema_folder}__sources.yml")
    if apply:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if os.path.exists(path):
            with open(path, encoding="utf-8") as fh:
                body = fh.read().rstrip("\n")
            body += f"\n      - name: {table}\n"
        else:
            body = ("version: 2\n\nsources:\n  - name: ripple_raw\n"
                    "    database: LIBRARY_RAW\n    schema: LANDING\n    tables:\n"
                    f"      - name: {table}\n")
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(body)
    declared[("ripple_raw", table)] = os.path.relpath(path, MODELS)
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--limit", type=int)
    args = ap.parse_args()

    declared = index_declared_sources()
    print(f"{len(declared)} source tables already declared in the project")

    conn = sc.connect()
    cur = conn.cursor()
    cur.execute("""
        select SOURCE_ID, NAME, DOMAIN_PRIMARY, LANDED_ROW_COUNT
        from LIBRARY_META.REGISTRY.CATALOG
        where LIFECYCLE in ('landed','stale')
          and _REAL_MART = FALSE
          and coalesce(LANDED_ROW_COUNT, 0) > 0
        order by LANDED_ROW_COUNT desc
    """)
    todo = cur.fetchall()
    if args.limit:
        todo = todo[:args.limit]
    print(f"{len(todo)} landed sources without a real mart\n")

    made = skipped = noview = 0
    views = []
    # Index EVERY existing mart by source before generating anything, so a mart that
    # already exists under a DIFFERENT domain folder is still recognised as a duplicate.
    already = existing_marts_by_source()
    print(f"{len(already)} source(s) already have a mart somewhere in the project")
    for source_id, name, domain, rows in todo:
        table = source_id.upper()
        folder = domain_folder(source_id, domain)
        model = f"{folder}__{source_id.lower()}"
        target = os.path.join(MARTS, folder, f"{model}.sql")
        if os.path.exists(target):
            skipped += 1
            continue
        prior = already.get(source_id.upper())
        if prior:
            # Cross-domain duplicate: this source is already modeled elsewhere. Say so
            # rather than silently skipping -- a hand-built mart under another domain is
            # exactly the case that used to slip through and publish a raw twin.
            print(f"  SKIP {source_id}: already modeled at {prior} "
                  f"(would have written a duplicate at {folder}/{model}.sql)")
            skipped += 1
            continue
        cols = sc.columns_of(table, conn=conn, with_types=True)
        if not cols:
            skipped += 1
            continue
        sql = build_model_sql(table, cols, folder, name, rows)
        if sql is None:
            skipped += 1
            continue
        if (rows or 0) > VIEW_ROW_THRESHOLD:
            views.append((model, rows))
        if args.apply:
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with open(target, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(sql)
        write_source_decl(folder, table, declared, args.apply)
        made += 1
    conn.close()

    print(f"models to generate: {made}   skipped (exists / no columns): {skipped}")
    if views:
        print(f"\nmaterialized as VIEWS (> {VIEW_ROW_THRESHOLD:,} rows):")
        for mname, rows in views:
            print(f"   {rows:>12,}  {mname}")
    if not args.apply:
        print("\nDRY RUN -- rerun with --apply to write files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
