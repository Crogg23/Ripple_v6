/* The Library Atlas — the one JavaScript file, and why it exists.
 *
 * Everything else in this app is Python. This file does the single thing
 * Python cannot do from the server: move 1,043 points smoothly, sixty times
 * a second, in the viewer's browser. Plotly's own frame animation can't
 * tween WebGL traces (they snap), so the morph is done by hand: a
 * requestAnimationFrame loop calling Plotly.restyle on the node trace.
 *
 * THE CHOREOGRAPHY of a lens switch:
 *   1. every trace that isn't the datasets fades out (~150ms) — links,
 *      tiles, pipeline. Lines tweening between topologies read as spaghetti;
 *      nodes flying in silence read as the map re-arguing itself.
 *   2. the 1,043 nodes glide to their new seats (~700ms, eased), while the
 *      camera glides to the new lens's home framing.
 *   3. at the halfway point the markers swap costume — colour, size, shape —
 *      for the new lens.
 *   4. the tween resolves, Dash's server rebuilds the full figure (new
 *      links, new furniture), and it lands exactly where the tween ended,
 *      so the swap is invisible.
 *
 * Dash wiring: this is an async clientside callback. It receives the lens
 * chips' clicks, runs the tween, and only THEN returns the picked lens —
 * which is what triggers the server redraw. The tween is the transition;
 * the server render is the destination.
 */

window.__atlas = { morphing: false, intro: null };
/* eslint-disable no-undef */

const EASE = (s) => (s < 0.5 ? 4 * s * s * s : 1 - Math.pow(-2 * s + 2, 3) / 2);

function graphDiv() {
  const host = document.getElementById("map");
  if (!host) return null;
  return host.classList.contains("js-plotly-plot")
    ? host
    : host.querySelector(".js-plotly-plot");
}

function nodeTraceIndex(gd) {
  return gd.data.findIndex((t) => t.name === "datasets");
}

/* Tween the node trace + camera from where they are to `to`. Resolves when
 * the map has settled. */
function runMorph(gd, tIdx, to) {
  const from = {
    x: Array.from(gd.data[tIdx].x),
    y: Array.from(gd.data[tIdx].y),
    xr: gd.layout.xaxis.range.slice(),
    yr: gd.layout.yaxis.range.slice(),
  };
  const others = gd.data.map((_, i) => i).filter((i) => i !== tIdx);
  const DURATION = 700;
  let swapped = false;

  // 1. everything that isn't a dataset steps aside.
  if (others.length) {
    Plotly.restyle(gd, { opacity: 0 }, others);
  }
  Plotly.relayout(gd, { hovermode: false });

  return new Promise((resolve) => {
    let start = null;
    function frame(now) {
      if (start === null) start = now;
      const s = Math.min(1, (now - start) / DURATION);
      const e = EASE(s);
      const n = from.x.length;
      const xs = new Array(n);
      const ys = new Array(n);
      for (let i = 0; i < n; i++) {
        xs[i] = from.x[i] + (to.x[i] - from.x[i]) * e;
        ys[i] = from.y[i] + (to.y[i] - from.y[i]) * e;
      }
      const patch = { x: [xs], y: [ys] };
      if (!swapped && s >= 0.5) {
        // 3. costume change at the midpoint, folded into the same frame.
        swapped = true;
        patch["marker.color"] = [to.colours];
        patch["marker.size"] = [to.sizes];
        patch["marker.opacity"] = [to.opac];
        patch["marker.symbol"] = to.symbol;
      }
      // One Plotly.update = one render pass per frame. Separate restyle +
      // relayout calls would draw every frame twice.
      Plotly.update(gd, patch, {
        "xaxis.range": [
          from.xr[0] + (to.xrange[0] - from.xr[0]) * e,
          from.xr[1] + (to.xrange[1] - from.xr[1]) * e,
        ],
        "yaxis.range": [
          from.yr[0] + (to.yrange[0] - from.yr[0]) * e,
          from.yr[1] + (to.yrange[1] - from.yr[1]) * e,
        ],
      }, [tIdx]);
      if (s < 1) {
        requestAnimationFrame(frame);
      } else {
        resolve();
      }
    }
    requestAnimationFrame(frame);
  });
}

/* THE CENSUS ROLL — the ~10 second opening. The rooms pour in largest
 * subject first while the counter ticks up to 1,043; it ends on the busiest
 * hub with its dossier open, and the map goes still. Any key or click skips
 * straight to the finished state. The beat is presence: the count going UP. */
function censusRoll(gd, tIdx, lens) {
  const meta = lens.meta;
  const target = lens.subject.opac;
  const reveal = meta.reveal;
  const steps = meta.steps;
  const overlay = document.getElementById("intro");
  const counter = document.getElementById("intro-count");
  const STEP_MS = 260;
  let skip = false;
  const skipNow = () => { skip = true; };
  document.addEventListener("keydown", skipNow, { once: true });
  document.addEventListener("pointerdown", skipNow, { once: true });

  // Curtain up on an empty building: rooms visible, datasets not yet home.
  Plotly.restyle(gd, { "marker.opacity": [target.map(() => 0)] }, [tIdx]);

  return new Promise((resolve) => {
    let step = 0;
    function tick() {
      if (skip) step = steps;
      const shown = target.map((o, i) => (reveal[i] < step ? o : 0));
      const count = reveal.reduce((n, r) => n + (r < step ? 1 : 0), 0);
      Plotly.restyle(gd, { "marker.opacity": [shown] }, [tIdx]);
      if (counter) {
        counter.textContent =
          count > 0 ? `${count.toLocaleString()} datasets` : "";
      }
      if (step < steps) {
        step += 1;
        setTimeout(tick, skip ? 0 : STEP_MS);
      } else {
        Plotly.restyle(gd, { "marker.opacity": [target] }, [tIdx]);
        if (counter) {
          counter.textContent = `${meta.tables.toLocaleString()} datasets · ${meta.links.toLocaleString()} verified links`;
        }
        if (overlay) {
          overlay.style.opacity = "0";
          setTimeout(() => { overlay.style.display = "none"; }, 1000);
        }
        resolve(meta.intro_pick);
      }
    }
    setTimeout(tick, 900); // one beat on the title card first
  });
}

/* Keyboard: 1/2/3 switch lenses, Escape clears the selection. */
document.addEventListener("keydown", (e) => {
  if (e.target && /INPUT|TEXTAREA/.test(e.target.tagName)) return;
  if (e.key >= "1" && e.key <= "3") {
    const chips = document.querySelectorAll("button.chip");
    const chip = chips[Number(e.key) - 1];
    if (chip) chip.click();
  } else if (e.key === "Escape") {
    const x = document.querySelector(".clearbtn");
    if (x) x.click();
  }
});

window.dash_clientside = Object.assign({}, window.dash_clientside, {
  atlas: {
    census_roll: async function (lens) {
      // Fires when the lens store lands at page load; runs exactly once.
      if (window.__atlas.intro !== null || !lens) {
        return window.dash_clientside.no_update;
      }
      window.__atlas.intro = "running";
      // Wait for Plotly to actually mount the figure.
      let gd = null, tIdx = -1;
      for (let tries = 0; tries < 200; tries++) {
        gd = graphDiv();
        tIdx = gd && gd.data ? nodeTraceIndex(gd) : -1;
        if (tIdx >= 0 && gd._fullLayout) break;
        await new Promise((r) => setTimeout(r, 50));
      }
      if (tIdx < 0) {
        window.__atlas.intro = "failed";
        const overlay = document.getElementById("intro");
        if (overlay) overlay.style.display = "none";
        return window.dash_clientside.no_update;
      }
      const pick = await censusRoll(gd, tIdx, lens);
      // Hand the hub to the selection store directly. Returning it through
      // this callback's own output chain (intro-done -> choose -> selected
      // -> figure) proved unreliable -- the renderer dropped the final
      // figure update -- while set_props enters the normal update path.
      window.dash_clientside.set_props("selected", { data: pick });
      window.__atlas.intro = "done";
      return true;
    },

    switch_lens: async function (nClicks, current, lens) {
      const ctx = window.dash_clientside.callback_context;
      const trig = ctx.triggered && ctx.triggered[0];
      // Fires once on page load with zero clicks — that is not a click.
      if (!trig || !trig.value) return window.dash_clientside.no_update;
      const picked = JSON.parse(trig.prop_id.split(".")[0]).value;
      if (picked === current || window.__atlas.morphing ||
          window.__atlas.intro === "running") {
        return window.dash_clientside.no_update;
      }
      const gd = graphDiv();
      const tIdx = gd && gd.data ? nodeTraceIndex(gd) : -1;
      if (tIdx < 0) return picked; // no figure yet: hard switch is honest
      window.__atlas.morphing = true;
      try {
        await runMorph(gd, tIdx, lens[picked]);
      } finally {
        window.__atlas.morphing = false;
      }
      // 4. hand the destination to the server.
      return picked;
    },
  },
});
