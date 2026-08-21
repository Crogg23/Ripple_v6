"""Layer 2: the moderate tier above "Things You Can Count."

Layer 1 (count_possibilities.py) is every single-table, single-column count.
This is the next step up in query complexity -- still cheap, still mostly
free to generate, but one notch past a bare count:

  1. Two-dimension cross-tabs inside one table, no join: kind by place
     (category x geo), place by year (geo x the table's clock), category by
     category (two category columns against each other). "Mix over time"
     (category x year) already exists in layer 1 and is not repeated here.
  2. A count turned into a share: not "how many are flagged" but "what
     percent are flagged"; not "the top kind" but every kind's percent of
     the total; the same for place; and the duplicate-rate version of
     layer 1's "how many show up more than once" (a straight fix for the
     "top ten is just who's biggest" trap layer 1's footer warns about).
  3. The real joins: layer 1 already flagged ~206 counts as needing two
     tables and wrote the per-key SQL. This regenerates those same pairs as
     one match/no-match overlap query each -- "how many rows really match,
     how many don't" -- ready to run, but NOT run here. See
     run_layer2_joins.py, which is gated behind Chris's go-ahead.

Nothing in THIS script touches the warehouse. Reuses count_possibilities.py's
column classifier and naming helpers rather than re-deriving them, so layer 2
tracks layer 1's judgement calls (what's a category, what's a geo, which
clock to trust) instead of drifting from them.

Output: reports/count_possibilities_layer2.json
"""
from __future__ import annotations

import itertools
import json
import os
import re
import sys
from collections import defaultdict

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(REPO, "scripts", "census"))
sys.path.insert(0, REPO)

import count_possibilities as cp1  # noqa: E402
from count_naming import humanize, plural  # noqa: E402

DB = cp1.DB

# Cross-tab pair caps, tighter than layer 1's own per-role caps (6 cats, 3
# geos), because pairing grows quadratically and a table with 6 categories
# does not need all 15 cat x cat combinations to make the point.
MAX_CATS_FOR_PAIRS = 4
MAX_GEOS_FOR_PAIRS = 2
SHARE_LIMIT = 25


def slug(s: str) -> str:
    return cp1.slug(s)


def build():
    cols, rowcounts, grain, clock = cp1.load()
    timeline = cp1.load_timeline()
    entries, tables = [], []

    for (schema, table), collist in sorted(cols.items()):
        if (schema, table) not in rowcounts:
            continue
        fqn = f"{DB}.{schema}.{table}"
        n_rows = rowcounts[(schema, table)]
        src = table.split("__", 1)[-1]
        desc = cp1.pe.TABLES.get(src.upper())
        what_it_is = desc or "No plain-English description has been written for this dataset yet."
        noun = cp1.row_noun(table, grain.get(table.upper()), desc)
        noun_known = noun != "record"
        nouns = plural(noun)

        collist_pairs = [(name, dtype) for name, dtype, _ in collist]
        roles = defaultdict(list)
        for name, dtype, ordinal in collist:
            roles[cp1.classify(name, dtype)].append((name, dtype))

        cats = roles["category"][:6]
        geos = roles["geo"][:3]
        ck = clock.get(table.upper())
        date_col = ck[0] if ck and ck[1] not in ("not_a_date", "unclear") else None
        if not date_col and roles["date"]:
            date_col = roles["date"][0][0]

        out = []

        def add(kind, question, means, sql, rank=50):
            out.append({"kind": kind, "question": question, "means": means,
                        "sql": sql.strip(), "table": f"{schema}.{table}", "fqn": fqn,
                        "dataset": what_it_is, "subject": schema.replace("_", " ").title(),
                        "rows": n_rows, "noun": noun, "noun_known": noun_known, "rank": rank})

        # ---- 1. cross-tabs -------------------------------------------------
        pair_cats = cats[:MAX_CATS_FOR_PAIRS]
        pair_geos = geos[:MAX_GEOS_FOR_PAIRS]

        for (c_name, c_dt), (g_name, g_dt) in itertools.product(pair_cats, pair_geos):
            c_lab, g_lab = humanize(c_name), humanize(g_name)
            add("Kind by place",
                f"How many {nouns} of each {c_lab}, in each {g_lab}?",
                f"Two dimensions at once: {c_lab} down, {g_lab} across. A pattern that "
                f"only shows up in one place is invisible in the by-kind or by-place "
                f"count alone.",
                f"select {g_name}, {c_name}, count(*) as n\nfrom {fqn}\n"
                f"where {g_name} is not null and {c_name} is not null\n"
                f"group by 1, 2\norder by 1, 3 desc;", rank=100)

        for (c1_name, c1_dt), (c2_name, c2_dt) in itertools.combinations(pair_cats, 2):
            c1_lab, c2_lab = humanize(c1_name), humanize(c2_name)
            add("Category by category",
                f"How many {nouns} at each combination of {c1_lab} and {c2_lab}?",
                f"Crosses two category columns from the same table. Finds pairings that "
                f"a single by-kind count would average away.",
                f"select {c1_name}, {c2_name}, count(*) as n\nfrom {fqn}\n"
                f"where {c1_name} is not null and {c2_name} is not null\n"
                f"group by 1, 2\norder by 3 desc;", rank=105)

        # ---- clock plumbing, same detection rule as layer 1 ----------------
        tl_view = f"{DB}.TIMELINE.{table}" if f"{schema}.{table}" in timeline else None
        raw_date_ok = date_col and any(
            dt.upper() in cp1.DATE_TYPES for nm, dt in collist_pairs if nm.upper() == date_col)
        if tl_view:
            t_from, t_expr = tl_view, "ripple_ts"
        elif raw_date_ok:
            t_from, t_expr = fqn, date_col
        else:
            t_from = t_expr = None

        if t_from:
            for g_name, g_dt in pair_geos:
                g_lab = humanize(g_name)
                add("Place by year",
                    f"How many {nouns} per year, in each {g_lab}?",
                    f"{g_lab} down, year across. A national trend can hide a single "
                    f"{g_lab.rstrip('s')} moving the opposite way; this is the only "
                    f"layer-1-adjacent count that would show it.",
                    f"select {g_name}, year({t_expr}) as yr, count(*) as n\nfrom {t_from}\n"
                    f"where {g_name} is not null and {t_expr} is not null\n"
                    f"group by 1, 2\norder by 1, 2;", rank=110)

        # ---- 2. counts turned into shares -----------------------------------
        for name, dtype in roles["flag"][:3]:
            label = humanize(name)
            add("What percent is flagged",
                f"What percent of {nouns} are marked '{label}'?",
                f"Same split layer 1 counts, plus the percent of the whole each side "
                f"is. Answers 'is this common or rare' without you doing the division.",
                f"select {name},\n       count(*) as n,\n"
                f"       round(100.0 * count(*) / sum(count(*)) over (), 1) as pct_of_total\n"
                f"from {fqn}\ngroup by 1\norder by 2 desc;", rank=120)

        for name, dtype in cats:
            label = humanize(name)
            add("What percent is each kind",
                f"What percent of {nouns} does each {label} account for?",
                f"The same by-kind count as layer 1, with each kind's share of the "
                f"total attached. This is the direct fix for 'the top one is just "
                f"biggest' -- a 90% share and a 9% share are different findings even "
                f"when they're both '#1 by count' in different tables.",
                f"select {name},\n       count(*) as n,\n"
                f"       round(100.0 * count(*) / sum(count(*)) over (), 1) as pct_of_total\n"
                f"from {fqn}\nwhere {name} is not null\n"
                f"group by 1\norder by 2 desc\nlimit {SHARE_LIMIT};", rank=125)

        for name, dtype in geos:
            label = humanize(name)
            add("What percent is each place",
                f"What percent of {nouns} does each {label} account for?",
                f"Same as the by-place count, with each place's share attached. Raw "
                f"counts follow population; a share at least tells you how "
                f"concentrated the total is before you go looking for a real "
                f"per-capita rate.",
                f"select {name},\n       count(*) as n,\n"
                f"       round(100.0 * count(*) / sum(count(*)) over (), 1) as pct_of_total\n"
                f"from {fqn}\nwhere {name} is not null\n"
                f"group by 1\norder by 2 desc\nlimit {SHARE_LIMIT};", rank=130)

        for name, dtype in (roles["id"] + roles["name"])[:6]:
            e_noun = cp1.entity_noun(name, noun)
            if not e_noun:
                continue
            add("What percent repeats",
                f"What percent of {plural(e_noun)} appear more than once?",
                f"The rate version of layer 1's once-vs-repeat split on "
                f"{humanize(name)}. A number close to 0% means the column is a real "
                f"one-per-row key; close to 100% means it's a grouping column and "
                f"any ranking on it is really 'who appears most'.",
                f"with per_{slug(e_noun)} as (\n  select {name}, count(*) as n\n"
                f"  from {fqn}\n  where {name} is not null\n  group by 1\n)\n"
                f"select round(100.0 * count(case when n > 1 then 1 end) "
                f"/ nullif(count(*), 0), 1) as pct_repeating\nfrom per_{slug(e_noun)};", rank=135)

        out.sort(key=lambda e: e["rank"])
        entries.extend(out)
        tables.append({"table": f"{schema}.{table}", "subject": schema.replace("_", " ").title(),
                       "dataset": what_it_is, "noun": noun, "noun_known": noun_known,
                       "rows": n_rows, "n_counts": len(out)})
    return entries, tables


if __name__ == "__main__":
    entries, tables = build()
    out = os.path.join(REPO, "reports", "count_possibilities_layer2.json")
    json.dump({"entries": entries, "tables": tables},
              open(out, "w", encoding="utf-8"), indent=1)
    from collections import Counter
    print(f"{len(entries):,} moderate-tier questions across "
          f"{sum(1 for t in tables if t['n_counts']):,} tables -> {out}")
    for k, n in Counter(e["kind"] for e in entries).most_common():
        print(f"  {n:>6,}  {k}")
