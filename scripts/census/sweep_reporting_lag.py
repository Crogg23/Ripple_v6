"""Shape 5 of the time census: how long between a thing happening and being told.

The first sweep asked "how many rows per period." This asks a question that
sweep structurally could not: for every table that carries BOTH a clock for when
something HAPPENED and a clock for when it was REPORTED or DECIDED, measure the
gap per row, then watch that gap move over time.

Why this is the shape that matters most right now: the 2026-08-20 sweep's
headline was that most warehouse strangeness is about COLLECTION, not the world.
Reporting lag measures collection directly. A lag that widens means a publisher
falling behind. A lag that suddenly collapses means a process change, not a world
change. A NEGATIVE lag means the data is impossible and the labels are wrong.

Per table, one aggregate:
  * bucket by the year the thing HAPPENED
  * per bucket: rows, share never reported, share reported before it happened,
    share reported more than a year later, and the 10th/50th/90th percentile lag

Read-only. Checkpointed. Writes reports/time_index/lag.jsonl.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _snowflake_conn import connect  # noqa: E402
from _time_targets import (TI, Checkpoint, DATE_TYPES, date_expr,  # noqa: E402
                           load_clock_roles, load_measured, pick_measurable,
                           table_alias_map, year_expr)

OUT = os.path.join(TI, "lag.jsonl")
CKPT = os.path.join(TI, "lag_done.json")

# "decided" is a legitimate downstream clock (a court ruling, an agency
# determination). It is kept separate from "reported" so the write-up can say
# which kind of gap it measured.
DOWNSTREAM = ("reported", "decided")


def load_targets():
    roles = load_clock_roles()
    meas = load_measured()
    alias = table_alias_map()
    targets = []
    for model, byrole in roles.items():
        if "happened" not in byrole:
            continue
        full = alias.get(model)
        if not full:
            continue
        hm = pick_measurable(byrole, "happened", model, meas)
        rm = down_role = None
        for role in DOWNSTREAM:
            rm = pick_measurable(byrole, role, model, meas)
            if rm is not None:
                down_role = role
                break
        if hm is None or rm is None:
            continue
        down = (down_role, rm)
        # both sides must actually hold values, or the gap is unmeasurable
        if int(hm["nonnull"] or 0) == 0 or int(rm["nonnull"] or 0) == 0:
            continue
        targets.append({
            "table": full, "model": model,
            "happened_col": hm["col"], "happened_dtype": hm["dtype"],
            "happened_grain": hm["grain"],
            "down_role": down[0], "down_col": rm["col"], "down_dtype": rm["dtype"],
            "down_grain": rm["grain"],
            "n_rows": int(hm["n_rows"] or 0),
        })
    targets.sort(key=lambda t: t["n_rows"])
    return targets


def build_sql(t):
    """Day-grain both sides -> lag in days. Anything year-only -> lag in years."""
    sch, tab = t["table"].split(".", 1)
    src = f'LIBRARY_MARTS."{sch}"."{tab}"'
    day_both = (t["happened_grain"] != "year" and t["down_grain"] != "year"
                and not (t["happened_dtype"] == "NUMBER" and t["happened_grain"] == "year"))

    if day_both:
        h = date_expr(t["happened_col"], t["happened_dtype"])
        r = date_expr(t["down_col"], t["down_dtype"])
        gap = f"datediff(day, h, r)"
        period = "to_varchar(year(h))"
        unit = "days"
        over = 365
    else:
        h = year_expr(t["happened_col"]) if t["happened_dtype"] not in DATE_TYPES \
            else f'year("{t["happened_col"]}")'
        r = year_expr(t["down_col"]) if t["down_dtype"] not in DATE_TYPES \
            else f'year("{t["down_col"]}")'
        gap = "r - h"
        period = "to_varchar(h)"
        unit = "years"
        over = 1

    sql = (
        f"with b as (select {h} as h, {r} as r from {src}), "
        f"g as (select h, r, iff(r is null, null, {gap}) as gap from b where h is not null) "
        f"select {period} as period, count(*) as n, "
        f"count_if(r is null) as n_unreported, "
        f"count_if(gap < 0) as n_negative, "
        f"count_if(gap > {over}) as n_slow, "
        f"approx_percentile(gap, 0.1) as p10, "
        f"approx_percentile(gap, 0.5) as p50, "
        f"approx_percentile(gap, 0.9) as p90 "
        f"from g group by 1 order by 1"
    )
    return sql, unit


def main():
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else None
    targets = load_targets()
    if limit:
        targets = targets[:limit]
    ck = Checkpoint(OUT, CKPT)
    conn = connect(database="LIBRARY_MARTS")
    cur = conn.cursor()
    print(f"{len(targets)} tables carry both a happened and a reported/decided clock; "
          f"{len(ck.done)} already measured", flush=True)

    ok = failed = 0
    for t in targets:
        key = f"{t['table']}|{t['happened_col']}|{t['down_col']}"
        if ck.has(key):
            continue
        sql, unit = build_sql(t)
        try:
            cur.execute(sql)
            pts = [{"period": str(r[0]), "n": int(r[1]), "unreported": int(r[2] or 0),
                    "negative": int(r[3] or 0), "slow": int(r[4] or 0),
                    "p10": None if r[5] is None else float(r[5]),
                    "p50": None if r[6] is None else float(r[6]),
                    "p90": None if r[7] is None else float(r[7])}
                   for r in cur.fetchall() if r[0] is not None]
        except Exception as e:
            ck.write(key, {**t, "error": str(e)[:300]})
            failed += 1
            continue
        rec = dict(t)
        rec["unit"] = unit
        rec["points"] = pts
        rec["n_measured"] = sum(p["n"] for p in pts)
        ck.write(key, rec)
        ok += 1
        if ok % 20 == 0:
            print(f"  {ok} measured ({failed} failed)", flush=True)

    print(f"LAG SWEEP DONE  measured={ok} failed={failed}", flush=True)


if __name__ == "__main__":
    main()
