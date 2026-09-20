// <orbital-atlas>: the shell any host can drop in.
//
//   <orbital-atlas registry="../topologies/registry.json"></orbital-atlas>
//
//   el.theme = {...}          partial themes are laid over the default
//   el.view  = {...}
//   await el.ready            resolves with stats once the first paint is done
//   await el.load(source, { header, onDuplicate })     source: sources.paste(text) | .file(f) | .url(u) | .rows(rows)
//                             resolves with { header, report, words }; also fires 'atlas-load'
//   'atlas-ready' / 'atlas-error' events
//
// The shell wires things together. It does no drawing of its own.

import { loadRegistry, loadTopology } from '../topology/registry.js';
import { buildDrawList } from '../engine/drawlist.js';
import { fit } from '../engine/frame.js';
import { DEFAULT_THEME, DEFAULT_VIEW, overlay } from '../engine/defaults.js';
import { CanvasPainter } from '../painter/canvas.js';
import { loadRows, resolvePeriod } from '../loader/load.js';
import { describeReport } from '../loader/report.js';
import { sources } from '../adapters/sources.js';

const STYLE = `
  :host { display: block; position: relative; width: 100%; height: 100%; min-height: 240px; overflow: hidden; }
  canvas { position: absolute; inset: 0; width: 100%; height: 100%; display: block; }
  .msg { position: absolute; left: 24px; bottom: 20px; right: 24px; pointer-events: none;
         font-size: 12px; line-height: 1.5; letter-spacing: 0.02em; opacity: 0.7; }
  .msg[hidden] { display: none; }
  .err { color: #ff8a80; opacity: 1; }
`;

export { sources };

export class OrbitalAtlas extends HTMLElement {
  static get observedAttributes() { return ['registry', 'topology']; }

  constructor() {
    super();
    const root = this.attachShadow({ mode: 'open' });
    root.innerHTML = `<style>${STYLE}</style><canvas part="canvas"></canvas><div class="msg" part="message" aria-live="polite" hidden></div>`;
    this._canvas = root.querySelector('canvas');
    this._msg = root.querySelector('.msg');
    this._painter = new CanvasPainter(this._canvas);
    this._theme = DEFAULT_THEME;
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
    this._load();
  }

  disconnectedCallback() { if (this._ro) this._ro.disconnect(); }

  attributeChangedCallback(_name, oldV, newV) { if (this.isConnected && oldV !== newV) this._load(); }

  get theme() { return this._theme; }
  set theme(t) { this._theme = overlay(DEFAULT_THEME, t || {}); this._rebuild(); }

  get view() { return this._view; }
  set view(v) {
    const before = this._view.topology;
    this._view = overlay(DEFAULT_VIEW, v || {});
    if (this._view.topology !== before && this.isConnected) this._load(); else this._rebuild();
  }

  get topology() { return this._topology; }
  get layer() { return this._layer; }

  /**
   * Load a layer. Every source goes through the same loader and yields the same report.
   * Slice 1 draws presence only: places with a row are lit. Colour by value arrives with the scale.
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
    this._view = overlay(this._view, { layer: loaded.header.id });
    this._rebuild();
    const detail = { header: loaded.header, report: loaded.report, words: describeReport(loaded.report) };
    this.dispatchEvent(new CustomEvent('atlas-load', { detail }));
    return detail;
  }

  /** Drop the layer and return to the empty state. */
  clear() { this._layer = null; this._view = overlay(this._view, { layer: null }); this._rebuild(); }

  _fills() {
    if (!this._layer) return null;
    const period = resolvePeriod(this._layer.table, this._view.period);
    if (!period) return null;
    const value = this._layer.table.byPeriod[period].value;
    const lit = this._theme.roles.present.color, dark = this._theme.roles.no_data.color;
    const fills = new Array(value.length);
    // Lit means "has a value". A row with an empty value is no data, exactly as the load report says.
    for (let i = 0; i < value.length; i++) fills[i] = Number.isNaN(value[i]) ? dark : lit;
    return fills;
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
  }

  _rebuild() {
    if (!this._topology) return;
    this._drawList = buildDrawList(this._topology, this._theme, { fills: this._fills() });
    this._queuePaint();
  }

  _queuePaint() {
    if (this._paintQueued) return;
    this._paintQueued = true;
    requestAnimationFrame(() => { this._paintQueued = false; this._paint(); });
  }

  _paint() {
    const p = this._painter, topo = this._topology;
    if (!topo || !this._drawList || !p.W) return;
    const t = fit(topo.bbox, p.W, p.H, 24);
    const result = p.paint(this._drawList, t);

    this._msg.style.fontFamily = this._theme.type.data;
    this._msg.style.color = this._theme.lines.outline.color;
    if (!this._layer) this._showMessage(this._view.empty_message || '', false); else this._msg.hidden = true;

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

  _showMessage(text, isError) {
    this._msg.textContent = text;
    this._msg.classList.toggle('err', !!isError);
    this._msg.hidden = !text;
  }
}

if (!customElements.get('orbital-atlas')) customElements.define('orbital-atlas', OrbitalAtlas);
