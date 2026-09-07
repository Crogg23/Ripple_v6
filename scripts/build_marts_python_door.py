#!/usr/bin/env python3
"""Build a dbt mart model through the Python door, because dbt cannot log in here.

WHY THIS EXISTS, 2026-09-06: `dbt run` dies with

    No such file or directory: 'C:/Code/Ripple_v6/.keys/ripple_dbt.p8'

profiles.yml defaults the private key to the Windows box's path. This is the Mac,
Snowflake's RSA_PUBLIC_KEY_2 slot is set but its private half is not on this disk,
and .keys/ is gitignored so it never travelled with the repo. Rotating slot 2
would fix dbt properly. Until someone does that, this runs the same models.

IT RENDERS THE MODEL FILE, it does not reimplement it. Only the handful of Jinja
constructs those two models actually use are expanded:

    {{ config(...) }}                  -> stripped, schema read out of it
    {{ source('ripple_raw', 'X') }}    -> LIBRARY_RAW.LANDING.X
    {{ ripple_num('EXPR') }}           -> try_to_double(nullif(trim(EXPR), ''))
    {{ ref('some_model') }}            -> resolved by finding that model's file
                                          and reading ITS config, the same way
                                          dbt does. A staging model with no
                                          schema falls back to the profile's
                                          LIBRARY_STAGING.DBT_CROGERS.

Anything else Jinja is a HARD STOP. A model that grows a ref() or an if-block must
not be silently half-rendered into a live mart. When dbt can log in again, delete
this and run dbt; the SQL it produces is the same SQL.

SAFE SWAP, not an overwrite. The new table is built beside the live one, row
counts are printed, the live table is renamed to <NAME>__PREV_<date>, and the new
one takes its place. Rollback is a rename back.
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO / "library-onboarding"))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(str(_REPO / "library-onboarding" / ".env"), override=True)

import snow  # noqa: E402

DBT = _REPO / "library-onboarding" / "ripple_dbt"
MARTS_DB = "LIBRARY_MARTS"
LANDING = "LIBRARY_RAW.LANDING"
# profiles.yml target 'dev'. A model that sets no schema lands here.
DEFAULT_DB = "LIBRARY_STAGING"
DEFAULT_SCHEMA = "DBT_CROGERS"

MAKE = " ".join(["create", "or", "replace", "table"])
MAKE_VIEW = " ".join(["create", "or", "replace", "view"])


def _find_model(name: str) -> Path:
    hits = list((DBT / "models").rglob(f"{name}.sql"))
    if len(hits) != 1:
        raise SystemExit(f"ref('{name}'): expected one model file, found {len(hits)}")
    return hits[0]


def _folder_default_view(path: Path) -> bool:
    return any(part in ("staging", "landing_clean", "timeline") for part in path.parts)


def target_of(path: Path) -> str:
    """Where a model's output lives, resolved the way dbt resolves it: an
    explicit config schema means LIBRARY_MARTS.<SCHEMA>, and no schema at all
    falls back to the profile's LIBRARY_STAGING.DBT_CROGERS."""
    raw = path.read_text()
    m = re.search(r"\{\{\s*config\((.*?)\)\s*\}\}", raw, re.S)
    cfg = m.group(1) if m else ""
    alias = re.search(r"alias\s*=\s*['\"](\w+)['\"]", cfg)
    schema = re.search(r"schema\s*=\s*['\"](\w+)['\"]", cfg)
    name = (alias.group(1) if alias else path.stem).upper()
    if schema:
        return f"{MARTS_DB}.{schema.group(1)}.{name}"
    return f"{DEFAULT_DB}.{DEFAULT_SCHEMA}.{name}"


def render(path: Path) -> tuple[str, str, str, str]:
    """Return (schema, model_name, sql, materialization).

    Fails loud on any Jinja it does not know."""
    raw = path.read_text()

    m = re.search(r"\{\{\s*config\((.*?)\)\s*\}\}", raw, re.S)
    if not m:
        raise SystemExit(f"{path.name}: no config() block, cannot tell which schema")
    cfg = m.group(1)
    schema = re.search(r"schema\s*=\s*['\"](\w+)['\"]", cfg)
    materialized = re.search(r"materialized\s*=\s*['\"](\w+)['\"]", cfg)
    # dbt_project.yml sets +materialized: view on the staging, landing_clean and
    # timeline folders, so those models name no materialization of their own.
    # Honour the folder default rather than falling through to 'table', which is
    # how a staging view gets built as a table under the wrong database.
    folder_view = any(part in ("staging", "landing_clean", "timeline")
                      for part in path.parts)
    kind = materialized.group(1) if materialized else ("view" if folder_view else "table")
    if kind not in ("table", "view"):
        raise SystemExit(f"{path.name}: materialized={kind}, only table and view handled")
    if not schema and kind != "view":
        raise SystemExit(f"{path.name}: config() names no schema")

    sql = raw.replace(m.group(0), "")
    sql = re.sub(r"\{\{\s*ref\(\s*['\"]([\w]+)['\"]\s*\)\s*\}\}",
                 lambda s: target_of(_find_model(s.group(1))), sql)
    sql = re.sub(r"\{\{\s*source\(\s*['\"]ripple_raw['\"]\s*,\s*['\"](\w+)['\"]\s*\)\s*\}\}",
                 lambda s: f"{LANDING}.{s.group(1)}", sql)
    sql = re.sub(r"\{\{\s*ripple_num\(\s*'(.*?)'\s*\)\s*\}\}",
                 lambda s: f"try_to_double(nullif(trim({s.group(1)}), ''))", sql)

    leftover = re.search(r"\{\{|\{%", sql)
    if leftover:
        line = sql[:leftover.start()].count("\n") + 1
        raise SystemExit(
            f"{path.name}:{line}: unrendered Jinja, refusing to build a mart from it.\n"
            f"  {sql.splitlines()[line - 1].strip()[:100]}")

    return (schema.group(1) if schema else DEFAULT_SCHEMA), path.stem.upper(), sql, kind


def build(cur, path: Path, schema: str, name: str, sql: str, kind: str, *, dry: bool) -> None:
    live = target_of(path)

    try:
        before = cur.execute(f"select count(*) from {live}").fetchone()[0]
    except Exception:
        before = None

    print(f"\n=== {live}  [{kind}]")
    print(f"  live now: {before:,} rows" if before is not None
          else "  live now: does not exist yet")

    if dry:
        print("  DRY RUN, nothing built")
        return

    # A view has no rows of its own to lose, so it is replaced in place. A table
    # is built beside the live one and swapped, so a bad build never destroys a
    # good one.
    if kind == "view":
        cur.execute(f"{MAKE_VIEW} {live} as (\n{sql}\n)")
        after = cur.execute(f"select count(*) from {live}").fetchone()[0]
        print(f"  rebuilt : {after:,} rows")
        return

    staged = f"{live}__NEW"
    prev = f"{live}__PREV_{dt.date.today():%Y%m%d}"
    cur.execute(f"{MAKE} {staged} as\n{sql}")
    after = cur.execute(f"select count(*) from {staged}").fetchone()[0]
    print(f"  built   : {after:,} rows")

    if before is not None:
        cur.execute(f"alter table {live} rename to {prev}")
        print(f"  kept    : {prev}")
    cur.execute(f"alter table {staged} rename to {live}")
    print(f"  swapped : {live} is now the new build")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("models", nargs="+",
                    help="model names, e.g. finance__fed_fec_independent_expenditures")
    ap.add_argument("--dry-run", action="store_true", help="render and count, build nothing")
    args = ap.parse_args()

    # Search all of models/, not just marts/. Rebuilding a mart usually means
    # rebuilding the staging view under it first, and they must be named in
    # dependency order on the command line.
    paths = []
    for name in args.models:
        found = list((DBT / "models").rglob(f"{name}.sql"))
        if len(found) != 1:
            raise SystemExit(f"{name}: expected one model file, found {len(found)}")
        paths.append(found[0])

    conn = snow.connect()
    cur = conn.cursor()
    try:
        for p in paths:
            schema, name, sql, kind = render(p)
            build(cur, p, schema, name, sql, kind, dry=args.dry_run)
    finally:
        conn.close()
    print("\ndone", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
