"""One-shot patch of join_handbook_template.html for the pass-2 layer (2026-08-29).

Adds the MEASURED / SUSPECT tiers, pulls glossary additions + traps + corrections from
DATA.notes, shows verdict/notes on expanded rows, and adds a "measured, not in spine" tally.
Safe to re-run: every replacement asserts its anchor and skips if already applied.
"""

from __future__ import annotations

from pathlib import Path

T = Path(__file__).resolve().parent / "join_handbook_template.html"
src = T.read_text(encoding="utf-8")
orig = src


def rep(old: str, new: str, must: bool = True):
    global src
    if new in src and old not in src:
        return  # already applied
    if old not in src:
        if must:
            raise SystemExit(f"anchor not found:\n{old[:120]}")
        return
    assert src.count(old) == 1, f"anchor not unique: {old[:80]}"
    src = src.replace(old, new)


# --- CSS: two new tier colours + row note styling
rep("  --t-corrob: #776c8c;\n",
    "  --t-corrob: #776c8c;\n  --t-measured: #6b4c9a;\n  --t-suspect: #a33a3a;\n")
rep("    --t-steel: #9dc0ea; --t-bridge: #ddad64; --t-geo: #7fc9a4; --t-corrob: #b3a9cb;\n",
    "    --t-steel: #9dc0ea; --t-bridge: #ddad64; --t-geo: #7fc9a4; --t-corrob: #b3a9cb; --t-measured: #b9a1e6; --t-suspect: #e08a8a;\n")
rep("  --t-steel: #9dc0ea; --t-bridge: #ddad64; --t-geo: #7fc9a4; --t-corrob: #b3a9cb;\n",
    "  --t-steel: #9dc0ea; --t-bridge: #ddad64; --t-geo: #7fc9a4; --t-corrob: #b3a9cb; --t-measured: #b9a1e6; --t-suspect: #e08a8a;\n")
rep(".t-CORROBORATED .pct { color: var(--t-corrob); }\n",
    ".t-CORROBORATED .pct { color: var(--t-corrob); }\n"
    ".t-MEASURED .dot { background: var(--t-measured); }\n"
    ".t-MEASURED .bar > i { background: var(--t-measured); }\n"
    ".t-MEASURED .pct { color: var(--t-measured); }\n"
    ".t-SUSPECT .dot { background: var(--t-suspect); }\n"
    ".t-SUSPECT .bar > i { background: var(--t-suspect); }\n"
    ".t-SUSPECT .pct { color: var(--t-suspect); }\n"
    ".verdict { margin: 8px 0 0; font-size: 12px; color: var(--ink-2); }\n"
    ".verdict b { color: var(--ink); }\n"
    ".verdict.bad b { color: var(--t-suspect); }\n"
    ".traps li { margin: 0 0 8px; font-size: 12.5px; line-height: 1.45; }\n"
    ".traps ul { margin: 0; padding-left: 18px; }\n"
    ".corr { width: 100%; border-collapse: collapse; font-size: 12px; }\n"
    ".corr td { padding: 5px 8px; border-top: 1px solid var(--border-soft); vertical-align: top; }\n"
    ".corr td:first-child { color: var(--ink-3); width: 38%; }\n")

# --- tier definitions
rep("  CORROBORATED: { label: 'Educated guess (name + ZIP)', short: 'no shared ID at all &mdash; least reliable by far', color: 'var(--t-corrob)',",
    "  MEASURED: { label: 'Measured, not yet in the spine', short: 'same official ID, checked live on 2026-08-29, awaiting spine registration', color: 'var(--t-measured)',\n"
    "            desc: 'Both tables print the same official ID and the overlap was measured against live data in connections pass 2 (2026-08-29). Where the row says SOLID, 60 random matched pairs were also checked by name and state. These are not yet registered in the spine\\'s edge table, so the spine\\'s own joins don\\'t use them yet.' },\n"
    "  SUSPECT: { label: 'Suspect &mdash; do not use', short: 'values overlap, but the matched pairs are often different organizations', color: 'var(--t-suspect)',\n"
    "            desc: 'The ID values overlap, but a name check showed that many of the matched pairs are different organizations. Listed so nobody rediscovers it by accident &mdash; the row says what to use instead.' },\n"
    "  CORROBORATED: { label: 'Educated guess (name + ZIP)', short: 'no shared ID at all &mdash; least reliable by far', color: 'var(--t-corrob)',")
rep("const TIER_ORDER = ['STEEL','STRONG','BRIDGE','GEO','CORROBORATED'];",
    "const TIER_ORDER = ['STEEL','STRONG','BRIDGE','MEASURED','GEO','SUSPECT','CORROBORATED'];")

# --- glossary additions ride in DATA.notes
rep("const keyInfo = k => KEY_INFO[k] || { name: k, desc: 'a shared identifier between these two tables' };",
    "const NOTES = DATA.notes || { keys: {}, traps: [], corrections: [] };\n"
    "Object.keys(NOTES.keys || {}).forEach(k => { if (!KEY_INFO[k]) KEY_INFO[k] = NOTES.keys[k]; });\n"
    "const keyInfo = k => KEY_INFO[k] || { name: k, desc: 'a shared identifier between these two tables' };")

# --- legend headings: no longer five
rep("<h3>The five kinds of connection</h3>", "<h3>The kinds of connection, most to least sure</h3>")
rep("'<div class=\"panel\"><h3>The five kinds of connection &mdash; most to least sure</h3>'",
    "'<div class=\"panel\"><h3>The kinds of connection &mdash; most to least sure</h3>'")

# --- meter: count the measured layer too
rep("const _seen = new Set(), _seenHard = new Set();",
    "const _seen = new Set(), _seenHard = new Set(), _seenMeasured = new Set();")
rep("  if (HARD_TIERS.indexOf(e.tier) > -1) _seenHard.add(pair);\n}));",
    "  if (HARD_TIERS.indexOf(e.tier) > -1) _seenHard.add(pair);\n  if (e.tier === 'MEASURED') _seenMeasured.add(pair);\n}));")
rep("  nf(hardJoins) + '</b> reliable joins &nbsp;&middot;&nbsp; ' + nf(totalJoins) + ' measured';",
    "  nf(hardJoins) + '</b> reliable joins &nbsp;&middot;&nbsp; <b>' + nf(_seenMeasured.size) + '</b> measured, not in spine yet &nbsp;&middot;&nbsp; ' + nf(totalJoins) + ' measured in all';")

# --- rail: tables whose only real IDs are pass-2 still count as "real IDs"
rep("  if (hideWeak) list = list.filter(t => t.n_hard > 0);",
    "  if (hideWeak) list = list.filter(t => t.n_hard > 0 || (t.n_measured || 0) > 0);")
rep("    : (a, b) => b.n_hard - a.n_hard || b.n_conn - a.n_conn || a.name.localeCompare(b.name));\n  railView = list;",
    "    : (a, b) => b.n_hard - a.n_hard || (b.n_measured || 0) - (a.n_measured || 0) || b.n_conn - a.n_conn || a.name.localeCompare(b.name));\n  railView = list;")

# --- detail tally + notice for suspect edges
rep("  const geoCount = count('GEO');\n  const fuzzyCount = count('CORROBORATED');",
    "  const geoCount = count('GEO');\n  const fuzzyCount = count('CORROBORATED');\n  const measuredCount = count('MEASURED');\n  const suspectCount = count('SUSPECT');")
rep("  h += '<div class=\"tally\">' + cell(hardCount, 'reliable joins') + cell(agencies, 'other agencies') +\n       cell(geoCount, 'place-based') + cell(fuzzyCount, 'name guesses') + '</div>';",
    "  h += '<div class=\"tally\">' + cell(hardCount, 'reliable joins') + cell(measuredCount, 'measured, not in spine') + cell(agencies, 'other agencies') +\n       cell(geoCount, 'place-based') + cell(fuzzyCount, 'name guesses') + '</div>';\n"
    "  if (suspectCount) {\n"
    "    h += '<div class=\"notice\"><span class=\"ic\">&#9888;</span><div><b>Heads up.</b> This table has a connection marked <b>suspect</b>: the ID values overlap, ' +\n"
    "         'but when matched pairs were checked by name about half were different organizations. Open the row for what to use instead.</div></div>';\n"
    "  }")

# --- expanded row: verdict + note
rep("      h += '<p class=\"say\">' + joinSentence(e) + '</p>';",
    "      h += '<p class=\"say\">' + joinSentence(e) + '</p>';\n"
    "      if (e.src === 'pass2') {\n"
    "        h += '<p class=\"verdict' + (e.tier === 'SUSPECT' ? ' bad' : '') + '\">checked ' + esc(e.measured_on || '') + ': <b>' + esc(e.verdict || '') + '</b>' +\n"
    "             (e.note ? ' &mdash; ' + esc(e.note) : '') + '</p>';\n"
    "      }")
rep("  if (e.tier === 'GEO')\n    return 'Matched on <b>' + esc(info.name.toLowerCase()) + '</b> &mdash; same place, not necessarily the same organization.';",
    "  if (e.tier === 'GEO')\n    return 'Matched on <b>' + esc(info.name.toLowerCase()) + '</b> &mdash; same place, not necessarily the same organization.';\n"
    "  if (e.tier === 'SUSPECT')\n    return 'About <b>' + rate.toFixed(0) + '%</b> of the ' + esc(info.name.toLowerCase()) + ' values also show up in ' + esc(e.other) +\n"
    "           ' &mdash; but roughly half of those pairs are <b>different organizations</b>. Do not use this join as-is.';")

# --- intro: traps + corrections panels
rep("    '<div class=\"panel\"><h3>Shortcuts</h3><div class=\"tips\">' + tipsHTML + '</div></div>' +\n    '</div></div>';\n  main.querySelectorAll",
    "    ((NOTES.traps || []).length ? '<div class=\"panel traps\"><h3>Traps &mdash; read before joining (pass 2, ' + esc(NOTES.measured_on || '') + ')</h3><ul>' +\n"
    "      NOTES.traps.map(t => '<li>' + esc(t) + '</li>').join('') + '</ul></div>' : '') +\n"
    "    ((NOTES.corrections || []).length ? '<div class=\"panel\"><h3>Corrections carried in from pass 2</h3><table class=\"corr\">' +\n"
    "      NOTES.corrections.map(c => '<tr><td>' + esc(c.was) + '</td><td>' + esc(c.now) + '</td></tr>').join('') + '</table></div>' : '') +\n"
    "    '<div class=\"panel\"><h3>Shortcuts</h3><div class=\"tips\">' + tipsHTML + '</div></div>' +\n    '</div></div>';\n  main.querySelectorAll")

if src == orig:
    print("template already patched; nothing to do")
else:
    T.write_text(src, encoding="utf-8")
    print(f"patched {T}")
