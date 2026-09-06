"""Build INDEX.md from each folder's findings.md HEADLINE/STATUS lines."""
import re, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
H = json.load(open(ROOT/'_shared/hunches.json'))
order = ['2','5','15','22','23','27','30','31','E38','E39','E40','E41','E42','E43','E44','E47','E48','E49','E57','E62','E68']
rows = []
for k in order:
    d = next(p for p in ROOT.iterdir() if p.is_dir() and (p.name.split('_')[0].lstrip('0') == k or p.name.split('_')[0] == k))
    f = (d/'findings.md').read_text()
    head = re.search(r'^\**HEADLINE:?\**:?\s*(.+)$', f, re.M).group(1).strip().strip('*')
    stat = re.search(r'^\**STATUS:?\**:?\s*(.+)$', f, re.M).group(1).strip().strip('*')
    q = re.match(r'### \S+\. (.*)', H[k]).group(1)
    rows.append((k, q, stat, head, d.name))
counts = {}
for r in rows: counts[r[2]] = counts.get(r[2], 0) + 1
out = ["# Tier 1 deep dive, 2026-09-05", "",
       "21 hunches. Each folder: story.html, findings.md, queries.py, queries.log.",
       "Every folder had a fresh-context skeptic pass; fixes applied before this index was cut.", "",
       "| status | count |", "|---|---|"] + [f"| {s} | {n} |" for s, n in sorted(counts.items())] + [""]
for k, q, stat, head, name in rows:
    out += [f"## {k}. {q}", f"- **{stat}**", f"- {head}", f"- [story]({name}/story.html) · [findings]({name}/findings.md)", ""]
(ROOT/'INDEX.md').write_text("\n".join(out))
print("\n".join(f"{k:4} {stat:28} {head[:90]}" for k,q,stat,head,name in rows))
