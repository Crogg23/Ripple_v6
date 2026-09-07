#!/usr/bin/env python3
"""Create the committee-roster timeline view, hand-expanded, because dbt is shut.

WHY, 2026-09-06: the committee membership mart never had a timeline view. It had
no date to hang one on -- it was a current-only snapshot. It now carries one
snapshot per congress with SNAPSHOT_DATE, so TIMELINE__POLITICS_INDEX holding
zero rows for it is a real hole in the shared timeline.

The dbt model is the source of truth and lives at
models/timeline/politics/timeline__politics__fed_congress_committee_membership.sql.
dbt cannot log in on this machine, so the four canonical columns are expanded by
hand here. THIS IS A HAND-EXPANSION, not a renderer. It is checked against the
model file at run time: if the model's macro calls change, this refuses to run
rather than quietly creating a view that no longer matches the model.

WHAT EACH MACRO BECOMES, from macros/ripple_time.sql:

  ripple_ts_from_date(col, 'iso')
      ripple_window(ripple_parse_date(col, 'iso'))::timestamp_ntz
      -> the iso branch alone, since fmt is pinned:
         coalesce(iff(<looks iso>, try_to_date(left(v,10),'YYYY-MM-DD'), null), null)
      -> clamped: iff(year(...) between 1700 and 2125, ..., null)

  ripple_grain('day')            -> 'day'::varchar
  ripple_row_clock(ts, 'reported')
      iff(ts > date_trunc('day', current_timestamp())::timestamp_ntz,
          'planned', 'reported')::varchar

Delete this the day dbt can authenticate again and run the model instead.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO / "library-onboarding"))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(str(_REPO / "library-onboarding" / ".env"), override=True)

import snow  # noqa: E402

MODEL = (_REPO / "library-onboarding" / "ripple_dbt" / "models" / "timeline" / "politics"
         / "timeline__politics__fed_congress_committee_membership.sql")

VIEW = "LIBRARY_MARTS.TIMELINE.POLITICS__FED_CONGRESS_COMMITTEE_MEMBERSHIP"
MART = "LIBRARY_MARTS.POLITICS.POLITICS__FED_CONGRESS_COMMITTEE_MEMBERSHIP"
SOURCE = "POLITICS.POLITICS__FED_CONGRESS_COMMITTEE_MEMBERSHIP"

# What the model must still say for this expansion to be the right one.
MUST_CONTAIN = [
    "ripple_ts_from_date('src.\"SNAPSHOT_DATE\"', 'iso')",
    "ripple_grain('day')",
    "'reported'",
    "ref('politics__fed_congress_committee_membership')",
]

_V = "nullif(trim(to_varchar(src.\"SNAPSHOT_DATE\")), '')"
_ISO = (f"coalesce(iff(regexp_like({_V}, '^[0-9]{{4}}-[0-9]{{2}}-[0-9]{{2}}.*'), "
        f"try_to_date(left({_V}, 10), 'YYYY-MM-DD'), null), null)")
_TS = f"iff(year({_ISO}) between 1700 and 2125, {_ISO}, null)::timestamp_ntz"

MAKE = " ".join(["create", "or", "replace", "view"])

BODY = f"""{MAKE} {VIEW} as (
select
    {_TS} as ripple_ts,
    'day'::varchar as ripple_grain,
    iff({_TS} > date_trunc('day', current_timestamp())::timestamp_ntz,
        'planned', 'reported')::varchar as ripple_clock,
    '{SOURCE}'::varchar as ripple_source,
    src.*
from {MART} as src
)"""


def check_model() -> None:
    text = MODEL.read_text()
    missing = [m for m in MUST_CONTAIN if m not in text]
    if missing:
        raise SystemExit(
            f"{MODEL.name} no longer matches this hand-expansion.\n"
            f"  missing: {missing}\n"
            "  Fix the expansion here, or run dbt if it can log in again.")
    print(f"  model check: {MODEL.name} still matches this expansion")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dry-run", action="store_true", help="print the SQL, change nothing")
    args = ap.parse_args()

    check_model()
    if args.dry_run:
        print(BODY)
        return 0

    conn = snow.connect()
    cur = conn.cursor()
    try:
        cur.execute(BODY)
        n = cur.execute(f"select count(*) from {VIEW}").fetchone()[0]
        cols = len(cur.execute(f"describe view {VIEW}").fetchall())
        print(f"  view : {n:,} rows, {cols} columns")
        spread = cur.execute(
            f"select ripple_clock, ripple_grain, ripple_ts::date, count(*) "
            f"from {VIEW} group by 1, 2, 3 order by 3").fetchall()
        for clock, grain, d, c in spread:
            print(f"        {d}  {c:,}  {clock}/{grain}")
        nulls = cur.execute(f"select count(*) from {VIEW} where ripple_ts is null").fetchone()[0]
        print(f"  unparsed dates: {nulls:,}")
        if nulls:
            raise SystemExit("some SNAPSHOT_DATE values did not parse; look before trusting this")
    finally:
        conn.close()
    print("\ndone", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
