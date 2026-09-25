"""Tally the judges' bins: hit rate, value added, blind hits, and the novelty test.

Reads judge/S*.json, stories.tsv and the search files. Prints the tables and writes scores.tsv.
Usage: python score.py [pilot] [judge_v2]   (pilot = only pilot stories; judge_v2 = read that folder)
"""
import csv, json, sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).parent
stories = {r["story_id"]: r for r in csv.DictReader(open(HERE / "stories.tsv", encoding="utf-8"), delimiter="\t")}
lead_novelty = {r["lead_id"]: r["novelty_guess"] for r in csv.DictReader(open(HERE / "leads.tsv", encoding="utf-8"), delimiter="\t")}
CONTROLS = {"S001", "S007"}
only = None
if "pilot" in sys.argv[1:]:
    only = {r["story_id"] for r in csv.DictReader(open(HERE / "pilot.tsv", encoding="utf-8"), delimiter="\t")}

BINS = ["Matched", "Matched + more", "Contradicted", "Not comparable", "Known pattern", "Unreported", "Insufficient search"]
MATCH = {"Matched", "Matched + more"}

JDIR = next((a for a in sys.argv[1:] if a.startswith("judge")), "judge")
rows = []
for f in sorted((HERE / JDIR).glob("S*.json")):
    j = json.loads(f.read_text(encoding="utf-8"))
    sid = j["story_id"]
    if only and sid not in only:
        continue
    s = stories[sid]
    src = json.loads((HERE / "search" / f"{sid}.json").read_text(encoding="utf-8"))
    types = {src["sources"][i].get("source_type", "") for i in j.get("deciding_sources", []) if i < len(src["sources"])}
    rows.append(dict(story_id=sid, bin=j["bin"], confidence=j.get("confidence", ""),
                     novelty=lead_novelty.get(s["primary_lead"], "") or "none", grade=s["grade"] or s["verdict"],
                     pre_known="control" if sid in CONTROLS else (s["pre_known"] or "blind"), post_cutoff=j.get("post_cutoff_match", False),
                     earliest=j.get("earliest_match_date", ""), news_match=j["bin"] in MATCH and bool(types & {"news", "trade press"}),
                     deciding_types=",".join(sorted(types)), what_we_add=j.get("what_we_add", ""),
                     headline=s["headline"][:90]))

n = len(rows)
print(f"stories judged: {n}\n")
c = Counter(r["bin"] for r in rows)
print("BIN                  COUNT")
for b in BINS:
    if c[b]:
        print(f"{b:<20} {c[b]:>5}")
m = sum(c[b] for b in MATCH)
print(f"\nhit rate, any source  {m}/{n}")
print(f"hit rate, news only   {sum(r['news_match'] for r in rows)}/{n}")
blind_rows = [r for r in rows if r["pre_known"] == "blind"]
print(f"hit rate, blind       {sum(r['bin'] in MATCH for r in blind_rows)}/{len(blind_rows)}  not pre-known, not a control")
print(f"value added           {c['Matched + more']}/{m} of matches carry a number the press lacks" if m else "")
blind = [r for r in rows if r["bin"] in MATCH and r["earliest"] > "2026-06-30" and r["pre_known"] == "blind"]
late = [r for r in rows if r["bin"] in MATCH and r["post_cutoff"]]
print(f"blind hits            {len(blind)}  earliest match dated after 2026-06-30, story not pre-known")
print(f"late coverage         {len(late)}  matches with any matching source after 2026-06-30")

print("\nNOVELTY GUESS vs BIN   1 = famous, 5 = nobody has it")
grid = defaultdict(Counter)
for r in rows:
    grid[r["novelty"]][r["bin"]] += 1
short = {"Matched": "match", "Matched + more": "m+more", "Contradicted": "contra", "Not comparable": "n/c",
         "Known pattern": "pattern", "Unreported": "unrep", "Insufficient search": "insuff"}
print("guess " + " ".join(f"{short[b]:>8}" for b in BINS))
for g in sorted(grid):
    print(f"{g:<5} " + " ".join(f"{grid[g][b]:>8}" for b in BINS))

# judge agreement: same story judged in both folders
other = "judge" if JDIR != "judge" else "judge_v2"
pairs = []
for r in rows:
    f = HERE / other / f"{r['story_id']}.json"
    if f.exists():
        pairs.append((r["story_id"], json.loads(f.read_text(encoding="utf-8"))["bin"], r["bin"]))
if pairs:
    same = [p for p in pairs if p[1] == p[2]]
    print(f"\njudge agreement, {other} vs {JDIR}: {len(same)}/{len(pairs)}")
    for sid, a, b in pairs:
        if a != b:
            print(f"  {sid}: {a} -> {b}")

with open(HERE / (f"scores_pilot_{JDIR}.tsv" if only else f"scores_{JDIR}.tsv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), delimiter="\t")
    w.writeheader()
    w.writerows(sorted(rows, key=lambda r: r["story_id"]))
