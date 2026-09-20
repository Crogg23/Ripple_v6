// Adapters. Four ways in, one way out: { rows, headerHint }.
// A future warehouse source is one of the last two: the host hands rows in, or a URL serves them.

import { parseText } from '../loader/parse.js';

function fromText(text) {
  const parsed = parseText(text);
  return { rows: parsed.rows, headerHint: parsed.labelHint ? { label: parsed.labelHint } : {} };
}

function fromJson(data) {
  if (Array.isArray(data)) return { rows: data, headerHint: {} };
  if (data && Array.isArray(data.rows)) return { rows: data.rows, headerHint: data.header || {} };
  throw new Error('JSON source must be an array of rows, or { header, rows }.');
}

function sniff(text) {
  const t = text.trimStart();
  if (t.startsWith('[') || t.startsWith('{')) { try { return fromJson(JSON.parse(text)); } catch { /* fall through to delimited text */ } }
  return fromText(text);
}

export const sources = {
  /** Pasted text: CSV, TSV, semicolons, or JSON. */
  paste: text => ({ load: async () => sniff(String(text || '')) }),
  /** A File from a drop or a file picker. */
  file: file => ({ load: async () => sniff(await file.text()) }),
  /** Anything that serves text or JSON over http. */
  url: url => ({
    load: async () => {
      const res = await fetch(url);
      if (!res.ok) throw new Error(`Could not fetch ${url} (${res.status}).`);
      return sniff(await res.text());
    }
  }),
  /** The host already has rows, such as a data app passing a query result. */
  rows: (rows, header) => ({ load: async () => ({ rows, headerHint: header || {} }) })
};
