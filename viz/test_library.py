"""
Playwright regression checks for the Library Atlas Dash app.

    python -m viz.test_library

Boots the app on a scratch port, drives it in headless Chromium, and checks
the behaviours a refactor is most likely to break: the intro finishing and
being skippable, clicks landing on the right dataset in all three lenses,
the morph settling exactly on the compiled coordinates, the honesty dial
surviving a lens switch, and a clean console.

Pattern follows viz/test_atlas.py: a CHECKS registry and a main(), run as a
module, not collected by pytest.
"""

from __future__ import annotations

import json
import os
import pathlib
import subprocess
import sys
import time

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parents[1]
PORT = 8061
URL = f"http://127.0.0.1:{PORT}"
LIB = json.loads((ROOT / "outputs" / "library.json").read_text(encoding="utf-8"))

CHECKS = []


def check(fn):
    CHECKS.append(fn)
    return fn


def wait_intro(pg):
    for _ in range(60):
        if pg.evaluate("() => window.__atlas && window.__atlas.intro === 'done'"):
            return True
        time.sleep(0.5)
    return False


def settle(pg, seconds=1.5):
    time.sleep(seconds)
    for _ in range(20):
        if not pg.evaluate("() => window.__atlas.morphing"):
            return
        time.sleep(0.25)


def node_positions(pg):
    return pg.evaluate("""() => {
        const gd = document.querySelector('#map .js-plotly-plot');
        const t = gd.data.find(t => t.name === 'datasets');
        return {x: Array.from(t.x), y: Array.from(t.y)};
    }""")


@check
def intro_completes_and_hides(pg, report):
    ok = wait_intro(pg)
    time.sleep(1.5)
    hidden = pg.evaluate(
        "() => document.getElementById('intro').style.display === 'none'")
    picked = pg.text_content("#panel h3")
    report("intro runs to completion", ok)
    report("title card steps aside", hidden)
    report("the busiest hub greets you, dossier open",
           picked == LIB["meta"]["hubs"][0][0], picked)


@check
def click_accuracy_each_lens(pg, report):
    # In each lens, click a specific dataset dead-centre via its compiled
    # coordinates and expect its own dossier.
    target = LIB["meta"]["hubs"][1][0]
    idx = next(i for i, t in enumerate(LIB["tables"]) if t["n"] == target)
    for key, lens in (("1", "subject"), ("2", "connection"), ("3", "journey")):
        pg.keyboard.press("Escape")
        time.sleep(0.5)
        pg.keyboard.press(key)
        settle(pg, 2.0)
        px = pg.evaluate("""(i) => {
            const gd = document.querySelector('#map .js-plotly-plot');
            const t = gd.data.find(t => t.name === 'datasets');
            const xa = gd._fullLayout.xaxis, ya = gd._fullLayout.yaxis;
            const box = gd.getBoundingClientRect();
            return [box.left + gd._fullLayout._size.l + xa.d2p(t.x[i]),
                    box.top + gd._fullLayout._size.t + ya.d2p(t.y[i])];
        }""", idx)
        pg.mouse.click(px[0], px[1])
        time.sleep(1.2)
        got = pg.text_content("#panel h3") if pg.query_selector("#panel h3") else None
        report(f"click lands on the right dataset ({lens})",
               got == target, f"got {got}")


@check
def morph_settles_on_compiled_seats(pg, report):
    pg.keyboard.press("1")
    settle(pg, 2.0)
    pg.keyboard.press("2")
    time.sleep(0.3)
    mid = pg.evaluate("() => window.__atlas.morphing")
    settle(pg, 2.5)
    pos = node_positions(pg)
    want = LIB["positions"]["connection"]
    worst = max(max(abs(pos["x"][i] - want[i][0]), abs(pos["y"][i] - want[i][1]))
                for i in range(len(want)))
    report("morph is actually animating mid-switch", bool(mid))
    report("morph settles on the compiled coordinates (≤0.5px)",
           worst <= 0.5, f"worst drift {worst:.3f}")


@check
def dial_survives_lens_switch(pg, report):
    before = pg.text_content("#dial-count")
    pg.click(".rung >> nth=3")
    time.sleep(1.2)
    dimmed = pg.text_content("#dial-count")
    pg.keyboard.press("3")
    settle(pg, 2.5)
    after = pg.text_content("#dial-count")
    pg.click(".rung >> nth=3")   # restore
    time.sleep(0.8)
    report("honesty dial strips links", dimmed != before, dimmed)
    report("dial setting survives a lens switch", after == dimmed, after)


@check
def dossier_walk(pg, report):
    pg.keyboard.press("2")
    settle(pg, 2.0)
    pg.click("#showme")
    time.sleep(1.2)
    start = pg.text_content("#panel h3")
    has_walk = pg.query_selector("button.walk") is not None
    report("dossier offers a walk", has_walk)
    if has_walk:
        pg.click("button.walk >> nth=0")
        arrived = None
        for _ in range(12):          # panel re-render is a server round-trip
            time.sleep(0.5)
            arrived = (pg.text_content("#panel h3")
                       if pg.query_selector("#panel h3") else None)
            if arrived and arrived != start:
                break
        report("clicking a neighbour walks there",
               arrived is not None and arrived != start, str(arrived))


@check
def page_stays_inside_itself(pg, report):
    over = pg.evaluate(
        "() => document.documentElement.scrollWidth"
        " > document.documentElement.clientWidth")
    report("no horizontal page scroll", not over)


def main():
    env = dict(os.environ, ATLAS_PORT=str(PORT))
    proc = subprocess.Popen([sys.executable, "-m", "viz.library_app"],
                            cwd=ROOT, env=env,
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL)
    fails, errors = [], []
    try:
        time.sleep(5)
        with sync_playwright() as p:
            browser = p.chromium.launch()
            pg = browser.new_page(viewport={"width": 1500, "height": 900})
            pg.on("console", lambda m: errors.append(m.text[:200])
                  if m.type == "error" else None)
            pg.on("pageerror", lambda e: errors.append(f"PAGEERROR: {e}"))
            pg.goto(URL, wait_until="networkidle")
            pg.wait_for_selector("#map .js-plotly-plot", timeout=20000)

            def report(name, ok, detail=""):
                print(f"  {'ok' if ok else 'FAIL'}  {name}"
                      + (f"  ({detail})" if detail and not ok else ""))
                if not ok:
                    fails.append(name)

            for fn in CHECKS:
                fn(pg, report)

            report("no console errors", not errors,
                   "; ".join(errors[:3]))
            browser.close()
    finally:
        proc.kill()

    print()
    if fails:
        raise SystemExit(f"{len(fails)} check(s) failed")
    print("all checks passed")


if __name__ == "__main__":
    main()
