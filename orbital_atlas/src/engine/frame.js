// Camera maths. A transform is { k, x, y }: screen = map * k + (x, y).

/**
 * Fit a map-space box into a screen of W by H, with padding on each side.
 * @param {[number, number, number, number]} bbox  x0, y0, x1, y1 in map units
 * @param {number} W
 * @param {number} H
 * @param {number} [pad]
 * @param {{top?: number, right?: number, bottom?: number, left?: number}} [inset]   screen space kept clear for type and callouts
 */
export function fit(bbox, W, H, pad = 24, inset = {}) {
  const [x0, y0, x1, y1] = bbox;
  const l = inset.left || 0, r = inset.right || 0, tp = inset.top || 0, b = inset.bottom || 0;
  const w = Math.max(1e-9, x1 - x0), h = Math.max(1e-9, y1 - y0);
  const k = Math.max(1e-9, Math.min((W - l - r - 2 * pad) / w, (H - tp - b - 2 * pad) / h));
  return { k, x: l + (W - l - r - k * (x0 + x1)) / 2, y: tp + (H - tp - b - k * (y0 + y1)) / 2 };
}

/** Where a map-space box lands on screen under a transform. */
export function project(bbox, t) {
  return [bbox[0] * t.k + t.x, bbox[1] * t.k + t.y, bbox[2] * t.k + t.x, bbox[3] * t.k + t.y];
}
