"""
Atlas regression tests.

These exist because a sign error in one line made the cached map and everything
drawn on top of it drift apart as soon as you dragged -- the map looked fine
sitting still and fell apart the moment you used it. Screenshots of a stationary
map will never catch that. These do.

    python -m viz.test_atlas

Needs playwright (`pip install playwright && playwright install chromium`).
"""

from __future__ import annotations

import pathlib
import sys

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "library-atlas.html"

# Read the layout the page itself is using, so the test can work out where a
# given dataset OUGHT to be on screen and check that it really is.
#
# The page thinks in canvas coordinates; Playwright's mouse thinks in viewport
# coordinates, and the two differ by the height of the toolbar. Everything that
# crosses that boundary goes through project()/viewport() below -- getting this
# wrong makes the PAGE look broken when it's the test that's confused.
PROJECT = """([i,lensName])=>{
  const A = window.__atlas, r = document.getElementById('cv').getBoundingClientRect();
  const p = A.pos(lensName)[i];
  return [A.sx(p[0]) + r.left, A.sy(p[1]) + r.top];
}"""

# Viewport point -> the map coordinate under it.
WORLD = """([x,y])=>{
  const r = document.getElementById('cv').getBoundingClientRect();
  return window.__atlas.world(x - r.left, y - r.top);
}"""

CHECKS = []


def check(name):
    def deco(fn):
        CHECKS.append((name, fn))
        return fn
    return deco


def near(pg, lens, name, vx, vy, tol=16):
    """Is `name` close enough to (vx,vy) that picking it was legitimate?

    Dots overlap in the connection view. Two datasets sharing a pixel means
    either answer is correct, and a test that insists on one of them is testing
    the layout's tie-breaking, not whether clicking works.
    """
    if not name:
        return False
    return pg.evaluate("""([lens,name,vx,vy,tol])=>{
      const A=window.__atlas, r=document.getElementById('cv').getBoundingClientRect();
      const i=A.tables.findIndex(t=>t.n===name); if(i<0) return false;
      const p=A.pos(lens)[i];
      return Math.hypot(A.sx(p[0])+r.left-vx, A.sy(p[1])+r.top-vy) <= tol;
    }""", [lens, name, vx, vy, tol])


def drag(pg, x0, y0, dx, dy):
    pg.mouse.move(x0, y0)
    pg.mouse.down()
    # Several steps, so it goes through the same path a real drag does.
    for s in range(1, 6):
        pg.mouse.move(x0 + dx * s / 5, y0 + dy * s / 5)
    pg.mouse.up()
    pg.wait_for_timeout(120)


@check("a click lands on the dataset that is actually under the cursor")
def t_click(pg):
    bad = []
    for lens, key in [("stacks", "1"), ("constellation", "2"), ("refinery", "3")]:
        pg.keyboard.press(key)
        pg.wait_for_timeout(1000)
        for i in (12, 90, 200, 331):
            pg.keyboard.press("Escape")
            pg.wait_for_timeout(340)          # the panel slides out over ~260ms
            x, y = pg.evaluate(PROJECT, [i, lens])
            if not (30 < x < 1450 and 130 < y < 860):
                continue
            pg.mouse.click(x, y)
            pg.wait_for_timeout(160)
            got = pg.inner_text("#panel h3")
            want = pg.evaluate("(i)=>window.__atlas.tables[i].n", i)
            if got != want and not near(pg, lens, got, x, y):
                bad.append(f"{lens}[{i}]: clicked {want}, selected {got or '(nothing)'}")
    return bad


@check("clicks stay accurate after the map has been dragged")
def t_click_after_pan(pg):
    bad = []
    for lens, key in [("stacks", "1"), ("constellation", "2")]:
        pg.keyboard.press(key)
        pg.wait_for_timeout(1000)
        pg.keyboard.press("Escape")
        drag(pg, 700, 430, 163, -97)          # a deliberately awkward offset
        for i in (12, 90, 240):
            pg.keyboard.press("Escape")
            pg.wait_for_timeout(340)          # the panel slides out over ~260ms
            x, y = pg.evaluate(PROJECT, [i, lens])
            if not (30 < x < 1450 and 130 < y < 860):
                continue
            pg.mouse.click(x, y)
            pg.wait_for_timeout(160)
            got = pg.inner_text("#panel h3")
            want = pg.evaluate("(i)=>window.__atlas.tables[i].n", i)
            if got != want and not near(pg, lens, got, x, y):
                bad.append(f"{lens}[{i}] after pan: clicked {want}, selected {got or '(nothing)'}")
        pg.keyboard.press("f")
        pg.wait_for_timeout(200)
    return bad


@check("the cached map and the live layer stay locked together while dragging")
def t_layers_locked(pg):
    """The room the cursor is over must not change identity mid-drag.

    Dragging moves the map under a fixed cursor, so what's beneath the cursor
    changes -- but the two LAYERS must agree at every instant. We check that by
    sampling the same world point before and after a pan and confirming it lands
    exactly where the projection says it should.
    """
    bad = []
    for lens, key in [("stacks", "1"), ("constellation", "2"), ("refinery", "3")]:
        pg.keyboard.press(key)
        pg.wait_for_timeout(1000)
        pg.keyboard.press("f")
        pg.wait_for_timeout(250)
        before = pg.evaluate(PROJECT, [90, lens])
        drag(pg, 700, 430, 137, -89)
        after = pg.evaluate(PROJECT, [90, lens])
        moved = (after[0] - before[0], after[1] - before[1])
        if abs(moved[0] - 137) > 1.5 or abs(moved[1] + 89) > 1.5:
            bad.append(f"{lens}: dragged (137,-89) but the point moved {moved}")
        # And the cached picture must have been offset by the same amount.
        off = pg.evaluate("()=>window.__atlas.cacheOffset()")
        if abs(off[0] - 137) > 1.5 or abs(off[1] + 89) > 1.5:
            bad.append(f"{lens}: cached layer offset {off}, expected (137,-89)")
        pg.keyboard.press("f")
        pg.wait_for_timeout(200)
    return bad


@check("the page never scrolls sideways")
def t_no_scroll(pg):
    bad = []
    for w, h in [(700, 800), (1100, 800), (1500, 900), (1920, 1080)]:
        pg.set_viewport_size({"width": w, "height": h})
        pg.wait_for_timeout(350)
        for state in ("closed", "open"):
            if state == "open":
                pg.fill("#search", "OSHA")
                pg.wait_for_timeout(250)
                pg.keyboard.press("Enter")
                pg.wait_for_timeout(350)
            over = pg.evaluate(
                "()=>[document.documentElement.scrollWidth>document.documentElement.clientWidth,"
                " document.documentElement.scrollLeft, document.body.scrollLeft]")
            if over[0] or over[1] or over[2]:
                bad.append(f"{w}x{h} panel {state}: overflow={over[0]} scrollLeft={over[1]}/{over[2]}")
            pg.keyboard.press("Escape")
            pg.wait_for_timeout(150)
    pg.set_viewport_size({"width": 1500, "height": 900})
    pg.wait_for_timeout(300)
    return bad


@check("zooming keeps the point under the cursor under the cursor")
def t_zoom_anchor(pg):
    bad = []
    pg.keyboard.press("2")
    pg.wait_for_timeout(900)
    pg.keyboard.press("f")
    pg.wait_for_timeout(250)
    ax, ay = 640, 400
    before = pg.evaluate(WORLD, [ax, ay])
    pg.mouse.move(ax, ay)
    for _ in range(4):
        pg.mouse.wheel(0, -220)
    pg.wait_for_timeout(300)
    after = pg.evaluate(WORLD, [ax, ay])
    if abs(after[0] - before[0]) > 1.0 or abs(after[1] - before[1]) > 1.0:
        bad.append(f"point under cursor drifted {before} -> {after}")
    pg.keyboard.press("f")
    return bad


@check("no console errors through a full workout")
def t_no_errors(pg):
    errs = pg.evaluate("()=>window.__errors||[]")
    return errs


def main():
    if not PAGE.exists():
        sys.exit(f"missing {PAGE}")
    failures = 0
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1500, "height": 900})
        pg.add_init_script("window.__errors=[];"
                           "addEventListener('error',e=>window.__errors.push(String(e.message)));")
        pg.on("console", lambda m: pg.evaluate(
            "(t)=>window.__errors.push(t)", m.text) if m.type == "error" else None)
        pg.goto(PAGE.resolve().as_uri())
        pg.wait_for_selector("#legend .row")
        pg.wait_for_timeout(700)
        if not pg.evaluate("()=>!!window.__atlas"):
            sys.exit("the page does not expose window.__atlas -- tests cannot run")
        for name, fn in CHECKS:
            bad = fn(pg) or []
            if bad:
                failures += 1
                print(f"FAIL  {name}")
                for line in bad[:8]:
                    print(f"        {line}")
            else:
                print(f"ok    {name}")
        b.close()
    print()
    print("all checks passed" if not failures else f"{failures} check(s) FAILED")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
