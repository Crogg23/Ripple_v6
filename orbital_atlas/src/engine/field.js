// Field encodings: the places are melted into one smooth surface, and the surface is drawn, not the places.
// Three ways to draw it: contour lines, stacked ridgelines, and flow strokes that run along the contours.
//
// Honesty: smoothing blends neighbours, so these show the SHAPE of the data, never one place's number.
// The legend says so, and the readout still reports each place exactly.
// Everything here is seeded and static. The same view always yields the same lines.

import { inPolygon } from './hit.js';

const rasters = new WeakMap();

/** Which place owns each grid cell. Geometry only, so it is worked out once per map and cell size. */
function rasterOf(topology, cell) {
  let byCell = rasters.get(topology);
  if (!byCell) rasters.set(topology, (byCell = new Map()));
  if (byCell.has(cell)) return byCell.get(cell);
  const [bx0, by0, bx1, by1] = topology.bbox;
  const cols = Math.ceil((bx1 - bx0) / cell) + 1, rows = Math.ceil((by1 - by0) / cell) + 1;
  const owner = new Int32Array(cols * rows).fill(-1);
  for (const p of topology.places) {
    const c0 = Math.max(0, Math.floor((p.bbox[0] - bx0) / cell)), c1 = Math.min(cols - 1, Math.ceil((p.bbox[2] - bx0) / cell));
    const r0 = Math.max(0, Math.floor((p.bbox[1] - by0) / cell)), r1 = Math.min(rows - 1, Math.ceil((p.bbox[3] - by0) / cell));
    for (let r = r0; r <= r1; r++) for (let c = c0; c <= c1; c++) {
      if (owner[r * cols + c] !== -1) continue;
      const x = bx0 + c * cell, y = by0 + r * cell;
      if (p.polygons.some(poly => inPolygon(poly, x, y))) owner[r * cols + c] = p.idx;
    }
  }
  const raster = { x0: bx0, y0: by0, cell, cols, rows, owner };
  byCell.set(cell, raster);
  return raster;
}

function blur(src, cols, rows, radius, passes) {
  let a = src;
  for (let pass = 0; pass < passes * 2; pass++) {
    const b = new Float32Array(a.length).fill(NaN), across = pass % 2 === 0;
    for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) {
      let sum = 0, n = 0;
      for (let d = -radius; d <= radius; d++) {
        const rr = across ? r : r + d, cc = across ? c + d : c;
        if (rr < 0 || cc < 0 || rr >= rows || cc >= cols) continue;
        const v = a[rr * cols + cc];
        if (!Number.isNaN(v)) { sum += v; n++; }
      }
      if (n && (!Number.isNaN(a[r * cols + c]) || pass < 2)) b[r * cols + c] = sum / n;     // the first pass also bleeds a little past the coast, so lines reach it
    }
    a = b;
  }
  return a;
}

/**
 * @param {Object} topology
 * @param {Float64Array} position   0..1 per place, NaN for no data
 * @param {{cell: number, smooth: number}} ink
 */
export function buildField(topology, position, ink) {
  const raster = rasterOf(topology, ink.cell);
  const raw = new Float32Array(raster.owner.length).fill(NaN);
  for (let i = 0; i < raw.length; i++) { const o = raster.owner[i]; if (o >= 0 && !Number.isNaN(position[o])) raw[i] = position[o]; }
  return { ...raster, height: blur(raw, raster.cols, raster.rows, Math.max(1, ink.smooth), 2) };
}

const round = v => Math.round(v * 10) / 10;

/** Marching squares. One set of short segments per level; the painter joins them by eye with round caps. */
export function contours(field, levels) {
  const { cols, rows, cell, x0, y0, height: h } = field;
  return levels.map(level => {
    const seg = [];
    const cut = (ax, ay, av, bx, by, bv) => { const u = (level - av) / (bv - av); return [round(ax + (bx - ax) * u), round(ay + (by - ay) * u)]; };
    for (let r = 0; r < rows - 1; r++) for (let c = 0; c < cols - 1; c++) {
      const a = h[r * cols + c], b = h[r * cols + c + 1], d = h[(r + 1) * cols + c], e = h[(r + 1) * cols + c + 1];
      if (Number.isNaN(a) || Number.isNaN(b) || Number.isNaN(d) || Number.isNaN(e)) continue;
      const X = x0 + c * cell, Y = y0 + r * cell, X1 = X + cell, Y1 = Y + cell;
      const pts = [];
      if ((a < level) !== (b < level)) pts.push(cut(X, Y, a, X1, Y, b));
      if ((b < level) !== (e < level)) pts.push(cut(X1, Y, b, X1, Y1, e));
      if ((d < level) !== (e < level)) pts.push(cut(X, Y1, d, X1, Y1, e));
      if ((a < level) !== (d < level)) pts.push(cut(X, Y, a, X, Y1, d));
      for (let k = 0; k + 1 < pts.length; k += 2) seg.push(pts[k][0], pts[k][1], pts[k + 1][0], pts[k + 1][1]);
    }
    return { level, segments: seg };
  });
}

/** Horizontal slices. Each run is x, y, h triplets over one unbroken stretch of land; h lifts the line when painted. */
export function ridges(field, count) {
  const { cols, rows, cell, x0, y0, height: h, owner } = field;
  const stride = Math.max(1, Math.floor(rows / count)), out = [];
  for (let r = 0; r < rows; r += stride) {
    const runs = [];
    let run = null;
    for (let c = 0; c < cols; c++) {
      const v = h[r * cols + c], land = owner[r * cols + c] >= 0 && !Number.isNaN(v);
      if (land) { if (!run) runs.push((run = [])); run.push(round(x0 + c * cell), round(y0 + r * cell), Math.round(v * 1000) / 1000); }
      else run = null;
    }
    const kept = runs.filter(u => u.length >= 9);
    if (kept.length) out.push({ y: round(y0 + r * cell), runs: kept });
  }
  return out;
}

/** Flow strokes. Each starts at a seeded point on land and walks ALONG the contours, so strokes wrap around highs and lows. */
export function currents(field, ink) {
  const { cols, rows, cell, x0, y0, height: h, owner } = field;
  const at = (x, y) => {
    const c = Math.round((x - x0) / cell), r = Math.round((y - y0) / cell);
    return c < 1 || r < 1 || c >= cols - 1 || r >= rows - 1 ? null : r * cols + c;
  };
  let seed = 9176;
  const rnd = () => (seed = (seed * 1103515245 + 12345) % 2147483648) / 2147483648;
  const strokes = [];
  for (let tries = 0; strokes.length < ink.count && tries < ink.count * 12; tries++) {
    let x = x0 + rnd() * (cols - 1) * cell, y = y0 + rnd() * (rows - 1) * cell;
    const start = at(x, y);
    if (start === null || owner[start] < 0 || Number.isNaN(h[start])) continue;
    const line = [round(x), round(y)];
    for (let s = 0; s < ink.steps; s++) {
      const i = at(x, y);
      if (i === null || Number.isNaN(h[i])) break;
      const gx = h[i + 1] - h[i - 1], gy = h[i + cols] - h[i - cols], len = Math.hypot(gx, gy);
      if (!(len > 1e-5)) break;                                   // dead flat: there is no contour to follow
      x += (-gy / len) * cell * 0.8; y += (gx / len) * cell * 0.8;
      line.push(round(x), round(y));
    }
    if (line.length >= 8) strokes.push({ t: h[start], line });
  }
  return strokes;
}
