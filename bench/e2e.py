#!/usr/bin/env python
"""
THE BENCH - e2e.py.  The two numbers a human actually feels.

    python bench/e2e.py                print the table
    python bench/e2e.py --runs 11      more samples
    python bench/e2e.py --json out.json

WHY THIS EXISTS SEPARATELY FROM perf.py
---------------------------------------
`perf.py` prices ONE POST at a time. That was the right shape when the whole
screen came back in one callback, because then one POST *was* the gesture. It
is not any more. Since the split, a gesture is:

    1. the browser POSTs `sync_spec`                 (the writer)
    2. `bench-spec` changes, so the browser fans OUT three more POSTs -
       `render_chart`, `render_knobs`, `render_picker` - in parallel

so "how long until the chart is on screen" is *not* any single row in perf.py.
It is step 1 plus whichever part of step 2 carries the figure, with the other
two lanes running alongside and competing for the same server. Timing one POST
in isolation flatters the split; timing the sum of all four slanders it. This
file does neither - it runs the fan-out concurrently, on separate connections,
the way a browser does, and stops the clock the moment the figure is in hand.

WHAT IS MEASURED, EXACTLY
-------------------------
  * CLICK A CHART - clock starts as the `sync_spec` request goes out for a
    picker click, stops when the response containing `bench-figure.figure`
    has been fully read.
  * TURN A KNOB   - same, for one widget moving.

Both are checked, not assumed: every run asserts the figure is really in the
response body and that it has traces or a layout, so a 200 carrying
`no_update` can never be reported as a repaint.

WHAT IT CANNOT SEE
------------------
No browser, so React's own reconcile-and-paint is not in these numbers. What
is in them is everything from "the gesture happened" to "the figure JSON is
back on the client", which is the part this repo controls.

THE SERVER
----------
Started as a subprocess on a spare port, talked to, and then killed BY PID.
There is no image name and no wildcard anywhere in this file.
"""

from __future__ import annotations

import argparse
import json
import os
import statistics
import subprocess
import sys
import tempfile
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from bench import perf  # noqa: E402  - Client, Screen, _body, _wire_values, _kill

KNOB_PATTERN = '{"bench":"knob","part":["ALL"],"path":["ALL"]}'


@dataclass
class Gesture:
    """One thing a human does, timed from the gesture to the figure."""

    name: str
    total_ms: list[float]
    sync_ms: list[float]
    fan_ms: list[float]
    lanes: dict[str, tuple[float, float]]   # lane -> (median ms, KB)
    request_kb: float
    note: str = ""

    def row(self) -> dict:
        return {
            "name": self.name,
            "median_ms": statistics.median(self.total_ms),
            "fast_ms": min(self.total_ms),
            "slow_ms": max(self.total_ms),
            "n": len(self.total_ms),
            "sync_ms": statistics.median(self.sync_ms),
            "fanout_to_figure_ms": statistics.median(self.fan_ms),
            "request_kb": self.request_kb,
            "lanes": {k: {"ms": v[0], "kb": v[1]} for k, v in self.lanes.items()},
            "note": self.note,
        }


class Browser:
    """Four keep-alive connections: one for the writer, three for the lanes.

    A real browser holds several sockets to one origin and fires the fan-out
    down them at once. One socket would serialise the three lanes and turn a
    parallel fan-out into a queue, which would measure something this app does
    not do.
    """

    def __init__(self, host: str, port: int):
        self.sync = perf.Client(host, port)
        self.lanes = {name: perf.Client(host, port)
                      for name in ("chart", "knobs", "picker")}

    def close(self) -> None:
        self.sync.close()
        for client in self.lanes.values():
            client.close()


def _post(client: perf.Client, payload: bytes) -> tuple[dict, float, int]:
    status, body, elapsed = client.request("POST", "/_dash-update-component",
                                           payload)
    if status != 200:
        raise RuntimeError(f"HTTP {status}: {body[:300]!r}")
    return json.loads(body), elapsed, len(body)


def _figure_in(answer: dict) -> bool:
    """Is there a real figure in this response, or just a `no_update`?"""
    slot = (answer.get("response") or {}).get("bench-figure") or {}
    fig = slot.get("figure")
    return isinstance(fig, dict) and ("data" in fig or "layout" in fig)


def _gesture(browser: Browser, sync_payload: bytes,
             lane_payload: dict[str, Any], name: str,
             runs: int, note: str = "") -> Gesture:
    """Fire one gesture `runs` times and time it to the figure.

    `lane_payload[lane]` is a callable taking the sync response and returning
    the bytes for that lane, because two of the three lanes are handed values
    the writer only just produced.
    """
    totals: list[float] = []
    syncs: list[float] = []
    fans: list[float] = []
    per_lane: dict[str, list[tuple[float, float]]] = {k: [] for k in lane_payload}

    for run in range(runs + 1):                 # run 0 is the warm-up
        results: dict[str, tuple[float, float]] = {}
        errors: list[BaseException] = []

        t0 = time.perf_counter()
        answer, sync_elapsed, _n = _post(browser.sync, sync_payload)
        t_sync = time.perf_counter()

        bodies = {lane: build(answer) for lane, build in lane_payload.items()}

        def fire(lane: str) -> None:
            try:
                reply, elapsed, size = _post(browser.lanes[lane], bodies[lane])
                results[lane] = (elapsed, size / 1024.0)
                if lane == "chart":
                    if not _figure_in(reply):
                        raise RuntimeError(
                            f"{name}: no figure in the chart response - "
                            f"{json.dumps(reply)[:200]}")
                    results["__figure_at__"] = (time.perf_counter(), 0.0)
            except BaseException as exc:        # noqa: BLE001 - re-raised below
                errors.append(exc)

        threads = [threading.Thread(target=fire, args=(lane,))
                   for lane in bodies]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        if errors:
            raise errors[0]

        figure_at = results["__figure_at__"][0]
        if run == 0:
            continue
        totals.append((figure_at - t0) * 1000.0)
        syncs.append(sync_elapsed * 1000.0)
        fans.append((figure_at - t_sync) * 1000.0)
        for lane in per_lane:
            per_lane[lane].append(results[lane])

    lanes = {lane: (statistics.median(ms for ms, _kb in samples) * 1000.0,
                    statistics.median(kb for _ms, kb in samples))
             for lane, samples in per_lane.items()}
    return Gesture(name, totals, syncs, fans, lanes,
                   request_kb=len(sync_payload) / 1024.0, note=note)


def run(runs: int = 9) -> tuple[list[Gesture], dict]:
    from bench import app as app_mod

    port = perf._free_port()
    env = dict(os.environ, BENCH_PORT=str(port))
    log_path = Path(tempfile.gettempdir()) / f"bench-e2e-{port}.log"
    log = open(log_path, "w", encoding="utf-8", errors="replace")
    proc = subprocess.Popen([sys.executable, str(_REPO / "bench" / "app.py")],
                            cwd=str(_REPO), env=env, stdout=log,
                            stderr=subprocess.STDOUT)
    browser = Browser("127.0.0.1", port)
    meta = {"port": port, "pid": proc.pid, "runs": runs,
            "when": time.strftime("%Y-%m-%d %H:%M:%S")}

    try:
        t0 = time.perf_counter()
        while time.perf_counter() - t0 < 180:
            if proc.poll() is not None:
                raise RuntimeError(f"the server exited {proc.returncode}, "
                                   f"see {log_path}")
            try:
                status, _b, _e = browser.sync.request("GET", "/")
                if status == 200:
                    break
            except Exception:
                time.sleep(0.25)
        else:
            raise RuntimeError("the server never answered")
        meta["boot_ms"] = (time.perf_counter() - t0) * 1000.0

        screen = perf.Screen(app_mod)          # a lazy first paint, as shipped
        wire = perf._wire_values(app_mod, screen)
        keys = {
            "sync": next(k for k in app_mod.app.callback_map
                         if "bench-knob-msg" in k),
            "chart": next(k for k in app_mod.app.callback_map
                          if "bench-figure" in k),
            "knobs": next(k for k in app_mod.app.callback_map
                          if "bench-knobs.children" in k),
            "picker": next(k for k in app_mod.app.callback_map
                           if "bench-picker.children" in k),
        }

        def lane_bodies():
            """The three render POSTs the browser fires when the spec changes."""
            def build(lane: str):
                def make(answer: dict) -> bytes:
                    got = answer.get("response") or {}
                    spec = (got.get("bench-spec") or {}).get("data")
                    override: dict = {}
                    if spec is not None:
                        override[("bench-spec", "data")] = spec
                    knob_echo = (got.get("bench-knob-echo") or {}).get("data")
                    if knob_echo is not None:
                        override[("bench-knob-echo", "data")] = knob_echo
                    return json.dumps(perf._body(app_mod, keys[lane],
                                                 ["bench-spec.data"], wire,
                                                 override)).encode()
                return make
            return {lane: build(lane) for lane in ("chart", "knobs", "picker")}

        # --- (a) click a chart in the picker -----------------------------
        click = json.dumps(perf._body(
            app_mod, keys["sync"],
            [perf._prop_id({"bench": "chart", "key": "scatter"}, "n_clicks")],
            wire)).encode()
        gestures = [_gesture(browser, click, lane_bodies(), "click a chart",
                             runs,
                             note="bar -> scatter; the pane and the picker DO "
                                  "rebuild, on their own lanes")]

        # --- (b) turn a knob ---------------------------------------------
        values = list(screen.values)
        knob_prop = None
        for i, cid in enumerate(screen.ids):
            if cid.get("path") == "layout.barmode" and cid.get("part") == "value":
                values[i] = "stack"
                knob_prop = perf._prop_id(cid, "value")
                break
        if knob_prop is None:                  # pragma: no cover
            raise RuntimeError("layout.barmode is not on the first paint")
        entries = [{"id": cid, "property": "value", "value": v}
                   for cid, v in zip(screen.ids, values)]
        turn = json.dumps(perf._body(
            app_mod, keys["sync"], [knob_prop], wire,
            {(KNOB_PATTERN, "value"): entries})).encode()
        gestures.append(_gesture(browser, turn, lane_bodies(),
                                 "turn a knob", runs,
                                 note="layout.barmode; pane and picker answer "
                                      "no_update, and still cost a round trip"))

        # --- (b2) the same knob turn with every tier open ----------------
        opened = perf.Screen(app_mod, open_all=True)
        wide = perf._wire_values(app_mod, opened)
        values = list(opened.values)
        for i, cid in enumerate(opened.ids):
            if cid.get("path") == "layout.barmode" and cid.get("part") == "value":
                values[i] = "stack"
                knob_prop = perf._prop_id(cid, "value")
                break
        entries = [{"id": cid, "property": "value", "value": v}
                   for cid, v in zip(opened.ids, values)]
        turn_wide = json.dumps(perf._body(
            app_mod, keys["sync"], [knob_prop], wide,
            {(KNOB_PATTERN, "value"): entries})).encode()

        def wide_lanes():
            base = lane_bodies()

            def build(lane: str):
                def make(answer: dict) -> bytes:
                    got = answer.get("response") or {}
                    spec = (got.get("bench-spec") or {}).get("data")
                    override: dict = {("bench-open", "data"): {
                        "key": app_mod.open_key(opened.spec),
                        "tokens": list(app_mod.ALL_TIERS_OPEN)}}
                    if spec is not None:
                        override[("bench-spec", "data")] = spec
                    knob_echo = (got.get("bench-knob-echo") or {}).get("data")
                    if knob_echo is not None:
                        override[("bench-knob-echo", "data")] = knob_echo
                    return json.dumps(perf._body(app_mod, keys[lane],
                                                 ["bench-spec.data"], wide,
                                                 override)).encode()
                return make
            return {lane: build(lane) for lane in base}

        gestures.append(_gesture(browser, turn_wide, wide_lanes(),
                                 "turn a knob, every tier open", runs,
                                 note="all six buckets expanded - the worst "
                                      "case you can ask this app for"))
    finally:
        browser.close()
        perf._kill(proc)
        log.close()
    return gestures, meta


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Time the two gestures.")
    parser.add_argument("--runs", type=int, default=9)
    parser.add_argument("--json", metavar="PATH")
    args = parser.parse_args(argv)

    gestures, meta = run(args.runs)
    say = perf._say

    say("=" * 100)
    say("THE BENCH - gesture to figure, over real HTTP")
    say("=" * 100)
    say(f"  when {meta['when']}   port {meta['port']}   pid {meta['pid']}   "
        f"boot {meta['boot_ms']:,.0f} ms   n={meta['runs']}")
    say("")
    say("  total = the clock from the gesture leaving to the FIGURE being read"
        " back.")
    say("  It is sync_spec, then the three render lanes fired together on "
        "separate sockets.")
    say("")
    say(f"{'gesture':<34} {'total ms':>9} {'fast':>8} {'slow':>8} {'n':>3} "
        f"{'sync':>7} {'to fig':>7} {'req KB':>8}")
    say("-" * 100)
    for g in gestures:
        r = g.row()
        say(f"{g.name:<34} {r['median_ms']:>9,.1f} {r['fast_ms']:>8,.1f} "
            f"{r['slow_ms']:>8,.1f} {r['n']:>3} {r['sync_ms']:>7,.1f} "
            f"{r['fanout_to_figure_ms']:>7,.1f} {r['request_kb']:>8,.1f}")
    say("")
    say("  the three lanes, each on its own socket (median ms, response KB):")
    for g in gestures:
        parts = "   ".join(f"{lane} {ms:,.1f} ms / {kb:,.1f} KB"
                           for lane, (ms, kb) in g.lanes.items())
        say(f"    {g.name:<32} {parts}")
        say(f"      {g.note}")
    if args.json:
        Path(args.json).write_text(
            json.dumps({"meta": meta, "gestures": [g.row() for g in gestures]},
                       indent=2), encoding="utf-8")
        say(f"\nwrote {args.json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
