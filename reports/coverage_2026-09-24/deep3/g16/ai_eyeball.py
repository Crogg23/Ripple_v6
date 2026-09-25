"""Eyeball the CA 'AI' matches on the local raw CAL-ACCESS cover file (no warehouse statement).

Same rules as q16: F635, latest amendment per filing, period year from FROM_DATE.
Writes g16/ai_eyeball.json and prints a summary.
"""
import csv
import json
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

csv.field_size_limit(10**9)
SRC = Path(__file__).resolve().parents[4] / "library-onboarding/raw_downloads/ca_lobby/CVR_LOBBY_DISCLOSURE_CD.TSV"
HERE = Path(__file__).resolve().parent

RX = re.compile(r"(^|[^A-Za-z])AI([^A-Za-z]|$)")
PH = re.compile(r"artificial intelligence", re.I)
SB = re.compile(r"SB ?1047", re.I)
AD = re.compile(r"automated decision", re.I)

latest = {}
with SRC.open(encoding="utf-8", errors="replace", newline="") as fh:
    rd = csv.reader(fh, delimiter="\t", quoting=csv.QUOTE_NONE)
    head = next(rd)
    ix = {k: i for i, k in enumerate(head)}
    for row in rd:
        if len(row) < len(head) or row[ix["FORM_TYPE"]] != "F635":
            continue
        try:
            am = int(row[ix["AMEND_ID"]])
        except ValueError:
            continue
        fid = row[ix["FILING_ID"]]
        if fid not in latest or am > latest[fid][0]:
            latest[fid] = (am, row)

per_year = defaultdict(lambda: defaultdict(set))
hits = []
for fid, (am, row) in latest.items():
    try:
        y = datetime.strptime(row[ix["FROM_DATE"]].split(" ")[0], "%m/%d/%Y").year
    except ValueError:
        continue
    if y < 2019 or y > 2026:
        continue
    act = row[ix["LBY_ACTVTY"]]
    filer = row[ix["FILER_ID"]]
    kinds = []
    if PH.search(act):
        kinds.append("phrase")
    if SB.search(act):
        kinds.append("sb1047")
    if AD.search(act):
        kinds.append("adt")
    if RX.search(act):
        kinds.append("rx")
    if not kinds:
        continue
    for k in kinds:
        per_year[y][k].add(filer)
    per_year[y]["any"].add(filer)
    m = RX.search(act) if kinds == ["rx"] else None
    snip = act[max(0, m.start() - 70): m.end() + 40] if m else act[:160]
    hits.append({"y": y, "filer": filer, "name": row[ix["FILER_NAML"]], "kinds": kinds, "snip": snip})

summary = {y: {k: len(v) for k, v in d.items()} for y, d in sorted(per_year.items())}
rx_only = [h for h in hits if h["kinds"] == ["rx"]]
(HERE / "ai_eyeball.json").write_text(json.dumps({"summary": summary, "rx_only": rx_only, "hits": hits}, indent=1), encoding="utf-8")
print("filings F635 latest:", len(latest))
for y, d in summary.items():
    print(y, d)
print("rx-only hits:", len(rx_only))
for h in rx_only[:60]:
    print(h["y"], "|", h["name"][:40], "|", h["snip"].replace("\n", " "))
