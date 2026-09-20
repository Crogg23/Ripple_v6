// The readout: everything known about one place, as plain data. The shell turns it into DOM.
//
// Rule the view cannot switch off: when the layer has a denominator, the raw value, the base, and the ratio
// are all in the readout. A view can promote rows to "always". It cannot remove them.

import { ratioOf } from './measure.js';
import { makeFormatter, NO_DATA } from './format.js';
import { describePlace } from './narrate.js';

/** Rank 1 is the highest value. Equal values share a rank. Places with no data get rank 0. */
export function rankAll(values) {
  const N = values.length;
  const live = [];
  for (let i = 0; i < N; i++) if (!Number.isNaN(values[i])) live.push(i);
  live.sort((a, b) => values[b] - values[a]);
  const rank = new Int32Array(N), tied = new Int32Array(N);
  for (let a = 0; a < live.length;) {
    let b = a; while (b + 1 < live.length && values[live[b + 1]] === values[live[a]]) b++;
    for (let r = a; r <= b; r++) { rank[live[r]] = a + 1; tied[live[r]] = b - a + 1; }
    a = b + 1;
  }
  return { rank, tied, of: live.length };
}

/**
 * @param {number} idx      place index
 * @param {Object} model    what colorize() kept: topology, header, report, cols, period, values, measure, ranks, view
 */
export function buildReadout(idx, model) {
  const { topology, header, report, cols, measure, ranks, view } = model;
  const place = topology.places[idx];
  const parentIdx = place.parentId != null ? topology.parentIndexById.get(place.parentId) : undefined;
  const always = new Set([...(view.readout && view.readout.always || []), measure]);
  const whole = makeFormatter(',.0f');
  const notes = [];
  const rows = [];
  const add = (key, label, text, unit) => rows.push({ key, label, text, unit: unit || null, always: always.has(key), driving: key === measure });

  const v = cols.value[idx], d = cols.denominator[idx];
  add('value', header.value.label, makeFormatter(header.value.format)(v), header.value.unit);
  if (report.has_denominator) {
    add('denominator', header.denominator.label, makeFormatter(header.denominator.format)(d), header.denominator.unit);
    const per = header.ratio && Number.isFinite(header.ratio.per) ? header.ratio.per : 1;
    add('ratio', header.ratio.label, makeFormatter(header.ratio.format)(ratioOf(v, d, per)), header.ratio.unit);
    if (d === 0) notes.push('The base is zero, so there is no rate here.');
  }
  if (report.has_n) add('n', header.n.label, whole(cols.n[idx]), null);
  if (report.has_tier) add('tier', 'Tier', cols.tier[idx] == null ? NO_DATA : String(cols.tier[idx]), null);

  const r = ranks.rank[idx];
  const rank = r
    ? { rank: r, of: ranks.of, tied: ranks.tied[idx], by: measure, always: always.has('rank'),
        text: `${whole(r)} of ${whole(ranks.of)}${ranks.tied[idx] > 1 ? `, tied with ${whole(ranks.tied[idx] - 1)}` : ''}` }
    : null;

  return {
    idx, id: place.id, name: place.name,
    parent: parentIdx !== undefined ? topology.parents[parentIdx].name : null,
    period: model.period, has_data: !!cols.has[idx], rows, rank, notes,
    sentence: describePlace(idx, model)
  };
}
