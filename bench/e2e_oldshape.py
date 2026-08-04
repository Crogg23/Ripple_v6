"""The same two gestures, against the OLD callback shape, over real HTTP.

A gesture there is TWO sequential POSTs - sync_spec, then the one render_all
that carries every output - so there is no fan-out to overlap and the clock
runs straight through both.
"""
from __future__ import annotations

import json
import os
import statistics
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from pathlib import Path as _Path
_REPO = _Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from bench import perf  # noqa: E402
from bench import e2e  # noqa: E402

from bench import oldshape  # noqa: E402

OLD = oldshape.old
# perf._body reaches for `.app` on the module it is handed.
from types import SimpleNamespace
SHIM = SimpleNamespace(app=OLD)
RUNS = int(os.environ.get("RUNS", "31"))
KNOB = '{"bench":"knob","part":["ALL"],"path":["ALL"]}'


def wire_for(spec, code, echo, ids, values):
    from bench import registry
    return {
        ('{"bench":"chart","key":["ALL"]}', "n_clicks"):
            [{"id": {"bench": "chart", "key": t.key}, "property": "n_clicks",
              "value": 0} for t in registry.TEMPLATES],
        (KNOB, "value"): [{"id": c, "property": "value", "value": v}
                          for c, v in zip(ids, values)],
        ("bench-code-draft", "data"): None,
        ("bench-code", "n_blur"): None,
        ("bench-code", "value"): code,
        ("bench-reset", "n_clicks"): 0,
        ("bench-src-kind", "value"): "demo",
        ("bench-src-demo", "value"): spec["source"].get("name"),
        ("bench-src-run", "n_clicks"): 0,
        ("bench-src-sql", "value"): "",
        ("bench-spec", "data"): spec,
        ("bench-echo", "data"): echo,
        ("bench-picker-search", "value"): "",
        ('{"bench":"panel","part":"search"}', "value"): "",
    }


def main() -> int:
    from bench import app as A

    spec = A.blank_spec()
    df, _meta = A.get_frame(spec["source"])
    cols = A._columns(df)
    pane = A.knob_pane(spec, cols, "", A.ALL_TIERS_OPEN)
    code = A.render_code(spec)
    ids, values = perf._widgets(pane)
    echo = {"code": code, "knobs": A.knob_echo(pane),
            "sig": [spec.get("chart"), cols, False, ""],
            "vals": A.knob_values_signature(spec)}
    wire = wire_for(spec, code, echo, ids, values)

    sync_key = next(k for k in OLD.callback_map if "bench-knob-msg" in k)
    all_key = next(k for k in OLD.callback_map if "bench-figure" in k)

    port = perf._free_port()
    env = dict(os.environ, BENCH_PORT=str(port))
    log_path = Path(tempfile.gettempdir()) / f"bench-old-{port}.log"
    log = open(log_path, "w", encoding="utf-8", errors="replace")
    proc = subprocess.Popen([sys.executable, str(_REPO / "bench" / "oldshape.py")],
                            cwd=str(_REPO), env=env, stdout=log,
                            stderr=subprocess.STDOUT)
    client = perf.Client("127.0.0.1", port)
    lane = perf.Client("127.0.0.1", port)
    try:
        t0 = time.perf_counter()
        while time.perf_counter() - t0 < 180:
            if proc.poll() is not None:
                raise RuntimeError(f"exited {proc.returncode}: "
                                   f"{log_path.read_text()[-2000:]}")
            try:
                if client.request("GET", "/")[0] == 200:
                    break
            except Exception:
                time.sleep(0.25)
        print(f"old-shape server up: pid {proc.pid} port {port} "
              f"({(time.perf_counter() - t0) * 1000:,.0f} ms)")

        def gesture(name, changed, override, note=""):
            sync_body = json.dumps(perf._body(SHIM, sync_key, changed, wire,
                                              override)).encode()
            totals, syncs, renders, sizes = [], [], [], []
            for run in range(RUNS + 1):
                t_start = time.perf_counter()
                answer, sync_ms, _n = e2e._post(client, sync_body)
                got = (answer.get("response") or {})
                ov = {}
                if (got.get("bench-spec") or {}).get("data") is not None:
                    ov[("bench-spec", "data")] = got["bench-spec"]["data"]
                if (got.get("bench-echo") or {}).get("data") is not None:
                    ov[("bench-echo", "data")] = got["bench-echo"]["data"]
                render_body = json.dumps(perf._body(SHIM, all_key,
                                                    ["bench-spec.data"], wire,
                                                    ov)).encode()
                reply, render_ms, size = e2e._post(lane, render_body)
                done = time.perf_counter()
                if not e2e._figure_in(reply):
                    raise RuntimeError(f"{name}: no figure in render_all")
                if run:
                    totals.append((done - t_start) * 1000)
                    syncs.append(sync_ms * 1000)
                    renders.append(render_ms * 1000)
                    sizes.append(size / 1024.0)
            print(f"{name:<30} total {statistics.median(totals):>8.1f} ms  "
                  f"fast {min(totals):>7.1f}  n={len(totals)}   "
                  f"sync {statistics.median(syncs):>7.1f}  "
                  f"render_all {statistics.median(renders):>8.1f} ms / "
                  f"{statistics.median(sizes):>8.1f} KB   "
                  f"req {len(sync_body) / 1024:,.0f} KB  {note}")
            return {"name": name, "median_ms": statistics.median(totals),
                    "fast_ms": min(totals), "n": len(totals),
                    "sync_ms": statistics.median(syncs),
                    "render_all_ms": statistics.median(renders),
                    "render_all_kb": statistics.median(sizes),
                    "request_kb": len(sync_body) / 1024.0}

        rows = []
        rows.append(gesture(
            "click a chart",
            [perf._prop_id({"bench": "chart", "key": "scatter"}, "n_clicks")],
            {}, "bar -> scatter"))

        vals = list(values)
        prop = None
        for i, cid in enumerate(ids):
            if cid.get("path") == "layout.barmode" and cid.get("part") == "value":
                vals[i] = "stack"
                prop = perf._prop_id(cid, "value")
                break
        entries = [{"id": c, "property": "value", "value": v}
                   for c, v in zip(ids, vals)]
        rows.append(gesture("turn a knob", [prop],
                            {(KNOB, "value"): entries}, "layout.barmode"))

        print()
        print("FIDELITY vs the baseline's own rows against the REAL old server:")
        base = {r["name"]: r for r in
                json.load(open(str(_REPO / "bench" / "perf-baseline.json")))["rows"]}
        for mine, theirs in (
                ("click a chart", "POST repaint after a chart pick (render_all)"),
                ("turn a knob", "POST repaint, pane NOT rebuilt (render_all)")):
            got = next(r for r in rows if r["name"] == mine)
            b = base[theirs]
            print(f"  render_all [{mine}]  reconstruction "
                  f"{got['render_all_ms']:>8.1f} ms / {got['render_all_kb']:>8.1f} KB"
                  f"   baseline {b['ms']:>8.1f} ms / {b['kb']:>8.1f} KB")
        for mine, theirs in (("click a chart", "POST pick a chart (sync_spec)"),
                             ("turn a knob", "POST turn a knob (sync_spec)")):
            got = next(r for r in rows if r["name"] == mine)
            b = base[theirs]
            print(f"  sync_spec  [{mine}]  reconstruction "
                  f"{got['sync_ms']:>8.1f} ms / req {got['request_kb']:>6.0f} KB"
                  f"   baseline {b['ms']:>8.1f} ms / {b['note']}")
        Path(_REPO / "bench" / "e2e-before.json").write_text(
            json.dumps(rows, indent=2), encoding="utf-8")
    finally:
        client.close()
        lane.close()
        perf._kill(proc)
        log.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
