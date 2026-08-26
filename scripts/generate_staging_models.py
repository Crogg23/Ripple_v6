#!/usr/bin/env python3
"""Deterministic staging-model generator -- the actual build, not the LLM one.

Reads GRAIN / NATURAL_KEY / SPINE_ENTITY off SOURCE_REGISTRY (populated by
scripts/profile_spine_backfill.py) plus each source's ACTUAL landed columns, and
emits a draft dbt staging model per source. Plain Python string templating --
NO model calls, ever. This is deliberately a different tool from
library-onboarding/scaffold_dbt.py (the interactive Checkpoint-4 generator,
which DOES call Claude, one source at a time, during onboarding) -- Chris's
non-negotiable principle for THIS generator is zero AI in the running system;
anywhere a source needs real judgment, profile_spine_backfill.py already left
it NULL and out of scope here.

Conventions this generator standardizes (existing hand-written staging models
are split ~50/50 on some of these -- see outputs/ Step-0 report; this is the
new house style going forward, not a retrofit of the old 55):

  - dedupe:     QUALIFY ROW_NUMBER() OVER (PARTITION BY <natural_key> ORDER BY
                _INGESTED_AT DESC) = 1   (one idiom, not two)
  - audit cols: _loaded_at (renamed from landing's _INGESTED_AT), _source_url
                (a literal constant from SOURCE_REGISTRY.URL -- Chris's spec,
                intentionally NOT the landing _SOURCE_RUN_ID/_SRC_SHA256 names)
  - casting:    snake_case rename only. NO type casts -- inferring a column's
                real type needs semantic knowledge this generator doesn't have.
                Every generated file says so in its header; finishing the casts
                by hand (or via a follow-up pass) is expected, not a bug.
  - spine join: when spine_entity is one connect/'s spine already resolves
                (provider/facility/vessel/person/organization), emit a computed
                SPINE_ENTITY_ID column using the EXACT formula
                connect/incremental.py's _entity_id_sql uses:
                    'ENT_' || LEFT(MD5(<KEY_TYPE> || '|' || normalize_sql(key,col)), 16)
                so a row that resolves here is guaranteed to also match
                LIBRARY_META."CONNECT".ENTITY_GOLDEN.ENTITY_ID with ZERO extra
                transformation downstream. Other spine_entity values (place,
                case, asset, event, payment, filing, aircraft) get NO such
                column -- connect/ has no resolver for them yet (documented in
                connect/spine_entity.py); the header comment says so per-model.

Scope: every SOURCE_ID with GRAIN IS NOT NULL (i.e. every source
profile_spine_backfill.py resolved HIGH or MEDIUM confidence). Sources still
NULL there are genuinely out of scope until a human resolves them -- this
script does not guess.

    python3 scripts/generate_staging_models.py                 # write all resolved sources
    python3 scripts/generate_staging_models.py --limit 10       # first 10 (validation)
    python3 scripts/generate_staging_models.py --source-id fed_cms_dialysis   # one source
    python3 scripts/generate_staging_models.py --dry-run         # print, write nothing

Writes .sql files into DBT_PROJECT_PATH/models/staging/<source_id>/ -- normal
git-tracked source code, not a Snowflake mutation, so (unlike the registry
scripts) this one is safe for the agent to run directly; materializing the
views is a separate `dbt run` step.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO / "library-onboarding"))
sys.path.insert(0, str(_REPO / "connect"))
try:
    from dotenv import load_dotenv
    load_dotenv(_REPO / "library-onboarding/.env", override=True)
except Exception:  # pragma: no cover
    pass

import snow  # noqa: E402
from config import settings  # noqa: E402
from keys import detect_key, normalize_sql, quote_ident  # noqa: E402

DBT_PROJECT = _REPO / "library-onboarding" / "ripple_dbt"
MODELS_DIR = DBT_PROJECT / "models" / "staging"

# spine_entity values connect/'s ENTITY_MAP already resolves -- only these get a
# SPINE_ENTITY_ID column. Everything else in SPINE_ENTITY_VOCAB is a label only.
JOINABLE_ENTITIES = {"provider", "facility", "vessel", "person", "organization"}

# spine_entity -> plural, for the model's <entity> filename segment. Small closed
# set (connect/spine_entity.py's SPINE_ENTITY_VOCAB) -- hand-mapped, not guessed.
PLURAL = {
    "provider": "providers", "facility": "facilities", "vessel": "vessels",
    "person": "people", "organization": "organizations", "place": "places",
    "payment": "payments", "filing": "filings", "case": "cases",
    "asset": "assets", "event": "events", "aircraft": "aircraft",
}

# The identifying key label (NPI/CCN/EIN/...) for a natural_key column is
# re-derived from the column NAME itself via connect/keys.py's tagger -- the
# same deterministic detection profile_spine_backfill.py used to find it in the
# first place. Re-deriving avoids adding a 4th registry column (Chris's ask was
# exactly grain/natural_key/spine_entity) and can't drift out of sync with the
# tagger the way a stored label could.
def _key_label_for_column(col: str) -> str | None:
    key, _tier = detect_key(col)
    return key


def fetch_sources(cur, source_id: str | None, limit: int | None) -> list[dict]:
    # SPINE_ENTITY may legitimately be NULL (grain/natural_key proven, but no
    # registry hint to say what the row is ABOUT -- e.g. a dataset catalog or
    # vulnerability database keyed by its own record ID). Still stageable;
    # just gets no spine_entity_id join column. Never required here.
    where = "WHERE r.GRAIN IS NOT NULL AND r.NATURAL_KEY IS NOT NULL"
    params: tuple = ()
    if source_id:
        where += " AND r.SOURCE_ID = %s"
        params = (source_id,)
    sql = (
        "SELECT r.SOURCE_ID, r.GRAIN, ARRAY_TO_STRING(r.NATURAL_KEY, ','), "
        "r.SPINE_ENTITY, COALESCE(r.URL, ''), COALESCE(r.NAME, r.SOURCE_ID) "
        f"FROM LIBRARY_META.REGISTRY.SOURCE_REGISTRY r {where} "
        "ORDER BY r.SOURCE_ID"
    )
    cur.execute(sql, params)
    rows = [
        {"source_id": r[0], "grain": r[1],
         "natural_key": [c for c in (r[2] or "").split(",") if c],
         "spine_entity": r[3], "url": r[4], "name": r[5]}
        for r in cur.fetchall()
    ]
    return rows[:limit] if limit else rows


def already_declared_source_tables() -> dict[str, set[str]]:
    """{ripple_raw_table_name: {folders whose *.yml declares it}}. dbt errors
    ("dbt found two sources with the name...") if a table is declared twice --
    e.g. the politics/ folder declares several tables in one shared
    _politics__sources.yml instead of per-source-folder schema.yml, so a
    per-folder existence check alone (checked separately, for hand-built .sql
    files) isn't enough; this catches cross-folder declaration collisions too.

    Returns the DECLARING FOLDERS (not just a flat set) so the caller can tell a
    real cross-folder collision from a source's OWN prior schema.yml -- otherwise
    every already-generated source would falsely skip its own regeneration (e.g.
    a spine_entity rename records->places could never be applied)."""
    import yaml

    declared: dict[str, set[str]] = {}
    for path in DBT_PROJECT.glob("models/**/*.yml"):
        try:
            doc = yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not doc:
            continue
        for src in doc.get("sources") or []:
            if src.get("name") != "ripple_raw":
                continue
            for t in src.get("tables") or []:
                if t.get("name"):
                    declared.setdefault(t["name"], set()).add(str(path.parent))
    return declared


# CLAUDE.md's audit-column convention is _INGESTED_AT/_SOURCE_RUN_ID/_SRC_SHA256
# (leading underscore) -- ~1,607 landing tables (almost all portal_*
# open-data-portal harvests, confirmed live via INFORMATION_SCHEMA) carry the
# SAME three columns WITHOUT the underscore instead. Never business data --
# excluded from "real" columns just like the underscore-prefixed ones, but the
# bare INGESTED_AT is a genuine per-row ingestion timestamp, so it's used for
# _loaded_at in preference to a fabricated CURRENT_TIMESTAMP() fallback.
_AUDIT_COLUMN_NAMES = {"INGESTED_AT", "SOURCE_RUN_ID", "SRC_SHA256"}


def fetch_columns(cur, table_name: str) -> tuple[list[tuple[str, str]], str | None]:
    """(real columns, ingested_at_column). ingested_at_column is '_INGESTED_AT',
    the bare 'INGESTED_AT', or None if neither is present."""
    cur.execute(
        "SELECT column_name, data_type FROM LIBRARY_RAW.INFORMATION_SCHEMA.COLUMNS "
        "WHERE table_schema='LANDING' AND table_name=%s ORDER BY ordinal_position",
        (table_name,),
    )
    rows = cur.fetchall()
    real = [(c, t) for c, t in rows if not c.startswith("_") and c not in _AUDIT_COLUMN_NAMES]
    all_cols = {c for c, _ in rows}
    ingested_at_column = "_INGESTED_AT" if "_INGESTED_AT" in all_cols else (
        "INGESTED_AT" if "INGESTED_AT" in all_cols else None)
    return real, ingested_at_column


def snake(name: str) -> str:
    return name.strip().lower()


def render_model(src: dict, columns: list[tuple[str, str]], ingested_at_column: str | None) -> str:
    sid = src["source_id"]
    landing_table = sid.upper()
    nk_cols = src["natural_key"]
    entity = src["spine_entity"]
    key_label = _key_label_for_column(nk_cols[0]) if len(nk_cols) == 1 else None

    col_lines = ",\n".join(f"        {quote_ident(c)} as {snake(c)}" for c, _ in columns)
    nk_snake = [snake(c) for c in nk_cols]
    partition_by = ", ".join(nk_snake)

    spine_join_col = ""
    spine_join_comment = ""
    if entity in JOINABLE_ENTITIES and key_label and len(nk_cols) == 1:
        raw_col = quote_ident(nk_cols[0])
        norm_expr = normalize_sql(key_label, raw_col)
        spine_join_col = (
            f",\n    'ENT_' || LEFT(MD5('{key_label}' || '|' || ({norm_expr})), 16) "
            f"as spine_entity_id  -- joins LIBRARY_META.\"CONNECT\".ENTITY_GOLDEN.ENTITY_ID"
        )
    elif entity:
        spine_join_comment = (
            f"\n-- spine_entity '{entity}' has no connect/ resolver yet "
            f"(see connect/spine_entity.py) -- no SPINE_ENTITY_ID emitted."
        )
    else:
        spine_join_comment = (
            "\n-- spine_entity not determined (grain/natural_key proven, but no "
            "registry hint says what this row is ABOUT) -- no SPINE_ENTITY_ID emitted."
        )

    if ingested_at_column == "_INGESTED_AT":
        loaded_at_expr = "_INGESTED_AT as _loaded_at"
        order_by_expr = "_loaded_at desc"
        audit_comment = ""
    elif ingested_at_column == "INGESTED_AT":
        # ~1,607 landing tables (almost all portal_* harvests) carry a real
        # per-row ingestion timestamp, just WITHOUT the leading underscore
        # (confirmed via INFORMATION_SCHEMA) -- used here exactly like the
        # underscore-prefixed convention, giving a genuine recency signal
        # instead of a fabricated one.
        loaded_at_expr = "INGESTED_AT as _loaded_at"
        order_by_expr = "_loaded_at desc"
        audit_comment = (
            "\n-- landing table's ingestion timestamp is named INGESTED_AT (no leading "
            "underscore) rather than the usual _INGESTED_AT -- confirmed via "
            "INFORMATION_SCHEMA, not assumed."
        )
    else:
        # No ingestion timestamp at all, in either naming convention (confirmed
        # via INFORMATION_SCHEMA). CURRENT_TIMESTAMP() is the honest fallback
        # (this is when the MODEL ran, not when the row landed). The QUALIFY
        # tiebreaker is moot today: profile_spine_backfill.py already proved
        # count(*) = count(distinct natural_key) on the landing table itself,
        # so there are no ties to break -- ordering by the natural key is just
        # a syntactically valid placeholder, not a real recency signal, in
        # case a future reload ever does introduce a duplicate.
        loaded_at_expr = "CURRENT_TIMESTAMP() as _loaded_at"
        order_by_expr = f"{partition_by}"
        audit_comment = (
            "\n-- landing table has NO ingestion-timestamp column at all (confirmed via "
            "INFORMATION_SCHEMA, not assumed) -- _loaded_at is model-run time, not ingest "
            "time. QUALIFY's ORDER BY has no real recency signal to break ties with; "
            "harmless today since grain is already proven duplicate-free at the landing layer."
        )

    url_escaped = src["url"].replace("'", "''")

    return f"""{{{{ config(tags=['spine_generated']) }}}}

-- GRAIN: {src['grain']}
-- SPINE_ENTITY: {entity or '(not determined)'}  (natural_key: {', '.join(nk_cols)})
-- Generated by scripts/generate_staging_models.py from SOURCE_REGISTRY -- deterministic,
-- no LLM. Casts kept as landed (TEXT) -- add explicit type casts by hand once each
-- column's real type is confirmed; this generator has no semantic type knowledge.{spine_join_comment}{audit_comment}

with source as (

    select * from {{{{ source('ripple_raw', '{landing_table}') }}}}

),

renamed as (

    select
{col_lines},
        {loaded_at_expr},
        '{url_escaped}' as _source_url{spine_join_col}

    from source

)

select * from renamed
qualify row_number() over (partition by {partition_by} order by {order_by_expr}) = 1
"""


def render_schema_yml(model_name: str, src: dict, nk_snake: list[str], landing_table: str,
                       include_source: bool = True) -> str:
    """version-2 schema.yml matching this project's live convention: a per-model-
    folder `sources:` block declaring the ripple_raw table (dbt errors at parse
    time without one -- 'depends on a source ... which was not found') PLUS
    `data_tests:` (not the deprecated bare `tests:` key -- every hand-written
    schema.yml in this project already uses data_tests:, confirmed against
    fed_cms_nursing_home/schema.yml and fed_sec_edgar_company_tickers/schema.yml).

    include_source=False when the raw table is already declared as a dbt source
    in ANOTHER folder (a genuine cross-folder collision, checked by the caller)
    -- dbt errors on a duplicate source declaration, so this folder's schema.yml
    gets ONLY the models: block and relies on the other folder's sources: block.
    2026-08-26: this used to mean skipping the model entirely, which silently
    left 86 sources with a real resolved key but no staging model at all --
    the fix is to still emit the model, just not re-declare the source.

    2026-08-26: also fixed per-column not_null severity on COMPOSITE keys.
    A multi-column natural key's real completeness gate is the combination
    (unique_combination_of_columns below) -- an individual column being null
    on some rows is common and often legitimate (e.g. a wide measure-catalog
    table where most rows only populate a handful of its many optional
    measure-id columns). Hard-erroring on every column individually produced
    111 test failures across 21 draft models the first time this ran, 67 of
    them from one source alone. Single-column keys keep not_null as a real
    error -- a null there means the row has no identity at all.
    """
    desc = f"GRAIN: {src['grain']}. SPINE_ENTITY: {src['spine_entity'] or '(not determined)'}.".replace('"', "'")
    if len(nk_snake) == 1:
        col_blocks = (f"      - name: {nk_snake[0]}\n        data_tests:\n"
                      "          - unique\n          - not_null")
        model_tests = ""
    else:
        col_blocks = "\n".join(
            f"      - name: {c}\n        data_tests:\n"
            "          - not_null:\n"
            "              config:\n"
            "                severity: warn"
            for c in nk_snake
        )
        model_tests = (
            "\n    data_tests:\n      - dbt_utils.unique_combination_of_columns:\n"
            "          arguments:\n            combination_of_columns:\n"
            + "\n".join(f"              - {c}" for c in nk_snake)
        )
    source_block = f"""sources:
  - name: ripple_raw
    database: LIBRARY_RAW
    schema: LANDING
    tables:
      - name: {landing_table}
        description: >
          Raw landing table for {src['name']}. All columns arrive as TEXT and
          are cast in the staging layer.

""" if include_source else ""
    return f"""version: 2

{source_block}models:
  - name: {model_name}
    description: "{desc}"
    columns:
{col_blocks}{model_tests}
"""


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate draft dbt staging models from SOURCE_REGISTRY.")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--source-id", default=None)
    ap.add_argument("--source-ids-file", default=None,
                    help="path to a newline-delimited list of source_ids to regenerate "
                         "(targets just those -- avoids churning all models when only a "
                         "handful changed, e.g. after a spine_entity backfill)")
    ap.add_argument("--dry-run", action="store_true", help="print, write nothing")
    ap.add_argument("--force", action="store_true", help="overwrite an existing model file (default: skip)")
    args = ap.parse_args()

    conn = snow.connect()
    try:
        cur = conn.cursor()
        sources = fetch_sources(cur, args.source_id, args.limit)
        if args.source_ids_file:
            wanted = {ln.strip() for ln in Path(args.source_ids_file).read_text().splitlines() if ln.strip()}
            sources = [s for s in sources if s["source_id"] in wanted]
            missing = wanted - {s["source_id"] for s in sources}
            if missing:
                print(f"  note: {len(missing)} id(s) in the file had no GRAIN/NATURAL_KEY row "
                      f"and were skipped: {', '.join(sorted(missing))}")
        print(f"{len(sources)} source(s) with GRAIN/NATURAL_KEY/SPINE_ENTITY populated.")
        declared = already_declared_source_tables()

        written, skipped = [], []
        for src in sources:
            sid = src["source_id"]
            own_dir = str(MODELS_DIR / sid)
            # The table's source: block may already be declared in a folder OTHER
            # than this source's own (a genuine cross-folder collision -- dbt
            # errors on a duplicate source declaration). That does NOT mean a
            # staging MODEL exists for this source -- only that this folder's
            # schema.yml must skip re-declaring the source and rely on the
            # other folder's declaration instead (include_source=False below).
            other_dirs = declared.get(sid.upper(), set()) - {own_dir}
            include_source = not other_dirs
            columns, ingested_at_column = fetch_columns(cur, sid.upper())
            if not columns:
                skipped.append((sid, "no landed columns found"))
                continue
            missing_nk = [c for c in src["natural_key"] if c not in {cn for cn, _ in columns}]
            if missing_nk:
                skipped.append((sid, f"natural_key column(s) no longer present: {missing_nk}"))
                continue

            entity_plural = PLURAL.get(src["spine_entity"]) or (
                src["spine_entity"] + "s" if src["spine_entity"] else "records"
            )
            model_name = f"stg_{sid}__{entity_plural}"
            out_dir = MODELS_DIR / sid
            out_path = out_dir / f"{model_name}.sql"
            yml_path = out_dir / "schema.yml"

            # Skip if this folder has ANY .sql model already -- not just the exact
            # target filename. A hand-built model can use a different <entity>
            # slug than this generator would choose (e.g. stg_fed_oyez__scotus_cases
            # vs. this generator's stg_fed_oyez__cases) -- checking only out_path
            # would silently add a second, competing draft model alongside it.
            existing_models = [] if args.dry_run else [
                p for p in out_dir.glob("*.sql")
                if args.force is False or "Generated by scripts/generate_staging_models.py"
                not in p.read_text(encoding="utf-8", errors="ignore")
            ]
            if existing_models:
                # non-empty here means a hand-built file (the --force filter above
                # already excludes this generator's own prior output) -- never
                # overwritten, --force or not.
                skipped.append((sid, f"{out_dir.name}/ already has a hand-built model "
                                      f"({', '.join(p.name for p in existing_models)}) -- not adding "
                                      "a second one."))
                continue

            sql = render_model(src, columns, ingested_at_column)
            nk_snake = [snake(c) for c in src["natural_key"]]
            yml = render_schema_yml(model_name, src, nk_snake, sid.upper(), include_source=include_source)

            if args.dry_run:
                print(f"\n{'=' * 78}\n-- {out_path}\n{'=' * 78}\n{sql}")
                print(f"-- {yml_path}\n{'=' * 78}\n{yml}")
            else:
                out_dir.mkdir(parents=True, exist_ok=True)
                # A prior generator run may have written this model under a
                # DIFFERENT <entity> slug (e.g. spine_entity went NULL->place, so
                # stg_x__records.sql should become stg_x__places.sql). Remove the
                # stale generator-produced sibling so the rename doesn't leave two
                # competing models in the folder. Only ever deletes THIS
                # generator's own output (never a hand-built model), and never the
                # file we're about to write.
                for p in out_dir.glob("stg_*.sql"):
                    if p != out_path and "Generated by scripts/generate_staging_models.py" \
                            in p.read_text(encoding="utf-8", errors="ignore"):
                        p.unlink()
                out_path.write_text(sql, encoding="utf-8")
                if not yml_path.exists() or args.force:
                    yml_path.write_text(yml, encoding="utf-8")
            written.append(str(out_path))

        cur.close()
        print(f"\n{'DRY RUN, nothing written' if args.dry_run else 'wrote'}: {len(written)} model(s)")
        if skipped:
            print(f"skipped {len(skipped)}:")
            for sid, why in skipped:
                print(f"  {sid}: {why}")
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
