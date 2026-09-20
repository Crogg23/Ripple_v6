// Text in, row objects out. Forgiving about delimiters and headers, strict about nothing else.
// Validation is not done here. See load.js.

const KNOWN = ['geo_id', 'geo_type', 'period', 'value', 'denominator', 'n', 'tier'];
const ALSO_KNOWN_AS = { fips: 'geo_id', geoid: 'geo_id', id: 'geo_id', denom: 'denominator' };

function pickDelimiter(line) {
  const counts = { '\t': 0, ',': 0, ';': 0 };
  let quoted = false;
  for (const ch of line) {
    if (ch === '"') quoted = !quoted;
    else if (!quoted && ch in counts) counts[ch]++;
  }
  return Object.entries(counts).sort((a, b) => b[1] - a[1])[0][0];
}

function splitLine(line, delim) {
  const out = [];
  let cur = '', quoted = false;
  for (let i = 0; i < line.length; i++) {
    const ch = line[i];
    if (quoted) {
      if (ch === '"' && line[i + 1] === '"') { cur += '"'; i++; }
      else if (ch === '"') quoted = false;
      else cur += ch;
    } else if (ch === '"') quoted = true;
    else if (ch === delim) { out.push(cur.trim()); cur = ''; }
    else cur += ch;
  }
  out.push(cur.trim());
  return out;
}

// Commas count only as thousands separators in groups of three. "12,5" is not a number here: it could be 12.5 or 125.
export const NUMBER = /^[-+]?(\d{1,3}(,\d{3})+|\d*)(\.\d+)?(e[-+]?\d+)?$/i;
export const looksNumeric = s => /\d/.test(s) && NUMBER.test(s);

/**
 * @param {string} text
 * @returns {{rows: Object[], columns: string[], labelHint: string|null, shorthand: boolean, lines: number}}
 */
export function parseText(text) {
  const lines = String(text || '').split(/\r?\n/).filter(l => l.trim().length);
  if (!lines.length) return { rows: [], columns: [], labelHint: null, shorthand: false, lines: 0 };

  const delim = pickDelimiter(lines[0]);
  const cells = lines.map(l => splitLine(l, delim));
  const first = cells[0].map(c => c.toLowerCase());
  const named = first.map(c => ALSO_KNOWN_AS[c] || c);
  const hasNamedHeader = named.includes('geo_id') && (named.length === 1 || named.some(c => c !== 'geo_id' && KNOWN.includes(c)));

  let columns, body, labelHint = null, shorthand = false;
  if (hasNamedHeader) {
    columns = named;
    body = cells.slice(1);
  } else {
    // Paste shorthand: geo_id, value [, denominator]. A first row whose second cell is not a number names the layer.
    shorthand = true;
    columns = ['geo_id', 'value', 'denominator'].slice(0, Math.max(2, Math.min(3, cells[0].length)));
    const firstIsHeader = cells[0].length > 1 && cells[0][1] !== '' && !looksNumeric(cells[0][1]);
    if (firstIsHeader) { labelHint = cells[0][1].slice(0, 60); body = cells.slice(1); } else body = cells;
  }

  const rows = body.map((c, i) => {
    const row = { _line: i + (body === cells ? 1 : 2) };
    while (c.length > columns.length && c[c.length - 1] === '') c.pop();      // trailing delimiters, common in spreadsheet exports
    if (c.length > columns.length) row._extra = c.length - columns.length;
    if (hasNamedHeader && c.length < columns.length) row._short = true;
    columns.forEach((name, j) => { if (KNOWN.includes(name)) row[name] = c[j] === undefined ? '' : c[j]; });
    return row;
  });
  return { rows, columns: columns.filter(c => KNOWN.includes(c)), labelHint, shorthand, lines: lines.length };
}
