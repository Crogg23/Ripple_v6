// Layer + view + theme -> one fill per place, a finished legend model, role marks, and what the readout needs.
// The legend is built from the same scale and the same ramp as the fills. There is no legend text to type.
//
// Order of paint for one place: scale colour -> hillshade -> highlight fill -> low-confidence wash.
// The wash goes last on purpose: a shaky place must look shaky even when it is also called out.

import { resolvePeriod } from '../loader/load.js';
import { measureValues, measureMeta } from './measure.js';
import { buildScale } from './scale.js';
import { familyRamp, normalizeHex, desaturate, shade } from './color.js';
import { makeFormatter } from './format.js';
import { rankAll } from './readout.js';
import { pickHighlight, pickLowConfidence } from './roles.js';
import { hillshade } from './light.js';
import { WORDS } from './config.js';
import { narrate, sayer } from './narrate.js';

const whole = makeFormatter(',.0f');
const SHADE_REACH = 0.16;          // the most a full-strength hillshade moves a colour's lightness

function caption(legend, fmt) {
  const classes = legend.kind === 'classes' ? ` · ${legend.classes.length} classes` : '';
  switch (legend.basis) {
    case 'percentile': return `percentile${classes}`;
    case 'diverging': return `diverging around ${fmt(legend.midpoint)}${classes}`;
    case 'log': return 'log scale';
    case 'threshold': return 'fixed thresholds';
    case 'binary': return 'zero or not';
    case 'categorical': return 'categories';
    default: return `${legend.basis}${classes}`;
  }
}

function classText(c, fmt, basis, categories) {
  if (c.label) return c.label;
  if (basis === 'categorical') return (categories && categories[String(c.code)]) || `code ${fmt(c.code)}`;
  if (c.lo === null && c.hi === null) return '';
  if (c.lo === null) return `under ${fmt(c.hi)}`;
  if (c.hi === null) return `${fmt(c.lo)} and up`;
  return c.lo === c.hi ? fmt(c.lo) : `${fmt(c.lo)} – ${fmt(c.hi)}`;
}

/**
 * The spread: how many places sit at each level, in bars that wear the map's own colours. It is the legend and the
 * distribution in one picture. A long thin tail would flatten everything else, so bars stop at the 98th percentile
 * and one last bar holds whatever lies beyond, and says so.
 */
function spreadOf(values, order, scale, colorAt, zeroColor, fmt) {
  const M = order.length, lo = values[order[0]], max = values[order[M - 1]];
  const p98 = values[order[Math.floor(0.98 * (M - 1))]];
  const hi = max > lo && (max - lo) > (p98 - lo) * 1.6 && p98 > lo ? p98 : max;
  const K = 36, width = (hi - lo) / K || 1;
  const bins = Array.from({ length: K }, (_, k) => ({ lo: lo + k * width, hi: lo + (k + 1) * width, count: 0, tone: 0, zero: 0, places: [] }));
  const beyond = { lo: hi, hi: max, count: 0, tone: 0, zero: 0, places: [], beyond: true };
  for (const i of order) {
    const b = values[i] > hi ? beyond : bins[Math.min(K - 1, Math.floor((values[i] - lo) / width))];
    b.count++; b.places.push(i);
    if (scale.zero[i]) b.zero++; else b.tone += scale.t[i];
  }
  const finish = b => ({ lo: b.lo, hi: b.hi, count: b.count, places: b.places, beyond: !!b.beyond,
    color: !b.count ? null : b.zero === b.count ? zeroColor : colorAt(b.tone / (b.count - b.zero)),
    text: b.beyond ? `above ${fmt(b.lo)}, up to ${fmt(b.hi)}` : `${fmt(b.lo)} to ${fmt(b.hi)}` });
  const out = bins.map(finish);
  if (beyond.count) out.push(finish(beyond));
  const median = values[order[Math.floor((M - 1) / 2)]];
  return { bins: out, lo, hi, max, median, median_text: fmt(median), lo_text: fmt(lo), hi_text: fmt(hi), max_text: fmt(max), peak: Math.max(...out.map(b => b.count)) };
}

/**
 * @param {{layer: Object, view: Object, theme: Object, topology: Object}} input
 * @returns {{fills: string[], legend: Object, marks: {highlight: number[], low_confidence: number[]}, model: Object}}
 */
export function colorize({ layer, view, theme, topology }) {
  const { header, table, report } = layer;
  if (table.topology !== topology.id) throw new Error(`This layer was loaded against "${table.topology}". The map is showing "${topology.id}". Load it again.`);
  if (view.layer && view.layer !== header.id) throw new Error(`The view asks for layer "${view.layer}". The loaded layer is "${header.id}".`);
  const measure = view.measure || 'value';
  if (!WORDS.built_encoding.includes(theme.encoding)) {
    if (WORDS.size_encoding.includes(theme.encoding) && measure === 'ratio') {
      throw new Error(`The theme draws "${theme.encoding}", which reads as size. Size on a rate misleads, so the engine will not draw it. Use a fill theme, or switch the measure to value.`);
    }
    throw new Error(`The "${theme.encoding}" encoding is not built yet. Built so far: ${WORDS.built_encoding.join(', ')}.`);
  }
  const period = resolvePeriod(table, view.period);
  if (!period) {
    throw new Error(table.periods.length
      ? `The view asks for period "${view.period}". This layer has: ${table.periods.join(', ')}.`
      : 'No rows of this layer matched a place on this map.');
  }
  const cols = table.byPeriod[period];
  const values = measureValues(cols, measure, header, report);
  const meta = measureMeta(measure, header);
  const fmt = makeFormatter(meta.format);
  const notes = [];

  const tiers = view.filter && view.filter.tier_in;
  if (tiers) {
    if (!report.has_tier) throw new Error('The view filters by tier, and this layer has no tier column.');
    let hidden = 0;
    for (let i = 0; i < values.length; i++) if (cols.has[i] && !tiers.includes(cols.tier[i])) { values[i] = measure === 'presence' ? 0 : NaN; hidden++; }
    notes.push(`Only tier ${tiers.join(', ')} is drawn. ${whole(hidden)} places are hidden by that filter.`);
  }

  const cfg = view.scale || {};
  const scale = buildScale(values, cfg, measure === 'presence' ? { zero: 'empty', nonzero: 'has data' } : {});

  const family = scale.type === 'categorical' ? 'categorical'
    : scale.type === 'binary' ? 'binary'
    : scale.type === 'diverging' ? 'diverging'
    : cfg.zero_class ? 'binary' : 'sequential';
  const palettes = theme.palettes || {};
  const swatches = family === 'categorical' ? (palettes.categorical || []).map(normalizeHex) : null;
  if (swatches && !swatches.length) throw new Error('The theme has no "categorical" palette.');
  const paint = swatches ? null : familyRamp(palettes, family);
  const at = u => paint(scale.invert ? 1 - u : u);
  const zeroColor = palettes.binary ? normalizeHex(palettes.binary.zero) : null;
  if (scale.legend.zero && !zeroColor) throw new Error('The theme has no "binary" palette, and this view needs a zero colour.');
  const noData = normalizeHex(theme.roles.no_data.color);

  const N = values.length;
  const fills = new Array(N);
  let missing = 0;
  for (let i = 0; i < N; i++) {
    if (scale.zero[i]) fills[i] = zeroColor;
    else if (Number.isNaN(scale.t[i])) { fills[i] = noData; missing++; }
    else fills[i] = swatches ? swatches[scale.cat[i] % swatches.length] : at(scale.t[i]);
  }

  if (theme.light.type === 'hillshade' && theme.light.strength > 0 && !swatches) {
    const height = Float64Array.from(scale.t, (u, i) => (scale.zero[i] ? 0 : u));
    const lit = hillshade(topology, height);
    for (let i = 0; i < N; i++) if (!Number.isNaN(height[i])) fills[i] = shade(fills[i], lit[i] * theme.light.strength * SHADE_REACH);
    notes.push('Relief shading repeats the colour. It shows no second number.');
  }

  // Ink encodings: the value is carried by dots or lines laid over the land. The ramp colour moves onto the ink.
  let ink = null;
  if (theme.encoding !== 'fill') {
    if (swatches) throw new Error(`The "${theme.encoding}" encoding shows how much, and a categorical scale has no how much. Use a fill theme.`);
    const position = Float64Array.from(scale.t, (u, i) => (scale.zero[i] ? 0 : u));
    ink = { kind: theme.encoding, position: Array.from(position, u => (Number.isNaN(u) ? null : u)), colors: fills.slice(), ramp: Array.from({ length: 21 }, (_, k) => at(k / 20)) };
    if (WORDS.field_encoding.includes(theme.encoding)) notes.push('Smoothed across neighbouring places. Read the shape here, and hover a place for its own number.');
    if (theme.ink.under === 'empty') { const land = normalizeHex(theme.ground.land_empty); for (let i = 0; i < N; i++) if (!Number.isNaN(position[i])) fills[i] = land; }
  }

  const hi = pickHighlight(values, view.highlight, fmt);
  const floorPart = header[(view.confidence && view.confidence.field) || 'n'];
  const low = pickLowConfidence(cols, view.confidence, header, report, values, makeFormatter((floorPart && floorPart.format) || null));
  const hiRole = theme.roles.highlight, lowRole = theme.roles.low_confidence;
  if (hi && (hiRole.style === 'accent_fill' || hiRole.style === 'fill')) for (const i of hi.idx) fills[i] = normalizeHex(hiRole.color);
  if (low && lowRole.style === 'desaturate') for (const i of low.idx) fills[i] = desaturate(fills[i], lowRole.amount);

  const src = scale.legend;
  const legend = {
    title: meta.label, unit: meta.unit, period, measure,
    kind: src.kind, caption: caption(src, fmt), notes: [...src.notes, ...notes]
  };
  if (src.kind === 'ramp') {
    legend.stops = Array.from({ length: 11 }, (_, k) => ({ t: k / 10, color: at(k / 10) }));
    legend.ticks = src.ticks.map(tk => ({ t: tk.t, value: tk.value, text: fmt(tk.value) }));
  } else {
    legend.classes = src.classes.map(c => ({
      color: swatches ? swatches[c.category % swatches.length] : at(c.t),
      lo: c.lo, hi: c.hi, count: c.count,
      text: classText(c, fmt, src.basis, header.categories), count_text: whole(c.count)
    }));
  }
  legend.zero = src.zero ? { color: zeroColor, text: src.zero.label, count: src.zero.count, count_text: whole(src.zero.count) } : null;
  legend.no_data = missing ? { color: noData, text: 'no data', count: missing, count_text: whole(missing) } : null;

  // Role entries appear whenever the view switches the role on. A theme cannot hide them.
  const sample = swatches ? swatches[0] : at(0.65);
  legend.roles = [];
  if (hi) legend.roles.push({ role: 'highlight', style: hiRole.style, color: normalizeHex(hiRole.color), under: sample, text: hi.words, count: hi.idx.length, count_text: whole(hi.idx.length) });
  if (low) legend.roles.push({
    role: 'low_confidence', style: lowRole.style, under: sample,
    color: lowRole.style === 'desaturate' ? desaturate(sample, lowRole.amount) : normalizeHex(lowRole.color),
    text: low.words, count: low.idx.length, count_text: whole(low.idx.length)
  });

  // Callouts: the view asks for the top few places to be named on the map itself.
  const wanted = (view.labels && view.labels.top) || 0;
  const order = [];
  if (wanted > 0) { for (let i = 0; i < N; i++) if (!Number.isNaN(values[i])) order.push(i); order.sort((a, b) => values[b] - values[a] || a - b); }
  const labels = order.slice(0, wanted).map((i, k) => {
    const pl = topology.places[i], par = pl.parentId != null ? topology.parentIndexById.get(pl.parentId) : undefined;
    return { idx: i, rank: k + 1, name: pl.name, parent: par !== undefined ? topology.parents[par].name : null, text: fmt(values[i]) };
  });

  const marks = { highlight: hi ? hi.idx : [], low_confidence: low ? low.idx : [] };
  // Sorted once, low to high, and shared: the narrator, the hover sentence and the spread all read the same order.
  const lowToHigh = [];
  for (let i = 0; i < N; i++) if (!Number.isNaN(values[i])) lowToHigh.push(i);
  lowToHigh.sort((a, b) => values[a] - values[b]);
  legend.spread = swatches || !lowToHigh.length ? null : spreadOf(values, lowToHigh, scale, u => at(u), zeroColor, sayer(meta.format));   // the chart sits beside sentences, so it speaks like them
  const model = { topology, header, report, cols, period, values, measure, ranks: rankAll(values), view, order: lowToHigh };
  return { fills, legend, ink, labels, marks, model, story: narrate(model, marks) };
}
