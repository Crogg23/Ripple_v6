// Fallback theme and view, so the tag draws something with no config at all.
// Partial configs are laid over these. Every field a config may carry has its default here.

export const DEFAULT_THEME = {
  schema: 'orbital.theme/1',
  id: 'default',
  label: 'Default',
  base: null,
  ground: { background: '#0b0f14', land_empty: '#18212b', texture: 'none', shadow: null },
  palettes: {
    sequential: ['#10202c', '#1d4253', '#3f7f86', '#a9c9b8', '#eef3e6'],
    diverging: { low: ['#4aa3ff', '#1c3f66'], mid: '#0d1117', high: ['#66231f', '#ff6b5e'] },
    binary: { zero: '#3b4856', nonzero: ['#5a3a1e', '#e5a54a'] },
    categorical: ['#4aa3ff', '#e5a54a', '#7bd389', '#ff6b5e', '#b49cff', '#9aa7b2']
  },
  encoding: 'fill',
  // How the non-fill encodings lay ink down. Sizes are screen pixels.
  ink: {
    under: 'empty',                 // what sits beneath the ink: 'empty' land, or the 'ramp' colour dimmed
    budget: 70000, gamma: 2, radius: 0.9, bloom: 0, bloom_strength: 0.8, blend: 'source-over',
    spacing: [9, 2.2], width: 0.9, angle: 45, classes: 6, color: null,
    // Field encodings: contour, ridge, current. The places are melted into one smooth surface first.
    cell: 3, smooth: 3, levels: 12, index_every: 4, rows: 70, amp: 46, count: 3200, steps: 46, opacity: 0.9, fill: null
  },
  layout: { inset: { top: 0, right: 0, bottom: 0, left: 0 }, callout_gutter: 190 },
  roles: {
    highlight:      { style: 'accent_fill', color: '#e5a54a', width: 1.6 },
    low_confidence: { style: 'desaturate', amount: 0.75, color: '#9aa7b2', width: 0.8 },
    no_data:        { style: 'fill', color: '#18212b' },
    hover:          { style: 'outline', color: '#ffffff', width: 1.2 },
    focus_dim:      { style: 'veil', color: '#02050a', amount: 0.6 }
  },
  light: { type: 'flat', strength: 0, source: null },
  glow: { on: 'none', blur: 10 },
  lines: {
    places:  { color: '#bedcf0', opacity: 0.12, width: 0.55 },
    parents: { color: '#d7ecfa', opacity: 0.5,  width: 0.9 },
    outline: { color: '#ebf6ff', opacity: 0.7,  width: 0.7 }
  },
  type: {
    display: "Georgia, 'Times New Roman', serif",
    text: "'Inter', system-ui, -apple-system, 'Segoe UI', sans-serif",
    data: "ui-monospace, 'SF Mono', Menlo, monospace",
    display_weight: 400,
    numerals: 'tabular'
  },
  motion: { zoom_ms: 250 }
};

export const DEFAULT_VIEW = {
  schema: 'orbital.view/1',
  id: 'empty',
  title: '',
  note: null,
  topology: null,
  layer: null,
  layer_b: null,
  period: 'latest',
  measure: 'value',
  measure_locked: false,
  scale: { type: 'quantile', bins: 0, ties: 'share', domain: null, midpoint: null, thresholds: null, zero_class: false, invert: false },
  highlight: { rule: 'none', value: null },
  confidence: { field: 'n', low_below: null },
  filter: { tier_in: null },
  frame: { type: 'national', id: null },
  on_click: 'focus_parent',
  readout: { always: ['value', 'rank'], on_demand: ['denominator', 'ratio', 'n', 'tier'] },
  labels: { top: 0 },
  empty_message: 'No layer loaded.'
};

/** Lay b over a, key by key, without mutating either. Arrays and scalars replace. */
export function overlay(a, b) {
  if (b === undefined) return a;
  if (a === null || b === null || typeof a !== 'object' || typeof b !== 'object' || Array.isArray(a) || Array.isArray(b)) return b;
  const out = { ...a };
  for (const k of Object.keys(b)) out[k] = overlay(a[k], b[k]);
  return out;
}
