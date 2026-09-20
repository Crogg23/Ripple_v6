// The draw list: the engine's whole output, as plain data.
// It says WHAT to draw. A painter decides HOW. Nothing in here touches a canvas.
// This wall is what lets a different painter (3D, someday) be swapped in.
//
// Ops, in paint order:
//   { op: 'ground',   color }
//   { op: 'land',     color, shadow: {color, blur, dx, dy}|null } fill the outline polygons, with an optional soft shadow beneath
//   { op: 'places',   fills: string[] }                         one colour per place, by idx
//   { op: 'glow',     places: number[], color, blur }           a halo behind the listed places; highlight only
//   { op: 'hatch',    places: number[], color, width, spacing, angle, offset } diagonal lines clipped to each listed place
//   { op: 'stipple',  runs: [{color, points}], radius, bloom, bloom_strength, blend }   dots; points are flat x, y pairs in map units
//   { op: 'strokes',  sets: [{color, width, opacity, segments|lines}], clip, blend, bloom }   contour segments or flow polylines, in map units
//   { op: 'ridges',   rows: [{y, runs}], amp, stroke, fill, width, ramp }   stacked slices; each run is x, y, h triplets and h lifts the line
//   { op: 'callouts', items: [{x, y, name, sub, text}], color, display, data }        named places with leader lines
//   { op: 'mesh',     which: 'places'|'parents'|'outline', color, opacity, width }
//   { op: 'outlines', places: number[], color, width }          a hard line round each listed place
//   { op: 'veil',     keep: number[], color, amount }           dim the whole land except the listed places
//   { op: 'dots',     points: [x, y][], color, radius }         one dot per listed place, in map units
//   { op: 'light',    type: 'radial', strength }                static shading over the whole frame
//   { op: 'texture',  kind: 'grain'|'paper'|'blueprint', color } static surface. Never animated.
//
// Widths, radii, blur and spacing are in screen pixels. The painter divides by zoom.

import { stipple } from './stipple.js';
import { buildField, contours, ridges, currents } from './field.js';

const HATCH_SPACING = 5, DOT_RADIUS = 1.6;

/** Turn the ink model from colorize() into ops. Density for stipple, line spacing for hatch. */
function inkOps(topology, theme, ink) {
  if (!ink) return [];
  const opt = theme.ink;
  const position = Float64Array.from(ink.position, u => (u === null ? NaN : u));
  const colorOf = i => opt.color || ink.colors[i];
  const tone = u => ink.ramp[Math.max(0, Math.min(20, Math.round(u * 20)))];
  if (ink.kind === 'contour') {
    const field = buildField(topology, position, opt);
    const levels = Array.from({ length: opt.levels }, (_, k) => (k + 1) / (opt.levels + 1));
    const sets = contours(field, levels).map((c, k) => {
      const index = (k + 1) % opt.index_every === 0;               // every few lines, a heavier one, as on a survey sheet
      return { color: opt.color || tone(c.level), width: opt.width * (index ? 2.1 : 1), opacity: opt.opacity * (index ? 1 : 0.75), segments: c.segments };
    }).filter(s => s.segments.length);
    return sets.length ? [{ op: 'strokes', sets, clip: true, blend: opt.blend, bloom: opt.bloom, bloom_strength: opt.bloom_strength }] : [];
  }
  if (ink.kind === 'ridge') {
    const rows = ridges(buildField(topology, position, opt), opt.rows);
    return rows.length ? [{ op: 'ridges', rows, amp: opt.amp, stroke: opt.color, ramp: opt.color ? null : ink.ramp, fill: opt.fill || theme.ground.background, width: opt.width }] : [];
  }
  if (ink.kind === 'current') {
    const byTone = new Map();
    for (const s of currents(buildField(topology, position, opt), opt)) { const c = opt.color || tone(s.t); if (!byTone.has(c)) byTone.set(c, []); byTone.get(c).push(s.line); }
    const sets = [...byTone].map(([color, lines]) => ({ color, width: opt.width, opacity: opt.opacity, lines }));
    return sets.length ? [{ op: 'strokes', sets, clip: true, blend: opt.blend, bloom: opt.bloom, bloom_strength: opt.bloom_strength }] : [];
  }
  if (ink.kind === 'stipple') {
    const runs = stipple(topology, position, opt).map(r => ({ color: colorOf(r.idx), points: r.points }));
    return runs.length ? [{ op: 'stipple', runs, radius: opt.radius, bloom: opt.bloom, bloom_strength: opt.bloom_strength, blend: opt.blend }] : [];
  }
  // Hatch: places fall into a few bands by position. Higher bands get tighter lines, so they read darker.
  const K = Math.max(2, opt.classes), bands = Array.from({ length: K }, () => []);
  position.forEach((u, i) => { if (!Number.isNaN(u) && u > 0) bands[Math.min(K - 1, Math.floor(u * K))].push(i); });
  const [wide, tight] = opt.spacing;
  return bands.map((places, k) => ({ op: 'hatch', places, color: opt.color || ink.colors[places[0]], width: opt.width, spacing: wide + ((tight - wide) * k) / (K - 1), angle: opt.angle, offset: [0, 0] })).filter(o => o.places.length);
}

function roleOps(topology, role, places) {
  if (!places || !places.length) return [];
  if (role.style === 'outline') return [{ op: 'outlines', places: [...places], color: role.color, width: role.width || 1.2 }];
  if (role.style === 'hatch') return [{ op: 'hatch', places: [...places], color: role.color, width: role.width || 0.8, spacing: role.spacing || HATCH_SPACING, angle: role.angle == null ? 45 : role.angle, offset: role.offset || [0, 0] }];
  if (role.style === 'dot') {
    const points = places.map(i => { const b = topology.places[i].bbox; return [(b[0] + b[2]) / 2, (b[1] + b[3]) / 2]; });
    return [{ op: 'dots', points, color: role.color, radius: DOT_RADIUS }];
  }
  return [];                                   // fill styles were already applied to the fills
}

/**
 * @param {import('../topology/registry.js').Topology} topology
 * @param {Object} theme      a complete theme
 * @param {Object} [state]
 * @param {string[]|null} [state.fills]   colour per place idx; null means no layer loaded
 * @param {{highlight: number[], low_confidence: number[]}} [state.marks]
 */
export function buildDrawList(topology, theme, state = {}) {
  const n = topology.places.length;
  const empty = theme.ground.land_empty;
  const fills = new Array(n);
  if (state.fills && state.fills.length !== n) {
    throw new Error(`Draw list got ${state.fills.length} fills for ${n} places.`);
  }
  for (let i = 0; i < n; i++) fills[i] = state.fills && state.fills[i] != null ? state.fills[i] : empty;
  const marks = state.marks || { highlight: [], low_confidence: [] };
  const roles = theme.roles || {};

  const ops = [
    { op: 'ground', color: theme.ground.background },
    { op: 'land', color: empty, shadow: theme.ground.shadow || null },
    { op: 'places', fills }
  ];
  const inked = inkOps(topology, theme, state.ink);
  ops.push(...inked.filter(o => o.op === 'hatch'));
  // Glow can only ever attach to highlighted places. There is no free-floating glow.
  if (theme.glow && theme.glow.on === 'highlight' && marks.highlight.length && roles.highlight) {
    ops.push({ op: 'glow', places: [...marks.highlight], color: roles.highlight.color, blur: theme.glow.blur || 10 });
  }
  const over = [
    ...(roles.low_confidence ? roleOps(topology, roles.low_confidence, marks.low_confidence) : []),
    ...(roles.highlight ? roleOps(topology, roles.highlight, marks.highlight) : [])
  ];
  ops.push(...over.filter(o => o.op === 'hatch'));
  for (const which of ['places', 'parents', 'outline']) {
    const l = theme.lines && theme.lines[which];
    if (l && l.opacity > 0 && l.width > 0 && topology.meshes[which].length) {
      ops.push({ op: 'mesh', which, color: l.color, opacity: l.opacity, width: l.width });
    }
  }
  ops.push(...inked.filter(o => o.op !== 'hatch'));
  ops.push(...over.filter(o => o.op !== 'hatch'));
  if (theme.light && theme.light.type === 'radial' && theme.light.strength > 0) ops.push({ op: 'light', type: 'radial', strength: theme.light.strength });
  const tex = theme.ground.texture;
  if (tex && tex !== 'none') ops.push({ op: 'texture', kind: tex, color: theme.lines && theme.lines.outline ? theme.lines.outline.color : '#ffffff' });
  // Type goes on last, over the grain, so it stays crisp.
  if (state.labels && state.labels.length) {
    const items = state.labels.map(l => { const b = topology.places[l.idx].bbox; return { x: (b[0] + b[2]) / 2, y: (b[1] + b[3]) / 2, name: l.name, sub: l.parent, text: l.text }; });
    ops.push({ op: 'callouts', items, color: theme.lines.outline.color, display: theme.type.display, data: theme.type.data, gutter: theme.layout.callout_gutter });
  }
  return { topologyId: topology.id, ops };
}

/** What sits on top of the finished map for the moment: the hovered place. Painted over a cached base, so hover is cheap. */
export function buildOverlay(theme, state = {}) {
  const ops = [];
  const dim = theme.roles && theme.roles.focus_dim;
  // Spotlight: the places a sentence is talking about stay lit. Everything else goes under a veil.
  if (dim && state.spotlight && state.spotlight.length) ops.push({ op: 'veil', keep: state.spotlight, color: dim.color, amount: dim.amount });
  const r = theme.roles && theme.roles.hover;
  if (r && state.pinned != null && state.pinned >= 0) ops.push({ op: 'outlines', places: [state.pinned], color: r.color, width: (r.width || 1.2) * 1.6 });
  if (r && state.hover != null && state.hover >= 0) ops.push({ op: 'outlines', places: [state.hover], color: r.color, width: r.width || 1.2 });
  return ops;
}
