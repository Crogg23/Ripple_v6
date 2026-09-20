// Camera maths. A transform is { k, x, y }: screen = map * k + (x, y).

/**
 * Fit a map-space box into a screen of W by H, with padding on each side.
 * @param {[number, number, number, number]} bbox  x0, y0, x1, y1 in map units
 * @param {number} W
 * @param {number} H
 * @param {number} [pad]
 */
export function fit(bbox, W, H, pad = 24) {
  const [x0, y0, x1, y1] = bbox;
  const w = Math.max(1e-9, x1 - x0), h = Math.max(1e-9, y1 - y0);
  const k = Math.max(1e-9, Math.min((W - 2 * pad) / w, (H - 2 * pad) / h));
  return { k, x: (W - k * (x0 + x1)) / 2, y: (H - k * (y0 + y1)) / 2 };
}

/** Where a map-space box lands on screen under a transform. */
export function project(bbox, t) {
  return [bbox[0] * t.k + t.x, bbox[1] * t.k + t.y, bbox[2] * t.k + t.x, bbox[3] * t.k + t.y];
}
