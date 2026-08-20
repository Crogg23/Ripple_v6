"""Shape 8 of the time census: things being BORN and things DYING.

The count sweep measures events. This one measures the population producing them.
For every clocked table whose rows repeat per entity -- the same facility, the
same firm, the same operator, the same prescriber appearing year after year --
it measures three curves nobody has ever looked at in this warehouse:

  BIRTHS   how many entities appear for the FIRST time in each year
  DEATHS   how many are seen for the LAST time in each year
  LIFESPAN how many years an entity stays in the data, as a histogram

Why this is a different question from the count sweep, not a restatement of it:
a flat event count can hide total population churn, and a rising event count can
come entirely from the same entities being counted more often. Births and deaths
separate those two. They are also the cheapest honest denominator available
inside a single table -- events per living entity needs no second source, which
is exactly what the parked "denominators" branch needs a second source for.

The death curve carries a permanent caveat, stated here so no reader misses it:
LAST SEEN IS NOT DEAD. An entity whose final appearance is the last year of the
data has not died; the data just stopped. The scorer drops the trailing period
for that reason, and the raw file keeps it so the choice stays visible.

Two stages per table, both aggregate-only:
  1. measure candidate identifier columns -- an entity column must REPEAT, so a
     column with one distinct value per row is a row id and is rejected
  2. one grouped pass returning births, deaths and the lifespan histogram

Read-only. Checkpointed per table. Writes reports/time_index/cohorts.jsonl.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _snowflake_conn import connect  # noqa: E402
from _time_targets import (TI, Checkpoint, DATE_TYPES, date_expr,  # noqa: E402
                           load_catalog, load_clock_roles, load_measured,
                           pick_measurable, table_alias_map, year_expr)

OUT = os.path.join(TI, "cohorts.jsonl")
CKPT = os.path.join(TI, "cohorts_done.json")

# Identifier-shaped column names. Deliberately wider than the verified spine key
# list: an unverified column that turns out to repeat sensibly is still a usable
# cohort axis for THIS measurement, which never joins to anything else.
ID_NAME = re.compile(
    r"(^|_)(ID|IDS|NUMBER|NUM|NO|EIN|NPI|CIK|CRD|DUNS|LEI|UEI|CCN|DEA|IRS|"
    r"CASE|DOCKET|PERMIT|LICENSE|LICENCE|REGISTRY|REGISTRANT|ACCESSION|"
    r"OPERATOR|FACILITY|ESTABLISHMENT|PROVIDER|SPONSOR|FILER|CONTRACTOR|"
    r"RECIPIENT|AWARDEE|EMPLOYER|INSTITUTION|COMPANY|ORG|ENTITY|MINE|VESSEL|"
    r"PLANT|SITE|STATION|BANK|UNION|SCHOOL|HOSPITAL)($|_)")
# Strongest first: these are the identifiers the platform already trusts.
STRONG = ["EIN", "NPI", "CIK", "LEI", "UEI", "DUNS", "CCN", "DEA", "CRD",
          "MINE_ID", "FACILITY_ID", "OPERATOR_ID", "PROVIDER_ID", "REGISTRY_ID"]
BAD_NAME = re.compile(r"(^|_)(ROW|LINE|SEQ|INDEX|IDX|RECORD|TRANSACTION|TXN|"
                      r"UUID|GUID|HASH|SK|SURROGATE)($|_)")
MAX_COLS = 8
CLOCK_RANK = {"happened": 0, "reported": 1, "decided": 2, "span_start": 3}
# An entity column must repeat. Above this share of rows it is a row identifier
# and births/deaths would just restate the count sweep.
MAX_DISTINCT_SHARE = 0.5
MIN_ENTITIES = 10


def _priority(col):
    for i, s in enumerate(STRONG):
        if s in col:
            return i
    return len(STRONG)


def load_targets(max_rows=None):
    roles = load_clock_roles()
    meas = load_measured()
    alias = table_alias_map()
    cat = load_catalog()
    targets, oversize = [], []
    for model, byrole in roles.items():
        clock = cm = None
        for role in sorted(CLOCK_RANK, key=CLOCK_RANK.get):
            cm = pick_measurable(byrole, role, model, meas)
            if cm is not None:
                clock = (role, cm)
                break
        full = alias.get(model)
        if clock is None or not full:
            continue
        if int(cm["trusted"] or 0) <= 0 and not (cm["ymin"] or "").strip():
            continue
        clock_col = cm["col"].upper()
        cands = [c for c, dt in cat.get(model, [])
                 if dt in ("TEXT", "NUMBER") and ID_NAME.search(c)
                 and not BAD_NAME.search(c) and c != clock_col
                 and not c.startswith("_")]
        if not cands:
            continue
        cands.sort(key=lambda c: (_priority(c), len(c)))
        n_rows = int(cm["n_rows"] or 0)
        rec = {
            "table": full, "model": model, "clock": clock[0],
            "clock_col": cm["col"], "clock_dtype": cm["dtype"],
            "clock_grain": cm["grain"],
            "candidates": cands[:MAX_COLS], "n_candidates_total": len(cands),
            "n_rows": n_rows,
        }
        if max_rows and n_rows > max_rows:
            oversize.append(rec)
            continue
        targets.append(rec)
    targets.sort(key=lambda t: t["n_rows"])
    oversize.sort(key=lambda t: -t["n_rows"])
    return targets, oversize


def year_of_clock(t):
    if t["clock_grain"] == "year" and t["clock_dtype"] not in DATE_TYPES:
        return year_expr(t["clock_col"])
    return "year({})".format(date_expr(t["clock_col"], t["clock_dtype"]))


def _src(t):
    sch, tab = t["table"].split(".", 1)
    return 'LIBRARY_MARTS."{}"."{}"'.format(sch, tab)


def cardinality_sql(t):
    parts = ["count(*)"]
    for c in t["candidates"]:
        parts.append('approx_count_distinct("{}")'.format(c))
        parts.append('count("{}")'.format(c))
    return "select {} from {}".format(", ".join(parts), _src(t))


def cohort_sql(t, col):
    return (
        'with b as (select nullif(trim(to_varchar("{col}")), \'\') as e, {y} as y '
        "from {src}), "
        "g as (select e, min(y) as fy, max(y) as ly, count(*) as cnt "
        "from b where e is not null and y is not null group by 1) "
        "select 'born' as kind, fy as bucket, count(*) as n_entities, sum(cnt) as n_rows "
        "from g group by 1, 2 "
        "union all "
        "select 'died', ly, count(*), sum(cnt) from g group by 1, 2 "
        "union all "
        "select 'lifespan', ly - fy, count(*), sum(cnt) from g group by 1, 2 "
        "order by 1, 2"
    ).format(col=col, y=year_of_clock(t), src=_src(t))


def main():
    args = [a for a in sys.argv[1:]]
    max_rows = None
    limit = None
    for a in args:
        if a.startswith("--max-rows="):
            max_rows = int(a.split("=", 1)[1])
        elif a.startswith("--limit="):
            limit = int(a.split("=", 1)[1])
    targets, oversize = load_targets(max_rows)
    if limit:
        targets = targets[:limit]
    ck = Checkpoint(OUT, CKPT)
    conn = connect(database="LIBRARY_MARTS")
    cur = conn.cursor()
    print("{} clocked tables carry a candidate entity column; {} already measured"
          .format(len(targets), len(ck.done)), flush=True)
    if oversize:
        # No silent caps: what was skipped is named, in the log AND in the file.
        print("SKIPPED {} tables over --max-rows={} ({:,} rows in total): {}"
              .format(len(oversize), max_rows, sum(t["n_rows"] for t in oversize),
                      ", ".join(t["table"] for t in oversize[:10])), flush=True)
        for t in oversize:
            if not ck.has(t["table"]):
                ck.write(t["table"], dict(t, skipped="over max_rows cap"))

    ok = skipped = failed = 0
    for t in targets:
        key = t["table"]
        if ck.has(key):
            continue
        try:
            cur.execute(cardinality_sql(t))
            row = cur.fetchone()
        except Exception as e:
            ck.write(key, dict(t, stage="cardinality", error=str(e)[:300]))
            failed += 1
            continue

        total = int(row[0] or 0)
        card = []
        for i, c in enumerate(t["candidates"]):
            card.append({"col": c, "approx_distinct": int(row[1 + 2 * i] or 0),
                         "nonnull": int(row[2 + 2 * i] or 0)})
        usable = [k for k in card
                  if k["approx_distinct"] >= MIN_ENTITIES
                  and total > 0
                  and k["approx_distinct"] <= MAX_DISTINCT_SHARE * total
                  and k["nonnull"] >= 0.5 * total]
        if not usable:
            ck.write(key, dict(t, n_rows_live=total, cardinality=card, chosen=None,
                               note="no column both repeats and is well populated"))
            skipped += 1
            continue
        # Prefer a trusted identifier; among equals, the one covering most rows.
        usable.sort(key=lambda k: (_priority(k["col"]), -k["nonnull"]))
        chosen = usable[0]["col"]

        try:
            cur.execute(cohort_sql(t, chosen))
            rows = cur.fetchall()
        except Exception as e:
            ck.write(key, dict(t, n_rows_live=total, cardinality=card,
                               chosen=chosen, stage="cohort", error=str(e)[:300]))
            failed += 1
            continue

        curves = {"born": [], "died": [], "lifespan": []}
        for r in rows:
            kind = str(r[0])
            if kind in curves and r[1] is not None:
                curves[kind].append([int(r[1]), int(r[2]), int(r[3] or 0)])
        rec = dict(t)
        rec["n_rows_live"] = total
        rec["cardinality"] = card
        rec["chosen"] = chosen
        rec["n_entities"] = sum(c[1] for c in curves["born"])
        rec["curves"] = curves
        ck.write(key, rec)
        ok += 1
        if ok % 25 == 0:
            print("  {} measured, {} had no repeating entity ({} failed)"
                  .format(ok, skipped, failed), flush=True)

    print("COHORT SWEEP DONE  measured={} skipped={} failed={}"
          .format(ok, skipped, failed), flush=True)


if __name__ == "__main__":
    main()
