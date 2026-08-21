"""Build the plain-English 'what could I chart over time' list.

One page, one list. Every dataset in the warehouse that can be put on a time axis
today, described in words a stranger would understand, with the sixteen worth
starting on pulled to the top.

Inputs (all local, no warehouse compute):
  reports/_trend_list.json   -- 403 datasets, measured from the shared timeline
  reports/_trend_picks.json  -- the hand-written 'why this one' lines
Output:
  reports/time_index/trend_list.html
"""
import html
import json
import os

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

THEME_ORDER = [
    "Health & medicine", "Money & markets", "Courts & policing", "Land, water & air",
    "Politics & influence", "Consumer harm", "Work & workers", "Companies & contracts",
    "Homes & mortgages", "Borders & schools", "Records & reference",
]

GRAIN_WORDS = {"day": "to the day", "month": "to the month",
               "quarter": "to the quarter", "year": "year only"}
CLOCK_WORDS = {"happened": "when it happened", "reported": "when it was reported",
               "decided": "when it was decided", "span_start": "start of a period",
               "span_end": "end of a period"}

e = html.escape


def meta_strip(r):
    bits = ["{}&ndash;{}".format(r["y0"], r["y1"])]
    if r["years"] >= 2:
        bits.append("{} yrs".format(r["years"]))
    bits.append("{:,} dated rows".format(r["dated"]))
    bits.append(GRAIN_WORDS[r["grain"]])
    bits.append(CLOCK_WORDS.get(r["clock"], r["clock"]))
    return ' <span class="dot">&middot;</span> '.join(bits)


def flags(r):
    out = []
    if r["fill"] is not None and r["fill"] < 60 and r["table_rows"] > 10000:
        out.append('<span class="flag">only {:g}% of rows carry this date</span>'.format(r["fill"]))
    if r["grain"] == "year":
        out.append('<span class="flag">year only &mdash; every record lands on 1 January</span>')
    if r["years"] < 2:
        out.append('<span class="flag">under two years &mdash; a snapshot, not a trend</span>')
    return "".join(out)


def row(r, why=None):
    search = (r["name"] + " " + r["what"] + " " + r["subject"]).lower()
    why_html = '<p class="why">{}</p>'.format(e(why)) if why else ""
    return (
        '<article class="row" data-theme-group="{group}" data-search="{search}">'
        '<h3>{name}</h3>'
        '<p class="what">{what}</p>'
        '{why}'
        '<p class="meta">{meta}</p>'
        '<p class="shape">{shape}</p>'
        '{flags}'
        '</article>'
    ).format(group=e(r["theme"]), search=e(search), name=e(r["name"]),
             what=e(r["what"]), why=why_html, meta=meta_strip(r),
             shape=e(r["shape"]), flags=flags(r))


def build():
    recs = json.load(open(os.path.join(REPO, "reports", "_trend_list.json"), encoding="utf-8"))
    picks = json.load(open(os.path.join(REPO, "reports", "_trend_picks.json"), encoding="utf-8"))

    picks_html = "".join(row(p["rec"], p["why"]) for p in picks)

    groups_html = []
    for theme in THEME_ORDER:
        rows = [r for r in recs if r["theme"] == theme]
        if not rows:
            continue
        groups_html.append(
            '<section class="group"><h2>{t} <span class="count">{n}</span></h2>{rows}</section>'.format(
                t=e(theme), n=len(rows), rows="".join(row(r) for r in rows)))
    groups_html = "".join(groups_html)

    chips = "".join(
        '<button class="chip" data-filter="{t}" aria-pressed="false">{t}</button>'.format(t=e(t))
        for t in THEME_ORDER)

    doc = TEMPLATE.format(picks=picks_html, n_picks=len(picks),
                          groups=groups_html, chips=chips, total=len(recs))
    out = os.path.join(REPO, "reports", "time_index", "trend_list.html")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(doc)
    return out, len(recs), len(picks)


TEMPLATE = """<title>403 Things That Move</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,400;6..72,500;6..72,600&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
:root {{
  --ground:#f4f7f7; --surface:#ffffff; --ink:#111d23; --ink-2:#3c4f59; --muted:#6c7f89;
  --accent:#0c6a64; --line:#dbe4e5; --flag:#84560f; --flag-soft:#f5ebd9;
}}
@media (prefers-color-scheme: dark) {{
  :root:not([data-theme="light"]) {{
    --ground:#0b1316; --surface:#111e23; --ink:#e2eaea; --ink-2:#b3c4c8; --muted:#7e939c;
    --accent:#4cc0b5; --line:#20313a; --flag:#dcb46b; --flag-soft:#2a2214;
  }}
}}
:root[data-theme="dark"] {{
  --ground:#0b1316; --surface:#111e23; --ink:#e2eaea; --ink-2:#b3c4c8; --muted:#7e939c;
  --accent:#4cc0b5; --line:#20313a; --flag:#dcb46b; --flag-soft:#2a2214;
}}
* {{ box-sizing:border-box; }}
body {{
  background:var(--ground); color:var(--ink); margin:0;
  font-family:"IBM Plex Sans", system-ui, -apple-system, "Segoe UI", sans-serif;
  font-size:16px; line-height:1.55; -webkit-font-smoothing:antialiased;
}}
.wrap {{ max-width:820px; margin:0 auto; padding:0 24px 96px; }}
header.top {{ padding:64px 0 26px; }}
h1 {{
  font-family:Newsreader, Georgia, serif; font-weight:500;
  font-size:clamp(34px, 6vw, 52px); line-height:1.06; letter-spacing:-0.015em;
  margin:0 0 14px; text-wrap:balance;
}}
.eyebrow {{
  font-family:"IBM Plex Mono", monospace; font-size:11.5px; letter-spacing:0.14em;
  text-transform:uppercase; color:var(--accent); margin:0 0 8px;
}}
.lede {{ font-size:18px; color:var(--ink-2); margin:0 0 10px; max-width:62ch; }}
.lede strong {{ color:var(--ink); font-weight:600; }}
.bar {{
  position:sticky; top:0; z-index:20; background:var(--ground);
  padding:14px 0 12px; border-bottom:1px solid var(--line);
  display:flex; flex-direction:column; gap:10px; margin-top:44px;
}}
#q {{
  width:100%; padding:11px 14px; font:inherit; font-size:15px;
  color:var(--ink); background:var(--surface);
  border:1px solid var(--line); border-radius:3px;
}}
#q:focus {{ outline:2px solid var(--accent); outline-offset:1px; border-color:var(--accent); }}
#q::placeholder {{ color:var(--muted); }}
.chips {{ display:flex; flex-wrap:wrap; gap:6px; }}
.chip {{
  font:inherit; font-size:12.5px; letter-spacing:0.02em; padding:5px 11px;
  border-radius:999px; cursor:pointer; color:var(--ink-2);
  background:transparent; border:1px solid var(--line);
}}
.chip:hover {{ border-color:var(--accent); color:var(--accent); }}
.chip[aria-pressed="true"] {{ background:var(--accent); border-color:var(--accent); color:var(--ground); }}
.chip:focus-visible {{ outline:2px solid var(--accent); outline-offset:2px; }}
h2 {{
  font-family:Newsreader, Georgia, serif; font-weight:500; font-size:26px;
  letter-spacing:-0.01em; margin:52px 0 2px;
  display:flex; align-items:baseline; gap:10px;
}}
h2 .count {{
  font-family:"IBM Plex Mono", monospace; font-size:12px; font-weight:400;
  color:var(--muted); letter-spacing:0.04em;
}}
.row {{ padding:20px 0; border-top:1px solid var(--line); }}
.row h3 {{
  font-family:Newsreader, Georgia, serif; font-weight:500; font-size:20px;
  line-height:1.25; margin:0 0 5px; letter-spacing:-0.005em; text-wrap:balance;
}}
.what {{ margin:0; color:var(--ink-2); font-size:15px; max-width:66ch; }}
.why {{
  margin:9px 0 0; padding-left:13px; border-left:2px solid var(--accent);
  color:var(--ink); font-size:15px; max-width:66ch;
}}
.meta {{
  font-family:"IBM Plex Mono", monospace; font-variant-numeric:tabular-nums;
  font-size:12px; color:var(--muted); margin:9px 0 0; letter-spacing:0.01em;
}}
.meta .dot {{ opacity:0.5; padding:0 2px; }}
.shape {{ margin:5px 0 0; font-size:13.5px; color:var(--accent); }}
.flag {{
  display:inline-block; margin:8px 8px 0 0; padding:3px 9px; border-radius:3px;
  background:var(--flag-soft); color:var(--flag);
  font-family:"IBM Plex Mono", monospace; font-size:11.5px;
}}
.note {{
  margin-top:60px; padding:24px; background:var(--surface);
  border:1px solid var(--line); border-radius:4px;
}}
.note h2 {{ margin:0 0 12px; font-size:21px; }}
.note p {{ margin:0 0 11px; color:var(--ink-2); font-size:15px; max-width:66ch; }}
.note p:last-child {{ margin-bottom:0; }}
.note strong {{ color:var(--ink); font-weight:600; }}
.empty {{ padding:40px 0; color:var(--muted); font-size:15px; display:none; }}
@media (prefers-reduced-motion:reduce) {{ * {{ transition:none !important; }} }}
</style>

<div class="wrap">
<header class="top">
  <p class="eyebrow">Everything with a clock on it</p>
  <h1>{total} things you can chart over time</h1>
  <p class="lede">Every dataset in the warehouse that can go on a time axis today, in plain English. <strong>Sixteen worth starting on</strong> sit at the top; the rest are grouped below.</p>
  <p class="lede">Each line says how far back it goes, how many rows actually carry a date, and how precise that date really is.</p>
</header>

<section class="picks">
  <h2>Start here <span class="count">{n_picks}</span></h2>
  {picks}
</section>

<div class="bar">
  <input id="q" type="search" placeholder="Search all {total} &mdash; try opioid, mine, sanctions, water&hellip;" autocomplete="off">
  <div class="chips">
    <button class="chip" data-filter="" aria-pressed="true">Everything</button>
    {chips}
  </div>
</div>

<p class="empty" id="empty">Nothing matches that.</p>

{groups}

<div class="note">
  <h2>Four ways these lines lie</h2>
  <p><strong>Counts measure reporting as much as the world.</strong> A line going up can mean the thing happened more, or that more of it got written down. Nursing home violations rose 446 times; almost all of that was more homes being inspected.</p>
  <p><strong>A date can be nearly empty.</strong> A dataset can be perfectly good and still carry that particular date on a tiny share of its rows. Where that happens, the line says so.</p>
  <p><strong>Year-only dates all land on 1 January.</strong> Put one on a daily axis beside a daily source and you invent a New Year&rsquo;s Day spike that never happened.</p>
  <p><strong>&ldquo;When it happened&rdquo; and &ldquo;when it was reported&rdquo; are different questions.</strong> Adding them together answers neither. Every line says which one it is.</p>
</div>
</div>

<script>
const q = document.getElementById('q');
const chips = [...document.querySelectorAll('.chip')];
const rows = [...document.querySelectorAll('.group .row')];
const groups = [...document.querySelectorAll('.group')];
const empty = document.getElementById('empty');
let filter = '';

function apply() {{
  const term = q.value.trim().toLowerCase();
  let shown = 0;
  rows.forEach(r => {{
    const ok = (!filter || r.dataset.themeGroup === filter) &&
               (!term || r.dataset.search.includes(term));
    r.style.display = ok ? '' : 'none';
    if (ok) shown++;
  }});
  groups.forEach(g => {{
    const any = [...g.querySelectorAll('.row')].some(r => r.style.display !== 'none');
    g.style.display = any ? '' : 'none';
  }});
  empty.style.display = shown ? 'none' : 'block';
}}
q.addEventListener('input', apply);
chips.forEach(c => c.addEventListener('click', () => {{
  filter = c.dataset.filter;
  chips.forEach(x => x.setAttribute('aria-pressed', x === c ? 'true' : 'false'));
  apply();
}}));
</script>
"""


if __name__ == "__main__":
    path, n, picks = build()
    print("wrote {} -- {} datasets, {} picks".format(path, n, picks))
