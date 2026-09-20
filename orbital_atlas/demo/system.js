// Design tokens, solved from a look. A theme says what the MAP looks like; this turns the same theme into the
// six colour roles and three voices the PAGE uses, so page and map can never drift apart.
// Every role is checked for contrast here. A look cannot produce unreadable chrome: the token is corrected, and the report says so.

import { contrast, quiet, ramp, normalizeHex } from '../src/engine/color.js';

export const TARGETS = { ink: 7, ink2: 4.5, signal: 3 };

/**
 * @param {Object} theme   a resolved theme
 * @returns {{vars: Object<string,string>, report: {role: string, color: string, on: string, ratio: number, target: number, corrected: boolean}[]}}
 */
export function solveTokens(theme) {
  const ground = normalizeHex(theme.ground.background);
  const wanted = normalizeHex(theme.lines.outline.color);
  // Ink: the look's own line colour, pushed away from the ground until sentences are comfortable to read.
  const pole = contrast('#000000', ground) > contrast('#ffffff', ground) ? '#000000' : '#ffffff';
  let ink = wanted, fixedInk = false;
  if (contrast(ink, ground) < TARGETS.ink) { const toPole = ramp([wanted, pole]); for (let u = 0.1; u <= 1.001; u += 0.1) { ink = toPole(u); if (contrast(ink, ground) >= TARGETS.ink) break; } fixedInk = true; }
  const mix = ramp([ground, ink]);
  const surface = mix(0.045), wash = mix(0.09);
  // Quiet text also sits on raised panels and on hovered rows. Solve it against the hardest of the three, so it holds on all of them.
  const hardest = [ground, surface, wash].sort((a, b) => contrast(ink, a) - contrast(ink, b))[0];
  const ink2 = quiet(ink, hardest, TARGETS.ink2 + 0.1);
  // Signal: the data's call-out colour. If the look's colour cannot be seen on the page, the page falls back to ink.
  const asked = normalizeHex(theme.roles.highlight.color);
  const signal = contrast(asked, ground) >= TARGETS.signal ? asked : ink;
  const row = (role, color, target, corrected) => ({ role, color, on: ground, ratio: Math.round(contrast(color, ground) * 10) / 10, target, corrected });
  return {
    vars: {
      '--ground': ground, '--surface': surface, '--ink': ink, '--ink-2': ink2, '--rule': mix(0.22), '--wash': wash, '--signal': signal,
      '--f-display': theme.type.display, '--f-text': theme.type.text, '--f-data': theme.type.data, '--w-display': String(theme.type.display_weight || 400)
    },
    report: [row('ink', ink, TARGETS.ink, fixedInk), row('ink-2', ink2, TARGETS.ink2, false), row('signal', signal, TARGETS.signal, signal !== asked)]
  };
}

/** Put the tokens on a page. Returns the contrast report. */
export function applyTokens(theme, root = document.documentElement) {
  const { vars, report } = solveTokens(theme);
  for (const [k, v] of Object.entries(vars)) root.style.setProperty(k, v);
  return report;
}

/** A sentence as DOM, with every figure set in the data voice so the eye can hop from number to number. */
export function sentence(text, doc = document) {
  const frag = doc.createDocumentFragment();
  const figure = /(-?\$?\d[\d,]*(?:\.\d+)?%?(?: (?:million|billion|trillion))?)/g;
  text.split(figure).forEach((part, k) => {
    if (!part) return;
    if (k % 2) { const b = doc.createElement('b'); b.className = 'num'; b.textContent = part; frag.append(b); }
    else frag.append(doc.createTextNode(part));
  });
  return frag;
}
