// The loader. Every source ends here: rows in, a clean table and a load report out.
// Rule: nothing is dropped, repaired, or set aside without showing up in the report.
// Order of work follows docs/02_CONTRACT.md, "Validation rules, in order".

import { cleanId } from '../topology/registry.js';
import { looksNumeric } from './parse.js';

const SAMPLE = 20;

/** Minimal header for a layer that arrived with none. */
export function makeHeader(partial = {}) {
  const label = partial.label || 'Your layer';
  return {
    schema: 'orbital.layer/1',
    id: partial.id || label.toLowerCase().replace(/[^a-z0-9]+/g, '_').replace(/^_|_$/g, '') || 'layer',
    label,
    source: partial.source || null,
    value: { label, unit: null, format: null, ...(partial.value || {}) },
    denominator: { label: 'Base', unit: null, format: null, ...(partial.denominator || {}) },
    ratio: { label: `${label} per base`, per: 1, unit: null, format: null, ...(partial.ratio || {}) },
    n: { label: 'Records', ...(partial.n || {}) },
    higher_is: partial.higher_is || 'neutral',
    categories: partial.categories || null,
    period_order: partial.period_order || null
  };
}

/** '' and null mean "no data". Returns null for those, NaN for anything that is not a plain finite number. */
function toNumber(raw) {
  if (raw === null || raw === undefined) return null;
  if (typeof raw === 'number') return Number.isFinite(raw) ? raw : NaN;
  const s = String(raw).trim();
  if (s === '') return null;
  if (!looksNumeric(s)) return NaN;
  const v = Number(s.replace(/,/g, ''));
  return Number.isFinite(v) ? v : NaN;
}

function bump(obj, key) { obj[key] = (obj[key] || 0) + 1; }
function sample(arr, item) { if (arr.length < SAMPLE) arr.push(item); }

function sortPeriods(periods, order) {
  if (order && order.length) {
    const rank = new Map(order.map((p, i) => [p, i]));
    return [...periods].sort((a, b) => (rank.has(a) ? rank.get(a) : 1e9) - (rank.has(b) ? rank.get(b) : 1e9) || (a < b ? -1 : 1));
  }
  return [...periods].sort((a, b) => (a === 'latest' ? 1 : b === 'latest' ? -1 : a < b ? -1 : a > b ? 1 : 0));
}

/**
 * @param {Object[]} rows                 raw rows; cells may be strings or numbers
 * @param {Object} opts
 * @param {import('../topology/registry.js').Topology} opts.topology
 * @param {Object} [opts.header]          partial layer header
 * @param {'reject'|'sum'|'last'} [opts.onDuplicate]
 * @param {string[]} [opts.knownGeoTypes] geo_types some registered topology can draw
 * @returns {{header: Object, table: Object, report: Object}}
 */
export function loadRows(rows, opts) {
  const { topology } = opts;
  const entry = topology.entry;
  const activeType = entry.geo_type;
  const onDuplicate = opts.onDuplicate || 'reject';
  if (!['reject', 'sum', 'last'].includes(onDuplicate)) throw new Error(`on_duplicate must be reject, sum, or last. Got "${onDuplicate}".`);
  const known = new Set((opts.knownGeoTypes || [activeType]).map(t => String(t).toLowerCase()));
  const aliases = entry.aliases || {};
  const header = makeHeader(opts.header);

  const report = {
    rows_in: rows.length, rows_used: 0, rows_kept: 0, short_rows: 0,
    places_covered: 0, places_total: topology.places.length,
    topology: topology.id, vintage: entry.vintage ?? null,
    periods: [], coverage_by_period: {},
    ids_repaired: 0,
    unmatched: { count: 0, sample: [] },
    aliased: { count: 0, sample: [] },
    duplicates: { count: 0, keys: 0, dropped: 0, policy: onDuplicate, sample: [] },
    rejected: { count: 0, reasons: {}, sample: [] },
    other_geo_types: {}, unknown_geo_types: {},
    empty_values: 0, zero_denominators: 0,
    has_denominator: false, has_n: false, has_tier: false
  };
  const setAside = {};                       // rows for other known geo_types, kept for drill-down
  const good = [];                           // cleaned rows for the active topology

  for (const r of rows) {
    const line = r._line ?? null;
    if (r._extra) {
      // More cells than columns. Usually a number with commas in it, unquoted. Guessing would put digits in the wrong column.
      report.rejected.count++; bump(report.rejected.reasons, 'too_many_cells'); sample(report.rejected.sample, { line, geo_id: String(r.geo_id ?? ''), why: 'too_many_cells' }); continue;
    }
    if (r._short) report.short_rows++;
    const rawId = r.geo_id;
    if (rawId === undefined || rawId === null || String(rawId).trim() === '') {
      report.rejected.count++; bump(report.rejected.reasons, 'geo_id_missing'); sample(report.rejected.sample, { line, why: 'geo_id_missing' }); continue;
    }
    const geoType = r.geo_type === undefined || r.geo_type === '' || r.geo_type === null ? activeType : String(r.geo_type).trim().toLowerCase();
    const period = r.period === undefined || r.period === '' || r.period === null ? 'latest' : String(r.period).trim();

    const value = toNumber(r.value);
    const denominator = toNumber(r.denominator);
    const n = toNumber(r.n);
    let why = null;
    if (Number.isNaN(value)) why = 'value_not_number';
    else if (Number.isNaN(denominator)) why = 'denominator_not_number';
    else if (denominator !== null && denominator < 0) why = 'denominator_negative';
    else if (Number.isNaN(n)) why = 'n_not_number';
    else if (n !== null && n < 0) why = 'n_negative';
    if (why) {
      report.rejected.count++; bump(report.rejected.reasons, why);
      sample(report.rejected.sample, { line, geo_id: String(rawId), why });
      continue;
    }

    const tier = r.tier === undefined || r.tier === null || r.tier === '' ? null : String(r.tier);
    if (geoType !== activeType) {
      const bucket = known.has(geoType) ? report.other_geo_types : report.unknown_geo_types;
      bump(bucket, geoType);
      if (known.has(geoType)) (setAside[geoType] = setAside[geoType] || []).push({ geo_id: String(rawId).trim(), geo_type: geoType, period, value, denominator, n, tier });
      continue;
    }

    const typed = String(rawId).trim().replace(/^"|"$/g, '');
    let id = cleanId(rawId, entry.id_rule);
    if (id !== typed) report.ids_repaired++;
    let idx = topology.indexById.get(id);
    if (idx === undefined && aliases[id] !== undefined && topology.indexById.has(aliases[id])) {
      report.aliased.count++; sample(report.aliased.sample, `${id} -> ${aliases[id]}`);
      id = aliases[id]; idx = topology.indexById.get(id);
    }
    if (idx === undefined) {
      report.unmatched.count++; sample(report.unmatched.sample, id);
      continue;
    }
    good.push({ idx, id, period, value, denominator, n, tier });
  }

  // Duplicates: same place, same period.
  const byKey = new Map();
  for (const g of good) {
    const key = `${g.id}|${g.period}`;
    if (!byKey.has(key)) byKey.set(key, []);
    byKey.get(key).push(g);
  }
  const kept = [];
  for (const [key, group] of byKey) {
    if (group.length === 1) { kept.push(group[0]); continue; }
    report.duplicates.keys++; report.duplicates.count += group.length; sample(report.duplicates.sample, key);
    if (onDuplicate === 'reject') report.duplicates.dropped += group.length;
    if (onDuplicate === 'last') { kept.push(group[group.length - 1]); report.duplicates.dropped += group.length - 1; }
    else if (onDuplicate === 'sum') {
      const add = f => group.some(g => g[f] !== null) ? group.reduce((s, g) => s + (g[f] ?? 0), 0) : null;
      kept.push({ ...group[0], value: add('value'), denominator: add('denominator'), n: add('n'), tier: group.every(g => g.tier === group[0].tier) ? group[0].tier : null });
    }
    // 'reject': none of the group is kept. The place shows as no data.
  }

  // Build the table: one set of columns per period, aligned to the topology's place order.
  const N = topology.places.length;
  const periods = sortPeriods(new Set(kept.map(k => k.period)), header.period_order);
  const byPeriod = {};
  for (const p of periods) {
    byPeriod[p] = {
      has: new Uint8Array(N),
      value: new Float64Array(N).fill(NaN),
      denominator: new Float64Array(N).fill(NaN),
      n: new Float64Array(N).fill(NaN),
      tier: new Array(N).fill(null)
    };
  }
  const covered = new Uint8Array(N);
  for (const k of kept) {
    const col = byPeriod[k.period];
    col.has[k.idx] = 1; covered[k.idx] = 1;
    if (k.value === null) report.empty_values++; else col.value[k.idx] = k.value;
    if (k.denominator !== null) { col.denominator[k.idx] = k.denominator; report.has_denominator = true; if (k.denominator === 0) report.zero_denominators++; }
    if (k.n !== null) { col.n[k.idx] = k.n; report.has_n = true; }
    if (k.tier !== null) { col.tier[k.idx] = k.tier; report.has_tier = true; }
  }
  // rows_kept: place-and-period cells in the table. rows_used: input rows that reached it. They differ only when duplicates are summed.
  report.rows_kept = kept.length;
  report.rows_used = good.length - report.duplicates.dropped;
  report.periods = periods;
  for (const p of periods) report.coverage_by_period[p] = byPeriod[p].has.reduce((s, v) => s + v, 0);
  report.places_covered = covered.reduce((s, v) => s + v, 0);

  return { header, table: { geo_type: activeType, topology: topology.id, periods, byPeriod, setAside }, report };
}

/** Which period a view setting points at. "latest" means the last one in sort order. */
export function resolvePeriod(table, wanted) {
  if (!table.periods.length) return null;
  if (!wanted || wanted === 'latest') return table.periods.includes('latest') ? 'latest' : table.periods[table.periods.length - 1];
  return table.periods.includes(wanted) ? wanted : null;
}
