// Scales: numbers in, a palette position per place out, plus a legend model. All plain data, no colours.
//
// Every position is a function of the value alone, so equal values always land on one colour.
// The one exception is ties: "spread", which is what v1 did by accident. It is opt-in and the legend says so.
//
// Positions run low to high. "invert" is applied when colours are looked up, so legends still read low to high.

export const SCALE_TYPES = ['linear', 'log', 'quantile', 'quantize', 'threshold', 'diverging', 'binary', 'categorical'];

const clamp01 = u => (u < 0 ? 0 : u > 1 ? 1 : u);
const classT = (k, K) => (K > 1 ? k / (K - 1) : 0.5);

/** Drop ticks that would print on top of each other. The last tick always survives. */
function thin(ticks, gap = 0.08) {
  const out = [];
  for (const tk of ticks) {
    const prev = out[out.length - 1];
    if (prev && (tk.value === prev.value || tk.t - prev.t < gap)) { if (tk === ticks[ticks.length - 1]) out[out.length - 1] = tk; continue; }
    out.push(tk);
  }
  return out;
}

function memberClasses(K, live, values, klass) {
  const out = Array.from({ length: K }, (_, k) => ({ t: classT(k, K), lo: null, hi: null, count: 0 }));
  live.forEach((i, j) => {
    const c = out[klass[j]], v = values[i];
    c.count++;
    if (c.lo === null || v < c.lo) c.lo = v;
    if (c.hi === null || v > c.hi) c.hi = v;
  });
  return out;
}

/**
 * @param {Float64Array} values      one number per place; NaN means no data
 * @param {Object} [cfg]             the view's scale block
 * @param {Object} [words]           { zero, nonzero } labels for the binary split
 * @returns {{type: string, t: Float64Array, zero: Uint8Array, cat: Int32Array|null, invert: boolean, legend: Object}}
 *   t: position 0..1, NaN for no data.  zero: 1 where the place takes the zero colour.  cat: category index, or -1.
 */
export function buildScale(values, cfg = {}, words = {}) {
  const type = cfg.type || 'quantile';
  if (!SCALE_TYPES.includes(type)) throw new Error(`Scale type "${type}" is not known. Choices: ${SCALE_TYPES.join(', ')}.`);
  const ties = cfg.ties || 'share';
  if (ties !== 'share' && ties !== 'spread') throw new Error(`scale.ties must be share or spread. Got "${ties}".`);
  const bins = cfg.bins == null ? 0 : cfg.bins;
  if (!Number.isInteger(bins) || bins < 0 || bins === 1) throw new Error(`scale.bins must be 0 for smooth, or a whole number of 2 or more. Got ${bins}.`);

  const N = values.length;
  const t = new Float64Array(N).fill(NaN);
  const zero = new Uint8Array(N);
  const notes = [];
  const flip = !!cfg.invert;

  if (type === 'binary') {
    let zeros = 0, others = 0;
    for (let i = 0; i < N; i++) {
      const v = values[i];
      if (Number.isNaN(v)) continue;
      const isZero = v === 0;
      if (isZero) zeros++; else others++;
      if (isZero !== flip) zero[i] = 1; else t[i] = 1;
    }
    const zeroWord = words.zero || 'zero', otherWord = words.nonzero || 'non-zero';
    return {
      type, t, zero, cat: null, invert: false,
      legend: {
        kind: 'classes', basis: 'binary', notes,
        classes: [{ t: 1, lo: null, hi: null, count: flip ? zeros : others, label: flip ? zeroWord : otherWord }],
        zero: { count: flip ? others : zeros, label: flip ? otherWord : zeroWord }
      }
    };
  }

  const pullZero = !!cfg.zero_class && type !== 'categorical';
  const live = [];
  let zeroCount = 0;
  for (let i = 0; i < N; i++) {
    const v = values[i];
    if (Number.isNaN(v)) continue;
    if (pullZero && v === 0) { zero[i] = 1; zeroCount++; continue; }
    live.push(i);
  }
  const zeroEntry = pullZero ? { count: zeroCount, label: words.zero || 'zero' } : null;
  const M = live.length;
  const done = (legend, cat = null) => ({ type, t, zero, cat, invert: flip, legend: { ...legend, notes, zero: zeroEntry } });
  if (!M) return done({ kind: 'classes', basis: type, classes: [] });

  let min = Infinity, max = -Infinity;
  for (const i of live) { const v = values[i]; if (v < min) min = v; if (v > max) max = v; }

  if (type === 'categorical') {
    const codes = [...new Set(live.map(i => values[i]))].sort((a, b) => a - b);
    const at = new Map(codes.map((c, k) => [c, k]));
    const cat = new Int32Array(N).fill(-1);
    const counts = new Array(codes.length).fill(0);
    for (const i of live) { const k = at.get(values[i]); cat[i] = k; t[i] = 0; counts[k]++; }
    return done({ kind: 'classes', basis: 'categorical', classes: codes.map((code, k) => ({ category: k, code, lo: code, hi: code, count: counts[k] })) }, cat);
  }

  if (type === 'quantile') {
    const order = live.map((i, j) => j).sort((a, b) => values[live[a]] - values[live[b]]);   // stable: equal values keep input order
    const sorted = order.map(j => values[live[j]]);
    if (ties === 'spread') notes.push('Ties are spread: equal values can get different colours.');
    if (!bins) {
      if (ties === 'spread') order.forEach((j, r) => { t[live[j]] = M > 1 ? r / (M - 1) : 0.5; });
      else {
        // Each tied group takes its middle rank. Then the lowest group is stretched to 0 and the highest to 1,
        // so the whole palette is used even when the ends are heavy ties.
        const groups = [];
        for (let a = 0; a < M;) {
          let b = a; while (b + 1 < M && sorted[b + 1] === sorted[a]) b++;
          groups.push([a, b, (a + b) / 2]);
          a = b + 1;
        }
        const p0 = groups[0][2], p1 = groups[groups.length - 1][2];
        for (const [a, b, p] of groups) {
          const u = p1 > p0 ? (p - p0) / (p1 - p0) : 0.5;
          for (let r = a; r <= b; r++) t[live[order[r]]] = u;
        }
      }
      // Ticks sit where their value's colour really is, so heavy ties and skew show up as uneven spacing.
      const ticks = [0, 0.1, 0.5, 0.9, 1].map(q => { const r = Math.round(q * (M - 1)); return { t: t[live[order[r]]], value: sorted[r] }; });
      return done({ kind: 'ramp', basis: 'percentile', ticks: thin(ticks) });
    }
    const klass = new Array(M);
    let K = bins;
    if (ties === 'spread') order.forEach((j, r) => { klass[j] = Math.min(K - 1, Math.floor((r * K) / M)); });
    else {
      let cuts = [];
      for (let k = 1; k < K; k++) cuts.push(sorted[Math.floor((k * M) / K)]);
      cuts = [...new Set(cuts)].filter(c => c > sorted[0]);
      if (cuts.length + 1 < K) notes.push(`Equal values share a class, so ${K} classes became ${cuts.length + 1}.`);
      K = cuts.length + 1;
      live.forEach((i, j) => { let k = 0; while (k < cuts.length && values[i] >= cuts[k]) k++; klass[j] = k; });
    }
    live.forEach((i, j) => { t[i] = classT(klass[j], K); });
    return done({ kind: 'classes', basis: 'percentile', classes: memberClasses(K, live, values, klass) });
  }

  if (type === 'threshold') {
    const th = cfg.thresholds;
    if (!Array.isArray(th) || !th.length || th.some(x => typeof x !== 'number' || !Number.isFinite(x)) || th.some((x, k) => k && x <= th[k - 1])) {
      throw new Error('A threshold scale needs scale.thresholds: a rising list of numbers.');
    }
    const K = th.length + 1;
    const classes = Array.from({ length: K }, (_, k) => ({ t: classT(k, K), lo: k ? th[k - 1] : null, hi: k < K - 1 ? th[k] : null, count: 0 }));
    for (const i of live) { let k = 0; while (k < th.length && values[i] >= th[k]) k++; t[i] = classT(k, K); classes[k].count++; }
    return done({ kind: 'classes', basis: 'threshold', classes });
  }

  const dom = cfg.domain;
  if (dom != null && (!Array.isArray(dom) || dom.length !== 2 || !(dom[0] < dom[1]))) throw new Error('scale.domain must be [low, high] with low below high.');

  if (type === 'log') {
    const bad = live.filter(i => values[i] <= 0).length;
    if (bad) throw new Error(`A log scale cannot show zero or negative values, and ${bad} places have them. Turn on zero_class, or pick another scale.`);
    if (dom && dom[0] <= 0) throw new Error('A log scale needs a domain above zero.');
    const [d0, d1] = dom || [min, max];
    const span = Math.log(d1) - Math.log(d0);
    for (const i of live) t[i] = span > 0 ? clamp01((Math.log(values[i]) - Math.log(d0)) / span) : 0.5;
    const ticks = [{ t: 0, value: d0 }];
    for (let e = Math.ceil(Math.log10(d0)); 10 ** e < d1; e++) if (10 ** e > d0 && span > 0) ticks.push({ t: (Math.log(10 ** e) - Math.log(d0)) / span, value: 10 ** e });
    ticks.push({ t: 1, value: d1 });
    return done({ kind: 'ramp', basis: 'log', ticks: span > 0 ? thin(ticks, 0.12) : [{ t: 0.5, value: d0 }] });
  }

  if (type === 'diverging') {
    const mid = cfg.midpoint;
    if (typeof mid !== 'number' || !Number.isFinite(mid)) throw new Error('A diverging scale needs scale.midpoint: the number the two colours split around.');
    // The same reach on both sides, so the midpoint is always the middle colour.
    const reach = dom ? Math.max(Math.abs(dom[0] - mid), Math.abs(dom[1] - mid)) : Math.max(Math.abs(min - mid), Math.abs(max - mid));
    const pos = v => (reach > 0 ? clamp01(0.5 + (v - mid) / (2 * reach)) : 0.5);
    if (!bins) {
      for (const i of live) t[i] = pos(values[i]);
      return done({ kind: 'ramp', basis: 'diverging', midpoint: mid, ticks: reach > 0 ? [{ t: 0, value: mid - reach }, { t: 0.5, value: mid }, { t: 1, value: mid + reach }] : [{ t: 0.5, value: mid }] });
    }
    const K = bins, step = (2 * reach) / K;
    const classes = Array.from({ length: K }, (_, k) => ({ t: classT(k, K), lo: mid - reach + k * step, hi: mid - reach + (k + 1) * step, count: 0 }));
    for (const i of live) { const k = Math.min(K - 1, Math.floor(pos(values[i]) * K)); t[i] = classT(k, K); classes[k].count++; }
    return done({ kind: 'classes', basis: 'diverging', midpoint: mid, classes });
  }

  // linear, and quantize: equal steps across the domain.
  const [d0, d1] = dom || [min, max];
  const pos = v => (d1 > d0 ? clamp01((v - d0) / (d1 - d0)) : 0.5);
  if (dom) {
    const beyond = live.filter(i => values[i] < d0 || values[i] > d1).length;
    if (beyond) notes.push(`${beyond} places sit beyond the ends of the scale and take the end colours.`);
  }
  const K = type === 'quantize' ? bins || 5 : bins;
  if (!K) {
    for (const i of live) t[i] = pos(values[i]);
    const ticks = d1 > d0 ? [0, 0.25, 0.5, 0.75, 1].map(u => ({ t: u, value: d0 + u * (d1 - d0) })) : [{ t: 0.5, value: d0 }];
    return done({ kind: 'ramp', basis: 'linear', ticks });
  }
  const step = (d1 - d0) / K;
  const classes = Array.from({ length: K }, (_, k) => ({ t: classT(k, K), lo: d0 + k * step, hi: d0 + (k + 1) * step, count: 0 }));
  for (const i of live) { const k = Math.min(K - 1, Math.floor(pos(values[i]) * K)); t[i] = classT(k, K); classes[k].count++; }
  return done({ kind: 'classes', basis: 'equal steps', classes });
}
