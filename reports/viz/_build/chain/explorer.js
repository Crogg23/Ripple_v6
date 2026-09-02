/* Explorer layer: Map / Routes / Trails tabs over the same HANDBOOK payload.
   Plain JS, no framework. The pivot (x-dc chain explorer) is untouched inside #view-pivot. */
(function () {
  const TABLES = window.HANDBOOK_TABLES || [];
  const CTX = window.HANDBOOK_CONTEXT || {};
  const META = window.HANDBOOK_META || {};
  const BY = {}; TABLES.forEach(t => { BY[t.id] = t; });
  const TIER_COLOR = { solid: '#f4a23a', strong: '#4c9aff', translation: '#b07cf0', measured: '#2dd4bf', location: '#3fb950' };
  const TIER_WORD = { solid: 'certain', strong: 'very likely', translation: 'verified translation', measured: 'measured, not wired in', location: 'same place only' };


  /* ---------- human names: what the table actually is, bar-speak ---------- */
  const HUMAN = window.HANDBOOK_HUMAN || {};
  function labelOf(id) {
    if (HUMAN[id]) return HUMAN[id];
    const t = BY[id]; return t && t.label ? t.label : id;
  }
  function rawLabel(id) { const t = BY[id]; return t && t.label ? t.label : id; }
  function short(id) { return id.replace(/^(FED|STATE|INTL|XC|LOCAL)_/, '').replace(/_/g, ' '); }
  function domOf(id) { const c = CTX[id]; return (c && c.dom ? String(c.dom) : 'other').split(' ')[0]; }

  /* ---------- undirected edge list (best tier per pair) ---------- */
  const TIER_RANK = { solid: 0, strong: 1, translation: 2, measured: 3, location: 4 };
  const pairMap = {};
  TABLES.forEach(t => t.conns.forEach(c => {
    if (!BY[c.id] || c.id === t.id) return;
    const k = t.id < c.id ? t.id + '|' + c.id : c.id + '|' + t.id;
    const cur = pairMap[k];
    if (!cur || TIER_RANK[c.tier] < TIER_RANK[cur.tier] || (c.tier === cur.tier && (c.pct || 0) > (cur.pct || 0))) {
      const cols = {}; if (c.lc) cols[t.id] = c.lc; if (c.rc) cols[c.id] = c.rc;
      pairMap[k] = { a: t.id < c.id ? t.id : c.id, b: t.id < c.id ? c.id : t.id, tier: c.tier, pct: c.pct, jk: c.jk, cols, norm: c.norm || '', note: c.note || '' };
    }
  }));
  const EDGES = Object.values(pairMap);
  const ID_EDGES = EDGES.filter(e => e.tier !== 'location');

  /* ---------- tabs ---------- */
  const tabs = ['things', 'map', 'routes', 'trails', 'pivot'];
  function show(name) {
    tabs.forEach(t => {
      const v = document.getElementById('view-' + t);
      if (v) v.style.display = t === name ? '' : 'none';
      const b = document.getElementById('tab-' + t);
      if (b) { b.style.background = t === name ? 'rgba(76,154,255,0.18)' : 'transparent'; b.style.color = t === name ? '#e8eaed' : '#9aa5b3'; b.style.borderColor = t === name ? 'rgba(76,154,255,0.5)' : 'rgba(255,255,255,0.10)'; }
    });
    if (name === 'things') initThings();
    if (name === 'map') initMap();
    if (name === 'routes') initRoutes();
    if (name === 'trails') initTrails();
    if (name === 'pivot') window.dispatchEvent(new Event('resize'));
    if (name !== 'pivot') setHash('#tab=' + name);
  }
  window.__showTab = show;
  let suppressHash = false;
  function setHash(h) { if (location.hash !== h) { suppressHash = true; location.hash = h; } }
  function openPivot(id, tries) {
    show('pivot'); setHash('#pivot=' + id);
    if (window.__openPivot) { window.__openPivot(id); return; }
    if ((tries || 0) < 20) setTimeout(() => openPivot(id, (tries || 0) + 1), 50);
  }
  function applyHash() {
    const h = location.hash.replace(/^#/, '');
    const m = h.match(/^(tab|thing|route|pivot)=(.*)$/);
    if (!m) { show('things'); return; }
    if (m[1] === 'tab') { show(tabs.indexOf(m[2]) >= 0 ? m[2] : 'things'); return; }
    if (m[1] === 'thing') { show('things'); if (window.__openThing) window.__openThing(m[2]); return; }
    if (m[1] === 'pivot') { openPivot(m[2]); return; }
    if (m[1] === 'route') {
      const ends = m[2].split('..');
      show('routes');
      const A = document.getElementById('route-a'), B = document.getElementById('route-b');
      if (A && B && ends.length === 2) { A.value = ends[0]; B.value = ends[1]; document.getElementById('route-go').click(); }
    }
  }
  window.addEventListener('hashchange', () => {
    if (suppressHash) { suppressHash = false; return; }
    applyHash();
  });

  /* ---------- MAP ---------- */
  const DOM_PALETTE = ['#4c9aff', '#f4a23a', '#3fb950', '#b07cf0', '#2dd4bf', '#e5534b', '#d9a441', '#7fb6ff', '#8fceac', '#e08fb7', '#9aa5b3', '#c0ca6e'];
  const domColor = {};
  function colorOfDom(d) {
    if (!domColor[d]) domColor[d] = DOM_PALETTE[Object.keys(domColor).length % DOM_PALETTE.length];
    return domColor[d];
  }
  let mapStarted = false;
  function initMap() {
    if (mapStarted) return; mapStarted = true;
    const cv = document.getElementById('map-canvas');
    const W = cv.width = cv.clientWidth * devicePixelRatio;
    const H = cv.height = cv.clientHeight * devicePixelRatio;
    const g = cv.getContext('2d');
    const px = devicePixelRatio;

    // each connected table joins the entity cluster it shares the most keys with
    const clusters = {};
    const nodes = [];
    const byN = {};
    TABLES.forEach(tb => {
      const deg = tb.conns.filter(c => c.tier !== 'location').length;
      if (!deg) return;
      const ks = Object.keys(tableKeys[tb.id] || {});
      let best = null, bestN = 0;
      ENTITIES.forEach(ent => {
        if (ent.place) return;
        const n = ks.filter(k => ent.keys.indexOf(k) >= 0).length;
        if (n > bestN) { bestN = n; best = ent; }
      });
      const cid = best ? best.id : 'other';
      (clusters[cid] = clusters[cid] || []).push({ id: tb.id, deg, r: (3 + Math.sqrt(deg) * 1.7) * px });
    });
    const order = ENTITIES.filter(en => clusters[en.id]).map(en => en.id).concat(clusters.other ? ['other'] : []);
    const entBy = {}; ENTITIES.forEach(en => { entBy[en.id] = en; });

    // anchors on a grid, cell area proportional-ish: big clusters get center row
    // row-packing: place clusters left to right, wrapping when a row fills;
    // each cluster claims a box sized by its real radius, so blobs never collide
    const anchors = {};
    const sorted = order.slice().sort((a, b) => clusters[b].length - clusters[a].length);
    let cx0 = 0, cy0 = 0, rowH = 0, usedW = 0;
    const PAD = 30 * px, LABEL = 34 * px;
    sorted.forEach(cid => {
      const r = 12 * px * Math.sqrt(clusters[cid].length + 0.6) + 14 * px;
      const ent0 = entBy[cid];
      const lblW = ((ent0 ? ent0.name.length : 9) + 3) * 8 * px;
      const boxW = Math.max(r * 2 + PAD, lblW), boxH = r * 2 + PAD + LABEL;
      if (cx0 + boxW > W && cx0 > 0) { cx0 = 0; cy0 += rowH; rowH = 0; }
      anchors[cid] = { x: cx0 + boxW / 2, y: cy0 + LABEL + r + PAD / 2, r };
      cx0 += boxW; rowH = Math.max(rowH, boxH);
      usedW = Math.max(usedW, cx0);
    });
    const usedH = cy0 + rowH + PAD;
    const scale = Math.min(1.45, (H - 12 * px) / usedH, (W - 12 * px) / usedW);
    Object.values(anchors).forEach(a => { a.x *= scale; a.y *= scale; a.s = scale; });

    // phyllotaxis spiral per cluster: biggest tables in the middle, deterministic
    order.forEach(cid => {
      const list = clusters[cid].sort((a, b) => b.deg - a.deg);
      const a0 = anchors[cid];
      const c = 12 * px * (anchors[cid].s || 1);
      list.forEach((n, i) => {
        const ang = i * 2.39996, r = c * Math.sqrt(i + 0.6);
        n.x = a0.x + Math.cos(ang) * r;
        n.y = a0.y + Math.sin(ang) * r;
        n.cluster = cid;
        nodes.push(n); byN[n.id] = n;
      });
    });

    let hover = null, showPlace = false, hoverLabel = null;
    const labelRects = {};
    function draw() {
      g.clearRect(0, 0, W, H);
      const hovered = hover ? byN[hover] : null;
      const near = {};
      if (hovered) { BY[hover].conns.forEach(c => { near[c.id] = c; }); }
      (showPlace ? EDGES : ID_EDGES).forEach(e => {
        const a = byN[e.a], b = byN[e.b];
        if (!a || !b) return;
        const sameCluster = a.cluster === b.cluster;
        const hot = hovered && (e.a === hover || e.b === hover);
        g.strokeStyle = TIER_COLOR[e.tier] || '#9aa5b3';
        g.globalAlpha = hot ? 0.9 : (hovered ? 0.02 : (e.tier === 'location' ? 0.04 : (sameCluster ? 0.05 : 0.14)));
        g.lineWidth = hot ? 1.6 * px : (sameCluster ? 0.5 : 0.8) * px;
        g.beginPath(); g.moveTo(a.x, a.y);
        if (sameCluster) { g.lineTo(b.x, b.y); }
        else {
          const mx = (a.x + b.x) / 2, my = (a.y + b.y) / 2 - Math.abs(a.x - b.x) * 0.12;
          g.quadraticCurveTo(mx, my, b.x, b.y);
        }
        g.stroke();
      });
      nodes.forEach(n => {
        const hot = hover === n.id || (hovered && near[n.id]);
        g.globalAlpha = hovered ? (hot ? 1 : 0.14) : 0.92;
        g.fillStyle = colorOfDom(domOf(n.id));
        g.beginPath(); g.arc(n.x, n.y, n.r * (hover === n.id ? 1.4 : 1), 0, 7); g.fill();
      });
      // anchor labels on top
      g.globalAlpha = 1;
      g.textAlign = 'center';
      order.forEach(cid => {
        const a0 = anchors[cid];
        const ent = entBy[cid];
        const lbl = ent ? ent.icon + ' ' + ent.name.replace(/^A /, '') : 'other keys';
        g.font = '600 ' + (12.5 * px) + 'px IBM Plex Sans, sans-serif';
        const w = g.measureText(lbl).width;
        const ext = 12 * px * (a0.s || 1) * Math.sqrt(clusters[cid].length + 0.6) + 16 * px;
        const ly = a0.y - ext - 6 * px;
        labelRects[cid] = { x: a0.x - w / 2 - 8 * px, y: ly - 12 * px, w: w + 16 * px, h: 18 * px };
        g.fillStyle = 'rgba(11,14,19,0.78)';
        g.fillRect(a0.x - w / 2 - 8 * px, ly - 12 * px, w + 16 * px, 18 * px);
        g.fillStyle = hoverLabel === cid ? '#ffffff' : '#c8ced5';
        g.fillText(lbl, a0.x, ly + 2 * px);
      });
      g.textAlign = 'left';
      if (hovered) {
        g.font = (12 * px) + 'px IBM Plex Sans, sans-serif';
        const tx = labelOf(hover) + ' · ' + BY[hover].conns.filter(c => c.tier !== 'location').length + ' ID joins';
        const tw = g.measureText(tx).width;
        const lx = Math.min(hovered.x + 12 * px, W - tw - 10 * px), ly = hovered.y - 12 * px;
        g.fillStyle = 'rgba(11,14,19,0.85)'; g.fillRect(lx - 5 * px, ly - 13 * px, tw + 10 * px, 19 * px);
        g.fillStyle = '#e8eaed'; g.fillText(tx, lx, ly);
      }
      document.getElementById('map-status').textContent = hovered
        ? labelOf(hover) + ' — click to open it in the pivot'
        : nodes.length + ' joined tables in ' + order.length + ' neighborhoods · ' + (TABLES.length - nodes.length) + ' tables with no ID join are not drawn · arcs = bridges between neighborhoods';
    }
    draw();
    cv.addEventListener('mousemove', ev => {
      const rect = cv.getBoundingClientRect();
      const mx = (ev.clientX - rect.left) * px, my = (ev.clientY - rect.top) * px;
      let best = null, bd = 18 * px;
      nodes.forEach(n => { const d = Math.hypot(n.x - mx, n.y - my); if (d < bd + n.r) { bd = d; best = n.id; } });
      let lblHit = null;
      if (!best) {
        Object.keys(labelRects).forEach(cid => {
          const r = labelRects[cid];
          if (mx >= r.x && mx <= r.x + r.w && my >= r.y && my <= r.y + r.h) lblHit = cid;
        });
      }
      if (best !== hover || lblHit !== hoverLabel) { hover = best; hoverLabel = lblHit; draw(); }
      cv.style.cursor = (best || (lblHit && lblHit !== 'other')) ? 'pointer' : 'default';
    });
    cv.addEventListener('mouseleave', () => { hover = null; draw(); });
    cv.addEventListener('click', () => {
      if (hover) { openPivot(hover); return; }
      if (hoverLabel && hoverLabel !== 'other' && window.__openThing) { show('things'); window.__openThing(hoverLabel); }
    });
    document.getElementById('map-place').addEventListener('change', ev => { showPlace = ev.target.checked; draw(); });
    const filt = document.getElementById('map-find');
    filt.addEventListener('input', () => {
      const q = filt.value.trim().toLowerCase();
      hover = null;
      if (q) { const hit = nodes.find(n => (n.id + ' ' + labelOf(n.id) + ' ' + rawLabel(n.id)).toLowerCase().includes(q)); if (hit) hover = hit.id; }
      draw();
    });
    const doms2 = {};
    nodes.forEach(n => { const d = domOf(n.id); doms2[d] = (doms2[d] || 0) + 1; });
    const lg = document.getElementById('map-legend');
    lg.innerHTML = '';
    Object.entries(doms2).sort((a, b) => b[1] - a[1]).forEach(([d, n]) => {
      const s = document.createElement('span');
      s.style.cssText = 'display:inline-flex;align-items:center;gap:6px;font-size:11px;color:#c8ced5;margin-right:14px;';
      s.innerHTML = '<span style="width:8px;height:8px;border-radius:50%;background:' + colorOfDom(d) + '"></span>' + d + ' (' + n + ')';
      lg.appendChild(s);
    });
  }

  /* ---------- ROUTES ---------- */
  let routesInit = false;
  function adjacency(usePlace) {
    const adj = {};
    (usePlace ? EDGES : ID_EDGES).forEach(e => {
      (adj[e.a] = adj[e.a] || []).push({ to: e.b, e });
      (adj[e.b] = adj[e.b] || []).push({ to: e.a, e });
    });
    return adj;
  }
  function shortestPath(adj, a, b, banned) {
    const prev = { [a]: null }; const q = [a];
    while (q.length) {
      const n = q.shift();
      if (n === b) break;
      (adj[n] || []).forEach(({ to, e }) => {
        const ek = e.a + '|' + e.b;
        if (banned && banned[ek]) return;
        if (!(to in prev)) { prev[to] = { n, e }; q.push(to); }
      });
    }
    if (!(b in prev)) return null;
    const path = []; let cur = b;
    while (prev[cur]) { path.unshift({ from: prev[cur].n, to: cur, e: prev[cur].e }); cur = prev[cur].n; }
    return path;
  }
  function widestPath(adj, a, b) {
    // maximise the weakest link's pct; place joins count as 0
    const best = { [a]: Infinity }; const prev = {}; const done = {};
    for (;;) {
      let n = null, bw = -1;
      Object.keys(best).forEach(k => { if (!done[k] && best[k] > bw) { bw = best[k]; n = k; } });
      if (n === null) break;
      if (n === b) break;
      done[n] = 1;
      (adj[n] || []).forEach(({ to, e }) => {
        const w = Math.min(best[n], e.pct == null ? 0 : e.pct);
        if (!(to in best) || w > best[to]) { best[to] = w; prev[to] = { n, e }; }
      });
    }
    if (!(b in best)) return null;
    const path = []; let cur = b;
    while (prev[cur]) { path.unshift({ from: prev[cur].n, to: cur, e: prev[cur].e }); cur = prev[cur].n; }
    return path.length ? path : null;
  }
  function weakestOf(path) {
    return path.reduce((m, s) => { const p = s.e.pct == null ? 0 : s.e.pct; return m == null || p < m ? p : m; }, null);
  }
  function findRoutes(a, b, usePlace) {
    const adj = adjacency(usePlace);
    const first = shortestPath(adj, a, b, null);
    if (!first) return [];
    const routes = [first];
    const seen = { [first.map(s => s.e.a + '|' + s.e.b).join('>')]: 1 };
    const wide = widestPath(adj, a, b);
    if (wide) {
      const key = wide.map(s => s.e.a + '|' + s.e.b).join('>');
      if (!seen[key]) { seen[key] = 1; routes.push(wide); }
    }
    for (const step of first) {
      if (routes.length >= 3) break;
      const alt = shortestPath(adj, a, b, { [step.e.a + '|' + step.e.b]: 1 });
      if (alt) {
        const key = alt.map(s => s.e.a + '|' + s.e.b).join('>');
        if (!seen[key]) { seen[key] = 1; routes.push(alt); }
      }
    }
    routes.sort((x, y) => weakestOf(y) - weakestOf(x) || x.length - y.length);
    return routes;
  }
  function routeCard(path, idx) {
    const weakest = path.reduce((m, s) => s.e.pct != null && (m == null || s.e.pct < m) ? s.e.pct : m, null);
    const hasPlace = path.some(s => s.e.tier === 'location');
    let html = '<div style="border:1px solid rgba(255,255,255,0.08);border-radius:12px;background:#10161d;padding:14px 16px;margin-top:12px;">';
    html += '<div style="display:flex;flex-wrap:wrap;align-items:center;gap:8px;">';
    html += '<span style="font-weight:600;color:#e8eaed;font-size:13px;">' + short(path[0].from) + '</span>';
    path.forEach(s => {
      const col = TIER_COLOR[s.e.tier] || '#9aa5b3';
      html += '<span style="font-family:monospace;font-size:10.5px;color:' + col + ';" title="' + TIER_WORD[s.e.tier] + '">—' + (s.e.jk || 'place') + (s.e.pct != null ? ' ' + s.e.pct + '%' : '') + '→</span>';
      html += '<span style="font-weight:600;color:#e8eaed;font-size:13px;cursor:pointer;text-decoration:underline dotted #4c9aff;" onclick="window.__openPivotFromExplorer(\'' + s.to + '\')">' + short(s.to) + '</span>';
    });
    html += '</div>';
    html += '<div style="display:flex;align-items:baseline;gap:14px;font-size:11.5px;color:#9aa5b3;margin-top:8px;">' + '<span>' + path.length + (path.length === 1 ? ' hop' : ' hops')
      + (weakest != null ? ' · weakest link ' + weakest + '%' : '')
      + (hasPlace ? ' · <span style="color:#3fb950">uses a place join — same location, never same thing</span>' : '') + '</span>'
      + '<span onclick="window.__copySQL(' + idx + ', event)" style="margin-left:auto;font-size:11px;color:#9fc4f5;border:1px solid rgba(76,154,255,0.35);border-radius:999px;padding:3px 11px;cursor:pointer;">copy the SQL</span>'
      + '</div></div>';
    return html;
  }
  let lastRoutes = [];
  function sqlOf(path) {
    const lines = [];
    const weakest = path.reduce((m, s) => { const p = s.e.pct == null ? 0 : s.e.pct; return m == null || p < m ? p : m; }, null);
    lines.push('-- route: ' + short(path[0].from) + ' -> ' + short(path[path.length - 1].to) + (weakest != null ? ' · weakest link ' + weakest + '%' : ''));
    path.forEach((s, i) => {
      lines.push('-- hop ' + (i + 1) + ': ' + (s.e.jk || 'place') + (s.e.pct != null ? ' · ' + s.e.pct + '%' : '') + ' · ' + (TIER_WORD[s.e.tier] || s.e.tier));
      if (s.e.note) lines.push('-- \u26a0 ' + s.e.note);
      if (s.e.norm) lines.push('-- \u26a0 normalize first: ' + s.e.norm);
    });
    const fqn = id => (SCHEMA_X[id] || {}).fqn || id;
    const col = (edge, id) => (edge.cols && edge.cols[id]) || null;
    lines.push('SELECT *');
    lines.push('FROM ' + fqn(path[0].from) + ' t0');
    path.forEach((s, i) => {
      const ca = col(s.e, s.from), cb = col(s.e, s.to);
      const jk = s.e.jk || '';
      if (!ca || !cb || jk.indexOf('~') >= 0) {
        lines.push('-- \u26a0 hop ' + (i + 1) + ' is a ' + (jk.indexOf('~') >= 0 ? 'translation (' + jk + ') — two different ID systems' : 'join with no recorded columns'));
        lines.push('-- \u26a0 route it through the crosswalk table; the columns below are NOT real:');
        lines.push('-- JOIN ' + fqn(s.to) + ' t' + (i + 1) + ' ON t' + i + '.<' + jk + '> = t' + (i + 1) + '.<' + jk + '>');
      } else {
        lines.push('JOIN ' + fqn(s.to) + ' t' + (i + 1)
          + ' ON t' + i + '.' + ca + ' = t' + (i + 1) + '.' + cb);
      }
    });
    lines.push(';');
    return lines.join('\n');
  }
  function copyText(txt, btn) {
    const done = () => { if (btn) { const was = btn.textContent; btn.textContent = 'copied \u2713'; setTimeout(() => { btn.textContent = was; }, 1400); } };
    if (navigator.clipboard && navigator.clipboard.writeText) { navigator.clipboard.writeText(txt).then(done, () => fallbackCopy(txt, done)); }
    else fallbackCopy(txt, done);
  }
  function fallbackCopy(txt, done) {
    const ta = document.createElement('textarea');
    ta.value = txt; ta.style.position = 'fixed'; ta.style.opacity = '0';
    document.body.appendChild(ta); ta.select();
    try { document.execCommand('copy'); } catch (e) {}
    document.body.removeChild(ta); done();
  }
  window.__copySQL = function (i, ev) {
    if (ev && ev.stopPropagation) ev.stopPropagation();
    if (lastRoutes[i]) copyText(sqlOf(lastRoutes[i]), ev && ev.target);
  };
  function initRoutes() {
    if (routesInit) return; routesInit = true;
    const dl = document.getElementById('route-tables');
    TABLES.slice().sort((a, b) => b.conns.length - a.conns.length).forEach(t => {
      const o = document.createElement('option'); o.value = t.id; o.label = labelOf(t.id); dl.appendChild(o);
    });
    const go = () => {
      let a = document.getElementById('route-a').value.trim().toUpperCase();
      let b = document.getElementById('route-b').value.trim().toUpperCase();
      const usePlace = document.getElementById('route-place').checked;
      const out = document.getElementById('route-out');
      const resolve = q => {
        if (BY[q]) return q;
        const ql = q.toLowerCase().trim();
        if (!ql) return null;
        const exact = TABLES.filter(tb => labelOf(tb.id).toLowerCase() === ql || rawLabel(tb.id).toLowerCase() === ql);
        if (exact.length) return exact[0].id;
        const hits = TABLES.filter(tb => (labelOf(tb.id) + ' ' + rawLabel(tb.id) + ' ' + tb.id).toLowerCase().includes(ql));
        return hits.length === 1 ? hits[0].id : null;
      };
      const ra = resolve(a) || resolve(document.getElementById('route-a').value.trim());
      const rb = resolve(b) || resolve(document.getElementById('route-b').value.trim());
      if (!ra || !rb) { out.innerHTML = '<div style="color:#c98b86;font-size:13px;margin-top:12px;">could not pin both ends to one table — type more of the name, or pick from the list</div>'; return; }
      a = ra; b = rb;
      setHash('#route=' + a + '..' + b);
      const routes = findRoutes(a, b, usePlace);
      if (!routes.length) {
        out.innerHTML = '<div style="color:#c98b86;font-size:13px;margin-top:12px;">no route on ID joins' + (usePlace ? ' or place' : '') + ' — ' + (usePlace ? 'these two live on different islands' : 'try allowing place joins') + '</div>';
        return;
      }
      lastRoutes = routes;
      out.innerHTML = routes.map((r, i) => routeCard(r, i)).join('') +
        '<div style="font-size:11px;color:#8a95a3;margin-top:10px;">strongest weakest-link first · a 0% link means the overlap is a handful of rows — real, rarely usable</div>';
    };
    document.getElementById('route-go').addEventListener('click', go);
    ['route-a', 'route-b'].forEach(id => document.getElementById(id).addEventListener('keydown', e => { if (e.key === 'Enter') go(); }));
    document.getElementById('route-swap').addEventListener('click', () => {
      const A = document.getElementById('route-a'), B = document.getElementById('route-b');
      const t = A.value; A.value = B.value; B.value = t;
    });
  }
  window.__openPivotFromExplorer = openPivot;
  window.__routeFrom = function (id) {
    show('routes'); initRoutes();
    const A = document.getElementById('route-a');
    if (A) { A.value = id; A.focus(); }
  };

  /* ---------- TRAILS ---------- */
  const TRAILS = [
    {
      title: 'Drug money to the prescription pad',
      why: 'The classic conflict-of-interest walk: who paid the doctor, and what did the doctor go on to prescribe.',
      steps: [
        { from: 'FED_CMS_OPEN_PAYMENTS', to: 'FED_CMS_NPPES', jk: 'NPI', why: 'Every payment a drug or device maker made to a provider carries the provider’s NPI. Same NPI, same doctor — the registry gives the name, address and specialty.' },
        { from: 'FED_CMS_NPPES', to: 'FED_CMS_PARTD_PRESCRIBER_DRUG', jk: 'NPI', why: 'The same NPI keys the Part D file: what that doctor prescribed under Medicare, drug by drug, year by year.' },
      ],
    },
    {
      title: 'Factory to its rap sheet',
      why: 'From a plant reporting toxic releases to its full inspection and enforcement history.',
      steps: [
        { from: 'FED_EPA_TRI_FACILITY', to: 'FED_EPA_FRS_FRS_FACILITIES', jk: 'FRS_ID', why: 'The toxics-release facility carries an EPA registry id — 99.9% of them resolve into the EPA’s master facility registry. This edge is the one pass 1 wrongly called dead.' },
        { from: 'FED_EPA_FRS_FRS_FACILITIES', to: 'FED_EPA_ECHO', jk: 'FRS_ID', why: 'The same registry id keys ECHO: inspections, violations and enforcement actions against that exact site.' },
      ],
    },
    {
      title: 'A donor’s check to the war chest',
      why: 'One person’s contribution, followed through the committee to the candidate and their money summary.',
      steps: [
        { from: 'FED_FEC_INDIV_CONTRIBUTIONS', to: 'FED_FEC_BULK_COMMITTEES', jk: 'FEC_CMTE_ID', why: 'Every itemized individual contribution names the committee it went to.' },
        { from: 'FED_FEC_BULK_COMMITTEES', to: 'FED_FEC_BULK_CANDIDATES', jk: 'FEC_CAND_ID', why: 'A campaign committee declares the candidate it backs.' },
        { from: 'FED_FEC_BULK_CANDIDATES', to: 'FED_FEC_BULK_SUMMARY', jk: 'FEC_CAND_ID', why: 'The candidate id keys the financial summary: total raised, spent, cash on hand.' },
      ],
    },
  ];
  function edgeOf(a, b, jk) {
    const t = BY[a]; if (!t) return null;
    return t.conns.find(c => c.id === b && c.jk === jk) || t.conns.find(c => c.id === b) || null;
  }
  window.__copyTrailSQL = function (i, ev) {
    if (ev && ev.stopPropagation) ev.stopPropagation();
    const tr = TRAILS[i]; if (!tr) return;
    const path = tr.steps.map(s => {
      const c = edgeOf(s.from, s.to, s.jk) || {};
      const cols = {}; cols[s.from] = c.lc || s.jk; cols[s.to] = c.rc || s.jk;
      return { from: s.from, to: s.to, e: { jk: s.jk, pct: c.pct, tier: c.tier || 'measured', cols, note: c.note || '', norm: c.norm || '' } };
    });
    copyText(sqlOf(path), ev && ev.target);
  };
  let trailsInit = false;
  function initTrails() {
    if (trailsInit) return; trailsInit = true;
    const host = document.getElementById('trails-host');
    host.innerHTML = TRAILS.map(tr => {
      let html = '<div style="border:1px solid rgba(255,255,255,0.08);border-radius:14px;background:#10161d;padding:18px 20px;margin-top:16px;">';
      html += '<div style="font-size:16px;font-weight:600;color:#e8eaed;">' + tr.title + '</div>';
      html += '<div style="font-size:12.5px;color:#9aa5b3;margin-top:4px;">' + tr.why + '</div>';
      tr.steps.forEach((s, i) => {
        const e = edgeOf(s.from, s.to, s.jk);
        const col = e ? (TIER_COLOR[e.tier] || '#9aa5b3') : '#e5534b';
        html += '<div style="display:flex;gap:12px;margin-top:14px;">';
        html += '<div style="font-family:monospace;font-size:11px;color:' + col + ';white-space:nowrap;padding-top:2px;">' + (i + 1) + ' · ' + s.jk + (e && e.pct != null ? ' · ' + e.pct + '%' : '') + '</div>';
        html += '<div><div style="font-size:13px;color:#e8eaed;"><span style="cursor:pointer;text-decoration:underline dotted #4c9aff;" onclick="window.__openPivotFromExplorer(\'' + s.from + '\')">' + short(s.from) + '</span> → <span style="cursor:pointer;text-decoration:underline dotted #4c9aff;" onclick="window.__openPivotFromExplorer(\'' + s.to + '\')">' + short(s.to) + '</span>'
          + (e ? ' <span style="font-size:10.5px;color:' + col + ';">' + TIER_WORD[e.tier] + '</span>' : ' <span style="font-size:10.5px;color:#e5534b;">edge missing from payload — do not trust this step</span>') + '</div>';
        html += '<div style="font-size:12px;line-height:1.55;color:#a4aeba;margin-top:3px;max-width:78ch;">' + s.why + '</div></div></div>';
      });
      html += '<div style="margin-top:12px;"><span onclick="window.__copyTrailSQL(' + TRAILS.indexOf(tr) + ', event)" style="font-size:11px;color:#9fc4f5;border:1px solid rgba(76,154,255,0.35);border-radius:999px;padding:3px 11px;cursor:pointer;">copy the SQL</span></div>';
      html += '</div>';
      return html;
    }).join('') + '<div style="font-size:11px;color:#8a95a3;margin-top:14px;">every % is a measured overlap from the join map — click any table name to open it in the pivot</div>';
  }


  /* ---------- THINGS: pick a thing in the world, see everything known about it ---------- */
  const ENTITIES = [
    { id: 'doctor', icon: '🩺', name: 'A doctor', keys: ['NPI', 'PECOS_ENRLMT', 'PECOS_PAC'], blurb: 'who they are, who paid them, what they prescribed, were they excluded' },
    { id: 'hospital', icon: '🏥', name: 'A hospital or clinic', keys: ['CCN', 'CCN~NPI', 'CHAIN_ID', 'BHCMIS'], blurb: 'quality, penalties, cost reports, ownership chains' },
    { id: 'company', icon: '🏢', name: 'A company', keys: ['EIN', 'UEI', 'DUNS', 'CAGE', 'LEI', 'CIK', 'CIK~EIN', 'EIN~UEI', 'DUNS~UEI', 'COMPANY_NO', 'OSHA_EST_ID', 'OFAC_ENT_NUM', 'SEC_SERIES_ID'], blurb: 'taxes, contracts, SEC filings, injuries, sanctions, global ownership' },
    { id: 'bank', icon: '🏦', name: 'A bank or lender', keys: ['FDIC_CERT', 'RSSD', 'RSSD_HC', 'NCUA_CHARTER', 'HMDA_ARID'], blurb: 'branches, failures, holding companies, mortgages — HMDA_ARID is unreliable, use the LEI crosswalk' },
    { id: 'politician', icon: '🗳️', name: 'A politician', keys: ['BIOGUIDE', 'ICPSR', 'FEC_CAND_ID'], blurb: 'votes, bills, committees, campaign money' },
    { id: 'committee', icon: '💰', name: 'A campaign committee', keys: ['FEC_CMTE_ID'], blurb: 'who gave, who got, committee-to-committee flows' },
    { id: 'factory', icon: '🏭', name: 'A factory or site', keys: ['FRS_ID', 'NPDES_ID', 'NRC_SEQ'], blurb: 'toxic releases, permits, inspections, enforcement' },
    { id: 'utility', icon: '⚡', name: 'A power plant or utility', keys: ['EIA_UTILITY_ID', 'EIA_PLANT_ID'], blurb: 'generation, fuel, ownership' },
    { id: 'water', icon: '💧', name: 'A water system', keys: ['PWSID'], blurb: 'violations, enforcement, who drinks from it' },
    { id: 'mine', icon: '⛏️', name: 'A mine', keys: ['MINE_ID'], blurb: 'accidents, violations, operators' },
    { id: 'vessel', icon: '🚢', name: 'A ship, plane or railroad', keys: ['IMO', 'CALLSIGN', 'N_NUMBER', 'RR_CODE'], blurb: 'vessels, aircraft, rail accidents' },
    { id: 'court', icon: '⚖️', name: 'A judge or court case', keys: ['CL_PERSON_ID', 'CL_COURT_ID', 'DOCKET'], blurb: 'dockets, opinions, financial disclosures — DOCKET is the one unreliable key' },
    { id: 'detention', icon: '🔒', name: 'A detention facility', keys: ['ICE_FACILITY'], blurb: 'stints, outcomes, facility codes' },
    { id: 'drug', icon: '💊', name: 'A drug', keys: ['NDC9'], blurb: 'price vs the FDA directory — pad to 5-4 first' },
    { id: 'device', icon: '🦾', name: 'A medical device', keys: ['UDI_DI'], blurb: 'device registry and identifiers' },
    { id: 'award', icon: '📜', name: 'A federal award', keys: ['PIID', 'FAIN', 'AWARD_KEY', 'NIH_PROJECT'], blurb: 'contracts, grants, research projects' },
    { id: 'place', icon: '📍', name: 'A place', keys: [], place: true, blurb: 'every table with a value-checked state, county, ZIP or address column' },
  ];
  // table -> keys it speaks (from its ID edges); key -> tables
  const tableKeys = {}; const keyTables = {};
  TABLES.forEach(tb => tb.conns.forEach(c => {
    if (c.tier === 'location' || !c.jk) return;
    (tableKeys[tb.id] = tableKeys[tb.id] || {})[c.jk] = 1;
    (tableKeys[c.id] = tableKeys[c.id] || {})[c.jk] = 1;
    (keyTables[c.jk] = keyTables[c.jk] || {})[tb.id] = 1;
    (keyTables[c.jk] = keyTables[c.jk] || {})[c.id] = 1;
  }));
  const SCHEMA_X = window.HANDBOOK_SCHEMA || {};
  function entTables(ent) {
    if (ent.place) {
      return TABLES.filter(tb => (SCHEMA_X[tb.id] || {}).place && SCHEMA_X[tb.id].place.some(p => !p.trap)).map(tb => tb.id);
    }
    const s = {};
    ent.keys.forEach(k => Object.keys(keyTables[k] || {}).forEach(id => { s[id] = 1; }));
    return Object.keys(s);
  }
  function entOf(key) { return ENTITIES.find(en => en.keys.indexOf(key) >= 0); }
  let thingsInit = false;
  function initThings() {
    if (thingsInit) return; thingsInit = true;
    renderCards();
  }
  function renderCards() {
    const host = document.getElementById('things-host');
    host.innerHTML = '<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px;">'
      + ENTITIES.map(ent => {
        const n = entTables(ent).length;
        return '<div onclick="window.__openThing(\'' + ent.id + '\')" style="border:1px solid rgba(255,255,255,0.08);border-radius:14px;background:#10161d;padding:16px 18px;cursor:pointer;" '
          + 'onmouseover="this.style.borderColor=\'rgba(76,154,255,0.5)\'" onmouseout="this.style.borderColor=\'rgba(255,255,255,0.08)\'">'
          + '<div style="font-size:22px;">' + ent.icon + '</div>'
          + '<div style="font-size:15px;font-weight:600;color:#e8eaed;margin-top:6px;">' + ent.name + '</div>'
          + '<div style="font-size:11px;color:#7fb6ff;margin-top:3px;">' + n + ' tables speak its language</div>'
          + '<div style="font-size:11.5px;color:#9aa5b3;margin-top:6px;line-height:1.5;">' + ent.blurb + '</div>'
          + '</div>';
      }).join('') + '</div>';
  }
  window.__openThing = function (id) {
    const ent = ENTITIES.find(en => en.id === id);
    if (!ent) return;
    const ids = entTables(ent);
    // bridges: entities sharing a table that speaks both languages
    const bridge = {};
    if (!ent.place) ids.forEach(tid => {
      Object.keys(tableKeys[tid] || {}).forEach(k => {
        const other = entOf(k);
        if (other && other.id !== ent.id) (bridge[other.id] = bridge[other.id] || { ent: other, via: {}, n: 0 }).via[tid] = 1;
      });
    });
    Object.values(bridge).forEach(b => { b.n = Object.keys(b.via).length; });
    const gloss = META.keys || {};
    const byDom = {};
    ids.forEach(tid => { const d = domOf(tid); (byDom[d] = byDom[d] || []).push(tid); });
    let html = '<div style="display:flex;align-items:baseline;gap:14px;flex-wrap:wrap;">'
      + '<span style="font-size:26px;">' + ent.icon + '</span>'
      + '<h3 style="font-size:20px;margin:0;color:#e8eaed;">' + ent.name + '</h3>'
      + '<span style="font-size:12px;color:#9aa5b3;">' + ids.length + ' tables · ' + ent.blurb + '</span>'
      + '<span onclick="window.__closeThing()" style="margin-left:auto;font-size:12px;color:#9fc4f5;cursor:pointer;border:1px solid rgba(76,154,255,0.35);border-radius:999px;padding:4px 12px;">← all things</span></div>';
    if (!ent.place) {
      html += '<div style="margin-top:10px;display:flex;gap:6px;flex-wrap:wrap;align-items:center;">'
        + '<span style="font-size:10px;letter-spacing:0.1em;text-transform:uppercase;color:#8a95a3;margin-right:4px;">its languages</span>'
        + ent.keys.filter(k => keyTables[k]).map(k => {
          const g = gloss[k] || {};
          return '<span title="' + ((g.name || k) + ' — ' + (g.desc || '')).replace(/"/g, '&quot;') + '" style="font-family:monospace;font-size:10.5px;color:#b07cf0;border:1px solid rgba(176,124,240,0.4);border-radius:999px;padding:3px 9px;">' + k + ' · ' + Object.keys(keyTables[k]).length + '</span>';
        }).join('') + '</div>';
    }
    const bl = Object.values(bridge).sort((a, b) => b.n - a.n);
    if (bl.length) {
      html += '<div style="margin-top:8px;display:flex;gap:6px;flex-wrap:wrap;align-items:center;">'
        + '<span style="font-size:10px;letter-spacing:0.1em;text-transform:uppercase;color:#8a95a3;margin-right:4px;">also appears as</span>'
        + bl.map(b => '<span onclick="window.__openThing(\'' + b.ent.id + '\')" title="' + b.n + ' tables speak both languages — the bridge between these two worlds" style="font-size:11.5px;color:#8fceac;border:1px solid rgba(143,206,172,0.35);border-radius:999px;padding:3px 10px;cursor:pointer;">' + b.ent.icon + ' ' + b.ent.name.toLowerCase() + ' · ' + b.n + '</span>').join('')
        + '</div>';
    }
    Object.entries(byDom).sort((a, b) => b[1].length - a[1].length).forEach(([d, list]) => {
      html += '<div style="margin-top:16px;"><div style="font-size:10.5px;letter-spacing:0.12em;text-transform:uppercase;color:' + colorOfDom(d) + ';">' + d + ' · ' + list.length + '</div>';
      html += '<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:6px;margin-top:6px;">';
      list.sort((a, b) => ((CTX[b] || {}).rows || 0) - ((CTX[a] || {}).rows || 0)).forEach(tid => {
        const ctx = CTX[tid] || {};
        const rows = ctx.rows ? (ctx.rows >= 1e6 ? (ctx.rows / 1e6).toFixed(1) + 'M' : ctx.rows >= 1e3 ? Math.round(ctx.rows / 1e3) + 'k' : ctx.rows) : '';
        const s = SCHEMA_X[tid] || {};
        const notes = s.notes || {};
        const brief = String(notes.grain || s.desc || '').split(/(?<=\.)\s/)[0].slice(0, 110);
        const nPlace = ((s.place || []).filter(p => !p.trap)).length;
        const trapTexts = []
          .concat(notes.note ? [String(notes.note)] : [])
          .concat((s.place || []).filter(p => p.trap && p.note).map(p => p.column + ': ' + p.note))
          .concat((s.time || []).filter(c => c.trap).map(c => c.column + ' looks like a date but is not'));
        const badges = []
          .concat(s.clock ? ['<span style="font-size:9.5px;color:#7fb6ff;">clock</span>'] : [])
          .concat(nPlace ? ['<span style="font-size:9.5px;color:#8fceac;">' + nPlace + ' place</span>'] : [])
          .concat(trapTexts.length ? ['<span style="font-size:9.5px;color:#e5534b;">&#9888; ' + trapTexts.length + (trapTexts.length === 1 ? ' trap' : ' traps') + '</span>'] : []);
        const tip = (rawLabel(tid) + ' · ' + tid + (trapTexts.length ? ' · ' + trapTexts.join(' · ') : '')).replace(/"/g, '&quot;');
        html += '<div onclick="window.__openPivotFromExplorer(\'' + tid + '\')" title="' + tip + '" style="border:1px solid rgba(255,255,255,0.06);border-radius:9px;background:#0e141b;padding:8px 12px;cursor:pointer;" '
          + 'onmouseover="this.style.borderColor=\'rgba(76,154,255,0.5)\'" onmouseout="this.style.borderColor=\'rgba(255,255,255,0.06)\'">'
          + '<div style="display:flex;justify-content:space-between;gap:10px;align-items:baseline;">'
          + '<span style="font-size:12px;color:#e8eaed;">' + labelOf(tid) + '</span>'
          + '<span style="display:flex;gap:8px;align-items:baseline;white-space:nowrap;">' + badges.join('')
          + '<span style="font-family:monospace;font-size:10.5px;color:#8a95a3;">' + rows + '</span>'
          + '<span onclick="event.stopPropagation();window.__routeFrom(\'' + tid + '\')" title="find a route from this table" style="font-size:10px;color:#9fc4f5;border:1px solid rgba(76,154,255,0.3);border-radius:999px;padding:1px 7px;">route &rarr;</span>'
          + '</span></div>'
          + (brief ? '<div style="font-size:10.5px;color:#8a95a3;margin-top:3px;">' + brief.replace(/</g, '&lt;') + '</div>' : '')
          + '</div>';
      });
      html += '</div></div>';
    });
    document.getElementById('things-host').innerHTML = html;
    setHash('#thing=' + id);
    window.scrollTo(0, 0);
  };
  window.__closeThing = renderCards;
  /* ---------- boot ---------- */
  document.getElementById('tab-things').onclick = () => show('things');
  document.getElementById('tab-map').onclick = () => show('map');
  document.getElementById('tab-routes').onclick = () => show('routes');
  document.getElementById('tab-trails').onclick = () => show('trails');
  document.getElementById('tab-pivot').onclick = () => show('pivot');
  applyHash();
})();
