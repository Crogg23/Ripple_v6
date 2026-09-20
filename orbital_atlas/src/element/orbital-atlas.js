// <orbital-atlas>: the shell any host can drop in.
//
//   <orbital-atlas registry="../topologies/registry.json"></orbital-atlas>
//
//   el.registerThemes([...])  themes another theme may name as its "base"
//   el.theme = {...}          partial themes are laid over their base chain, then over the default
//   el.view  = {...}          partial views are laid over the default
//                             both are checked on the way in; a bad one is refused in words, never half-drawn
//   await el.ready            resolves with stats once the first paint is done
//   await el.load(source, { header, onDuplicate })     source: sources.paste(text) | .file(f) | .url(u) | .rows(rows)
//                             resolves with { header, report, words }; also fires 'atlas-load'
//   el.legend                 the legend model, plain data, generated from the scale
//   el.readout(geoId)         the readout model for one place, plain data
//   el.story                  what the map says, in sentences: { headline, evidence, lines: [{kind, text, places}], caveats }
//   el.spotlight(places)      light up the places a sentence is about; null clears
//   el.pin(geoId)             keep one place outlined
//   'atlas-ready' / 'atlas-error' / 'place-hover' / 'place-click' / 'view-change' events
//
// A view the engine must refuse (a ratio with no denominator, a log scale over zeros) shows its reason
// in words and fires 'atlas-error'. The map falls back to no colour. It never guesses.
//
// The shell wires things together. It does no drawing of its own.

import { loadRegistry, loadTopology } from '../topology/registry.js';
import { buildDrawList, buildOverlay } from '../engine/drawlist.js';
import { checkView, checkTheme, resolveTheme } from '../engine/config.js';
import { fit } from '../engine/frame.js';
import { DEFAULT_THEME, DEFAULT_VIEW, overlay } from '../engine/defaults.js';
import { CanvasPainter } from '../painter/canvas.js';
import { colorize } from '../engine/colorize.js';
import { buildReadout } from '../engine/readout.js';
import { hitTest, unproject } from '../engine/hit.js';
import { loadRows } from '../loader/load.js';
import { describeReport } from '../loader/report.js';
import { sources } from '../adapters/sources.js';

const STYLE = `
  :host { display: block; position: relative; width: 100%; height: 100%; min-height: 240px; overflow: hidden; }
  canvas { position: absolute; inset: 0; width: 100%; height: 100%; display: block; }
  .msg { position: absolute; left: 24px; bottom: 20px; right: 24px; pointer-events: none;
         font-size: 12px; line-height: 1.5; letter-spacing: 0.02em; opacity: 0.7; }
  .msg[hidden] { display: none; }
  .err { color: #ff8a80; opacity: 1; }
  .panel { position: absolute; left: 24px; font-size: 11px; line-height: 1.45; pointer-events: none;
           font-variant-numeric: tabular-nums; padding: 10px 12px; border-radius: 6px; max-width: 300px; }
  .panel[hidden] { display: none; }
  .legend { bottom: 20px; width: 260px; }
  .readout { top: 20px; pointer-events: auto; }
  .ttl { font-size: 13px; }
  .dim { opacity: 0.6; }
  .ramp { height: 10px; border-radius: 2px; margin-top: 8px; }
  .ticks { position: relative; height: 38px; margin-bottom: 2px; }
  .ticks span { position: absolute; top: 0; padding-top: 7px; white-space: nowrap; transform: translateX(-50%); }
  .ticks span::before { content: ''; position: absolute; top: 0; left: 50%; width: 1px; height: 5px; background: currentColor; opacity: 0.6; }
  .ticks span.low { padding-top: 20px; } .ticks span.low::before { height: 18px; }
  .ticks span.first { transform: none; } .ticks span.first::before { left: 0; }
  .ticks span.last { transform: translateX(-100%); } .ticks span.last::before { left: auto; right: 0; }
  .cl { display: grid; grid-template-columns: 14px 1fr auto; gap: 8px; align-items: center; margin-top: 3px; }
  .cl i { width: 14px; height: 10px; border-radius: 2px; display: block; box-shadow: 0 0 0 1px rgba(128,128,128,0.35); }
  .cl.gap { margin-top: 8px; }
  .cl i.outline { background: none; }
  .cl i.dot { position: relative; }
  .cl i.dot::after { content: ''; position: absolute; left: 5px; top: 3px; width: 4px; height: 4px; border-radius: 50%; background: var(--mark); }
  .note { margin-top: 6px; opacity: 0.75; }
  .kv { display: grid; grid-template-columns: auto auto; gap: 2px 14px; margin-top: 6px; }
  .kv .v { text-align: right; }
  .kv .drive { font-weight: 700; }
  details { margin-top: 6px; } summary { cursor: pointer; opacity: 0.7; }
`;

export { sources };

export class OrbitalAtlas extends HTMLElement {
  static get observedAttributes() { return ['registry', 'topology']; }

  constructor() {
    super();
    const root = this.attachShadow({ mode: 'open' });
    root.innerHTML = `<style>${STYLE}</style><canvas part="canvas"></canvas><div class="msg" part="message" aria-live="polite" hidden></div><div class="panel readout" part="readout" hidden></div><div class="panel legend" part="legend" hidden></div>`;
    this._canvas = root.querySelector('canvas');
    this._msg = root.querySelector('.msg');
    this._legendEl = root.querySelector('.legend');
    this._readoutEl = root.querySelector('.readout');
    this._colored = null;
    this._refusal = null;
    this._hoverIdx = -1;
    this._pinnedIdx = -1;
    this._spotlight = null;
    this._moreOpen = false;
    this._canvas.setAttribute('role', 'img');
    this._canvas.addEventListener('click', e => this._onClick(e));
    this._canvas.addEventListener('pointermove', e => this._onPointer(e));
    this._canvas.addEventListener('pointerleave', e => { if (!this._readoutEl.contains(e.relatedTarget)) this._setHover(-1); });
    this._readoutEl.addEventListener('pointerleave', e => { if (e.relatedTarget !== this._canvas) this._setHover(-1); });
    this._painter = new CanvasPainter(this._canvas);
    this._theme = DEFAULT_THEME;
    this._themeRaw = {};
    this._themes = {};
    this._themeError = null;
    this._view = DEFAULT_VIEW;
    this._topology = null;
    this._registry = null;
    this._layer = null;
    this._drawList = null;
    this._paintQueued = false;
    this._loadToken = 0;
    this.stats = null;
    this.ready = new Promise((res, rej) => { this._resolveReady = res; this._rejectReady = rej; });
    this.ready.catch(() => {});
  }

  connectedCallback() {
    this._ro = new ResizeObserver(() => this._resize());
    this._ro.observe(this);
    // Place names are lettered on the canvas. A web typeface can arrive after the first paint, so letter them again when it does.
    const fonts = this.ownerDocument.fonts;
    if (fonts && !this._fontsWatched) { this._fontsWatched = true; const again = () => { this._painter.invalidate(); this._queuePaint(); }; fonts.ready.then(again); fonts.addEventListener('loadingdone', again); }
    this._load();
  }

  disconnectedCallback() { if (this._ro) this._ro.disconnect(); }

  attributeChangedCallback(_name, oldV, newV) { if (this.isConnected && oldV !== newV) this._load(); }

  get theme() { return this._theme; }
  set theme(t) { this._themeRaw = t || {}; this._resolveTheme(); this._rebuild(); }

  /** Make themes available as a "base" for other themes. Keyed by their id. */
  registerThemes(list) {
    for (const t of list) this._themes[t.id] = t;
    this._resolveTheme();
    this._rebuild();
  }

  _resolveTheme() {
    try { this._theme = resolveTheme(this._themeRaw, this._themes); this._themeError = null; }
    catch (err) { this._themeError = String(err.message || err); }
  }

  get view() { return this._view; }
  set view(v) {
    const before = this._view.topology;
    this._view = overlay(DEFAULT_VIEW, v || {});
    if (this._view.topology !== before && this.isConnected) this._load(); else this._rebuild();
  }

  get topology() { return this._topology; }
  get layer() { return this._layer; }
  get legend() { return this._colored ? this._colored.legend : null; }
  /** The places the view asked to be named, highest first: [{ idx, rank, name, parent, text }]. */
  get callouts() { return this._colored ? this._colored.labels : []; }
  /** What the map says, in plain sentences worked out from the data: { headline, lines, caveats }. */
  get story() { return this._colored ? this._colored.story : null; }

  /** Light up some places and veil the rest. Pass place ids or indexes; pass null to clear. Used to show what a sentence is about. */
  spotlight(places) {
    const topo = this._topology;
    const idx = !places || !topo ? [] : places.map(p => (typeof p === 'number' ? p : topo.indexById.get(String(p)))).filter(i => i !== undefined && i >= 0);
    this._spotlight = idx.length ? idx : null;
    this._queuePaint();
  }

  /** Keep one place outlined, by id. Pass null to let go. Returns its readout model. */
  pin(geoId) {
    const idx = geoId == null || !this._topology ? undefined : this._topology.indexById.get(String(geoId));
    this._pinnedIdx = idx === undefined ? -1 : idx;
    this._queuePaint();
    return this._pinnedIdx >= 0 && this._colored ? buildReadout(this._pinnedIdx, this._colored.model) : null;
  }

  /** The readout model for one place id, or null when there is no layer or no such place. */
  readout(geoId) {
    if (!this._colored || !this._topology) return null;
    const idx = this._topology.indexById.get(String(geoId));
    return idx === undefined ? null : buildReadout(idx, this._colored.model);
  }

  /**
   * Load a layer. Every source goes through the same loader and yields the same report.
   * Colour comes from the view's measure and scale. The load report is the same whatever the view says.
   */
  async load(source, options = {}) {
    await this.ready;
    const { rows, headerHint } = await source.load();
    const knownGeoTypes = Object.values(this._registry.topologies).map(t => t.geo_type);
    const loaded = loadRows(rows, {
      topology: this._topology,
      header: { ...headerHint, ...(options.header || {}) },
      onDuplicate: options.onDuplicate,
      knownGeoTypes
    });
    this._layer = loaded;
    this._spotlight = null; this._pinnedIdx = -1;
    this._view = overlay(this._view, { layer: loaded.header.id });
    this._rebuild();
    const detail = { header: loaded.header, report: loaded.report, words: describeReport(loaded.report) };
    this.dispatchEvent(new CustomEvent('atlas-load', { detail }));
    return detail;
  }

  /** Drop the layer and return to the empty state. */
  clear() { this._spotlight = null; this._pinnedIdx = -1; this._layer = null; this._view = overlay(this._view, { layer: null }); this._rebuild(); }

  /** Run the colour pipeline. A refusal is kept as words, shown, and announced. It never throws out of here. */
  _colorize() {
    this._colored = null;
    const before = this._refusal;
    this._refusal = null;
    try {
      const problems = [...(this._themeError ? [this._themeError] : checkTheme(this._theme)), ...checkView(this._view)];
      if (problems.length) throw new Error(problems.join(' '));
      if (!this._layer) return null;
      this._colored = colorize({ layer: this._layer, view: this._view, theme: this._theme, topology: this._topology });
      return this._colored.fills;
    } catch (err) {
      this._refusal = String(err.message || err);
      if (this._refusal !== before) this.dispatchEvent(new CustomEvent('atlas-error', { detail: { message: this._refusal } }));
      return null;
    }
  }

  async _load() {
    const url = this.getAttribute('registry');
    const token = ++this._loadToken;
    try {
      if (!url) throw new Error('<orbital-atlas> needs a registry attribute pointing at a topology registry file.');
      const registry = await loadRegistry(url);
      this._registry = registry;
      const id = this._view.topology || this.getAttribute('topology') || registry.default;
      const topology = await loadTopology(registry, id);
      if (token !== this._loadToken) return;
      if (this._layer && this._layer.table.topology !== topology.id) this._layer = null;
      this._topology = topology;
      this._painter.setTopology(topology);
      this._resize(true);
    } catch (err) {
      if (token !== this._loadToken) return;
      this._showMessage(String(err.message || err), true);
      this.dispatchEvent(new CustomEvent('atlas-error', { detail: { message: String(err.message || err) } }));
      this._rejectReady(err);
    }
  }

  _resize(force) {
    const W = this.clientWidth, H = this.clientHeight;
    if (!W || !H) return;
    const dpr = Math.min(2, globalThis.devicePixelRatio || 1);
    const p = this._painter;
    if (!force && W === p.W && H === p.H && dpr === p.dpr) return;
    p.resize(W, H, dpr);
    this._rebuild();
    this._paint();          // resizing wipes a canvas. Paint now, inside the same frame, so the map never flashes blank.
  }

  _rebuild() {
    if (!this._topology) return;
    const began = performance.now();
    const fills = this._colorize();
    const c = this._colored;
    this._drawList = buildDrawList(this._topology, this._theme, { fills, marks: c ? c.marks : undefined, ink: c ? c.ink : null, labels: c ? c.labels : null });
    this._renderLegend();
    this._renderReadout();
    this.rebuild_ms = Math.round((performance.now() - began) * 10) / 10;
    // A screen reader gets the same headline a sighted reader does.
    this._canvas.setAttribute('aria-label', this._refusal || (this._colored ? this._colored.story.headline : this._view.empty_message || 'Map, no data loaded.'));
    this._queuePaint();
    // Whatever surrounds the map (a headline, a legend, a table) redraws from this. It fires after every rebuild, however it was caused.
    this.dispatchEvent(new CustomEvent('view-change', { detail: { view: this._view, legend: this.legend, story: this.story, refusal: this._refusal } }));
  }

  _queuePaint() {
    if (this._paintQueued) return;
    this._paintQueued = true;
    requestAnimationFrame(() => { this._paintQueued = false; this._paint(); });
  }

  _paint() {
    const p = this._painter, topo = this._topology;
    if (!topo || !this._drawList || !p.W) return;
    // The theme may keep room clear for type. Callouts, when the view asks for them, take a gutter on the right.
    const lay = this._theme.layout, named = this._colored && this._colored.labels.length;
    const t = fit(topo.bbox, p.W, p.H, 24, { ...lay.inset, right: (lay.inset.right || 0) + (named ? lay.callout_gutter : 0) });
    const lit = !!this._colored;
    const result = p.paint(this._drawList, t, buildOverlay(this._theme, { hover: lit ? this._hoverIdx : -1, pinned: lit ? this._pinnedIdx : -1, spotlight: lit ? this._spotlight : null }));

    this._msg.style.fontFamily = this._theme.type.data;
    this._msg.style.color = this._theme.lines.outline.color;
    if (this._refusal) this._showMessage(this._refusal, true);
    else if (!this._layer) this._showMessage(this._view.empty_message || '', false);
    else this._msg.hidden = true;

    const first = !this.stats;
    this.stats = {
      topology: topo.id, places: topo.places.length, parents: topo.parents.length,
      bbox: topo.bbox, painted: result.places, transform: t, size: [p.W, p.H]
    };
    if (first) {
      this._resolveReady(this.stats);
      this.dispatchEvent(new CustomEvent('atlas-ready', { detail: this.stats }));
    }
  }

  _onPointer(e) {
    if (!this.stats || !this._topology) return;
    const box = this._canvas.getBoundingClientRect();
    const [mx, my] = unproject(this.stats.transform, e.clientX - box.left, e.clientY - box.top);
    this._setHover(hitTest(this._topology, mx, my));
  }

  _onClick(e) {
    if (!this.stats || !this._topology || !this._colored) return;
    const box = this._canvas.getBoundingClientRect();
    const [mx, my] = unproject(this.stats.transform, e.clientX - box.left, e.clientY - box.top);
    const idx = hitTest(this._topology, mx, my);
    this.dispatchEvent(new CustomEvent('place-click', { detail: idx < 0 ? null : buildReadout(idx, this._colored.model) }));
  }

  _setHover(idx) {
    if (idx === this._hoverIdx) return;
    this._hoverIdx = idx;
    this._queuePaint();
    const detail = this._renderReadout();
    this.dispatchEvent(new CustomEvent('place-hover', { detail }));
  }

  _panelLook(el) {
    el.style.fontFamily = this._theme.type.data;
    el.style.color = this._theme.lines.outline.color;
    el.style.background = this._theme.ground.background + 'e6';
    el.style.boxShadow = `0 0 0 1px ${this._theme.lines.outline.color}22`;
  }

  _renderLegend() {
    const L = this.legend, el = this._legendEl;
    if (!L) { el.hidden = true; el.replaceChildren(); return; }
    const mk = (cls, text) => { const d = document.createElement('div'); d.className = cls; if (text != null) d.textContent = text; return d; };
    const swatch = (entry, extra) => {
      const row = mk('cl' + (extra ? ' ' + extra : ''));
      const i = document.createElement('i'); i.style.background = entry.color;
      row.append(i, mk('', entry.text), mk('dim', entry.count_text));
      return row;
    };
    const kids = [mk('ttl', L.title), mk('dim', [L.caption, L.unit, L.period === 'latest' ? null : L.period].filter(Boolean).join(' · '))];
    kids[0].style.fontFamily = this._theme.type.display;
    if (L.kind === 'ramp') {
      const bar = mk('ramp');
      bar.style.background = `linear-gradient(to right, ${L.stops.map(s => `${s.color} ${s.t * 100}%`).join(', ')})`;
      const ticks = mk('ticks');
      // Labels alternate between two rows, so close ticks stay readable instead of printing over each other.
      L.ticks.forEach((tk, k) => {
        const s = document.createElement('span');
        s.textContent = tk.text; s.style.left = `${tk.t * 100}%`;
        s.className = (k % 2 ? 'low ' : '') + (tk.t < 0.12 ? 'first' : tk.t > 0.88 ? 'last' : '');
        ticks.append(s);
      });
      kids.push(bar, ticks);
    } else {
      L.classes.forEach((c, k) => kids.push(swatch(c, k ? '' : 'gap')));
    }
    if (L.zero) kids.push(swatch(L.zero, 'gap'));
    if (L.no_data) kids.push(swatch(L.no_data, L.zero ? '' : 'gap'));
    // Role swatches are drawn the way the theme draws the role, over a sample of the map's own colour.
    L.roles.forEach((r, k) => {
      const row = swatch({ color: r.under, text: r.text, count_text: r.count_text }, k ? '' : 'gap');
      const i = row.firstChild;
      if (r.style === 'accent_fill' || r.style === 'fill' || r.style === 'desaturate') i.style.background = r.color;
      else if (r.style === 'outline') { i.style.boxShadow = `inset 0 0 0 2px ${r.color}`; }
      else if (r.style === 'hatch') i.style.background = `repeating-linear-gradient(135deg, ${r.color} 0 1px, ${r.under} 1px 4px)`;
      else if (r.style === 'dot') { i.className = 'dot'; i.style.setProperty('--mark', r.color); }
      kids.push(row);
    });
    for (const n of L.notes) kids.push(mk('note', n));
    this._panelLook(el);
    el.replaceChildren(...kids);
    el.hidden = false;
  }

  /** Draw the readout for the hovered place. Returns the model, so the hover event can carry it. */
  _renderReadout() {
    const el = this._readoutEl;
    if (!this._colored || this._hoverIdx < 0) { el.hidden = true; el.replaceChildren(); return null; }
    const R = buildReadout(this._hoverIdx, this._colored.model);
    const mk = (cls, text) => { const d = document.createElement('div'); d.className = cls; if (text != null) d.textContent = text; return d; };
    const grid = rows => {
      const g = mk('kv');
      for (const r of rows) g.append(mk(r.driving ? 'drive' : 'dim', r.label), mk('v' + (r.driving ? ' drive' : ''), r.text));
      return g;
    };
    const head = mk('ttl', R.parent ? `${R.name}, ${R.parent}` : R.name);
    head.style.fontFamily = this._theme.type.display;
    const kids = [head, mk('dim', R.id + (R.has_data ? '' : ' · no data'))];
    const rankRow = R.rank ? [{ label: 'Rank', text: R.rank.text, driving: false }] : [];
    const top = R.rows.filter(r => r.always), rest = R.rows.filter(r => !r.always);
    kids.push(grid([...top, ...(R.rank && R.rank.always ? rankRow : [])]));
    const more = [...rest, ...(R.rank && !R.rank.always ? rankRow : [])];
    if (more.length) {
      const d = document.createElement('details');
      d.open = this._moreOpen;
      d.addEventListener('toggle', () => { this._moreOpen = d.open; });
      const sum = document.createElement('summary'); sum.textContent = 'more';
      d.append(sum, grid(more));
      kids.push(d);
    }
    for (const n of R.notes) kids.push(mk('note', n));
    this._panelLook(el);
    el.replaceChildren(...kids);
    el.hidden = false;
    return R;
  }

  _showMessage(text, isError) {
    this._msg.textContent = text;
    this._msg.classList.toggle('err', !!isError);
    this._msg.hidden = !text;
  }
}

if (!customElements.get('orbital-atlas')) customElements.define('orbital-atlas', OrbitalAtlas);
