// Which place is under a point. Plain geometry in map units: a box check, then even-odd ray casting.
// No pixels are read, so there are no blended edge colours to misread.

function inRing(ring, x, y) {
  let inside = false;
  for (let i = 0, j = ring.length - 1; i < ring.length; j = i++) {
    const [xi, yi] = ring[i], [xj, yj] = ring[j];
    if ((yi > y) !== (yj > y) && x < ((xj - xi) * (y - yi)) / (yj - yi) + xi) inside = !inside;
  }
  return inside;
}

/** Holes are rings too, so even-odd across all rings of a polygon handles them. */
export function inPolygon(rings, x, y) {
  let inside = false;
  for (const ring of rings) if (inRing(ring, x, y)) inside = !inside;
  return inside;
}

const grids = new WeakMap();
const BUCKET = 24;

/** Places filed by the grid squares their boxes touch. Built once per map. A lookup then checks a handful, not thousands. */
function gridOf(topology) {
  let g = grids.get(topology);
  if (g) return g;
  const [x0, y0, x1, y1] = topology.bbox;
  const cols = Math.max(1, Math.ceil((x1 - x0) / BUCKET)), rows = Math.max(1, Math.ceil((y1 - y0) / BUCKET));
  const cells = Array.from({ length: cols * rows }, () => []);
  for (const p of topology.places) {
    const c0 = Math.max(0, Math.floor((p.bbox[0] - x0) / BUCKET)), c1 = Math.min(cols - 1, Math.floor((p.bbox[2] - x0) / BUCKET));
    const r0 = Math.max(0, Math.floor((p.bbox[1] - y0) / BUCKET)), r1 = Math.min(rows - 1, Math.floor((p.bbox[3] - y0) / BUCKET));
    for (let r = r0; r <= r1; r++) for (let c = c0; c <= c1; c++) cells[r * cols + c].push(p.idx);
  }
  g = { x0, y0, cols, rows, cells };
  grids.set(topology, g);
  return g;
}

/** @returns {number} place index, or -1 */
export function hitTest(topology, x, y) {
  if (!Number.isFinite(x) || !Number.isFinite(y)) return -1;
  const list = topology.bbox ? (() => {
    const g = gridOf(topology), c = Math.floor((x - g.x0) / BUCKET), r = Math.floor((y - g.y0) / BUCKET);
    return c < 0 || r < 0 || c >= g.cols || r >= g.rows ? [] : g.cells[r * g.cols + c];
  })() : topology.places.map(p => p.idx);
  for (const idx of list) {
    const p = topology.places[idx], b = p.bbox;
    if (x < b[0] || x > b[2] || y < b[1] || y > b[3]) continue;
    for (const poly of p.polygons) if (inPolygon(poly, x, y)) return p.idx;
  }
  return -1;
}

/** Screen point to map point, under a { k, x, y } transform. */
export function unproject(t, sx, sy) { return [(sx - t.x) / t.k, (sy - t.y) / t.k]; }
