// Roles: the view says WHO is called out or shaky. The theme says HOW that looks. This file is the "who".
// Every rule is a function of the value alone, so tied places are flagged together or not at all.

export const HIGHLIGHT_RULES = ['none', 'percentile_above', 'percentile_below', 'top_n', 'bottom_n', 'value_above', 'value_below', 'outlier_iqr', 'outlier_z'];
export const CONFIDENCE_FIELDS = ['n', 'denominator'];

const pct = x => `${Number((x * 100).toFixed(1))}%`;

function quantileOf(sorted, q) {
  const pos = q * (sorted.length - 1), lo = Math.floor(pos), hi = Math.ceil(pos);
  return sorted[lo] + (sorted[hi] - sorted[lo]) * (pos - lo);
}

/**
 * @param {Float64Array} values   the driving measure; NaN is no data
 * @param {{rule: string, value: number|null}} cfg
 * @param {(v: number) => string} fmt
 * @returns {{idx: number[], words: string}|null}   null when the rule is "none"
 */
export function pickHighlight(values, cfg, fmt) {
  const rule = (cfg && cfg.rule) || 'none';
  if (!HIGHLIGHT_RULES.includes(rule)) throw new Error(`Highlight rule "${rule}" is not known. Choices: ${HIGHLIGHT_RULES.join(', ')}.`);
  if (rule === 'none') return null;
  const x = cfg.value;
  if (typeof x !== 'number' || !Number.isFinite(x)) throw new Error(`Highlight rule "${rule}" needs highlight.value: a number.`);

  const live = [];
  for (let i = 0; i < values.length; i++) if (!Number.isNaN(values[i])) live.push(i);
  const sorted = Float64Array.from(live, i => values[i]).sort();
  const M = sorted.length;
  let test = () => false, words;

  if (rule === 'percentile_above' || rule === 'percentile_below') {
    if (!(x > 0 && x < 1)) throw new Error(`Highlight rule "${rule}" needs a value between 0 and 1, such as 0.9. Got ${x}.`);
    const above = rule === 'percentile_above';
    words = above ? `top ${pct(1 - x)}` : `bottom ${pct(x)}`;
    if (M) {
      const cut = above ? sorted[Math.min(M - 1, Math.floor(x * M))] : sorted[Math.max(0, Math.ceil(x * M) - 1)];
      // When the cut lands on the far end, every place would be flagged. Flagging all is flagging none.
      if (above ? cut > sorted[0] : cut < sorted[M - 1]) test = v => (above ? v >= cut : v <= cut);
    }
  } else if (rule === 'top_n' || rule === 'bottom_n') {
    if (!Number.isInteger(x) || x < 1) throw new Error(`Highlight rule "${rule}" needs a whole number of 1 or more. Got ${x}.`);
    const top = rule === 'top_n';
    words = `${top ? 'top' : 'bottom'} ${x}`;
    if (M > x) { const cut = top ? sorted[M - x] : sorted[x - 1]; test = v => (top ? v >= cut : v <= cut); }
    // Asking for the top 10 of 6 places would flag all 6. Flagging all is flagging none.
  } else if (rule === 'value_above') { words = `above ${fmt(x)}`; test = v => v > x; }
  else if (rule === 'value_below') { words = `below ${fmt(x)}`; test = v => v < x; }
  else {
    if (!(x > 0)) throw new Error(`Highlight rule "${rule}" needs a value above zero. Got ${x}.`);
    if (rule === 'outlier_iqr') {
      words = `outliers, beyond ${x} × the middle spread`;
      if (M >= 4) { const q1 = quantileOf(sorted, 0.25), q3 = quantileOf(sorted, 0.75), r = (q3 - q1) * x; test = v => v < q1 - r || v > q3 + r; }
    } else {
      words = `outliers, beyond ${x} standard deviations`;
      if (M >= 2) {
        let mean = 0; for (const v of sorted) mean += v / M;
        let sd = 0; for (const v of sorted) sd += (v - mean) ** 2 / M;
        sd = Math.sqrt(sd);
        if (sd > 0) test = v => Math.abs(v - mean) / sd > x;
      }
    }
  }
  return { idx: live.filter(i => test(values[i])), words };
}

/**
 * Places whose sample or base is too small to trust. Only places that have data can be shaky.
 * @returns {{idx: number[], words: string}|null}   null when the view sets no floor
 */
export function pickLowConfidence(cols, cfg, header, report, shown, fmt) {
  if (!cfg || cfg.low_below == null) return null;
  const field = cfg.field || 'n';
  if (!CONFIDENCE_FIELDS.includes(field)) throw new Error(`confidence.field must be n or denominator. Got "${field}".`);
  if (typeof cfg.low_below !== 'number' || !Number.isFinite(cfg.low_below)) throw new Error('confidence.low_below must be a number.');
  if (field === 'n' ? !report.has_n : !report.has_denominator) throw new Error(`The view marks low confidence by "${field}", and this layer has no ${field} column.`);
  const col = cols[field], idx = [];
  for (let i = 0; i < col.length; i++) if (!Number.isNaN(shown[i]) && col[i] < cfg.low_below) idx.push(i);
  return { idx, words: `low confidence: ${header[field].label.toLowerCase()} under ${fmt(cfg.low_below)}` };
}
