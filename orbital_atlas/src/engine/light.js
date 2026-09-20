// Faked hillshade. The height of a place is its position on the scale, so the shading can only ever
// repeat what the colour already says. It can never carry a second variable.
// The light sits up and to the left. A place that rises away from the light catches it; one that rises toward it is in shadow.

const LIGHT = [-Math.SQRT1_2, -Math.SQRT1_2];
const GAIN = 2.5;

/**
 * @param {Object} topology
 * @param {Float64Array} height   0..1 per place, NaN where there is no surface
 * @returns {Float64Array}        -1 (shadow) .. 1 (lit), 0 where flat or unknown
 */
export function hillshade(topology, height) {
  const places = topology.places;
  const out = new Float64Array(places.length);
  const mid = b => [(b[0] + b[2]) / 2, (b[1] + b[3]) / 2];
  for (const p of places) {
    const h = height[p.idx];
    if (Number.isNaN(h)) continue;
    const [cx, cy] = mid(p.bbox);
    let gx = 0, gy = 0, n = 0;
    for (const j of p.neighbors) {
      const hj = height[j];
      if (Number.isNaN(hj)) continue;
      const [nx, ny] = mid(places[j].bbox);
      const dx = nx - cx, dy = ny - cy, len = Math.hypot(dx, dy);
      if (!len) continue;
      gx += ((hj - h) * dx) / len; gy += ((hj - h) * dy) / len; n++;
    }
    if (!n) continue;
    const toward = (gx * LIGHT[0] + gy * LIGHT[1]) / n;           // how fast the ground rises toward the light
    out[p.idx] = Math.max(-1, Math.min(1, -toward * GAIN));
  }
  return out;
}
