// Slice 3 checks: configs. Every version of the map is a view plus a theme, read from JSON on disk.
import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

import { decodeTopology } from '../src/topology/registry.js';
import { parseText } from '../src/loader/parse.js';
import { loadRows } from '../src/loader/load.js';
import { DEFAULT_THEME, DEFAULT_VIEW, overlay } from '../src/engine/defaults.js';
import { checkView, checkTheme, resolveTheme, WORDS } from '../src/engine/config.js';
import { colorize } from '../src/engine/colorize.js';
import { buildDrawList, buildOverlay } from '../src/engine/drawlist.js';
import { pickHighlight } from '../src/engine/roles.js';
import { hillshade } from '../src/engine/light.js';
import { desaturate, shade, hexToOklab } from '../src/engine/color.js';
import { makeLayer } from '../demo/layers.js';
import { viewSchema, themeSchema, render } from '../tools/make_schemas.js';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const json = rel => JSON.parse(readFileSync(join(root, rel), 'utf8'));
const registry = json('topologies/registry.json');
const entry = registry.topologies.us_counties_2018;
const topo = decodeTopology('us_counties_2018', entry, json(join('topologies', entry.url)));
const at = id => topo.indexById.get(id);
const F = a => Float64Array.from(a);
const fmt = v => String(v);

const index = json('configs/index.json');
const library = Object.fromEntries(index.themes.map(id => [id, json(`configs/themes/${id}.json`)]));
const theme = id => resolveTheme(library[id], library);
const view = id => overlay(DEFAULT_VIEW, json(`configs/views/${id}.json`));
const layers = {};
const layer = id => layers[id] || (layers[id] = (() => { const { rows, header } = makeLayer(id, topo); return loadRows(rows, { topology: topo, header }); })());
const draw = (v, th) => {
  const c = colorize({ layer: layer(v.layer), view: v, theme: th, topology: topo });
  return { ...c, list: buildDrawList(topo, th, { fills: c.fills, marks: c.marks }) };
};

test('THE ACCEPTANCE TEST: all nine illustration rows load from JSON, pass their checks, and render', () => {
  assert.deepEqual(index.rows.map(r => r.row), ['1', '2', '3', '4', '5', '6', '7', '7b', '8', '9']);
  for (const row of index.rows) {
    const v = view(row.view), th = theme(row.theme);
    assert.deepEqual(checkView(v), [], `row ${row.row} view`);
    assert.deepEqual(checkTheme(th), [], `row ${row.row} theme`);
    if (v.layer === null) {                                                    // row 9, the empty state
      const list = buildDrawList(topo, th, { fills: null });
      assert.ok(list.ops[2].fills.every(c => c === th.ground.land_empty));
      assert.ok(v.empty_message.length > 0);
      continue;
    }
    const { fills, legend, list } = draw(v, th);
    assert.equal(fills.length, topo.places.length);
    assert.ok(new Set(fills).size > 1, `row ${row.row} is one flat colour`);
    assert.ok(fills.every(c => /^#[0-9a-f]{6}$/.test(c)), `row ${row.row} has a bad colour`);
    assert.deepEqual(JSON.parse(JSON.stringify(list)), list, `row ${row.row} draw list is not plain data`);
    assert.deepEqual(JSON.parse(JSON.stringify(legend)), legend);
    assert.ok(legend.title.length > 0);
  }
});

test('what each row promises, it does', () => {
  const r1 = draw(view('01_money'), theme('restraint'));
  assert.equal(r1.legend.roles[0].text, 'top 10%');
  assert.ok(Math.abs(r1.marks.highlight.length - topo.places.length / 10) < 5);
  assert.ok(r1.marks.highlight.every(i => r1.fills[i] === '#e5a54a'));
  assert.equal(r1.fills.filter(c => c === '#e5a54a').length, r1.marks.highlight.length);      // the accent is reserved

  const r2 = draw(view('02_fatalities'), theme('alarm'));
  assert.equal(r2.legend.zero.text, 'zero');
  assert.ok(r2.legend.zero.count > 500);
  assert.match(r2.legend.caption, /^percentile · \d classes/);
  assert.ok(r2.legend.no_data.count > 300);                                   // places with no row, and rows with an empty value
  assert.notEqual(r2.legend.zero.color, r2.legend.no_data.color);

  const v3 = view('03_fines_per_bed'), r3 = draw(v3, theme('ledger'));
  assert.equal(v3.measure_locked, true);
  assert.equal(r3.legend.title, 'Fines per bed');
  assert.equal(r3.legend.unit, '$ per bed');

  const r5 = draw(view('05_overdose'), theme('washed'));
  assert.equal(r5.legend.roles[0].text, 'low confidence: people under 5,000');
  assert.ok(r5.marks.low_confidence.length > 100);
  const cols = layer('overdose_deaths').table.byPeriod.latest;
  assert.ok(r5.marks.low_confidence.every(i => cols.denominator[i] < 5000));
  const chroma = c => Math.hypot(...hexToOklab(c).slice(1));
  const plain = draw(overlay(view('05_overdose'), { confidence: { low_below: null } }), theme('washed'));
  assert.ok(r5.marks.low_confidence.every(i => chroma(r5.fills[i]) <= chroma(plain.fills[i]) + 1e-9), 'a washed place gained colour');
  assert.deepEqual(plain.legend.roles, []);

  const r6 = draw(view('06_lean'), theme('lean'));
  assert.match(r6.legend.caption, /^diverging around 0\.0%/);
  assert.equal(r6.legend.ticks[1].text, '0.0%');
  assert.equal(r6.legend.ticks[0].value, -r6.legend.ticks[2].value);

  const a = draw(view('07_presence'), theme('ledger')), b = draw(view('07b_absence'), theme('ledger'));
  assert.equal(new Set(a.fills).size, 2);
  assert.ok(a.fills.every((c, i) => c !== b.fills[i]), 'the inverse view must flip every place');
  assert.equal(a.legend.classes[0].count + a.legend.zero.count, topo.places.length);
});

test('THE SPLIT: swapping the themes of rows 1 and 4 changes the look, never the meaning', () => {
  for (const v of [view('01_money'), view('04_disputes')]) {
    const dark = draw(v, theme('restraint')), light = draw(v, theme('paper'));
    assert.deepEqual(dark.marks, light.marks);                                 // who is called out
    assert.deepEqual(dark.legend.roles.map(r => [r.text, r.count]), light.legend.roles.map(r => [r.text, r.count]));
    assert.deepEqual(dark.legend.ticks.map(t => [t.t, t.text]), light.legend.ticks.map(t => [t.t, t.text]));
    assert.equal(dark.legend.caption, light.legend.caption);
    assert.deepEqual(dark.model.ranks, light.model.ranks);
    assert.notDeepEqual(dark.fills, light.fills);                              // the look
    // Same role, two looks: the dark theme fills, the light theme outlines.
    assert.equal(dark.list.ops.some(o => o.op === 'outlines'), false);
    const outline = light.list.ops.find(o => o.op === 'outlines');
    assert.deepEqual(outline.places, light.marks.highlight);
    assert.equal(outline.color, '#111111');
    assert.ok(light.list.ops.some(o => o.op === 'texture' && o.kind === 'paper'));
    assert.ok(light.marks.highlight.every(i => light.fills[i] !== '#111111'), 'an outline theme must leave the fill alone');
  }
  const r4 = draw(view('04_disputes'), theme('paper'));
  assert.match(r4.legend.roles[0].text, /^outliers/);
  assert.ok(r4.marks.highlight.length > 20 && r4.marks.highlight.length < 400);
});

test('theme "base": a partial theme lays over its chain; loops and missing bases are refused', () => {
  const t = theme('restraint');
  assert.equal(t.palettes.sequential.length, 4);                               // its own
  assert.deepEqual(t.palettes.binary, library.ledger.palettes.binary);         // from ledger
  assert.equal(t.roles.hover.color, DEFAULT_THEME.roles.hover.color);          // from the default
  assert.equal(DEFAULT_THEME.palettes.sequential.length, 5);                   // nothing was mutated
  assert.throws(() => resolveTheme({ id: 'x', base: 'nope' }, library), /no theme with that id/);
  assert.throws(() => resolveTheme({ id: 'a', base: 'b' }, { a: { id: 'a', base: 'b' }, b: { id: 'b', base: 'a' } }), /base loop/);
  assert.equal(resolveTheme({ id: 'solo', future_field: 7 }).future_field, 7); // unknown fields are kept, never dropped
});

test('checks speak plainly, and catch what a schema alone cannot', () => {
  const v = p => checkView(overlay(DEFAULT_VIEW, p)).join(' ');
  assert.equal(v({}), '');
  assert.match(v({ schema: 'orbital.view/2' }), /This engine reads "orbital.view\/1"/);
  assert.match(v({ measure: 'vibes' }), /measure is "vibes"\. Choices: value, ratio/);
  assert.match(v({ scale: { type: 'diverging' } }), /needs scale\.midpoint/);
  assert.match(v({ scale: { type: 'threshold' } }), /needs scale\.thresholds/);
  assert.match(v({ scale: { type: 'categorical', invert: true } }), /no direction/);
  assert.match(v({ highlight: { rule: 'best' } }), /highlight\.rule is "best"/);
  assert.match(v({ readout: { always: ['mood'] } }), /readout\.always is "mood"/);
  assert.match(v({ filter: { tier_in: [] } }), /tier_in/);
  const t = p => checkTheme(overlay(DEFAULT_THEME, p)).join(' ');
  assert.equal(t({}), '');
  assert.match(t({ motion: { zoom_ms: 900 } }), /zoom_ms must be a number from 0 to 400/);
  assert.match(t({ motion: { zoom_ms: '250' } }), /must be a number from 0 to 400\. Got "250"/);
  // A block written as null is refused in plain words. It never surfaces as a programmer error.
  for (const k of ['scale', 'highlight', 'confidence', 'filter', 'frame', 'readout']) assert.match(checkView({ ...DEFAULT_VIEW, [k]: null }).join(' '), new RegExp(`"${k}" must be a block of settings`));
  for (const k of ['ground', 'roles', 'light', 'glow', 'lines', 'type', 'motion']) assert.match(checkTheme({ ...DEFAULT_THEME, [k]: null }).join(' '), new RegExp(`"${k}" must be a block of settings`));
  assert.match(v({ highlight: { rule: 'top_n', value: null } }), /needs highlight\.value: a number/);
  assert.match(v({ highlight: { rule: 'top_n', value: '10' } }), /needs highlight\.value: a number/);
  assert.match(t({ light: { type: 'hillshade', source: 'n' } }), /may only repeat what the colour says/);
  assert.match(t({ glow: { on: 'everything' } }), /glow\.on is "everything"/);
  assert.match(t({ roles: { highlight: { style: 'veil' } } }), /roles\.highlight\.style is "veil"/);
  assert.match(t({ roles: { highlight: { color: 'gold' } } }), /"gold" is not a hex colour/);
  assert.match(t({ palettes: { diverging: null } }), /no "diverging" palette/);
});

test('cross-checks at draw time: wrong layer, wrong map, size on a rate, unbuilt encodings, tiers', () => {
  const th = theme('ledger'), fines = layer('cms_fines');
  const go = (v, t = th, l = fines, map = topo) => colorize({ layer: l, view: overlay(DEFAULT_VIEW, v), theme: t, topology: map });
  assert.throws(() => go({ layer: 'payments' }), /asks for layer "payments"\. The loaded layer is "cms_fines"/);
  assert.throws(() => go({}, th, fines, { ...topo, id: 'some_other_map' }), /loaded against "us_counties_2018"/);
  assert.throws(() => go({ measure: 'ratio' }, overlay(th, { encoding: 'dots' })), /Size on a rate misleads/);
  assert.throws(() => go({ measure: 'value' }, overlay(th, { encoding: 'dots' })), /not built yet/);
  assert.throws(() => go({ filter: { tier_in: ['exact'] } }), /no tier column/);
  assert.throws(() => go({ confidence: { field: 'n', low_below: 5 } }), /no n column/);
  assert.throws(() => go({ highlight: { rule: 'percentile_above', value: 90 } }), /between 0 and 1/);
  assert.throws(() => go({ highlight: { rule: 'top_n' } }), /needs highlight\.value/);

  const tiered = loadRows(parseText('geo_id,value,tier\n48201,5,exact\n06037,9,fuzzy\n17031,7,exact').rows, { topology: topo });
  const kept = go({ filter: { tier_in: ['exact'] } }, th, tiered);
  assert.equal(kept.fills[at('06037')], th.roles.no_data.color);
  assert.notEqual(kept.fills[at('48201')], th.roles.no_data.color);
  assert.match(kept.legend.notes.join(' '), /Only tier exact is drawn\. 1 places are hidden/);
  assert.equal(kept.model.ranks.of, 2);
});

test('highlight rules: ties are flagged together, and flagging everyone is flagging no one', () => {
  const pick = (vals, rule, value) => pickHighlight(F(vals), { rule, value }, fmt);
  assert.equal(pick([1, 2, 3], 'none', null), null);
  assert.deepEqual(pick([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'percentile_above', 0.9).idx, [9]);
  assert.deepEqual(pick([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'percentile_below', 0.2).idx, [0, 1]);
  assert.deepEqual(pick([5, 9, 9, 9, 1, NaN], 'top_n', 1).idx, [1, 2, 3]);                 // three-way tie for first: all three
  assert.deepEqual(pick([5, 9, 1, 1], 'bottom_n', 1).idx, [2, 3]);
  assert.deepEqual(pick([7, 7, 7, 7], 'percentile_above', 0.9).idx, []);
  assert.deepEqual(pick([1, 2, 3], 'top_n', 99999).idx, []);                               // the top 99999 of 3 is everyone, so no one
  assert.deepEqual(pick([1, 2, 3], 'bottom_n', 3).idx, []);                  // all equal: nobody stands out
  assert.deepEqual(pick([1, 5, 10], 'value_above', 5).idx, [2]);
  assert.deepEqual(pick([1, 5, 10], 'value_below', 5).idx, [0]);
  assert.deepEqual(pick([10, 11, 12, 13, 14, 15, 16, 200], 'outlier_iqr', 1.5).idx, [7]);
  assert.deepEqual(pick([10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 500], 'outlier_z', 3).idx, [11]);
  assert.deepEqual(pick([4, 4, 4], 'outlier_z', 3).idx, []);
  assert.equal(pick([1, 2], 'percentile_above', 0.75).words, 'top 25%');
  assert.equal(pick([1, 2], 'top_n', 10).words, 'top 10');
});

test('every role style reaches the draw list as plain data; glow only ever follows the highlight', () => {
  const v = view('01_money');
  const styled = (role, style, extra = {}) => draw(v, overlay(theme('ledger'), { roles: { [role]: { style, color: '#ff00ff' } }, ...extra }));
  const hatch = styled('highlight', 'hatch');
  assert.deepEqual(hatch.list.ops.find(o => o.op === 'hatch').places, hatch.marks.highlight);
  assert.ok(hatch.list.ops.findIndex(o => o.op === 'hatch') < hatch.list.ops.findIndex(o => o.op === 'mesh'), 'hatching sits under the border lines');
  const dot = styled('highlight', 'dot');
  assert.equal(dot.list.ops.find(o => o.op === 'dots').points.length, dot.marks.highlight.length);
  const glow = styled('highlight', 'accent_fill', { glow: { on: 'highlight' } });
  assert.deepEqual(glow.list.ops.find(o => o.op === 'glow').places, glow.marks.highlight);
  const noOne = draw(overlay(v, { highlight: { rule: 'none' } }), overlay(theme('ledger'), { glow: { on: 'highlight' } }));
  assert.equal(noOne.list.ops.some(o => o.op === 'glow'), false);
  const radial = draw(v, overlay(theme('ledger'), { light: { type: 'radial', strength: 0.5 }, ground: { texture: 'grain' } }));
  assert.deepEqual(radial.list.ops.slice(-2).map(o => o.op), ['light', 'texture']);
  // A place can be shaky and called out at once. Both marks survive.
  const both = draw(overlay(view('05_overdose'), { highlight: { rule: 'percentile_above', value: 0.5 } }), theme('paper'));
  const shared = both.marks.highlight.filter(i => both.marks.low_confidence.includes(i));
  assert.ok(shared.length > 0);
  assert.ok(both.list.ops.some(o => o.op === 'hatch') && both.list.ops.some(o => o.op === 'outlines'));
  assert.equal(both.legend.roles.length, 2);
});

test('hover is an overlay, so the map underneath is not rebuilt', () => {
  assert.deepEqual(buildOverlay(DEFAULT_THEME, { hover: -1 }), []);
  assert.deepEqual(buildOverlay(DEFAULT_THEME, { hover: 7 }), [{ op: 'outlines', places: [7], color: '#ffffff', width: 1.2 }]);
  assert.equal(buildOverlay(theme('paper'), { hover: 7 })[0].color, '#b3261e');
});

test('hillshade repeats the colour: flat ground gets none, a slope is lit on the side facing up-left', () => {
  const flat = hillshade(topo, new Float64Array(topo.places.length).fill(0.5));
  assert.ok(flat.every(s => s === 0));
  // Height rises to the right and down, away from the light: every interior place faces the light.
  const [x0, y0, x1, y1] = topo.bbox;
  const ramp = Float64Array.from(topo.places, p => ((p.bbox[0] - x0) / (x1 - x0) + (p.bbox[1] - y0) / (y1 - y0)) / 2);
  const lit = hillshade(topo, ramp);
  assert.ok(lit.filter(s => s > 0).length > topo.places.length * 0.9);
  const dark = hillshade(topo, ramp.map(h => 1 - h));
  assert.ok(dark.filter(s => s < 0).length > topo.places.length * 0.9);
  // In row 8, shading moves lightness only, never hue, and leaves ranks and legend alone.
  const v = view('08_land_area'), shaded = draw(v, theme('relief')), plain = draw(v, theme('ledger'));
  assert.deepEqual(shaded.legend.ticks, plain.legend.ticks);
  assert.notDeepEqual(shaded.fills, plain.fills);
  assert.match(shaded.legend.notes.join(' '), /shows no second number/);
  assert.equal(shade('#3f7f86', 0), '#3f7f86');
  assert.ok(hexToOklab(shade('#3f7f86', 0.1))[0] > hexToOklab('#3f7f86')[0]);
  assert.equal(desaturate('#3f7f86', 0), '#3f7f86');
  assert.match(desaturate('#3f7f86', 1), /^#([0-9a-f]{2})\1\1$/);
});

test('schema files on disk match the engine word for word; every config on disk passes', () => {
  assert.equal(readFileSync(join(root, 'configs/schema/orbital.view.1.json'), 'utf8'), render(viewSchema()), 'run: node tools/make_schemas.js');
  assert.equal(readFileSync(join(root, 'configs/schema/orbital.theme.1.json'), 'utf8'), render(themeSchema()), 'run: node tools/make_schemas.js');
  assert.deepEqual(viewSchema().properties.scale.properties.type.enum, WORDS.scale_type);
  const viewKeys = new Set(Object.keys(viewSchema().properties)), themeKeys = new Set(Object.keys(themeSchema().properties));
  for (const f of readdirSync(join(root, 'configs/views'))) {
    const raw = json(`configs/views/${f}`);
    for (const k of Object.keys(raw)) assert.ok(k === '$schema' || viewKeys.has(k), `${f}: "${k}" is not a view field`);
    assert.deepEqual(checkView(overlay(DEFAULT_VIEW, raw)), [], f);
  }
  for (const f of readdirSync(join(root, 'configs/themes'))) {
    const raw = json(`configs/themes/${f}`);
    for (const k of Object.keys(raw)) assert.ok(k === '$schema' || themeKeys.has(k), `${f}: "${k}" is not a theme field`);
    assert.deepEqual(checkTheme(resolveTheme(raw, library)), [], f);
    assert.ok(index.themes.includes(raw.id), `${f} is not listed in configs/index.json`);
  }
});

test('configs are flat enough to be warehouse rows: a view and a theme survive a trip through text', () => {
  for (const row of index.rows) {
    const v = json(`configs/views/${row.view}.json`), t = library[row.theme];
    assert.deepEqual(JSON.parse(JSON.stringify(v)), v);
    assert.deepEqual(JSON.parse(JSON.stringify(t)), t);
    assert.equal(typeof v.id, 'string'); assert.equal(typeof t.id, 'string');
  }
});
