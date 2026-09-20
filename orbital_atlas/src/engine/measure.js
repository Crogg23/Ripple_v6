// Which number drives the colour. The source never sends a rate: the engine divides, here and only here.
// NaN means no data. It is never zero, and a rate is never infinity.

export const MEASURES = ['value', 'ratio', 'denominator', 'n', 'presence'];
const TWO_LAYER = ['difference', 'ratio_ab'];

/** value / denominator * per. No data when either side is missing or the base is zero. */
export function ratioOf(value, denominator, per = 1) {
  if (Number.isNaN(value) || Number.isNaN(denominator) || denominator === 0) return NaN;
  return (value / denominator) * per;
}

/**
 * @param {{value: Float64Array, denominator: Float64Array, n: Float64Array}} cols   one period's columns
 * @param {string} which
 * @param {Object} header
 * @param {Object} report    the load report, which knows what the layer carries
 * @returns {Float64Array}
 */
export function measureValues(cols, which, header, report) {
  if (TWO_LAYER.includes(which)) throw new Error(`Measure "${which}" needs a second layer. Two-layer views are not built yet.`);
  if (!MEASURES.includes(which)) throw new Error(`Measure "${which}" is not known. Choices: ${MEASURES.join(', ')}.`);
  if ((which === 'ratio' || which === 'denominator') && !report.has_denominator) {
    throw new Error(`This layer has no denominator, so "${which}" cannot be drawn. Switch the measure to value.`);
  }
  if (which === 'n' && !report.has_n) throw new Error('This layer has no n column, so "n" cannot be drawn. Switch the measure to value.');

  const N = cols.value.length;
  if (which === 'value' || which === 'denominator' || which === 'n') return Float64Array.from(cols[which]);
  const out = new Float64Array(N);
  if (which === 'presence') {
    // "Exists" means the value is not empty. A row with an empty value is still no data.
    for (let i = 0; i < N; i++) out[i] = Number.isNaN(cols.value[i]) ? 0 : 1;
    return out;
  }
  const per = header.ratio && Number.isFinite(header.ratio.per) ? header.ratio.per : 1;
  for (let i = 0; i < N; i++) out[i] = ratioOf(cols.value[i], cols.denominator[i], per);
  return out;
}

/** Label, unit, and format string for a measure, straight from the layer header. */
export function measureMeta(which, header) {
  if (which === 'presence') return { label: `${header.label}: where data exists`, unit: null, format: null };
  if (which === 'n') return { label: header.n.label, unit: null, format: header.n.format || null };
  const part = header[which];
  return { label: part.label, unit: part.unit || null, format: part.format || null };
}
