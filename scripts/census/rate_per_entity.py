"""Events per LIVING entity -- the denominator, from inside a single table.

WHY THIS EXISTS
---------------
The 2026-08-20 count sweep ended on an uncomfortable result: most of the strange
shapes in this warehouse are about how the data was collected, not what happened.
Its conclusion was that no trend claim is safe without a denominator -- events per
inspector, filings per filer, monitors online -- and that getting one meant
pairing every series with a SECOND table. That was parked as expensive.

The entity-cohort sweep changes the price. For every table where the same entity
recurs across years, the population is already measurable inside that one table:
an entity is present in year Y if it was first seen on or before Y and last seen
on or after Y. Divide the event count by that population and the question
"more violations, or more mines?" becomes answerable with no join at all.

This script does exactly that, using two measurements that already exist:

    series.jsonl   events per period, from the count sweep
    cohorts.jsonl  first-seen and last-seen per entity, from the cohort sweep

No warehouse. No new queries. Pure arithmetic over files already on disk.

WHAT THIS DENOMINATOR IS, AND IS NOT
------------------------------------
It counts entities VISIBLE IN THIS DATASET, which is a proxy for the real
population and not the population itself. A mine with no violations in a given
year still counts as present if it has violations either side -- that is what
makes it a usable denominator -- but a mine that never appears at all is
invisible, so the true count of operating mines is higher than this number. A
rate built this way answers "per entity we can see," which is the honest version
of the question and is a great deal better than no denominator at all.

Two censoring rules carried over: the first year is excluded (everyone is new)
and the last year is excluded (everyone looks like they just left).
"""
import csv
import json
import os

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TI = os.path.join(REPO, "reports", "time_index")

MIN_ENTITIES = 100      # a rate over a handful of entities is noise
MIN_YEARS = 6           # need enough years for a trend to mean anything
MIN_EVENTS = 5000


def load_series_by_year():
    """table -> {year: events}, rolling the count sweep's buckets up to years."""
    out = {}
    path = os.path.join(TI, "series.jsonl")
    if not os.path.exists(path):
        return out
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        if r.get("error") or not r.get("points"):
            continue
        by_year = {}
        for period, n in r["points"]:
            y = str(period)[:4]
            if not y.isdigit():
                continue
            by_year[int(y)] = by_year.get(int(y), 0) + int(n)
        out[r["table"].upper()] = {"column": (r.get("column") or "").upper(),
                                   "years": by_year}
    return out


def load_cohorts():
    """table -> the cohort record, for tables with a usable repeating entity."""
    out = {}
    path = os.path.join(TI, "cohorts.jsonl")
    if not os.path.exists(path):
        return out
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        if r.get("error") or r.get("skipped") or not r.get("curves"):
            continue
        if not r.get("chosen"):
            continue
        out[r["table"].upper()] = r
    return out


def living_curve(rec):
    """year -> entities present that year, from the first-seen/last-seen curves."""
    born = {y: n for y, n, _ in rec["curves"].get("born", [])}
    died = {y: n for y, n, _ in rec["curves"].get("died", [])}
    years = sorted(set(born) | set(died))
    living, alive = {}, 0
    for y in years:
        alive += born.get(y, 0)
        living[y] = alive
        alive -= died.get(y, 0)
    return living


def trend(pairs):
    """Compare the mean of the first three years against the last three."""
    if len(pairs) < 4:
        return None, None, 0.0
    k = min(3, len(pairs) // 2)
    early = sum(v for _, v in pairs[:k]) / k
    late = sum(v for _, v in pairs[-k:]) / k
    if early <= 0:
        return early, late, 0.0
    return early, late, late / early


def _md_table(rows, cols, headers):
    out = ["| " + " | ".join(headers) + " |",
           "|" + "|".join("---" for _ in headers) + "|"]
    for r in rows:
        out.append("| " + " | ".join(
            str(r.get(c) if r.get(c) not in (None, "") else "-").replace("|", "/")
            for c in cols) + " |")
    return "\n".join(out)


def append_findings(rows, mismatched):
    """Append the denominator section to the widened-census write-up.

    Run AFTER score_widened_shapes.py, which rewrites that file from scratch.
    """
    path = os.path.join(TI, "WIDENED_FINDINGS.md")
    if not rows or not os.path.exists(path):
        return
    cols = ["table", "entity_col", "total_events", "population_x", "events_x",
            "rate_x", "verdict"]
    heads = ["table", "entity", "events", "population x", "events x",
             "PER ENTITY x", "verdict"]
    L = ["", "---", "", "## 5. Events per living entity -- the denominator, for free", "",
         "The count sweep's closing line was that no trend here is safe without a",
         "denominator, and that getting one meant a second table per series. For",
         "**{} tables that turned out to be wrong**: where the same entity recurs".format(len(rows)),
         "across years, the population is measurable inside the SAME table. An entity",
         "is present in year Y if it was first seen on or before Y and last seen on",
         "or after Y. Divide the events by that and the question answers itself.", "",
         "This denominator counts entities VISIBLE IN THIS DATASET, which is a proxy",
         "for the real population, not the population. An entity that never appears",
         "is invisible, so the true count is higher. It answers 'per entity we can",
         "see' -- the honest version, and far better than no denominator.", "",
         "{} tables were skipped because the count sweep and the cohort sweep picked".format(mismatched),
         "different clocks, so numerator and denominator would count different years.", ""]

    def bucket(name):
        return [r for r in rows if r["verdict"] == name]

    for title, key, blurb in [
        ("### The rise was really MORE ENTITIES, not more per entity",
         "the rise is MORE ENTITIES, not more per entity",
         "The raw count climbed, and the per-entity rate did not. These are the "
         "cases where a headline number would have been wrong."),
        ("### The fall was really FEWER ENTITIES",
         "the fall is FEWER ENTITIES, not fewer per entity",
         "The raw count dropped because the population shrank, not because each "
         "one is doing less."),
        ("### A flat total hiding a moving rate", "flat total hides a RISING per-entity rate",
         "Nothing looked like it was happening. Per entity, it was."),
        ("### A flat total hiding a falling rate", "flat total hides a FALLING per-entity rate",
         ""),
        ("### The rise SURVIVES the denominator", "rise survives the denominator",
         "Both the total and the per-entity rate moved the same way. These are the "
         "strongest candidates in the warehouse."),
        ("### The fall SURVIVES the denominator", "fall survives the denominator", ""),
        ("### Not interpretable: the denominator is itself a coverage ramp",
         "denominator is a coverage ramp -- not interpretable",
         "The visible population multiplies by more than twenty, which is a dataset "
         "filling in rather than a world of new entities."),
    ]:
        grp = bucket(key)
        if not grp:
            continue
        L += [title, ""]
        if blurb:
            L += [blurb, ""]
        L += [_md_table(sorted(grp, key=lambda r: -r["total_events"])[:15], cols, heads), ""]

    # Slot the section in before the closing caveats, not after the file list.
    body = open(path, encoding="utf-8").read()
    anchor = "## What these four sweeps still cannot do"
    block = "\n".join(L) + "\n\n"
    body = body.replace(anchor, block + anchor, 1) if anchor in body else body + block
    open(path, "w", encoding="utf-8").write(body)


def main():
    series = load_series_by_year()
    cohorts = load_cohorts()
    rows = []
    skipped_clock_mismatch = 0

    for table, rec in cohorts.items():
        ser = series.get(table)
        if not ser:
            continue
        # Both sweeps must have used the SAME clock, or the numerator and the
        # denominator are counting different years.
        if ser["column"] and ser["column"] != (rec.get("clock_col") or "").upper():
            skipped_clock_mismatch += 1
            continue
        living = living_curve(rec)
        events = ser["years"]
        common = sorted(set(living) & set(events))
        if len(common) < MIN_YEARS + 2:
            continue
        # Censoring: drop the first and last year of the population curve.
        common = common[1:-1]
        pairs = [(y, events[y] / living[y]) for y in common
                 if living.get(y, 0) >= MIN_ENTITIES]
        if len(pairs) < MIN_YEARS:
            continue
        total_events = sum(events[y] for y, _ in pairs)
        if total_events < MIN_EVENTS:
            continue

        e_rate, l_rate, rate_mult = trend(pairs)
        pop = [(y, living[y]) for y, _ in pairs]
        e_pop, l_pop, pop_mult = trend(pop)
        ev = [(y, events[y]) for y, _ in pairs]
        e_ev, l_ev, ev_mult = trend(ev)

        # When the visible population multiplies by hundreds, the denominator is
        # itself a coverage ramp -- the dataset filling in, not a world of new
        # entities. A rate built on that is not interpretable either way.
        coverage_ramp = bool(pop_mult and (pop_mult > 20 or pop_mult < 0.05))

        # The whole point: does the raw event trend survive dividing by the
        # population, or was it the population all along?
        verdict = "unclear"
        if coverage_ramp:
            verdict = "denominator is a coverage ramp -- not interpretable"
        elif ev_mult and rate_mult:
            if ev_mult >= 1.5 and rate_mult >= 1.4:
                verdict = "rise survives the denominator"
            elif ev_mult >= 1.5 and rate_mult < 1.2:
                verdict = "the rise is MORE ENTITIES, not more per entity"
            elif ev_mult <= 0.67 and rate_mult <= 0.75:
                verdict = "fall survives the denominator"
            elif ev_mult <= 0.67 and rate_mult > 0.85:
                verdict = "the fall is FEWER ENTITIES, not fewer per entity"
            elif 0.8 <= ev_mult <= 1.25 and rate_mult > 1.4:
                verdict = "flat total hides a RISING per-entity rate"
            elif 0.8 <= ev_mult <= 1.25 and rate_mult < 0.7:
                verdict = "flat total hides a FALLING per-entity rate"

        rows.append({
            "table": table,
            "entity_col": rec.get("chosen"),
            "clock_col": rec.get("clock_col"),
            "first_year": pairs[0][0], "last_year": pairs[-1][0],
            "n_years": len(pairs),
            "total_events": total_events,
            "entities_early": round(e_pop or 0, 1),
            "entities_late": round(l_pop or 0, 1),
            "population_x": round(pop_mult, 2) if pop_mult else None,
            "events_early": round(e_ev or 0, 1),
            "events_late": round(l_ev or 0, 1),
            "events_x": round(ev_mult, 2) if ev_mult else None,
            "rate_early": round(e_rate or 0, 2),
            "rate_late": round(l_rate or 0, 2),
            "rate_x": round(rate_mult, 2) if rate_mult else None,
            "coverage_ramp": coverage_ramp,
            "verdict": verdict,
            "_curve": [(y, round(v, 3)) for y, v in pairs],
        })

    # Rank by how far the per-entity rate moved, in either direction.
    def move(r):
        m = r["rate_x"] or 1.0
        return max(m, 1 / m) if m > 0 else 1.0
    rows.sort(key=lambda r: -move(r))

    cols = [c for c in (rows[0] if rows else {}) if not c.startswith("_")]
    if rows:
        with open(os.path.join(TI, "rate_per_entity.csv"), "w", newline="",
                  encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=cols)
            w.writeheader()
            w.writerows({k: v for k, v in r.items() if not k.startswith("_")}
                        for r in rows)
    json.dump(rows, open(os.path.join(TI, "rate_per_entity.json"), "w"), indent=1)

    append_findings(rows, skipped_clock_mismatch)

    print("RATE PER ENTITY")
    print("  tables with both a count series and a repeating population: {}"
          .format(len(rows)))
    print("  skipped, the two sweeps used different clocks: {}"
          .format(skipped_clock_mismatch))
    buckets = {}
    for r in rows:
        buckets[r["verdict"]] = buckets.get(r["verdict"], 0) + 1
    for k, v in sorted(buckets.items(), key=lambda kv: -kv[1]):
        print("  {:<48} {}".format(k, v))


if __name__ == "__main__":
    main()
