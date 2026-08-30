"""Regenerate reports/JOIN_HANDBOOK.md from the same payload the HTML handbook uses.

Reads the `const DATA = {...}` line out of reports/viz/join_handbook.html (so run
build_join_handbook.py first) and writes the markdown twin. Friendly names, the ID
glossary, and tier wording are mirrored from join_handbook_template.html so the two
files never drift.

    python reports/viz/_build/build_join_handbook.py
    python reports/viz/_build/build_join_handbook_md.py
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

BUILD = Path(__file__).resolve().parent
VIZ = BUILD.parent
REPORTS = VIZ.parent
PAGE = BUILD / "legacy" / "join_handbook_rail.html"  # legacy rail page; the real handbook is built by build_chain_handbook.py
TEMPLATE = BUILD / "join_handbook_template.html"
OUT = REPORTS / "JOIN_HANDBOOK.md"
SNAPSHOT = "2026-08-29"
CSV_NAME = f"handbook_edges_{SNAPSHOT}.csv"

HARD = ("STEEL", "STRONG", "BRIDGE")
TIER_LABEL = {
    "STEEL": "Rock-solid match",
    "STRONG": "Strong code match",
    "BRIDGE": "Different number, known translation",
    "MEASURED": "Measured 2026-08-29, not yet in the spine",
    "GEO": "Same location",
    "SUSPECT": "Suspect -- do not use",
    "CORROBORATED": "Educated guess (name + ZIP)",
}
TIER_ORDER = ["STEEL", "STRONG", "BRIDGE", "MEASURED", "GEO", "SUSPECT"]
PLACE_NOTES: dict | None = None
TIME_NOTES: dict | None = None


# ---------- pull the JS constants out of the template so names stay in sync ----------

def _js_block(template: str, name: str) -> str:
    m = re.search(r"const %s = (\{.*?\n\});" % name, template, re.S)
    if not m:
        raise SystemExit(f"could not find const {name} in template")
    return m.group(1)


def parse_key_info(template: str) -> dict:
    block = _js_block(template, "KEY_INFO")
    out = {}
    for m in re.finditer(r"^\s*'?([A-Z_@~]+)'?:\s*\{\s*name:\s*'((?:[^'\\]|\\.)*)',\s*desc:\s*'((?:[^'\\]|\\.)*)'", block, re.M):
        out[m.group(1)] = dict(name=m.group(2).replace("\\'", "'"), desc=m.group(3).replace("\\'", "'"))
    return out


def parse_agency_map(template: str) -> list[tuple[str, str]]:
    m = re.search(r"const AGENCY_MAP = \[(.*?)\n\];", template, re.S)
    return re.findall(r"\['([^']+)',\s*'((?:[^'\\]|\\.)*)'\]", m.group(1))


def ascii(s: str) -> str:
    return (s.replace("—", "--").replace("–", "-").replace("’", "'").replace("‘", "'")
             .replace("↔", "<->").replace("→", "->").replace("…", "...")
             .replace("&mdash;", "--").replace("&hellip;", "...").replace("&rarr;", "->"))


def make_friendly(agency_map):
    def titled(rest):
        return " ".join(w if (len(w) <= 4 and w == w.upper()) else w[0] + w[1:].lower()
                        for w in rest.split("_") if w)

    def friendly(table):
        for p, label in agency_map:
            if table.startswith(p):
                words = titled(table[len(p):].lstrip("_"))
                return ascii(f"{label}: {words}" if words else label)
        return titled(re.sub(r"^FED_", "", table)) or table
    return friendly


# ---------- rendering ----------

def nf(n):
    return f"{int(n):,}" if n is not None else "n/a"


def edge_line(self, e, key_info, friendly):
    info = key_info.get(e["key"], dict(name=e["key"], desc="a shared identifier"))
    kname = ascii(info["name"]).lower()
    other = e["other"]
    fr = friendly(other)
    e = dict(e, rate=min(100.0, e["rate"] or 0))  # crosswalk edges can exceed 100%; cap like the HTML does
    if e["tier"] == "GEO":
        head = f"- `{other}` ({fr}) -- same location as `{other}`"
    elif e["tier"] == "SUSPECT":
        head = (f"- `{other}` ({fr}) -- **{e['rate']:.0f}%** of the {kname} values also appear in `{other}` "
                f"({nf(e['matched'])} matching) -- **but about half of those pairs are different organizations**")
    else:
        head = f"- `{other}` ({fr}) -- **{e['rate']:.0f}%** of the {kname} values also appear in `{other}` ({nf(e['matched'])} matching)"
    cols = f"`{self}.{e['col_self']}` = `{other}.{e['col_other']}`" if e.get("col_self") and e.get("col_other") else "via a crosswalk table"
    sub = f"  <sub>joins on: {cols} &middot; key: `{e['key']}`</sub>"
    lines = [head, sub]
    if e.get("src") == "pass2":
        extra = f"  <sub>checked {e.get('measured_on', SNAPSHOT)}: {ascii(e.get('verdict', ''))}"
        if e.get("names_pct") is not None:
            extra += f" -- {e.get('pairs')} matched pairs spot-checked: names agree **{e['names_pct']}%**"
            if e.get("states_pct") is not None:
                extra += f", states agree **{e['states_pct']}%**"
        if e.get("note"):
            extra += f" -- {ascii(e['note'])}"
        lines.append(extra + "</sub>")
    return "\n".join(lines)


def table_section(t, edges, key_info, friendly):
    name = t["name"]
    by = {k: [] for k in TIER_ORDER}
    fuzzy = 0
    for e in edges:
        if e["tier"] == "CORROBORATED":
            fuzzy += 1
        elif e["tier"] in by:
            by[e["tier"]].append(e)
    hard = sum(len(by[k]) for k in HARD)
    measured = len(by["MEASURED"])
    geo = len(by["GEO"])
    place = t.get("place") or []
    place_good = [p for p in place if not p.get("trap")]
    clocks = t.get("time") or []
    clocks_good = [c for c in clocks if not c.get("trap")]
    if hard + measured + geo + len(by["SUSPECT"]) + len(place_good) + len(clocks_good) == 0:
        return None
    parts = [f"{hard} reliable connection{'s' if hard != 1 else ''}"]
    if measured:
        parts.append(f"{measured} measured {SNAPSHOT} (not yet in the spine)")
    if geo:
        parts.append(f"{geo} place-based")
    if place_good:
        parts.append(f"{len(place_good)} value-checked place column{'s' if len(place_good) != 1 else ''}")
    if clocks_good:
        parts.append(f"{len(clocks_good)} value-checked clock column{'s' if len(clocks_good) != 1 else ''}")
    summary = ", ".join(parts)
    if fuzzy:
        summary += f" -- plus {fuzzy} low-confidence name+ZIP guess{'es' if fuzzy != 1 else ''} not shown here"
    out = [f"### `{name}`", f"*{friendly(name)}*", "", summary + ".", ""]
    if place:
        axis_tables = ((PLACE_NOTES or {}).get("axis_tables") or {})
        out.append(f"**Meets other tables on place** (columns value-checked {place[0].get('measured_on', '')}):")
        out.append("")
        for p in place:
            partners = max(0, axis_tables.get(p["kind"], 0) - 1)
            flag = "**TRAP** -- " if p.get("trap") else ""
            tail = "" if p.get("trap") else f" -- {partners} other tables carry a clean {ascii(p['label'])}"
            note = f" ({ascii(p['note'])})" if p.get("note") else ""
            out.append(f"- {flag}{ascii(p['label'])}: `{p['column']}` fills {p['fill']:.0f}% of rows, {nf(p.get('distinct'))} distinct -- {ascii(p['verdict'])}{note}{tail}")
        out.append("")
    if clocks:
        grain_tables = ((TIME_NOTES or {}).get("grain_tables") or {})
        best = t.get("clock")
        out.append(f"**Runs on a clock** (date columns value-checked {clocks[0].get('measured_on', '')})" +
                   (f" -- best clock: `{best['column']}`, {ascii(best['label'])}, to the {best['grain']}, {best['lo']} -> {best['hi']}:" if best else ":"))
        out.append("")
        for c in clocks:
            same = max(0, grain_tables.get(c["grain"], 0) - 1)
            flag = "**NOT A CLOCK** -- " if c.get("trap") else ""
            tail = "" if c.get("trap") else f" -- {same} other tables keep a clock to the {c['grain']}"
            desc = f" ({ascii(c['desc'])})" if c.get("desc") else ""
            out.append(f"- {flag}`{c['column']}`: {ascii(c['label'])}, {c['format']}, {c['lo']} -> {c['hi']}, {nf(c.get('rows'))} rows{desc}{tail}")
        out.append("")
    if not edges:
        out += ["*No shared-ID connections measured -- reachable by place and/or time only.*", ""]
        return "\n".join(out)
    if any(e["key"] == "DOCKET" for e in edges):
        out += ["> **Heads up:** this table has a docket / case-number connection, which is currently ~40% wrong. See the warning at the top.", ""]
    for tier in TIER_ORDER:
        lst = by[tier]
        if not lst:
            continue
        if tier != "GEO":
            lst = sorted(lst, key=lambda e: (-(e["rate"] or 0), e["other"]))
        out.append(f"**{TIER_LABEL[tier]}:**")
        out.append("")
        out += [edge_line(name, e, key_info, friendly) for e in lst]
        out.append("")
    return "\n".join(out)


def header(data, key_info, n_tables_listed, n_fuzzy_only, hard_pairs, measured_pairs):
    notes = data.get("notes") or {}
    lines = [
        "# The Join Handbook",
        "",
        "**What this is:** every table in the Ripple warehouse, and every other table it can be joined",
        "to, measured against the live data -- not guessed from column names. Built from the spine's",
        f"own measured-overlap table (`CONNECT_EDGES`), snapshot {SNAPSHOT}, plus the connections pass 2",
        f"measured live on {notes.get('measured_on', SNAPSHOT)} that are not registered in the spine yet.",
        "",
        f"- **{len(data['tables'])} tables** have at least one measured connection.",
        f"- **{hard_pairs:,} reliable connections** (hard ID, strong code, or known translation), each counted once.",
        f"- **{measured_pairs:,} more connections measured {notes.get('measured_on', SNAPSHOT)}** and name-checked, but not yet in the",
        "  spine's edge table -- listed under their own heading on each table so they are never mistaken for spine-verified ones.",
        "- Fuzzy name+ZIP guesses exist for almost every table but are **left out of this file** (mostly noise --",
        "  median match rate across all of them is 0.7%). Full CSV with everything, including those:",
        f"  `reports/{CSV_NAME}`. The pass-2 layer: `reports/viz/_build/handbook_pass2_edges_{SNAPSHOT}.csv`.",
        "",
        "## How to read a connection",
        "",
        "Every line under a table says: **this table** and **that table** both have a column holding the",
        "same kind of ID. The percentage is how many of the ID values in this table actually showed up in",
        "the other one, when checked live -- not a guess.",
        "",
        "## The kinds of connection, most to least sure",
        "",
        "- **Rock-solid match** -- Both tables print the exact same official ID number. As close to certain as it gets.",
        "- **Strong code match** -- Same official code in both tables, but this code system occasionally reuses numbers, so treat as very likely rather than certain.",
        "- **Different number, known translation** -- Two different ID systems for the same kind of thing (e.g. an old ID and its replacement) -- a verified way to translate one into the other.",
        f"- **Measured {SNAPSHOT}, not yet in the spine** -- Same official ID in both tables, overlap measured live, and (where marked SOLID) 60 random matched pairs were checked by name and state. Not yet registered in the spine's edge table, so the spine's own joins don't use them yet.",
        "- **Same location** -- Matched on geography, not on an identity number. Good for \"what else happened near here,\" not \"is this the same org.\"",
        "- **Suspect -- do not use** -- The values overlap, but a name check showed the matched pairs are often different organizations. Listed so nobody rediscovers it; the line says what to use instead.",
        "- **Educated guess (name + ZIP)** -- No shared ID at all -- matched because the name and ZIP look similar. Least reliable by far; most of these are false positives.",
        "",
        "## ID glossary",
        "",
        "| ID | What it actually is |",
        "|---|---|",
    ]
    for k in sorted(key_info, key=lambda k: key_info[k]["name"].lower()):
        lines.append(f"| **{ascii(key_info[k]['name'])}** | {ascii(key_info[k]['desc'])} |")
    lines += [
        "",
        "> **Heads up: docket / case number is currently unreliable.** Bank ID numbers and Supreme Court",
        "> case numbers accidentally look the same, so roughly 4 in 10 of those matches are wrong. Treat",
        "> any DOCKET connection below as unverified until it's fixed.",
        "",
    ]
    if notes.get("corrections"):
        lines += [f"## Corrections carried in from connections pass 2 ({notes.get('measured_on', SNAPSHOT)})", "",
                  "| Earlier claim | What pass 2 found |", "|---|---|"]
        lines += [f"| {ascii(c['was'])} | {ascii(c['now'])} |" for c in notes["corrections"]]
        lines.append("")
    if notes.get("traps"):
        lines += ["## Traps -- read before joining", ""]
        lines += [f"- {ascii(t)}" for t in notes["traps"]]
        lines.append("")
    pl = notes.get("place")
    if pl:
        lines += [f"## Meeting on place -- every place column value-checked {pl['measured_on']}", "",
                  f"Time and place are first-class joins (Chris, 2026-08-29). Every place-shaped column in the warehouse was measured live on "
                  f"{pl['measured_on']} (fill, distinct values, sentinel share, and a shape test per kind). **{pl['tables_with_place']} tables** carry at least "
                  f"one column that really holds a place; **{pl['place_only_tables']}** of them have no shared-ID connection at all and are reachable by "
                  f"place only -- they appear below for the first time. Source: `{pl['source']}`.", "",
                  "| kind of place | tables that carry a clean one |", "|---|---:|"]
        for k, n in pl["axis_tables"].items():
            lines.append(f"| {ascii(pl['axis_label'].get(k, k))} | {n:,} |")
        if pl.get("traps"):
            lines += ["", "Place traps found (marked **TRAP** on the table): " +
                      "; ".join(f"{ascii(k)} ({n})" for k, n in pl["traps"].items()) + "."]
        lines.append("")
    tm = notes.get("time")
    if tm:
        lines += [f"## Meeting on time -- every date column value-checked {tm['measured_on']}", "",
                  f"Every date / month / quarter / year column in the warehouse was value-scanned on {tm['measured_on']} (the time index) and each one "
                  f"was read for what its clock means. **{tm['tables_with_time']} tables** run on a real clock; **{tm['time_only_tables']}** of them have "
                  f"neither a shared-ID connection nor a verified place column. Source: `{tm['source']}`.", "",
                  "| has a clock to the... | tables |", "|---|---:|"]
        for k, n in tm["grain_tables"].items():
            lines.append(f"| {k} | {n:,} |")
        lines += ["", "| what the clock means | tables |", "|---|---:|"]
        for k, n in tm["meaning_tables"].items():
            lines.append(f"| {ascii(tm['meaning_label'].get(k, k))} | {n:,} |")
        if tm.get("traps"):
            lines += ["", "Not clocks (marked **NOT A CLOCK** on the table): " +
                      "; ".join(f"{ascii(tm['meaning_label'].get(k, k))} ({n})" for k, n in tm["traps"].items()) + "."]
        lines.append("")
    lines += [
        "---",
        "",
        "## Tables",
        "",
        "Search this file for a table name (`Ctrl+F` / `grep`), or scan the list below.",
        "",
        f"{n_tables_listed} tables have at least one reliable, measured, or place-based connection and are listed below.",
        f"({n_fuzzy_only} more tables only have fuzzy name+ZIP guesses -- see the CSV.)",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=OUT)
    args = ap.parse_args()

    html = PAGE.read_text(encoding="utf-8")
    i = html.find("const DATA = ")
    data = json.loads(html[i + 13:html.find("\n", i)].rstrip().rstrip(";").replace("<\\/", "</"))
    template = TEMPLATE.read_text(encoding="utf-8")
    key_info = parse_key_info(template)
    key_info.update((data.get("notes") or {}).get("keys", {}))
    friendly = make_friendly(parse_agency_map(template))

    seen_hard, seen_meas = set(), set()
    for self, lst in data["edges"].items():
        for e in lst:
            pair = (tuple(sorted([self, e["other"]])), e["key"], tuple(sorted([e["col_self"] or "", e["col_other"] or ""])))
            if e["tier"] in HARD:
                seen_hard.add(pair)
            elif e["tier"] == "MEASURED":
                seen_meas.add(pair)

    global PLACE_NOTES, TIME_NOTES
    PLACE_NOTES = (data.get("notes") or {}).get("place")
    TIME_NOTES = (data.get("notes") or {}).get("time")
    sections = []
    for t in sorted(data["tables"], key=lambda t: t["name"]):
        s = table_section(t, data["edges"].get(t["name"], []), key_info, friendly)
        if s:
            sections.append(s)
    n_fuzzy_only = len(data["tables"]) - len(sections)

    body = header(data, key_info, len(sections), n_fuzzy_only, len(seen_hard), len(seen_meas))
    body += "\n" + "\n\n".join(sections) + "\n"
    args.out.write_text(body, encoding="utf-8")
    print(f"wrote {args.out}  ({len(body):,} chars, {len(sections)} tables listed, "
          f"{len(seen_hard):,} reliable + {len(seen_meas):,} measured-not-in-spine pairs)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
