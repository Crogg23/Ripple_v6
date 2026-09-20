// Host-side scaffolding for the demo and the tests. NOT part of the engine.
// Every number in here is made up, except land_area, which is measured from the shapes themselves.
// The numbers are seeded, so every run and every machine gets the same table.

function rng(seed) { return () => (seed = (seed * 1103515245 + 12345) % 2147483648) / 2147483648; }

function shapeArea(place) {
  let total = 0;
  for (const poly of place.polygons) poly.forEach((ring, k) => {
    let a = 0;
    for (let i = 0; i < ring.length - 1; i++) a += ring[i][0] * ring[i + 1][1] - ring[i + 1][0] * ring[i][1];
    total += (k ? -1 : 1) * Math.abs(a / 2);
  });
  return Math.max(0, total);
}

const MADE_UP = 'Made-up demo numbers. Not real data.';

export const LAYER_HEADERS = {
  payments: { id: 'payments', label: 'Payments', source: MADE_UP, value: { label: 'Payments', unit: '$', format: '$,.3s' } },
  fatalities: { id: 'fatalities', label: 'Fatalities', source: MADE_UP, value: { label: 'Fatalities', format: ',.0f' }, n: { label: 'Incidents' } },
  cms_fines: { id: 'cms_fines', label: 'Fines', source: MADE_UP, value: { label: 'Fines', unit: '$', format: '$,.3s' },
    denominator: { label: 'Beds', unit: 'beds', format: ',.0f' }, ratio: { label: 'Fines per bed', per: 1, unit: '$ per bed', format: '$,.0f' }, higher_is: 'bad' },
  disputes: { id: 'disputes', label: 'Disputes', source: MADE_UP, value: { label: 'Disputes', format: ',.0f' },
    denominator: { label: 'Accounts', format: ',.0f' }, ratio: { label: 'Disputes per 1,000 accounts', per: 1000, format: ',.1f' } },
  overdose_deaths: { id: 'overdose_deaths', label: 'Overdose deaths', source: MADE_UP, value: { label: 'Deaths', format: ',.0f' },
    denominator: { label: 'People', format: ',.0f' }, ratio: { label: 'Deaths per 100,000 people', per: 100000, format: ',.1f' }, higher_is: 'bad' },
  pres_2024: { id: 'pres_2024', label: 'Vote margin', source: MADE_UP, value: { label: 'Vote margin', format: ',.0f' },
    denominator: { label: 'Votes cast', format: ',.0f' }, ratio: { label: 'Margin, share of votes', per: 1, format: '.1%' } },
  pulse: { id: 'pulse', label: 'Signal', source: MADE_UP + ' Shaped like a country: a few big metros, regional hot zones, quiet plains.',
    value: { label: 'Events', format: ',.3s' }, denominator: { label: 'People', format: ',.3s' },
    ratio: { label: 'Events per 100,000 people', per: 100000, format: ',.0f' } },
  land_area: { id: 'land_area', label: 'Shape area', source: 'Measured from the map shapes, in map units. Real, but not square miles.',
    value: { label: 'Shape area', unit: 'map units', format: ',.0f' } }
};

/** @returns {{rows: Object[], header: Object}} */
export function makeLayer(id, topology) {
  const header = LAYER_HEADERS[id];
  if (!header) throw new Error(`No demo layer called "${id}".`);
  const rnd = rng(id.split('').reduce((s, c) => s * 31 + c.charCodeAt(0), 7) % 2147483647);
  const rows = [];
  if (id === 'pulse') {
    // A made-up country with structure: metros pull people in, and a few broad regions run hot. Neighbours resemble each other.
    const mid = pl => [(pl.bbox[0] + pl.bbox[2]) / 2, (pl.bbox[1] + pl.bbox[3]) / 2];
    const pick = () => mid(topology.places[Math.floor(rnd() * topology.places.length)]);
    const metros = Array.from({ length: 70 }, (_, k) => ({ at: pick(), pull: 1 / (k + 1) ** 0.9, reach: 5 + rnd() * 13 }));
    const zones = Array.from({ length: 8 }, () => ({ at: pick(), heat: 0.5 + rnd() * 1.3, reach: 35 + rnd() * 55 }));
    const bump = (c, o, reach) => Math.exp(-((c[0] - o.at[0]) ** 2 + (c[1] - o.at[1]) ** 2) / (2 * reach * reach));
    for (const pl of topology.places) {
      const c = mid(pl);
      const urban = metros.reduce((sum, m) => sum + m.pull * bump(c, m, m.reach), 0);
      const people = Math.round(1500 + 9000 * rnd() + 2600000 * urban ** 1.35);
      const heat = zones.reduce((sum, z) => sum + z.heat * bump(c, z, z.reach), 0);
      const rate = (9 + 34 * heat + 6 * urban) * (0.85 + rnd() * 0.3);
      const expected = people * rate / 100000;
      rows.push({ geo_id: pl.id, value: Math.max(0, Math.round(expected + (rnd() - 0.5) * 2 * Math.sqrt(expected + 0.5))), denominator: people });
    }
    return { rows, header };
  }
  for (const pl of topology.places) {
    const people = Math.round(800 * Math.exp(rnd() * 7.5));
    const row = { geo_id: pl.id };
    if (id === 'payments') row.value = Math.round(people * (20 + rnd() * rnd() * 900));
    else if (id === 'fatalities') {
      if (rnd() < 0.12) continue;                                   // no row at all
      const incidents = rnd() < 0.45 ? 0 : 1 + Math.floor(rnd() * rnd() * 30);
      row.value = rnd() < 0.05 ? '' : incidents ? Math.ceil(incidents * rnd() * 1.4) : 0;   // a few rows arrive with an empty value
      row.n = incidents;
    } else if (id === 'cms_fines') {
      row.denominator = rnd() < 0.03 ? 0 : Math.round(people / 90);
      row.value = rnd() < 0.25 ? 0 : Math.round(row.denominator * rnd() * rnd() * 4000 + rnd() * 2000);
    } else if (id === 'disputes') {
      row.denominator = Math.round(people * 0.6);
      row.value = Math.round(row.denominator * (0.004 + rnd() * 0.004) * (rnd() < 0.03 ? 4 + rnd() * 4 : 1));
    } else if (id === 'overdose_deaths') {
      row.denominator = people;
      const expected = people * (8 + rnd() * 30) / 100000;
      row.value = Math.max(0, Math.round(expected + (rnd() - 0.5) * 2 * Math.sqrt(expected + 0.5)));
    } else if (id === 'pres_2024') {
      row.denominator = Math.round(people * 0.45);
      row.value = Math.round(row.denominator * Math.max(-0.95, Math.min(0.95, rnd() * 1.4 - 0.85 + Math.min(0.5, people / 600000))));
    } else if (id === 'land_area') row.value = Math.round(shapeArea(pl) * 100) / 100;
    rows.push(row);
  }
  return { rows, header };
}
