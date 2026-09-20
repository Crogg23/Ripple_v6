// Slice 0 checks. Run from the orbital_atlas folder:  node --test test/
import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

import { decodeTopology, cleanId, parentIdOf } from '../src/topology/registry.js';
import { buildDrawList } from '../src/engine/drawlist.js';
import { fit, project } from '../src/engine/frame.js';
import { DEFAULT_THEME, overlay } from '../src/engine/defaults.js';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const registry = JSON.parse(readFileSync(join(root, 'topologies/registry.json'), 'utf8'));
const entry = registry.topologies.us_counties_2018;
const raw = JSON.parse(readFileSync(join(root, 'topologies', entry.url), 'utf8'));
const topo = decodeTopology('us_counties_2018', entry, raw);

test('3,142 places, 51 parents, all with shape, id, and name', () => {
  assert.equal(topo.places.length, 3142);
  assert.equal(topo.parents.length, 51);
  assert.equal(topo.indexById.size, 3142);
  for (const p of topo.places) {
    assert.match(p.id, /^\d{5}$/);
    assert.ok(p.name.length > 0);
    assert.ok(p.polygons.length > 0 && p.polygons[0][0].length >= 4, `no shape for ${p.id}`);
  }
});

test('bounding box is measured, and is not the 0 to 975 box v1 assumed', () => {
  const [x0, y0, x1, y1] = topo.bbox;
  assert.ok(x0 < -50, `x0 was ${x0}`);           // the Aleutians
  assert.ok(x1 > 950 && x1 < 975);
  assert.ok(y0 > 0 && y1 < 610);
  // The file's own bbox is slightly loose, by under half a unit. Ours is measured from the shapes, so it sits inside it.
  assert.ok(x0 >= raw.bbox[0] - 1e-6 && y0 >= raw.bbox[1] - 1e-6 && x1 <= raw.bbox[2] + 1e-6 && y1 <= raw.bbox[3] + 1e-6, 'measured box escapes the file box');
  for (let i = 0; i < 4; i++) assert.ok(Math.abs(topo.bbox[i] - raw.bbox[i]) < 1, `bbox[${i}] is far from the file`);
});

test('every place finds its parent through the registry rule, not hardcoded logic', () => {
  for (const p of topo.places) assert.ok(topo.parentIndexById.has(p.parentId), `${p.id} has no parent ${p.parentId}`);
  assert.equal(parentIdOf('48201', {}, { by: 'prefix', length: 2 }), '48');
  assert.equal(parentIdOf('X1', { region: 'R9' }, { by: 'property', field: 'region' }), 'R9');
  assert.equal(parentIdOf('48201', {}, null), null);
});

test('id rule repairs a lost leading zero', () => {
  assert.equal(cleanId(6037, entry.id_rule), '06037');
  assert.equal(cleanId(' "1001" ', entry.id_rule), '01001');
  assert.equal(cleanId('48201', entry.id_rule), '48201');
});

test('adjacency: Harris County, Texas touches its known neighbours', () => {
  const harris = topo.places[topo.indexById.get('48201')];
  const names = harris.neighbors.map(i => topo.places[i].name);
  for (const n of ['Montgomery', 'Fort Bend', 'Galveston']) assert.ok(names.includes(n), `missing ${n}: ${names}`);
});

test('draw list is plain data: one fill per place, meshes after fills', () => {
  const dl = buildDrawList(topo, DEFAULT_THEME, { fills: null });
  assert.deepEqual(JSON.parse(JSON.stringify(dl)), dl);            // survives JSON, so no functions or canvas objects
  const kinds = dl.ops.map(o => o.op);
  assert.deepEqual(kinds, ['ground', 'land', 'places', 'mesh', 'mesh', 'mesh']);
  const places = dl.ops.find(o => o.op === 'places');
  assert.equal(places.fills.length, 3142);
  assert.ok(places.fills.every(c => c === DEFAULT_THEME.ground.land_empty));   // empty state
});

test('fit keeps the whole measured box on screen, Aleutians included', () => {
  const t = fit(topo.bbox, 1200, 800, 24);
  const [sx0, sy0, sx1, sy1] = project(topo.bbox, t);
  assert.ok(sx0 >= 23.9 && sy0 >= 23.9 && sx1 <= 1176.1 && sy1 <= 776.1, `${[sx0, sy0, sx1, sy1]}`);
});

test('partial themes lay over the default without mutating it', () => {
  const t = overlay(DEFAULT_THEME, { ground: { background: '#fff' } });
  assert.equal(t.ground.background, '#fff');
  assert.equal(t.ground.land_empty, DEFAULT_THEME.ground.land_empty);
  assert.equal(DEFAULT_THEME.ground.background, '#0b0f14');
});

function jsFiles(dir) {
  return readdirSync(dir).flatMap(f => {
    const p = join(dir, f);
    return statSync(p).isDirectory() ? jsFiles(p) : p.endsWith('.js') ? [p.replace(/\\/g, '/')] : [];
  });
}
const ours = jsFiles(join(root, 'src')).filter(p => !p.includes('/vendor/'));

test('the wall: only the painter and the shell mention a canvas', () => {
  for (const p of ours) {
    if (p.includes('/painter/')) continue;
    const code = readFileSync(p, 'utf8').replace(/\/\/.*$/gm, '').replace(/\/\*[\s\S]*?\*\//g, '');
    assert.ok(!/getContext|Path2D|CanvasRendering|\bctx\b/.test(code), `${p} touches canvas`);
  }
});

test('draw list refuses a fills array of the wrong length', () => {
  assert.throws(() => buildDrawList(topo, DEFAULT_THEME, { fills: ['#fff'] }), /fills for 3142 places/);
  const fills = new Array(3142).fill(null); fills[7] = '#123456';
  const dl = buildDrawList(topo, DEFAULT_THEME, { fills });
  assert.equal(dl.ops[2].fills[7], '#123456');
  assert.equal(dl.ops[2].fills[8], DEFAULT_THEME.ground.land_empty);
});

test('motion rule: no timers and no self-restarting animation frames', () => {
  for (const p of ours) {
    const code = readFileSync(p, 'utf8');
    assert.ok(!/setInterval/.test(code), `${p} uses setInterval`);
    assert.ok(!/@keyframes|animation\s*:/.test(code), `${p} declares a CSS animation`);
    assert.ok(!/setTimeout/.test(code), `${p} uses setTimeout`);
  }
  // One animation-frame call site in the whole codebase: the shell's guarded, one-shot paint queue.
  // A new one must be argued for here, not slipped in.
  const sites = ours.flatMap(p => (readFileSync(p, 'utf8').match(/requestAnimationFrame/g) || []).map(() => p));
  assert.equal(sites.length, 1, `animation-frame call sites: ${sites}`);
  assert.ok(sites[0].endsWith('orbital-atlas.js'));
});

test('engine is domain-free: no place names or state codes in src', () => {
  for (const p of ours) {
    const code = readFileSync(p, 'utf8');
    assert.ok(!/Texas|Alaska|county|695662|\b975\b|\b610\b/i.test(code.replace(/\/\/.*$/gm, '')), `${p} knows about a specific place or box`);
  }
});
