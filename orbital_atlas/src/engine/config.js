// Config checks. A view or theme is plain JSON; this file says, in plain words, what is wrong with one.
// Unknown fields are kept and never dropped, so a newer config survives an older engine.
// The word lists here are the single source. The JSON Schema files in configs/schema repeat them, and a test holds the two together.

import { DEFAULT_THEME, overlay } from './defaults.js';
import { MEASURES } from './measure.js';
import { SCALE_TYPES } from './scale.js';
import { HIGHLIGHT_RULES, CONFIDENCE_FIELDS } from './roles.js';
import { normalizeHex } from './color.js';

export const VIEW_SCHEMA = 'orbital.view/1';
export const THEME_SCHEMA = 'orbital.theme/1';

export const WORDS = {
  measure: [...MEASURES, 'difference', 'ratio_ab'],
  scale_type: SCALE_TYPES,
  ties: ['share', 'spread'],
  highlight_rule: HIGHLIGHT_RULES,
  confidence_field: CONFIDENCE_FIELDS,
  frame_type: ['national', 'parent', 'places', 'neighbors', 'path'],
  on_click: ['focus_parent', 'select', 'none'],
  readout_key: ['value', 'denominator', 'ratio', 'n', 'tier', 'rank'],
  texture: ['none', 'grain', 'paper', 'blueprint'],
  encoding: ['fill', 'dots', 'hatch', 'stipple', 'bars', 'contour', 'ridge', 'current'],
  size_encoding: ['dots', 'bars'],
  built_encoding: ['fill', 'stipple', 'hatch', 'contour', 'ridge', 'current'],
  field_encoding: ['contour', 'ridge', 'current'],
  ink_under: ['empty', 'ramp'],
  ink_blend: ['source-over', 'lighter', 'multiply', 'screen'],
  light_type: ['flat', 'radial', 'hillshade'],
  glow_on: ['none', 'highlight'],
  role: ['highlight', 'low_confidence', 'no_data', 'hover', 'focus_dim'],
  role_style: {
    highlight: ['accent_fill', 'fill', 'outline', 'hatch', 'dot'],
    low_confidence: ['desaturate', 'hatch', 'dot', 'outline'],
    no_data: ['fill'],
    hover: ['outline'],
    focus_dim: ['veil']
  }
};
export const ZOOM_MS_CAP = 400;

/** A block written as null, a string, or a list cannot be read field by field. Say so in words and stop there. */
function brokenBlocks(out, config, names) {
  for (const k of names) {
    const v = config[k];
    if (v === null || typeof v !== 'object' || Array.isArray(v)) out.push(`"${k}" must be a block of settings like { ... }. Got ${v === null ? 'null' : JSON.stringify(v)}. Leave it out to take the defaults.`);
  }
  return out.length > 0;
}

const oneOf = (out, where, v, list) => { if (!list.includes(v)) out.push(`${where} is "${v}". Choices: ${list.join(', ')}.`); };

/** @returns {string[]} problems, in plain words. Empty means the view is sound. */
export function checkView(view) {
  const out = [];
  if (view.schema !== VIEW_SCHEMA) out.push(`This view says schema "${view.schema}". This engine reads "${VIEW_SCHEMA}".`);
  if (brokenBlocks(out, view, ['scale', 'highlight', 'confidence', 'filter', 'frame', 'readout'])) return out;
  oneOf(out, 'measure', view.measure, WORDS.measure);
  const s = view.scale || {};
  oneOf(out, 'scale.type', s.type, WORDS.scale_type);
  oneOf(out, 'scale.ties', s.ties, WORDS.ties);
  oneOf(out, 'highlight.rule', view.highlight.rule, WORDS.highlight_rule);
  if (view.highlight.rule !== 'none' && WORDS.highlight_rule.includes(view.highlight.rule) && (typeof view.highlight.value !== 'number' || !Number.isFinite(view.highlight.value))) {
    out.push(`Highlight rule "${view.highlight.rule}" needs highlight.value: a number.`);
  }
  oneOf(out, 'confidence.field', view.confidence.field, WORDS.confidence_field);
  oneOf(out, 'frame.type', view.frame.type, WORDS.frame_type);
  oneOf(out, 'on_click', view.on_click, WORDS.on_click);
  for (const list of ['always', 'on_demand']) for (const k of view.readout[list] || []) oneOf(out, `readout.${list}`, k, WORDS.readout_key);
  if (view.filter.tier_in != null && (!Array.isArray(view.filter.tier_in) || !view.filter.tier_in.length)) out.push('filter.tier_in must be a list of tier names, or null.');
  if (s.type === 'diverging' && typeof s.midpoint !== 'number') out.push('A diverging scale needs scale.midpoint: the number the two colours split around.');
  if (s.type === 'threshold' && !Array.isArray(s.thresholds)) out.push('A threshold scale needs scale.thresholds: a rising list of numbers.');
  if (s.invert && s.type === 'categorical') out.push('A categorical scale has no direction, so scale.invert means nothing on it.');
  return out;
}

function checkHex(out, where, v) { try { normalizeHex(v); } catch { out.push(`${where}: "${v}" is not a hex colour like #1d4253.`); } }

/** @returns {string[]} problems with a complete theme, one that has already been laid over its base. */
export function checkTheme(theme) {
  const out = [];
  if (theme.schema !== THEME_SCHEMA) out.push(`This theme says schema "${theme.schema}". This engine reads "${THEME_SCHEMA}".`);
  if (brokenBlocks(out, theme, ['ground', 'roles', 'light', 'glow', 'lines', 'type', 'motion', 'ink', 'layout'])) return out;
  oneOf(out, 'ink.under', theme.ink.under, WORDS.ink_under);
  oneOf(out, 'ink.blend', theme.ink.blend, WORDS.ink_blend);
  if (!(theme.ink.budget > 0 && theme.ink.budget <= 250000)) out.push(`ink.budget must be a dot count from 1 to 250,000. Got ${JSON.stringify(theme.ink.budget)}.`);
  if (theme.ink.color != null) checkHex(out, 'ink.color', theme.ink.color);
  if (theme.ground.shadow != null) checkHex(out, 'ground.shadow.color', theme.ground.shadow.color);
  oneOf(out, 'ground.texture', theme.ground.texture, WORDS.texture);
  oneOf(out, 'encoding', theme.encoding, WORDS.encoding);
  oneOf(out, 'light.type', theme.light.type, WORDS.light_type);
  oneOf(out, 'glow.on', theme.glow.on, WORDS.glow_on);
  if (theme.light.type === 'hillshade' && theme.light.source !== 'value') out.push('light.source must be "value". Hillshade may only repeat what the colour says.');
  if (typeof theme.motion.zoom_ms !== 'number' || !(theme.motion.zoom_ms >= 0 && theme.motion.zoom_ms <= ZOOM_MS_CAP)) out.push(`motion.zoom_ms must be a number from 0 to ${ZOOM_MS_CAP}. Got ${JSON.stringify(theme.motion.zoom_ms)}.`);
  for (const role of WORDS.role) {
    const r = theme.roles[role];
    if (!r) { out.push(`The theme has no "${role}" role.`); continue; }
    oneOf(out, `roles.${role}.style`, r.style, WORDS.role_style[role]);
    if (r.color != null) checkHex(out, `roles.${role}.color`, r.color);
  }
  const p = theme.palettes || {};
  for (const c of Array.isArray(p.sequential) ? p.sequential : []) checkHex(out, 'palettes.sequential', c);
  for (const c of Array.isArray(p.categorical) ? p.categorical : []) checkHex(out, 'palettes.categorical', c);
  if (p.diverging) for (const c of [...(p.diverging.low || []), p.diverging.mid, ...(p.diverging.high || [])]) checkHex(out, 'palettes.diverging', c);
  if (p.binary) for (const c of [p.binary.zero, ...(p.binary.nonzero || [])]) checkHex(out, 'palettes.binary', c);
  for (const fam of ['sequential', 'diverging', 'binary', 'categorical']) if (!p[fam]) out.push(`The theme has no "${fam}" palette. A complete theme supplies all four.`);
  for (const k of ['background', 'land_empty']) checkHex(out, `ground.${k}`, theme.ground[k]);
  return out;
}

/**
 * Lay a partial theme over its base chain, then over the default. "base" names another theme by id.
 * @param {Object} raw               the theme as written
 * @param {Object<string, Object>} [library]   themes by id, as written
 */
export function resolveTheme(raw, library = {}) {
  const chain = [];
  const seen = new Set();
  for (let t = raw || {}; t; ) {
    chain.unshift(t);
    if (t.base == null) break;
    if (seen.has(t.base)) throw new Error(`Theme "${raw.id}" has a base loop through "${t.base}".`);
    seen.add(t.base);
    if (!library[t.base]) throw new Error(`Theme "${t.id}" builds on "${t.base}", and no theme with that id is registered.`);
    t = library[t.base];
  }
  return chain.reduce((acc, t) => overlay(acc, t), DEFAULT_THEME);
}
