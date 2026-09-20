// Stipple: value as dot density. Dots per unit of area rise with a place's position on the scale,
// so a big empty place and a small empty place look equally empty. Density is the honest reading; dot count is not.
// Every dot position is seeded by its place, so dots never move when the view changes. Nothing shimmers.

import { inPolygon } from './hit.js';

function areaOf(polygons) {
  let total = 0;
  for (const poly of polygons) poly.forEach((ring, k) => {
    let a = 0;
    for (let i = 0; i < ring.length - 1; i++) a += ring[i][0] * ring[i + 1][1] - ring[i + 1][0] * ring[i][1];
    total += (k ? -1 : 1) * Math.abs(a / 2);
  });
  return Math.max(0, total);
}

/**
 * @param {Object} topology
 * @param {Float64Array} position   0..1 per place, NaN where there is nothing to draw
 * @param {{budget: number, gamma: number}} ink   total dots across the map, and how hard density leans toward the top
 * @returns {{idx: number, points: number[]}[]}   flat x, y pairs in map units, one run per place that got dots
 */
export function stipple(topology, position, ink) {
  const places = topology.places;
  const want = new Float64Array(places.length);
  let total = 0;
  for (const p of places) {
    const u = position[p.idx];
    if (Number.isNaN(u) || u <= 0) continue;
    want[p.idx] = u ** ink.gamma * areaOf(p.polygons);
    total += want[p.idx];
  }
  if (!total) return [];
  const runs = [];
  for (const p of places) {
    if (!want[p.idx]) continue;
    let seed = (p.idx * 2654435761 + 97) % 2147483648;
    const rnd = () => (seed = (seed * 1103515245 + 12345) % 2147483648) / 2147483648;
    const exact = (want[p.idx] / total) * ink.budget;
    const n = Math.floor(exact) + (rnd() < exact - Math.floor(exact) ? 1 : 0);
    if (!n) continue;
    const [x0, y0, x1, y1] = p.bbox;
    const points = [];
    for (let tries = 0; points.length < n * 2 && tries < n * 40; tries++) {
      const x = x0 + rnd() * (x1 - x0), y = y0 + rnd() * (y1 - y0);
      if (p.polygons.some(poly => inPolygon(poly, x, y))) points.push(Math.round(x * 100) / 100, Math.round(y * 100) / 100);
    }
    if (points.length) runs.push({ idx: p.idx, points });
  }
  return runs;
}
