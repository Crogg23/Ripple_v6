"""Shape 6 of the time census: stock, not flow -- what was LIVE on a given date.

Every series the first sweep pulled was a FLOW: things happening per period.
Seventy-five warehouse tables describe something quite different -- a thing with
a beginning and an end. A permit, a detention, a debarment, a survey window, an
employment spell, a contract. For those, "how many started this year" is the
least interesting question. The real ones are:

  * how many were ACTIVE on any given date (the stock curve)
  * how long they last (the duration distribution, and whether it is drifting)
  * how many never ended (still open -- or never closed out in the data)
  * how many END BEFORE THEY START (impossible; a labelling or parsing fault)

Method, one aggregate per table: return the count of rows for every
(start year, end year) pair, plus the median duration in each. The active-on-date
curve is then reconstructed client-side by pure arithmetic -- no second query,
no cross join, no calendar table needed at sweep time.

Read-only. Checkpointed. Writes reports/time_index/spans.jsonl.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _snowflake_conn import connect  # noqa: E402
from _time_targets import (TI, Checkpoint, DATE_TYPES, date_expr,  # noqa: E402
                           load_clock_roles, load_measured, pick_measurable,
                           table_alias_map, year_expr)

OUT = os.path.join(TI, "spans.jsonl")
CKPT = os.path.join(TI, "spans_done.json")

# A (start year, end year) grid is small for real data and enormous for junk.
# If a table blows past this it is telling us something is wrong with it, so the
# cap is RECORDED on the row rather than silently applied.
MAX_CELLS = 40000


def load_targets():
    roles = load_clock_roles()
    meas = load_measured()
    alias = table_alias_map()
    targets = []
    for model, byrole in roles.items():
        if not (byrole.get("span_start") and byrole.get("span_end")):
            continue
        full = alias.get(model)
        if not full:
            continue
        sm = pick_measurable(byrole, "span_start", model, meas)
        em = pick_measurable(byrole, "span_end", model, meas)
        if sm is None or em is None or int(sm["nonnull"] or 0) == 0:
            continue
        targets.append({
            "table": full, "model": model,
            "start_col": sm["col"], "start_dtype": sm["dtype"], "start_grain": sm["grain"],
            "end_col": em["col"], "end_dtype": em["dtype"], "end_grain": em["grain"],
            "n_rows": int(sm["n_rows"] or 0),
        })
    targets.sort(key=lambda t: t["n_rows"])
    return targets


def build_sql(t):
    sch, tab = t["table"].split(".", 1)
    src = f'LIBRARY_MARTS."{sch}"."{tab}"'
    day_both = t["start_grain"] != "year" and t["end_grain"] != "year"

    if day_both:
        s = date_expr(t["start_col"], t["start_dtype"])
        e = date_expr(t["end_col"], t["end_dtype"])
        ys, ye = "year(s)", "year(e)"
        dur = "datediff(day, s, e)"
        unit = "days"
    else:
        s = (year_expr(t["start_col"]) if t["start_dtype"] not in DATE_TYPES
             else f'year("{t["start_col"]}")')
        e = (year_expr(t["end_col"]) if t["end_dtype"] not in DATE_TYPES
             else f'year("{t["end_col"]}")')
        ys, ye = "s", "e"
        dur = "e - s"
        unit = "years"

    sql = (
        f"with b as (select {s} as s, {e} as e from {src}) "
        f"select {ys} as y_start, {ye} as y_end, count(*) as n, "
        f"approx_percentile({dur}, 0.5) as p50_dur "
        f"from b where s is not null group by 1, 2 order by 1, 2"
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
    print(f"{len(targets)} tables describe a thing with a start and an end; "
          f"{len(ck.done)} already measured", flush=True)

    ok = failed = 0
    for t in targets:
        key = f"{t['table']}|{t['start_col']}|{t['end_col']}"
        if ck.has(key):
            continue
        sql, unit = build_sql(t)
        try:
            cur.execute(sql)
            rows = cur.fetchmany(MAX_CELLS)
            truncated = len(rows) == MAX_CELLS and cur.fetchone() is not None
            cells = [[None if r[0] is None else int(r[0]),
                      None if r[1] is None else int(r[1]),
                      int(r[2]),
                      None if r[3] is None else float(r[3])] for r in rows]
        except Exception as e:
            ck.write(key, {**t, "error": str(e)[:300]})
            failed += 1
            continue
        rec = dict(t)
        rec["unit"] = unit
        rec["cells"] = cells                       # [y_start, y_end|None, n, p50]
        rec["truncated"] = truncated
        rec["n_measured"] = sum(c[2] for c in cells)
        rec["n_open"] = sum(c[2] for c in cells if c[1] is None)
        rec["n_backwards"] = sum(c[2] for c in cells
                                 if c[1] is not None and c[0] is not None and c[1] < c[0])
        ck.write(key, rec)
        ok += 1
        if ok % 20 == 0:
            print(f"  {ok} measured ({failed} failed)", flush=True)

    print(f"SPAN SWEEP DONE  measured={ok} failed={failed}", flush=True)


if __name__ == "__main__":
    main()
