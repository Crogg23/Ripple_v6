// Canvas painter. The ONLY module allowed to touch a canvas.
// It receives a draw list and a camera transform and carries them out.
//
// The finished map is kept on a hidden canvas. Hover paints that copy back and adds one outline,
// so moving the pointer never redraws thousands of shapes.

function pathFromPolygons(polygons) {
  const p = new Path2D();
  for (const poly of polygons) {
    for (const ring of poly) {
      if (!ring.length) continue;
      p.moveTo(ring[0][0], ring[0][1]);
      for (let i = 1; i < ring.length; i++) p.lineTo(ring[i][0], ring[i][1]);
      p.closePath();
    }
  }
  return p;
}

function pathFromLines(lines) {
  const p = new Path2D();
  for (const line of lines) {
    if (!line.length) continue;
    p.moveTo(line[0][0], line[0][1]);
    for (let i = 1; i < line.length; i++) p.lineTo(line[i][0], line[i][1]);
  }
  return p;
}

/** A static noise tile. Seeded, so it is the same every time and never shimmers. */
function noiseTile(doc, size, warm) {
  const c = doc.createElement('canvas');
  c.width = c.height = size;
  const g = c.getContext('2d');
  const img = g.createImageData(size, size);
  let seed = 20260919;
  for (let i = 0; i < img.data.length; i += 4) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    const v = 96 + Math.floor((seed / 2147483648) * 128);
    img.data[i] = warm ? Math.min(255, v + 18) : v; img.data[i + 1] = warm ? v + 6 : v; img.data[i + 2] = warm ? Math.max(0, v - 14) : v; img.data[i + 3] = 255;
  }
  g.putImageData(img, 0, 0);
  return c;
}

export class CanvasPainter {
  /** @param {HTMLCanvasElement} canvas */
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.topologyId = null;
    this.placePaths = [];
    this.placeBoxes = [];
    this.meshPaths = {};
    this.landPath = null;
    this.W = 0; this.H = 0; this.dpr = 1;
    this._base = null; this._baseKey = null; this._tiles = {};
  }

  /** Build shape paths once per topology. Zoom is a transform, never a rebuild. */
  setTopology(topology) {
    this.topologyId = topology.id;
    this.placePaths = topology.places.map(pl => pathFromPolygons(pl.polygons));
    this.placeBoxes = topology.places.map(pl => pl.bbox);
    this.meshPaths = {
      places: pathFromLines(topology.meshes.places),
      parents: pathFromLines(topology.meshes.parents),
      outline: pathFromLines(topology.meshes.outline)
    };
    this.landPath = topology.outlinePolygons.length ? pathFromPolygons(topology.outlinePolygons) : null;
    this._baseKey = null;
  }

  /** Forget the cached map, so the next paint redraws it. Used when a typeface finishes loading. */
  invalidate() { this._baseKey = null; }

  resize(W, H, dpr) {
    this.W = W; this.H = H; this.dpr = dpr;
    this.canvas.width = Math.max(1, Math.round(W * dpr));
    this.canvas.height = Math.max(1, Math.round(H * dpr));
    this._baseKey = null;
  }

  /**
   * @param {{topologyId: string, ops: Object[]}} drawList
   * @param {{k: number, x: number, y: number}} t
   * @param {Object[]} [overlay]   ops painted over the cached map, such as the hover outline
   * @returns {{places: number, ops: number, cached: boolean}} what was actually painted
   */
  paint(drawList, t, overlay = []) {
    if (drawList.topologyId !== this.topologyId) throw new Error('Draw list and painter disagree on topology.');
    const w = this.canvas.width, h = this.canvas.height;
    if (!this._base) this._base = this.canvas.ownerDocument.createElement('canvas');
    const base = this._base;
    const cached = this._baseKey && this._baseKey.list === drawList && this._baseKey.k === t.k && this._baseKey.x === t.x && this._baseKey.y === t.y;
    if (!cached) {
      base.width = w; base.height = h;
      this._painted = this._run(base.getContext('2d'), drawList.ops, t, w, h);
      this._baseKey = { list: drawList, k: t.k, x: t.x, y: t.y };
    }
    const ctx = this.ctx;
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over';
    ctx.clearRect(0, 0, w, h);
    ctx.drawImage(base, 0, 0);
    if (overlay.length) this._run(ctx, overlay, t, w, h);
    return { places: this._painted, ops: drawList.ops.length, cached: !!cached };
  }

  _run(ctx, ops, t, w, h) {
    const dpr = this.dpr, paths = this.placePaths;
    const camera = () => ctx.setTransform(dpr * t.k, 0, 0, dpr * t.k, dpr * t.x, dpr * t.y);
    let painted = 0, lastFills = null;
    camera();
    for (const op of ops) {
      if (op.op === 'ground') {
        ctx.setTransform(1, 0, 0, 1, 0, 0);
        ctx.globalAlpha = 1;
        ctx.fillStyle = op.color;
        ctx.fillRect(0, 0, w, h);
        camera();
      } else if (op.op === 'land') {
        if (this.landPath) {
          ctx.save();
          if (op.shadow) { ctx.shadowColor = op.shadow.color; ctx.shadowBlur = (op.shadow.blur || 0) * dpr; ctx.shadowOffsetX = (op.shadow.dx || 0) * dpr; ctx.shadowOffsetY = (op.shadow.dy || 0) * dpr; }
          ctx.fillStyle = op.color; ctx.fill(this.landPath);
          ctx.restore();
        }
      } else if (op.op === 'places') {
        if (op.fills.length !== paths.length) throw new Error(`Painter got ${op.fills.length} fills for ${paths.length} shapes.`);
        let last = null;
        for (let i = 0; i < paths.length; i++) {
          const c = op.fills[i];
          if (c !== last) { ctx.fillStyle = c; last = c; }
          ctx.fill(paths[i]);
          painted++;
        }
        lastFills = op.fills;
      } else if (op.op === 'glow') {
        ctx.save();
        ctx.shadowColor = op.color; ctx.shadowBlur = op.blur * dpr;
        for (const i of op.places) { ctx.fillStyle = lastFills ? lastFills[i] : op.color; ctx.fill(paths[i]); }
        ctx.restore();
      } else if (op.op === 'hatch') {
        ctx.strokeStyle = op.color; ctx.lineWidth = op.width / t.k;
        const gap = op.spacing / t.k, back = op.angle < 0;
        const [ox, oy] = (op.offset || [0, 0]).map(v => v / t.k);       // a nudge, for the misregistered second ink of a print look
        for (const i of op.places) {
          const [x0, y0, x1, y1] = this.placeBoxes[i];
          ctx.save();
          ctx.clip(paths[i]);
          ctx.beginPath();
          // Each line is x + y = c (or x - y = c), with c on a map-wide grid. So hatching lines up across neighbours.
          if (back) for (let c = Math.ceil((x0 - y1) / gap) * gap; c <= x1 - y0; c += gap) { ctx.moveTo(c + y0 + ox, y0 + oy); ctx.lineTo(c + y1 + ox, y1 + oy); }
          else for (let c = Math.ceil((x0 + y0) / gap) * gap; c <= x1 + y1; c += gap) { ctx.moveTo(c - y1 + ox, y1 + oy); ctx.lineTo(c - y0 + ox, y0 + oy); }
          ctx.stroke();
          ctx.restore();
        }
      } else if (op.op === 'stipple') {
        // Dots go on their own sheet first, so a soft bloom of the same sheet can sit under the sharp dots.
        const sheet = this._sheet || (this._sheet = this.canvas.ownerDocument.createElement('canvas'));
        sheet.width = w; sheet.height = h;
        const g = sheet.getContext('2d');
        g.setTransform(dpr * t.k, 0, 0, dpr * t.k, dpr * t.x, dpr * t.y);
        const r = op.radius / t.k, round = op.radius * dpr > 1.1;
        for (const run of op.runs) {
          g.fillStyle = run.color;
          g.beginPath();
          for (let j = 0; j < run.points.length; j += 2) {
            const x = run.points[j], y = run.points[j + 1];
            if (round) { g.moveTo(x + r, y); g.arc(x, y, r, 0, Math.PI * 2); } else g.rect(x - r, y - r, 2 * r, 2 * r);
          }
          g.fill();
        }
        ctx.save();
        ctx.setTransform(1, 0, 0, 1, 0, 0);
        ctx.globalCompositeOperation = op.blend || 'source-over';
        if (op.bloom > 0) {
          for (const [blur, alpha] of [[op.bloom * 2.4, 0.55], [op.bloom, 1]]) {
            ctx.filter = `blur(${blur * dpr}px)`; ctx.globalAlpha = Math.min(1, op.bloom_strength * alpha);
            ctx.drawImage(sheet, 0, 0);
          }
          ctx.filter = 'none';
        }
        ctx.globalAlpha = 1;
        ctx.drawImage(sheet, 0, 0);
        ctx.restore();
      } else if (op.op === 'strokes') {
        // Lines go on their own sheet, clipped to the land, so a bloom of the same sheet can sit under them.
        const sheet = this._sheet || (this._sheet = this.canvas.ownerDocument.createElement('canvas'));
        sheet.width = w; sheet.height = h;
        const g = sheet.getContext('2d');
        g.setTransform(dpr * t.k, 0, 0, dpr * t.k, dpr * t.x, dpr * t.y);
        if (op.clip && this.landPath) g.clip(this.landPath);
        g.lineCap = 'round'; g.lineJoin = 'round';
        for (const set of op.sets) {
          g.strokeStyle = set.color; g.lineWidth = set.width / t.k; g.globalAlpha = set.opacity == null ? 1 : set.opacity;
          g.beginPath();
          if (set.segments) for (let j = 0; j < set.segments.length; j += 4) { g.moveTo(set.segments[j], set.segments[j + 1]); g.lineTo(set.segments[j + 2], set.segments[j + 3]); }
          else for (const line of set.lines) { g.moveTo(line[0], line[1]); for (let j = 2; j < line.length; j += 2) g.lineTo(line[j], line[j + 1]); }
          g.stroke();
        }
        ctx.save();
        ctx.setTransform(1, 0, 0, 1, 0, 0);
        ctx.globalCompositeOperation = op.blend || 'source-over';
        if (op.bloom > 0) { ctx.filter = `blur(${op.bloom * dpr}px)`; ctx.globalAlpha = Math.min(1, op.bloom_strength); ctx.drawImage(sheet, 0, 0); ctx.filter = 'none'; ctx.globalAlpha = 1; }
        ctx.drawImage(sheet, 0, 0);
        ctx.restore();
      } else if (op.op === 'ridges') {
        // Back to front. Each slice is filled with the ground colour below its line, so nearer slices hide farther ones.
        const lift = op.amp / t.k;
        ctx.lineJoin = 'round'; ctx.lineWidth = op.width / t.k;
        for (const row of op.rows) for (const run of row.runs) {
          let peak = 0;
          ctx.beginPath();
          ctx.moveTo(run[0], run[1]);
          for (let j = 0; j < run.length; j += 3) { ctx.lineTo(run[j], run[j + 1] - run[j + 2] * lift); if (run[j + 2] > peak) peak = run[j + 2]; }
          ctx.lineTo(run[run.length - 3], run[run.length - 2]);
          ctx.closePath();
          ctx.fillStyle = op.fill; ctx.fill();
          ctx.beginPath();
          ctx.moveTo(run[0], run[1] - run[2] * lift);
          for (let j = 3; j < run.length; j += 3) ctx.lineTo(run[j], run[j + 1] - run[j + 2] * lift);
          ctx.strokeStyle = op.stroke || op.ramp[Math.max(0, Math.min(20, Math.round(peak * 20)))];
          ctx.stroke();
        }
      } else if (op.op === 'callouts') {
        // Labels stack in the right gutter, in the same top-to-bottom order as their places, each tied back by a thin leader.
        ctx.save();
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
        const W = w / dpr, H = h / dpr, left = W - (op.gutter || 190) + 14, step = 44;
        const items = op.items.map(it => ({ ...it, sx: it.x * t.k + t.x, sy: it.y * t.k + t.y })).sort((a, b) => a.sy - b.sy);
        let top = Math.max(40, Math.min(items.length ? items[0].sy - 10 : 40, H - 40 - step * items.length));
        items.forEach((it, k) => { it.ly = Math.max(top + step * k, Math.min(it.sy, H - 40 - step * (items.length - 1 - k))); top = it.ly - step * k; });
        ctx.strokeStyle = op.color; ctx.fillStyle = op.color; ctx.lineWidth = 0.75;
        for (const it of items) {
          ctx.globalAlpha = 0.45;
          ctx.beginPath(); ctx.moveTo(it.sx, it.sy); ctx.lineTo(left - 26, it.ly - 4); ctx.lineTo(left - 8, it.ly - 4); ctx.stroke();
          ctx.globalAlpha = 1;
          ctx.beginPath(); ctx.arc(it.sx, it.sy, 2.2, 0, Math.PI * 2); ctx.fill();
          ctx.font = `15px ${op.display}`; ctx.textBaseline = 'alphabetic';
          ctx.fillText(it.name, left, it.ly);
          ctx.globalAlpha = 0.78; ctx.font = `11px ${op.data}`;
          ctx.fillText(`${it.text}${it.sub ? '  ·  ' + it.sub.toUpperCase() : ''}`, left, it.ly + 14);
          ctx.globalAlpha = 1;
        }
        ctx.restore();
        camera();
      } else if (op.op === 'mesh') {
        ctx.globalAlpha = op.opacity;
        ctx.strokeStyle = op.color;
        ctx.lineWidth = op.width / t.k;
        ctx.lineJoin = 'round';
        ctx.stroke(this.meshPaths[op.which]);
        ctx.globalAlpha = 1;
      } else if (op.op === 'veil') {
        // One path: the land, plus every kept place. Even-odd filling then covers the land and skips the kept places.
        if (this._veilFor !== op.keep) {
          const hole = new Path2D();
          if (this.landPath) hole.addPath(this.landPath);
          for (const i of op.keep) hole.addPath(paths[i]);
          this._veil = hole; this._veilFor = op.keep;
        }
        ctx.globalAlpha = op.amount; ctx.fillStyle = op.color;
        ctx.fill(this._veil, 'evenodd');
        ctx.globalAlpha = 1;
      } else if (op.op === 'outlines') {
        ctx.strokeStyle = op.color; ctx.lineWidth = op.width / t.k; ctx.lineJoin = 'round';
        for (const i of op.places) ctx.stroke(paths[i]);
      } else if (op.op === 'dots') {
        ctx.fillStyle = op.color;
        ctx.beginPath();
        for (const [x, y] of op.points) { ctx.moveTo(x + op.radius / t.k, y); ctx.arc(x, y, op.radius / t.k, 0, Math.PI * 2); }
        ctx.fill();
      } else if (op.op === 'light') {
        ctx.setTransform(1, 0, 0, 1, 0, 0);
        const g = ctx.createRadialGradient(w * 0.42, h * 0.38, 0, w * 0.5, h * 0.5, Math.hypot(w, h) * 0.6);
        g.addColorStop(0, 'rgba(0,0,0,0)');
        g.addColorStop(1, `rgba(0,0,0,${Math.min(1, op.strength) * 0.6})`);
        ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
        camera();
      } else if (op.op === 'texture') {
        ctx.setTransform(1, 0, 0, 1, 0, 0);
        if (op.kind === 'blueprint') {
          ctx.globalAlpha = 0.07; ctx.strokeStyle = op.color; ctx.lineWidth = 1;
          ctx.beginPath();
          for (let x = 0.5; x < w; x += 24 * dpr) { ctx.moveTo(x, 0); ctx.lineTo(x, h); }
          for (let y = 0.5; y < h; y += 24 * dpr) { ctx.moveTo(0, y); ctx.lineTo(w, y); }
          ctx.stroke();
        } else {
          const warm = op.kind === 'paper';
          const tile = this._tiles[op.kind] || (this._tiles[op.kind] = noiseTile(this.canvas.ownerDocument, 128, warm));
          ctx.globalCompositeOperation = warm ? 'multiply' : 'overlay';
          ctx.globalAlpha = warm ? 0.22 : 0.12;
          ctx.fillStyle = ctx.createPattern(tile, 'repeat');
          ctx.fillRect(0, 0, w, h);
        }
        ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over';
        camera();
      }
    }
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    return painted;
  }
}
