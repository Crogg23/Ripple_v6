// The narrator: the map says what it means in plain sentences, and every sentence is worked out from the table.
import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

import { decodeTopology } from '../src/topology/registry.js';
import { parseText } from '../src/loader/parse.js';
import { loadRows } from '../src/loader/load.js';
import { DEFAULT_THEME, DEFAULT_VIEW, overlay } from '../src/engine/defaults.js';
import { colorize } from '../src/engine/colorize.js';
import { buildReadout } from '../src/engine/readout.js';
import { timesWords, shareWords } from '../src/engine/narrate.js';
import { makeLayer } from '../demo/layers.js';
import { hitTest } from '../src/engine/hit.js';
import { buildOverlay } from '../src/engine/drawlist.js';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const json = rel => JSON.parse(readFileSync(join(root, rel), 'utf8'));
const entry = json('topologies/registry.json').topologies.us_counties_2018;
const topo = decodeTopology('us_counties_2018', entry, json(join('topologies', entry.url)));
const at = id => topo.indexById.get(id);
const tell = (text, view = {}, header) => colorize({ layer: loadRows(parseText(text).rows, { topology: topo, header }), view: overlay(DEFAULT_VIEW, view), theme: DEFAULT_THEME, topology: topo });
const say = (c, id) => buildReadout(at(id), c.model).sentence;

const PASTED = `geo_id,value,denominator
48201,900,100000
06037,40,100000
17031,30,100000
04013,20,100000
01001,10,100000
01003,1,0
01005,,50000`;
const HEAD = { label: 'Cases', denominator: { label: 'People' }, ratio: { label: 'Cases per 100,000 people', per: 100000, format: ',.0f' } };

test('a pasted table gets a headline made from its own numbers: the standout against the typical', () => {
  const { story } = tell(PASTED, { measure: 'ratio' }, HEAD);
  assert.equal(story.headline, 'Harris, Texas stands at 900 cases per 100,000 people. That is about 30 times the typical county.');
  assert.equal(story.lines[0].text, 'The typical county sits at 30. Half are above that, half below.');
  assert.match(story.caveats.join(' '), /These are rates, not counts: cases for every 100,000 people/);
  assert.match(story.caveats.join(' '), /3,137 counties have no number, so they are left blank, never guessed/);
  assert.match(story.caveats.join(' '), /1 of those have a base of zero/);
  assert.deepEqual(JSON.parse(JSON.stringify(story)), story);                   // plain data
});

test('change the question and the words change with it', () => {
  const counts = tell(PASTED, { measure: 'value' }, HEAD).story;
  assert.match(counts.headline, /^Harris, Texas stands at 900 cases\. That is about 45 times/);
  assert.equal(counts.lines.some(l => l.kind === 'concentration'), false);      // six places are too few to call anything concentrated or spread out
  assert.match(counts.caveats.join(' '), /raw counts\. Big counties will look big\. Switch to the rate/);
  const noBase = tell('geo_id,value\n48201,5\n06037,5\n17031,5').story;
  assert.equal(noBase.headline, 'Every county shows the same number: 5.');
  assert.equal(noBase.caveats.some(c => /rate/.test(c)), false);                // no base column, so no talk of rates
});

test('a place describes itself: the raw facts, the rate, and where it stands', () => {
  const c = tell(PASTED, { measure: 'ratio' }, HEAD);
  assert.equal(say(c, '48201'), 'Harris, Texas. 900 cases among 100,000 people, which works out to 900 per 100,000 people. That is the highest of 5 counties, about 30 times the typical county.');
  assert.equal(say(c, '17031'), 'Cook, Illinois. 30 cases among 100,000 people, which works out to 30 per 100,000 people. That is right around the middle, 3 of 5.');
  assert.equal(say(c, '01003'), 'Baldwin, Alabama. 1 case among 0 people. With a base of zero there is no rate to show.');   // "1 case", never "1 cases"
  assert.equal(say(c, '01005'), 'Barbour, Alabama. There is a row for it, but the number is empty.');
  assert.equal(say(c, '56001'), 'Albany, Wyoming. No data here, so it is left blank.');
});

test('zero ties, signed data, and even data each get honest words, not a nonsense multiple', () => {
  const zeros = tell('geo_id,value\n48201,0\n06037,0\n17031,0\n04013,8');
  assert.equal(say(zeros, '48201'), 'Harris, Texas. 0. It shows zero, the same as 2 other counties.');
  assert.match(zeros.story.headline, /^Most counties show nothing at all\. Maricopa, Arizona tops the list at 8\./);
  const signed = tell('geo_id,value\n48201,-40\n06037,2\n17031,60').story;
  assert.equal(signed.headline, 'It runs from -40 to 60. The typical county sits at 2.');
  assert.doesNotMatch(signed.headline + say(tell('geo_id,value\n48201,-40\n06037,2\n17031,60'), '17031'), /times/);
  const even = tell('geo_id,value\n48201,10\n06037,11\n17031,12').story;
  assert.match(even.headline, /^This is fairly even\. The top county is about the same as the typical one\./);
});

test('numbers are said the way people say them', () => {
  assert.equal(timesWords(6.83), 'about 7 times');
  assert.equal(timesWords(2.1), 'about double');
  assert.equal(timesWords(1.05), 'about the same as');
  assert.equal(timesWords(37), 'about 35 times');
  assert.equal(timesWords(340), 'about 350 times');
  assert.equal(timesWords(4200), 'more than 4,000 times');
  assert.equal(shareWords(0.51), 'about half');
  assert.equal(shareWords(0.34), 'about a third');
  assert.equal(shareWords(0.61), '61%');
  assert.equal(shareWords(0.99), 'nearly all');
  // A compact legend format like "$,.3s" prints $4.1M on the legend and "$4.1 million" in a sentence.
  const { rows, header } = makeLayer('payments', topo);
  const c = colorize({ layer: loadRows(rows, { topology: topo, header }), view: DEFAULT_VIEW, theme: DEFAULT_THEME, topology: topo });
  assert.match(c.story.headline, /stands at \$\d+(\.\d)? (million|billion) in payments\./);
  assert.doesNotMatch(c.story.headline + c.story.lines.map(l => l.text).join(' '), /\d[kMG]\b/);
});

test('on a full map it says where the top tenth sits, and whether the total is piled up or spread out', () => {
  const { rows, header } = makeLayer('pulse', topo);
  const layer = loadRows(rows, { topology: topo, header });
  const rate = colorize({ layer, view: overlay(DEFAULT_VIEW, { measure: 'ratio', confidence: { field: 'denominator', low_below: 5000 } }), theme: DEFAULT_THEME, topology: topo });
  const where = rate.story.lines.find(l => l.kind === 'where').text;
  assert.match(where, /of the highest tenth sits in just 3 areas: \w+/);
  assert.match(rate.story.caveats.join(' '), /are small enough that one more or one fewer would swing the number\. They are marked as shaky\./);
  const count = colorize({ layer, view: overlay(DEFAULT_VIEW, { measure: 'value' }), theme: DEFAULT_THEME, topology: topo });
  assert.match(count.story.lines.find(l => l.kind === 'concentration').text, /^Just \d+ of 3,142 counties account for half of all events/);
  // The engine stays domain-free: the noun comes from the map's registry, and falls back to "place".
  const plain = colorize({ layer, view: DEFAULT_VIEW, theme: DEFAULT_THEME, topology: { ...topo, entry: { ...topo.entry, noun: undefined } } });
  assert.match(plain.story.lines[0].text, /^The typical place sits at/);
});

test('every sentence carries its evidence: the places it is about, so a page can light them up', () => {
  const { rows, header } = makeLayer('pulse', topo);
  const c = colorize({ layer: loadRows(rows, { topology: topo, header }), view: overlay(DEFAULT_VIEW, { measure: 'ratio' }), theme: DEFAULT_THEME, topology: topo });
  const { story, model } = c, v = model.values, by = Object.fromEntries(story.lines.map(l => [l.kind, l]));
  assert.deepEqual(story.evidence, [model.order[model.order.length - 1]]);                  // the headline is about the top place
  assert.ok(by.zeros.places.length > 0 && by.zeros.places.every(i => v[i] === 0));
  assert.match(by.zeros.text, new RegExp(`^${by.zeros.places.length} counties show exactly zero`));
  const p90 = v[model.order[Math.floor(0.9 * (model.order.length - 1))]];
  assert.ok(by.standout.places.every(i => v[i] > p90));
  const named = by.where.text.split(': ')[1].replace(/\.$/, '').split(/, | and /);
  assert.ok(by.where.places.every(i => named.includes(topo.parents[topo.parentIndexById.get(topo.places[i].parentId)].name)));
  const state = by.region.text.match(/^Taken as a whole, (.+?) runs highest/)[1];
  assert.ok(by.region.places.length >= 3 && by.region.places.every(i => topo.parents[topo.parentIndexById.get(topo.places[i].parentId)].name === state));
  for (const l of story.lines) assert.ok(l.places.every(i => Number.isInteger(i) && !Number.isNaN(v[i])), l.kind);
});

test('"put together" is total over total, never an average of rates; a region is judged the same way', () => {
  const c = tell('geo_id,value,denominator\n' + topo.places.slice(0, 40).map((p, k) => `${p.id},${k === 0 ? 900 : 10},${k === 0 ? 1000000 : 1000}`).join('\n'), { measure: 'ratio' }, HEAD);
  // One huge place at 90 per 100,000 and 39 tiny ones at 1,000. Total over total is about 124. The average of the rates would be 977.
  const overall = c.story.lines.find(l => l.kind === 'overall').text;
  assert.match(overall, /^Put every county together and it comes to 124\. That is below the typical county: the low ones pull the total down\./);
});

test('a standout that is also one of the smallest places says so, right next to the headline', () => {
  const rows = topo.places.slice(0, 60).map((p, k) => `${p.id},${k === 7 ? 3 : 20 + k},${k === 7 ? 50 : 100000 + k * 1000}`);
  const small = tell('geo_id,value,denominator\n' + rows.join('\n'), { measure: 'ratio' }, HEAD).story;
  assert.match(small.headline, /It is also one of the smallest, with 50 people, so a few cases move it a lot\.$/);
  const big = tell(PASTED, { measure: 'ratio' }, HEAD).story;
  assert.doesNotMatch(big.headline, /one of the smallest/);
});

test('the spread is the legend and the distribution in one: bars in the colours of the map, every place counted once', () => {
  const { rows, header } = makeLayer('payments', topo);
  const c = colorize({ layer: loadRows(rows, { topology: topo, header }), view: DEFAULT_VIEW, theme: DEFAULT_THEME, topology: topo });
  const S = c.legend.spread;
  assert.equal(S.bins.reduce((n, b) => n + b.count, 0), c.model.order.length);
  assert.equal(new Set(S.bins.flatMap(b => b.places)).size, c.model.order.length);
  assert.equal(S.bins[S.bins.length - 1].beyond, true);                                     // a long tail gets one honest last bar, and says so
  assert.match(S.bins[S.bins.length - 1].text, /^above .+, up to /);
  for (const b of S.bins) { assert.equal(b.color === null, b.count === 0); if (b.color) assert.match(b.color, /^#[0-9a-f]{6}$/); }
  assert.ok(S.median >= S.lo && S.median <= S.hi);
  assert.deepEqual(JSON.parse(JSON.stringify(c.legend)), c.legend);
  assert.equal(colorize({ layer: loadRows(parseText('geo_id,value\n48201,2\n06037,1').rows, { topology: topo }), view: overlay(DEFAULT_VIEW, { scale: { type: 'categorical' } }), theme: DEFAULT_THEME, topology: topo }).legend.spread, null);
});

test('the fast hit test agrees with checking every place, and the spotlight veils all but the chosen', () => {
  const slow = (x, y) => { for (const p of topo.places) { if (x < p.bbox[0] || x > p.bbox[2] || y < p.bbox[1] || y > p.bbox[3]) continue; if (hitTest({ places: [{ ...p, idx: 0 }] }, x, y) === 0) return p.idx; } return -1; };
  let seed = 11, hits = 0;
  const rnd = () => (seed = (seed * 1103515245 + 12345) % 2147483648) / 2147483648;
  const [x0, y0, x1, y1] = topo.bbox;
  for (let k = 0; k < 600; k++) { const x = x0 - 20 + rnd() * (x1 - x0 + 40), y = y0 - 20 + rnd() * (y1 - y0 + 40); const a = hitTest(topo, x, y); assert.equal(a, slow(x, y), `at ${x}, ${y}`); if (a >= 0) hits++; }
  assert.ok(hits > 150, `only ${hits} of 600 probes landed on a place`);
  assert.deepEqual(buildOverlay(DEFAULT_THEME, { spotlight: [3, 9], pinned: 4, hover: 7 }).map(o => [o.op, o.keep || o.places]), [['veil', [3, 9]], ['outlines', [4]], ['outlines', [7]]]);
  assert.deepEqual(buildOverlay(DEFAULT_THEME, { spotlight: [], pinned: -1, hover: -1 }), []);
});

// ---- Found by the skeptic on 2026-09-20. Each of these was a sentence that read well and was false. ----

test('a sentence only claims a share it has counted: ties at zero used to turn nine in ten into "eight in ten"', () => {
  const rows = topo.places.slice(0, 100).map((p, k) => `${p.id},${k < 30 ? 0 : k}`);
  const c = tell('geo_id,value' + '\n' + rows.join('\n'));
  const line = c.story.lines.find(l => l.kind === 'standout'), v = c.model.values, live = c.model.order;
  const [, lo, hi] = line.text.match(/fall between (\d+) and (\d+)/).map(Number);
  const inside = live.filter(i => v[i] >= lo && v[i] <= hi).length;
  assert.match(line.text, new RegExp(`^${['', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine'][Math.round(inside / live.length * 10)]} in ten fall between`));
  assert.equal(inside, 90);                                                                 // ninety of a hundred, which the old sentence called "eight in ten"
  assert.match(line.text, new RegExp(`The ${line.places.length} above ${hi} are where to look first`));
  assert.ok(line.places.every(i => v[i] > hi));
});

test('"half above, half below" is only said when it is true; heavy ties at the middle are counted out loud', () => {
  const rows = topo.places.slice(0, 100).map((p, k) => `${p.id},${k < 70 ? 5 : 6 + k}`);
  const typical = tell('geo_id,value' + '\n' + rows.join('\n')).story.lines.find(l => l.kind === 'typical');
  assert.equal(typical.text, 'The typical county sits at 5. 70 sit exactly there, 30 above and 0 below.');
  assert.equal(typical.places.length, 70);
});

test('when every place shows the same number, it says that one thing and stops: no top tenth, no region, no spread', () => {
  const zeros = tell('geo_id,value' + '\n' + topo.places.slice(0, 50).map(p => `${p.id},0`).join('\n')).story;
  assert.equal(zeros.headline, 'Every county shows the same number: 0.');
  assert.deepEqual(zeros.lines, []);
  assert.match(zeros.caveats.join(' '), /3,092 counties have no number/);
  const one = tell('geo_id,value' + '\n' + '48201,7').story;
  assert.equal(one.headline, 'Only one county has a number: Harris, Texas, at 7.');
  assert.deepEqual(one.lines, []);                                                          // it used to call one place of one "spread out"
});

test('"one of the smallest" needs a real small end: equal bases never trigger it, and an unnamed number never leaks a placeholder', () => {
  const same = topo.places.slice(0, 60).map((p, k) => `${p.id},${k === 7 ? 900 : 20 + k},1000`);
  assert.doesNotMatch(tell('geo_id,value,denominator' + '\n' + same.join('\n'), { measure: 'ratio' }, HEAD).story.headline, /one of the smallest/);
  const unnamed = tell('geo_id,value' + '\n' + topo.places.slice(0, 100).map((p, k) => `${p.id},${k < 84 ? 1 : 500}`).join('\n')).story;
  const all = [unnamed.headline, ...unnamed.lines.map(l => l.text), ...unnamed.caveats].join(' ');
  assert.doesNotMatch(all, /your layer/i);
  assert.match(all, /Just \d+ of 100 counties account for half of the total\./);
});

test('the words for size only ever go up as the number goes up, and a fraction is only named when it is close', () => {
  const size = w => (w === 'about the same as' ? 1 : w === 'about double' ? 2 : Number(w.replace(/[^0-9.]/g, '')));
  let last = 0;
  for (let x = 1; x < 5000; x *= 1.013) { const n = size(timesWords(x)); assert.ok(n >= last, `${x} -> "${timesWords(x)}" after ${last}`); last = n; }
  assert.equal(timesWords(2.24), 'about double'); assert.equal(timesWords(2.6), 'about 3 times');
  assert.equal(shareWords(0.0833), '8%');                                                   // not "about a tenth"
  assert.equal(shareWords(0.1), 'about a tenth');
  assert.equal(hitTest(topo, NaN, NaN), -1);
  assert.equal(hitTest(topo, Infinity, 3), -1);
});
