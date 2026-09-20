// Slice 2 checks: honest colour. Ties share, the legend comes from the scale, the readout keeps every number reachable.
import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

import { decodeTopology } from '../src/topology/registry.js';
import { parseText } from '../src/loader/parse.js';
import { loadRows } from '../src/loader/load.js';
import { DEFAULT_THEME, DEFAULT_VIEW, overlay } from '../src/engine/defaults.js';
import { buildScale } from '../src/engine/scale.js';
import { measureValues, ratioOf } from '../src/engine/measure.js';
import { ramp, hexToOklab, oklabToHex } from '../src/engine/color.js';
import { makeFormatter } from '../src/engine/format.js';
import { rankAll, buildReadout } from '../src/engine/readout.js';
import { colorize } from '../src/engine/colorize.js';
import { hitTest, unproject } from '../src/engine/hit.js';
import { buildDrawList } from '../src/engine/drawlist.js';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const registry = JSON.parse(readFileSync(join(root, 'topologies/registry.json'), 'utf8'));
const entry = registry.topologies.us_counties_2018;
const topo = decodeTopology('us_counties_2018', entry, JSON.parse(readFileSync(join(root, 'topologies', entry.url), 'utf8')));
const at = id => topo.indexById.get(id);
const load = (text, opts = {}) => loadRows(parseText(text).rows, { topology: topo, ...opts });
const view = patch => overlay(DEFAULT_VIEW, patch);
const paint = (layer, v = {}, theme = DEFAULT_THEME) => colorize({ layer, view: view(v), theme, topology: topo });
const F = a => Float64Array.from(a);

// Six places. Three share the value 10. v1 would have given them three colours, by file order.
const TIES = `geo_id,value,denominator
48201,10,100
06037,10,50
17031,10,0
01001,1,10
01003,50,10
04013,900,`;

test('ties share: equal values get one colour, under every scale type', () => {
  const layer = load(TIES);
  const tied = ['48201', '06037', '17031'].map(at);
  for (const scale of [
    { type: 'quantile' }, { type: 'quantile', bins: 3 }, { type: 'linear' }, { type: 'quantize', bins: 4 }, { type: 'log' },
    { type: 'threshold', thresholds: [5, 100] }, { type: 'diverging', midpoint: 10 }, { type: 'binary' }, { type: 'categorical' }
  ]) {
    const { fills } = paint(layer, { scale });
    assert.equal(new Set(tied.map(i => fills[i])).size, 1, `${scale.type}: tied places got ${tied.map(i => fills[i])}`);
    if (scale.type !== 'binary') assert.notEqual(fills[at('48201')], fills[at('04013')], `${scale.type}: 10 and 900 look the same`);
  }
});

test('ties: "spread" is the v1 behaviour, it is opt-in, and the legend admits it', () => {
  const layer = load(TIES);
  const { fills, legend } = paint(layer, { scale: { type: 'quantile', ties: 'spread' } });
  assert.equal(new Set(['48201', '06037', '17031'].map(i => fills[at(i)])).size, 3);
  assert.match(legend.notes.join(' '), /equal values can get different colours/);
  assert.equal(paint(layer).legend.notes.length, 0);
});

test('binned quantile: heavy ties merge classes, and the legend says how many are left', () => {
  const values = F([...new Array(70).fill(0), ...Array.from({ length: 30 }, (_, k) => k + 1)]);
  const s = buildScale(values, { type: 'quantile', bins: 5 });
  const zeros = new Set(Array.from(s.t.slice(0, 70)));
  assert.equal(zeros.size, 1);
  assert.ok(s.legend.classes.length < 5);
  assert.match(s.legend.notes[0], /5 classes became \d/);
  assert.equal(s.legend.classes.reduce((n, c) => n + c.count, 0), 100);
  for (let k = 1; k < s.legend.classes.length; k++) assert.ok(s.legend.classes[k].lo > s.legend.classes[k - 1].hi, 'classes overlap');
});

test('quantile legend: says "percentile", shows real values from the data, at uneven spacing', () => {
  const rows = ['geo_id,value', ...topo.places.slice(0, 400).map((p, k) => `${p.id},${Math.round(Math.exp(k / 40))}`)].join('\n');
  const { legend } = paint(load(rows));
  assert.equal(legend.kind, 'ramp');
  assert.match(legend.caption, /^percentile/);
  const real = new Set(topo.places.slice(0, 400).map((_, k) => Math.round(Math.exp(k / 40))));
  for (const tk of legend.ticks) assert.ok(real.has(tk.value), `${tk.value} is not a value in the data`);
  const gaps = legend.ticks.slice(1).map((tk, k) => +(tk.t - legend.ticks[k].t).toFixed(3));
  assert.ok(new Set(gaps).size > 1, `tick gaps are all equal: ${gaps}`);
  // The values are skewed, so a linear reading of the ticks would be wrong: the middle tick is nowhere near the middle value.
  const mid = legend.ticks.find(tk => Math.abs(tk.t - 0.5) < 0.05);
  assert.ok(mid.value < (legend.ticks[0].value + legend.ticks[legend.ticks.length - 1].value) / 4);
  assert.equal(legend.stops.length, 11);
});

test('smooth quantile uses the whole palette even when both ends are heavy ties', () => {
  const s = buildScale(F([0, 0, 0, 0, 5, 9, 9, 9]), { type: 'quantile' });
  assert.equal(s.t[0], 0); assert.equal(s.t[7], 1);
  assert.ok(s.t[4] > 0 && s.t[4] < 1);
  assert.deepEqual(s.legend.ticks.map(tk => tk.value), [0, 5, 9]);
});

test('zero denominator: the rate is no data. Never infinity, never zero', () => {
  assert.ok(Number.isNaN(ratioOf(10, 0, 1)));
  assert.ok(Number.isNaN(ratioOf(0, 0, 1)));
  assert.ok(Number.isNaN(ratioOf(NaN, 5, 1)));
  assert.equal(ratioOf(10, 50, 100), 20);
  const layer = load(TIES);
  const { fills, legend, model } = paint(layer, { measure: 'ratio' });
  assert.ok(model.values.every(v => Number.isNaN(v) || Number.isFinite(v)));
  assert.equal(fills[at('17031')], DEFAULT_THEME.roles.no_data.color);       // base of zero
  assert.equal(fills[at('04013')], DEFAULT_THEME.roles.no_data.color);       // base missing
  assert.notEqual(fills[at('48201')], DEFAULT_THEME.roles.no_data.color);
  assert.equal(legend.no_data.count, topo.places.length - 4);
  const r = buildReadout(at('17031'), model);
  assert.equal(r.rows.find(x => x.key === 'ratio').text, 'no data');
  assert.equal(r.rows.find(x => x.key === 'value').text, '10');
  assert.match(r.notes.join(' '), /base is zero/i);
  assert.equal(r.rank, null);
});

test('readout: with a denominator, value, base, and ratio are all there, whatever the view asks for', () => {
  const layer = load(TIES, { header: { label: 'Fines', value: { format: '$,.0f' }, denominator: { label: 'Beds' }, ratio: { label: 'Fines per bed', format: '$,.2f' } } });
  const { model } = paint(layer, { measure: 'ratio', readout: { always: [], on_demand: [] } });
  const r = buildReadout(at('06037'), model);
  assert.deepEqual(r.rows.map(x => x.key), ['value', 'denominator', 'ratio']);
  assert.deepEqual(r.rows.map(x => x.text), ['$10', '50', '$0.20']);
  assert.equal(r.rows.find(x => x.key === 'ratio').always, true);             // the driving measure is always shown
  assert.equal(r.rows.find(x => x.key === 'ratio').driving, true);
  assert.equal(r.name, 'Los Angeles'); assert.equal(r.parent, 'California');
  assert.deepEqual(JSON.parse(JSON.stringify(r)), r);                          // plain data
  const bare = buildReadout(at('06037'), paint(load('geo_id,value\n06037,4')).model);
  assert.deepEqual(bare.rows.map(x => x.key), ['value']);
});

test('rank: 1 is highest, ties share a rank, "of N" counts places with data', () => {
  const k = rankAll(F([5, NaN, 9, 5, 1]));
  assert.deepEqual(Array.from(k.rank), [2, 0, 1, 2, 4]);
  assert.deepEqual(Array.from(k.tied), [2, 0, 1, 2, 1]);
  assert.equal(k.of, 4);
  const { model } = paint(load(TIES));
  assert.equal(buildReadout(at('04013'), model).rank.text, '1 of 6');
  assert.equal(buildReadout(at('48201'), model).rank.text, '3 of 6, tied with 2');
});

test('the engine refuses views that would mislead, and says why in plain words', () => {
  const noBase = load('geo_id,value\n48201,4\n06037,0');
  assert.throws(() => paint(noBase, { measure: 'ratio' }), /no denominator/);
  assert.throws(() => paint(noBase, { measure: 'n' }), /no n column/);
  assert.throws(() => paint(noBase, { measure: 'difference' }), /second layer/);
  assert.throws(() => paint(noBase, { measure: 'vibes' }), /not known/);
  assert.throws(() => paint(noBase, { scale: { type: 'log' } }), /log scale cannot show zero or negative values, and 1 places/);
  assert.throws(() => paint(noBase, { scale: { type: 'diverging' } }), /needs scale\.midpoint/);
  assert.throws(() => paint(noBase, { scale: { type: 'threshold' } }), /needs scale\.thresholds/);
  assert.throws(() => paint(noBase, { scale: { type: 'threshold', thresholds: [5, 1] } }), /rising/);
  assert.throws(() => paint(noBase, { scale: { type: 'rainbow' } }), /not known/);
  assert.throws(() => paint(noBase, { scale: { bins: 1 } }), /scale\.bins/);
  assert.throws(() => paint(noBase, { period: '1999' }), /This layer has: latest/);
  assert.doesNotThrow(() => paint(noBase, { scale: { type: 'log', zero_class: true } }));   // zeros pulled out first, so log is fine
});

test('the legend is generated from the scale: every colour on the map is a colour in the legend', () => {
  const rows = ['geo_id,value,denominator', ...topo.places.slice(0, 900).map((p, k) => `${p.id},${k % 7 === 0 ? 0 : (k * 37) % 500},${k % 11 === 0 ? 0 : 100 + k}`)].join('\n');
  const layer = load(rows);
  for (const v of [
    { scale: { type: 'quantile', bins: 5 } }, { scale: { type: 'quantile', bins: 4, zero_class: true } }, { scale: { type: 'quantize', bins: 6 } },
    { scale: { type: 'threshold', thresholds: [10, 100, 300] } }, { scale: { type: 'diverging', midpoint: 250, bins: 5 } }, { scale: { type: 'binary' } },
    { measure: 'ratio', scale: { type: 'quantile', bins: 5, invert: true } }, { measure: 'presence', scale: { type: 'binary' } }
  ]) {
    const { fills, legend } = paint(layer, v);
    const inLegend = new Set([...legend.classes.map(c => c.color), legend.zero && legend.zero.color, legend.no_data && legend.no_data.color]);
    for (const c of new Set(fills)) assert.ok(inLegend.has(c), `${JSON.stringify(v)}: ${c} is on the map but not in the legend`);
    const counted = legend.classes.reduce((n, c) => n + c.count, 0) + (legend.zero ? legend.zero.count : 0) + (legend.no_data ? legend.no_data.count : 0);
    assert.equal(counted, topo.places.length, `${JSON.stringify(v)}: legend counts do not add up to every place`);
    assert.deepEqual(JSON.parse(JSON.stringify(legend)), legend);
  }
});

test('zero_class: zero gets its own colour and legend entry, the rest are scaled without it', () => {
  const layer = load('geo_id,value\n48201,0\n06037,0\n17031,5\n01001,50\n01003,500');
  const { fills, legend } = paint(layer, { scale: { type: 'quantile', bins: 3, zero_class: true } });
  assert.equal(fills[at('48201')], DEFAULT_THEME.palettes.binary.zero);
  assert.equal(fills[at('06037')], DEFAULT_THEME.palettes.binary.zero);
  assert.notEqual(DEFAULT_THEME.palettes.binary.zero, DEFAULT_THEME.roles.no_data.color, 'zero must not look like no data');
  assert.deepEqual({ text: legend.zero.text, count: legend.zero.count }, { text: 'zero', count: 2 });
  assert.deepEqual(legend.classes.map(c => c.count), [1, 1, 1]);
  assert.equal(fills[at('01003')], '#e5a54a');                                 // top class takes the end of the non-zero ramp
});

test('diverging: the midpoint is exactly the middle colour, and the reach is the same on both sides', () => {
  const layer = load('geo_id,value\n48201,-10\n06037,0\n17031,40');
  const { fills, legend } = paint(layer, { scale: { type: 'diverging', midpoint: 0 } });
  assert.equal(fills[at('06037')], DEFAULT_THEME.palettes.diverging.mid);
  assert.equal(fills[at('17031')], '#ff6b5e');
  assert.notEqual(fills[at('48201')], '#4aa3ff');                              // -10 is only a quarter of the way out
  assert.deepEqual(legend.ticks.map(tk => tk.value), [-40, 0, 40]);
  assert.match(legend.caption, /^diverging around 0/);
});

test('invert flips colours, not the legend: it still reads low to high', () => {
  const layer = load('geo_id,value\n48201,1\n06037,2\n17031,3');
  const a = paint(layer, { scale: { type: 'linear' } }), b = paint(layer, { scale: { type: 'linear', invert: true } });
  assert.equal(a.fills[at('48201')], b.fills[at('17031')]);
  assert.deepEqual(a.legend.ticks.map(tk => tk.value), b.legend.ticks.map(tk => tk.value));
  assert.equal(a.legend.stops[0].color, b.legend.stops[10].color);
});

test('presence and its inverse: "exists" means the value is not empty', () => {
  const layer = load('geo_id,value\n48201,7\n06037,');
  const a = paint(layer, { measure: 'presence', scale: { type: 'binary' } });
  const lit = a.fills[at('48201')], dark = a.fills[at('06037')];
  assert.notEqual(lit, dark);
  assert.equal(a.fills[at('17031')], dark);                                    // no row at all is also empty
  assert.deepEqual(a.legend.classes.map(c => [c.text, c.count]), [['has data', 1]]);
  assert.deepEqual([a.legend.zero.text, a.legend.zero.count], ['empty', topo.places.length - 1]);
  const b = paint(layer, { measure: 'presence', scale: { type: 'binary', invert: true } });
  assert.equal(b.fills[at('48201')], dark); assert.equal(b.fills[at('06037')], lit);
  assert.deepEqual(b.legend.classes.map(c => [c.text, c.count]), [['empty', topo.places.length - 1]]);
});

test('categorical: codes take labels from the header, colours from the theme list', () => {
  const layer = load('geo_id,value\n48201,2\n06037,1\n17031,2', { header: { categories: { 1: 'Rural', 2: 'Urban' } } });
  const { fills, legend } = paint(layer, { scale: { type: 'categorical' } });
  assert.equal(fills[at('06037')], DEFAULT_THEME.palettes.categorical[0]);
  assert.equal(fills[at('48201')], DEFAULT_THEME.palettes.categorical[1]);
  assert.deepEqual(legend.classes.map(c => [c.text, c.count]), [['Rural', 1], ['Urban', 2]]);
});

test('a fixed domain clamps, and the legend says how many places sit beyond it', () => {
  const s = buildScale(F([1, 5, 50]), { type: 'linear', domain: [0, 10] });
  assert.deepEqual(Array.from(s.t), [0.1, 0.5, 1]);
  assert.match(s.legend.notes[0], /1 places sit beyond/);
});

test('colour: ramps hit their stops exactly, blend in between, and refuse bad hex', () => {
  const r = ramp(['#000000', '#ffffff']);
  assert.equal(r(0), '#000000'); assert.equal(r(1), '#ffffff'); assert.equal(r(-3), '#000000'); assert.equal(r(NaN), '#000000');
  assert.match(r(0.5), /^#([0-9a-f]{2})\1\1$/);                                // a grey
  assert.notEqual(r(0.5), '#808080');                                          // perceptual middle, not the sRGB middle
  assert.equal(ramp(['#ABC'])(0.7), '#aabbcc');
  for (const h of ['#3f7f86', '#e5a54a', '#0b0f14', '#ffffff']) assert.equal(oklabToHex(hexToOklab(h)), h);
  assert.throws(() => ramp(['teal']), /not a hex colour/);
  assert.throws(() => paint(load('geo_id,value\n48201,1'), {}, overlay(DEFAULT_THEME, { palettes: { sequential: null } })), /no "sequential" palette/);
});

test('number formats: the contract examples, negatives, and no guessing at a bad string', () => {
  assert.equal(makeFormatter('$,.3s')(4731145), '$4.73M');
  assert.equal(makeFormatter('$,.3s')(999999), '$1.00M');
  assert.equal(makeFormatter('.3s')(980), '980');
  assert.equal(makeFormatter('.2s')(0.0042), '4.2m');
  assert.equal(makeFormatter(',.0f')(8400), '8,400');
  assert.equal(makeFormatter('$,.0f')(-120000), '-$120,000');
  assert.equal(makeFormatter(',.2f')(1234567.891), '1,234,567.89');
  assert.equal(makeFormatter('.1%')(0.256), '25.6%');
  assert.equal(makeFormatter(',d')(1999.6), '2,000');
  assert.equal(makeFormatter('.1f')(-0.04), '0.0');                            // no "-0.0"
  assert.equal(makeFormatter(null)(10014009), '10,014,009');
  assert.equal(makeFormatter(null)(0.123456), '0.12');
  assert.equal(makeFormatter(null)(148.806), '148.8');
  assert.equal(makeFormatter(',.0f')(NaN), 'no data');
  assert.equal(makeFormatter(',.0f')(Infinity), 'no data');
  assert.throws(() => makeFormatter('0,0.00'), /not understood/);
});

test('measure returns a copy, so nothing downstream can write into the loaded table', () => {
  const layer = load(TIES);
  const cols = layer.table.byPeriod.latest;
  const v = measureValues(cols, 'value', layer.header, layer.report);
  v[at('48201')] = -1;
  assert.equal(cols.value[at('48201')], 10);
});

test('hit test: geometry, not pixels. Inside, outside, a hole, and a real place', () => {
  const sq = (x, y, w) => [[x, y], [x + w, y], [x + w, y + w], [x, y + w], [x, y]];
  const place = (idx, polygons, bbox) => ({ idx, polygons, bbox });
  const toy = { places: [place(0, [[sq(0, 0, 10), sq(4, 4, 2)]], [0, 0, 10, 10]), place(1, [[sq(4, 4, 2)]], [4, 4, 6, 6]), place(2, [[sq(10, 0, 10)]], [10, 0, 20, 10])] };
  assert.equal(hitTest(toy, 1, 1), 0);
  assert.equal(hitTest(toy, 5, 5), 1);                                         // the hole belongs to the place inside it
  assert.equal(hitTest(toy, 15, 5), 2);
  assert.equal(hitTest(toy, 25, 5), -1);
  assert.deepEqual(unproject({ k: 2, x: 10, y: 20 }, 30, 40), [10, 10]);

  // A real place: the area centroid of a compact shape lies inside it.
  const harris = topo.places[at('48201')];
  const ring = harris.polygons[0][0];
  let A = 0, cx = 0, cy = 0;
  for (let i = 0; i < ring.length - 1; i++) { const f = ring[i][0] * ring[i + 1][1] - ring[i + 1][0] * ring[i][1]; A += f; cx += (ring[i][0] + ring[i + 1][0]) * f; cy += (ring[i][1] + ring[i + 1][1]) * f; }
  assert.equal(hitTest(topo, cx / (3 * A), cy / (3 * A)), harris.idx);
  assert.equal(hitTest(topo, -5000, -5000), -1);
});

test('the full pipe still ends in a plain draw list with one colour per place', () => {
  const { fills } = paint(load(TIES), { measure: 'ratio', scale: { type: 'quantile', bins: 3 } });
  const dl = buildDrawList(topo, DEFAULT_THEME, { fills });
  assert.deepEqual(JSON.parse(JSON.stringify(dl)), dl);
  assert.ok(dl.ops[2].fills.every(c => /^#[0-9a-f]{6}$/.test(c)));
});
