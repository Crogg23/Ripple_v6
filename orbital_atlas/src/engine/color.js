// Palette maths, hand-written. Blending happens in Oklab, so a ramp's midpoint looks like a midpoint.
// Colours in and out are hex strings, so everything stays plain data.

const toLinear = c => (c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4);
const toGamma = c => (c <= 0.0031308 ? 12.92 * c : 1.055 * c ** (1 / 2.4) - 0.055);

/** '#abc' or '#aabbcc' -> '#aabbcc', lower case. Anything else is refused. */
export function normalizeHex(hex) {
  const m = /^#([0-9a-f]{3}|[0-9a-f]{6})$/i.exec(String(hex).trim());
  if (!m) throw new Error(`"${hex}" is not a hex colour like #1d4253.`);
  const h = m[1].length === 3 ? m[1].replace(/./g, c => c + c) : m[1];
  return '#' + h.toLowerCase();
}

export function hexToOklab(hex) {
  const h = normalizeHex(hex);
  const [r, g, b] = [1, 3, 5].map(i => toLinear(parseInt(h.slice(i, i + 2), 16) / 255));
  const l = Math.cbrt(0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b);
  const m = Math.cbrt(0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b);
  const s = Math.cbrt(0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b);
  return [
    0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
    1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
    0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s
  ];
}

export function oklabToHex([L, a, b]) {
  const l = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3;
  const m = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3;
  const s = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3;
  const rgb = [
    4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
    -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
    -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s
  ];
  return '#' + rgb.map(c => Math.round(255 * Math.min(1, Math.max(0, toGamma(c)))).toString(16).padStart(2, '0')).join('');
}

/**
 * A ramp: position 0..1 in, hex out. Stops are evenly spaced unless positions are given.
 * A position that lands on a stop returns that stop exactly.
 */
export function ramp(colors, positions) {
  if (!Array.isArray(colors) || !colors.length) throw new Error('A palette needs at least one colour.');
  const hexes = colors.map(normalizeHex);
  const labs = hexes.map(hexToOklab);
  const pos = positions || hexes.map((_, i) => (hexes.length === 1 ? 0 : i / (hexes.length - 1)));
  return t => {
    if (hexes.length === 1 || !(t > 0)) return hexes[0];
    if (t >= 1) return hexes[hexes.length - 1];
    let j = 0;
    while (j < pos.length - 2 && t > pos[j + 1]) j++;
    const u = (t - pos[j]) / (pos[j + 1] - pos[j]);
    if (u <= 0) return hexes[j];
    if (u >= 1) return hexes[j + 1];
    return oklabToHex(labs[j].map((c, k) => c + (labs[j + 1][k] - c) * u));
  };
}

/** The ramp a scale family paints with. A theme must supply the family, or the engine says which one is missing. */
export function familyRamp(palettes, family) {
  const p = palettes && palettes[family];
  if (!p) throw new Error(`The theme has no "${family}" palette.`);
  if (family === 'diverging') return ramp([...p.low, p.mid, ...p.high]);
  if (family === 'binary') return ramp(p.nonzero);
  return ramp(p);
}

/** Pull a colour toward grey by amount 0..1, keeping its lightness. */
export function desaturate(hex, amount) {
  const [L, a, b] = hexToOklab(hex);
  const keep = 1 - Math.min(1, Math.max(0, amount));
  return oklabToHex([L, a * keep, b * keep]);
}

/** Lighten or darken by a signed amount of Oklab lightness. Hue is untouched. */
export function shade(hex, amount) {
  if (!amount) return normalizeHex(hex);
  const [L, a, b] = hexToOklab(hex);
  return oklabToHex([Math.min(1, Math.max(0, L + amount)), a, b]);
}

/** WCAG relative luminance of a hex colour. */
export function luminance(hex) {
  const h = normalizeHex(hex);
  const [r, g, b] = [1, 3, 5].map(i => toLinear(parseInt(h.slice(i, i + 2), 16) / 255));
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

/** WCAG contrast ratio between two colours, 1 to 21. Body text wants 4.5 or more; large type and marks want 3. */
export function contrast(a, b) {
  const la = luminance(a), lb = luminance(b);
  return (Math.max(la, lb) + 0.05) / (Math.min(la, lb) + 0.05);
}

/**
 * The quietest version of an ink that can still be read on a ground: blend ink toward ground, but stop
 * while the contrast is still at or above the target. Quiet text is a design choice. Unreadable text is a bug.
 */
export function quiet(ink, ground, target = 4.6) {
  const blend = ramp([ground, ink]);
  let lo = 0, hi = 1;
  if (contrast(ink, ground) <= target) return normalizeHex(ink);
  for (let k = 0; k < 14; k++) { const mid = (lo + hi) / 2; if (contrast(blend(mid), ground) >= target) hi = mid; else lo = mid; }
  return blend(hi);
}
