"""Freeze the 239 leads into stories before any press search.

Reads reports/coverage_2026-09-24/LEADS.md, resolves every "Same story as" link,
folds linked leads into one story, and writes leads.tsv and stories.tsv here.
Novelty is the guess made before any search: 1 = famous story, 5 = nobody has it.
"""
import csv, hashlib, re
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE.parent / "coverage_2026-09-24"
text = (SRC / "LEADS.md").read_text(encoding="utf-8")

# deep pass 3 menu: rank -> novelty
d3_novelty = {}
for line in (SRC / "deep3" / "MENU.md").read_text(encoding="utf-8").splitlines():
    m = re.match(r"\|\s*=?\s*(\d+)\s*\|\s*#(\d+) g\d+\s*\|[^|]*\|[^|]*\|\s*(\d)\s*\|\s*(\d)\s*\|", line)
    if m:
        d3_novelty[int(m.group(2))] = int(m.group(4))

sections = [(m.start(), m.group(1)) for m in re.finditer(r"^## (Join dossiers|The full menu|Deep pass 3, graded B|Deep pass 3, graded C or D)", text, re.M)]
def section_of(pos):
    name = None
    for start, s in sections:
        if start <= pos:
            name = s
    return {"Join dossiers": "dossier", "The full menu": "menu",
            "Deep pass 3, graded B": "deep3", "Deep pass 3, graded C or D": "deep3cd"}[name]

def field(body, name):
    m = re.search(r"^- \*\*" + re.escape(name) + r":\*\*\s*(.*)$", body, re.M)
    return m.group(1).strip() if m else ""

leads = []
for m in re.finditer(r"^### (\d+)\. (.*)$", text, re.M):
    end = text.find("\n### ", m.end())
    body = text[m.end(): end if end != -1 else len(text)]
    lid, head = int(m.group(1)), m.group(2).strip()
    grade_line = field(body, "Grade")
    sec = section_of(m.start())
    aliases = set()
    if (j := re.search(r"dossier (j\d)", grade_line)):
        aliases.add(("dossier", j.group(1)))
    if (n := re.search(r"menu #(\d+)", grade_line)):
        aliases.add(("menu", n.group(1)))
    if (f := re.search(r"\b(F-\d+)", grade_line)):
        aliases.add(("menuF", f.group(1)))
    if (d := re.search(r"deep pass 3 #(\d+)", grade_line)):
        aliases.add(("deep3", d.group(1)))
    nov = ""
    if (s := re.search(r"novelty (\d)", grade_line)):
        nov = s.group(1)
    elif (d := re.search(r"deep pass 3 #(\d+)", grade_line)) and int(d.group(1)) in d3_novelty:
        nov = str(d3_novelty[int(d.group(1))])
    letter = re.match(r"([ABCD])\b", grade_line)
    verdict = re.search(r"\b(confirmed|narrowed|unchecked|broken)\b", grade_line)
    leads.append(dict(
        lead_id=lid, section=sec, headline=head,
        number=field(body, "The number"), tables=field(body, "Tables"),
        joined_on=field(body, "Joined on"), grade_line=grade_line,
        grade=letter.group(1) if letter else "", verdict=verdict.group(1) if verdict else "",
        novelty=nov, watch_out=field(body, "Watch out"),
        same_story=field(body, "Same story as"), aliases=aliases,
        cites_press=bool(re.search(r"press reports?|already news|well covered|famous|ProPublica|New York Times|Washington Post", body, re.I))))

by_alias = {}
for L in leads:
    for a in L["aliases"]:
        by_alias[a] = L["lead_id"]

parent = {L["lead_id"]: L["lead_id"] for L in leads}
def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x
def union(a, b):
    parent[find(a)] = find(b)

unresolved = []
for L in leads:
    s = L["same_story"]
    if not s:
        continue
    refs = []
    refs += [("dossier", j) for j in re.findall(r"dossier (j\d)", s)]
    refs += [("menuF", f) for f in re.findall(r"\b(F-\d+)", s)]
    refs += [("menu", n) for n in re.findall(r"menu #(\d+)", s)]
    refs += [("deep3", n) for n in re.findall(r"deep(?: pass )?3 #(\d+)", s)]
    refs += [("deep3", n) for n in re.findall(r"deep3 #\d+ and #(\d+)", s)]
    # bare "#N" means the lead's own section numbering
    bare = re.sub(r"(menu|deep pass 3|deep3|dossier)\s*#?\w+", "", s)
    bare = re.sub(r"deep3 #\d+ and #\d+", "", bare)
    local = {"menu": "menu", "deep3": "deep3", "deep3cd": "deep3", "dossier": "menu"}[L["section"]]
    refs += [(local, n) for n in re.findall(r"#(\d+)", bare)]
    for r in refs:
        if r in by_alias:
            union(L["lead_id"], by_alias[r])
        else:
            unresolved.append((L["lead_id"], r))

groups = {}
for L in leads:
    groups.setdefault(find(L["lead_id"]), []).append(L)

# the top-3 brief searched the press for these leads on 2026-09-24, before this freeze
PRE_SEARCHED = {1, 2, 7}

rank = {"A": 0, "B": 1, "C": 2, "D": 3, "": 4}
stories = []
for members in groups.values():
    members.sort(key=lambda L: (rank[L["grade"]], L["lead_id"]))
    stories.append(members)
stories.sort(key=lambda ms: min(L["lead_id"] for L in ms))

with open(HERE / "stories.tsv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh, delimiter="\t")
    w.writerow(["story_id", "lead_ids", "primary_lead", "headline", "number", "grade", "verdict",
                "novelty_guess", "pre_known", "sections", "tables", "watch_out", "frozen_sha1"])
    for i, ms in enumerate(stories, 1):
        p = ms[0]
        novs = [int(L["novelty"]) for L in ms if L["novelty"]]
        row = [f"S{i:03d}", ",".join(str(L["lead_id"]) for L in sorted(ms, key=lambda L: L["lead_id"])),
               p["lead_id"], p["headline"], p["number"], p["grade"], p["verdict"],
               min(novs) if novs else "",
               "press_checked_2026-09-24" if any(L["lead_id"] in PRE_SEARCHED for L in ms)
               else "lead_cites_press" if any(L["cites_press"] for L in ms) else "",
               ",".join(sorted({L["section"] for L in ms})),
               p["tables"], p["watch_out"]]
        row.append(hashlib.sha1("\t".join(map(str, row)).encode()).hexdigest()[:12])
        w.writerow(row)

with open(HERE / "leads.tsv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh, delimiter="\t")
    w.writerow(["lead_id", "story_id", "section", "grade", "verdict", "novelty_guess", "headline"])
    sid = {L["lead_id"]: f"S{i:03d}" for i, ms in enumerate(stories, 1) for L in ms}
    for L in sorted(leads, key=lambda L: L["lead_id"]):
        w.writerow([L["lead_id"], sid[L["lead_id"]], L["section"], L["grade"], L["verdict"], L["novelty"], L["headline"]])

print("leads", len(leads), "stories", len(stories))
print("multi-lead stories", sum(1 for ms in stories if len(ms) > 1))
print("with novelty guess", sum(1 for ms in stories if any(L["novelty"] for L in ms)))
print("unresolved refs", unresolved)
print("pre_known", sum(1 for ms in stories if any(L["lead_id"] in PRE_SEARCHED or L["cites_press"] for L in ms)))
