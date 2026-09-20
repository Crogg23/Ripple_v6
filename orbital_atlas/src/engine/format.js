// Number formats are strings, so they can live in a saved header. This reads the d3-format subset the
// contract uses:  [$][,][.precision][type]   with type f, d, %, or s.   Examples: "$,.3s"  ",.0f"  ".1%"
// As in d3, f and % default to 6 decimals when no precision is given.
// A format string outside the subset is refused, never guessed at.

const SPEC = /^(\$)?(,)?(?:\.(\d+))?([fd%s])?$/;
const SI = { '-6': 'µ', '-3': 'm', 0: '', 3: 'k', 6: 'M', 9: 'G', 12: 'T' };
export const NO_DATA = 'no data';

function group(digits) {
  const [int, frac] = digits.split('.');
  const g = int.replace(/\B(?=(\d{3})+$)/g, ',');
  return frac === undefined ? g : `${g}.${frac}`;
}

function auto(a) {
  if (Number.isInteger(a)) return group(String(a));
  if (a >= 1000) return group(a.toFixed(0));
  if (a >= 100) return a.toFixed(1);
  if (a >= 1) return a.toFixed(2);
  return String(Number(a.toPrecision(2)));
}

function si(a, p) {
  if (a === 0) return '0';
  let e3 = Math.min(12, Math.max(-6, Math.floor(Math.log10(a) / 3) * 3));
  let s = Number((a / 10 ** e3).toPrecision(p));
  if (s >= 1000 && e3 < 12) { e3 += 3; s = Number((a / 10 ** e3).toPrecision(p)); }
  const decimals = Math.max(0, p - 1 - Math.floor(Math.log10(s)));
  return s.toFixed(decimals) + SI[e3];
}

/** @param {string|null} spec  @returns {(v: number) => string} */
export function makeFormatter(spec) {
  const m = SPEC.exec(spec == null ? '' : String(spec).trim());
  if (!m) throw new Error(`Number format "${spec}" is not understood. Use the shape [$][,][.precision][f|d|%|s], such as "$,.3s".`);
  const [, dollar, comma, prec, type] = m;
  const p = prec === undefined ? null : Number(prec);
  return v => {
    if (typeof v !== 'number' || !Number.isFinite(v)) return NO_DATA;
    const a = Math.abs(v);
    let body;
    if (!type && p === null) body = auto(a);
    else if (type === 's') body = si(a, p === null ? 3 : Math.max(1, p));
    else if (type === 'd') body = a.toFixed(0);
    else if (type === '%') body = (a * 100).toFixed(p === null ? 6 : p);
    else body = a.toFixed(p === null ? 6 : p);
    if (comma && type !== 's') body = group(body);
    const shownZero = Number(body.replace(/[^0-9.]/g, '')) === 0;
    return (v < 0 && !shownZero ? '-' : '') + (dollar ? '$' : '') + body + (type === '%' ? '%' : '');
  };
}
