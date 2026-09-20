// Slice 1 checks: data in, nothing silent.
import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

import { decodeTopology } from '../src/topology/registry.js';
import { parseText } from '../src/loader/parse.js';
import { loadRows, resolvePeriod, makeHeader } from '../src/loader/load.js';
import { describeReport } from '../src/loader/report.js';
import { sources } from '../src/adapters/sources.js';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const registry = JSON.parse(readFileSync(join(root, 'topologies/registry.json'), 'utf8'));
const entry = registry.topologies.us_counties_2018;
const topo = decodeTopology('us_counties_2018', entry, JSON.parse(readFileSync(join(root, 'topologies', entry.url), 'utf8')));
const at = id => topo.indexById.get(id);
const load = (text, opts = {}) => loadRows(parseText(text).rows, { topology: topo, ...opts });
const words = r => describeReport(r).map(l => l.text).join('\n');

// The three examples from docs/02_CONTRACT.md, word for word.
const MINIMAL = `geo_id,geo_type,period,value
48201,county,latest,4731145
06037,county,latest,10014009`;
const FULL = `geo_id,geo_type,period,value,denominator,n,tier
48201,county,2023,1250000,8400,61,exact
48201,county,2022,980000,8350,60,exact
01001,county,2023,0,210,2,fuzzy`;
const LEAN = `geo_id,geo_type,period,value,denominator
48201,county,2024,-120000,1500000
48453,county,2024,210000,640000`;

test('contract example 1: minimal', () => {
  const { table, report } = load(MINIMAL);
  assert.equal(report.rows_in, 2); assert.equal(report.rows_kept, 2); assert.equal(report.places_covered, 2);
  assert.deepEqual(table.periods, ['latest']);
  assert.equal(table.byPeriod.latest.value[at('06037')], 10014009);
  assert.equal(report.has_denominator, false); assert.equal(report.has_n, false);
  assert.match(words(report), /No denominator: raw view only/);
});

test('contract example 2: denominator, n, tier, two periods', () => {
  const { table, report } = load(FULL);
  assert.deepEqual(table.periods, ['2022', '2023']);
  assert.equal(resolvePeriod(table, 'latest'), '2023');
  assert.equal(resolvePeriod(table, '2022'), '2022');
  assert.equal(resolvePeriod(table, '1999'), null);
  const p = table.byPeriod['2023'];
  assert.equal(p.value[at('48201')], 1250000); assert.equal(p.denominator[at('48201')], 8400);
  assert.equal(p.n[at('01001')], 2); assert.equal(p.tier[at('01001')], 'fuzzy');
  assert.equal(p.value[at('01001')], 0);                         // a real zero
  assert.equal(p.has[at('01001')], 1);
  assert.deepEqual(report.coverage_by_period, { '2022': 1, '2023': 2 });
  assert.equal(report.has_denominator, true); assert.equal(report.has_n, true); assert.equal(report.has_tier, true);
});

test('political-lean case from the contract prose: negative values are allowed', () => {
  const { table, report } = load(LEAN);
  assert.equal(report.rejected.count, 0);
  assert.equal(table.byPeriod['2024'].value[at('48201')], -120000);
});

test('Connecticut planning regions and new Alaska ids are reported as unmatched, by id', () => {
  const { report } = load(`geo_id,value\n09110,5\n09120,6\n02063,7\n02066,8\n09001,9`);
  assert.equal(report.rows_kept, 1);                             // 09001 is in the 2018 list
  assert.equal(report.unmatched.count, 4);
  assert.deepEqual(report.unmatched.sample, ['09110', '09120', '02063', '02066']);
  const w = words(report);
  assert.match(w, /4 rows matched no place on this map: 09110, 09120, 02063, 02066/);
  assert.match(w, /2018 list of places/);
});

test('a duplicate key is rejected and listed by default; the place shows no data', () => {
  const { table, report } = load(`geo_id,period,value\n48201,2023,10\n48201,2023,20\n06037,2023,5`);
  assert.equal(report.duplicates.keys, 1); assert.equal(report.duplicates.count, 2);
  assert.deepEqual(report.duplicates.sample, ['48201|2023']);
  assert.equal(report.rows_kept, 1);
  assert.equal(table.byPeriod['2023'].has[at('48201')], 0);
  assert.match(words(report), /48201 in 2023.*set aside/s);
});

test('duplicates: sum adds value, denominator and n; last keeps the last', () => {
  const text = `geo_id,period,value,denominator,n\n48201,2023,10,100,1\n48201,2023,20,300,2`;
  const s = load(text, { onDuplicate: 'sum' }).table.byPeriod['2023'];
  assert.deepEqual([s.value[at('48201')], s.denominator[at('48201')], s.n[at('48201')]], [30, 400, 3]);
  const l = load(text, { onDuplicate: 'last' }).table.byPeriod['2023'];
  assert.equal(l.value[at('48201')], 20);
  assert.throws(() => load(text, { onDuplicate: 'first' }), /on_duplicate/);
});

test('empty is not zero; zero denominator is kept and counted; bad cells are rejected with a reason and a line', () => {
  const { table, report } = load(`geo_id,value,denominator,n\n48201,,100,\n06037,5,0,\n01001,abc,1,\n01003,5,-2,\n01005,5,1,-1\n,5,1,`);
  const p = table.byPeriod.latest;
  assert.equal(p.has[at('48201')], 1); assert.ok(Number.isNaN(p.value[at('48201')]));
  assert.equal(report.empty_values, 1);
  assert.equal(p.denominator[at('06037')], 0); assert.equal(report.zero_denominators, 1);
  assert.deepEqual(report.rejected.reasons, { value_not_number: 1, denominator_negative: 1, n_negative: 1, geo_id_missing: 1 });
  assert.equal(report.rejected.sample[0].line, 4);
  assert.match(words(report), /Shown as no data, not as zero/);
});

test('every input row lands in exactly one bucket, under all three duplicate policies', () => {
  for (const onDuplicate of ['reject', 'sum', 'last']) {
  const { report } = load(`geo_id,geo_type,period,value
48201,county,2023,9
48201,county,2023,1
48201,county,2023,2
99999,county,2023,3
06037,county,2023,x
48201001000,tract,2023,4
Z1,district,2023,5
06037,County,2023,6`, { knownGeoTypes: ['county', 'tract'], onDuplicate });
  const other = Object.values(report.other_geo_types).reduce((s, v) => s + v, 0) + Object.values(report.unknown_geo_types).reduce((s, v) => s + v, 0);
  assert.equal(report.rows_used + report.rejected.count + report.unmatched.count + report.duplicates.dropped + other, report.rows_in, onDuplicate);
  assert.equal(report.duplicates.count, 3);
  assert.deepEqual([report.rows_used, report.rows_kept, report.duplicates.dropped], { reject: [1, 1, 3], sum: [4, 2, 0], last: [2, 2, 2] }[onDuplicate], onDuplicate);
  assert.deepEqual(report.other_geo_types, { tract: 1 });
  assert.deepEqual(report.unknown_geo_types, { district: 1 });
  assert.match(words(report), /1 row is for "district" places\. No registered map can draw those/);
  }
});

test('a comma is only ever a thousands separator; decimal commas are refused, never reinterpreted', () => {
  const { report, table } = load('geo_id;value;denominator\n48201;12,5;100\n06037;3,25;200\n01001;1,234,567;1\n01003;1,23,4;1\n01005;,5;1\n01007;1,,2;1');
  assert.equal(report.rows_used, 1);
  assert.equal(table.byPeriod.latest.value[at('01001')], 1234567);
  assert.deepEqual(report.rejected.reasons, { value_not_number: 5 });
  assert.match(words(report), /"12,5" is refused/);
});

test('trailing delimiters, a lone geo_id header, short rows, and geo_type case do not lose or mislabel rows', () => {
  const a = load('geo_id,value\n48201,5,\n06037,6,,');
  assert.equal(a.report.rows_used, 2); assert.equal(a.report.rejected.count, 0);
  const b = load('geo_id\n48201');
  assert.equal(b.report.rows_in, 1); assert.equal(b.report.unmatched.count, 0); assert.equal(b.report.empty_values, 1);
  const c = load('geo_id,value,denominator\n48201,5');
  assert.equal(c.report.short_rows, 1); assert.match(words(c.report), /shorter than the header/);
  const d = load('geo_id,geo_type,value\n48201,COUNTY,5');
  assert.equal(d.report.rows_used, 1);
});

test('paste shorthand: no header, a naming header, lost leading zeros, tabs, semicolons, quoted thousands', () => {
  const a = parseText('48201,4731145\n6037,10014009');
  assert.equal(a.shorthand, true); assert.equal(a.labelHint, null); assert.equal(a.rows.length, 2);
  const b = parseText('fips\tPopulation\n48201\t4731145');
  assert.equal(b.labelHint, 'Population'); assert.equal(b.rows.length, 1);
  const c = load('6037;"10,014,009"\n1001;55,869');
  assert.equal(c.report.ids_repaired, 2);
  assert.equal(c.table.byPeriod.latest.value[at('06037')], 10014009);
  assert.match(words(c.report), /2 place ids were repaired/);
  const d = parseText('fips,value\n48201,1');
  assert.equal(d.shorthand, false); assert.equal(d.rows[0].geo_id, '48201');
});

test('an unquoted number with commas is rejected, not split into the wrong columns', () => {
  const { report, table } = load('48201,4,731,145\n06037,5');
  assert.deepEqual(report.rejected.reasons, { too_many_cells: 1 });
  assert.equal(report.rows_kept, 1);
  assert.equal(table.byPeriod.latest.has[at('48201')], 0);
  assert.match(words(report), /unquoted number with commas/);
});

test('aliases map retired ids when the registry declares them, and say so', () => {
  const aliased = { ...topo, entry: { ...entry, aliases: { '46113': '46102' } } };   // Shannon County became Oglala Lakota
  const { report, table } = loadRows(parseText('geo_id,value\n46113,7').rows, { topology: aliased });
  assert.equal(report.aliased.count, 1); assert.equal(report.unmatched.count, 0);
  assert.equal(table.byPeriod.latest.value[at('46102')], 7);
  assert.match(words(report), /46113 -> 46102/);
});

test('adapters: paste, rows, and JSON text all reach the same shape', async () => {
  const p = await sources.paste(MINIMAL).load();
  const r = await sources.rows([{ geo_id: '48201', value: 1 }], { label: 'Host rows' }).load();
  const j = await sources.paste('{"header":{"label":"J"},"rows":[{"geo_id":"48201","value":2}]}').load();
  assert.equal(p.rows.length, 2); assert.equal(r.headerHint.label, 'Host rows'); assert.equal(j.headerHint.label, 'J');
  assert.equal(loadRows(r.rows, { topology: topo }).report.rows_kept, 1);           // numeric cells, not strings
  assert.equal(makeHeader({ label: 'Nursing home fines' }).id, 'nursing_home_fines');
});
