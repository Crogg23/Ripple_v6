// The narrator. It reads the numbers on the map and says what they mean, the way you would tell a friend.
// Every sentence is worked out from the data in front of it. Nothing here is typed by hand per dataset,
// and nothing names a real place or subject: labels come from the layer header, nouns from the map's registry.
//
// Output is plain data: { headline, evidence, lines: [{kind, label, text, places}], caveats: [text], figures: [{key, label, big, small, places}] }.
// kinds: typical, standout, overall, concentration, where, region, zeros. "places" is the evidence: who the sentence is about.

import { makeFormatter } from './format.js';
import { measureMeta } from './measure.js';
import { UNNAMED } from '../loader/load.js';

const whole = makeFormatter(',.0f');

/** "about 7 times", "nearly double", "about the same as". Round numbers, because nobody says 6.83 times out loud. */
export function timesWords(x) {
  if (!(x > 0) || !Number.isFinite(x)) return null;
  if (x < 1.15) return 'about the same as';
  if (x < 1.75) return `about ${Math.round(x * 10) / 10} times`;
  if (x < 2.5) return 'about double';
  if (x < 9.5) return `about ${Math.round(x)} times`;
  if (x < 97.5) return `about ${Math.round(x / 5) * 5} times`;
  if (x < 1000) return `about ${whole(Math.round(x / 50) * 50)} times`;
  return `more than ${whole(Math.floor(x / 1000) * 1000)} times`;
}

/** 0.52 -> "about half". Falls back to a percent when no everyday fraction is close. */
export function shareWords(p) {
  const known = [[0.1, 'a tenth'], [0.2, 'a fifth'], [0.25, 'a quarter'], [1 / 3, 'a third'], [0.5, 'half'], [2 / 3, 'two thirds'], [0.75, 'three quarters'], [0.9, 'nine tenths']];
  for (const [v, w] of known) if (Math.abs(p - v) <= Math.min(0.025, v * 0.1)) return `about ${w}`;
  if (p > 0.97) return 'nearly all';
  return `${Math.round(p * 100)}%`;
}

function listWords(names) {
  if (names.length <= 1) return names.join('');
  return `${names.slice(0, -1).join(', ')} and ${names[names.length - 1]}`;
}

const lower = s => String(s || '').charAt(0).toLowerCase() + String(s || '').slice(1);

/**
 * A number the way it is said out loud. Compact formats like "3.63k" are for legends; in a sentence it is "3,630",
 * and past a million it is "1.1 million". Formats that carry meaning, like percent or fixed decimals, are kept.
 */
export function sayer(format) {
  const spec = format == null ? '' : String(format);
  if (spec && !spec.endsWith('s')) return makeFormatter(spec);
  const money = spec.startsWith('$') ? '$' : '';
  return v => {
    if (typeof v !== 'number' || !Number.isFinite(v)) return 'no data';
    const a = Math.abs(v), sign = v < 0 ? '-' : '';
    const big = [[1e12, 'trillion'], [1e9, 'billion'], [1e6, 'million']].find(([size]) => a >= size);
    if (big) return `${sign}${money}${Number((a / big[0]).toPrecision(2))} ${big[1]}`;
    if (a >= 10000) return `${sign}${money}${whole(Number(a.toPrecision(3)))}`;
    return `${sign}${money}${Number.isInteger(a) ? whole(a) : String(Number(a.toPrecision(3)))}`;
  };
}

/** "Eight in ten", from a share that was actually counted. */
function inTen(share) {
  const n = Math.round(share * 10);
  if (n >= 10) return share >= 0.995 ? 'All' : 'Nearly all';
  return `${['None', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine'][n]} in ten`;
}

/**
 * A number with its label, the way a person would put it: "$1.1 billion in payments", "1,139 events",
 * "194 events per 100,000 people", "a shape area of 2,169". An unnamed number is just the number.
 */
function amount(text, part, format) {
  if (part.label === UNNAMED) return text;
  const label = lower(part.label);
  if (String(format || '').startsWith('$')) return `${text} in ${label}`;
  if (label.includes(' per ') || /s$/.test(label.split(/[ ,]/)[0])) return `${text} ${label}`;
  return `${/^[aeiou]/.test(label) ? 'an' : 'a'} ${label} of ${text}`;
}

/** "1 events" is the giveaway of a machine. One of something drops its plural, unless the header supplies the word. */
function counted(text, amount, part) {
  if (part.label === UNNAMED) return text;                          // a table that never named its number just gets the number
  const label = lower(part.label);
  if (String(part.format || '').startsWith('$')) return `${text} in ${label}`;
  if (amount !== 1) return `${text} ${label}`;
  if (part.one) return `${text} ${lower(part.one)}`;
  return `${text} ${label.endsWith('ies') ? label.slice(0, -3) + 'y' : label.endsWith('s') && !label.endsWith('ss') ? label.slice(0, -1) : label}`;
}

function nounsOf(topology) {
  const n = topology.entry && topology.entry.noun;
  return Array.isArray(n) && n.length === 2 ? { one: n[0], many: n[1] } : { one: 'place', many: 'places' };
}

function placeName(topology, idx) {
  const pl = topology.places[idx];
  const par = pl.parentId != null ? topology.parentIndexById.get(pl.parentId) : undefined;
  return par !== undefined ? `${pl.name}, ${topology.parents[par].name}` : pl.name;
}

function sortedLive(values) {
  const live = [];
  for (let i = 0; i < values.length; i++) if (!Number.isNaN(values[i])) live.push(i);
  live.sort((a, b) => values[a] - values[b]);
  return live;
}

/**
 * The story of the whole map.
 * @param {Object} model   what colorize() kept: topology, header, report, cols, values, measure, ranks
 * @param {{highlight: number[], low_confidence: number[]}} marks
 */
export function narrate(model, marks = { highlight: [], low_confidence: [] }) {
  const { topology, header, values, measure, cols, report } = model;
  const noun = nounsOf(topology);
  const meta = measureMeta(measure, header);
  const fmt = sayer(meta.format);
  const named = meta.label !== UNNAMED;
  const what = named ? lower(meta.label) : '';
  const live = model.order || sortedLive(values), M = live.length, N = values.length;
  const lines = [], caveats = [];
  // Every sentence carries its evidence: the places it is talking about. A page can light them up when the sentence is touched.
  const LABEL = { typical: 'Typical', standout: 'Range', overall: 'All together', concentration: 'Piled up?', where: 'Where', region: 'Top region', zeros: 'Zeros' };
  const say = (kind, text, places = []) => lines.push({ kind, label: LABEL[kind], text, places });
  if (!M) return { headline: `None of the ${whole(N)} ${noun.many} has a number to show.`, evidence: [], lines, caveats };

  if (measure === 'presence') {
    const have = live.filter(i => values[i] === 1);
    return { headline: `${whole(have.length)} of ${whole(N)} ${noun.many} have data. ${whole(N - have.length)} do not.`, evidence: have, lines, caveats };
  }

  const median = values[live[Math.floor((M - 1) / 2)]];
  const top = live[M - 1], max = values[top], min = values[live[0]];
  const zeros = live.filter(i => values[i] === 0);
  const ratio = median > 0 ? max / median : null;

  // The headline: the typical case against the standout. That gap is nearly always the story.
  let headline;
  if (M === 1) headline = `Only one ${noun.one} has a number: ${placeName(topology, top)}, at ${fmt(max)}.`;
  else if (max === min) headline = `Every ${noun.one} shows the same number: ${fmt(max)}.`;
  else if (min < 0) headline = `${named ? meta.label : 'It'} runs from ${fmt(min)} to ${fmt(max)}. The typical ${noun.one} sits at ${fmt(median)}.`;
  else if (ratio && ratio >= 1.75) headline = `${placeName(topology, top)} stands at ${amount(fmt(max), meta, meta.format)}. That is ${timesWords(ratio)} the typical ${noun.one}.`;
  else if (median === 0) headline = `Most ${noun.many} show nothing at all. ${placeName(topology, top)} tops the list at ${fmt(max)}.`;
  else headline = `${named ? meta.label : 'This'} is fairly even. The top ${noun.one} is ${(ratio || 1) < 1.15 ? 'about the same as' : 'only ' + timesWords(ratio)} the typical one.`;

  const blank = N - M;
  const gaps = () => { if (blank) caveats.push(`${whole(blank)} ${blank === 1 ? noun.one + ' has' : noun.many + ' have'} no number, so ${blank === 1 ? 'it is' : 'they are'} left blank, never guessed.`); };
  // When every place shows the same number there is no top, no tenth, and no spread to describe. Say the one true thing and stop.
  if (M === 1 || max === min) { gaps(); return { headline, evidence: M === 1 ? [top] : [], lines, caveats }; }

  // A rate on a tiny base is the oldest trap in the book. If the standout is one of the smallest places, say so next to the headline.
  if (measure === 'ratio' && M >= 20 && max !== min) {
    const bases = live.map(i => cols.denominator[i]).sort((a, b) => a - b), small = bases[Math.floor(0.1 * (M - 1))];
    const d = cols.denominator[top];
    // "One of the smallest" has to mean it: at or under the bottom tenth, and that tenth really is smaller than the middle.
    if (d <= small && small < bases[Math.floor((M - 1) / 2)]) headline += ` It is also one of the smallest, with ${counted(sayer(header.denominator.format)(d), d, header.denominator)}, so a few ${lower(header.value.label)} move it a lot.`;
  }

  const band = (lo, hi) => live.slice(Math.floor(lo * (M - 1)), Math.floor(hi * (M - 1)) + 1);
  // Count, never assume. With heavy ties "half above, half below" can be flatly false, so the sentence says what was counted.
  const atMedian = live.filter(i => values[i] === median), above = live.filter(i => values[i] > median).length, below = M - above - atMedian.length;
  const opener = min < 0 ? '' : `The typical ${noun.one} sits at ${fmt(median)}. `;
  if (atMedian.length > 1 && atMedian.length / M > 0.05) say('typical', `${opener}${whole(atMedian.length)} sit exactly ${min < 0 ? 'at ' + fmt(median) : 'there'}, ${whole(above)} above and ${whole(below)} below.`, atMedian);
  else say('typical', min < 0 ? `Half are above ${fmt(median)}, half below.` : `${opener}Half are above that, half below.`, band(0.45, 0.55));

  if (M >= 20) {
    const p90 = values[live[Math.floor(0.9 * (M - 1))]], p10 = values[live[Math.floor(0.1 * (M - 1))]];
    const inside = live.filter(i => values[i] >= p10 && values[i] <= p90).length, over = live.filter(i => values[i] > p90);
    const tail = over.length ? ` The ${whole(over.length)} above ${fmt(p90)} ${over.length === 1 ? 'is' : 'are'} where to look first.` : '';
    say('standout', `${inTen(inside / M)} fall between ${fmt(p10)} and ${fmt(p90)}.${tail}`, over);
  }

  // All of it put together. For a rate this is total over total, which is NOT the typical place: big places weigh more.
  const withBase = live.filter(i => !Number.isNaN(cols.value[i]) && cols.denominator[i] > 0);
  const per = header.ratio && Number.isFinite(header.ratio.per) ? header.ratio.per : 1;
  let overall = null;
  if (measure === 'ratio' && withBase.length >= 20 && min >= 0) {
    let sv = 0, sd = 0; for (const i of withBase) { sv += cols.value[i]; sd += cols.denominator[i]; }
    overall = (sv / sd) * per;
    const lean = median > 0 && overall / median >= 1.3 ? ` That is above the typical ${noun.one}: the high ones pull the total up.`
      : median > 0 && median / overall >= 1.3 ? ` That is below the typical ${noun.one}: the low ones pull the total down.` : '';
    say('overall', `Put every ${noun.one} together and it comes to ${fmt(overall)}.${lean}`, []);
  }

  // For counts, how concentrated is it? "A handful of places hold half of everything" is the plainest big-data sentence there is.
  if (measure === 'value' && min >= 0 && M >= 10) {                  // with a handful of places, "concentrated" and "spread out" mean nothing
    let total = 0; for (const i of live) total += values[i];
    if (total > 0) {
      let run = 0, k = 0;
      for (let j = M - 1; j >= 0 && run < total / 2; j--) { run += values[live[j]]; k++; }
      const ofWhat = header.value.label === UNNAMED ? 'the total' : `all ${lower(header.value.label)}`;
      if (k / M <= 0.34) say('concentration', `Just ${whole(k)} of ${whole(M)} ${noun.many} ${k === 1 ? 'accounts' : 'account'} for half of ${ofWhat}. It is concentrated, not spread out.`, live.slice(M - k));
      else say('concentration', `It takes ${whole(k)} of ${whole(M)} ${noun.many} to reach half of ${ofWhat}, so this is spread out, not piled up in a few.`, live.slice(M - k));
    }
  }

  if (topology.parents.length > 1 && M >= 30) {
    const parentName = id => topology.parents[topology.parentIndexById.get(id)].name;
    // Where: which parent regions hold the top tenth.
    const cut = Math.floor(0.9 * M), tally = new Map();
    for (let j = cut; j < M; j++) { const id = topology.places[live[j]].parentId; tally.set(id, (tally.get(id) || 0) + 1); }
    const ranked = [...tally].sort((a, b) => b[1] - a[1]), inTop = M - cut;
    const lead = ranked.slice(0, 3), share = lead.reduce((s, r) => s + r[1], 0) / inTop;
    const leadIds = new Set(lead.map(r => r[0]));
    if (share >= 0.4) say('where', `${shareWords(share).replace(/^./, c => c.toUpperCase())} of the highest tenth sits in just ${lead.length === 1 ? 'one area' : lead.length + ' areas'}: ${listWords(lead.map(r => parentName(r[0])))}.`, live.slice(cut).filter(i => leadIds.has(topology.places[i].parentId)));
    else say('where', `The highest tenth is scattered across ${whole(ranked.length)} areas. No single region owns it.`, live.slice(cut));

    // Region: each parent taken as a whole. A rate is total over total, so one tiny place cannot carry its region.
    if (min >= 0) {
      const sums = new Map();
      for (const i of measure === 'ratio' ? withBase : live) {
        const id = topology.places[i].parentId, s = sums.get(id) || { v: 0, d: 0, n: 0 };
        s.v += measure === 'ratio' ? cols.value[i] : values[i]; s.d += cols.denominator[i] || 0; s.n++; sums.set(id, s);
      }
      const score = s => (measure === 'ratio' ? (s.v / s.d) * per : s.v);
      const best = [...sums].filter(([, s]) => s.n >= 3 && (measure !== 'ratio' || s.d > 0)).sort((a, b) => score(b[1]) - score(a[1]))[0];
      if (best) {
        const [id, s] = best, places = live.filter(i => topology.places[i].parentId === id);
        if (measure === 'ratio' && overall > 0) say('region', `Taken as a whole, ${parentName(id)} runs highest at ${fmt(score(s))}, ${timesWords(score(s) / overall)} the overall figure.`, places);
        else if (measure === 'value') { let total = 0; for (const i of live) total += values[i]; if (total > 0) say('region', `${parentName(id)} has the most in total: ${fmt(s.v)}, ${shareWords(s.v / total)} of everything.`, places); }
      }
    }
  }

  if (zeros.length && median !== 0) say('zeros', `${whole(zeros.length)} ${zeros.length === 1 ? noun.one + ' shows' : noun.many + ' show'} exactly zero.`, zeros);

  if (measure === 'ratio') caveats.push(`These are rates, not counts: ${lower(header.value.label)} ${header.ratio.per === 1 ? 'divided by' : 'for every ' + whole(header.ratio.per)} ${lower(header.denominator.label)}. So a big ${noun.one} and a small one compare fairly.`);
  else if (measure === 'value' && report.has_denominator) caveats.push(`These are raw counts. Big ${noun.many} will look big. Switch to the rate to compare them fairly.`);
  gaps();
  if (report.zero_denominators && measure === 'ratio') caveats.push(`${whole(report.zero_denominators)} of those have a base of zero, so there is no rate to work out.`);
  if (marks.low_confidence.length) caveats.push(`${whole(marks.low_confidence.length)} are small enough that one more or one fewer would swing the number. They are marked as shaky.`);
  // Figures: the same story as a handful of big numbers, for a page that leads with numbers instead of sentences.
  const cap = w => w.charAt(0).toUpperCase() + w.slice(1);
  const figures = [{ key: 'typical', label: `Typical ${noun.one}`, big: fmt(median), small: 'half are above, half below', places: band(0.45, 0.55) },
    { key: 'top', label: 'Highest', big: fmt(max), small: placeName(topology, top), places: [top] }];
  if (min >= 0 && ratio && ratio >= 1.15) figures.push({ key: 'gap', label: 'The gap', big: `${ratio >= 9.5 ? whole(Number(ratio.toPrecision(2))) : Math.round(ratio * 10) / 10}×`, small: `highest against typical`, places: [top] });
  const piled = lines.find(l => l.kind === 'concentration');
  if (overall !== null) figures.push({ key: 'overall', label: 'All together', big: fmt(overall), small: `every ${noun.one} pooled`, places: [] });
  else if (piled) figures.push({ key: 'half', label: 'Half of the total', big: whole(piled.places.length), small: `of ${whole(M)} ${noun.many} hold it`, places: piled.places });
  if (zeros.length && median !== 0) figures.push({ key: 'zeros', label: 'At zero', big: whole(zeros.length), small: cap(noun.many), places: zeros });
  if (blank) figures.push({ key: 'blank', label: 'No data', big: whole(blank), small: 'left blank, never guessed', places: [] });
  return { headline, evidence: [top], lines, caveats, figures };
}

/**
 * One place, in a sentence or two. This is what hover says.
 * @returns {string}
 */
export function describePlace(idx, model) {
  const { topology, header, values, measure, cols, report, ranks } = model;
  const noun = nounsOf(topology);
  const name = placeName(topology, idx);
  const v = cols.value[idx], d = cols.denominator[idx], shown = values[idx];
  const fmtV = sayer(header.value.format), fmtD = sayer(header.denominator.format);
  const meta = measureMeta(measure, header), fmt = sayer(meta.format);
  if (!cols.has[idx]) return `${name}. No data here, so it is left blank.`;

  let facts;
  if (report.has_denominator && !Number.isNaN(v) && !Number.isNaN(d)) {
    facts = `${counted(fmtV(v), v, header.value)} among ${counted(fmtD(d), d, header.denominator)}`;
    if (d === 0) return `${name}. ${facts}. With a base of zero there is no rate to show.`;
    if (measure === 'ratio') facts += `, which works out to ${fmt(shown)} ${lower(meta.label).replace(lower(header.value.label), '').trim()}`;
  } else if (!Number.isNaN(v)) facts = counted(fmtV(v), v, header.value);
  else return `${name}. There is a row for it, but the number is empty.`;
  if (Number.isNaN(shown)) return `${name}. ${facts}.`;

  const live = model.order || sortedLive(values), M = live.length, median = values[live[Math.floor((M - 1) / 2)]];
  const r = ranks.rank[idx], frac = M > 1 ? (r - 1) / (M - 1) : 0, signed = values[live[0]] < 0;
  const others = ranks.tied[idx] - 1;
  if (shown === 0 && others >= 1) return `${name}. ${facts}. It shows zero, the same as ${whole(others)} other ${others === 1 ? noun.one : noun.many}.`;
  let where;
  if (r === 1) where = `That is the highest of ${whole(M)} ${noun.many}`;
  else if (r + ranks.tied[idx] - 1 >= M) where = `That is the lowest of ${whole(M)} ${noun.many}`;
  else if (frac <= 0.1) where = `That puts it in the top tenth, ${whole(r)} of ${whole(M)}`;
  else if (frac < 0.4) where = `That is above the middle, ${whole(r)} of ${whole(M)}`;
  else if (frac <= 0.6) where = `That is right around the middle, ${whole(r)} of ${whole(M)}`;
  else if (frac < 0.9) where = `That is below the middle, ${whole(r)} of ${whole(M)}`;
  else where = `That puts it in the bottom tenth, ${whole(r)} of ${whole(M)}`;
  if (!signed && median > 0 && shown > 0) {
    if (shown / median >= 1.75) where += `, ${timesWords(shown / median)} the typical ${noun.one}`;
    else if (median / shown >= 1.75) where += `. The typical ${noun.one} runs ${timesWords(median / shown)} that`;
  }
  return `${name}. ${facts}. ${where}.`;
}
