// The load report, in words. Shown to the person, never buried in a console.
// Each line is { level, text }. level: 'ok' | 'note' | 'warn'.

const num = v => Number(v).toLocaleString('en-US');
const pl = (c, one, many) => `${num(c)} ${c === 1 ? one : many}`;
const list = (arr, more) => arr.join(', ') + (more > arr.length ? `, and ${num(more - arr.length)} more` : '');

const REASONS = {
  too_many_cells: 'had more cells than columns, often an unquoted number with commas',
  geo_id_missing: 'had no place id',
  value_not_number: 'had a value that is not a plain number; a comma is read only as a thousands separator, so "12,5" is refused',
  denominator_not_number: 'had a denominator that is not a number',
  denominator_negative: 'had a negative denominator',
  n_not_number: 'had an n that is not a number',
  n_negative: 'had a negative n'
};

export function describeReport(report) {
  const out = [];
  const say = (level, text) => out.push({ level, text });

  say(report.rows_used ? 'ok' : 'warn', `${num(report.rows_used)} of ${num(report.rows_in)} rows loaded.`);
  say('ok', `${num(report.places_covered)} of ${num(report.places_total)} places have a row.`);
  if (report.periods.length > 1) say('ok', `${report.periods.length} periods: ${report.periods.join(', ')}.`);

  if (report.unmatched.count) {
    const vintage = report.vintage ? ` This map uses a ${report.vintage} list of places, so newer or retired ids will not match.` : '';
    say('warn', `${pl(report.unmatched.count, 'row', 'rows')} matched no place on this map: ${list(report.unmatched.sample, report.unmatched.count)}.${vintage}`);
  }
  if (report.aliased.count) say('note', `${pl(report.aliased.count, 'row was', 'rows were')} mapped through known id changes: ${list(report.aliased.sample, report.aliased.count)}.`);
  if (report.duplicates.keys) {
    const did = { reject: 'All of them were set aside, so those places show as no data.', sum: 'They were added together, so every one of those rows is in use.', last: `The last row for each was kept and ${num(report.duplicates.dropped)} earlier ${report.duplicates.dropped === 1 ? 'row was' : 'rows were'} dropped.` }[report.duplicates.policy];
    say('warn', `${pl(report.duplicates.keys, 'place-and-period pair', 'place-and-period pairs')} appeared more than once, across ${num(report.duplicates.count)} rows: ${list(report.duplicates.sample.map(k => k.replace('|', ' in ')), report.duplicates.keys)}. ${did}`);
  }
  if (report.rejected.count) {
    const why = Object.entries(report.rejected.reasons).map(([k, c]) => `${num(c)} ${REASONS[k] || k}`).join('; ');
    const where = report.rejected.sample.filter(s => s.line).slice(0, 5).map(s => `line ${s.line}`).join(', ');
    say('warn', `${pl(report.rejected.count, 'row was', 'rows were')} rejected: ${why}.${where ? ` First at ${where}.` : ''}`);
  }
  for (const [t, c] of Object.entries(report.other_geo_types)) say('note', `${pl(c, 'row is', 'rows are')} for "${t}" places, kept aside for that map.`);
  for (const [t, c] of Object.entries(report.unknown_geo_types)) say('warn', `${pl(c, 'row is', 'rows are')} for "${t}" places. No registered map can draw those.`);
  if (report.short_rows) say('note', `${pl(report.short_rows, 'row was', 'rows were')} shorter than the header. The missing cells were read as empty.`);
  if (report.ids_repaired) say('note', `${pl(report.ids_repaired, 'place id was', 'place ids were')} repaired, such as a lost leading zero.`);
  if (report.empty_values) say('note', `${pl(report.empty_values, 'row has', 'rows have')} an empty value. Shown as no data, not as zero.`);
  if (report.zero_denominators) say('warn', `${pl(report.zero_denominators, 'row has', 'rows have')} a denominator of zero. The rate there shows as no data.`);
  say('note', report.has_denominator ? 'Denominator found: raw and rate views are both available.' : 'No denominator: raw view only.');
  say('note', report.has_n ? 'n found: low-confidence marking is available.' : 'No n: confidence marking is off.');
  return out;
}
