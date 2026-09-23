"""One note card per docket idea, sorted so the easiest joins come first."""
import csv, re

DAY = "2026-09-22"
GRADE_ORDER = ["A measured", "A measured +gap", "B hard ID", "B hard ID +gap",
               "C geo", "C geo +gap", "D name match", "D name match +gap",
               "single table", "E no shared key"]
STATUS_ORDER = ["not started", "found a little", "part done", "missing a piece",
                "found something", "same as another", "nothing there"]

def load(p):
    with open(p, encoding="utf-8") as f:
        return {r["id"]: r for r in csv.DictReader(f)}

deck = load("docket/docket.csv")
join = load(f"docket/docket_join_plan_{DAY}.csv")
tmap = load(f"docket/docket_table_map_{DAY}.csv")

def short(t):
    return t.split(".")[-1].strip()

def rank(i):
    j = join.get(i, {})
    g = j.get("join_grade", "")
    s = j.get("status", "")
    gi = GRADE_ORDER.index(g) if g in GRADE_ORDER else 99
    si = STATUS_ORDER.index(s) if s in STATUS_ORDER else 99
    m = re.match(r'^(\D*)(\d+)$', i)
    return (gi, si, m.group(1) if m else i, int(m.group(2)) if m else 0)

ids = sorted(deck, key=rank)

out = [f"# Docket note cards — {len(ids)} ideas", "",
       "Sorted easiest-join first. Grade A joins are measured, real, counted.",
       "Grade E has no shared key — those need a bridge or a new idea.", "", "---", ""]

# index
out += ["## The deck at a glance", "",
        "| # | grade | status | family | question |", "|---|---|---|---|---|"]
for i in ids:
    d, j = deck[i], join.get(i, {})
    q = d["question"].replace("|", "/")[:70]
    out.append(f"| {i} | {j.get('join_grade','')} | {j.get('status','')} | {j.get('family','')} | {q} |")
out += ["", "---", ""]

for i in ids:
    d, j, t = deck[i], join.get(i, {}), tmap.get(i, {})
    out += [f"## {i}. {d['title']}", "",
            f"**Ask** — {d['question']}",
            f"**Why** — {d['why_it_matters']}",
            "",
            "| field | value |", "|---|---|",
            f"| grade | {j.get('join_grade','')} |",
            f"| status | {d['where_it_stands']} |",
            f"| family | {j.get('family','')} |",
            f"| rows | {d['rows']} |",
            f"| live tables | {t.get('tables_with_live_rows','')} of {t.get('n_tables','')} |",
            f"| window | {d['time_window']} |",
            f"| effort | {d['effort']} |",
            ""]
    out.append("**Tables**")
    for tb in d["tables"].split("|"):
        if tb.strip():
            out.append(f"- `{tb.strip()}`")
    out.append("")
    plan = j.get("join_plan", "").strip()
    if plan:
        out += ["**Join on**", "```"]
        out += [p.strip() for p in plan.split(";") if p.strip()]
        out += ["```", ""]
    for label, key in [("Bridge needed", "bridge_needed"), ("No key between", "no_key_pairs"),
                       ("Note", "manual_note")]:
        v = j.get(key, "").strip()
        if v:
            out += [f"**{label}** — {v}", ""]
    filt = j.get("filter_columns", "").strip()
    if filt:
        out += ["**Filter columns**", "```"]
        out += [c.strip() for c in filt.split("|") if c.strip()]
        out += ["```", ""]
    if d.get("watch_out", "").strip():
        out += [f"**Watch out** — {d['watch_out'].strip()}", ""]
    if d.get("needs", "").strip():
        out += [f"**Needs** — {d['needs'].strip()}", ""]
    if d.get("probe", "").strip():
        out += ["**Probe**", "```sql", d["probe"].strip(), "```", ""]
    out += ["---", ""]

path = f"reports/docket_notecards_{DAY}.md"
with open(path, "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print(path, len(ids), "cards")
