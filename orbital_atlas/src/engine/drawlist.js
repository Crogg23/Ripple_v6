// The draw list: the engine's whole output, as plain data.
// It says WHAT to draw. A painter decides HOW. Nothing in here touches a canvas.
// This wall is what lets a different painter (3D, someday) be swapped in.
//
// Ops, in paint order:
//   { op: 'ground',  color }
//   { op: 'land',    color }                          fill the outline polygons
//   { op: 'places',  fills: string[] }                one colour per place, by idx
//   { op: 'mesh',    which: 'places'|'parents'|'outline', color, opacity, width }
//
// Widths are in screen pixels. The painter divides by zoom.

/**
 * @param {import('../topology/registry.js').Topology} topology
 * @param {Object} theme      a complete theme
 * @param {Object} [state]
 * @param {string[]|null} [state.fills]   colour per place idx; null means no layer loaded
 */
export function buildDrawList(topology, theme, state = {}) {
  const n = topology.places.length;
  const empty = theme.ground.land_empty;
  const fills = new Array(n);
  if (state.fills && state.fills.length !== n) {
    throw new Error(`Draw list got ${state.fills.length} fills for ${n} places.`);
  }
  for (let i = 0; i < n; i++) fills[i] = state.fills && state.fills[i] != null ? state.fills[i] : empty;

  const ops = [
    { op: 'ground', color: theme.ground.background },
    { op: 'land', color: empty },
    { op: 'places', fills }
  ];
  for (const which of ['places', 'parents', 'outline']) {
    const l = theme.lines && theme.lines[which];
    if (l && l.opacity > 0 && l.width > 0 && topology.meshes[which].length) {
      ops.push({ op: 'mesh', which, color: l.color, opacity: l.opacity, width: l.width });
    }
  }
  return { topologyId: topology.id, ops };
}
