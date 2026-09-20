// Canvas painter. The ONLY module allowed to touch a canvas.
// It receives a draw list and a camera transform and carries them out.

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

export class CanvasPainter {
  /** @param {HTMLCanvasElement} canvas */
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.topologyId = null;
    this.placePaths = [];
    this.meshPaths = {};
    this.landPath = null;
    this.W = 0; this.H = 0; this.dpr = 1;
  }

  /** Build shape paths once per topology. Zoom is a transform, never a rebuild. */
  setTopology(topology) {
    this.topologyId = topology.id;
    this.placePaths = topology.places.map(pl => pathFromPolygons(pl.polygons));
    this.meshPaths = {
      places: pathFromLines(topology.meshes.places),
      parents: pathFromLines(topology.meshes.parents),
      outline: pathFromLines(topology.meshes.outline)
    };
    this.landPath = topology.outlinePolygons.length ? pathFromPolygons(topology.outlinePolygons) : null;
  }

  resize(W, H, dpr) {
    this.W = W; this.H = H; this.dpr = dpr;
    this.canvas.width = Math.max(1, Math.round(W * dpr));
    this.canvas.height = Math.max(1, Math.round(H * dpr));
  }

  /**
   * @param {{topologyId: string, ops: Object[]}} drawList
   * @param {{k: number, x: number, y: number}} t
   * @returns {{places: number, ops: number}} what was actually painted
   */
  paint(drawList, t) {
    if (drawList.topologyId !== this.topologyId) throw new Error('Draw list and painter disagree on topology.');
    const { ctx, dpr } = this;
    let painted = 0;
    for (const op of drawList.ops) {
      if (op.op === 'ground') {
        ctx.setTransform(1, 0, 0, 1, 0, 0);
        ctx.globalAlpha = 1;
        ctx.fillStyle = op.color;
        ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        ctx.setTransform(dpr * t.k, 0, 0, dpr * t.k, dpr * t.x, dpr * t.y);
      } else if (op.op === 'land') {
        if (this.landPath) { ctx.fillStyle = op.color; ctx.fill(this.landPath); }
      } else if (op.op === 'places') {
        const paths = this.placePaths;
        if (op.fills.length !== paths.length) throw new Error(`Painter got ${op.fills.length} fills for ${paths.length} shapes.`);
        let last = null;
        for (let i = 0; i < paths.length; i++) {
          const c = op.fills[i];
          if (c !== last) { ctx.fillStyle = c; last = c; }
          ctx.fill(paths[i]);
          painted++;
        }
      } else if (op.op === 'mesh') {
        ctx.globalAlpha = op.opacity;
        ctx.strokeStyle = op.color;
        ctx.lineWidth = op.width / t.k;
        ctx.lineJoin = 'round';
        ctx.stroke(this.meshPaths[op.which]);
        ctx.globalAlpha = 1;
      }
    }
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    return { places: painted, ops: drawList.ops.length };
  }
}
