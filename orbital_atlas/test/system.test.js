// The design system: tokens are solved from a look, and readability is proven, never eyeballed.
import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

import { resolveTheme } from '../src/engine/config.js';
import { overlay, DEFAULT_THEME } from '../src/engine/defaults.js';
import { contrast, quiet, luminance } from '../src/engine/color.js';
import { solveTokens, TARGETS } from '../demo/system.js';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const json = rel => JSON.parse(readFileSync(join(root, rel), 'utf8'));
const library = Object.fromEntries(readdirSync(join(root, 'configs/themes')).map(f => json(`configs/themes/${f}`)).map(t => [t.id, t]));
const css = readFileSync(join(root, 'demo/system.css'), 'utf8');

test('contrast maths matches the published WCAG figures', () => {
  assert.equal(Math.round(contrast('#000000', '#ffffff') * 10) / 10, 21);
  assert.equal(contrast('#ffffff', '#ffffff'), 1);
  assert.equal(Math.round(contrast('#777777', '#ffffff') * 100) / 100, 4.48);   // the well-known grey that just fails AA
  assert.equal(contrast('#123456', '#fedcba'), contrast('#fedcba', '#123456'));
  assert.ok(luminance('#ffffff') > luminance('#808080') && luminance('#808080') > luminance('#000000'));
});

test('quiet text is as quiet as it can be and still readable, on light and on dark', () => {
  for (const [ink, ground] of [['#2a2418', '#e9e2d0'], ['#ebf6ff', '#0b0f14'], ['#000000', '#ffffff'], ['#ffffff', '#000000']]) {
    const q = quiet(ink, ground, 4.6);
    assert.ok(contrast(q, ground) >= 4.6, `${q} on ${ground} is ${contrast(q, ground)}`);
    assert.ok(contrast(q, ground) < 5.0, `${q} on ${ground} could be quieter: ${contrast(q, ground)}`);
    assert.ok(contrast(q, ground) < contrast(ink, ground));
  }
  assert.equal(quiet('#777777', '#ffffff', 4.6), '#777777');                     // already under the bar: never made fainter
});

test('EVERY look yields readable tokens: ink 7 to 1, quiet ink 4.5 to 1, signal 3 to 1', () => {
  assert.ok(Object.keys(library).length >= 12);
  for (const id of Object.keys(library)) {
    const { vars, report } = solveTokens(resolveTheme(library[id], library));
    for (const r of report) assert.ok(r.ratio >= r.target, `${id}: ${r.role} ${r.color} is ${r.ratio} to 1 on ${r.on}, needs ${r.target}`);
    assert.ok(contrast(vars['--ink'], vars['--surface']) >= 4.5, `${id}: ink on a raised panel`);
    // Quiet text does not only sit on the page. It sits on raised panels and on hovered rows too. (The skeptic caught this: it was proven on ground alone.)
    for (const back of ['--ground', '--surface', '--wash']) assert.ok(contrast(vars['--ink-2'], vars[back]) >= 4.5, `${id}: quiet ink on ${back} is ${contrast(vars['--ink-2'], vars[back]).toFixed(2)}`);
    assert.ok(contrast(vars['--ground'], vars['--ink']) >= 4.5, `${id}: a solid button, ground on ink`);
    for (const k of ['--ground', '--surface', '--ink', '--ink-2', '--rule', '--wash', '--signal']) assert.match(vars[k], /^#[0-9a-f]{6}$/, `${id} ${k}`);
    for (const k of ['--f-display', '--f-text', '--f-data']) assert.ok(vars[k].length > 3, `${id} ${k}`);
  }
});

test('a look with unreadable colours gets corrected, and the report says so', () => {
  const faint = solveTokens(overlay(DEFAULT_THEME, { ground: { background: '#f4f1ea' }, lines: { outline: { color: '#d8d2c4' } }, roles: { highlight: { color: '#f0e9d8' } } }));
  const by = Object.fromEntries(faint.report.map(r => [r.role, r]));
  assert.equal(by.ink.corrected, true);
  assert.ok(by.ink.ratio >= TARGETS.ink);
  assert.equal(by.signal.corrected, true);                                       // an invisible call-out colour falls back to ink
  assert.equal(by.signal.color, faint.vars['--ink']);
  const fine = solveTokens(resolveTheme(library.survey, library));
  assert.ok(fine.report.every(r => !r.corrected));
});

test('the stylesheet keeps its own rules: seven sizes, seven gaps, nothing under 11, nothing moves', () => {
  const body = css.slice(css.indexOf('*/') + 2);
  const sizes = [...body.matchAll(/--t\d: (\d+)px/g)].map(m => Number(m[1]));
  assert.deepEqual(sizes, [11, 13, 15, 18, 22, 28, 34]);
  assert.deepEqual([...body.matchAll(/--s\d: (\d+)px/g)].map(m => Number(m[1])), [4, 8, 12, 16, 24, 32, 48]);
  // Every font declaration takes its size from a token (or inherits). A raw pixel size would be an eighth size.
  for (const m of body.matchAll(/font(?:-size)?:\s*([^;}]+)[;}]/g)) assert.doesNotMatch(m[1], /\b\d+(\.\d+)?px\b/, `raw font size in "${m[0]}"`);
  assert.doesNotMatch(body, /transition|animation|@keyframes/);
  // Pages that use the system set no sizes of their own either.
  for (const page of ['story.html', 'system.html']) {
    const style = readFileSync(join(root, 'demo', page), 'utf8').match(/<style>([\s\S]*?)<\/style>/)[1];
    for (const m of style.matchAll(/font(?:-size)?:\s*([^;}]+)[;}]/g)) assert.doesNotMatch(m[1], /\b\d+(\.\d+)?px\b/, `${page}: raw font size in "${m[0]}"`);
    assert.doesNotMatch(style, /#[0-9a-fA-F]{3,6}\b/, `${page} hard-codes a colour`);
  }
});

test('rule 2 is enforced, not just written down: padding, margin and gap take the seven gaps and nothing else', () => {
  const body = css.slice(css.indexOf('*/') + 2);
  const allowed = new Set([0, 1, 2, 4, 8, 12, 16, 24, 32, 48]);                 // 1 and 2 are line weights
  for (const m of body.matchAll(/(?:^|[\s;{])(padding|margin|gap|column-gap|row-gap)(?:-[a-z]+)?:\s*([^;}]+)[;}]/g)) {
    for (const px of m[2].matchAll(/(-?\d+(?:\.\d+)?)px/g)) assert.ok(allowed.has(Math.abs(Number(px[1]))), `"${m[1]}: ${m[2].trim()}" uses ${px[1]}px, which is not one of the seven gaps`);
  }
  // No hard-coded colour outside the fallback tokens at the top. A shadow is the one stated exception, and it is black.
  const afterRoot = body.slice(body.indexOf('}') + 1);
  assert.doesNotMatch(afterRoot, /#[0-9a-fA-F]{3,8}\b/, 'a hex colour is hard-coded inside the system');
  assert.deepEqual([...afterRoot.matchAll(/rgba?\([^)]*\)/g)].map(m => m[0]), ['rgb(0 0 0 / 0.16)']);
  // Every control that takes focus shows it.
  for (const sel of ['.field:focus-visible', '.btn:focus-visible', '.seg button:focus-visible', '.touch:focus-visible']) assert.ok(body.includes(sel), `${sel} has no focus style`);
});
