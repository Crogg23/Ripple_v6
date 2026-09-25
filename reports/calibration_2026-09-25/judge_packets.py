"""Build one blind packet per story for the judge.

The packet holds the frozen lead and the sources' quotes, outlets, dates and quote-check status.
It drops the searcher's own notes, so the judge never sees the searcher's opinion.
Usage: python judge_packets.py [S001 ...]   (no args = every searched story)
"""
import csv, hashlib, json, re, sys
from pathlib import Path

HERE = Path(__file__).parent
stories = {r["story_id"]: r for r in csv.DictReader(open(HERE / "stories.tsv", encoding="utf-8"), delimiter="\t")}
qc = {}
if (HERE / "quotecheck.tsv").exists():
    for r in csv.DictReader(open(HERE / "quotecheck.tsv", encoding="utf-8"), delimiter="\t"):
        qc[(r["story_id"], int(r["idx"]))] = r["status"]

def context(url, quote, width=300):
    """About 300 characters either side of the quote, from the cached page text."""
    f = HERE / "pages" / (hashlib.sha1(url.encode()).hexdigest()[:16] + ".txt")
    if not f.exists():
        return ""
    text = re.sub(r"\s+", " ", f.read_text(encoding="utf-8"))
    toks = re.findall(r"[a-z]+|[0-9]+", quote.lower().replace("’", "").replace("'", ""))
    for n in (6, 4, 3):
        if len(toks) >= n:
            m = re.search(r"[^a-z0-9]*".join(map(re.escape, toks[:n])), text, re.I)
            if m:
                return text[max(0, m.start() - width): m.end() + len(quote) + width]
    return ""

out = HERE / "judge" / "packets"
out.mkdir(parents=True, exist_ok=True)
ids = set(sys.argv[1:])
for f in sorted((HERE / "search").glob("S*.json")):
    if ids and f.stem not in ids:
        continue
    d = json.loads(f.read_text(encoding="utf-8"))
    s = stories[d["story_id"]]
    packet = {
        "story_id": s["story_id"],
        "lead": {k: s[k] for k in ["headline", "number", "grade", "verdict", "watch_out"]},
        "queries_logged": len(d.get("queries", [])),
        "queries": [q["q"] for q in d.get("queries", [])],
        "sources": [
            {"idx": i, "url": src["url"], "outlet": src.get("outlet", ""), "date": src.get("date", "unknown"),
             "source_type": src.get("source_type", ""), "entity_named": src.get("entity_named", ""),
             "quote": src.get("quote", ""), "paywalled": src.get("paywalled", False),
             "quote_check": qc.get((d["story_id"], i), "not run"),
             "page_context": context(src["url"], src.get("quote", ""))
             if qc.get((d["story_id"], i)) in ("exact", "near") else ""}
            for i, src in enumerate(d.get("sources", []))
        ],
    }
    (out / f"{s['story_id']}.json").write_text(json.dumps(packet, indent=1, ensure_ascii=False), encoding="utf-8")
    print(s["story_id"], len(packet["sources"]), "sources")
