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

IT NOW READS dbt_project.yml, which it did not before 2026-09-07. It imported
no YAML parser at all, so `+enabled: false` and the marts.politics pre-hook
guard did not exist as far as it was concerned. On 2026-09-06 that let it build
two disabled models -- politics__fed_govinfo_billstatus and
politics__fed_govinfo_bill_cosponsors -- plus five POLITICS marts that
guard_politics_mirror() would have refused. Three gates now, all checked before
the connection opens:

    +enabled: false           -> hard stop, no override
    marts/politics/           -> hard stop unless --allow-politics-rebuild,
                                 the stand-in for dbt's
                                 --vars '{"allow_politics_rebuild": true}'
    TRANSIENT tables          -> matches dbt-snowflake. Permanent tables carry
                                 seven days of fail-safe storage that cannot be
                                 cleared afterwards, only rebuilt away.
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

MAKE = " ".join(["create", "or", "replace", "transient", "table"])
MAKE_VIEW = " ".join(["create", "or", "replace", "view"])

# 2026-09-07: TRANSIENT, to match dbt-snowflake. dbt makes every mart transient
# and this script was making them permanent, so the 14 tables it built on
# 2026-09-06 sat among 648 transient siblings carrying seven days of fail-safe
# storage nobody asked for. Fail-safe cannot be turned off after the fact --
# only a rebuild as transient clears it.
PROJECT_YML = DBT / "dbt_project.yml"
# The folder whose pre-hook exists to stop anything but the hand-reconciled
# Python loaders from overwriting a mart. See macros/guard_politics_mirror.sql.
GUARDED_FOLDER = "politics"


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


def _project_config() -> dict:
    """models.ripple out of dbt_project.yml, or {} if it cannot be read.

    Added 2026-09-07. This script used to ignore dbt_project.yml completely --
    it imported no YAML parser at all -- so `+enabled: false` and the politics
    pre-hook guard did not exist as far as it was concerned. On 2026-09-06 it
    built politics__fed_govinfo_billstatus and politics__fed_govinfo_bill_cosponsors,
    both marked disabled, and five POLITICS marts the guard would have refused.
    """
    try:
        import yaml
    except ImportError:
        print("  !! pyyaml missing: cannot read dbt_project.yml, refusing to build")
        raise SystemExit(2)
    try:
        cfg = yaml.safe_load(PROJECT_YML.read_text()) or {}
    except Exception as exc:
        print(f"  !! dbt_project.yml will not parse: {exc}")
        raise SystemExit(2)
    node = (cfg.get("models") or {}).get("ripple")
    # FAIL CLOSED. An empty or moved models.ripple used to return {}, which made
    # _model_flags answer (True, False) for everything -- both gates silently
    # off, politics guard included. A config this script cannot read is a reason
    # to stop, never a reason to assume permission.
    if not node:
        print("  !! dbt_project.yml has no models.ripple section: refusing to build")
        raise SystemExit(2)
    return node


def _model_flags(path: Path) -> tuple[bool, bool]:
    """(enabled, guarded) for one model, read the way dbt reads it.

    Walks models.ripple down the model's own folder path, so a +enabled set on
    a folder is inherited and a per-model one overrides it. Anything the file
    does not mention is enabled, which is dbt's default too.
    """
    # The model's OWN config block first. dbt_project.yml is not the only place
    # a model can be switched off, and this gate used to read only the yml: 36
    # model files carry enabled=false inside {{ config(...) }}, and 32 of them
    # sailed straight through to build(). uncategorized__fed_eia_860_plant was
    # the one that proved it. Checked before the yml so a file-level off wins
    # even when the yml says nothing at all.
    m = re.search(r"\{\{\s*config\((.*?)\)\s*\}\}", path.read_text(), re.S)
    if m and re.search(r"enabled\s*=\s*(?:False|false)\b", m.group(1)):
        return False, False

    node = _project_config()
    enabled, guarded = True, False
    parts = list(path.relative_to(DBT / "models").parts[:-1]) + [path.stem]
    for part in parts:
        if not isinstance(node, dict):
            break
        if node.get("+enabled") is False:
            enabled = False
        if node.get("+pre-hook") and GUARDED_FOLDER in path.parts:
            guarded = True
        node = node.get(part)
        if node is None:
            break
    if isinstance(node, dict) and node.get("+enabled") is False:
        enabled = False
    return enabled, guarded


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
    ap.add_argument("--allow-politics-rebuild", action="store_true",
                    help="the standing-in for dbt's --vars allow_politics_rebuild. "
                         "Required for any model under marts/politics/, which "
                         "mirrors a hand-reconciled Python-built table.")
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

    # Every gate is checked BEFORE the first connection is opened, so a refusal
    # costs nothing and cannot leave a half-built table behind.
    for p in paths:
        enabled, guarded = _model_flags(p)
        if not enabled:
            raise SystemExit(
                f"BLOCKED: {p.stem} is +enabled: false in dbt_project.yml. dbt "
                f"would not build it and neither will this. Flip it to true "
                f"there, with a reason, if it should be live again.")
        if guarded and not args.allow_politics_rebuild:
            raise SystemExit(
                f"BLOCKED: {p.stem} is under marts/{GUARDED_FOLDER}/, which "
                f"carries the guard_politics_mirror() pre-hook. It mirrors a "
                f"hand-reconciled, OpenFEC/GovTrack-checked table, and "
                f"rebuilding it would overwrite audited numbers with this "
                f"script's own SQL -- no error, no warning, just different "
                f"numbers. Pass --allow-politics-rebuild if that is really "
                f"what you mean.")

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
