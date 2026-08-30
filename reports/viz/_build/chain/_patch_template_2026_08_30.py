"""One-off patch applied to chain_template.html on 2026-08-30: measured tier, glossary merge,
verdict / spot-check on cards, place + clock panels. Kept as the receipt of what changed."""
from pathlib import Path

p = Path(__file__).resolve().parent / "chain_template.html"
s = p.read_text(encoding="utf-8")
if "Meets other tables on place" in s:
    raise SystemExit("already patched")


def rep(old, new, count=1):
    global s
    assert s.count(old) >= 1, old[:90]
    s = s.replace(old, new, count)


# 1. tiers
rep("const TIER_COLOR = { solid: '#f4a23a', strong: '#4c9aff', translation: '#b07cf0', location: '#3fb950' };",
    "const TIER_COLOR = { solid: '#f4a23a', strong: '#4c9aff', translation: '#b07cf0', measured: '#2dd4bf', location: '#3fb950' };")
rep("const TIER_ORDER = ['solid', 'strong', 'translation', 'location'];",
    "const TIER_ORDER = ['solid', 'strong', 'translation', 'measured', 'location'];")
rep("const TIER_WORD = { solid: 'certain', strong: 'very likely', translation: 'verified translation', location: 'same place only' };",
    "const TIER_WORD = { solid: 'certain', strong: 'very likely', translation: 'verified translation', measured: 'measured, not in the spine yet', location: 'same place only' };")
rep("  ['location', 'same place only', 'Geography. Never proof that two records are the same thing'],\n];",
    "  ['measured', 'measured, not in the spine yet', 'Overlap measured live on 08-29/30; where the card says so, 60 matched pairs were name-checked. The live machine does not use these joins yet — only the tiers above are wired in'],\n  ['location', 'same place only', 'Geography. Never proof that two records are the same thing'],\n];")
# 2. glossary merge from META
rep("const ACRONYMS = {};",
    "Object.keys(META.keys || {}).forEach(k => { if (!KEY_TITLE[k]) KEY_TITLE[k] = [META.keys[k].name, META.keys[k].desc]; });\nconst ACRONYMS = {};")
# 3. helpers
rep("const lines = (s, per) => Math.max(1, Math.ceil(String(s || '').length / per));",
    r"""const lines = (s, per) => Math.max(1, Math.ceil(String(s || '').length / per));
function verdictShort(c) {
  if (c.tier !== 'measured') return '';
  const v = String(c.verdict || '');
  if (/^SOLID/.test(v)) return v.trim();
  if (/^SUSPECT/.test(v)) return 'SUSPECT';
  if (/^level 2/.test(v)) return 'overlap only — not name-checked';
  return v;
}
function spotCheck(c) {
  if (c.tier !== 'measured' || !c.pairs) return '';
  return c.pairs + ' matched pairs spot-checked: names agree ' + c.names_pct + '%' + (c.states_pct != null ? ', states agree ' + c.states_pct + '%' : '');
}
const PLACE_COLOR = { state: '#8fceac', zip: '#8fceac', county: '#8fceac', fips: '#8fceac', coordinates: '#8fceac', city: '#7fb6ff' };
function placeRows(s) {
  return (s.place || []).map(p => ({
    label: p.label || p.kind, column: p.column, color: p.trap ? '#e5534b' : (PLACE_COLOR[p.kind] || '#9aa5b3'),
    fill: p.fill == null ? '' : p.fill + '% filled', verdict: p.verdict || '',
    others: p.others ? Math.max(0, p.others - 1) + ' other tables carry a clean ' + (p.label || p.kind) : '',
    hasNote: !!(p.note || p.trap), note: (p.trap ? '⚠ trap — ' : '') + (p.note || ''),
    title: p.column + ' · ' + (p.verdict || '') + (p.distinct != null ? ' · ' + Number(p.distinct).toLocaleString() + ' distinct values' : '') + ' · value-checked ' + ((META.place || {}).measuredOn || ''),
  }));
}
function timeRows(s) {
  return (s.time || []).map(c => ({
    column: c.column, color: c.trap ? '#e5534b' : (c.meaning === 'happened' ? '#7fb6ff' : '#9aa5b3'),
    grain: c.trap ? '⚠ not a clock' : ('to the ' + c.grain), label: c.label || c.meaning || '',
    range: (!c.trap && c.lo) ? c.lo + ' → ' + c.hi : '', hasDesc: !!c.desc, desc: c.desc || '',
    title: c.column + ' · ' + (c.format || '') + (c.rows ? ' · ' + Number(c.rows).toLocaleString() + ' rows carry it' : ''),
  }));
}
function clockLine(s) {
  const k = s.clock;
  if (!k) return '';
  return 'Best clock: ' + k.column + ' — ' + (k.label || k.meaning) + ', to the ' + k.grain + (k.lo ? ' (' + k.lo + ' → ' + k.hi + ')' : '');
}
function usable(list, trapKey) { return (list || []).filter(x => !x.trap).length; }
function placeSummary(s) {
  const n = usable(s.place), t = (s.place || []).length - n;
  return n + ' usable place column' + (n === 1 ? '' : 's') + (t ? ' · ' + t + ' trap' + (t === 1 ? '' : 's') : '') + ' · value-checked ' + ((META.place || {}).measuredOn || '');
}
function timeSummary(s) {
  const n = usable(s.time), t = (s.time || []).length - n;
  return n + ' clock column' + (n === 1 ? '' : 's') + (t ? ' · ' + t + ' look' + (t === 1 ? 's' : '') + ' like a date but is not' : '');
}""")
# 4. dossier fields + heights
rep("""    hasDesc: !!s.desc, desc: s.desc || '', notes,
    colCount: cols.length + (cols.length === 1 ? ' column recorded' : ' columns recorded'),""",
    """    hasDesc: !!s.desc, desc: s.desc || '', notes,
    hasPlace: !!(s.place && s.place.length), place: placeRows(s), placeSummary: placeSummary(s),
    hasTime: !!(s.time && s.time.length), time: timeRows(s), clock: clockLine(s), timeSummary: timeSummary(s),
    colCount: cols.length + (cols.length === 1 ? ' column recorded' : ' columns recorded'),""")
rep("""  notes.forEach(n => { h += 18 + lines(n.text, Math.floor(per * 0.9)) * 19; });
  h += 34 + lines(d.colSource, per) * 18 + 28;""",
    """  notes.forEach(n => { h += 18 + lines(n.text, Math.floor(per * 0.9)) * 19; });
  if (d.hasPlace) { h += 48; d.place.forEach(p => { h += 42 + (p.hasNote ? lines(p.note, per) * 17 : 0); }); }
  if (d.hasTime) { h += 48 + (d.clock ? lines(d.clock, per) * 18 : 0); d.time.forEach(c => { h += 30 + (c.hasDesc ? lines(c.desc, Math.floor(per * 0.9)) * 17 : 0); }); }
  h += 34 + lines(d.colSource, per) * 18 + 28;""")
rep("t ? t.conns.length + ' joins warehouse-wide' : '']",
    "t ? t.conns.length + ' joins warehouse-wide' : '', (s.place && s.place.length) ? 'meets others on place' : '', s.clock ? 'runs on a clock' : '']")
# 5. cards
rep("""            notes: dos ? dos.notes : [],
            colCount: dos ? dos.colCount : '',""",
    """            notes: dos ? dos.notes : [],
            hasPlace: dos ? dos.hasPlace : false, place: dos ? dos.place : [], placeSummary: dos ? dos.placeSummary : '',
            hasTime: dos ? dos.hasTime : false, time: dos ? dos.time : [], clock: dos ? dos.clock : '', timeSummary: dos ? dos.timeSummary : '',
            hasVerdict: c.tier === 'measured', verdict: verdictShort(c), spot: spotCheck(c), edgeNote: c.note || '',
            colCount: dos ? dos.colCount : '',""")
rep("""                  : 'new at step ' + (depth + 1) + ' · ' + [fmtRows(ctx.rows), (() => {""",
    """                  : 'new at step ' + (depth + 1) + ' · ' + [c.tier === 'measured' ? verdictShort(c) : '', fmtRows(ctx.rows), (() => {""")
rep("""              + (RISKY[c.jk] ? ' · UNRELIABLE: roughly 4 in 10 DOCKET matches are wrong' : ''),""",
    """              + (RISKY[c.jk] ? ' · UNRELIABLE: roughly 4 in 10 DOCKET matches are wrong' : '')
              + (c.tier === 'measured' ? ' · MEASURED, NOT IN THE SPINE YET: ' + String(c.verdict || '') + (spotCheck(c) ? ' · ' + spotCheck(c) : '') + (c.note ? ' · ' + c.note : '') : ''),""")
# measured card height: verdict block
rep("          const cardH = isOpen ? dos.h : CARD_H;",
    "          const cardH = isOpen ? dos.h + (c.tier === 'measured' ? 70 + lines(spotCheck(c) + (c.note || ''), 60) * 17 : 0) : CARD_H;")
# 6. source box
rep("""        sourceCols: ((SCHEMA[src.id] || {}).cols || []).map(colEntry),""",
    """        sourceCols: ((SCHEMA[src.id] || {}).cols || []).map(colEntry),
        sourceHasPlace: !!((SCHEMA[src.id] || {}).place || []).length, sourcePlace: placeRows(SCHEMA[src.id] || {}), sourcePlaceSummary: placeSummary(SCHEMA[src.id] || {}),
        sourceHasTime: !!((SCHEMA[src.id] || {}).time || []).length, sourceTime: timeRows(SCHEMA[src.id] || {}), sourceClock: clockLine(SCHEMA[src.id] || {}), sourceTimeSummary: timeSummary(SCHEMA[src.id] || {}),""")
rep("sourceCtx: [agencyOf(src.id), fmtRows(ctxSrc.rows), ctxSrc.dom ? String(ctxSrc.dom).replace(/_/g, ' ') : ''].filter(Boolean).join(' · '),",
    "sourceCtx: [agencyOf(src.id), fmtRows(ctxSrc.rows), ctxSrc.dom ? String(ctxSrc.dom).replace(/_/g, ' ') : '', src.conns.length + ' ID joins', usable((SCHEMA[src.id] || {}).place) ? 'meets others on place' : '', (SCHEMA[src.id] || {}).clock ? 'runs on a clock' : ''].filter(Boolean).join(' · '),")
# intro + footnotes
rep("""      intro: labelOf(src.id) + ' joins to ' + src.conns.length + ' datasets. Each of those joins to more. This page just keeps going: every column is one real step, and every line is a join that has been measured.',""",
    """      intro: (src.conns.length ? labelOf(src.id) + ' joins to ' + src.conns.length + ' datasets. Each of those joins to more.' : labelOf(src.id) + ' has no shared-ID join at all — it is reachable only by place or by time (see its panels on the left).') + ' This page just keeps going: every column is one real step, and every line is a join that has been measured. ' + TABLES.length + ' tables in all; ' + (META.newTables || 0) + ' are here only because they meet other tables on place or on a clock.',""")
rep("""        'Counts are warehouse-wide, not filtered by anything on this page.',
      ],""",
    """        'Counts are warehouse-wide, not filtered by anything on this page.',
        'Teal joins were measured on ' + (META.measuredOn || '2026-08-29') + ' but are not in the live machine\\u2019s spine yet; the card says whether the matched pairs were name-checked or only counted.',
        'Every table\\u2019s + panel lists its value-checked place columns (' + ((META.place || {}).tables || 0) + ' tables, checked ' + ((META.place || {}).measuredOn || '') + ') and its clocks (' + ((META.time || {}).tables || 0) + ' tables). Same state / ZIP / county / day is a real join in Ripple, with no ID needed — but never proof that two records are the same thing.',
      ],""")
# pick options
rep("""              id: t.id, label: labelOf(t.id), joins: t.conns.length + (t.conns.length === 1 ? ' join' : ' joins'),""",
    """              id: t.id, label: labelOf(t.id), joins: (t.conns.length ? t.conns.length + (t.conns.length === 1 ? ' join' : ' joins') : 'no ID joins') + (usable((SCHEMA[t.id] || {}).place) ? ' · place' : '') + ((SCHEMA[t.id] || {}).clock ? ' · clock' : ''),""")


def panel(has_place, place_summary, place_list, has_time, time_summary, clock, time_list):
    return f"""
          <sc-if value="{{{{ {has_place} }}}}" hint-placeholder-val="{{{{ false }}}}">
            <div style="margin-top: 13px; padding-top: 10px; border-top: 1px solid #1c2530;">
              <div style="display: flex; align-items: baseline; gap: 8px; flex-wrap: wrap;">
                <span style="font-size: 9.5px; letter-spacing: 0.1em; text-transform: uppercase; color: #8fceac;">Meets other tables on place</span>
                <span style="font-size: 10.5px; color: #9aa5b3;">{{{{ {place_summary} }}}}</span>
              </div>
              <sc-for list="{{{{ {place_list} }}}}" as="pl" hint-placeholder-count="2">
                <div title="{{{{ pl.title }}}}" style="margin-top: 8px;">
                  <div style="display: flex; align-items: baseline; gap: 8px; flex-wrap: wrap;">
                    <span style="font-family: 'IBM Plex Mono', monospace; font-size: 10px; color: {{{{ pl.color }}}}; border: 1px solid {{{{ pl.color }}}}; border-radius: 999px; padding: 2px 7px; white-space: nowrap;">{{{{ pl.label }}}}</span>
                    <span style="font-family: 'IBM Plex Mono', monospace; font-size: 11px; color: #ffffff; word-break: break-all;">{{{{ pl.column }}}}</span>
                    <span style="font-size: 11px; color: #9aa5b3;">{{{{ pl.fill }}}} · {{{{ pl.verdict }}}}</span>
                  </div>
                  <div style="font-size: 10.5px; color: #8a95a3; margin-top: 3px; padding-left: 2px;">{{{{ pl.others }}}}</div>
                  <sc-if value="{{{{ pl.hasNote }}}}" hint-placeholder-val="{{{{ false }}}}">
                    <div style="font-size: 11px; line-height: 1.5; color: #c98b86; margin-top: 2px; padding-left: 2px;">{{{{ pl.note }}}}</div>
                  </sc-if>
                </div>
              </sc-for>
            </div>
          </sc-if>
          <sc-if value="{{{{ {has_time} }}}}" hint-placeholder-val="{{{{ false }}}}">
            <div style="margin-top: 13px; padding-top: 10px; border-top: 1px solid #1c2530;">
              <div style="display: flex; align-items: baseline; gap: 8px; flex-wrap: wrap;">
                <span style="font-size: 9.5px; letter-spacing: 0.1em; text-transform: uppercase; color: #7fb6ff;">Runs on a clock</span>
                <span style="font-size: 10.5px; color: #9aa5b3;">{{{{ {time_summary} }}}}</span>
              </div>
              <div style="font-size: 11.5px; line-height: 1.5; color: #e8eaed; margin-top: 6px;">{{{{ {clock} }}}}</div>
              <sc-for list="{{{{ {time_list} }}}}" as="tc" hint-placeholder-count="2">
                <div title="{{{{ tc.title }}}}" style="margin-top: 8px;">
                  <div style="display: flex; align-items: baseline; gap: 8px; flex-wrap: wrap;">
                    <span style="font-family: 'IBM Plex Mono', monospace; font-size: 10px; color: {{{{ tc.color }}}}; border: 1px solid {{{{ tc.color }}}}; border-radius: 999px; padding: 2px 7px; white-space: nowrap;">{{{{ tc.grain }}}}</span>
                    <span style="font-family: 'IBM Plex Mono', monospace; font-size: 11px; color: #ffffff; word-break: break-all;">{{{{ tc.column }}}}</span>
                    <span style="font-size: 11px; color: #9aa5b3;">{{{{ tc.label }}}} · {{{{ tc.range }}}}</span>
                  </div>
                  <sc-if value="{{{{ tc.hasDesc }}}}" hint-placeholder-val="{{{{ false }}}}">
                    <div style="font-size: 11px; line-height: 1.5; color: #a4aeba; margin-top: 2px; padding-left: 2px; text-wrap: pretty;">{{{{ tc.desc }}}}</div>
                  </sc-if>
                </div>
              </sc-for>
            </div>
          </sc-if>"""


anchor_src = """          </sc-for>

          <div style="display: flex; align-items: baseline; gap: 8px; margin-top: 14px; padding-top: 11px; border-top: 1px solid #22303e;">
            <span style="font-size: 9.5px; letter-spacing: 0.1em; text-transform: uppercase; color: #7fb6ff;">Columns</span>"""
rep(anchor_src, "          </sc-for>\n" + panel("view.sourceHasPlace", "view.sourcePlaceSummary", "view.sourcePlace",
                                           "view.sourceHasTime", "view.sourceTimeSummary", "view.sourceClock", "view.sourceTime")
    + anchor_src[len("          </sc-for>\n"):])

anchor_card = """                </sc-for>

                <div style="display: flex; align-items: center; gap: 10px; margin-top: 13px; padding-top: 10px; border-top: 1px solid #1c2530;">
                  <span style="font-size: 9.5px; letter-spacing: 0.1em; text-transform: uppercase; color: #7fb6ff;">Columns</span>"""
verdict_block = """
                <sc-if value="{{ c.hasVerdict }}" hint-placeholder-val="{{ false }}">
                  <div style="margin-top: 11px; padding: 9px 11px; border-radius: 8px; background: rgba(45,212,191,0.06); border: 1px solid rgba(45,212,191,0.25);">
                    <div style="font-size: 9.5px; letter-spacing: 0.1em; text-transform: uppercase; color: #2dd4bf;">Measured, not in the spine yet</div>
                    <div style="font-size: 12px; line-height: 1.5; color: #e8eaed; margin-top: 4px;">{{ c.verdict }}</div>
                    <div style="font-size: 11.5px; line-height: 1.5; color: #c8ced5; margin-top: 2px;">{{ c.spot }}</div>
                    <div style="font-size: 11px; line-height: 1.5; color: #9aa5b3; margin-top: 2px; text-wrap: pretty;">{{ c.edgeNote }}</div>
                  </div>
                </sc-if>"""
rep(anchor_card, "                </sc-for>\n" + verdict_block
    + panel("c.hasPlace", "c.placeSummary", "c.place", "c.hasTime", "c.timeSummary", "c.clock", "c.time")
    + anchor_card[len("                </sc-for>\n"):])

p.write_text(s, encoding="utf-8")
print("patched", len(s))
