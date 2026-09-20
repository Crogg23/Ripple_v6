// Fallback theme and view, so the tag draws something with no config at all.
// Partial configs are laid over these.

export const DEFAULT_THEME = {
  schema: 'orbital.theme/1',
  id: 'default',
  ground: { background: '#0b0f14', land_empty: '#18212b', texture: 'none' },
  roles: {
    present: { style: 'fill', color: '#3f7f86' },
    no_data: { style: 'fill', color: '#18212b' }
  },
  lines: {
    places:  { color: '#bedcf0', opacity: 0.12, width: 0.55 },
    parents: { color: '#d7ecfa', opacity: 0.5,  width: 0.9 },
    outline: { color: '#ebf6ff', opacity: 0.7,  width: 0.7 }
  },
  type: {
    display: "Georgia, 'Times New Roman', serif",
    data: "ui-monospace, 'SF Mono', Menlo, monospace",
    numerals: 'tabular'
  },
  motion: { zoom_ms: 250 }
};

export const DEFAULT_VIEW = {
  schema: 'orbital.view/1',
  id: 'empty',
  title: '',
  topology: null,
  layer: null,
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
