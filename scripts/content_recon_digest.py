"""Read every content-recon JSON and write one digest: what the warehouse says.

Sections, each a plain list, biggest first:
  coverage      how many tables answered each atom
  money         top tables by dollar sum, with their main amount column
  weird max     amount columns where max dwarfs the 99th percentile
  spikes        year curves where one year is 3x its neighbours
  cliffs        year curves that stop dead before 2024
  same name     top-20 names that show up in the most tables (gen 3 preview, local only)
  errors        columns the probe could not read

Output: reports/recon/content/DIGEST.md
"""
from __future__ import annotations
import json, re
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "reports" / "recon" / "content"
JSON_DIR = OUT / "json"
AUDIT = re.compile(r"INGEST|LOADED|_AT$|RUN_ID|SHA", re.I)


def fmt(x):
    if x is None:
        return "-"
    a = abs(x)
    if a >= 1e12: return f"{x/1e12:.2f}T"
    if a >= 1e9: return f"{x/1e9:.2f}B"
    if a >= 1e6: return f"{x/1e6:.2f}M"
    if a >= 1e3: return f"{x/1e3:.1f}K"
    return f"{x:,.0f}"


def main():
    R = [json.loads(p.read_text(encoding="utf-8")) for p in sorted(JSON_DIR.glob("*.json"))]
    L = [f"# Content recon digest — {len(R)} tables", ""]

    # coverage
    cov = Counter()
    for r in R:
        for atom, key in (("when", "when"), ("how big", "how_big"), ("who", "who"), ("who x when", "who_x_when"), ("where", "where"), ("what", "what")):
            if r.get(key):
                cov[atom] += 1
    cov["portal tables"] = sum(1 for r in R if r["table"].startswith("PORTAL"))
    cov["portal at 10,000 cap"] = sum(1 for r in R if r["table"].startswith("PORTAL") and r["rows"] == 10000)
    L += ["## coverage", "", "| atom | tables answering |", "|---|---|"]
    L += [f"| {k} | {v} |" for k, v in cov.most_common()]
    L.append("")

    # money
    money = []
    for r in R:
        for col, s in r.get("how_big", {}).items():
            if s.get("sum") and not AUDIT.search(col) and not r["profile"].get(col, {}).get("date_fmt"):
                money.append((abs(s["sum"]), r["table"], col, s))
    money.sort(reverse=True)
    L += ["## largest numeric sums — top 40; shares, pounds, and daily balances included, not all dollars", "", "| table | column | sum | n | median | p99 | max |", "|---|---|---|---|---|---|---|"]
    for _, t, col, s in money[:40]:
        L.append(f"| {t} | {col} | {fmt(s['sum'])} | {fmt(s['n'])} | {fmt(s['median'])} | {fmt(s['p99'])} | {fmt(s['max'])} |")
    L.append("")

    # weird max
    weird = []
    for r in R:
        for col, s in r.get("how_big", {}).items():
            if s.get("p99") and s.get("max") and s["p99"] > 0 and s["max"] / s["p99"] >= 1000 and (s.get("n") or 0) >= 1000 and not AUDIT.search(col):
                weird.append((s["max"] / s["p99"], r["table"], col, s))
    weird.sort(reverse=True)
    L += ["## weird max — max is 1,000x the 99th percentile or more", "", "| table | column | max | p99 | ratio | n |", "|---|---|---|---|---|---|"]
    for ratio, t, col, s in weird[:40]:
        L.append(f"| {t} | {col} | {fmt(s['max'])} | {fmt(s['p99'])} | {fmt(ratio)}x | {fmt(s['n'])} |")
    L.append("")

    # spikes and cliffs
    spikes, cliffs = [], []
    for r in R:
        for col, hist in r.get("when", {}).items():
            if AUDIT.search(col) or len(hist) < 4:
                continue
            h = {y: n for y, n in hist if 1990 <= y <= 2026}
            if len(h) < 4:
                continue
            ys = sorted(h)
            for i, y in enumerate(ys[1:-1], 1):
                a, b = h[ys[i - 1]], h[ys[i + 1]]
                if h[y] >= 10000 and h[y] >= 3 * max(a, b, 1):
                    spikes.append((h[y] / max(a, b, 1), r["table"], col, y, h[y], a, b))
            last = ys[-1]
            if last <= 2022 and r["rows"] >= 10000 and h[last] >= 0.05 * max(h.values()):
                cliffs.append((r["rows"], r["table"], col, ys[0], last))
    spikes.sort(reverse=True)
    cliffs.sort(reverse=True)
    L += ["## spikes — one year at least 3x both neighbours", "", "| table | column | year | rows | year before | year after |", "|---|---|---|---|---|---|"]
    for _, t, col, y, n, a, b in spikes[:40]:
        L.append(f"| {t} | {col} | {y} | {fmt(n)} | {fmt(a)} | {fmt(b)} |")
    L.append("")
    L += ["## cliffs — the curve stops before 2023, table over 10K rows", "", "| table | column | first year | last year | rows |", "|---|---|---|---|---|"]
    for rows, t, col, y0, y1 in cliffs[:40]:
        L.append(f"| {t} | {col} | {y0} | {y1} | {fmt(rows)} |")
    L.append("")

    # same name across tables
    seen = defaultdict(set)
    for r in R:
        if r["table"].startswith("PORTAL"):
            continue
        for col, d in r.get("who", {}).items():
            if re.search(r"CITY|COUNTY|FIRST|LAST|MIDDLE|STREET|ADDR|STATE|COUNTRY|TITLE|TYPE|DESC", col, re.I):
                continue
            for v, _ in d.get("by_rows", []):
                k = re.sub(r"[^A-Z0-9 ]", "", v.upper()).strip()
                k = re.sub(r"\s+", " ", k)
                if len(k) >= 8 and " " in k and not k.isdigit() and not k.startswith("SUITE"):
                    seen[k].add(r["table"])
    multi = sorted(((len(t), k, t) for k, t in seen.items() if len(t) >= 3), reverse=True)
    L += ["## same name, many tables — a top-20 name seen in 3+ non-portal tables", "", "| name | tables | where |", "|---|---|---|"]
    for n, k, t in multi[:60]:
        L.append(f"| {k[:50]} | {n} | {', '.join(sorted(t))[:160]} |")
    L.append("")

    # errors
    errs = [(r["table"], k, v) for r in R for k, v in (r.get("errors") or {}).items()]
    L += [f"## errors — {len(errs)} columns the probe could not read", ""]
    for t, k, v in errs[:60]:
        L.append(f"- {t}.{k}: {v[:100]}")
    L.append("")
    (OUT / "DIGEST.md").write_text("\n".join(L), encoding="utf-8")
    print(f"digest: {len(R)} tables, money {len(money)}, weird {len(weird)}, spikes {len(spikes)}, cliffs {len(cliffs)}, multi-names {len(multi)}, errors {len(errs)}")


if __name__ == "__main__":
    main()
